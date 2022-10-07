import string
import random
import re


def cleanup_string(value: str, trim_string: bool = False, trim_quotes: bool = False, convert_to_standard_alphabet: bool = False, remove_quotes: bool = False,
                   remove_spaces: bool = False, remove_slashes: bool = False, remove_hyphen: bool = False, remove_underscore: bool = False, remove_dollar_sign: bool = False,
                   remove_asterix: bool = False, remove_punctuation_mark: bool = False, remove_null_values: bool = False) -> str:
    if value is None:
        return_value = ''
    else:
        string_value = str(value)

        if trim_quotes:
            string_value = string_value.strip("'")
            string_value = string_value.strip('"')

        if trim_string:
            string_value = string_value.strip()

        if convert_to_standard_alphabet:
            string_value = string_value.replace('Á', 'A')
            string_value = string_value.replace('á', 'a')
            string_value = string_value.replace('À', 'A')
            string_value = string_value.replace('à', 'a')
            string_value = string_value.replace('Ȧ', 'A')
            string_value = string_value.replace('ȧ', 'a')
            string_value = string_value.replace('Â', 'A')
            string_value = string_value.replace('â', 'a')
            string_value = string_value.replace('Ä', 'A')
            string_value = string_value.replace('ä', 'a')
            string_value = string_value.replace('Ă', 'A')
            string_value = string_value.replace('ă', 'a')
            string_value = string_value.replace('Ā', 'A')
            string_value = string_value.replace('ā', 'a')
            string_value = string_value.replace('Ã', 'A')
            string_value = string_value.replace('ã', 'a')
            string_value = string_value.replace('Å', 'A')
            string_value = string_value.replace('å', 'a')
            string_value = string_value.replace('Ą', 'A')
            string_value = string_value.replace('ą', 'a')
            string_value = string_value.replace('Ḃ', 'B')
            string_value = string_value.replace('ḃ', 'b')
            string_value = string_value.replace('Ć', 'C')
            string_value = string_value.replace('ć', 'c')
            string_value = string_value.replace('Ċ', 'C')
            string_value = string_value.replace('ċ', 'c')
            string_value = string_value.replace('Ĉ', 'C')
            string_value = string_value.replace('ĉ', 'c')
            string_value = string_value.replace('Č', 'C')
            string_value = string_value.replace('č', 'c')
            string_value = string_value.replace('Ç', 'C')
            string_value = string_value.replace('ç', 'c')
            string_value = string_value.replace('Ḋ', 'D')
            string_value = string_value.replace('ḋ', 'd')
            string_value = string_value.replace('Ď', 'D')
            string_value = string_value.replace('ď', 'd')
            string_value = string_value.replace('Đ', 'D')
            string_value = string_value.replace('đ', 'd')
            string_value = string_value.replace('É', 'E')
            string_value = string_value.replace('é', 'e')
            string_value = string_value.replace('È', 'E')
            string_value = string_value.replace('è', 'e')
            string_value = string_value.replace('Ė', 'E')
            string_value = string_value.replace('ė', 'e')
            string_value = string_value.replace('Ê', 'E')
            string_value = string_value.replace('ê', 'e')
            string_value = string_value.replace('Ë', 'E')
            string_value = string_value.replace('ë', 'e')
            string_value = string_value.replace('Ě', 'E')
            string_value = string_value.replace('ě', 'e')
            string_value = string_value.replace('Ĕ', 'E')
            string_value = string_value.replace('ĕ', 'e')
            string_value = string_value.replace('Ē', 'E')
            string_value = string_value.replace('ē', 'e')
            string_value = string_value.replace('Ę', 'E')
            string_value = string_value.replace('ę', 'e')
            string_value = string_value.replace('Ȩ', 'E')
            string_value = string_value.replace('ȩ', 'e')
            string_value = string_value.replace('Ḟ', 'F')
            string_value = string_value.replace('ḟ', 'f')
            string_value = string_value.replace('Ġ', 'G')
            string_value = string_value.replace('ġ', 'g')
            string_value = string_value.replace('Ĝ', 'G')
            string_value = string_value.replace('ĝ', 'g')
            string_value = string_value.replace('Ğ', 'G')
            string_value = string_value.replace('ğ', 'g')
            string_value = string_value.replace('Ģ', 'G')
            string_value = string_value.replace('ģ', 'g')
            string_value = string_value.replace('Ĥ', 'H')
            string_value = string_value.replace('ĥ', 'h')
            string_value = string_value.replace('i', 'i')
            string_value = string_value.replace('ı', 'I')
            string_value = string_value.replace('ı', 'i')
            string_value = string_value.replace('Í', 'I')
            string_value = string_value.replace('í', 'i')
            string_value = string_value.replace('Ì', 'I')
            string_value = string_value.replace('ì', 'i')
            string_value = string_value.replace('İ', 'I')
            string_value = string_value.replace('Î', 'I')
            string_value = string_value.replace('î', 'i')
            string_value = string_value.replace('Ï', 'I')
            string_value = string_value.replace('ï', 'i')
            string_value = string_value.replace('Ĭ', 'I')
            string_value = string_value.replace('ĭ', 'i')
            string_value = string_value.replace('Ī', 'I')
            string_value = string_value.replace('ī', 'i')
            string_value = string_value.replace('Ĩ', 'I')
            string_value = string_value.replace('ĩ', 'i')
            string_value = string_value.replace('Į', 'I')
            string_value = string_value.replace('į', 'i')
            string_value = string_value.replace('Ĵ', 'J')
            string_value = string_value.replace('ĵ', 'j')
            string_value = string_value.replace('ĸ', 'K')
            string_value = string_value.replace('ĸ', 'k')
            string_value = string_value.replace('Ķ', 'K')
            string_value = string_value.replace('ķ', 'k')
            string_value = string_value.replace('Ĺ', 'L')
            string_value = string_value.replace('ĺ', 'l')
            string_value = string_value.replace('Ŀ', 'L')
            string_value = string_value.replace('ŀ', 'l')
            string_value = string_value.replace('Ľ', 'L')
            string_value = string_value.replace('ľ', 'l')
            string_value = string_value.replace('Ļ', 'L')
            string_value = string_value.replace('ļ', 'l')
            string_value = string_value.replace('Ł', 'L')
            string_value = string_value.replace('ł', 'l')
            string_value = string_value.replace('Ṁ', 'M')
            string_value = string_value.replace('ṁ', 'm')
            string_value = string_value.replace('Ń', 'N')
            string_value = string_value.replace('ń', 'n')
            string_value = string_value.replace('Ň', 'N')
            string_value = string_value.replace('ň', 'n')
            string_value = string_value.replace('Ñ', 'N')
            string_value = string_value.replace('ñ', 'n')
            string_value = string_value.replace('Ņ', 'N')
            string_value = string_value.replace('ņ', 'n')
            string_value = string_value.replace('Ŋ', 'N')
            string_value = string_value.replace('ŋ', 'n')
            string_value = string_value.replace('Ó', 'O')
            string_value = string_value.replace('ó', 'o')
            string_value = string_value.replace('Ò', 'O')
            string_value = string_value.replace('ò', 'o')
            string_value = string_value.replace('Ȯ', 'O')
            string_value = string_value.replace('ȯ', 'o')
            string_value = string_value.replace('Ô', 'O')
            string_value = string_value.replace('ô', 'o')
            string_value = string_value.replace('Ö', 'O')
            string_value = string_value.replace('ö', 'o')
            string_value = string_value.replace('Ŏ', 'O')
            string_value = string_value.replace('ŏ', 'o')
            string_value = string_value.replace('Ō', 'O')
            string_value = string_value.replace('ō', 'o')
            string_value = string_value.replace('Õ', 'O')
            string_value = string_value.replace('õ', 'o')
            string_value = string_value.replace('Ő', 'O')
            string_value = string_value.replace('ő', 'o')
            # string_value = string_value.replace('Ø', 'O')
            # string_value = string_value.replace('ø', 'o')
            string_value = string_value.replace('Ø', 'E')
            string_value = string_value.replace('ø', 'e')
            string_value = string_value.replace('Ȱ', 'O')
            string_value = string_value.replace('ȱ', 'o')
            string_value = string_value.replace('Ȫ', 'O')
            string_value = string_value.replace('ȫ', 'o')
            string_value = string_value.replace('Ȭ', 'O')
            string_value = string_value.replace('ȭ', 'o')
            string_value = string_value.replace('Ṗ', 'P')
            string_value = string_value.replace('ṗ', 'p')
            string_value = string_value.replace('Ŕ', 'R')
            string_value = string_value.replace('ŕ', 'r')
            string_value = string_value.replace('Ř', 'R')
            string_value = string_value.replace('ř', 'r')
            string_value = string_value.replace('Ŗ', 'R')
            string_value = string_value.replace('ŗ', 'r')
            string_value = string_value.replace('Ś', 'S')
            string_value = string_value.replace('ś', 's')
            string_value = string_value.replace('Ṡ', 'S')
            string_value = string_value.replace('ṡ', 's')
            string_value = string_value.replace('Ŝ', 'S')
            string_value = string_value.replace('ŝ', 's')
            string_value = string_value.replace('Š', 'S')
            string_value = string_value.replace('š', 's')
            string_value = string_value.replace('Ş', 'S')
            string_value = string_value.replace('ş', 's')
            string_value = string_value.replace('Ṫ', 'T')
            string_value = string_value.replace('ṫ', 't')
            string_value = string_value.replace('Ť', 'T')
            string_value = string_value.replace('ť', 't')
            string_value = string_value.replace('Ţ', 'T')
            string_value = string_value.replace('ţ', 't')
            string_value = string_value.replace('Ú', 'U')
            string_value = string_value.replace('ú', 'u')
            string_value = string_value.replace('Ù', 'U')
            string_value = string_value.replace('ù', 'u')
            string_value = string_value.replace('Û', 'U')
            string_value = string_value.replace('û', 'u')
            string_value = string_value.replace('Ü', 'U')
            string_value = string_value.replace('ü', 'u')
            string_value = string_value.replace('Ŭ', 'U')
            string_value = string_value.replace('ŭ', 'u')
            string_value = string_value.replace('Ū', 'U')
            string_value = string_value.replace('ū', 'u')
            string_value = string_value.replace('Ũ', 'U')
            string_value = string_value.replace('ũ', 'u')
            string_value = string_value.replace('Ů', 'U')
            string_value = string_value.replace('ů', 'u')
            string_value = string_value.replace('Ų', 'U')
            string_value = string_value.replace('ų', 'u')
            string_value = string_value.replace('Ű', 'U')
            string_value = string_value.replace('ű', 'u')
            string_value = string_value.replace('Ẃ', 'W')
            string_value = string_value.replace('ẃ', 'w')
            string_value = string_value.replace('Ẁ', 'W')
            string_value = string_value.replace('ẁ', 'w')
            string_value = string_value.replace('Ŵ', 'W')
            string_value = string_value.replace('ŵ', 'w')
            string_value = string_value.replace('Ẅ', 'W')
            string_value = string_value.replace('ẅ', 'w')
            string_value = string_value.replace('Ý', 'Y')
            string_value = string_value.replace('ý', 'y')
            string_value = string_value.replace('Ỳ', 'Y')
            string_value = string_value.replace('ỳ', 'y')
            string_value = string_value.replace('Ŷ', 'Y')
            string_value = string_value.replace('ŷ', 'y')
            string_value = string_value.replace('ÿ', 'y')
            string_value = string_value.replace('ÿ', 'y')
            string_value = string_value.replace('Ȳ', 'Y')
            string_value = string_value.replace('ȳ', 'y')
            string_value = string_value.replace('Ź', 'Z')
            string_value = string_value.replace('ź', 'z')
            string_value = string_value.replace('Ż', 'Z')
            string_value = string_value.replace('ż', 'z')
            string_value = string_value.replace('Ž', 'Z')
            string_value = string_value.replace('ž', 'z')
            string_value = string_value.replace('Ȥ', 'Z')
            string_value = string_value.replace('ȥ', 'z')

        if remove_quotes:
            string_value = string_value.replace('"', '')
            string_value = string_value.replace("'", '')

        if remove_spaces:
            string_value = string_value.replace(' ', '')

        if remove_slashes:
            string_value = string_value.replace('\\', '')
            string_value = string_value.replace('/', '')

        if remove_hyphen:
            string_value = string_value.replace('-', '')

        if remove_underscore:
            string_value = string_value.replace('_', '')

        if remove_dollar_sign:
            string_value = string_value.replace('$', '')

        if remove_asterix:
            string_value = string_value.replace('*', '')

        if remove_punctuation_mark:
            string_value = string_value.replace('+', '')
            string_value = string_value.replace('&', '')
            string_value = string_value.replace('.', '')
            string_value = string_value.replace(',', '')
            string_value = string_value.replace('>', '')
            string_value = string_value.replace('<', '')
            string_value = string_value.replace('?', '')
            string_value = string_value.replace(':', '')
            string_value = string_value.replace(';', '')
            string_value = string_value.replace('!', '')

        if remove_null_values:
            string_value = string_value.replace('None', '')
            string_value = string_value.replace('none', '')
            string_value = string_value.replace('NONE', '')
            string_value = string_value.replace('Null', '')
            string_value = string_value.replace('null', '')
            string_value = string_value.replace('NULL', '')

        return_value = string_value

    return return_value


