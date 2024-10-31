# explain.py

import os
from PIL import Image

def create_spritesheet_images():
    # Ask for user inputs
    folder_path = input("Enter the folder path containing the spritesheets: ").replace('"','')

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            spritesheet_path = os.path.join(folder_path, filename)
            spritesheet_name = os.path.splitext(filename)[0]
            output_dir = os.path.join(folder_path, spritesheet_name)
            os.makedirs(output_dir, exist_ok=True)

            # Load the spritesheet
            spritesheet = Image.open(spritesheet_path)

            # Ask for user inputs for rows and columns
            rows = int(input(f"Enter the number of rows for {filename}: "))  # New input for rows
            columns = int(input(f"Enter the number of columns for {filename}: "))  # New input for columns

            # Calculate width and height based on the spritesheet dimensions
            width = spritesheet.width // columns  # Calculate width based on columns
            height = spritesheet.height // rows    # Calculate height based on rows

            # Extract and save each sprite
            for row in range(rows):
                for col in range(columns):  # Use the new columns input
                    left = col * width
                    upper = row * height
                    right = left + width
                    lower = upper + height
                    sprite = spritesheet.crop((left, upper, right, lower))
                    
                    # Ensure the sprite touches the borders and resize it
                    sprite = ensure_image_touches_borders(sprite)

                    sprite.save(os.path.join(output_dir, f"{spritesheet_name}_{row * columns + col + 1}.png"))

def create_sprites_from_columns():
    # Ask for user input
    folder_path = input("Enter the folder path containing the spritesheets: ")

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            spritesheet_path = os.path.join(folder_path, filename)
            spritesheet_name = os.path.splitext(filename)[0]
            output_dir = os.path.join(folder_path, spritesheet_name)
            os.makedirs(output_dir, exist_ok=True)

            # Load the spritesheet
            spritesheet = Image.open(spritesheet_path)

            #spritesheet = remove_empty_space(spritesheet)

            # Ask for the number of columns for the current image
            columns = int(input(f"Enter the number of columns for {filename}: "))
            # Calculate rows based on the image height and sprite height
            sprite_height = spritesheet.height  # Use the full height for a single row
            rows = 1  # Since the height is fixed, we only have one row

            # Extract and save each sprite
            for col in range(columns):
                left = col * (spritesheet.width // columns)
                upper = 0  # Always start from the top
                right = left + (spritesheet.width // columns)
                lower = upper + sprite_height
                sprite = spritesheet.crop((left, upper, right, lower))
                sprite.save(os.path.join(output_dir, f"{spritesheet_name}_{col + 1}.png"))

            # Check if sprites were created
            if not os.listdir(output_dir):  # If the output directory is empty
                print(f"No sprites created for {filename}. Check dimensions or input.")



def adjust_height():
    # Ask for user inputs
    folder_path = input("Enter the folder path containing the images: ").replace('"','')
    cut_height = int(input("Enter the height to cut from the top: "))

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, f"adjusted_{filename}")

            # Load the image
            image = Image.open(image_path)

            # Calculate new height and crop the image
            new_height = image.height - cut_height
            if new_height > 0:  # Ensure the new height is valid
                cropped_image = image.crop((0, cut_height, image.width, image.height))
                cropped_image.save(output_path)
            else:
                print(f"Cannot cut {cut_height} from {filename}. Height is too small.")

def adjust_width_both_sides():
    # Ask for user inputs
    folder_path = input("Enter the folder path containing the images: ").replace('"','')
    cut_width = int(input("Enter the width to cut from both sides: "))

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, f"adjusted_{filename}")

            # Load the image
            image = Image.open(image_path)

            # Calculate new width and crop the image
            new_width = image.width - (2 * cut_width)
            if new_width > 0:  # Ensure the new width is valid
                cropped_image = image.crop((cut_width, 0, image.width - cut_width, image.height))
                cropped_image.save(output_path)
            else:
                print(f"Cannot cut {cut_width} from {filename}. Width is too small.")

def adjust_height_both_sides():
    # Ask for user inputs
    folder_path = input("Enter the folder path containing the images: ").replace('"','')
    cut_height = int(input("Enter the height to cut from both top and bottom: "))  # Updated prompt

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, f"adjusted_{filename}")

            # Load the image
            image = Image.open(image_path)

            # Calculate new height and crop the image
            new_height = image.height - (2 * cut_height)  # Adjusted for both top and bottom
            if new_height > 0:  # Ensure the new height is valid
                cropped_image = image.crop((0, cut_height, image.width, image.height - cut_height))  # Adjusted crop
                cropped_image.save(output_path)
            else:
                print(f"Cannot cut {cut_height} from {filename}. Height is too small.")

def scale_images(folder_path, scale_factor):
    # Ask for user inputs
    

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, f"scaled_{filename}")

            # Load the image
            image = Image.open(image_path)

            # Calculate new dimensions
            new_width = int(image.width * scale_factor)
            new_height = int(image.height * scale_factor)

            # Scale the image using LANCZOS filter
            scaled_image = image.resize((new_width, new_height), Image.LANCZOS)
            scaled_image.save(output_path)

def ensure_image_touches_borders(image, border_threshold=0):
    """
    Ensure the image touches at least two borders in one axis.
    If not, crop the image until it does, then resize to 64x64.

    :param image: PIL Image object
    :param border_threshold: Minimum pixel value to consider as touching the border
    :return: Cropped and resized PIL Image object
    """
    width, height = image.size

    # Check vertical borders (top and bottom)
    top_touching = image.getbbox()[1] <= border_threshold  # Top border
    bottom_touching = image.getbbox()[3] >= height - border_threshold  # Bottom border

    # Check horizontal borders (left and right)
    left_touching = image.getbbox()[0] <= border_threshold  # Left border
    right_touching = image.getbbox()[2] >= width - border_threshold  # Right border

    # If not touching at least two borders in one axis, crop
    if not (top_touching and bottom_touching) and not (left_touching and right_touching):
        # Crop the image to ensure it touches at least two borders
        if not top_touching and not bottom_touching:
            # Crop from top and bottom
            new_image = image.crop((0, border_threshold, width, height - border_threshold))
        else:
            new_image = image  # No cropping needed if it touches at least two borders

        # Resize the image to 64x64
        new_image = new_image.resize((64, 64), Image.LANCZOS)
        return new_image

    # Resize the original image to 64x64 if already touching at least two borders
    return image.resize((64, 64), Image.LANCZOS)


#create_sprites_from_columns()
#adjust_height_both_sides()
#adjust_height()
#adjust_width_both_sides()
create_spritesheet_images()
scale_images()