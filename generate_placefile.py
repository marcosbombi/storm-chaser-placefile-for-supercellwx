import requests
import random
import os
from datetime import datetime

API_KEY = os.getenv('YOUTUBE_API_KEY')  # Read API key from environment variable
SEARCH_QUERY = "storm chasing tornado severe weather"
MAX_RESULTS = 25

# Approximate central location for storm chasing (e.g. Oklahoma)
BASE_LAT = 35.5
BASE_LON = -97.5

def search_youtube_live_streams(api_key, query, max_results=25):
    if not api_key:
        print("❌ Error: No YouTube API key found in environment.")
        exit(1)

    print("🔍 Searching YouTube for live streams...")
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'eventType': 'live',
        'type': 'video',
        'q': query,
        'maxResults': max_results,
        'key': api_key,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ YouTube API request failed with status code {response.status_code}")
        print(response.text)
        exit(1)

    data = response.json()
    return data.get('items', [])

def generate_placefile(streams):
    lines = []
    lines.append(f"# Generated: {datetime.utcnow().isoformat()}Z")
    lines.append("Title: YouTube Storm Chaser Live Streams")
    lines.append("Refresh: 300")
    lines.append("Color: 255 0 0\n")

    for i, item in enumerate(streams):
        video_id = item['id']['videoId']
        title = item['snippet']['title'].replace('"', "'")  # sanitize quotes
        url = f"https://www.youtube.com/watch?v={video_id}"
        # Random offset location near base lat/lon for display
        lat = BASE_LAT + (random.random() - 0.5) * 1.0  # ±0.5 degrees
        lon = BASE_LON + (random.random() - 0.5) * 1.0

        lines.append(f"Object: {lat:.4f} {lon:.4f} 20")
        lines.append(f"  Icon: 1")
        lines.append(f'  Text: 0,1,1,"{title} 🔴 [Live]({url})"')
        lines.append("End:\n")

    return "\n".join(lines)

if __name__ == "__main__":
    print("📦 Starting placefile generator...")
    print(f"Environment has YOUTUBE_API_KEY: {'Yes' if API_KEY else 'No'}")

    streams = search_youtube_live_streams(API_KEY, SEARCH_QUERY, MAX_RESULTS)
    print(f"✅ Found {len(streams)} live stream(s)")

    if not streams:
        print("⚠️ No streams found. Exiting without creating placefile.")
        exit(0)

    placefile_text = generate_placefile(streams)
    filename = "youtube_chasers.txt"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(placefile_text)
        print(f"✅ Placefile generated: {filename}")
    except Exception as e:
        print(f"❌ Failed to write file: {e}")
        exit(1)

    # List current working directory
    print("\n📂 Current working directory contents:")
    for file in os.listdir():
        print(f" - {file}")
