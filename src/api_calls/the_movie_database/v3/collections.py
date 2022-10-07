from api_calls.api_call import ApiCall


class TmdbCollections(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self) -> dict:
        pass

    def get_images(self) -> dict:
        pass

    def get_translations(self) -> dict:
        pass
