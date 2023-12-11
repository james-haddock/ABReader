import pytest

from flask import Flask, request, session
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage
from src.controller import upload, app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_get(client):
    response = client.get('/upload')
    assert response.status_code == 200

@patch('src.controller.epub_validator')
@patch('src.controller.extract_book.extractbook')
@patch('src.controller.class_textbook.Textbook')
@patch('src.controller.crud_book.create_book_in_db')
@patch('src.controller.crud_textbook.create_textbook_in_db')
@patch('src.controller.s3_crud.upload_to_s3')
def test_upload_post_valid_epub(mock_upload_to_s3, mock_create_textbook_in_db, mock_create_book_in_db, mock_Textbook, mock_extractbook, mock_epub_validator, client):
    mock_epub_validator.return_value = True
    mock_file = MagicMock(spec=FileStorage)
    mock_file.filename = 'test.epub'
    data = {
        'file': (mock_file, 'test.epub')
    }
    with client.session_transaction() as session:
        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert ('message', 'Book uploaded successfully!') in session['_flashes']

@patch('src.controller.epub_validator')
def test_upload_post_invalid_epub(mock_epub_validator, client):
    mock_epub_validator.return_value = False
    mock_file = MagicMock(spec=FileStorage)
    mock_file.filename = 'test.epub'
    data = {
        'file': (mock_file, 'test.epub')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    with client.session_transaction() as session:
        assert ('message', 'Invalid file. Only valid EPUB files are allowed.') in session['_flashes']

def test_upload_post_no_file(client):
    response = client.post('/upload', content_type='multipart/form-data')
    assert response.status_code == 400
    with client.session_transaction() as session:
        assert ('message', 'No file selected') in session['_flashes']