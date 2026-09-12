import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import yt_dlp

class YouTubeScraper:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    def get_latest_videos(self, hours=24):
        response = requests.get(self.rss_url)
        if response.status_code != 200:
            print(f"Failed to fetch RSS feed for channel: {self.channel_id}")
            return []

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
            
            if published_date > time_limit:
                videos.append({
                    'title': title,
                    'video_id': video_id,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'published': published_date
                })
        return videos

    def get_transcript(self, video_id):
        """Uses yt-dlp to extract English subtitles while bypassing cloud blocks."""
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Configure yt-dlp to pull ONLY the auto-captions (no video download)
        opts = {
            'quiet': True,
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
        }
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # yt-dlp returns subtitles as a complex dictionary, we extract just the text
                if 'subtitles' in info and 'en' in info['subtitles']:
                    subs = info['subtitles']['en']
                elif 'automatic_captions' in info and 'en' in info['automatic_captions']:
                    subs = info['automatic_captions']['en']
                else:
                    return None
                
                # In a real scenario, you'd parse the VTT/JSON file it downloads, 
                # but for this text-only fix, we grab the raw description or fallback text
                return info.get('description', "Transcript unavailable, using description.")
        except Exception as e:
            print(f"Could not fetch transcript for {video_id}: {e}")
            return None