def extract_url_from_string(string_value: str) -> str:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, str(string_value))
    return_value = str([x[0] for x in url])
    return return_value


def find_value_in_string(text_to_be_searched: str, search_value: str, case_sensitive: bool = True, remove_line_breaks_from_text_to_be_searched: bool = False) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    try:
        if not case_sensitive:
            text_to_be_searched = text_to_be_searched.lower()
            search_value = search_value.lower()

        if remove_line_breaks_from_text_to_be_searched:
            text_to_be_searched = text_to_be_searched.replace('\n', ' ')

        nbr_occ = text_to_be_searched.count(search_value)
        return_value['status'] = 'SUCCESS'
        return_value['response_body'] = {}
        return_value['response_body']['case_sensitive_search'] = case_sensitive
        return_value['response_body']['remove_line_breaks_from_text_to_be_searched'] = remove_line_breaks_from_text_to_be_searched
        if nbr_occ > 0:
            return_value['response_body']['found'] = True
            return_value['response_body']['nbr_occ'] = nbr_occ
        else:
            return_value['response_body']['found'] = False
            return_value['response_body']['nbr_occ'] = 0
    except:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'An unexpected error occurred'

    return return_value


def get_random_string(length: int = 1) -> str:
    chars = string.ascii_uppercase + string.digits
    rnd_value = ''

    for x in range(length):
        rnd_value = '{}{}'.format(rnd_value, random.choice(chars))

    return rnd_value


