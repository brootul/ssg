# main.py
import os
import logging
from htmlnode import markdown_to_html_node, extract_title

# Setting up logging
logging.basicConfig(level=logging.INFO)

def copy_file(src, dest):
    """
    Copy the contents of a file from src to dest.
    """
    with open(src, 'rb') as f_src:
        with open(dest, 'wb') as f_dest:
            f_dest.write(f_src.read())
            logging.info(f"Copied: {src} to {dest}")

def copy_directory_contents(src, dest):
    """
    Copies the contents of src directory to dest directory recursively.
    """
    if not os.path.exists(dest):
        os.makedirs(dest)
        logging.info(f"Created directory: {dest}")

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            copy_directory_contents(src_path, dest_path)
        else:
            copy_file(src_path, dest_path)

def clear_directory(dir_path):
    """
    Clears the contents of the given directory path.
    """
    if os.path.exists(dir_path):
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            if os.path.isdir(item_path):
                clear_directory(item_path)
                os.rmdir(item_path)
                logging.info(f"Removed directory: {item_path}")
            else:
                os.remove(item_path)
                logging.info(f"Removed: {item_path}")

def generate_page(from_path, template_path, dest_path):
    """
    Generates an HTML page from a markdown file using a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, 'r') as md_file:
        markdown_content = md_file.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(markdown_content).to_html()

    # Extract the title
    title = extract_title(markdown_content)

    # Read the template file
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    # Replace placeholders in the template
    page_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Create necessary directories if they don't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the new HTML to the destination file
    with open(dest_path, 'w') as dest_file:
        dest_file.write(page_content)
        logging.info(f"Generated page at {dest_path}")

def main():
    # Paths for the source and destination directories
    src_directory = "static"
    dest_directory = "public"

    # Clear the destination directory
    clear_directory(dest_directory)

    # Copy the contents from the source to the destination
    copy_directory_contents(src_directory, dest_directory)

    # Now generate the index.html page from the markdown file
    from_path = 'content/index.md'
    template_path = 'template.html'
    dest_path = os.path.join(dest_directory, 'index.html')

    # Generate the index.html page
    generate_page(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
    