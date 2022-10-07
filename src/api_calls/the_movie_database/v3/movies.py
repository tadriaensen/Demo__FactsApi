from api_calls.api_call import ApiCall


class TmdbMovies(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self):
        pass

    def get_account_states(self):
        pass

    def get_alternative_titles(self):
        pass

    def get_changes(self):
        pass

    def get_credits(self):
        pass

    def get_external_ids(self):
        pass

    def get_images(self):
        pass

    def get_keywords(self):
        pass

    def get_lists(self):
        pass

    def get_recommendations(self):
        pass

    def get_release_dates(self):
        pass

    def get_reviews(self):
        pass

    def get_similar_movies(self):
        pass

    def get_videos(self):
        pass

    def get_watch_providers(self):
        pass

    def rate_movie(self):
        pass

    def delete_rating(self):
        pass

    def get_latest(self):
        pass

    def get_now_playing(self):
        pass

    def get_popular(self):
        pass

    def get_top_rated(self):
        pass

    def get_upcoming(self):
        pass
