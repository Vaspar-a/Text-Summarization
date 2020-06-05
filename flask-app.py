from flask import Flask, render_template, jsonify, make_response, request
from Doc_Summ import Doc_Summ
import os

app = Flask(__name__, template_folder='.\\venv\\templates', static_folder='.\\venv\\static')


@app.route('/')
def func():
    return render_template('index.html')


# @app.after_request
# def apply_caching(response):
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     return response

# If URL is entered by the user
@app.route('/test', methods=["POST"])
def func1():
    #print('In func1')
    url = request.form['url']
    no_of_lines = int(request.form['lines'])
    doc = Doc_Summ()
    doc.web_scraping(url)
    #l = ['hfef', 'fere', 'efefe', 'efe', 'wqq', 'fewfwa']
    l1 = doc.create_summary(no_of_lines)
    return jsonify(l1)

# If normal text is entered by the user
@app.route('/test1', methods=["POST"])
def func2():
    #print('In func2')
    input_text = request.form['text']
    no_of_lines = int(request.form['lines'])
    # print(input_text)
    f = open('.\\test.txt', 'w')
    f.write(input_text)
    f.flush()
    f.close()
    doc = Doc_Summ()
    doc.txt_sum()
    l1 = doc.create_summary(no_of_lines)
    # os.remove('.\\test.txt')
    return jsonify(l1)


if __name__ == "__main__":
    app.run(debug=True)
