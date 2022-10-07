from helpers.Json import JsonHelper
from helpers.Xml import XmlHelper
from requests.auth import HTTPBasicAuth
from flask import make_response
import utils.Url as UrlUtils
import urllib3
import requests
import json


class RestHelper:
    def __init__(self, api_configuration: dict):
        self.config_successfully_initialised = False

        self.request_auth = None
        self.request_ssl_verification = None
        self.request_method = None
        self.request_url = None
        self.request_header = None
        self.request_body = None
        self.request_execution_failed = None
        self.request_execution_error_message = None
        self.request_execution_debug = None
        self.request_response_statuscode = None
        self.request_response_body = None

        try:
            self.api_config = JsonHelper()
            self.api_config.load_dict(json_dict=api_configuration)

            if self.api_config.successfully_loaded():
                self.base_url = self.api_config.get_element_value(element_path='base_url')['response_body']
                self.config_successfully_initialised = True
        except:
            self.config_successfully_initialised = False

    def perform_delete(self, path: str = None, header: dict = None, auth: bool = True, body: str = None, debug: bool = False) -> dict:
        # DELETE request is used to delete the data on the server at a specified location.
        execution_result = self.__rest_call(method='DELETE',
                                            path=path,
                                            header=header,
                                            auth=auth,
                                            body=body,
                                            debug=debug)
        return execution_result

    def perform_get(self, path: str = None, header: dict = None, auth: bool = True, debug: bool = False) -> dict:
        # GET request is used to read/retrieve data from a web server.
        # GET returns an HTTP status code of 200 (OK) if the data is successfully retrieved from the server.
        execution_result = self.__rest_call(method='GET',
                                            path=path,
                                            header=header,
                                            auth=auth,
                                            debug=debug)
        return execution_result

    def perform_patch(self, path: str = None, header: dict = None, auth: bool = True, body: str = None, debug: bool = False) -> dict:
        # PATCH is similar to PUT request, but the only difference is, it modifies a part of the data.
        # It will only replace the content that you want to update.
        execution_result = self.__rest_call(method='PATCH',
                                            path=path,
                                            header=header,
                                            auth=auth,
                                            body=body,
                                            debug=debug)
        return execution_result

    def perform_post(self, path: str = None, header: dict = None, auth: bool = True, body: str = None, debug: bool = False) -> dict:
        # POST request is used to send data (file, form data, etc.) to the server.
        # On successful creation, it returns an HTTP status code of 201.
        execution_result = self.__rest_call(method='POST',
                                            path=path,
                                            header=header,
                                            auth=auth,
                                            body=body,
                                            debug=debug)
        return execution_result

    def perform_put(self, path: str = None, header: dict = None, auth: bool = True, body: str = None, debug: bool = False) -> dict:
        # PUT request is used to modify the data on the server.
        # It replaces the entire content at a particular location with data that is passed in the body payload.
        # If there are no resources that match the request, it will generate one.
        execution_result = self.__rest_call(method='PUT',
                                            path=path,
                                            header=header,
                                            auth=auth,
                                            body=body,
                                            debug=debug)
        return execution_result

    def successfully_initialised(self) -> bool:
        return self.config_successfully_initialised

    def __print_debug_details_response(self):
        if self.request_execution_debug:
            print()
            print('-- RESPONSE')
            print('-- ----------------------------------------------------------------------------')
            if self.request_execution_failed:
                print('Failed to parse response')
                print()
            else:
                print('StatusCode: {}'.format(self.request_response_statuscode))
                print('ResponseBody:')
                if self.request_response_body is None:
                    print('>> No body')
                else:
                    try:
                        tmp_obj = JsonHelper()
                        tmp_obj.load_dict(json_dict=self.request_response_body)
                        tmp_obj.print_to_console()
                    except:
                        print(self.request_response_body)
                print()

    def __print_debug_details_request(self):
        if self.request_execution_debug:
            print()
            print('-- REQUEST')
            print('-- ----------------------------------------------------------------------------')
            if self.request_execution_failed:
                print('Request failed')
                print()
            else:
                print('Method: {}'.format(self.request_method))
                print('Url: {}'.format(self.request_url))
                if self.request_auth:
                    print('Authentication: True')
                else:
                    print('Authentication: False')
                print('RequestSslVerification: {}'.format(self.request_ssl_verification))
                print('Header(s):')

                for header_entry in self.request_header:
                    print('   {}; {}'.format(header_entry, self.request_header[header_entry]))
                print('Body:')
                if self.request_body is None:
                    print('>> No body')
                else:
                    try:
                        tmp_obj = JsonHelper()
                        tmp_obj.load_dict(json_dict=self.request_body)
                        tmp_obj.print_to_console()
                    except:
                        print(self.request_body)

    def __reset_request(self):
        self.request_auth = None
        self.request_ssl_verification = None
        self.request_method = None
        self.request_url = None
        self.request_header = None
        self.request_body = None
        self.request_execution_failed = False
        self.request_execution_error_message = None
        self.request_execution_debug = None
        self.request_response_statuscode = None
        self.request_response_body = None

    def __rest_call(self, method: str, path: str, header: dict, auth: bool, debug: bool, body: str = None) -> dict:
        return_value = {'status': '', 'error_message': '', 'status_code': '', 'response_body': ''}

        self.__reset_request()

        # Setup request
        try:
            self.request_execution_debug = debug

            self.request_ssl_verification = False

            self.request_method = method

            if path is None or path.strip() == '':
                self.request_url = self.base_url
            else:
                self.request_url = '{}/{}'.format(self.base_url, path)

            self.request_header = {'Content-Type': 'application/json'}
            if header is not None:
                for header_entry in header:
                    self.request_header[header_entry] = header[header_entry]

            self.request_body = body

            request_http_auth = None
            if auth:
                auth_type = self.api_config.get_element_value(element_path='authentication.type')['response_body'].lower()
                if auth_type == 'http_auth__basic':
                    request_http_auth = HTTPBasicAuth(self.api_config.get_element_value(element_path='authentication.username')['response_body'], self.api_config.get_element_value(element_path='authentication.password')['response_body'])
                    self.request_auth = True
                elif auth_type == 'http_auth__baerer':
                    self.request_header['Authorization'] = 'Bearer {}'.format(self.api_config.get_element_value(element_path='authentication.bearer_access_token')['response_body'])
                    self.request_auth = True
                elif auth_type == 'api_key__header':
                    self.request_header['X-API-Key'] = self.api_config.get_element_value(element_path='authentication.api_key')['response_body']
                    self.request_auth = True
                elif auth_type == 'api_key__query_string':
                    query_string = 'api_key={}'.format(self.api_config.get_element_value(element_path='authentication.api_key')['response_body'])
                    if UrlUtils.url_has_query_string(url=self.request_url):
                        self.request_url = '{}&{}'.format(self.request_url, query_string)
                    else:
                        self.request_url = '{}?{}'.format(self.request_url, query_string)
                    self.request_auth = True
                else:
                    self.request_auth = False
            else:
                self.request_auth = False
        except:
            request_http_auth = None
            self.request_execution_failed = True
            self.request_execution_error_message = 'Request setup failed'

        self.__print_debug_details_request()

        # Execute request
        if not self.request_execution_failed:
            try:
                urllib3.disable_warnings()
                response = requests.request(method=self.request_method,
                                            url=self.request_url,
                                            headers=self.request_header,
                                            auth=request_http_auth,
                                            verify=self.request_ssl_verification)
                self.request_response_statuscode = response.status_code
                try:
                    self.request_response_body = json.loads(response.text)
                except:
                    self.request_response_body = response.text
            except:
                self.request_response_statuscode = None
                self.request_response_body = None
                self.request_execution_failed = True
                self.request_execution_error_message = 'Request execution failed'

            self.__print_debug_details_response()

        # Create response
        if self.request_execution_failed:
            return_value['status'] = 'FAILED'
        else:
            return_value['status'] = 'SUCCESS'

        return_value['error_message'] = self.request_execution_error_message

        return_value['status_code'] = self.request_response_statuscode

        return_value['response_body'] = self.request_response_body

        return return_value


