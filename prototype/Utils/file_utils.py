import os

def get_file_content(file_dir, file_name):
    try:
        file_path = os.path.join(file_dir, file_name)
        with open(file_path, 'r') as file:
            content = file.read()

        return content
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return ""