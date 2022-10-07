from helpers.Rest import RestHelper
from api_calls.api_call import ApiCall


class TmdbAccounts(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self, session_id: str) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'account?session_id={}'.format(session_id)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def get_created_lists(self, session_id: str, account_id: str = None, language: str = None, page: int = None) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        if account_id is not None:
            request_path = 'account/{account_id}/lists?session_id={session_id}'.format(account_id=account_id, session_id=session_id)
        else:
            request_path = 'account/{account_id}/lists?session_id={session_id}'.format(account_id=account_id, session_id=session_id)
        if language is not None:
            request_path = '{request_path}&language={language}'.format(request_path=request_path, language=language)
        if page is not None:
            request_path = '{request_path}&page={page}'.format(request_path=request_path, page=page)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def get_favorite_movies(self, session_id: str, account_id: str = None, language: str = None, sort_by: str = None, page: int = None) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'account/{account_id}/favorite/movies?session_id={session_id}'.format(account_id=account_id, session_id=session_id)
        if language is not None:
            request_path = '{request_path}&language={language}'.format(request_path=request_path, language=language)
        if sort_by is not None:
            request_path = '{request_path}&sort_by={sort_by}'.format(request_path=request_path, sort_by=sort_by)
        if page is not None:
            request_path = '{request_path}&page={page}'.format(request_path=request_path, page=page)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def get_favorite_tv_shows(self, session_id: str, account_id: str = None, language: str = None, sort_by: str = None, page: int = None) -> dict:
        obj_api = RestHelper(api_configuration=self.api_configuration)
        request_path = 'account/{account_id}/favorite/tv?session_id={session_id}'.format(account_id=account_id, session_id=session_id)
        if language is not None:
            request_path = '{request_path}&language={language}'.format(request_path=request_path, language=language)
        if sort_by is not None:
            request_path = '{request_path}&sort_by={sort_by}'.format(request_path=request_path, sort_by=sort_by)
        if page is not None:
            request_path = '{request_path}&page={page}'.format(request_path=request_path, page=page)
        request_header = None
        self.last_response = obj_api.perform_get(path=request_path,
                                                 header=request_header,
                                                 auth=True,
                                                 debug=self.debug_enabled
                                                 )
        return self.last_response

    def mark_as_favorite(self) -> dict:
        pass

    def get_rated_movies(self) -> dict:
        pass

    def get_rated_tv_shows(self) -> dict:
        pass

    def get_rated_tv_episodes(self) -> dict:
        pass

    def get_movie_watchlist(self) -> dict:
        pass

    def get_tv_show_watchlist(self) -> dict:
        pass

    def add_to_watchlist(self) -> dict:
        pass
