import utils.Config as ConfigUtils


class ApiCall:
    def __init__(self, api_name: str, authentication_overwrite_default: dict = None):
        self.api_successfully_loaded = False
        self.api_configuration = None
        self.debug_enabled = False
        self.last_response = None
        try:
            api_config = ConfigUtils.get_api_configuration(api_name=api_name)
            if api_config['status'] == 'SUCCESS':
                self.api_configuration = api_config['response_body']

                if authentication_overwrite_default is not None:
                    self.api_configuration['authentication']['type'] = authentication_overwrite_default['type']
                    self.api_configuration['authentication']['username'] = authentication_overwrite_default['username']
                    self.api_configuration['authentication']['password'] = authentication_overwrite_default['password']
                    self.api_configuration['authentication']['api_key'] = authentication_overwrite_default['api_key']
                    self.api_configuration['authentication']['bearer_access_token'] = authentication_overwrite_default['bearer_access_token']

                self.api_successfully_loaded = True
        except:
            pass

    def enable_debug(self):
        self.debug_enabled = True

    def successfully_loaded(self) -> bool:
        return self.api_successfully_loaded
