import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import pickle
import numpy as np
import pandas as pd

from dnn import SCRM_Model
from variables import*
from util import*

class SCRM_Inference(object):
    def __init__(self):
        self.scrm = SCRM_Model()
        self.scrm.run()
        self.vocab = self.scrm.word2index

    def data_to_features(self):
        data = np.load(data_feature_path, allow_pickle=True)
        features = data['name1']
        solutions = data['name2']
        student_id = data['name3']

        self.features = features
        self.solutions = solutions
        self.student_id = student_id

    def nearest_neighbor_model(self):
        with open(n_neighbour_weights, 'rb') as file:
            self.neighbor = pickle.load(file)

    def process_inf_data(self, concern):
        preprocessed_concern = preprocess_one(concern)
        pad_concerns = sequence_and_padding_concerns([preprocessed_concern], self.vocab)
        embedding_concern = word_embeddings(pad_concerns, self.vocab)
        embedding_concern = embedding_concern.reshape(max_length, embedding_dim)
        return embedding_concern

    def predict_one(self, concern):
        embedding_concern = self.process_inf_data(concern)
        feature_vector = self.scrm.runTFliteInference(embedding_concern, False).squeeze()
        categories = self.scrm.runTFliteInference(embedding_concern).squeeze()
        return feature_vector, categories

    @staticmethod
    def create_df_from_categories(categories):
        categories = categories.reshape(1, -1)
        df_pred = pd.DataFrame(
                        data = categories,
                        columns=['Department', 'Sub_Section', 'Concern_Type']
                        )
        return df_pred

    def apply_inverse_transform(self, categories):
        df_pred = SCRM_Inference.create_df_from_categories(categories)
        with open(encoder_dict_path, 'rb') as handle:
            encoder_dict = pickle.load(handle)
        df_pred = df_pred.apply(lambda x: encoder_dict[x.name].inverse_transform(x))
        output = df_pred.values.squeeze().tolist()
        return output

    def predict_best_solution(self, concern):
        feature_vector, categories = self.predict_one(concern)

        neighbor = self.neighbor.kneighbors([feature_vector], 1)[1]
        neighbor = neighbor.squeeze()

        categories = self.apply_inverse_transform(categories)
        return self.solutions[neighbor], categories

    def make_response(self, request):
        concern = request['concern']
        solution, categories = self.predict_best_solution(concern)

        response = {
            'concern':concern,
            'solution': solution,
            'Department' : categories[0],
            'Sub_Section' : categories[1],
            'Concern_Type' : categories[2]
                }

        return response