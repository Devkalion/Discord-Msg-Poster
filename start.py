import os

import discord
import dotenv

from utils import output, save_data, get_message_config, get_message_files

client = discord.Client()


async def post_message(message_file, test):
    message_config = get_message_config(message_file)
    if test:
        message_config['channel_id'] = os.environ['TEST_DESTINATION']
    else:
        message_config['channel_id'] = message_config.get('channel_id', os.environ['DEFAULT_DESTINATION'])
    await client.http.send_message(**message_config)


async def send_file(file_name, test):
    if test:
        channel_id = os.environ['TEST_DESTINATION']
    else:
        channel_id = os.environ['DEFAULT_DESTINATION']
    with open(f'data/{file_name}', 'rb') as f:
        content = f.read()
    await client.http.send_files(channel_id, files=[(content, file_name)])


async def post(test=True):
    for message_file in get_message_files():
        if message_file.endswith('.json'):
            await post_message(message_file, test)
        else:
            await send_file(message_file, test)
    print('Messages posted successfully')


@client.event
async def on_ready():
    valid_commands = ('post', 'test', 'exit')
    print('Bot connected', 'Enter your commands', sep='\n')
    while True:
        dotenv.load_dotenv()
        command = input('> ').lower()

        if command not in valid_commands:
            print('Invalid command')
            print('Valid commands are:', ', '.join(valid_commands))
        elif command == 'exit':
            save_data()
            break
        else:
            await post(command == 'test')
    await client.logout()


if __name__ == '__main__':
    dotenv.load_dotenv()
    if 'TOKEN' not in os.environ:
        output('Please specify bot token', True)

    TOKEN = os.environ['TOKEN']
    print('Waiting while bot connecting')
    client.run(TOKEN)
    print('Bot disconnected')
