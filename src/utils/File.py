import os
import shutil
import requests
import time
import datetime
import utils.String as StringUtils


def directory_exists(path: str) -> bool:
    return_value = False
    if os.path.isdir(path):
        return_value = True
    return return_value


def directory_copy(source_path: str, target_path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    try:
        shutil.copytree(source_path, target_path)
        return_value['status'] = 'SUCCESS'
    except:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unexpected error while copying file(s)'

    return return_value


def directory_create(path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    if directory_exists(path=path):
        return_value['status'] = 'WARNING'
        return_value['error_message'] = 'Directory already exists'

    if return_value['status'] == '':
        try:
            os.makedirs(path)
        except:
            return_value['status'] = 'FAILED'

    if return_value['status'] == '':
        if directory_exists(path=path):
            return_value['status'] = 'SUCCESS'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to create directory'

    return return_value


def directory_delete(path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    try:
        shutil.rmtree(path)
        if not directory_exists(path=path):
            return_value['status'] = 'SUCCESS'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Directory was not successfully deleted'
    except:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to delete directory'

    return return_value


def directory_move(source_path: str, target_path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}
    continue_execution = True

    if not directory_exists(path=source_path):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Source folder does not exist'

    if continue_execution and directory_exists(path=target_path):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Target folder already exists'

    if continue_execution:
        try:
            shutil.move(src=source_path, dst=target_path)
            if directory_exists(path=target_path):
                return_value['status'] = 'SUCCESS'
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Directory was not successfully moved'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to move directory'

    return return_value


def file_append_content(full_file_path: str, content: str, encoding: str = 'utf-8', content_on_new_line: bool = True) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    if file_exists(full_file_path=full_file_path):
        if encoding is None:
            file = open(full_file_path, 'r+')
        else:
            file = open(full_file_path, 'r+', encoding=encoding)

        if content_on_new_line:
            if len(file.readlines()) > 0:
                content = '\n{}'.format(content)
            else:
                content = str(content)
        else:
            content = str(content)

        file.write(content)
        file.close()

        return_value['status'] = 'SUCCESS'
    else:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'File does not exist'

    return return_value


def file_copy(source_full_file_path: str, target_path: str, new_file_name: str = None) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    if new_file_name is None:
        res = split_full_file_path(full_file_path=source_full_file_path)
        if res['status'] == 'SUCCESS' and not res['response_body']['file_name'] == '':
            new_file_name = res['response_body']['file_name']
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Target file name could not be defined'

    if return_value['status'] == '':
        if not file_exists(full_file_path=source_full_file_path):
            return_value['status'] = 'FAILED'
            return_value['errorMessage'] = 'Source file is not accessible'

    if return_value['status'] == '':
        if target_path is None or not directory_exists(path=target_path):
            return_value['status'] = 'FAILED'
            return_value['errorMessage'] = 'Target path was not supplied or is not accessible'
        else:
            target_full_file_path = path_join(path=target_path, filename_or_foldername=new_file_name)
            try:
                shutil.copy2(src=source_full_file_path, dst=target_full_file_path)
                if file_exists(full_file_path=target_full_file_path):
                    return_value['status'] = 'SUCCESS'
                else:
                    return_value['status'] = 'FAILED'
                    return_value['error_message'] = 'Unexpected error while copying file(s)'
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unexpected error while copying file(s)'

    return return_value


def file_copy_filtered(source_path: str, target_path: str, file_extension_filter: str = None) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}
    return_value['response_body']['nbr_files_copied'] = 0
    continue_execution = True

    if not directory_exists(path=source_path):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Source directory is not accessible'

    if continue_execution:
        if not directory_exists(path=target_path):
            continue_execution = False
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Target directory is not accessible'

    if continue_execution:
        if file_extension_filter is None:
            try:
                nbr_files_copied = 0
                for file in os.listdir(path=source_path):
                    shutil.copy2(src=path_join(path=source_path, filename_or_foldername=file), dst=target_path)
                    nbr_files_copied += 1
                return_value['status'] = 'SUCCESS'
                return_value['response_body']['nbr_files_copied'] = nbr_files_copied
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'File copy went wrong'
        else:
            try:
                nbr_files_copied = 0
                for file in os.listdir(path=source_path):
                    file_extension = os.path.splitext(file)[1]
                    file_extension = file_extension[-(len(file_extension) - 1):]
                    if file_extension.lower() == file_extension_filter.lower():
                        shutil.copy2(src=path_join(path=source_path, filename_or_foldername=file), dst=target_path)
                        nbr_files_copied += 1
                return_value['status'] = 'SUCCESS'
                return_value['response_body']['nbr_files_copied'] = nbr_files_copied
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'File copy went wrong'

    return return_value


def file_exists(full_file_path: str, path_is_url: bool = False) -> bool:
    return_value = False
    if path_is_url:
        if requests.head(full_file_path).status_code == requests.codes.ok:
            return_value = True
    else:
        if os.path.isfile(full_file_path):
            return_value = True
    return return_value


def file_create(full_file_path: str, content: str = None, overwrite: bool = True, encoding: str = 'utf-8'):
    return_value = {'status': '', 'error_message': '', 'response_body': ''}
    continue_execution = True

    res = split_full_file_path(full_file_path=full_file_path)
    if res['status'] == 'SUCCESS':
        if not directory_exists(res['response_body']['path']):
            continue_execution = False
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Save path not available'
    else:
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'An unexpected error occurred'

    if continue_execution:
        if not overwrite and file_exists(full_file_path=full_file_path):
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'File already exists'
        else:
            try:
                if encoding is None:
                    file = open(full_file_path, 'w')
                else:
                    file = open(full_file_path, 'w', encoding=encoding)
                if content is not None:
                    file.writelines(content)
                file.close()
                return_value['status'] = 'SUCCESS'
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unable to save file'

    return return_value


def file_delete(full_file_path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    try:
        os.remove(full_file_path)
        if not file_exists(full_file_path=full_file_path):
            return_value['status'] = 'SUCCESS'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'File was not successfully deleted'
    except:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to delete file'

    return return_value


def file_move(file_name: str, source_path: str, target_path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}
    continue_execution = True

    if not directory_exists(path=source_path):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Source directory is not accessible'
    elif not directory_exists(path=target_path):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Target directory is not accessible'
    elif not file_exists(full_file_path=path_join(path=source_path, filename_or_foldername=file_name)):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Source file is not accessible'

    if continue_execution:
        try:
            shutil.move(src=path_join(path=source_path, filename_or_foldername=file_name), dst=target_path)
        except:
            continue_execution = False
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to move file'

    if continue_execution:
        if file_exists(path_join(path=target_path, filename_or_foldername=file_name)):
            if not file_exists(path_join(path=source_path, filename_or_foldername=file_name)):
                return_value['status'] = 'SUCCESS'
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'File moved however the old file still exists'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to move file'

    return return_value


def file_read(full_file_path: str, encoding: str = 'utf-8') -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    try:
        if encoding is None:
            file = open(full_file_path, 'r')
        else:
            file = open(full_file_path, 'r', encoding=encoding)
        file_content = file.read()
        return_value['status'] = 'SUCCESS'
        return_value['response_body'] = file_content
    except:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to open file'

    return return_value


def file_rename(full_file_path: str, file_name_new: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    if file_exists(full_file_path=full_file_path):
        path, source_file_name = os.path.split(full_file_path)
        if not file_exists(full_file_path=path_join(path=path, filename_or_foldername=file_name_new)):
            try:
                os.rename(src=full_file_path, dst=path_join(path=path, filename_or_foldername=file_name_new))
                return_value['status'] = 'SUCCESS'
            except:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unable to rename file'
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Target file already exists'
    else:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Source file does not exist'

    return return_value


def find_string_in_file(full_file_path: str, search_value: str, case_sensitive: bool = False) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    if search_value == '':
        if file_exists(full_file_path=full_file_path):
            search_value_found = False
            file = open(full_file_path, 'rt')
            if case_sensitive:
                for line in file:
                    if search_value in line:
                        search_value_found = True
                        break
            else:
                for line in file:
                    if search_value.upper() in line.upper():
                        search_value_found = True
                        break
            file.close()

            return_value['status'] = 'SUCCESS'
            return_value['response_body'] = {}
            if search_value_found:
                return_value['response_body']['found'] = True
            else:
                return_value['response_body']['found'] = False
        else:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'File does not exist'
    else:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Search value is empty'

    return return_value


def get_directory_file_extensions(path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': []}

    try:
        file_extension_list = []
        for file in os.listdir(path):
            file_extension = os.path.splitext(file)[1]
            file_extension = file_extension[-(len(file_extension) - 1):]
            if not file_extension == '':
                file_extension_list.append(file_extension.lower())

        file_extension_list = sorted(list(set(file_extension_list)))
        return_value['status'] = 'SUCCESS'
        return_value['response_body'] = file_extension_list
    except:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to retrieve file extensions'
        return_value['response_body'] = []

    return return_value


def get_directory_files(path: str, file_extension_filter: str = None) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}
    return_value['response_body']['path'] = str(path)
    if file_extension_filter is None:
        file_extension_filter = ''
    return_value['response_body']['file_extension_filter'] = file_extension_filter
    return_value['response_body']['nbr_files_found'] = 0
    return_value['response_body']['files'] = []
    continue_execution = True

    if not directory_exists(path=path):
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Directory is not accessible'
        continue_execution = False

    if continue_execution:
        try:
            for file in os.listdir(path):
                if not os.path.isdir(path_join(path=path, filename_or_foldername=file)):
                    if file_extension_filter == '':
                        return_value['response_body']['files'].append(file)
                        return_value['response_body']['nbr_files_found'] += 1
                    else:
                        file_extension = os.path.splitext(file)[1]
                        file_extension = file_extension[-(len(file_extension) - 1):]
                        if file_extension.lower() == file_extension_filter.lower():
                            return_value['response_body']['files'].append(file)
                            return_value['response_body']['nbr_files_found'] += 1

            return_value['status'] = 'SUCCESS'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unexpected error'

    return return_value


def get_directory_folders(path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}
    return_value['response_body']['path'] = str(path)
    return_value['response_body']['nbr_directories_found'] = 0
    return_value['response_body']['directories'] = []
    continue_execution = True

    if not directory_exists(path=path):
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Directory is not accessible'
        continue_execution = False

    if continue_execution:
        try:
            for file_folder in os.listdir(path):
                if os.path.isdir(path_join(path=path, filename_or_foldername=file_folder)):
                    return_value['response_body']['directories'].append(file_folder)
                    return_value['response_body']['nbr_directories_found'] += 1
            return_value['status'] = 'SUCCESS'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unexpected error'

    return return_value


def get_directory_structure(path: str, path_root_alias_name: str = None) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}
    return_value['response_body']['json_tree'] = {}
    return_value['response_body']['list'] = []
    continue_execution = True

    if not directory_exists(path=path):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Path does not exist'

    # Generate json_tree output
    if continue_execution:
        try:
            rootparts = path.split(os.sep)
            results = {'path': path, 'relative_path': '/', 'sub_folders': {}, 'files': {}, 'details': {}}
            for (dirpath, dirnames, filenames) in os.walk(path):
                dirparts = dirpath.split(os.sep)
                relativedirparts = dirparts[len(rootparts):len(dirparts)]
                curr = results
                for folder in relativedirparts:
                    tmp_json_entry = {'path': dirpath, 'relative_path': ''}
                    for el in dirparts[len(rootparts):len(dirparts)]:
                        tmp_json_entry['relative_path'] = tmp_json_entry['relative_path'] + '/' + str(el)
                    tmp_json_entry['sub_folders'] = {}
                    tmp_json_entry['files'] = {}
                    curr = curr['sub_folders'].setdefault(folder, tmp_json_entry)

                for file in filenames:
                    curr['files'][file] = get_file_details(full_file_path=path_join(path=dirpath, filename_or_foldername=file))['response_body']

            if path_root_alias_name == '':
                path_root_alias_name = '/'
            return_value['response_body']['json_tree'][path_root_alias_name] = {}
            return_value['response_body']['json_tree'][path_root_alias_name] = results
        except:
            return_value['response_body']['json_tree'] = {}
            continue_execution = False
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to generate json_tree output'

    # Generate list output (based on the generated json_tree)
    if continue_execution:
        try:
            return_value['response_body']['list'] = ConvertDirectoryStructure2List(directory_as_json_tree=return_value['response_body']['json_tree']).retrieve_list()
        except:
            continue_execution = False
            return_value['response_body']['list'] = []
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Unable to generate list output (based on the generated json_tree)'

    # Finalisation
    if continue_execution:
        return_value['status'] = 'SUCCESS'

    return return_value


def get_file_details(full_file_path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}
    continue_execution = True

    # File name, path, extension, type
    try:
        return_value['response_body']['full_file_path'] = full_file_path

        path, file_name = os.path.split(full_file_path)
        return_value['response_body']['path'] = path
        return_value['response_body']['file_name'] = file_name
        return_value['response_body']['file_name_without_extension'] = os.path.splitext(file_name)[0]

        # File extension
        file_extension = os.path.splitext(file_name)[1]
        file_extension = file_extension[-(len(file_extension) - 1):]
        file_extension = file_extension.lower()
        return_value['response_body']['file_extension'] = file_extension

        # File type
        if file_extension in ['doc', 'docx', 'dot', 'dotx']:
            return_value['response_body']['file_type'] = 'Word'
        elif file_extension in ['accdb', 'accde', 'accdr', 'accdt']:
            return_value['response_body']['file_type'] = 'Access'
        elif file_extension in ['xls', 'xlsx', 'xlsm', 'xltx', 'xltm']:
            return_value['response_body']['file_type'] = 'Excel'
        elif file_extension in ['ppt', 'pptx']:
            return_value['response_body']['file_type'] = 'PowerPoint'
        elif file_extension in ['txt']:
            return_value['response_body']['file_type'] = 'txt'
        elif file_extension in ['json']:
            return_value['response_body']['file_type'] = 'JSON'
        elif file_extension in ['xml']:
            return_value['response_body']['file_type'] = 'XML'
        elif file_extension in ['sql']:
            return_value['response_body']['file_type'] = 'SQL'
        elif file_extension in ['csv']:
            return_value['response_body']['file_type'] = 'csv'
        elif file_extension in ['avi', 'mp4', 'mp3']:
            return_value['response_body']['file_type'] = 'Media'
        elif file_extension in ['bmp', 'jpg', 'jpeg', 'tiff', 'png', 'gif']:
            return_value['response_body']['file_type'] = 'Image'
        elif file_extension in ['htm', 'html']:
            return_value['response_body']['file_type'] = 'Html'
        elif file_extension in ['pdf']:
            return_value['response_body']['file_type'] = 'Pdf'
        elif file_extension in ['log']:
            return_value['response_body']['file_type'] = 'log'
        elif file_extension in ['py']:
            return_value['response_body']['file_type'] = 'Python code'
        else:
            return_value['response_body']['file_type'] = 'Unknown'
    except:
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to retrieve basic file details'
        return_value['response_body']['full_file_path'] = ''
        return_value['response_body']['path'] = ''
        return_value['response_body']['file_name'] = ''
        return_value['response_body']['file_name_without_extension'] = ''
        return_value['response_body']['file_extension'] = ''
        return_value['response_body']['file_type'] = ''

    # Check if file exists
    if continue_execution:
        if file_exists(full_file_path=full_file_path):
            return_value['response_body']['file_exists'] = True
        else:
            return_value['response_body']['file_exists'] = False
    else:
        return_value['response_body']['file_exists'] = False

    # File size
    return_value['response_body']['file_size'] = {}
    if continue_execution and return_value['response_body']['file_exists']:
        file_size_in_byes = os.path.getsize(full_file_path)
        return_value['response_body']['file_size']['bytes'] = file_size_in_byes

        file_size_in_kilobytes = file_size_in_byes / 1024
        return_value['response_body']['file_size']['kilobytes'] = round(file_size_in_kilobytes, 2)

        file_size_in_megabytes = file_size_in_kilobytes / 1024
        return_value['response_body']['file_size']['megabytes'] = round(file_size_in_megabytes, 2)
    else:
        return_value['response_body']['file_size']['bytes'] = ''
        return_value['response_body']['file_size']['kilobytes'] = ''
        return_value['response_body']['file_size']['megabytes'] = ''

    # File timestamps
    return_value['response_body']['file_timestamps'] = {}
    if continue_execution and return_value['response_body']['file_exists']:
        # Created
        file_timestamp = time.ctime(os.path.getctime(full_file_path))
        file_timestamp = datetime.datetime.strptime(file_timestamp, '%c')
        return_value['response_body']['file_timestamps']['created'] = file_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Modified
        file_timestamp = time.ctime(os.path.getmtime(full_file_path))
        file_timestamp = datetime.datetime.strptime(file_timestamp, '%c')
        return_value['response_body']['file_timestamps']['modified'] = file_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return_value['response_body']['file_timestamps']['created'] = ''
        return_value['response_body']['file_timestamps']['modified'] = ''

    if continue_execution:
        return_value['status'] = 'SUCCESS'

    return return_value


def path_join(path: str, filename_or_foldername: str) -> str:
    return os.path.join(os.sep, path, filename_or_foldername)


def split_full_file_path(full_file_path: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}
    return_value['response_body']['path'] = ''
    return_value['response_body']['file_name'] = ''

    try:
        path, file_name = os.path.split(full_file_path)
        return_value['status'] = 'SUCCESS'
        return_value['response_body']['path'] = path
        return_value['response_body']['file_name'] = file_name
    except:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to split full file path'

    return return_value


def create_zip_achive(source_path: str, target_path: str, file_name_zip_file: str, overwrite: bool = True) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}
    continue_execution = True

    target_full_file_path = path_join(path=target_path, filename_or_foldername=file_name_zip_file)

    if not directory_exists(path=source_path):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Source folder does not exist'

    if continue_execution and not directory_exists(path=target_path):
        continue_execution = False
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Target folder does not exist'

    if continue_execution:
        if overwrite:
            if not file_delete(full_file_path=target_full_file_path)['status'] == 'SUCCESS':
                continue_execution = False
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'Unable to delete existing file'
        elif file_exists(full_file_path=target_full_file_path):
            continue_execution = False
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'Target file already exists'

    if continue_execution:
        try:
            shutil.make_archive(base_name=target_full_file_path, format='zip', root_dir=source_path)
            if file_exists(full_file_path=target_full_file_path):
                return_value['status'] = 'SUCCESS'
            else:
                return_value['status'] = 'FAILED'
                return_value['error_message'] = 'An unexpected error occurred while creation archive'
        except:
            return_value['status'] = 'FAILED'
            return_value['error_message'] = 'An unexpected error occurred while creation archive'

    return return_value


class ConvertDirectoryStructure2List:
    def __init__(self, directory_as_json_tree: dict):
        self.result_list = []
        self.__convert(directory_as_json_tree=directory_as_json_tree)

    def retrieve_list(self) -> list:
        return self.result_list

    def __convert(self, directory_as_json_tree: dict):
        if len(directory_as_json_tree) > 0:
            for folder in directory_as_json_tree:
                tmp_record = {'file_or_folder': 'folder', 'path': directory_as_json_tree[folder]['path'], 'relative_path': directory_as_json_tree[folder]['relative_path']}
                if len(self.result_list) == 0:
                    tmp_record['level_depth'] = 0
                else:
                    tmp_record['level_depth'] = len(directory_as_json_tree[folder]['relative_path'].split('/')) - 1
                tmp_record['name'] = folder
                self.result_list.append(tmp_record)

                if len(directory_as_json_tree[folder]['files']) > 0:
                    for file in directory_as_json_tree[folder]['files']:
                        tmp_record_file = {'file_or_folder': 'file', 'path': directory_as_json_tree[folder]['path'], 'relative_path': directory_as_json_tree[folder]['relative_path'] + '/' + file}
                        if StringUtils.left(string_value=tmp_record_file['relative_path'], count=2) == '//':
                            tmp_record_file['level_depth'] = len(directory_as_json_tree[folder]['relative_path'].split('/')) - 1
                            tmp_record_file['relative_path'] = tmp_record_file['relative_path'].replace('//', '/')
                        else:
                            tmp_record_file['LevelDepth'] = len(directory_as_json_tree[folder]['relative_path'].split('/'))
                        tmp_record_file['name'] = file
                        tmp_record_file['details'] = get_file_details(full_file_path=path_join(path=tmp_record_file['path'], filename_or_foldername=tmp_record_file['name']))['response_body']
                        self.result_list.append(tmp_record_file)

                if len(directory_as_json_tree[folder]['sub_folders']) > 0:
                    self.__convert(directory_as_json_tree=directory_as_json_tree[folder]['sub_folders'])
