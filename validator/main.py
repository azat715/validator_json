import json
from json import JSONDecodeError
from pathlib import Path
from datetime import datetime

from pydantic import ValidationError
import fire

from validator.cmarker_created import CmarkerCreated
from validator.label_selected import LabelSelected
from validator.sleep_created import SleepCreated
from validator.workout_created import WorkoutCreated


validators = {
    "cmarker_created": CmarkerCreated,
    "label_selected": LabelSelected,
    "sleep_created": SleepCreated,
    "workout_created": WorkoutCreated,
}

class CustomValidateError(Exception):
    def __init__(self, file, msg, error = None, status = False, schema = None):
        super().__init__()
        self.file = file
        self.msg = msg
        self.error = error
        self.status = status
        self.schema = schema
    def __str__(self):
        return f"""Error
                   В файле {self.file} произошла ошибка
                   {self.msg} 
                   Схема валидации {self.schema}
                   Статус {self.status}"""
    def asdict(self):
        return {
            'file': self.file,
            'msg': self.msg,
            'error': self.error,
            'status': self.status,
            'schema': self.schema,
        }

def main_validator(file):
    if not file.exists():
        raise CustomValidateError(str(file), 'Файл не найден')
    try:
        decoded_json = json.loads(file.read_bytes())
    except JSONDecodeError as err:
        raise CustomValidateError(str(file), 'Невалидный json', error = str(err)) from err       
    if not decoded_json:
        raise CustomValidateError(str(file), 'Некорректный json')
    event = decoded_json.get("event")
    data = decoded_json["data"]
    if not data or not event:
        raise CustomValidateError(str(file), 'Невалидная разметка json (нет data key)')
    if not event in validators.keys():
        raise CustomValidateError(str(file), 'Отсутствует json schema')
    try:
        validators[event](**data)
    except ValidationError as err:
        raise CustomValidateError(str(file), 'Ошибка валидации', error = json.loads(err.json()), schema = event) from err
    else:
        return {
            'file': str(file),
            'msg': None,
            'error': None,
            'status': True,
            'schema': event,
        }
    

def main(path):
    """Валидация json.

    PATH - путь к json файлу или катологу
    """
    path = Path(path)
    if path.is_dir():
        files = path.glob("*.json")
    else:
        files = [
            path,
        ]
    res_all = []
    for file in files:
        try:
            res = main_validator(file)
        except CustomValidateError as e:
            res_all.append(e.asdict())
        else:
            res_all.append(res)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = Path.cwd() / Path('log_' + timestamp + '.json')
    with log_file.open('w') as f:
        json.dump(res_all, f, ensure_ascii=False, indent=4)
    print("Валидация завершена")
    print(f"Лог файл {log_file}")
    
def cli():
    fire.Fire(main)
