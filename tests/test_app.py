import os
import pytest
from io import BytesIO
from flask_app.app import app, images

pytestmark = pytest.mark.filterwarnings("ignore:.*ast.Str is deprecated.*")

# Configure pytest fixtures
@pytest.fixture
def client():
    """Set up a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    client = app.test_client()

    # Ensure the test upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    yield client

    # Teardown: Remove all files in the test upload folder and delete the folder
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir(app.config['UPLOAD_FOLDER'])

    # Clear the images list
    images.clear()

# Test cases
def test_index_page(client):
    """Test the index page renders successfully."""
    response = client.get('/')
    assert response.status_code == 200

    # Debug: Print response data for troubleshooting
    print(response.data.decode('utf-8'))

    # Update the assertion to match the actual title
    assert b'<title>Image Gallery - Upload and Explore</title>' in response.data


def test_upload_image(client):
    """Test uploading a valid image."""
    data = {
        'image': (BytesIO(b"dummy image content"), 'test_image.png'),
        'description': 'A test image'
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert b'File successfully uploaded!' in response.data

    # Verify the image was added to the list
    assert len(images) == 1
    assert images[0]['filename'] == 'test_image.png'

def test_upload_invalid_file(client):
    """Test uploading an invalid file type."""
    data = {
        'image': (BytesIO(b"dummy text content"), 'test_file.txt'),
        'description': 'A test text file'
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid file type' in response.data

    # Ensure the image list is still empty
    assert len(images) == 0

def test_delete_image(client):
    """Test deleting an image."""
    # First, upload an image
    data = {
        'image': (BytesIO(b"dummy image content"), 'test_image_to_delete.png'),
        'description': 'A test image to delete'
    }
    client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)

    # Delete the uploaded image
    response = client.post('/delete/0', follow_redirects=True)
    assert response.status_code == 200
    assert b'Image deleted successfully' in response.data

    # Verify the image list is empty
    assert len(images) == 0
