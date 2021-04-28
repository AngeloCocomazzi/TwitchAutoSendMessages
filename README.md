# TwitchAutoSendMessages
Twitch bot in python to automatically send messages every preset interval. The bot prints the most written message in the chat, imitating the behavior of the chat. Avoiding swear words, predefined users and special characters, obviously all to be defined by the user, within the program.

---
# Explanation

When the bot has started, it will start listening to chat messages in the channel listed in the settings.txt file. The bot will print all the information it receives.
---

# Note
Unlike my other bots, this one is not designed to be used by people with no programming experience. This repo is more of a showcase or backup. I only use this repo for testing/debugging purposes.
---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>"
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Requirements
* [Python 3.6+](https://www.python.org/downloads/)
* [Module requirements](requirements.txt)<br>
Install these modules using `pip install -r requirements.txt`

---


