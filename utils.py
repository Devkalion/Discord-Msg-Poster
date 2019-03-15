import json
import os
import shutil

DATE_FRMT = '%Y-%m-%dT%H:%M:%S.%fZ'


def output(text, _exit=False):
    print(text)
    if _exit:
        exit()


def get_message_files():
    files = sorted(os.listdir('data'))
    return filter(lambda x: os.path.isfile(x) and not x.endswith('.gitignore') and not x.endswith('.example'), files)


def get_message_config(path):
    with open(f'data/{path}', encoding='utf8') as f:
        return json.load(f)


def save_data():
    messages = list(get_message_files())
    if not len(messages):
        return
    if input('Save data? (N) ').lower() in ('y', 'yes'):
        dirname = os.environ.get('DEFAULT_DIR_NAME', 'dir')
        dirname = input(f'Enter dirname ({dirname}): ') or dirname
        os.makedirs(f'data/{dirname}', exist_ok=True)
        for message in messages:
            shutil.copy2(f'data/{message}', f'data/{dirname}/{message}')
    for message in messages:
        os.remove(f'data/{message}')
