import os

# Path to your Downloads folder (works for most systems)
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

# Name of the project folder
project_folder = os.path.join(downloads_folder, "project-folder")

# List of HTML files to create
html_files = [
    "index.html",
    "home.html",
    "skills.html",
    "projects.html",
    "experience.html",
    "education.html",
    "resume.html",
    "certifications.html",
    "contact.html"
]

# HTML template for each file
template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-black text-white">
    <div class="min-h-screen flex items-center justify-center">
        <h1 class="text-4xl font-bold text-green-400">{title}</h1>
    </div>
</body>
</html>
"""

# Create project folder
os.makedirs(project_folder, exist_ok=True)

# Create HTML files
for filename in html_files:
    title = filename.replace(".html", "").capitalize()
    file_path = os.path.join(project_folder, filename)
    with open(file_path, "w") as file:
        file.write(template.format(title=title))

print(f"✅ Project folder with HTML files created at: {project_folder}")
