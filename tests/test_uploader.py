import os
import unittest
os.environ.pop('PATREON_API_KEY', None)
from src.utils.uploader import post_audio

class TestUploader(unittest.TestCase):

    def test_post_audio_success(self):
        # Mock the parameters for a successful post
        audio_file = 'test_audio.mp3'
        title = 'Test Post Title'
        description = 'This is a test description for the audio post.'
        
        # Call the post_audio function and check for expected behavior
        result = post_audio(audio_file, title, description)
        self.assertTrue(result['success'])
        self.assertEqual(result['title'], title)

    def test_post_audio_failure(self):
        # Mock the parameters for a failed post
        audio_file = 'invalid_audio.txt'  # Assuming this format is not allowed
        title = 'Invalid Post Title'
        description = 'This should fail due to invalid audio format.'
        
        # Call the post_audio function and check for expected failure behavior
        result = post_audio(audio_file, title, description)
        self.assertFalse(result['success'])
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main()