class RestResponse:
    def __init__(self):
        self.config_successfully_initialised = True
        self.error_list = {
            401: {'code': 401, 'message': 'Unauthorized'},
            402: {'code': 402, 'message': 'Paymet Required'},
            403: {'code': 403, 'message': 'Forbidden'},
            404: {'code': 404, 'message': 'Not Found'},
            405: {'code': 405, 'message': 'Method Not Allowed'},
            406: {'code': 406, 'message': 'Not Acceptable'},
            407: {'code': 407, 'message': 'Proxy Authentication Required'},
            408: {'code': 408, 'message': 'Request Timeout'},
            409: {'code': 409, 'message': 'Conflict'},
            410: {'code': 410, 'message': 'Gone'},
            500: {'code': 500, 'message': 'Internal Server Error'},
            501: {'code': 501, 'message': 'Not Implemented'},
            503: {'code': 503, 'message': 'Service Unavailable'}
        }

    def successfully_initialised(self) -> bool:
        return self.config_successfully_initialised

    def create_response(self, response_code: int, response_json: dict | list = None, output: str = 'JSON'):
        if response_json is None:
            response_json = {}
        if self.config_successfully_initialised:
            if output.upper() == 'JSON':
                return_value = make_response(response_json, response_code)
            elif output.upper() == 'XML':
                obj_response = XmlHelper()
                obj_response.load_dict(xml_dict=response_json)
                response_xml = obj_response.get_as_xml_string()['response_body']
                return_value = make_response(response_xml, response_code)
            else:
                return_value = make_response(response_json, response_code)
        else:
            return_value = create_error_response(response_code=500, output='JSON')

        return return_value

    def create_error_response(self, response_code: int, output='JSON'):
        if self.error_list.get(response_code) is None:
            response_code = 500

        response_json = self.error_list.get(response_code)
        if output.upper() == 'JSON':
            return_value = make_response(response_json, response_code)
        elif output.upper() == 'XML':
            obj_response = XmlHelper()
            obj_response.load_dict(xml_dict=response_json)
            response_xml = obj_response.get_as_xml_string()['response_body']
            return_value = make_response(response_xml, response_code)
        else:
            return_value = make_response(response_json, response_code)

        return return_value
