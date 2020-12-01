import json
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
    res = []
    for file in files:
        message = {}
        decoded_json = json.loads(file.read_bytes())
        message['file'] = str(file)
        if not decoded_json:
            message['error'] = 'Некорректный json'
            message['status'] = False
            res.append(message)
            continue
        event = decoded_json["event"]
        data = decoded_json["data"]
        if not data:
            message['error'] = 'Невалидная разметка json (нет data key)'
            message['status'] = False
            res.append(message)
            continue
        if not event in validators.keys():
            message['error'] = 'Отсутствует json schema'
            message['status'] = False
            res.append(message)
            continue
        try:
            validators[event](**data)
        except ValidationError as e:
            message['schema'] = event
            message['error'] = json.loads(e.json())
            message['status'] = False
            res.append(message)
        else:
            message['status'] = True
            res.append(message)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = Path.cwd() / Path('log_' + timestamp + '.json')
    with log_file.open('w') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    print("Валидация завершена")
    
def cli():
    fire.Fire(main)
