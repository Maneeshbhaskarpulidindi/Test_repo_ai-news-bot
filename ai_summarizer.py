import os
from dotenv import load_dotenv
#from openai import OpenAI
from groq import Groq  # <-- CHANGED

# Load the API keys from your .env file
load_dotenv()

class AISummarizer:
    def __init__(self):
        # Automatically uses the OPENAI_API_KEY from your .env file
        self.client = Groq()
        # We use gpt-4o-mini because it is incredibly fast and cheap for text processing
        self.model = "openai/gpt-oss-120b"

    def summarize_transcript(self, text, video_title):
        """Sends the transcript to OpenAI to get a clean, readable summary."""
        
        prompt = f"""
        You are an AI news summarizer. I am going to give you the transcript of a recent YouTube video titled "{video_title}".
        Your job is to read it and extract the most important points, announcements, or tutorials.
        
        Format the output as a short, easy-to-read daily digest update. 
        Use bullet points for key takeaways.
        
        Transcript: 
        {text}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that summarizes technical news."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return None