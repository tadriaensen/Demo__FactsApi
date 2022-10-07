def to_bool(value: str) -> bool:
    valid = {'true': True, 't': True, '1': True, 'yes': True, 'ja': True, 'on': True,
             'false': False, 'f': False, '0': False, 'no': False, 'nee': False, 'off': False
             }

    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        raise ValueError('Invalid literal for boolean. Not a string.')

    lower_value = value.lower()
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError('Invalid literal for boolean: "%s"' % value)
