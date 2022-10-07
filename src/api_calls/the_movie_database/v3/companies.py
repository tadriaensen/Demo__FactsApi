from helpers.Rest import RestHelper
from api_calls.api_call import ApiCall


class TmdbCompanies(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self, company_id: str) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'company/{}'.format(company_id)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def get_alternative_names(self, company_id: str) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'company/{}/alternative_names'.format(company_id)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def get_images(self, company_id: str) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'company/{}/images'.format(company_id)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response
