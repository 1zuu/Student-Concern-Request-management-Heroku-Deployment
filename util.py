import json
import pickle
import pandas as pd
import numpy as np
import pandas as pd
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from variables import*

def word2vector():
    word2vec = np.load(word2vec_path, allow_pickle=True)
    word2vec = word2vec['name1'].tolist()
    return word2vec

def lemmatization(lemmatizer,sentence):
    '''
        Lemmatize texts in the terms
    '''
    lem = [lemmatizer.lemmatize(k) for k in sentence]
    lem = list(dict.fromkeys(lem))

    return [k for k in lem]

def remove_stop_words(stopwords_list,sentence):
    '''
        Remove stop words in texts in the terms
    '''
    return [k for k in sentence if k not in stopwords_list]

def preprocess_one(concern):
    '''
        Text preprocess on term text using above functions
    '''
    lemmatizer = WordNetLemmatizer()
    tokenizer = RegexpTokenizer(r'\w+')
    stopwords_list = stopwords.words('english')
    concern = concern.lower()
    remove_punc = tokenizer.tokenize(concern) # Remove puntuations
    remove_num = [i for i in remove_punc if len(i)>0] # Remove empty strings
    lemmatized = lemmatization(lemmatizer,remove_num) # Word Lemmatization
    remove_stop = remove_stop_words(stopwords_list,lemmatized) # remove stop words
    updated_concern = ' '.join(remove_stop)
    return updated_concern

def preprocessed_data(concerns):
    '''
        Preprocess entire terms
    '''
    updated_concerns = []
    if isinstance(concerns, np.ndarray) or isinstance(concerns, list):
        for concern in concerns:
            updated_concern = preprocess_one(concern)
            updated_concerns.append(updated_concern)
    elif isinstance(concerns, np.str_)  or isinstance(concerns, str):
        updated_concerns = [preprocess_one(concerns)]

    return np.array(updated_concerns)

def derive_vocabulary():
    file_ = open(vocabulary_path,'rb')
    word2index = pickle.load(file_)
    file_.close()
    
    return word2index

def sequence_and_padding_concerns(processed_concerns, word2index):
    seq_concerns = []
    for concern in processed_concerns:
        seq_concern = []
        concern = concern.split(' ')
        for word in concern:
            word = word.strip().lower()
            if word in word2index: 
                seq_concern.append(word2index[word])
            else:
                seq_concern.append(word2index[oov_tok])
        seq_concerns.append(seq_concern)

    pad_concerns = pad_sequences(
                            seq_concerns, 
                            maxlen=max_length, 
                            truncating=trunc_type,
                            padding=padding
                            )
    pad_concerns = np.array(pad_concerns)
    return pad_concerns

def word_embeddings(pad_concerns, word2index):
    N = pad_concerns.shape[0]
    embedding_concerns = np.zeros((N, max_length, embedding_dim))

    index2word = {v:k for k,v in word2index.items()}

    word2vec = word2vector()
    for i, concern in enumerate(pad_concerns):
        for j, index in enumerate(concern):
            word = index2word[index]
            if (word not in word2vec) and (word != pad_token):
                embedding_concerns[i,j,:] = word2vec['unk']
            else:
                if word != pad_token: 
                    embedding_concerns[i,j,:] = word2vec[word]
    return embedding_concerns

def connect_mongo():
    client = MongoClient(db_url)
    db = client[database]
    return db

def create_database():

    db = connect_mongo()
    if db_collection not in db.list_collection_names():
        coll = db[db_collection]
        data = pd.read_csv(data_path)
        data = data.dropna(axis=0)
        payload = json.loads(data.to_json(orient='records'))
        coll.remove()
        coll.insert(payload)
        print('Database created')
    else:
        print('Database already exists')

def read_mongo():
    create_database()
    db = connect_mongo()
    cursor = db[db_collection].find({})
    df =  pd.DataFrame(list(cursor))
    del df['_id']

    return df

def get_data():
    return derive_vocabulary()