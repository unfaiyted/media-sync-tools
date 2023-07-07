    # Example usage of emby class:
def filter_array_by_key_value(array, key, value):
    filtered_array = [item for item in array if item.get(key) == value]
    return filtered_array
