import os
from pathlib import Path
from block_markdown import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("Title not found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise Exception(f"File not found {from_path}")

    if not os.path.exists(template_path):
        raise Exception(f"Template file not found {template_path}")

    print(f"Reading markdown file from {from_path}")
    markdown_handle = open(from_path)
    markdown = markdown_handle.read()
    markdown_handle.close()

    print(f"Reading template file {template_path}")
    template_handle = open(template_path)
    template = template_handle.read()
    template_handle.close()

    print("Generating HTML")
    html = markdown_to_html_node(markdown).to_html()
    print("Extracting title")
    title = extract_title(markdown)

    print("Replacing template variables")
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    print(f"Writing output file {dest_path}")
    dest_dirs = os.path.dirname(dest_path)
    if dest_dirs != "":
        os.makedirs(dest_dirs, exist_ok=True)
    output = open(dest_path, "w")
    output.write(template)
    output.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception(f"Invalid path {dir_path_content}")

    for filename in os.listdir(dir_path_content):
        outfile = os.path.join(dest_dir_path, filename)
        source_file_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(source_file_path):
            outfile = Path(outfile).with_suffix(".html")
            generate_page(source_file_path, template_path, outfile)
        else:
            generate_pages_recursive(source_file_path, template_path, outfile)
