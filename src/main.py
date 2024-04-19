import os
import shutil
from copystatic import copy_files_recursive
from generate_content import generate_pages_recursive

dir_static = "./static"
dir_public = "./public"
dir_content = "./content"
template_path = "./template.html"


def main():
    if os.path.exists(dir_public):
        print("Removing old public assets")
        shutil.rmtree(dir_public)
    print("Copying new static assets")
    copy_files_recursive(dir_static, dir_public)
    generate_pages_recursive(dir_content, template_path, dir_public)


main()
