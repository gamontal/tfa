#!flask/bin/python3

import os

from flask import Flask, jsonify, make_response, request, redirect, url_for, send_from_directory
from tfa_nltk import analyzer

app = Flask(__name__)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

@app.route('/tfa', methods=['POST'])
def get_results():

    inputfile = request.files['inputfile']
    fileContent = inputfile.stream.read().decode('utf-8')

    options = {
        'allow_digits': request.form['allow_digits'],
        'ignore_list': request.form['ignore_list'],
        'content': fileContent,
        'max_n_word': int(request.form['max_n_word']),
        'top_n': int(request.form['top_n_grams'])
    }

    return jsonify(analyzer(options)), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({ 'error': 'Not Found' }), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({ 'error': 'Bad Request'}), 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) # start flask server on port 8080
