import json
import utils.File as FileUtils


class JsonHelper:
    def __init__(self):
        self.json_object = {}
        self.json_successfully_loaded = False

    def element_available(self, element_path: str) -> bool:
        try:
            tmp_json_object = self.json_object

            path_list = element_path.split('.')
            for el in path_list:
                if el.isnumeric():
                    tmp_json_object = tmp_json_object[int(el)]
                else:
                    tmp_json_object = tmp_json_object[el]

            return_value = True
        except:
            return_value = False

        return return_value

    def get_as_dict(self) -> dict:
        return self.json_object

    def get_as_string(self, formatted: bool = False) -> str:
        if formatted:
            return_value = json.dumps(self.json_object, indent=2)
        else:
            return_value = json.dumps(self.json_object)
        return return_value

    def get_element_value(self, element_path: str) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            tmp_json_object = self.json_object

            path_list = element_path.split('.')
            for el in path_list:
                if el.isnumeric():
                    tmp_json_object = tmp_json_object[int(el)]
                else:
                    tmp_json_object = tmp_json_object[el]

            return_value['status'] = 'SUCCESS'
            return_value['response_body'] = tmp_json_object
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to retrieve element value'

        return return_value

    def get_index_from_key(self, key_to_find: str, element_path: str = None) -> int:
        if element_path is None:
            dict_to_search = self.json_object
        else:
            dict_to_search = self.get_element_value(element_path=element_path)['response_body']
        for index, key in enumerate(dict_to_search.keys()):
            if key == key_to_find:
                return index
        return None  # the key doesn't exist

    def get_key_from_index(self, index_to_find: int, element_path: str = None) -> str:
        if element_path is None:
            dict_to_search = self.json_object
        else:
            dict_to_search = self.get_element_value(element_path=element_path)['response_body']
        for index, key in enumerate(dict_to_search.keys()):
            if index == index_to_find:
                return key
        return None  # the index doesn't exist

    def load_dict(self, json_dict: dict) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            self.json_object = json_dict
            return_value['status'] = 'SUCCESS'
            self.json_successfully_loaded = True
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to parse dict as JSON object'

        return return_value

    def load_file(self, full_file_path: str) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        res = FileUtils.file_read(full_file_path=full_file_path)
        if res['status'] == 'SUCCESS':
            try:
                self.json_object = json.loads(res['response_body'])
                return_value['status'] = 'SUCCESS'
                self.json_successfully_loaded = True
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unable to parse file as JSON object'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = res['error_message']

        return return_value

    def load_string(self, json_string: str) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}

        try:
            self.json_object = json.loads(json_string)
            return_value['status'] = 'SUCCESS'
            self.json_successfully_loaded = True
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to parse string as JSON object'

        return return_value

    def print_to_console(self, element_path: str = None):
        if element_path is None:
            value2print = self.json_object
        else:
            res = self.get_element_value(element_path=element_path)
            if res['status'] == 'SUCCESS':
                value2print = res['response_body']
            else:
                value2print = {}
        print(json.dumps(value2print, indent=2))

    def save(self, full_file_path: str, overwrite: bool = True) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}
        continue_execution = True

        if FileUtils.file_exists(full_file_path=full_file_path):
            if not overwrite:
                continue_execution = False
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'File already exists'
            else:
                if FileUtils.file_delete(full_file_path=full_file_path)['status'] == 'FAILED':
                    continue_execution = False
                    return_value['status'] = 'FAILED'
                    return_value['error_message'] = 'Unable to overwrite file'

        if continue_execution:
            try:
                res = FileUtils.file_create(full_file_path=full_file_path, content=json.dumps(self.json_object, indent=4), overwrite=True, encoding='utf-8')['status']
                if res['status'] == 'SUCCESS':
                    return_value['status'] = 'SUCCESS'
                else:
                    return_value['status'] = 'FAILED'
                    return_value['error_message'] = 'Unable to save file'
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unable to save file'

        return return_value

    def successfully_loaded(self) -> bool:
        return self.json_successfully_loaded
