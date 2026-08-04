from app.services.transcript_service import TranscriptService


def main():
    url = input("Enter YouTube URL: ")
    service = TranscriptService()
    transcript = service.fetch_transcript(url)
    service.save_transcript(transcript)

if __name__ == "__main__":
    main()

    