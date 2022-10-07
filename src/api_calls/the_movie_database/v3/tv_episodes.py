from api_calls.api_call import ApiCall


class TmdbEpisodes(ApiCall):
    def __init__(self, api_name: str):
        super().__init__(api_name=api_name)

    def get_details(self) -> dict:
        pass

    def get_account_states(self) -> dict:
        pass

    def get_changes(self) -> dict:
        pass

    def get_credits(self) -> dict:
        pass

    def get_external_ids(self) -> dict:
        pass

    def get_images(self) -> dict:
        pass

    def get_translations(self) -> dict:
        pass

    def rate_tv_episode(self) -> dict:
        pass

    def delete_rating(self) -> dict:
        pass

    def get_videos(self) -> dict:
        pass
