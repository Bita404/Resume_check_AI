import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
# >>>>>>>>>>  token in is .env file
load_dotenv()
TOKEN = os.getenv("token")


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

class ResumeBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()

        
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.store_job_desc))
        self.application.add_handler(MessageHandler(filters.Document.PDF | filters.Document.DOCX, self.handle_file))

        
        self.user_data = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sends a welcome message."""
        await update.message.reply_text("Hello! Send me a job description first, then upload your resume (PDF/DOCX).")

    async def store_job_desc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stores job description sent by user."""
        user_id = update.message.chat_id
        self.user_data[user_id] = {"job_desc": update.message.text}
        await update.message.reply_text("Job description saved! Now, send your resume.")

    async def handle_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processes resume file and sends it to the backend."""
        user_id = update.message.chat_id
        if user_id not in self.user_data or "job_desc" not in self.user_data[user_id]:
            await update.message.reply_text("Please send a job description before uploading your resume.")
            return  

        file = update.message.document
        file_path = f'./{file.file_name}'
        await file.download_to_drive(file_path)

      
        with open(file_path, "rb") as f:
            files = {"resume": f}
            data = {"job_desc": self.user_data[user_id]["job_desc"]}
            response = requests.post("http://127.0.0.1:5000/process", files=files, data=data)

        #>>>>>>>>>>>> Response 
        if response.status_code == 200:
            match_score = response.json().get("match_score", "N/A")
            await update.message.reply_text(f"Match Score: {match_score}%")
        else:
            await update.message.reply_text("Error processing the resume.")

    def run(self):
        """Starts the bot."""
        print("Bot is running...")
        self.application.run_polling()


if __name__ == "__main__":
    bot = ResumeBot(TOKEN)
    bot.run()
