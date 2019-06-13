token = ""  # bot token
botName = ""  # bot username
chatId = -1001182112156  # id of chat where bot should work

# DB settings
database = "bnf747l6otb4n"
host = "ec2-67-154-119-214.eu-west-1.compute.amazonaws.com"
user = "keshandyandhg"
password = "0c2gbb1983776f19837ddaf1218736661b30dc1b8e198739bdde0dd7a7b04ad"

admins = [183654961, 0, 0]  # users ids that can use /ban and /unban commands

helpText = """
To *add karma*, reply with the phrase "Thank you" to the message of the person who helped you.
\nTo *reduce karma*, reply with the phrase "Minus" to the message of who you want to reduce karma.

\n/top20 - displays top 20 users with positive karma
\n/untop20 - displays top 20 users with negative karma
\n/help - help on bot commands
"""

# text for new users
welcomeText = """
Hey, @%s!
\nWe are glad to see you in the chat.
\nTell me something about yourself.
"""

# text for new users without username
welcomeUser = """
Hey, %s!
\nWe are glad to see you in the chat.
\nI noticed that you don't have a username :( Please set it, so that I can change your karma. Thank you!
\nAnd now tell me something about yourself.
"""

# text for chat where bot don't work
dontWork = "Sorry, but I don't work in this chat."

# karma text for user without username
notUsername = "Unfortunately, the user you thanked doesn't have a username, so I can't change his karma :("

# text for message without reply
shouldReply = "@%s, you must respond to a message that helped you!"
shouldReply2 = "@%s, you must respond to a message you didn't like!"

# text with thanks to bot
thxToBot = "@%s, always happy to help!"

# text with reduce karma to bot
botMinus = "@%s, I don't have a karma!"

# text with karma to urself
masturbate = "@%s, hey, you can't add karma to yourself!"
unmasturbate = "@%s, why don't you love yourself? :("

# text to karma add
karmaPlus = """
Added karma to @%s
\n-------------------
@%s has %d karma
"""

# text to reduce karma
karmaMinus = """
Reduces karma to @%s
\n-------------------
@%s has %d karma
"""

# text for a ban for a little karma
banForKarma = "@%s has -100 karma. He is banned."

# text for ban if user doesn't exist in DB
cantBan = "There is no such user in my database, you can ban it only manually."

# text for unban if user doesn't exist in DB
cantUnban = "There is no such user in my database, you can unban it only manually."

# text for ban
banned = "Banned"

# text for unban
unbanned = "Unbanned"
