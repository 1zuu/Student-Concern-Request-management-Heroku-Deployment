import warnings
import numpy as np
import tensorflow as tf

from variables import *
from util import*

np.random.seed(seed)
warnings.simplefilter("ignore", DeprecationWarning)

class SCRM_Model():
    def __init__(self):
        word2index = get_data()
        self.word2index = word2index

    def TFinterpreter(self, converter_path):
        # Load the TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(model_path=converter_path)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        return interpreter, input_details, output_details

    def TFliteInference(self, description, interpreter, input_details, output_details, train):
        input_shape = input_details[0]['shape']
        input_data = np.expand_dims(description, axis=0).astype(np.float32)
        assert np.array_equal(input_shape, input_data.shape), "required shape : {} doesn't match with provided shape : {}".format(input_shape, input_data.shape)

        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        if train:
            concern_type = interpreter.get_tensor(output_details[0]['index']) #Concern_Type
            department = interpreter.get_tensor(output_details[1]['index']) #Department
            subsection = interpreter.get_tensor(output_details[2]['index']) #Sub_Section

            concern_type = concern_type.squeeze().argmax(axis=-1)
            department = department.squeeze().argmax(axis=-1)
            subsection = subsection.squeeze().argmax(axis=-1)
            
            output_data = np.array([department, subsection, concern_type])

        else:
            output_data = interpreter.get_tensor(output_details[0]['index'])
            
        return output_data
        
    def runTFinterpreter(self):
        interpreter, input_details, output_details = self.TFinterpreter(model_converter)
        self.model_interpreter = interpreter
        self.model_input_details = input_details
        self.model_output_details = output_details

        interpreter, input_details, output_details = self.TFinterpreter(fmodel_converter)
        self.fmodel_interpreter = interpreter
        self.fmodel_input_details = input_details
        self.fmodel_output_details = output_details

    def runTFliteInference(self, description, train=True):
        if train:
            interpreter = self.model_interpreter
            input_details = self.model_input_details
            output_details = self.model_output_details
        else:
            interpreter = self.fmodel_interpreter
            input_details = self.fmodel_input_details
            output_details = self.fmodel_output_details
        return self.TFliteInference(description, interpreter, input_details, output_details, train)

    def run(self):
        self.runTFinterpreter()