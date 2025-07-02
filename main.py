import logging
import sys
from typing import NoReturn
from config import TOKEN
from iter_bot.core.bot import ITERBot

logger = logging.getLogger(__name__)


def main() -> NoReturn:
    """
    Initialize and run the Discord bot
    """
    try:
        bot = ITERBot()
        bot.run(TOKEN)
    except Exception as e:
        logger.critical(f'Failed to start bot: {str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    main()