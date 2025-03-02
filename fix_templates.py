import os
import re
import sys


def convert_to_flask_links(file_path):
    """Reads an HTML file and replaces href/src paths with Flask-friendly url_for()."""

    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure paths use forward slashes (important for Windows users)
    content = content.replace("\\", "/")

    # Replace href="assets/..." → href="{{ url_for('static', filename='assets/...') }}"
    content = re.sub(r'href="assets/(.*?)"', r'href="{{ url_for(\'static\', filename=\'assets/\1\') }}"', content)

    # Replace src="assets/..." → src="{{ url_for('static', filename='assets/...') }}"
    content = re.sub(r'src="assets/(.*?)"', r'src="{{ url_for(\'static\', filename=\'assets/\1\') }}"', content)

    # Write back to the same file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Successfully updated: {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python fix_template.py <path_to_html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    convert_to_flask_links(html_file)