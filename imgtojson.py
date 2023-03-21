import os
import json

# Get the path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))


# Initialize an empty dictionary to store the image information
image_dict = {}

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image (you may need to modify this check for your specific use case)
    if filename.endswith(".jpg") or filename.endswith(".JPG"):
        # Create a dictionary to store the image information
        image_info = {"url": filename}
        # Add the image information to the image dictionary using the file name as the key
        image_dict[filename] = image_info

# Create a dictionary to store the image dictionary and the title
data = {"image": image_dict, "title": "Reconocimientos"}

# Write the data dictionary to a JSON file for each image file
for filename in image_dict:
    with open(os.path.join(script_dir, f"{filename}.json"), "w") as outfile:
        json.dump(data, outfile)
