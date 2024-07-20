from googleapiclient.discovery import build
import webbrowser

api_key = 'api_key'
youtube = build('youtube', 'v3', developerKey=api_key)

def open_first_youtube_result(track_name, artist_name):
    query = f"{track_name} {artist_name} Official Audio"
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()

    if not response.get('items'):
        print("No results found.")
        return

    video_id = response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    webbrowser.open(video_url)
