word2vec_path = 'data/glove_vectors.npz'
vocabulary_path = 'data/vocabulary.pickle'
n_neighbour_weights = 'data/nearest_neighbour.pickle'
encoder_dict_path = 'data/label_encoder.pickle'

data_feature_path = 'data/features.npz'

model_weights = 'data/model_weights.h5'
model_converter = 'data/model_converter.tflite'

fmodel_weights = 'data/feature_model_weights.h5'
fmodel_converter = 'data/feature_model_converter.tflite'

data_path = 'data/Student Concerns_6.csv'

seed = 42
database = 'SCRMS'
db_collection = 'concerns'
live_collection = 'live_concerns'
db_url = "mongodb+srv://admin:admin@cluster0.lx3sd.mongodb.net/test"
model_url = "https://student-concern-request-manage.herokuapp.com/concern"

heroku_url = '0.0.0.0'
heroku_port = 5000
vocab_size = 1000
max_length = 30
embedding_dim = 200
trunc_type = 'post'
padding = 'post'
oov_tok = "<oov>"
pad_token = '<pad>'
num_epochs = 20
batch_size = 32
size_lstm1  = 256
size_lstm2  = 128
dense1 = 256
dense2 = 128
dense3 = 64
keep_prob = 0.4

test_size = 0.005
val_size = 0.15
n_neighbors = 1