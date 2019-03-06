import json
import os
import sys

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


@client.event
async def on_ready():
    for message_file in get_message_files():
        message_config = get_message_config(message_file)

        message_config['destination'] = client.get_channel(message_config.get('destination', destination))
        if 'embed' in message_config:
            embed_config = message_config['embed']
            embed_config['timestamp'] = discord.Embed.Empty  # Not supported yet
            message_config['embed'] = discord.Embed.from_data(embed_config).set_footer(**embed_config['footer'])
        await client.send_message(**message_config)
    await client.logout()
    print('Messages posted successfully')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage:\npython message test\npython message post')
    elif len(sys.argv) > 2:
        print(f'Expected 1 argument but {len(sys.argv)} were given')
    else:
        if sys.argv[1] == 'test':
            destination = settings.TEST_DESTINATION
        elif sys.argv[1] == 'post':
            destination = settings.DEFAULT_DESTINATION
        else:
            print('Usage:\npython message test\npython message post')
            exit(1)
        client.run(settings.TOKEN)
