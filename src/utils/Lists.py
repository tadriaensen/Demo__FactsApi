def diff(list1: list, list2: list) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}
    return_value['response_body']['list1_minus_list2'] = []
    return_value['response_body']['list2_minus_list1'] = []

    try:
        list1 = sorted(list(set(list1)))
        list2 = sorted(list(set(list2)))
        return_value['response_body']['list1_minus_list2'] = list(set(list1) - set(list2))
        return_value['response_body']['list2_minus_list1'] = list(set(list2) - set(list1))
        return_value['status'] = 'SUCCESS'
    except:
        return_value['status'] = 'FAILED'
        return_value['response_body']['list1_minus_list2'] = []
        return_value['response_body']['list2_minus_list1'] = []

    return return_value


def element_in_list(list_to_search: list, search_value: any) -> bool:
    return_value = False
    for entry in list_to_search:
        if str(entry).upper() == str(search_value).upper():
            return_value = True
            break
    return return_value


def filter_list_containing_dicts(list_to_filter: list, filter_key: str, filter_value: any) -> list:
    try:
        filtered_list = []
        for row in list_to_filter:
            if row[filter_key] == filter_value:
                filtered_list.append(row)
    except:
        filtered_list = []
    return filtered_list


def get_dict_element_from_list(list_containing_dicts: list, key_column: str, search_value: any) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': ''}

    for el in list_containing_dicts:
        if return_value['status'] != 'SUCCESS':
            if el[key_column].upper() == search_value.upper():
                return_value['status'] = 'SUCCESS'
                return_value['response_body'] = el
            else:
                return_value['status'] = 'FAILED'

    return return_value


def get_unique_values(list_to_manipulate: list, alphabetically_ordered: bool = True) -> list:
    return_value = list(set(list_to_manipulate))
    if alphabetically_ordered:
        return_value = sorted(return_value)
    return return_value


def get_unique_values_from_list_containing_dicts(list_to_manipulate: list) -> list:
    # if uniquely identified by whole object
    return_value = [dict(s) for s in set(frozenset(my_object.items()) for my_object in list_to_manipulate)]
    return return_value


def sort_list(list_to_sort: list, key_column: str = None, order: str = 'ASC') -> list:
    if key_column is None:
        if order.upper() == 'DESC':
            return_value = sorted(list_to_sort).reverse()
        else:
            return_value = sorted(list_to_sort)
    else:
        if order.upper() == 'DESC':
            return_value = sorted(list_to_sort, key=lambda x: x[key_column]).reverse()
        else:
            return_value = sorted(list_to_sort, key=lambda x: x[key_column])
    return return_value


def string2list(string_value: str, separator: str = ',') -> list:
    return string_value.split(separator)
