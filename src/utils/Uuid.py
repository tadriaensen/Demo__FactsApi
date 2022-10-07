import uuid


def generate_uuid(remove_hyphen: bool = False) -> str:
    generated_value = str(uuid.uuid4())
    if remove_hyphen:
        generated_value = generated_value.replace('-', '')
    return generated_value
