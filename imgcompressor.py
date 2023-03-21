import os
import tinify
import requests
from tkinter import filedialog
from tkinter import Tk

tinify.key = 'wrXV04WBGN3fzc7wZdvHNFxQpk2nf8Fk'
convertio_api_key = 'df208fd10a5e79b6316f3dfab8d82978'  # Replace this with your Convertio API key

def compress_image(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(input_folder, filename)
            
            # Save compressed JPEG (or PNG) version
            output_file_path = os.path.join(output_folder, filename)
            source = tinify.from_file(file_path)
            source.to_file(output_file_path)
            print(f"Compressed {filename} and saved to {output_file_path}")

            # Save WebP version using Convertio API
            output_file_path_webp = os.path.join(output_folder, os.path.splitext(filename)[0] + '.webp')
            convert_to_webp(file_path, output_file_path_webp)

def convert_to_webp(input_file_path, output_file_path):
    # Start the conversion process
    url = f'https://api.convertio.co/convert?apikey={convertio_api_key}&inputformat=auto&outputformat=webp'
    with open(input_file_path, 'rb') as file:
        response = requests.post(url, files={'file': file}).json()

    if 'data' not in response:
        print(f"Error during conversion: {response}")
        return

    conversion_id = response['data']['id']

    # Check the status and download the converted file
    status_url = f'https://api.convertio.co/convert/{conversion_id}/status?apikey={convertio_api_key}'
    while True:
        status_response = requests.get(status_url).json()
        if status_response['status'] == 'finished':
            download_url = status_response['output']['url']
            download_response = requests.get(download_url)
            with open(output_file_path, 'wb') as output_file:
                output_file.write(download_response.content)
            print(f"WebP version saved to {output_file_path}")
            break
        elif status_response['status'] == 'error':
            print(f"Error during conversion: {status_response}")
            break

def choose_folder():
    root = Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory()
    return folder_path

if __name__ == '__main__':
    input_folder = choose_folder()  # Select the folder containing the images to compress
    output_folder = 'output_images'  # Folder where the compressed images and WebP versions will be saved

    if input_folder:
        compress_image(input_folder, output_folder)
    else:
        print("No folder selected. Exiting.")
