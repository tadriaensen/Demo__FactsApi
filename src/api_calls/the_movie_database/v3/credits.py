from api_calls.api_call import ApiCall


class TmdbCredits(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self):
        pass
