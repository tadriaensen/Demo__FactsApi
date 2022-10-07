from helpers.Rest import RestHelper
from api_calls.api_call import ApiCall


class TmdbSearch(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def search_companies(self, query: str, page: int = None) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        if page is None:
            request_path = 'search/company?query={}&page={}'.format(query, page)
        else:
            request_path = 'search/company?query={}'.format(query)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def search_collections(self):
        pass

    def search_keywords(self):
        pass

    def search_movies(self, query: str, page: int = None) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        if page is None:
            request_path = 'search/movie?query={}&page={}'.format(query, page)
        else:
            request_path = 'search/movie?query={}'.format(query)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def search_multi_search(self):
        pass

    def search_people(self, query: str, page: int = None) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        if page is None:
            request_path = 'search/person?query={}&page={}'.format(query, page)
        else:
            request_path = 'search/person?query={}'.format(query)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def search_tv_shows(self, query: str, page: int = None) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        if page is None:
            request_path = 'search/tv?query={}&page={}'.format(query, page)
        else:
            request_path = 'search/tv?query={}'.format(query)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response
