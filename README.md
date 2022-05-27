# Composer or Pasta?
This project provides a simple implementation for a Telegram bot that hosts games of "Composer or Pasta?", where you guess whether a given word is the name of a composer or a type of pasta.

The bot can host one concurrent game per chat, which can be single or multiplayer, across multiple chats. The bot will also store high scores, which persist through restarts.

## Technical Details

- Python Version: 3.10+
- Telegram Bot API Wrapper: [python-telegram-bot v13.X](https://github.com/python-telegram-bot/python-telegram-bot)

## Instructions

1. Create Telegram Bot with the [**Bot Father**](https://core.telegram.org/bots#6-botfather)
2. Set the bot's commands using `/setcommands` with the **Bot Father**:
    ```
    newgame - Start a new game of "Composer or Pasta?"
    cancel - Cancel the current game
    myhiscore - See your highest score
    hiscore - See the high score in the leaderboards
    ``` 
3. Set up environment
   - Add Python to Path
     - Note: Try using `python --version` in the command line. Please use Python **3.10** or higher.
   - Run the set-up script (`setup.bat` on **Windows** and `setup.sh` for **Linux** and **Mac**)
     - Note: Use `chmod 755 setup.sh` to give the script permissions
4. Fill in your bot token in `token.txt`
5. Run the start script (`start.bat` on **Windows** and `start.sh` for **Linux** and **Mac**)
    - Note: Use `chmod 755 start.sh` to give the script permissions
6. Either DM `/start` the bot with the Telegram handle you've set for the bot in Step 1, or add the bot to a group chat. 