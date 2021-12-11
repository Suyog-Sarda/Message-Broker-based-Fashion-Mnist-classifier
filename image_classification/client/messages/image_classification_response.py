import json


class ImageClassificationResponse:

    def __init__(self, request_id, results):
        self.request_id = request_id
        self.results = results

    def key_bytes(self):
        return bytes(self.request_id, encoding='utf-8')

    def to_json(self):
        payload = {
            'request_id': self.request_id,
            'results': self.results
        }
        return json.dumps(payload)

    def to_bytes(self):
        return bytes(self.to_json(), encoding='utf-8')

    @staticmethod
    def from_json(json_str):
        payload = json.loads(json_str)
        return ImageClassificationResponse(payload['request_id'], payload['results'])

    @staticmethod
    def from_bytes(payload):
        json_str = str(payload, encoding='utf-8')
        return ImageClassificationResponse.from_json(json_str)

