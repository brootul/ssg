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
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}")

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generates HTML pages for each markdown file found in dir_path_content.
    """
    for item in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, item)
        
        if os.path.isdir(full_path):
            # Create a corresponding subdirectory in the destination directory
            sub_dest_path = os.path.join(dest_dir_path, item)
            os.makedirs(sub_dest_path, exist_ok=True)
            # Recurse into the subdirectory
            generate_pages_recursive(full_path, template_path, sub_dest_path)
        elif item.endswith('.md'):
            # Found a markdown file, generate an HTML page
            markdown_file = full_path
            html_file = os.path.join(dest_dir_path, item.replace('.md', '.html'))
            generate_page(markdown_file, template_path, html_file)

def main():
    # Paths for the source and destination directories
    src_directory = "static"
    dest_directory = "public"

    # Clear the destination directory
    clear_directory(dest_directory)

    # Copy the contents from the source to the destination
    copy_directory_contents(src_directory, dest_directory)

    # Generate HTML pages for all Markdown files in the content directory
    content_directory = "content"  # Adjust this path if your content directory is different
    template_path = 'template.html'  # Adjust if necessary

    generate_pages_recursive(content_directory, template_path, dest_directory)

if __name__ == "__main__":
    main()
