import os
import shutil
from block_markdown import markdown_to_html_node, extract_title


def copy_static_to_public(src_dir, dest_dir):
    """
    Recursively copy all contents from source directory to destination directory.
    
    This function:
    1. Deletes the destination directory if it exists
    2. Creates a fresh destination directory
    3. Recursively copies all files and subdirectories
    
    Args:
        src_dir: Path to the source directory (e.g., "static")
        dest_dir: Path to the destination directory (e.g., "public")
    """
    # Delete the destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Deleting existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    print(f"Creating directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    # Recursively copy contents
    _copy_directory_contents(src_dir, dest_dir)


def _copy_directory_contents(src_dir, dest_dir):
    """
    Helper function to recursively copy directory contents.
    
    Args:
        src_dir: Path to the source directory
        dest_dir: Path to the destination directory
    """
    # List all items in the source directory
    items = os.listdir(src_dir)
    
    for item in items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(src_path):
            # It's a file, copy it
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            # It's a directory, create it and recurse
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_directory_contents(src_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template file
        dest_path: Path where the generated HTML should be written
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the generated HTML to the destination
    with open(dest_path, 'w') as f:
        f.write(final_html)
    
    print(f"Page generated successfully at {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages from all markdown files in a directory.
    
    Args:
        dir_path_content: Path to the content directory containing markdown files
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory for generated HTML files
    """
    # List all items in the content directory
    items = os.listdir(dir_path_content)
    
    for item in items:
        src_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(src_path):
            # It's a file - check if it's a markdown file
            if item.endswith('.md'):
                # Convert .md extension to .html
                dest_filename = item[:-3] + '.html'
                dest_path = os.path.join(dest_dir_path, dest_filename)
                
                # Generate the HTML page
                generate_page(src_path, template_path, dest_path)
        else:
            # It's a directory - create corresponding directory in dest and recurse
            new_dest_dir = os.path.join(dest_dir_path, item)
            if not os.path.exists(new_dest_dir):
                os.makedirs(new_dest_dir)
            
            # Recursively process the subdirectory
            generate_pages_recursive(src_path, template_path, new_dest_dir)


def main():
    """Main function to generate the static site."""
    print("Starting static site generation...")
    
    # Get the path relative to where the script is located
    # Since main.py is in src/, we need to go up one level to access root files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    static_dir = os.path.join(root_dir, "static")
    public_dir = os.path.join(root_dir, "public")
    content_dir = os.path.join(root_dir, "content")
    template_path = os.path.join(root_dir, "template.html")
    
    # Copy static files to public directory
    copy_static_to_public(static_dir, public_dir)
    
    # Generate all pages recursively
    generate_pages_recursive(content_dir, template_path, public_dir)
    
    print("\nStatic site generation complete!")


if __name__ == "__main__":
    main()
