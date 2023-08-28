import json
import boto3


class HandleJson:

    def __init__(self, bucket_name='json-for-mehir-lamishtaken', object_key='data/data.json'):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.s3 = boto3.client('s3')

    def write_data_to_json(self, data):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=self.object_key)
            current_data = json.loads(response['Body'].read().decode('utf-8'))
        except Exception:
            current_data = {}
        current_data.update(data)
        updated_json = json.dumps(current_data)
        self.s3.put_object(Body=updated_json, Bucket=self.bucket_name, Key=self.object_key)

    def read_data_from_json(self):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=self.object_key)
            data = json.loads(response['Body'].read().decode('utf-8'))
            return data
        except Exception as e:
            print(f"Error reading data from S3: {e}")
            return {}

    def empty_json_file(self):
        try:
            empty_data = {}
            empty_json = json.dumps(empty_data)
            self.s3.put_object(Body=empty_json, Bucket=self.bucket_name, Key=self.object_key)
            print("File emptied successfully")
        except Exception as e:
            print(f"Error emptying file: {e}")
