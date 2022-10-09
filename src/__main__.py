from flask import Flask, render_template, request, make_response, jsonify, send_from_directory, redirect, abort, session, Response, send_file
from helpers.Rest import RestResponse
from werkzeug.exceptions import HTTPException
import utils.Config as ConfigUtils
import utils.Uuid as UuidUtils
from datetime import timedelta
from helpers.Json import JsonHelper
import utils.File as FileUtils
import utils.Numeric as NumericUtils
import utils.Lists as ListUtils


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

    request_payload = ''
    try:
        if not isinstance(request.json, type(None)):
            request_payload = request.json
    except:
        request_payload = ''

    if __api_authentication_successful(request):
        if request.method.upper() == 'GET':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_subjects = data_obj.get_element_value(element_path='subjects')['response_body']
            response_json = []
            for subject in dict_subjects:
                response_json.append({'subject_id': subject, 'subject_name': dict_subjects[subject]})
            return_value = obj_response.create_response(response_code=200, response_json=response_json, output=response_output_type)
        elif request.method.upper() == 'POST':
            if request_payload.get('subject_name') is not None and str(request_payload.get('subject_name')).strip() != '':
                generated_key = UuidUtils.generate_uuid()
                data_config = ConfigUtils.get_data_configuration()['response_body']
                data_obj = JsonHelper()
                data_obj.load_file(full_file_path=data_config['data_file_full_path'])
                dict_subjects = data_obj.get_as_dict()['subjects']

                subject_exists = False
                for subject in dict_subjects:
                    if (str(dict_subjects[subject]).strip()).lower() == (str(request_payload.get('subject_name')).strip()).lower():
                        subject_exists = True

                if not subject_exists:
                    dict_subjects[generated_key] = request_payload.get('subject_name')
                    data_obj.save(full_file_path=data_config['data_file_full_path'], overwrite=True)
                    response_json = {'subject_id': generated_key}
                    return_value = obj_response.create_response(response_code=201, response_json=response_json, output=response_output_type)
                else:
                    return_value = obj_response.create_error_response(response_code=403, output=response_output_type)
            else:
                return_value = obj_response.create_error_response(response_code=400, output=response_output_type)
        else:
            return_value = obj_response.create_error_response(response_code=405, output=response_output_type)
    else:
        return_value = obj_response.create_error_response(response_code=401, output=response_output_type)

    return return_value


@app.route('/subjects/<string:subject_id>', methods=['GET', 'PUT', 'DELETE'])
def subjects_subjectid(subject_id) -> Response:
    obj_response = RestResponse()

    response_output_type = 'JSON'
    if not isinstance(request.args.get('format'), type(None)):
        response_output_type = request.args.get('format')

    request_payload = ''
    try:
        if not isinstance(request.json, type(None)):
            request_payload = request.json
    except:
        request_payload = ''

    if __api_authentication_successful(request):
        if request.method.upper() == 'GET':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_subject = data_obj.get_element_value('subjects.{}'.format(subject_id))
            if dict_subject['status'] == 'SUCCESS':
                dict_subject = dict_subject['response_body']
                response_json = {'subject_id': subject_id, 'subject_name': dict_subject}
                return_value = obj_response.create_response(response_code=200, response_json=response_json, output=response_output_type)
            else:
                return_value = obj_response.create_error_response(response_code=404, output=response_output_type)
        elif request.method.upper() == 'PUT':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_subjects = data_obj.get_as_dict()['subjects']
            dict_subject = data_obj.get_element_value('subjects.{}'.format(subject_id))
            if dict_subject['status'] == 'SUCCESS':
                subject_exists = False
                for subject in dict_subjects:
                    if (str(dict_subjects[subject]).strip()).lower() == (str(request_payload.get('subject_name')).strip()).lower():
                        subject_exists = True

                if not subject_exists:
                    dict_subjects[subject_id] = request_payload.get('subject_name')
                    data_obj.save(full_file_path=data_config['data_file_full_path'], overwrite=True)
                    return_value = obj_response.create_response(response_code=204, output=response_output_type)
                else:
                    return_value = obj_response.create_error_response(response_code=403, output=response_output_type)
            else:
                return_value = obj_response.create_error_response(response_code=404, output=response_output_type)
        elif request.method.upper() == 'DELETE':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_subjects = data_obj.get_element_value('subjects')['response_body']
            dict_facts = data_obj.get_element_value('facts')['response_body']
            try:
                dict_subjects.pop(subject_id)

                lst_fact_to_delete = []
                for fact in dict_facts:
                    if dict_facts[fact]['subject_id'] == subject_id:
                        lst_fact_to_delete.append(fact)
                for fact_id in lst_fact_to_delete:
                    dict_facts.pop(fact_id)

                data_obj.save(full_file_path=data_config['data_file_full_path'], overwrite=True)
                return_value = obj_response.create_response(response_code=204, output=response_output_type)
            except:
                return_value = obj_response.create_error_response(response_code=404, output=response_output_type)
        else:
            return_value = obj_response.create_error_response(response_code=405, output=response_output_type)
    else:
        return_value = obj_response.create_error_response(response_code=401, output=response_output_type)

    return return_value


