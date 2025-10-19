import argparse
import json
# load environment from .env (src/config.py calls load_dotenv())
import config
from post_to_patreon import post_audio
import sys

def main():
    parser = argparse.ArgumentParser(description='Upload audio file to Patreon.')
    parser.add_argument('audio_file', type=str, help='Path to the audio file to upload')
    parser.add_argument('title', type=str, help='Title of the Patreon post')
    parser.add_argument('description', type=str, help='Description of the Patreon post')

    args = parser.parse_args()

    post_audio(args.audio_file, args.title, args.description)
    result = post_audio(args.audio_file, args.title, args.description)
    # print readable JSON for debugging
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result.get('success'):
        # return non-zero so CI/terminal can detect failure
        sys.exit(1)

if __name__ == '__main__':
    main()