from api_calls.api_call import ApiCall


class TmdbAuthentication(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def create_guest_session(self) -> dict:
        pass

    def create_request_token(self) -> dict:
        pass

    def create_session(self) -> dict:
        pass

    def create_session_with_login(self) -> dict:
        pass

    def create_session_from_v4_access_token(self) -> dict:
        pass

    def delete_session(self) -> dict:
        pass
