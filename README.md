# Karmabot for chat in Telegram
This is chat-bot for Telegram, that helps reward people for useful tips.
When you reply to a person’s message with the phrase “Thank you” the bot adds the karma. So bot reduces the karma, when you reply to a person's message with the phrase "Minus". You can change these phrases to any other.

### Settings
- First, you must set the token and bot username in the **config.py** file.
- You should also set the chat id where the bot should work. You can find out your chat number in ["Show Json Bot"](https://t.me/ShowJsonBot).
- Set the database settings. The bot runs on PostgreSQL.
- In the admins array add IDs of users that can use */ban* and */unban* commands.
- In the **web.py** file you should to set your webhook settings.
```bash
bot.set_webhook(url="https://karmabot.herokuapp.com/%s/" % token)
```

*You can also change all the answers of the bot, which are in the config file. But don't remove the variables **@%s**, **%s** and **%d** in the texts.*


### Installation
I recommend deploying the bot to Heroku. You can also create a PostgreSQL database in the "Add-Ons" tab.
