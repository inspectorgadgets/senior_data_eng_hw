import argparse
import os
import re
from util import find_files

def fix_file(backup_file, fixed_file, regex_sub_dict):
    regex = re.compile(
        "(%s)" % "|".join(map(re.escape, regex_sub_dict.keys()))
            )

    print('Opening {} to check for errors, writing results to {}'.format(backup_file, fixed_file))

    with open(backup_file, 'r') as original:
        with open(fixed_file, 'w') as fixed:
            content = regex.sub(
                lambda x: regex_sub_dict[x.string[x.start(): x.end()]],
                original.read()
            )
            fixed.write(content)


parser = argparse.ArgumentParser(description='Fix input files')
parser.add_argument('--input-file-dir', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    files_to_fix = find_files(args.input_file_dir)
    
    print('Found the following files to fix:\n{}'.format('\n'.join(files_to_fix)))

    regex_sub_dict = {
        "\n,": ",",
        "\n\n": "\n",
        "\0": ""
    }

    # Make a backup dir for the original files to be fixed
    backup_dir = args.input_file_dir + '/backup'
    if not os.path.exists(backup_dir):
        print('Creating {} directory'.format(backup_dir))
        os.mkdir(backup_dir)

    for file in files_to_fix:
        original_file = args.input_file_dir + '/' + file
        # Keep a copy of the original files as a backup in /backup within the dataset directory
        backup_file = '{}/{}.bak'.format(backup_dir, file)
        print('Backup file will be {}'.format(backup_file))
        os.rename(original_file, backup_file)
        print('Moved {} to {}'.format(file, backup_dir))
        # Use the regex_sub_dict to replace any errors in the file 
        fix_file(backup_file, original_file, regex_sub_dict)

