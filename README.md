# 🚀 Space Quiz Bot

A Discord bot that tests your knowledge of space objects! You're shown images of nebulae, stars, and other celestial objects — and you have to identify them.

## Features

- **Image-based quiz** — Each round shows a real astronomical image for you to identify
- **12 space objects** — Including the Crab Nebula, Helix Nebula, Cassiopeia A, Orion Molecular Cloud Complex, and more
- **Fuzzy matching** — Typos are forgiven! Close enough answers (≥80% match) still count
- **Score tracking** — See your final score at the end of each quiz
- **Slash commands** — Clean Discord slash command interface

## Commands

| Command | Description |
|---------|-------------|
| `/quiz_start` | Start a new quiz with randomized image order |
| `/quiz_guess <answer>` | Submit your guess for the current image |

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/V01D-CALLSIGN/SpaceQuizBot.git
   cd SpaceQuizBot
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install discord.py python-dotenv thefuzz
   ```

3. **Add your Discord bot token**
   
   Create a `.env` file:
   ```
   DISCORD_TOKEN=your_token_here
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Tech Stack

- **Python** + [discord.py](https://discordpy.readthedocs.io/)
- **thefuzz** for fuzzy text matching
- **python-dotenv** for environment variable management
