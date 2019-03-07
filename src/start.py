import json
import os
import shutil

import discord

import settings

client = discord.Client()


def get_message_files():
    files = os.listdir('../data')
    return filter(lambda x: x.endswith('.json'), files)


def get_message_config(path):
    with open(f'../data/{path}', encoding='utf8') as f:
        return json.load(f)


def make_message(message_config):
    content = message_config['content']
    embed = discord.Embed(**message_config['embed'])
    return content, embed


async def post(test=True):
    for message_file in get_message_files():
        message_config = get_message_config(message_file)
        if test:
            destination = settings.TEST_DESTINATION
        else:
            destination = message_config.get('destination', settings.DEFAULT_DESTINATION)
        message_config['destination'] = client.get_channel(destination)
        if 'embed' in message_config:
            embed_config = message_config['embed']
            embed_config['timestamp'] = discord.Embed.Empty  # Not supported yet
            message_config['embed'] = discord.Embed.from_data(embed_config).set_footer(**embed_config['footer'])
        await client.send_message(**message_config)
    print('Messages posted successfully')


@client.event
async def on_ready():
    valid_commands = ('post', 'test', 'exit')
    print('Bot connected', 'Enter your commands', sep='\n')
    while True:
        command = input('> ')

        if command not in valid_commands:
            print('Invalid command')
            print('Valid commands are:', ', '.join(valid_commands))
        elif command == 'exit':
            messages = list(get_message_files())
            if not len(messages):
                break
            if input('Save data? (N) ') in ('Y', 'y', 'yes', 'Yes'):
                dirname = input(f'Enter dirname ({settings.DEFAULT_DIR_NAME}): ') or settings.DEFAULT_DIR_NAME
                os.makedirs(f'../data/{dirname}', exist_ok=True)
                for message in messages:
                    shutil.copy2(f'../data/{message}', f'../data/{dirname}/{message}')
            for message in messages:
                os.remove(f'../data/{message}')
            break
        else:
            await post(command == 'test')
    await client.logout()


if __name__ == '__main__':
    print('Waiting while bot connecting')
    client.run(settings.TOKEN)
    print('Bot disconnected')
