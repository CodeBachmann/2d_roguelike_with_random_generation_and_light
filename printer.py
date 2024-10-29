import os

def print_image_files(directory):
    # List all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file is an image (you can add more extensions if needed)
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(filename)

# Specify the path to the graphics/icons directory
icons_directory = 'graphics/icons'
print_image_files(icons_directory)