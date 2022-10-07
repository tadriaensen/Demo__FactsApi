from api_calls.api_call import ApiCall


class TmdbPeople(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self):
        pass

    def get_changes(self):
        pass

    def get_movie_credits(self):
        pass

    def get_tv_credits(self):
        pass

    def get_combined_credits(self):
        pass

    def get_external_ids(self):
        pass

    def get_images(self):
        pass

    def get_tagged_images(self):
        pass

    def get_translations(self):
        pass

    def get_latest(self):
        pass

    def get_popular(self):
        pass
