import json
import boto3
class HandleJson:

    def __init__(self, filename='data.json'):
        self.filename = filename

    def write_data_to_json(self, data):
        with open(self.filename, 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def read_data_from_json(self):
        try:
            with open(self.filename, 'r', encoding="utf-8") as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            return {}

    def empty_json_file(self):
        try:
            with open(self.filename, 'w') as file:
                file.truncate(0)
            print("File 'data.json' emptied successfully")
        except Exception as e:
            print(f"Error emptying file 'data.json': {e}")
