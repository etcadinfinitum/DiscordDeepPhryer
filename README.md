# Deep Phryer

*A Discord bot built in Python*

### Usage and Commands

This bot fries images! Specifically, it applies some color settings to a jpeg, png or gif file.

The bot is invoked with the command `FryThis`. If the originating message was not sent with an attachment, the bot will pick from a set of stock images. 

Some arguments are supported. Invoking with `params` will return the parameter set the image used in the response body. Some default color settings are supported: `galaxy`, ``. The `chaos` argument on a GIF 

A help message will print with the command `deepfriedHELP`. It includes much of this information.

Example Usages:
| Command | Attachment | Example Image Result | Example Message |
| `FryThis` | none | | |
| `FryThis galaxy` | jpg | | |
| `FryThis params` | | | |
| `FryThis dark params` | | | |
| `FryThis chaos` | gif | | |

### Get your own Phryer

##### Step 1
Go through the steps to create and authorize a bot on a Discord server. Steps are described [here](https://www.devdungeon.com/content/make-discord-bot-python), among other places.

##### Step 2 
The script expects important data to be in a file called `creds.py`. Create this file, and add the following lines:
| Code Line | Data Needed | 
| --------- | ----------- | 
| `TOKEN='XXXXXX_YOUR_TOKEN_HERE_XXXXXXXXX'` | The bot's unique token, which can be obtained in the bot's administrative settings panel. Log in [here](https://www.discordapp.com/developers) with your server's credentials (refer to Step 1). | 

This file (`creds.py`) will be ignored in Version Control with the existing .gitigore. Proceed with caution when modifying this setting. 

##### Step 3
The bot requires Wand and imagemagick to be installed. Make sure you have the necessary packages installed; read the installation docs [here](http://docs.wand-py.org/en/0.4.1/guide/install.html).

### Long-Term Support

If you have a good idea, log an issue for the project. If you implement a good idea, submit a PR.

### Credits

This bot is licensed under GPL v3.0. Go forth and propogate, but do not privatize. See the LICENSE docs for more information.

This project was started by [Finn](https://github.com/thefinn93) as a [Signal](https://www.signal.org/) bot. Huge props to him for building much of the core functionality and for encouraging me to add support for GIFs. The original bot code is [here](https://git.callpipe.com/finn/deep-fried-sigger).
