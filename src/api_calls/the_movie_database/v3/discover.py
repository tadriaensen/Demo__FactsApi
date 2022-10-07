from api_calls.api_call import ApiCall


class TmdbDiscover(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def movie_discover(self) -> dict:
        pass

    def tv_discover(self) -> dict:
        pass
