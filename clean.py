import os
import sys
import shutil

# Default folder names to search for virtual environments and node_modules
DEFAULT_VENV_FOLDERS = ['.venv', 'venv', 'node_modules', '.mypy_cache']


def is_virtual_env_or_node_modules(path):
    """
    Check if a directory is a Python virtual environment or a node_modules directory.
    """
    return (
        # Check for virtual environment indicators
        os.path.isfile(os.path.join(path, 'pyvenv.cfg')) or
        os.path.isdir(os.path.join(path, 'bin')) and os.path.isfile(os.path.join(path, 'bin', 'python')) or
        os.path.isdir(os.path.join(path, 'Scripts')) and os.path.isfile(os.path.join(path, 'Scripts', 'python.exe')) or
        # Check if it is a node_modules directory
        os.path.basename(path) == 'node_modules' or
        os.path.basename(path) == '.mypy_cache'
    )


def delete_directory(path, skip_confirmation):
    """Delete the specified directory, with optional confirmation."""
    if not skip_confirmation:
        confirm = input(
            f"Do you want to delete the directory at {path}? (y/n, default: y): ").strip().lower()

        # Treat empty input (Enter) as 'y'
        if confirm not in ('y', 'n', ''):
            print("Invalid input. Skipped deletion.")
            return
        if confirm == 'n':
            print(f"Skipped deletion of: {path}")
            return

    try:
        shutil.rmtree(path)
        print(f"Deleted directory at: {path}")
    except Exception as e:
        print(f"Error deleting {path}: {e}")


def find_and_delete_dirs(root_path, skip_confirmation, search_folders):
    """Recursively find and delete specified directories like virtual environments and node_modules."""
    for dirpath, dirnames, filenames in os.walk(root_path):
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            if dirname in search_folders and is_virtual_env_or_node_modules(full_path):
                delete_directory(full_path, skip_confirmation)
                # Prevent os.walk from traversing deleted directories
                dirnames.remove(dirname)


def parse_arguments():
    """Parse command-line arguments to get the root path, skip confirmation flag, and folders to search."""
    if len(sys.argv) < 2:
        print(
            "Usage: python delete_dirs.py <path> [--skip-confirmation] [--add <folder1,folder2,...>] [--replace <folder1,folder2,...>]")
        sys.exit(1)

    root_path = sys.argv[1]
    skip_confirmation = '--skip-confirmation' in sys.argv

    # Handle additional folder names
    search_folders = DEFAULT_VENV_FOLDERS.copy()
    if '--add' in sys.argv:
        add_index = sys.argv.index('--add') + 1
        additional_folders = sys.argv[add_index].split(',')
        search_folders.extend(additional_folders)

    if '--replace' in sys.argv:
        replace_index = sys.argv.index('--replace') + 1
        search_folders = sys.argv[replace_index].split(',')

    return root_path, skip_confirmation, search_folders


if __name__ == "__main__":
    root_path, skip_confirmation, search_folders = parse_arguments()

    if not os.path.isdir(root_path):
        print("Error: The specified path does not exist or is not a directory.")
        sys.exit(1)

    find_and_delete_dirs(root_path, skip_confirmation, search_folders)
