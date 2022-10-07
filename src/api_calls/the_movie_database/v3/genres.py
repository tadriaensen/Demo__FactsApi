from api_calls.api_call import ApiCall


class TmdbGenres(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_movie_list(self):
        pass

    def get_tv_list(self):
        pass
