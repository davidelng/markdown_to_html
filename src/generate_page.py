import os
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

    print("Reading markdown file")
    markdown_handle = open(from_path)
    markdown = markdown_handle.read()
    markdown_handle.close()

    print("Reading template file")
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

    print("Writing output file")
    dest_dirs = os.path.dirname(dest_path)
    if not os.path.exists(dest_dirs):
        os.makedirs(dest_dirs)
    output = open(dest_path, "w")
    output.write(template)
    output.close()
