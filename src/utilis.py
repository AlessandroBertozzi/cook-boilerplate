import json
import os
import glob


def find_json_files(directory):
    # Create a pattern for matching JSON files
    pattern = os.path.join(directory, '*.json')

    # Use glob.glob to find all files in the directory matching the pattern
    json_files = glob.glob(pattern)

    return json_files


# Function to save data to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# Function to load data from a JSON file
def load_from_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def check_and_create_dir(dir_path):
    """
    Check if a directory exists at the specified path, and create it if it does not.

    Parameters:
    - dir_path (str): The path of the directory to check and potentially create.

    Returns:
    None
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        pass


def delete_file(file_path):
    """
    Deletes a specific file.

    :param file_path: Path to the file to be deleted.
    """
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
