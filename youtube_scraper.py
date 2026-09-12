import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeScraper:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        # YouTube provides a hidden RSS feed for every channel
        self.rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    def get_latest_videos(self, hours=24):
        """Fetches videos uploaded to the channel in the last X hours."""
        response = requests.get(self.rss_url)
        if response.status_code != 200:
            print(f"Failed to fetch RSS feed for channel: {self.channel_id}")
            return []

        # Parse the XML data from the RSS feed
        root = ET.fromstring(response.content)
        ns = {'yt': 'http://www.youtube.com/xml/schemas/2015',
              'atom': 'http://www.w3.org/2005/Atom'}
        
        videos = []
        now = datetime.now(timezone.utc)
        time_limit = now - timedelta(hours=hours)

        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text
            video_id = entry.find('yt:videoId', ns).text
            published_str = entry.find('atom:published', ns).text
            
            published_date = datetime.fromisoformat(published_str)
            
            # Only grab the video if it's new
            if published_date > time_limit:
                videos.append({
                    'title': title,
                    'video_id': video_id,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'published': published_date
                })
        return videos
    def get_transcript(self, video_id):
            """Downloads the full text transcript of the video."""
            try:
                # Initialize the API and use the new fetch() method
                yt_api = YouTubeTranscriptApi()
                transcript_list = yt_api.fetch(video_id)
                
                # NEW FIX: Use object attribute (.text) instead of dictionary syntax (['text'])
                full_text = " ".join([piece.text for piece in transcript_list])
                return full_text
            except Exception as e:
                print(f"Could not fetch transcript for {video_id}: {e}")
                return None
    # --- Local Testing ---
if __name__ == "__main__":
    # Dave Ebbelaar's active channel ID
    TEST_CHANNEL = "UCn8ujwUInbJkBhffxqAPBVQ" 
    scraper = YouTubeScraper(TEST_CHANNEL)
    
    print("Checking for videos in the last 200 hours...")
    recent_videos = scraper.get_latest_videos(hours=200)
    
    if not recent_videos:
        print("No recent videos found.")
    else:
        for vid in recent_videos:
            print(f"\nFound Video: {vid['title']}")
            print("Fetching transcript...")
            text = scraper.get_transcript(vid['video_id'])
            if text:
                print(f"\nSuccess! Transcript snippet: \n{text[:300]}...")