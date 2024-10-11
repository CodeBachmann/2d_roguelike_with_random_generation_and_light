from csv import reader
import os
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in os.walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def load_images_from_folder(folder_path):
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):  # Add other formats if needed
                img_path = os.path.join(folder_path, filename)
                image = pygame.image.load(img_path).convert_alpha()  # Load the image
                images.append((image, filename))  # Store as a tuple (image, filename)
        return images