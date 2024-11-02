from flask import Flask, render_template, request, jsonify
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai_api_key = open('OPENAI_API_KEY.env').read()
client = OpenAI(api_key=openai_api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_relevance', methods=['POST'])
def calculate_relevance():
    data = request.json
    job_description = data.get('job_description')
    resume = data.get('resume')

    if not job_description or not resume:
        return jsonify({'error': 'Both job description and resume are required.'}), 400

    prompt = f'''Please calculate relevance percentage between job description & resume attached below. Do so by comparing keywords in the jd and resume. Please start your answer with relevance percentage, then suggest keywords that would improve it and help the resume get through the ATS. :\n\nJob Description:\n{job_description}\n\nResume:\n{resume}'''

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an assistant for matching job descriptions and resumes."},
                      {"role": "user", "content": prompt}],
            max_tokens=500
        )
        answer = response.choices[0].message.content  # Use dot notation
        return jsonify({'Answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_cover_letter', methods=['POST'])
def generate_cover_letter():
    data = request.json
    job_description = data.get('job_description')
    resume = data.get('resume')

    if not job_description or not resume:
        return jsonify({'error': 'Both job description and resume are required.'}), 400

    prompt = f'''Write cover letter based on job description & resume attached below. :\n\nJob Description:\n{job_description}\n\nResume:\n{resume}'''

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an assistant for generating cover letters based on resumes and job descriptions."},
                      {"role": "user", "content": prompt}],
            max_tokens=500
        )
        answer = response.choices[0].message.content  # Use dot notation
        return jsonify({'Answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)