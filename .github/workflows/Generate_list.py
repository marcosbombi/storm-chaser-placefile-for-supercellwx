import requests
import random
import os

API_KEY = os.getenv('YOUTUBE_API_KEY')  # Read API key from environment variable
SEARCH_QUERY = "storm chasing tornado severe weather"
MAX_RESULTS = 25

# Approximate central location for storm chasing (e.g. Oklahoma)
BASE_LAT = 35.5
BASE_LON = -97.5

def search_youtube_live_streams(api_key, query, max_results=25):
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
    data = response.json()
    return data.get('items', [])

def generate_placefile(streams):
    lines = []
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

        lines.append(f"Object: Stream{i}")
        lines.append("Type: ICON")
        lines.append("Icon: 1,0,0")
        lines.append("Threshold: 999")
        lines.append(f"Lat: {lat:.4f}")
        lines.append(f"Lon: {lon:.4f}")
        lines.append(f'Text: 0,1,1,"{title} 🔴 [Live]({url})"')
        lines.append("End:\n")

    return "\n".join(lines)

if __name__ == "__main__":
    if not API_KEY:
        print("Error: YouTube API key not found in environment variables.")
        exit(1)

    streams = search_youtube_live_streams(API_KEY, SEARCH_QUERY, MAX_RESULTS)
    placefile_text = generate_placefile(streams)

    with open("youtube_chasers.txt", "w", encoding="utf-8") as f:
        f.write(placefile_text)

    print("Placefile generated: youtube_chasers.txt")
