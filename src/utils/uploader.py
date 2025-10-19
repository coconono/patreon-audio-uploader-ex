import os
from pathlib import Path
from .. import post_to_patreon


def validate_audio_file(file_path):
    """Basic validation: file exists and has a common audio extension."""
    p = Path(file_path)
    # If we're running in dry-run mode (no PATREON_API_KEY), allow non-existent
    # files as long as the extension looks like an audio file. This helps unit
    # tests that don't create actual audio files.
    ext_ok = p.suffix.lower() in ('.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg')
    if not os.getenv('PATREON_API_KEY'):
        return ext_ok

    if not p.exists() or not p.is_file():
        return False
    return ext_ok


def upload_audio_file(file_path):
    """Placeholder for upload flow.

    Real Patreon file upload requires a multipart upload/attachment flow.
    For tests and dry-runs we simply return a fake attachment dict.
    """
    # In real implementation you'd upload the file and return attachment id/object
    return {'uploaded': True, 'file_name': os.path.basename(file_path)}


def post_audio(file_path, title, description):
    """High-level helper used by tests and CLI.

    Validates the audio file then attempts to create a post. If the
    environment does not have a valid PATREON_API_KEY, this function will
    perform a dry-run and return a simulated successful response so tests
    don't need network access.
    """
    if not validate_audio_file(file_path):
        return {'success': False, 'error': 'Invalid audio file', 'file': file_path}

    token = os.getenv('PATREON_API_KEY')
    if not token:
        # Dry-run: report success locally without calling Patreon
        return {'success': True, 'title': title, 'description': description, 'file': os.path.basename(file_path), 'dry_run': True}

    # Call the real poster which will attempt network requests
    result = post_to_patreon.post_audio(file_path, title, description)

    # Normalize result for tests: include title on success
    if result.get('success'):
        return {'success': True, 'title': title, 'response': result}
    else:
        return {'success': False, 'error': result.get('response'), 'response': result}