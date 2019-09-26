import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

from PIL import Image
import face_recognition

import sqlite3
from flask import g

import json

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
                    # This loads the image from the diskfile where it was 
                    # uploaded. It would be much nicer to just read the bytes
                    # in directly, but it works for now
                    image = face_recognition.load_image_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
                    flash("Found {} face(s) in the photo.".format(len(face_locations)))

                    g.db = sqlite3.connect("database.db")
                    encodings = []    
                        
                    my_face_encoding = face_recognition.face_encodings(image)[0]

                    myEncoding = json.dumps(my_face_encoding.tolist())

                    flash('JSON: ' + myEncoding)

                    flash('File successfully uploaded')
                    return redirect('/')
                else:
                        flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                        return redirect(request.url)

@app.route('/list_faces')
def list_faces():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from known_faces")

    rows = cur.fetchall();

    return render_template("faces.html", rows = rows)

if __name__ == "__main__":
    app.run()
