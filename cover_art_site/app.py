import os
from flask import Flask, render_template, request, url_for, jsonify, send_file, after_this_request
import eyed3
from eyed3.id3.frames import ImageFrame

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-mp3', methods=['POST'])
def upload_mp3():
    mp3_file = request.files['mp3']
    if mp3_file and allowed_file(mp3_file.filename, {'mp3'}):
        global mp3_filename
        mp3_filename = os.path.join(app.config['UPLOAD_FOLDER'], mp3_file.filename)
        print(mp3_filename)
        mp3_file.save(mp3_filename)
        return jsonify({'mp3_file_status': 'MP3 file uploaded successfully!'})
    return jsonify({'mp3_file_status': 'Invalid MP3 file!'})

@app.route('/upload-image', methods=['POST'])
def upload_image():
    image_file = request.files['image']
    if image_file and allowed_file(image_file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
        global image_filename
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        print(image_filename)
        image_file.save(image_filename)
        return jsonify({'image_file_status': 'Image uploaded successfully!'})
    return jsonify({'image_file_status': 'Invalid Image file!'})

@app.route('/overlay')
def overlay():
    mp3_file = eyed3.load(mp3_filename)
    if (mp3_file.tag == None):
        mp3_file.initTag()
    mp3_file.tag.images.set(ImageFrame.FRONT_COVER, open(image_filename, 'rb').read(), 'image/jpeg')
    mp3_file.tag.save()
    
    # @after_this_request
    # def remove_file(response):
    #     try:
    #         os.remove(mp3_filename)
    #         mp3_file.close()
    #     except Exception as error:
    #         app.logger.error('Error removing or closing downloaded file handle', error)
    #     return response
    
    return send_file(mp3_filename, as_attachment=True)
    
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    app.run(debug=True)
    
