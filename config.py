from os import environ, getenv
if getenv("RAILWAY_ENVIRONMENT"):
    print("Running on Railway, not loading .env")
else:
    from dotenv import load_dotenv
    load_dotenv()
TOKEN = environ.get('TOKEN') # Should raise if missing
DEV_USER_ID = int(getenv('DEV'))
NCHANNEL = int(getenv('NOTICE_CHANNEL'))
LCHANNEL = int(getenv('LOG_CHANNEL'))