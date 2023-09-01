import zipfile
import os
from flask import abort

def extract_book(epub_book, id):
    extract_directory = f'data/{id}'
    try:
        os.makedirs(extract_directory)
    except FileExistsError:
        return FileExistsError('file already exists!!!')
    with zipfile.ZipFile(epub_book, 'r') as zip:
        zip.extractall(extract_directory)
        print("File successfully unzipped!")
