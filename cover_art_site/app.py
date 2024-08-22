import os
from flask import Flask, render_template, request, url_for, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mp3_file_status = ''
image_file_status = ''

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-mp3', methods=['POST'])
def upload_mp3():
    mp3_file = request.files['mp3']
    if mp3_file and allowed_file(mp3_file.filename, {'mp3'}):
        mp3_filename = os.path.join(app.config['UPLOAD_FOLDER'], mp3_file.filename)
        mp3_file.save(mp3_filename)
        return jsonify({'mp3_file_status': 'MP3 file uploaded successfully!'})
    return jsonify({'mp3_file_status': 'Invalid MP3 file!'})

@app.route('/upload-image', methods=['POST'])
def upload_image():
    image_file = request.files['image']
    if image_file and allowed_file(image_file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_filename)
        return jsonify({'image_file_status': 'Image uploaded successfully!'})
    return jsonify({'image_file_status': 'Invalid Image file!'})
 
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    app.run(debug=True)