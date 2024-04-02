def get_text_before_colon(input_string):
    # Find the index of the first occurrence of ":"
    colon_index = input_string.find(":")

    # If ":" exists in the string
    if colon_index != -1:
        # Return the text before ":"
        return input_string[:colon_index].strip()
    else:
        # Return the whole string if ":" is not found
        return input_string.strip()