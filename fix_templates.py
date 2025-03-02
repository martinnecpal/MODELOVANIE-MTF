import os
import re

TEMPLATE_DIR = "templates"  # Set your templates folder

def convert_to_flask_links(file_path):
    """Read an HTML file and replace href/src paths with Flask-friendly url_for()."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace href="assets/..." → href="{{ url_for('static', filename='assets/...') }}"
    content = re.sub(r'href="assets/(.*?)"', r'href="{{ url_for(\'static\', filename=\'assets/\1\') }}"', content)

    # Replace src="assets/..." → src="{{ url_for('static', filename='assets/...') }}"
    content = re.sub(r'src="assets/(.*?)"', r'src="{{ url_for(\'static\', filename=\'assets/\1\') }}"', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def process_templates():
    """Loop through all HTML files in the templates folder."""
    for root, _, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                convert_to_flask_links(file_path)

# Run the script
process_templates()