@app.route('/facts', methods=['GET', 'POST'])
def facts() -> Response:
    obj_response = RestResponse()

    response_output_type = 'JSON'
    if not isinstance(request.args.get('format'), type(None)):
        response_output_type = request.args.get('format')

    request_payload = ''
    try:
        if not isinstance(request.json, type(None)):
            request_payload = request.json
    except:
        request_payload = ''

    if __api_authentication_successful(request):
        if request.method.upper() == 'GET':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_subjects = data_obj.get_element_value(element_path='subjects')['response_body']
            dict_facts = data_obj.get_element_value(element_path='facts')['response_body']

            response_json = {}
            for subject in dict_subjects:
                response_json[dict_subjects[subject]] = []

            for fact in dict_facts:
                tmp_fact = {'fact_id': fact, 'fact_description': dict_facts[fact]['description']}
                response_json[dict_subjects[dict_facts[fact]['subject_id']]].append(tmp_fact)

            return_value = obj_response.create_response(response_code=200, response_json=response_json, output=response_output_type)
        elif request.method.upper() == 'POST':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_facts = data_obj.get_element_value(element_path='facts')['response_body']

            fact_description = (str(request_payload.get('fact_description')).strip())
            fact_subject_id = (str(request_payload.get('fact_subject_id')).strip())

            if data_obj.get_element_value('subjects.{}'.format(fact_subject_id))['status'] == 'SUCCESS':
                generated_uuid = UuidUtils.generate_uuid()
                dict_facts[generated_uuid] = {}
                dict_facts[generated_uuid]['description'] = fact_description
                dict_facts[generated_uuid]['subject_id'] = fact_subject_id
                data_obj.save(full_file_path=data_config['data_file_full_path'], overwrite=True)
                response_json = {'fact_id': generated_uuid}
                return_value = obj_response.create_response(response_code=201, response_json=response_json, output=response_output_type)
            else:
                return_value = obj_response.create_error_response(response_code=403, output=response_output_type)
        else:
            return_value = obj_response.create_error_response(response_code=405, output=response_output_type)
    else:
        return_value = obj_response.create_error_response(response_code=401, output=response_output_type)

    return return_value


@app.route('/facts/<string:fact_id>', methods=['GET', 'PATCH', 'DELETE'])
def facts_factid(fact_id) -> Response:
    obj_response = RestResponse()

    response_output_type = 'JSON'
    if not isinstance(request.args.get('format'), type(None)):
        response_output_type = request.args.get('format')

    request_payload = ''
    try:
        if not isinstance(request.json, type(None)):
            request_payload = request.json
    except:
        request_payload = ''

    if __api_authentication_successful(request):
        if request.method.upper() == 'GET':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_subjects = data_obj.get_element_value(element_path='subjects')['response_body']
            dict_facts = data_obj.get_element_value(element_path='facts')['response_body']

            if data_obj.get_element_value(element_path='facts.{}'.format(fact_id))['status'] == 'SUCCESS':
                if data_obj.get_element_value(element_path='subjects.{}'.format(dict_facts[fact_id]['subject_id']))['status'] == 'SUCCESS':
                    response_json = {'fact_id': fact_id,
                                     'fact_description': dict_facts[fact_id]['description'],
                                     'fact_subject_name': dict_subjects[dict_facts[fact_id]['subject_id']]
                                     }
                    return_value = obj_response.create_response(response_code=200, response_json=response_json, output=response_output_type)
                else:
                    return_value = obj_response.create_error_response(response_code=403, output=response_output_type)
            else:
                return_value = obj_response.create_error_response(response_code=404, output=response_output_type)
        elif request.method.upper() == 'PATCH':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_facts = data_obj.get_element_value(element_path='facts')['response_body']

            subject_id = (str(request_payload.get('subject_id')).strip())

            if data_obj.get_element_value(element_path='facts.{}'.format(fact_id))['status'] == 'SUCCESS':
                if data_obj.get_element_value(element_path='subjects.{}'.format(subject_id))['status'] == 'SUCCESS':
                    dict_facts[fact_id]['subject_id'] = subject_id
                    data_obj.save(full_file_path=data_config['data_file_full_path'], overwrite=True)
                    return_value = obj_response.create_response(response_code=204, output=response_output_type)
                else:
                    return_value = obj_response.create_error_response(response_code=403, output=response_output_type)
            else:
                return_value = obj_response.create_error_response(response_code=404, output=response_output_type)
        elif request.method.upper() == 'DELETE':
            data_config = ConfigUtils.get_data_configuration()['response_body']
            data_obj = JsonHelper()
            data_obj.load_file(full_file_path=data_config['data_file_full_path'])
            dict_facts = data_obj.get_element_value(element_path='facts')['response_body']

            if data_obj.get_element_value(element_path='facts.{}'.format(fact_id))['status'] == 'SUCCESS':
                dict_facts.pop(fact_id)

                data_obj.save(full_file_path=data_config['data_file_full_path'], overwrite=True)
                return_value = obj_response.create_response(response_code=204, output=response_output_type)
            else:
                return_value = obj_response.create_error_response(response_code=404, output=response_output_type)
        else:
            return_value = obj_response.create_error_response(response_code=405, output=response_output_type)
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
