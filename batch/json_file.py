import json
from enum import Enum
from functools import partial


class FileFormat(Enum):
    JSONL = 1


class JsonlineClient:
    def __init__(self, dir_path: str) -> None:
        self.dir_path = dir_path

    def insert(self, json_list: list, file_name):
        file_path = f'{self.dir_path}/{file_name}.jsonl'
        with open(file_path, 'a', encoding='utf8') as f:
            for dic in json_list:
                json.dump(dic, f, ensure_ascii=False)
                f.write('\n')
