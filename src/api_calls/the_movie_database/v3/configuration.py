from api_calls.api_call import ApiCall


class TmdbConfiguration(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_api_configuration(self):
        pass

    def get_countries(self):
        pass

    def get_jobs(self):
        pass

    def get_languages(self):
        pass

    def get_primary_translations(self):
        pass

    def get_timezones(self):
        pass


