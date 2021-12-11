import json


class ImageClassificationRequest:

    def __init__(self, request_id, folder_path):
        self.request_id = request_id
        self.folder_path = folder_path

    def key_bytes(self):
        return bytes(self.request_id, encoding='utf-8')

    def to_json(self):
        payload = {
            'request_id': self.request_id,
            'folder_path': self.folder_path
        }
        return json.dumps(payload)

    def to_bytes(self):
        return bytes(self.to_json(), encoding='utf-8')

    @staticmethod
    def from_json(json_str):
        payload = json.loads(json_str)
        return ImageClassificationRequest(payload['request_id'], payload['folder_path'])

    @staticmethod
    def from_bytes(payload):
        json_str = str(payload, encoding='utf-8')
        return ImageClassificationRequest.from_json(json_str)