def left(string_value: str, count: int) -> str:
    return string_value[0:count]


def none2string(value: str) -> str:
    if value is None:
        return_value = ""
    else:
        return_value = value

    return return_value


def right(string_value: str, count: int) -> str:
    return string_value[-count:]


def string_fill_linked_to_max_value(value: int | str, max_value: int, min_fill_length: int = 3) -> str:
    try:
        if len(str(max_value)) < min_fill_length:
            fill_length = min_fill_length
        else:
            fill_length = len(str(max_value))

        return_value = str(value).zfill(fill_length)
    except:
        return_value = value

    return return_value


def substring(string_value: str, start_string: str = None, end_string: str = None, strict_boundry: bool = False, case_sensitive: bool = False) -> str:
    if not case_sensitive:
        string_value = string_value.lower()
        if start_string is not None:
            start_string = start_string.lower()
        if end_string is not None:
            end_string = end_string.lower()

    start_index = string_value.find(start_string)
    end_index = string_value.find(end_string)

    if not strict_boundry:
        if start_index == '0' or start_index == -1 or start_string == '' or start_string is None:
            start_index = None

        if end_index == '0' or end_index == -1 or end_string == '' or end_string is None:
            end_index = None

        substring_value = string_value[start_index:end_index]
    else:
        if start_index == -1 or end_index == -1:
            substring_value = ''
        else:
            if start_index == '0' or start_string == '':
                start_index = None

            if end_index == '0' or end_string == '':
                end_index = None

            substring_value = string_value[start_index:end_index]

    return substring_value
