from youtube_scraper import YouTubeScraper
from ai_summarizer import AISummarizer
from email_sender import EmailSender
from datetime import datetime

def main():
    # Add as many YouTube channel IDs as you want to this list
    TARGET_CHANNELS = [
        "UCn8ujwUInbJkBhffxqAPBVQ",  # Dave Ebbelaar
        "UCfzlCWGWYyIQ0aLC5w48gBQ",  # Sentdex (Example)
        # "Another_Channel_ID_Here"
    ]

    summarizer = AISummarizer()
    master_digest = ""

    print("Starting multi-channel sweep...")

    # Loop through every channel in your list
    for channel_id in TARGET_CHANNELS:
        scraper = YouTubeScraper(channel_id)
        # Changed to 24 hours since your GitHub Action runs daily
        recent_videos = scraper.get_latest_videos(hours=24) 
        
        if not recent_videos:
            continue

        # Process the newest video from the current channel
        video = recent_videos[0]
        print(f"Found new video: {video['title']}")
        
        transcript = scraper.get_transcript(video['video_id'])
        if transcript:
            print("Generating summary...")
            summary = summarizer.summarize_transcript(transcript, video['title'])
            # Append this summary to the master email body
            master_digest += f"\n\n📺 {video['title']}\n{'-'*40}\n{summary}\n"

    # Only send an email if at least one video was found and summarized
    if master_digest.strip():
        print("\nSending master digest email...")
        email_sender = EmailSender()
        today = datetime.now().strftime("%b %d, %Y")
        subject = f"🤖 AI News Digest - {today}"
        
        email_sender.send_email(subject, master_digest.strip())
    else:
        print("No new videos in the last 24 hours. No email sent.")

if __name__ == "__main__":
    main()