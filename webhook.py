import asyncio
import os
from datetime import datetime

import aiohttp
import dotenv
from discord import AsyncWebhookAdapter, Webhook, Embed, File

from utils import output, save_data, get_message_files, get_message_config, DATE_FRMT


async def is_webhook_correct(session, url):
    async with session.get(url) as response:
        return response.status == 200


async def post(webhook):
    dotenv.load_dotenv()

    for message_file in get_message_files():
        data = {
            'username': os.environ.get('WEBHOOK_USERNAME'),
            'avatar_url': os.environ.get('WEBHOOK_AVATAR_URL')
        }
        if message_file.endswith('.json'):
            msg_cfg = get_message_config(message_file)
            data['content'] = msg_cfg.get('content')
            if 'embed' in msg_cfg:
                if 'timestamp' in msg_cfg['embed']:
                    msg_cfg['embed']['timestamp'] = str(datetime.strptime(msg_cfg['embed']['timestamp'], DATE_FRMT))
                data['embed'] = Embed.from_dict(msg_cfg['embed'])

        else:
            data['file'] = File(f'data/{message_file}')

        await webhook.send(**data)

    print('Messages posted successfully')


async def interface(prod, test):
    valid_commands = ('post', 'test', 'exit')
    output('Enter your commands')
    while True:
        command = input('> ').lower()

        if command not in valid_commands:
            output('Invalid command')
            output(f'Valid commands are: {", ".join(valid_commands)}')
        elif command == 'exit':
            save_data()
            break
        else:
            webhook = test if command == 'test' else prod
            await post(webhook)


async def main():
    dotenv.load_dotenv()
    if 'WEBHOOK_URL' not in os.environ:
        output('Please specify webhook url', True)
    has_test_webhook = 'TEST_WEBHOOK_URL' in os.environ
    if not has_test_webhook:
        output('You have no test webhook')
    url = os.environ['WEBHOOK_URL']
    test_url = os.environ.get('TEST_WEBHOOK_URL', url)

    output('Checking webhooks connections')
    async with aiohttp.ClientSession() as session:
        prod = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
        test = Webhook.from_url(test_url, adapter=AsyncWebhookAdapter(session))

        await interface(prod, test)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
