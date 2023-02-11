import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import load_img, img_to_array


hw={'height':224, 'width':224}

def TestProcess(imgname):
    modelname_text = open("./recicippemodel/recicippemodel.json").read()
    json_strings = modelname_text.split('##########')
    textlist = json_strings[1].replace("[", "").replace("]", "").replace("\'", "").split()
    model = model_from_json(json_strings[0]) 
    model.load_weights("./recicippemodel/model-34.h5")
    img = load_img(imgname, target_size=(hw['height'], hw['width']))
    TEST = img_to_array(img)/255
    pred = model.predict(np.array([TEST]), batch_size=1, verbose=0)
    
    name = textlist[np.argmax(pred)].replace(",", "")
    return name