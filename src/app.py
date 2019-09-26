from flask import Flask
import face_recognition
from sklearn import svm

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['clf'] = svm.SVC(gamma='scale')
