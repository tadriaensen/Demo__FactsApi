from api_calls.api_call import ApiCall


class TmdbNetworks(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self):
        pass

    def get_alternative_names(self):
        pass

    def get_images(self):
        pass
