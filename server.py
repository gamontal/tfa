#!flask/bin/python

import os

from flask import Flask, jsonify, make_response, request, redirect, url_for, send_from_directory
from tfa import *

server = Flask(__name__)

@server.route('/')
def root():
    return server.send_static_file('index.html')

@server.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return server.send_static_file(path)

@server.route('/tfa', methods=['POST'])
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

    results = wfa(options).calc();

    return jsonify(results), 200

@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({ 'error': 'Not Found' }), 404)

@server.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({ 'error': 'Bad Request'}), 400)

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080) # start flask server on port 8080
