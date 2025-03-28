import os
import shutil
from markdown_blocks import markdown_to_html_node

def main():
    shutil.rmtree("public/", True)
    print("Deleted the public directory")
    os.mkdir("public")
    print("created a new public directory")
    del_and_copy_all("static/", "public/")
    generate_pages_recursive("content/", "template.html", "public/")


def del_and_copy_all(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        print(f"created new {dest_dir} folder")
    for entry in os.listdir(source_dir):
        src_file_path = source_dir + entry
        if os.path.isfile(src_file_path):
            shutil.copy(src_file_path,dest_dir)
            print(f"copied {src_file_path} to {dest_dir}")
        else:
            del_and_copy_all(f"{source_dir}{entry}/", f"{dest_dir}{entry}/")

def extract_title(markdown):
    file_lines = markdown.split("\n")
    for line in file_lines:
        if line.startswith("# "):
            return line.lstrip("#").strip(" ")
    raise Exception("No h1 header in file")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_file = open(from_path).read()
    template_file = open(template_path).read()
    html_node = markdown_to_html_node(md_file)
    html_string = html_node.to_html()
    title = extract_title(md_file)
    new_template = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    index_file = open(dest_path + "index.html", "x+")
    index_file.write(new_template)
    index_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        print(f"created new {dest_dir_path} folder")
    template_file = open(template_path).read()
    for entry in os.listdir(dir_path_content):
        src_file_path = dir_path_content + entry
        if os.path.isfile(src_file_path):
            filename = os.path.splitext(entry)[0]
            md_file = open(src_file_path).read()
            html_node = markdown_to_html_node(md_file)
            html_string = html_node.to_html()
            title = extract_title(md_file)
            new_template = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
            new_file = open(dest_dir_path + filename + ".html", "x+")
            new_file.write(new_template)
            new_file.close()
        else:
            generate_pages_recursive(f"{dir_path_content}{entry}/",template_path, f"{dest_dir_path}{entry}/")





main()