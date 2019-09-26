import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from PIL import Image
import face_recognition

ALLOWED_EXTENSION = set( [ 'png', 'jpg', 'jpeg' ] )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION 

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
        if request.method == 'POST':
        # check if the post request has the file part
                if 'file' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                        flash('No file selected for uploading')
                        return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    #file = request.files.get('file')
                    #    img = file.stream.read()
                    image = face_recognition.load_image_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    face_locations = face_recognition.face_locations(image)
                    flash("Found {} face(s) in the photo.".format(len(face_locations)))

                    #filename = secure_filename(file.filename)
                    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash('File successfully uploaded')
                    return redirect('/')
                else:
                        flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                        return redirect(request.url)

if __name__ == "__main__":
    app.run()
