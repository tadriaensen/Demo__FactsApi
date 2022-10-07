from api_calls.api_call import ApiCall


class TmdbSessions(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_rates_movies(self) -> dict:
        pass

    def get_rated_tv_shows(self) -> dict:
        pass

    def get_rated_episodes(self) -> dict:
        pass
