from os import environ, getenv

from dotenv import load_dotenv

load_dotenv()
TOKEN = environ.get('TOKEN') # Should raise if missing
DEV_USER_ID = int(getenv('DEV'))
NCHANNEL = int(getenv('NOTICE_CHANNEL'))
LCHANNEL = int(getenv('LOG_CHANNEL'))