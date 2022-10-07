import utils.String as StringUtils


def url_has_query_string(url: str) -> bool:
    try:
        if len(url_breakdown(url=url)['response_body']['query_params']) > 0:
            return_value = True
        else:
            return_value = False
    except:
        return_value = False

    return return_value


def url_breakdown(url: str) -> dict:
    return_value = {'status': '', 'error_message': '', 'response_body': {}}

    try:
        return_value['response_body']['url'] = url
        return_value['response_body']['scheme'] = url.split('://', 1)[0]
        return_value['response_body']['authority'] = StringUtils.substring(string_value=StringUtils.right(string_value=url,
                                                                                                          count=len(url) - len('{}://'.format(return_value['response_body']['scheme']))
                                                                                                          ),
                                                                           start_string='',
                                                                           end_string='/')
        return_value['response_body']['path'] = StringUtils.substring(string_value=StringUtils.right(string_value=url,
                                                                                                     count=len(url) - len('{}://{}'.format(return_value['response_body']['scheme'], return_value['response_body']['authority']))
                                                                                                     ),
                                                                      start_string='',
                                                                      end_string='?')
        return_value['response_body']['query_params'] = []
        return_value['response_body']['anchors'] = []
        if len(url.split('?')) > 1:
            for qry_param in url.split('?')[1].split('&'):
                if qry_param != '':
                    if len(qry_param.split('=', 1)) == 2:
                        key = qry_param.split('=', 1)[0]
                        value = qry_param.split('=', 1)[1]
                    else:
                        key = 'unknown'
                        value = qry_param
                    if len(value.split('#')) > 1:
                        return_value['response_body']['anchors'].append(value.split('#')[1])
                    else:
                        return_value['response_body']['query_params'].append({'key': key, 'value': value})

        return_value['status'] = 'SUCCESS'
    except:
        return_value['status'] = 'FAILED'
        return_value['error_message'] = 'Unable to break down the supplied url.'

    return return_value
