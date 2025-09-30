from yfpy.query import YahooFantasySportsQuery
import os
from pathlib import Path

YAHOO_LEAGUE_ID = os.getenv("YAHOO_LEAGUE_ID")
YAHOO_CONSUMER_KEY = os.getenv("YAHOO_CONSUMER_KEY")
YAHOO_CONSUMER_SECRET = os.getenv("YAHOO_CONSUMER_SECRET")
YAHOO_ACCESS_TOKEN = os.getenv("YAHOO_ACCESS_TOKEN")
YAHOO_TOKEN_GUID = os.getenv("YAHOO_TOKEN_GUID")
YAHOO_REFRESH_TOKEN = os.getenv("YAHOO_REFRESH_TOKEN")

def get_ff_query():
    return YahooFantasySportsQuery(
        league_id=YAHOO_LEAGUE_ID,
        game_code="nfl",
        game_id=461,
        # yahoo_consumer_key=YAHOO_CONSUMER_KEY,
        # yahoo_consumer_secret=YAHOO_CONSUMER_SECRET,
        save_token_data_to_env_file=True,
        env_file_location=Path(r"."),
        env_var_fallback=False,
        yahoo_access_token_json={
            "access_token": YAHOO_ACCESS_TOKEN,
            "consumer_key": YAHOO_CONSUMER_KEY,
            "consumer_secret": YAHOO_CONSUMER_SECRET,
            "guid": YAHOO_TOKEN_GUID,
            "refresh_token": YAHOO_REFRESH_TOKEN,
            "token_time": 1234567890.123456,
            "token_type": "bearer"
        }
    )