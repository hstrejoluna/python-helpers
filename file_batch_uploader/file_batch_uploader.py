import os
import boto3
import tkinter as tk
from tkinter import filedialog
from botocore.client import Config
from botocore.exceptions import ClientError
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# Replace these with your DigitalOcean Spaces credentials and target Space
DO_SPACES_KEY = os.getenv("DO_SPACES_KEY")
DO_SPACES_SECRET = os.getenv("DO_SPACES_SECRET")
DO_SPACES_REGION = os.getenv("DO_SPACES_REGION")
DO_SPACES_NAME = os.getenv("DO_SPACES_NAME")

# Set up the boto3 client
session = boto3.session.Session()
config = Config(
    signature_version="s3v4",
    retries={"max_attempts": 10, "mode": "standard"},
    read_timeout=300,
    connect_timeout=300,
)
client = session.client(
    "s3",
    region_name=DO_SPACES_REGION,
    endpoint_url=f"https://{DO_SPACES_REGION}.digitaloceanspaces.com",
    aws_access_key_id=DO_SPACES_KEY,
    aws_secret_access_key=DO_SPACES_SECRET,
    config=config,
)

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path

def upload_file(client, local_path, space_name, space_key):
    try:
        with open(local_path, "rb") as f:
            print(f"Uploading {local_path} to {space_key}")
            client.upload_fileobj(f, space_name, space_key, ExtraArgs={"ACL": "public-read"})
    except ClientError as e:
        print(f"Error uploading {local_path} to {space_key}: {e}")

def upload_folder(client, folder_path, space_name, prefix=""):
    file_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, folder_path)
            space_key = os.path.join(prefix, relative_path).replace("\\", "/")
            file_list.append((local_path, space_key))
    
    for local_path, space_key in tqdm(file_list, desc="Uploading files"):
        upload_file(client, local_path, space_name, space_key)

# Replace these with your folder path and optional Space prefix
folder_path = select_folder()
space_prefix = "images/programs/"

upload_folder(client, folder_path, DO_SPACES_NAME, space_prefix)
