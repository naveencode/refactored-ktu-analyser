from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from pdftotext import convert_pdf_to_txt
from data_extract import extractor

app = Flask(__name__)


def convert_file(source, destination):
   
    raw_text = convert_pdf_to_txt(source)
    text_file = open(destination, "w")
    text_file.write(raw_text)
    text_file.close()
    extractor(destination, "converted/result.csv")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        f = request.files['pdf']
        f.save('uploads/result.pdf')
        convert_file('uploads/result.pdf', "converted/result.txt")
        return send_from_directory('converted',
                                   'result.csv', as_attachment=True)
    return render_template('index.html')




# @app.route('/', methods=['POST', 'GET'])
# def get_url():
#     error = None
#     if request.method == 'POST':
#         if(valid_url(request.form['url'])):
#             return download_pdf(request.form['url'])
#         else:
#             error = 'Invalid URL'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('index.html', error=error)
