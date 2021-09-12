# from flask import Flask, request, jsonify
# from inference import SCRM_Inference

# from variables import*

# app = Flask(__name__)

# model = SCRM_Inference()
# model.data_to_features()
# model.nearest_neighbor_model()

# @app.route("/concern", methods=['GET','POST'])
# def predictions():
#     try:
#         concerns = request.get_json(force=True)
#         response = model.make_response(concerns)
#         return jsonify(response)

#     except Exception as e:
#         return jsonify({
#             "error": str(e)
#         })

# if __name__ == '__main__':
#     app.run(debug=True, host=heroku_url, port=heroku_port, threaded=False, use_reloader=False)


import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, Response, request
from inference import SCRM_Inference
from variables import*

app = Flask(__name__)

model = SCRM_Inference()
model.data_to_features()
model.nearest_neighbor_model()

try:
    client = MongoClient(db_url)
    db = client[database]
    client.server_info()

except Exception as e:
    print(e)

@app.route("/insert", methods=["POST"])
def insert():
    try:
        concerns_data = request.get_json()
        cursor = db[live_collection].find()
        data = list(cursor)
        if len(data) == 0:
           concerns_data['student_id'] = str(1)
        else:
           concerns_data['student_id'] = str(int(data[-1]['student_id']) + 1)
        
        if list(concerns_data.keys()) == ['student_id', 'Gender', 'Age Group' , 'Year']:

            dbResponse = db[live_collection].insert_one(concerns_data)
            return Response(
                        response=json.dumps({
                            "status": "success",
                            "id" : str(dbResponse.inserted_id)
                                }), 
                        status=200, 
                        mimetype="application/json"
                        )
        else:
            return Response(
                        response=json.dumps({
                            "status": "success",
                            "id" : "Invalid Response. Please Input Gender, Age Group & Year"
                                }), 
                        status=200, 
                        mimetype="application/json"
                        )       

    except Exception as e:
        print(e)

@app.route("/get", methods=["GET"])
def get():
    try:
        cursor = db[live_collection].find()
        data = list(cursor)
        for param in data:
            param["_id"] = str(param["_id"])
        return Response(
                    response=json.dumps(data), 
                    status=500, 
                    mimetype="application/json"
                    )


    except Exception as e:
        print(e)
        return Response(
                    response=json.dumps({
                        "status": "unsuccessful"
                            }), 
                    status=500, 
                    mimetype="application/json"
                    )

@app.route("/update", methods=["PATCH"])
def update():
    try:
        data = list(db[live_collection].find())[-1]
        obj_id = str(data["_id"])

        concern_data = request.get_json()
        response = model.make_response(concern_data)
        dbResponse = db[live_collection].update_one(
                                        {"_id": ObjectId(obj_id)}, 
                                        {"$set": response}
                                             )
        return Response(
                    response=json.dumps({
                        "status": response
                            }), 
                    status=200, 
                    mimetype="application/json"
                    )
    except Exception as e:
        print(e)
        return Response(
                    response=json.dumps({
                        "status": "can not update user {}".format(id)
                            }), 
                    status=500, 
                    mimetype="application/json"
                    )

if __name__ == '__main__':
    app.run(debug=True, host=heroku_url, port=heroku_port)