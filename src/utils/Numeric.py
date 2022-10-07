import random
import utils.Lists as ListUtils


def cleanup_integer(value: int) -> str:
    if value is None:
        return_value = ''
    else:
        return_value = str(int(value))

    return return_value


def get_list_of_numbers(nbr_elements_requested: int, min_value: int, max_value: int, unique_values: bool = False) -> list:
    generated_numbers = []
    max_numbers_in_range = max_value - min_value
    if nbr_elements_requested > max_numbers_in_range:
        nbr_elements_requested = max_numbers_in_range

    while len(generated_numbers) < nbr_elements_requested:
        generated_value = random.randint(min_value, int(max_value))
        generated_numbers.append(generated_value)

        if unique_values:
            if not ListUtils.element_in_list(list_to_search=generated_numbers, search_value=generated_value):
                generated_numbers.append(generated_value)
        else:
            generated_numbers.append(generated_value)

    return generated_numbers


def get_random_number(max_value: int) -> int:
    generated_number = random.randint(0, max_value)
    return generated_number


def get_random_number_with_preceding_characters(max_nbr_characters_excl_prefix: int, prefix: str = None) -> str:
    max_nbr = ''
    counter001 = 0
    while counter001 < max_nbr_characters_excl_prefix:
        max_nbr = max_nbr + '9'
        counter001 += 1

    generated_number = random.randint(0, int(max_nbr))

    if prefix is None:
        prefix = ''

    return_value = '{}{}'.format(prefix, str(generated_number).zfill(max_nbr_characters_excl_prefix))

    return return_value


def get_random_number_between_border(min_value: int, max_value: int) -> int:
    return random.randint(int(min_value), int(max_value))
