import requests
from utils.constants import API_URL


class APIClient:

    BASE_URL = API_URL

    def process_video(
        self,
        url: str,
    ):

        response = requests.post(
            f"{self.BASE_URL}/process-video",
            json={
                "url": url,
            },
        )

        response.raise_for_status()

        return response.json()

    def chat(
        self,
        question: str,
        video_id: str,
    ):

        response = requests.post(
            f"{self.BASE_URL}/chat",
            json={
                "question": question,
                "video_id": video_id,
            },
        )

        response.raise_for_status()

        return response.json()

    def health(
        self,
    ):

        response = requests.get(
            f"{self.BASE_URL}/health"
        )

        response.raise_for_status()

        return response.json()