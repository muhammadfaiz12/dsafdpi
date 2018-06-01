from config.global_parameters import default_model_name
from utils import load_pkl
from keras.optimizers import Adam, RMSprop
import numpy as np
from model_utils import spatial_model
from model_utils import lstm_model
from model_utils import mlp_model



def train_classifier(genres=['comedy', 'horror', 'action'],model_train='spatial', model_name=default_model_name, epoch=100):
    
    """Gather data for selected genres"""
    trainingData = []
    trainingLabels = []
#    num_of_random_frames = 75
    num_of_classes = len(genres)
    print("Number of classes:",num_of_classes)
    for genreIndex, genre in enumerate(genres):
#        print "Looking for pickle file: data/{0}{1}.p".format(genre, str(num_of_videos)),
        try:
            print("train/"+genre+"_train_"+model_name)
            genreFeatures = load_pkl("train/"+genre+"_train_"+model_name)
            genreFeatures = np.array([np.array(f) for f in genreFeatures]) # numpy hack
        except Exception as e:
            print(e)
            return
        print("OK.")
        for videoFeatures in genreFeatures:
            """to get all frames from a video -- hacky"""
            randomIndices = range(len(videoFeatures))
            selectedFeatures = np.array(videoFeatures[randomIndices])
            for feature in selectedFeatures:
                trainingData.append(feature)
                trainingLabels.append([genreIndex])
    trainingData = np.array(trainingData)
    trainingLabels = np.array(trainingLabels)
    print(trainingData.shape) 
    print(trainingLabels.shape)
#    trainingLabels = to_categorical(trainingLabels, num_of_classes)
    print(trainingLabels)
#    trainingLabels = trainingLabels.reshape((-1,num_of_classes))

    """Initialize the mode"""
    if(model_train == 'mlp'):
        model = mlp_model(num_of_classes, trainingData.shape[1])
        model.compile(optimizer='adadelta', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    elif (model_train == 'lstm'):
        num_of_frames = 9
        num_of_samples = len(trainingLabels)
        trainingDataTensor = np.zeros((num_of_samples, num_of_frames, trainingData.shape[1]))
        print (len(trainingData))
        for sampleIndex in range(num_of_samples):
            for vectorIndex in range(num_of_frames):
                try:
                    trainingDataTensor[sampleIndex][vectorIndex] = trainingData[sampleIndex][vectorIndex]
                except Exception as e:
                    print (e)
                    continue
        print (trainingDataTensor.shape)
        trainingData=trainingDataTensor
        model = lstm_model(num_of_classes, input_dim=trainingData.shape[2])
        model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    elif (model_train == 'spatial'):
        model = spatial_model(num_of_classes, trainingData.shape[1])
        model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])        

   
    """Start training"""
    batch_size = 32
    #b_epoch = 100 

    model.fit(trainingData, trainingLabels, batch_size=batch_size, epochs=int(epoch))#, callbacks=[remote])
    modelOutPath ='data/models/'+model_train+'_'+model_name+'_'+str(num_of_classes)+"g_bs"+str(batch_size)+"_ep"+str(epoch)+".h5"
    model.save(modelOutPath)
    print("Model saved at",modelOutPath)
 

if __name__=="__main__":
    from sys import argv
    nama_model_train = argv[1]
    nama_extract = argv[2]
    epochnum = argv[3]
    #train_classifier(genres=['action','drama','fantasy','horror','romance'])
    #train_classifier(genres=['action','horror','romance'], model_train=nama_model_train)
    train_classifier(genres=['action','horror','romance'], model_train=nama_model_train, model_name=nama_extract, epoch=epochnum)
