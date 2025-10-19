import os
import requests
import json


def _get_api_base():
    return os.getenv('PATREON_API_URL', 'https://www.patreon.com/api/oauth2/v2/')


def _get_token():
    return os.getenv('PATREON_API_KEY')


def _identity_info(token):
    """Call the identity endpoint to validate the token and discover campaigns.

    Returns (status_code, json_or_text)
    """
    api_base = _get_api_base()
    # Do not include unsupported include parameters by default. Some Patreon
    # identity endpoints reject `include=campaigns` for the user type which
    # returns a 400. Call the identity endpoint without include params and
    # avoid the ParameterInvalidOnType error.
    url = f"{api_base}identity"
    headers = {'Authorization': f'Bearer {token}'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        try:
            return r.status_code, r.json()
        except ValueError:
            return r.status_code, r.text
    except requests.RequestException as e:
        return None, str(e)


def post_audio(audio_file, post_title, description):
    """Create a basic Patreon post (no file upload flow).

    This function validates the token via the identity endpoint, discovers the
    campaign id if it's not provided in the environment, and then creates a
    simple post with title/content. Attaching/uploading audio files requires
    the multipart/file upload flow which is not implemented here.

    Returns a dict with keys: success (bool), status (int|None), response (dict|string), debug (dict)
    """
    token = _get_token()
    api_base = _get_api_base()
    debug = {'api_base': api_base}

    if not token:
        return {'success': False, 'status': None, 'response': 'Missing PATREON_API_KEY', 'debug': debug}

    # validate token and discover campaigns
    status, identity = _identity_info(token)
    debug['identity_status'] = status
    debug['identity_response'] = identity

    if status is None:
        return {'success': False, 'status': None, 'response': f'Identity request failed: {identity}', 'debug': debug}

    if status == 401:
        return {'success': False, 'status': 401, 'response': identity, 'debug': debug}

    # try to find campaign id
    campaign_id = os.getenv('CAMPAIGN_ID')
    debug['campaign_discovery'] = {'from_env': bool(campaign_id)}
    if not campaign_id:
        # look for included -> campaigns, then relationships -> campaigns -> data
        try:
            if isinstance(identity, dict):
                included = identity.get('included', [])
                for item in included:
                    if item.get('type') == 'campaign':
                        campaign_id = item.get('id')
                        debug['campaign_discovery']['from_included'] = campaign_id
                        break

                # if not in included, check the relationships on the main data object
                if not campaign_id:
                    relationships = identity.get('data', {}).get('relationships', {})
                    campaigns_rel = relationships.get('campaigns', {}).get('data', [])
                    for c in campaigns_rel:
                        if c.get('type') == 'campaign' and c.get('id'):
                            campaign_id = c.get('id')
                            debug['campaign_discovery']['from_relationships'] = campaign_id
                            break
        except Exception:
            campaign_id = None

    if not campaign_id:
        return {
            'success': False,
            'status': None,
            'response': 'Campaign ID not provided and could not be discovered from identity endpoint',
            'debug': debug,
        }

    # build post payload (simple post with title + content)
    post_url = f"{api_base}campaigns/{campaign_id}/posts"
    debug['post_url'] = post_url
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'data': {
            'type': 'post',
            'attributes': {
                'title': post_title,
                'content': description
            },
            'relationships': {
                'campaign': {
                    'data': {'type': 'campaign', 'id': campaign_id}
                }
            }
        }
    }

    try:
        r = requests.post(post_url, headers=headers, json=payload, timeout=15)
    except requests.RequestException as e:
        return {'success': False, 'status': None, 'response': str(e), 'debug': debug}

    debug['post_status'] = r.status_code
    try:
        resp_json = r.json()
    except ValueError:
        resp_json = r.text

    if r.status_code in (200, 201):
        return {'success': True, 'status': r.status_code, 'response': resp_json, 'debug': debug}
    else:
        return {'success': False, 'status': r.status_code, 'response': resp_json, 'debug': debug}