import argparse
import sys
from pytube import YouTube, extract
from bs4 import BeautifulSoup
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)


def extract_plaintext_from_caption_xml(xml_captions: str) -> str:
    """Convert caption XML to plain text."""
    soup = BeautifulSoup(xml_captions, "xml")
    texts = [p.get_text().replace('\n', ' ') for p in soup.find_all('text')]
    return "\n".join(texts)


def get_plaintext_subtitles(video_url: str, language_code: str = "a.en") -> str:
    """Fetch subtitles from a YouTube video."""
    errors = []

    try:
        yt = YouTube(video_url)
        captions = yt.captions
        if language_code not in captions:
            available = ", ".join(captions.keys())
            raise ValueError(
                f"No subtitles for language code: {language_code}. Available: {available}"
            )

        caption = captions[language_code]
        xml_captions = caption.xml_captions
        return extract_plaintext_from_caption_xml(xml_captions)
    except Exception as e:  # pylint: disable=broad-except
        errors.append(e)

    # Fallback to youtube_transcript_api
    try:
        video_id = extract.video_id(video_url)
        fallback_language = language_code.split(".")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[fallback_language])
        lines = [entry["text"].replace("\n", " ") for entry in transcript]
        return "\n".join(lines)
    except (TranscriptsDisabled, NoTranscriptFound, Exception) as e:  # pylint: disable=broad-except
        errors.append(e)
        raise RuntimeError(f"Failed to fetch subtitles: {errors[-1]}") from e



def main() -> None:
    parser = argparse.ArgumentParser(description="Download YouTube subtitles as plain text.")
    parser.add_argument("video_url", help="YouTube video URL")
    parser.add_argument(
        "-l",
        "--language",
        default="a.en",
        help="Subtitle language code (default: a.en)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="subtitles.txt",
        help="Output text file",
    )
    args = parser.parse_args()

    try:
        subtitles = get_plaintext_subtitles(args.video_url, args.language)
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(subtitles)


if __name__ == "__main__":
    main()
