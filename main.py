from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
img_size = 200
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
@cross_origin()
def index():
    # Initiate returned structure
    data = {
        "success": False
    }
    if request.method == "POST":
        if('audio_file' in request.files):
            print('Got it! it works')
    return jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
    "please wait until server has fully started"))
    app.run(host='localhost', port=8000)