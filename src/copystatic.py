import os
import shutil


def copy_files_recursive(src, dest):
    if not os.path.exists(src):
        raise Exception(f"Path doesn't exists {src}")

    if not os.path.exists(dest):
        os.mkdir(dest)

    for filename in os.listdir(src):
        source_path = os.path.join(src, filename)
        dest_path = os.path.join(dest, filename)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_files_recursive(source_path, dest_path)
