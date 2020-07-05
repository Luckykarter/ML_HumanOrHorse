from getdata import get_data, get_user_file
import os
from printimages import print_images, print_intermediate_representations, show_dataset_examples
import tensorflow as tf
import numpy as np
from numba import jit, cuda
from stoptraining import StopTraining
from keras_preprocessing import image

#test br
SHOW_DATASET_EXAMPLE = False
horse_dir, human_dir, horse_dir_validation, human_dir_validation = get_data()
work_dir = os.path.dirname(horse_dir)
work_dir_validation = os.path.dirname(horse_dir_validation)
print('total training horse images:', len(os.listdir(horse_dir)))
print('total training human images:', len(os.listdir(human_dir)))
print('total validation horse images:', len(os.listdir(horse_dir_validation)))
print('total validation human images:', len(os.listdir(human_dir_validation)))

# display dataset examples
show_dataset_examples(SHOW_DATASET_EXAMPLE)

model = tf.keras.models.Sequential([
    # 1
    tf.keras.layers.Conv2D(16, (3, 3), activation=tf.nn.relu, input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # 2
    tf.keras.layers.Conv2D(32, (3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D(2, 2),
    # 3
    tf.keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D(2, 2),
    # 4 and 5 are tremoved because size of pictures decreased
    # tf.keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu),
    # tf.keras.layers.MaxPooling2D(2, 2),
    # 5
   # tf.keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu),
   # tf.keras.layers.MaxPooling2D(2, 2),
    # flatten the image
    tf.keras.layers.Flatten(),
    # 512 connected neurons
    tf.keras.layers.Dense(512, activation=tf.nn.relu),
    # 0 - horses, 1 - humans
    tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)

])

model.summary()
model.compile(loss=tf.keras.losses.binary_crossentropy,
              optimizer=tf.keras.optimizers.RMSprop(lr=0.001),
              metrics=['accuracy'])

# all images will be rescaled by 1.0 / 255
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
validation_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)

# flow training images in batches of 128
train_generator = train_datagen.flow_from_directory(
    work_dir,               # directory with all images
    target_size=(150, 150), # all images will be resized to ...
    batch_size= 128,
    class_mode='binary'     # binary labels
)
validation_generator = validation_datagen.flow_from_directory(
    work_dir_validation,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'
)

# training:
def train():
    return model.fit(train_generator,
                     steps_per_epoch=8,
                     epochs=15,
                     callbacks=[StopTraining(accuracy=0.98)],
                     verbose=1,
                     validation_data=validation_generator,
                     validation_steps=8)

@jit(target='cuda')
def train_with_gpu():
    print('Start training using GPU')
    train()

try:
    train_with_gpu()
except:
    print('Start training using CPU')
    train()

#printIntermediateRepresentations(show_images, model)

print("Recognize user images: ")

img_paths = get_user_file()
while img_paths:
    labels = list()
    for file in img_paths:
        img = image.load_img(
            file, target_size=(150, 150)
        )
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = model.predict(images, batch_size=10)
        # print(classes[0])
        if classes[0] > 0.5:
            # print(file + '\nis a human')
            labels.append("Human")
        else:
            # print(file + '\nis a horse')
            labels.append("Horse")
    print_images(img_paths, "Neural network guesses", labels)
    img_paths = get_user_file()

