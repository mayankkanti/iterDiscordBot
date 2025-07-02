# ITER Notice Bot 🔔

A Discord bot that automatically monitors and posts new notices from the ITER website to your Discord server.

## Features

- **Automatic Notice Monitoring**: Checks ITER website every 10 minutes for new notices
- **Real-time Notifications**: Posts new notices to Discord with @everyone ping
- **Manual Check**: Force check for notices with `? checknotices` command

## Setup

1. **Install dependencies**
   ```bash
   uv sync
   ```

2. **Configure environment**
   ```env
   TOKEN=your_discord_bot_token
   NOTICE_CHANNEL=your_channel_id
   LOG_CHANNEL=your_log_channel_id
   DEV=your_user_id
   ```

3. **Run the bot**
   ```bash
   python main.py
   ```

## How It Works

The bot scrapes the [ITER News & Events page](https://www.soa.ac.in/iter-news-and-events), compares with previously seen notices in `seen_notices.json`, and posts new ones to your Discord channel.

## Commands

- `? checknotices` - Manually check for new notices
- `? ping` - Check bot status

---