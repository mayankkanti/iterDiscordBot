from os import getenv

TOKEN = getenv('TOKEN')
DEV = getenv('DEV')
NCHANNEL = getenv('NOTICE_CHANNEL')
LCHANNEL = getenv('LOG_CHANNEL')


DEV_USER_ID = int(DEV)
NCHANNEL = int(NCHANNEL)
LCHANNEL = int(LCHANNEL)