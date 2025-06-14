# Yt-scraper

A small tool to download subtitles from YouTube videos.

## Local usage

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the scraper:
   ```bash
   python subtitle_scraper.py <VIDEO_URL> -l a.en -o subtitles.txt
   ```
   Replace `<VIDEO_URL>` with the link to the video and adjust the language code if necessary.

## GitHub Actions

The repository includes a workflow that can be triggered manually to scrape subtitles and provide them as a build artifact.

To use it:

1. Open the **Actions** tab in GitHub.
2. Start the **Scrape Subtitles** workflow and provide the `video_url` input. Optionally set `language`.
3. When the workflow completes, download the `subtitles` artifact from the run summary.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
