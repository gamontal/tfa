#!flask/bin/python

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
    content = inputfile.stream.read().decode("utf-8")

    options = {
        'allow_digits': False,
        'ignore_list': [],
        'content': content,
        'max_n_word': 3,
        'top_n': 20
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
    server.run(debug=True)
