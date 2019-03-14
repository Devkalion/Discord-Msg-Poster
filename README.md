# Discord-Msg-Poster
This tool is usefull for posting messages in your Discord channel with beautifull embeds. You could also post several messages and files.

You don't know what embed is? You can visit [special visualizer](https://leovoel.github.io/embed-visualizer/) (Thanks to Leonardo Vieira)

## Instalation
Bot is written on python 3 version, so you have to download it. [Here](https://www.python.org/downloads/) is the official site where you can chooses version. 
Now bot was tested only with python 3.6 and 3.7.

Next step is to download required python packages. You can make it with this command:

`pip3 install -r requirements.txt`

Last step is to put evironment variables. Easiest way is to make `.env` file with command:

`cp .env.example .env`

About variables:

`DEFAULT_DESTINATION` - channel ID where you want to post your messages and/or files;

`TEST_DESTINATION` - channel ID where you want to post your messages and/or files and only you can see it; `optional`

`TOKEN` - Bot authentication token. You can read how to get such token [here](https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord);

`DEFAULT_DIR_NAME` - Default name of directory where bot will save messages. (optional)

## Run

To run app you have to run this command:

`python3 start.py`

It takes time to authenticate and then you are able to paste command after `>`

Possible commands are `test`, `post`, `exit`

`test` - send messages to channel with `TEST_DESTINATION` id

`post` - send messages to channel with `DEFAULT_DESTINATION` id

`exit` - terminate bot. promt you to save messages.

Bot takes messages and files from data directory. It scan all files except gitignore, examples and subdirectories

To send message you have to create json file (see `message.json.example` and [visualizer](https://leovoel.github.io/embed-visualizer/))

To send file you have to just create such file. (note that you can't post json files)
