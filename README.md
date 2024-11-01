# Job Help

## Description
Job Help is a web application designed to help job seekers find suitable job opportunities by matching their resumes with job descriptions. The application utilizes the OpenAI API to analyze and compare the content of resumes and job postings, providing users with a match percentage, relevant keywords, and tailored suggestions.

## Features
- **Keyword Matching**: Analyze job descriptions and resumes to identify matching keywords.
- **Match Percentage**: Calculate and display the match percentage between a resume and a job description.
- **Suggestions**: Provide suggestions for improving resumes based on the analyzed job description.

## Technologies Used
- Python
- Flask (for the web application)
- OpenAI API
- HTML/CSS (for the frontend)
- JavaScript (for client-side interactions)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/salmanriazsyed/jobhelp
   cd jobhelp
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Place your OPENAI API key in OPENAI_API_KEY.env and place it in the jobhelp folder.

## Usage
1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000` to access the application.

3. Upload your resume and job description, and click the "Match" button to see the results.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
- [OpenAI](https://openai.com/) for providing the powerful API that enables this project.
- [Flask](https://flask.palletsprojects.com/) for simplifying web application development in Python.