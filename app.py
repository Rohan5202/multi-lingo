from flask import Flask, render_template, jsonify, request
import os
import PyPDF2
from googletrans import Translator
import googletrans
import cv2
import pytesseract

app = Flask(__name__)

if not os.path.isdir(os.path.join(os.getcwd(),'images')):
   os.mkdir(os.path.join(os.getcwd(),'images'))

custom_config = r'--oem 3 --psm 6'

pytesseract.pytesseract.tesseract_cmd = './.apt/usr/share/tesseract-ocr/4.00/tessdata'
# print(googletrans.LANGUAGES)
@app.route("/")
def front():
    return render_template('index.html')

@app.route("/display", methods=['POST'])
def display():
    text=request.form['lan']
    # print(text)
    file = request.files['myfile']
    pathOfFile = os.path.join(os.getcwd(), 'images', file.filename)
    file.save(pathOfFile)
    a=PyPDF2.PdfFileReader(os.path.join(os.getcwd(),'images',file.filename))
    stri=""
    count_page=a.getNumPages()
    # k='i warnd that not more than 10 pages
    if count_page>10:
     for i in range(0,5):
        stri+=a.getPage(i).extractText()
    else:
        for i in range(0,count_page):
         stri+=a.getPage(i).extractText()

    m=text
    print(stri)
    translator = Translator()
    translated = translator.translate(stri,dest=m)
    p=translated.text

    # print(p)
    app_data={
    "TRANSLATED":p
    }
    os.remove(pathOfFile)
    return render_template('display.html',app_data=app_data)

@app.route("/nischay", methods=["POST"])
def img_text():
    image=request.files['im']
    pathofFile = os.path.join(os.getcwd(), 'images', image.filename)
    image.save(pathofFile)
    img = cv2.imread(pathofFile)   
    print(img)
    text=pytesseract.image_to_string(img)
    print(text)
    translator=Translator()
    translation1=translator.translate(text,dest="hi")
    print(translation1.text)
    app_data={
    "trn":translation1.text
    }
    return render_template('nischay.html',app_data=app_data)
    
if __name__=="__main__":
    app.run(debug=True)
