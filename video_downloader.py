import praw
import requests
import os

CLIENT_ID = ""
CLIENT_SECRET = ""
USER_AGENT = ""

reddit = praw.Reddit(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT
)


def download_video(url, download_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(download_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {url}")
        else:
            print(f"Failed to download {url}: Status code {response.status_code}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def fetch_video_from_post(post_url, download_path):
    submission = reddit.submission(url=post_url)
    if submission.media:
        media_url = submission.media["reddit_video"]["fallback_url"]
        video_filename = os.path.join(download_path, f"{submission.id}.mp4")
        download_video(media_url, video_filename)
    else:
        print("No video found in the given Reddit post.")


if __name__ == "__main__":
    post_url = ""
    download_path = ""

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    fetch_video_from_post(post_url, download_path)
