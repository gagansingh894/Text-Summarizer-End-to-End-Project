from flask import Flask, request
from flask.json import jsonify
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'Deploy'))
dir_path = os.path.dirname(os.path.realpath(__file__))

import textsummarizer

app = Flask(__name__, root_path=dir_path)
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Service Up and Running'})

@app.route('/summarize', methods=['POST'])
def summary():
    
    res = None
    data = request.get_json()
    print(data)
    
    if (list(data.keys()))[0] == 'value':
        summarizer = textsummarizer.Summarizer(data['value'])
        res = summarizer.summarize()
    
    else:
        res = 'Wrong Key'

    return jsonify({'result': res})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
