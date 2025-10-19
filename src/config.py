import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # read the token from an env var named PATREON_API_KEY
    PATREON_API_KEY = os.getenv('PATREON_API_KEY')
    PATREON_API_URL = "https://www.patreon.com/api/oauth2/v2/"
    AUDIO_UPLOAD_ENDPOINT = "campaigns/{campaign_id}/posts"