from django.conf import settings
from os.path import join
from json import dump


def check_limit(data: list, key: str, limit: float):
    return all(float(i[key]) <= limit for i in data['items'])


def json_to_file(data, file_name):
    path = join(settings.BASE_DIR, 'small_business', 'rooms', 'tests', 'results', f'{file_name}.json')
    with open(path, 'w', encoding='utf-8') as json_file:
        dump(data, json_file, ensure_ascii=False, indent=4)
