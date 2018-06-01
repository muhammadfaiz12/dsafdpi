"""This is where we test data"""
import os
from video import get_frames
from model_utils import get_features_batch
from config.global_parameters import default_model_name
from config.resources import video_resource
from config.resources import model_resource
from glob import glob
import numpy as np
from utils import dump_pkl, load_pkl, load_moviescope_model
from collections import defaultdict
from sklearn.metrics import confusion_matrix
from keras.models import load_model

def gather_testing_data(genre, model_name=default_model_name):
    """Driver function to collect frame features for a genre"""

    testPath = os.path.join(video_resource,'test',genre)
    print (testPath) 
    videoPaths = glob(testPath+'/*')
    genreFeatures = []
    for videoPath in videoPaths:
        print (videoPath,":",)
        frames =list(get_frames(videoPath, time_step=1000))
        print (len(frames),)
        if len(frames)==0:
            print ("corrupt.")
            continue
        videoFeatures = get_features_batch(frames)
        print (videoFeatures.shape)
        genreFeatures.append(videoFeatures)

    outPath = genre+"_test_"+model_name
    dump_pkl(genreFeatures, outPath)

def test_video(videoPath):
    """Return the genre type for each video input"""
    frames = list(get_frames(videoPath, time_step=1000))
    if len(frames)==0:
        print ("Error in video")
        return
    
    print ("Processing",videoPath)
    modelName = "spatialvgg16_3g_bs48_ep150.h5"
    model = load_model(model_resource + modelName)

    videoFeatures = get_features_batch(frames)
    predictedClasses = model.predict_classes(videoFeatures)
    predictedScores = model.predict(videoFeatures)
    return predictedClasses, predictedScores
    

def ultimate_evaluate(model):
    genres = ['action','horror','romance']
    testingData = []
    testingLabels = []
    total = defaultdict.fromkeys(range(len(genres)),0)
    correct = defaultdict.fromkeys(range(len(genres)),0)
    yTrue, yPredict = [], []
    for genreIndex, genre in enumerate(genres):
#        print "Looking for pickle file: data/{0}{1}.p".format(genre, str(num_of_videos)),
        try:
            genreFeatures = load_pkl("test/"+genre+"_test_"+default_model_name)
            genreFeatures = np.array([np.array(f) for f in genreFeatures]) # numpy hack
        except Exception as e:
            print (e)
            return
        print ("OK.")
        for videoFeatures in genreFeatures:
            """to get all frames from a video -- hacky"""
            total[genreIndex]+=1
            d = defaultdict(int)
            predictedClasses = model.predict_classes(videoFeatures) #List of predictions, per-frame
            print (predictedClasses)
            for i in predictedClasses:
                d[i]+=1
            predictedGenre = max(d.items(), key=lambda x: x[1])[0]
            yPredict.append(predictedGenre)
            yTrue.append(genreIndex)
            if predictedGenre == genreIndex:
                correct[genreIndex]+=1

    print (correct, total)

    confusionMatrix = confusion_matrix(yTrue, yPredict)
    print (confusionMatrix)
    '''
    tp_action = confusionMatrix[0][0]
    tp_horror = confusionMatrix[1][1]
    tp_romance = confusionMatrix[2][2]
    fp_action = confusionMatrix[1][0] + confusionMatrix[2][0]
    fp_horror = confusionMatrix[0][1] + confusionMatrix[2][1]
    fp_romance = confusionMatrix[0][2] + confusionMatrix[1][2]
    fn_action = confusionMatrix[0][1] + confusionMatrix[0][2]
    fn_horror = confusionMatrix[1][0] + confusionMatrix[1][2]
    fn_romance = confusionMatrix[2][0] + confusionMatrix[2][1]
    tn_action = confusionMatrix[1][1] + confusionMatrix[1][2] + confusionMatrix[2][1] + confusionMatrix[2][2]
    tn_horror = confusionMatrix[0][0] + confusionMatrix[0][2] + confusionMatrix[2][0] + confusionMatrix[2][2]
    tn_romance = confusionMatrix[0][0] + confusionMatrix[0][1] + confusionMatrix[1][0] + confusionMatrix[1][1]
    prec_action = tp_action/(fp_action+tp_action)
    prec_horror = tp_horror/(fp_horror+tp_horror)
    prec_romance = tp_romance/(fp_romance+tp_romance)
    rec_action = tp_action/(fn_action+tp_action)
    rec_horror = tp_horror/(fn_horror+tp_horror)
    rec_romance = tp_romance/(fn_romance+tp_romance)
    '''
    total_acc = 0
    for i in range(len(genres)):
        tp = confusionMatrix[i][i]
        fp = 0
        for j in range(len(genres)):
            if (i != j):
                fp = fp + confusionMatrix[j][i]
        fn = 0
        for j in range(len(genres)):
            if (i != j):
                fn = fn + confusionMatrix[i][j]
        tn = 0
        for j in range(len(genres)):
            for k in range(len(genres)):
                if (i != j):
                    if (i != k):
                        tn = tn + confusionMatrix[j][k]
        prec = tp/(tp+fp)*100
        rec = tp/(tp+fn)*100
        f1 = (prec+rec)/2
        acc = (tp+tn)/(tp+fp+fn+tn)*100
        print ("Precision of "+genres[i]+" is "+str(round(prec,2))+"%\n")
        print ("Recall of "+genres[i]+" is "+str(round(rec,2))+"%\n")
        print ("F1 of "+genres[i]+" is "+str(round(f1,2))+"%\n")
        print ("Accuracy of "+genres[i]+" is "+str(round(acc,2))+"%\n")
        print("---------------")
        total_acc = total_acc + acc
    total_acc = total_acc/3
    print ("Overall Accuracy is "+str(round(total_acc,2))+"%\n")

#
if __name__=="__main__":

    from sys import argv
    model = load_moviescope_model(argv[1])
    ultimate_evaluate(model)
    """to call test_video"""
#    genres, scores = test_video(argv[1])
    #print("genresArr", genres)
#    print("jumlah per genre: ", np.bincount(genres))
#    predictedGenre = np.argmax(np.bincount(genres))                                                  
#    genreDict = {0:'action',1:'horror',2:'comedy'}                                        
#    frameSequence=' | '.join([genreDict[key] for key in genres])                                     

#    print (predictedGenre)
#    print (frameSequence)
	
#    print("\nGenre of this video is ", genreDict[predictedGenre])
