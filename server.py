from flask import Flask, request, jsonify
from Res_pro import ResumeProcessor

app = Flask(__name__)
processor = ResumeProcessor()

@app.route("/process", methods=["POST"])
def process_resume():
    """Receives resume and job description, then calculates match score."""
    job_desc = request.form["job_desc"]
    resume_file = request.files["resume"]

    # Extract text from resume
    resume_text = processor.extract_text(resume_file)

    # Compute match score
    match_score = processor.calculate_match_score(resume_text, job_desc)

    return jsonify({"match_score": match_score})

if __name__ == "__main__":
    app.run(debug=True)
