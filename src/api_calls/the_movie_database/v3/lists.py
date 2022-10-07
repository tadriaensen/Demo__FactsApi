from api_calls.api_call import ApiCall


class TmdbLists(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self):
        pass

    def check_item_status(self):
        pass

    def create_list(self):
        pass

    def add_movie(self):
        pass

    def remove_movie(self):
        pass

    def clear_list(self):
        pass

    def delete_list(self):
        pass
