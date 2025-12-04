import uuid


def generate_unique_filepath(path: str, file_type) -> str:
    return path + "/" + str(uuid.uuid4()) + "." + file_type


def format_size(size_in_bytes: int) -> int:
    return round(size_in_bytes / 1048576)