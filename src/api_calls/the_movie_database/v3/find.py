from api_calls.api_call import ApiCall


class TmdbCertifications(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def find_by_id(self) -> dict:
        pass
