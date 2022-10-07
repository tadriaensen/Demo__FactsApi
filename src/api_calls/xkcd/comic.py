from helpers.Rest import RestHelper
from api_calls.api_call import ApiCall


class XkcdComic(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def retrieve_current_comic(self) -> dict:
        obj_xkcd_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'info.0.json'
        request_header = None
        self.last_response = obj_xkcd_api.perform_get(path=request_path,
                                                      header=request_header,
                                                      auth=False,
                                                      debug=self.debug_enabled
                                                      )
        return self.last_response

    def retrieve_specific_comic(self, comic_nbr: int) -> dict:
        obj_xkcd_api = RestHelper(api_configuration=self.api_configuration)
        request_path = '{}/info.0.json'.format(comic_nbr)
        request_header = None
        self.last_response = obj_xkcd_api.perform_get(path=request_path,
                                                      header=request_header,
                                                      auth=False,
                                                      debug=self.debug_enabled
                                                      )
        return self.last_response
