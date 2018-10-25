from django.http import JsonResponse


def java_string_hashcode(string):
    string_hash = 0
    for char in string:
        string_hash = (31 * string_hash + ord(char)) & 0xFFFFFFFF
    return ((string_hash + 0x80000000) & 0xFFFFFFFF) - 0x80000000


class JsonResponseContainer:
    def __init__(self):
        self.data = {}
        self.status = 200

    def get_json_response(self):
        return JsonResponse(self.data, status=self.status)
