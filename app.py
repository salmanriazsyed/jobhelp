from flask import Flask, render_template, request, jsonify
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai_api_key = file('OPENAI_API_KEY.env').read()
client = OpenAI(api_key=openai_api_key)

# Function to extract keywords from a text
def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return list(set(words))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    data = request.form
    job_description = data.get('job_description')
    resume = data.get('resume')
    
    if not job_description or not resume:
        return jsonify({'error': 'Both job description and resume are required.'}), 400
    
    # Extract keywords
    job_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume)
    
    # Match keywords
    matching_keywords = set(job_keywords) & set(resume_keywords)
    match_percentage = (len(matching_keywords) / len(job_keywords)) * 100 if job_keywords else 0
    
    # Calculate relevance score and suggestions
    relevance_score, suggestions = calculate_relevance_score(job_description, resume)
    
    return jsonify({
        'match_percentage': round(match_percentage, 2),
        'matching_keywords': list(matching_keywords),
        'relevance_score': relevance_score,
        'suggestions': suggestions
    })

def calculate_relevance_score(job_description, resume):
    prompt = f"Evaluate the relevance of the following resume to this job description. Provide a relevance score between 0 and 100 and list any keywords or phrases that should be added to the resume for better alignment.\n\nJob Description:\n{job_description}\n\nResume:\n{resume}\n\nResponse format: 'Score: X, Suggestions: Y'"
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo",  # Change to gpt-3.5-turbo or any available model
            messages=[{"role": "system", "content": "You are an assistant for matching job descriptions and resumes."},
                      {"role": "user", "content": prompt}],
            prompt=prompt,
            max_tokens=100,
            temperature=0.5
        )
        text = response.choices[0].text.strip()
        score_match = re.search(r'Score:\s*(\d+)', text)
        suggestions_match = re.search(r'Suggestions:\s*(.*)', text)
        
        relevance_score = int(score_match.group(1)) if score_match else None
        suggestions = suggestions_match.group(1).strip() if suggestions_match else None
        return relevance_score, suggestions
    except Exception as e:
        return None, str(e)

@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter():
    data = request.form
    job_description = data.get('job_description')
    resume = data.get('resume')
    
    if not job_description or not resume:
        return jsonify({'error': 'Both job description and resume are required.'}), 400

    prompt = f"Generate a personalized cover letter based on the following job description and resume:\n\nJob Description:\n{job_description}\n\nResume:\n{resume}\n\nCover Letter:"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Change to gpt-3.5-turbo or any available model
            messages=[{"role": "system", "content": "You are an assistant for matching job descriptions and resumes."},
                      {"role": "user", "content": prompt}],
            max_tokens=500
        )
        cover_letter = response.choices[0].text.strip()
        return jsonify({'cover_letter': cover_letter})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
