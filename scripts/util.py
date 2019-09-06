import os

def find_files(path_to_dir, suffix='.csv'):
    filenames = os.listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]
