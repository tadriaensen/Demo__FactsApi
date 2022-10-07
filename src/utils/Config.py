from pathlib import Path
from helpers.Json import JsonHelper
import utils.File as FileUtils


def get_project_root() -> str:
    return str(Path(__file__).parent.parent)


def get_project_resource_location() -> str:
    return FileUtils.path_join(path=get_project_root(), filename_or_foldername='resources')


def get_system_configuration() -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}

    obj_config = JsonHelper()
    obj_config.load_file(full_file_path=FileUtils.path_join(path=get_project_resource_location(), filename_or_foldername='config_system.json'))
    if obj_config.successfully_loaded():
        return_value['status'] = 'SUCCESS'
        return_value['response_body'] = obj_config.get_as_dict()
    else:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to load system configuration'

    return return_value


def get_api_configuration() -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}

    obj_config = JsonHelper()
    obj_config.load_file(full_file_path=FileUtils.path_join(path=get_project_resource_location(), filename_or_foldername='config_api.json'))
    if obj_config.successfully_loaded():
        return_value['status'] = 'SUCCESS'
        return_value['response_body'] = obj_config.get_as_dict()
    else:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to load api configuration'

    return return_value


def get_data_configuration() -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}

    folder_path = FileUtils.path_join(path=get_project_root(), filename_or_foldername='data')
    return_value['response_body']['path'] = folder_path
    return_value['response_body']['data_file_name'] = 'data.json'
    return_value['response_body']['data_file_full_path'] = FileUtils.path_join(path=folder_path, filename_or_foldername=return_value['response_body']['data_file_name'])
    return_value['response_body']['data_reset_file_name'] = 'data_reset.json'
    return_value['response_body']['data_reset_file_full_path'] = FileUtils.path_join(path=folder_path, filename_or_foldername=return_value['response_body']['data_reset_file_name'])

    return return_value
