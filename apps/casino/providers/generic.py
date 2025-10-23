import os
import uuid
from typing import Dict


def create_session(provider, game, user) -> Dict[str, str]:
    """
    Create a launch session with a casino provider.
        This supports two modes controlled by env var CASINO_USE_DEMO (default '1').
        - DEMO (CASINO_USE_DEMO='1'): returns a local placeholder launch_url.
        - REAL (CASINO_USE_DEMO='0'): call out to provider API using provider.base_url/provider.config.
            The real-call block is scaffolded and should be implemented once credentials are available.
    """
    use_demo = os.getenv('CASINO_USE_DEMO', '1') == '1'

    if use_demo:
        session_id = uuid.uuid4().hex
        launch_url = f"/casino/play/{game.slug}?sid={session_id}"
        return {"session_id": session_id, "launch_url": launch_url}

    # REAL mode scaffolding — replace with actual HTTP call to provider API
    # Example pseudo-implementation:
    # import requests
    # api_key = provider.config.get('api_key')
    # secret = provider.config.get('secret')
    # payload = {
    #     'player_id': str(user.id),
    #     'game_id': game.provider_game_id,
    #     'currency': getattr(user.wallet, 'currency', 'BDT'),
    #     'lang': 'bn' if getattr(user, 'preferred_lang', 'en') == 'bn' else 'en',
    # }
    # headers = {'Authorization': f'Bearer {api_key}'}
    # resp = requests.post(f"{provider.base_url}/v1/sessions", json=payload, headers=headers, timeout=10)
    # resp.raise_for_status()
    # data = resp.json()
    # return { 'session_id': data['id'], 'launch_url': data['launch_url'] }

    # Until implemented, fall back to demo to avoid breaking flow
    session_id = uuid.uuid4().hex
    launch_url = f"/casino/play/{game.slug}?sid={session_id}&mode=fallback"
    return {"session_id": session_id, "launch_url": launch_url}
