import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Secret key for flash messages
app.secret_key = 'supersecretkey'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Upload folder configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# List to hold uploaded images (simulating database storage)
images = []

# Check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Render the gallery page with the list of uploaded images
    return render_template('gallery.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['image']
    description = request.form.get('description', '')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Add image to the list (simulating a database)
        images.append({'filename': filename, 'description': description})
        flash('File successfully uploaded!', 'success')
    else:
        flash('Invalid file type. Please upload an image file (png, jpg, jpeg, gif).', 'error')

    return redirect(url_for('index'))

@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    # Simulate deletion by removing the image from the list
    if 0 <= image_id < len(images):
        # Get the filename to delete it from the file system
        filename = images[image_id]['filename']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Remove file from the server
        if os.path.exists(file_path):
            os.remove(file_path)

        # Remove image from the list
        del images[image_id]
        flash('Image deleted successfully', 'success')
    else:
        flash('Error: Image not found', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
