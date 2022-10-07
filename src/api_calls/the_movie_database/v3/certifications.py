from helpers.Rest import RestHelper
from api_calls.api_call import ApiCall


class TmdbCertifications(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_movie_certifications(self) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'certification/movie/list'
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def get_tv_certifications(self) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'certification/tv/list'
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response
