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
import base64

import io

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


@app.route('/train')
def train():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select distinct name from known_faces")

    rows = cur.fetchall()

    return render_template("train.html")

@app.route('/train', methods=['POST'])
def train_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = face_recognition.load_image_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
            print("Found: {} face(s) in the uploaded image.".format(len(face_locations)))

            lFaces = []
            for face_loc in face_locations:
                top, right, bottom, left = face_loc
                print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                #lFaces.append(base64.b64encode(pil_image.tobytes()).decode('utf-8'))

                buff_img= io.BytesIO()
                pil_image.save(buff_img, "PNG")
                img_str = base64.b64encode(buff_img.getvalue()).decode('ascii')
                lFaces.append(img_str)


            data_uri = base64.b64encode(open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb').read()).decode('utf-8')
            img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)

            

    #return redirect(request.url)
    return render_template("train.html", img_tag=data_uri, faces=lFaces)

if __name__ == "__main__":
    app.run('0.0.0.0', '5000', True)
