from flask import Flask, render_template, request, make_response, jsonify, send_from_directory, redirect, abort, session, Response, send_file
from helpers.Rest import RestResponse
from werkzeug.exceptions import HTTPException
import utils.Config as ConfigUtils
import utils.Uuid as UuidUtils
from datetime import timedelta
from helpers.Json import JsonHelper
import utils.File as FileUtils
import utils.Numeric as NumericUtils

app = Flask(__name__)
app.secret_key = UuidUtils.generate_uuid(remove_hyphen=False)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


@app.route('/health', methods=['GET'])
def manage_health() -> Response:
    json_response = {'status': 'server is up and running'}

    response_output_type = 'JSON'
    if not isinstance(request.args.get('format'), type(None)):
        response_output_type = request.args.get('format')

    obj_response = RestResponse()
    return obj_response.create_response(response_code=200, response_json=json_response, output=response_output_type)


@app.route('/manage/reset', methods=['POST'])
def manage_reset() -> Response:
    response_output_type = 'JSON'
    if not isinstance(request.args.get('format'), type(None)):
        response_output_type = request.args.get('format')

    if __api_authentication_successful(request):
        obj_response = RestResponse()
        data_config = ConfigUtils.get_data_configuration()

        FileUtils.file_delete(full_file_path=data_config['response_body']['data_file_full_path'])
        if not FileUtils.file_exists(full_file_path=data_config['response_body']['data_file_full_path'], path_is_url=False):
            if FileUtils.file_copy(source_full_file_path=data_config['response_body']['data_reset_file_full_path'],
                                   target_path=data_config['response_body']['path'],
                                   new_file_name=data_config['response_body']['data_file_name']
                                   )['status'] == 'SUCCESS':
                return_value = obj_response.create_response(response_code=204, output=response_output_type)
            else:
                return_value = obj_response.create_error_response(response_code=500, output=response_output_type)
        else:
            return_value = obj_response.create_error_response(response_code=500, output=response_output_type)
    else:
        obj_response = RestResponse()
        return_value = obj_response.create_error_response(response_code=401, output='json')
    return return_value


@app.route('/subjects', methods=['GET', 'POST'])
def subjects() -> Response:
    obj_response = RestResponse()

    response_output_type = 'JSON'
    if not isinstance(request.args.get('format'), type(None)):
        response_output_type = request.args.get('format')

    if __api_authentication_successful(request):
        if request.method.upper() == 'GET':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_subjects = data_obj.get_element_value(element_path='subjects')['response_body']
            response_json = []
            for subject in dict_subjects:
                response_json.append({'subject_id': subject, 'subject_description': dict_subjects[subject]})
            return_value = obj_response.create_response(response_code=200, response_json=response_json, output=response_output_type)
        elif request.method.upper() == 'POST':
            return_value = ''
        else:
            return_value = obj_response.create_error_response(response_code=405, output=response_output_type)
    else:
        return_value = obj_response.create_error_response(response_code=401, output=response_output_type)
    return return_value


@app.route('/subjects/{subject_id}', methods=['GET', 'PUT', 'DELETE'])
def subjects_subjectid() -> Response:
    if __api_authentication_successful(request):
        obj_response = RestResponse()
        return_value = obj_response.create_error_response(response_code=501, output='json')
    else:
        obj_response = RestResponse()
        return_value = obj_response.create_error_response(response_code=401, output='json')
    return return_value


@app.route('/facts', methods=['GET', 'POST'])
def facts() -> Response:
    if __api_authentication_successful(request):
        obj_response = RestResponse()
        return_value = obj_response.create_error_response(response_code=501, output='json')
    else:
        obj_response = RestResponse()
        return_value = obj_response.create_error_response(response_code=401, output='json')
    return return_value


@app.route('/facts/{fact_id}', methods=['GET', 'PATCH', 'DELETE'])
def facts_factid() -> Response:
    if __api_authentication_successful(request):
        obj_response = RestResponse()
        return_value = obj_response.create_error_response(response_code=501, output='json')
    else:
        obj_response = RestResponse()
        return_value = obj_response.create_error_response(response_code=401, output='json')
    return return_value


@app.route('/facts/random', methods=['GET'])
def facts_random() -> Response:
    response_output_type = 'JSON'
    if not isinstance(request.args.get('format'), type(None)):
        response_output_type = request.args.get('format')

    if __api_authentication_successful(request):
        obj_response = RestResponse()
        data_config = ConfigUtils.get_data_configuration()['response_body']
        data_obj = JsonHelper()
        data_obj.load_file(full_file_path=data_config['data_file_full_path'])
        dict_facts = data_obj.get_element_value(element_path='facts')['response_body']
        fact_index = NumericUtils.get_random_number(len(dict_facts)-1)
        fact_key = data_obj.get_key_from_index(index_to_find=fact_index, element_path='facts')
        fact_obj = data_obj.get_element_value(element_path='facts.{}'.format(fact_key))['response_body']
        response_json = {'fact_id': fact_key,
                         'fact_description': fact_obj['description'],
                         'fact_subject_name': data_obj.get_element_value(element_path='subjects.{}'.format(fact_obj['subject_id']))['response_body']
                         }
        return_value = obj_response.create_response(response_code=200, response_json=response_json, output=response_output_type)
    else:
        obj_response = RestResponse()
        return_value = obj_response.create_error_response(response_code=401, output=response_output_type)
    return return_value


@app.errorhandler(HTTPException)
def http_error(error) -> Response:
    response_output_type = 'JSON'
    if not isinstance(request.args.get('format'), type(None)):
        response_output_type = request.args.get('format')

    obj_response = RestResponse()
    return obj_response.create_error_response(response_code=error.code, output=response_output_type)


def __api_authentication_successful(http_request: request) -> bool:
    proceed = False

    try:
        api_configuration = ConfigUtils.get_api_configuration()['response_body']
        if api_config['api_authentication']['enabled']:
            if http_request.headers.get('X-Api-Key') == api_configuration['api_authentication']['api_key']:
                proceed = True
        else:
            proceed = True
    except:
        pass

    return proceed


if __name__ == '__main__':
    rs = ConfigUtils.get_api_configuration()
    if rs['status'] == 'SUCCESS':
        api_config = rs['response_body']
        app.run(debug=api_config['api_service']['debug'], port=api_config['api_service']['port'])
    else:
        print('ERROR -- Service can\'t be started as an error occurred while loading the API configuration')
