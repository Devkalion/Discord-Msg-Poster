import json
import os
import shutil

import discord
import dotenv

client = discord.Client()


def get_message_files():
    files = sorted(os.listdir('data'))
    return filter(lambda x: not x.endswith('.gitignore') and not x.endswith('.example'), files)


def get_message_config(path):
    with open(f'data/{path}', encoding='utf8') as f:
        return json.load(f)


def make_message(message_config):
    content = message_config['content']
    embed = discord.Embed(**message_config['embed'])
    return content, embed


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


def save_data():
    messages = list(get_message_files())
    if not len(messages):
        return
    if input('Save data? (N) ') in ('Y', 'y', 'yes', 'Yes'):
        dirname = os.environ.get('DEFAULT_DIR_NAME', 'dir')
        dirname = input(f'Enter dirname ({dirname}): ') or dirname
        os.makedirs(f'data/{dirname}', exist_ok=True)
        for message in messages:
            shutil.copy2(f'data/{message}', f'data/{dirname}/{message}')
    for message in messages:
        os.remove(f'data/{message}')


@client.event
async def on_ready():
    valid_commands = ('post', 'test', 'exit')
    print('Bot connected', 'Enter your commands', sep='\n')
    while True:
        dotenv.load_dotenv()
        command = input('> ')

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
    TOKEN = os.environ['TOKEN']
    print('Waiting while bot connecting')
    client.run(TOKEN)
    print('Bot disconnected')
