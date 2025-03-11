import pdfplumber
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class ResumeProcessor:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def extract_text(self, file):
        """Extracts text from a PDF or DOCX file."""
        if file.filename.endswith(".pdf"):
            return self.extract_text_from_pdf(file)
        elif file.filename.endswith(".docx"):
            return self.extract_text_from_docx(file)
        return ""

    def extract_text_from_pdf(self, file):
        """Extracts text from PDF using pdfplumber."""
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    def extract_text_from_docx(self, file):
        """Extracts text from DOCX using python-docx."""
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs]).strip()

    def calculate_match_score(self, resume_text, job_desc):
        """Calculates match score using BERT embeddings."""
        resume_embedding = self.model.encode(resume_text).reshape(1, -1)
        job_embedding = self.model.encode(job_desc).reshape(1, -1)

        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        return round(similarity * 100, 2)
