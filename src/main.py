import os
import shutil
from copystatic import copy_files_recursive
from generate_page import generate_page

dir_static = "./static"
dir_public = "./public"


def main():
    if os.path.exists(dir_public):
        print("Removing old public assets")
        shutil.rmtree(dir_public)
    print("Copying new static assets")
    copy_files_recursive(dir_static, dir_public)
    generate_page("./content/index.md", "./template.html", "public/index.html")


main()
