from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
DEV = getenv("DEV")
NCHANNEL = getenv("NOTICE_CHANNEL")
LCHANNEL = getenv("LOG_CHANNEL")
TASK_FREQUENCY = getenv("TASK_FREQUENCY")

DEV_USER_ID = int(DEV)
NCHANNEL = int(NCHANNEL)
LCHANNEL = int(LCHANNEL)
TASK_FREQUENCY = int(TASK_FREQUENCY)