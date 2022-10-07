import utils.Config as ConfigUtils
import utils.String as StringUtils
import utils.File as FileUtils
import utils.DateTime as DateTimeUtils


class LoggingHelper:
    def __init__(self):
        self.log_file = {}
        self.logging_successfully_initialised = False

        obj_config = ConfigUtils.get_system_configuration()
        if obj_config['status'] == 'SUCCESS':
            obj_config = obj_config['response_body']
            self.config_log_level = obj_config.get_element_value(element_path='logging.log_level')['response_body']

            self.console_logging_enabled = obj_config.get_element_value(element_path='logging.console.enabled')['response_body']

            self.file_logging_enabled = obj_config.get_element_value(element_path='logging.file.enabled')['response_body']
            self.log_file_path = obj_config.get_element_value(element_path='logging.file.path')['response_body']
            self.log_file_name = obj_config.get_element_value(element_path='logging.file.file_name')['response_body']
            self.log_file_full_file_path = FileUtils.path_join(path=self.log_file_path, filename_or_foldername=self.log_file_name)
            self.log_file_max_file_size_kilobyte = obj_config.get_element_value(element_path='logging.file.max_file_size_kilobyte')['response_body']

            if self.file_logging_enabled:
                if FileUtils.directory_exists(path=self.log_file_path):
                    self.logging_successfully_initialised = True
            else:
                self.logging_successfully_initialised = True

    def add(self, log_level: str, component: str | None, message: str):
        if log_level.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            # LOGLEVEL CONFIGURATION
            # ALL; Messages with loglevel DEBUG, INFO, WARNING and ERROR are reported
            if self.config_log_level.upper() == 'ALL' and log_level.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
                self.__add_log_entry(log_level=log_level, component=component, message=message)
            # DEBUG; Messages with loglevel DEBUG, INFO, WARNING and ERROR are reported
            elif self.config_log_level.upper() == 'DEBUG' and log_level.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
                self.__add_log_entry(log_level=log_level, component=component, message=message)
            # INFO; Messages with loglevel INFO, WARNING and ERROR are reported
            elif self.config_log_level.upper() == 'INFO' and log_level.upper() in ['INFO', 'WARNING', 'ERROR']:
                self.__add_log_entry(log_level=log_level, component=component, message=message)
            # WARNING; Messages with loglevel WARNING and ERROR are reported
            elif self.config_log_level.upper() == 'WARNING' and log_level.upper() in ['WARNING', 'ERROR']:
                self.__add_log_entry(log_level=log_level, component=component, message=message)
            # ERROR; Messages with loglevel ERROR are reported
            elif self.config_log_level.upper() == 'ERROR' and log_level.upper() in ['ERROR']:
                self.__add_log_entry(log_level=log_level, component=component, message=message)
            # OFF; Nothing is logged
            else:
                pass
        else:
            self.__add_log_entry_to_console(log_level='ERROR', component='SYSTEM', message='Log level {} not supported, only the levels DEBUG, INFO, WARNING and ERROR are allowed.'.format(log_level.upper()))

    def clear(self) -> dict:
        return_value = {'status': '', 'error_message': '', 'response_body': ''}
        try:
            if FileUtils.file_exists(full_file_path=self.log_file_full_file_path):
                if FileUtils.file_delete(full_file_path=self.log_file_full_file_path)['status'] == 'SUCCESS':
                    return_value['status'] = 'SUCCESS'
                else:
                    return_value['status'] = 'FAILED'
                    return_value['error_message'] = 'Unable to delete the log file'
            else:
                return_value['status'] = 'SUCCESS'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Something went wrong when clearing the logging'

        return return_value

    def successfully_initialised(self) -> bool:
        return self.logging_successfully_initialised

    def __add_log_entry(self, log_level: str, component: str | None, message: str):
        if self.console_logging_enabled:
            self.__add_log_entry_to_console(log_level=log_level, component=component, message=message)

        if self.file_logging_enabled:
            self.__add_log_entry_to_file(log_level=log_level, component=component, message=message)

    @staticmethod
    def __add_log_entry_to_console(log_level: str, component: str | None, message: str):
        if StringUtils.none2string(component) == '':
            log_entry = '{} -- {} -- {}'.format(DateTimeUtils.get_timestamp_formatted_iso(), log_level, message)
        else:
            log_entry = '{} -- {} -- {} -- {}'.format(DateTimeUtils.get_timestamp_formatted_iso(), log_level, component, message)
        print(log_entry)

    def __add_log_entry_to_file(self, log_level: str, component: str | None, message: str):
        if StringUtils.none2string(component) == '':
            log_entry = '{} -- {} -- {}'.format(DateTimeUtils.get_timestamp_formatted_iso(), log_level, message)
        else:
            log_entry = '{} -- {} -- {} -- {}'.format(DateTimeUtils.get_timestamp_formatted_iso(), log_level, component, message)
        if FileUtils.file_exists(full_file_path=self.log_file_full_file_path):
            FileUtils.file_append_content(full_file_path=self.log_file_full_file_path, content=log_entry)
        else:
            FileUtils.file_create(full_file_path=self.log_file_full_file_path, content=log_entry)
