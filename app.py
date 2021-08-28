from flask import Flask, request, jsonify
from inference import SCRM_Inference

from variables import*

app = Flask(__name__)

model = SCRM_Inference()
model.data_to_features()
model.nearest_neighbor_model()

@app.route("/concern", methods=['GET','POST'])
def predictions():
    try:
        concerns = request.get_json(force=True)
        response = model.make_response(concerns)
        return jsonify(response)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(debug=True, host=heroku_url, port=heroku_port, threaded=False, use_reloader=False)