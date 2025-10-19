import patreon
from flask import request
client_id = "KH9gjTrShEyaZn4VXABBn0N_Xwi92QDC6Ot2vHlV8JOQeVIcgX-Or_mxgs7LxC6f"
redirect_uri = "https://linktree.com/coconono"
  
# Construct the authorization URL
auth_url = f"https://www.patreon.com/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=identity%20identity.memberships"
print(f"Please visit this URL to authorize your application: {auth_url}")

# Example using patreon library (in a Flask route, for instance)
@app.route('/oauth/redirect')
def oauth_redirect():
    oauth_client = patreon.OAuth(client_id, client_secret)
    tokens = oauth_client.get_tokens(request.args.get('code'), redirect_uri)
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']
    # Store tokens securely for future use
    return "Tokens received!"
