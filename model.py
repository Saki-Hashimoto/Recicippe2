import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D,Input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

os.environ['KMP_DUPLICATE_LIB_OK']='True'

n_categories=21
batch_size=32

train_dir='./images/train'
validation_dir='./images/validation'
test_dir='./images/test'
file_name='./recicippemodel/recicippemodel'

ClassNames=['bacon', 'broccoli', 'carott', 'chicken', 'daikon', 'eggplant', 
    'enoki', 'eringi', 'greenonion', 'greenpepper', 'hikiniku', 'maitake', 'moyashi',
    'onion', 'pork', 'pumpkin', 'saba', 'salmon', 'simeji', 'tofu', 'tomato']

base_model=VGG16(weights='imagenet',
                 include_top=False,
                 input_tensor=Input(shape=(224,224,3)))

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x)
prediction=Dense(n_categories,activation='softmax')(x)
model=Model(inputs=base_model.input,outputs=prediction)

for layer in base_model.layers[:15]:
    layer.trainable=False

model.compile(optimizer=SGD(lr=0.0001,momentum=0.9),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

json_string=model.to_json()
json_string+='##########' + str(ClassNames)
open(file_name + 'model.json',"w").write(json_string)

train_datagen=ImageDataGenerator(
    rescale=1.0/255, rotation_range=15) 

validation_datagen=ImageDataGenerator(rescale=1.0/255)

train_generator=train_datagen.flow_from_directory(
    train_dir,   
    target_size=(224,224),    
    batch_size=batch_size,    
    class_mode='categorical',    
    shuffle=True   
)

validation_generator=validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
    )

MODEL_DIR = "./temp"
if not os.path.exists(MODEL_DIR):  
    os.makedirs(MODEL_DIR)

cp_callback = ModelCheckpoint(
    filepath=os.path.join(MODEL_DIR, "model-{epoch:02d}.h5"),
    save_weights_only=True, 
    verbose=1,  
    period=1 
    )

hist=model.fit_generator(train_generator,
                         epochs=60,
                         verbose=1,
                         validation_data=validation_generator,
                         callbacks=[cp_callback,
                                    CSVLogger(file_name+'.csv'),
                                    EarlyStopping(monitor='val_loss', patience=2, min_delta=0.0,  verbose=1)]                        
                         )

score=model.evaluate_generator(train_generator)
print('\n train loss:',score[0])
print('\n train_acc:',score[1])

score=model.evaluate_generator(validation_generator)
print('\n validation loss:',score[0])
print('\n validation_acc:',score[1])
model.save(file_name+'weight.h5')

test_datagen=ImageDataGenerator(rescale=1.0/255)
test_generator=test_datagen.flow_from_directory(
    test_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

score=model.evaluate_generator(test_generator)
print('\n test loss:',score[0])
print('\n test_acc:',score[1])