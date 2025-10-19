# Patreon Audio Uploader

This project provides a simple command-line tool to upload audio files to your Patreon account. It interacts with the Patreon API to create new posts with audio content.


It doesn't actually work because Patreon has stopped this kind of tomfoolery for very obvious reasons

## Features

- Upload audio files to Patreon
- Specify post titles and descriptions
- Command-line interface for easy usage

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/patreon-audio-uploader.git
   cd patreon-audio-uploader
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables. Copy the `.env.example` to `.env` and fill in your Patreon API keys and other necessary configurations.

## Usage

To upload an audio file, use the command line interface as follows:

```bash
python src/cli.py --audio <path_to_audio_file> --title "<post_title>" --description "<post_description>"
```

Replace `<path_to_audio_file>`, `<post_title>`, and `<post_description>` with your audio file path, desired post title, and description respectively.

## Testing

To run the tests for the uploader functionality, navigate to the `tests` directory and run:

```bash
pytest test_uploader.py
```

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Environment

The project uses environment variables to configure access to the Patreon API. Create a `.env` file in the project root (this repository includes a `.env.example`) and set the following:

- `PATREON_API_KEY`: Your Patreon OAuth2 access token (required for real uploads)
- `CAMPAIGN_ID`: (optional) Your campaign ID. If not provided, the tool will attempt to discover it from the identity endpoint when `PATREON_API_KEY` is present.

Example `.env` (do NOT commit real tokens):

```env
PATREON_API_KEY=your_real_patreon_access_token_here
CAMPAIGN_ID=1234567
```

If `PATREON_API_KEY` is not set the uploader runs in a dry-run mode useful for development and tests
