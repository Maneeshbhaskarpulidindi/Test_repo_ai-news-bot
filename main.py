from youtube_scraper import YouTubeScraper
from ai_summarizer import AISummarizer
from email_sender import EmailSender
from datetime import datetime

def main():
    # 1. Connect to the data source
    scraper = YouTubeScraper("UCn8ujwUInbJkBhffxqAPBVQ")
    print("Checking for new videos...")
    recent_videos = scraper.get_latest_videos(hours=200)
    
    if not recent_videos:
        print("No new videos found.")
        return

    video = recent_videos[0]
    print(f"Found: {video['title']}")
    
    # 2. Extract the text
    print("Fetching transcript...")
    transcript = scraper.get_transcript(video['video_id'])
    
    if transcript:
        # 3. Process with AI
        print("Sending to AI for summarization...")
        summarizer = AISummarizer()
        summary = summarizer.summarize_transcript(transcript, video['title'])
        
        print("\n" + "="*40)
        print("📰 YOUR AI DAILY DIGEST")
        print("="*40 + "\n")
        print(summary)
        
        # 4. Email the Digest
        print("\nSending email...")
        email_sender = EmailSender()
        today = datetime.now().strftime("%b %d, %Y")
        subject = f"🤖 Your AI News Digest - {today}"
        
        email_sender.send_email(subject, summary)

if __name__ == "__main__":
    main()