# YouTube Downloader

YouTube Downloader is a graphical user interface (GUI) application that allows users to download YouTube videos in various resolutions or as audio files.

## Features

- Download YouTube videos in multiple resolutions (1080p, 1440p, 4K).
- Download audio-only versions of YouTube videos.
- Select destination folder and set custom filenames.
- Progress bar and percentage display for download progress.
- Dark mode support with a custom color theme.

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/IPG2004/YouTube-Downloader.git
    cd YouTube-Downloader
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python src/app.py
    ```

2. Enter the URL of the YouTube video you want to download.

3. Choose the download mode (Video/Audio) and resolution.

4. Select the destination folder and set a custom filename.

5. Click the "Download" button to start downloading the video.

## Project Structure

```plaintext
YouTube-Downloader/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── src/
    ├── __init__.py
│   ├── app.py
│   └── resources/
        ├── __init__.py
│       └── red.json
└── tests/
    ├── __init__.py
    └── test_app.py

```
- `src/`: Contains the main application code.
    - `app.py`: Main GUI application.
    - `resources/`: Contains additional resources if needed.
- `tests/`: Contains test files.
    - `test_app.py`: Test cases for the application.

## License

This project is licensed under the MIT license - see the [LICENSE](LICENSE) for more details.

## Credits

Made by [@IPG2004](https://github.com/IPG2004)