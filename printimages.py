import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import sqrt, ceil
import numpy as np
import random
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import tensorflow as tf
from getdata import get_data, get_random_items
import os

def print_images(images, title, img_titles = None):
    ncols = ceil(sqrt(len(images)))
    nrows = ceil(len(images) / ncols)

    fig = plt.gcf()
    fig.canvas.set_window_title(title)
    # fig.set_size_inches(ncols * 4, nrows * 4)

    for i, img_path in enumerate(images):
        # set up subplot
        sp = plt.subplot(nrows, ncols, i + 1 )
        if img_titles:
            sp.set_title(img_titles[i])

        sp.axis('Off')

        img = mpimg.imread(img_path)
        plt.imshow(img)
    plt.show()

def print_intermediate_representations(images, model):
    successive_outputs = [layer.output for layer in model.layers[1:]]
    visualization_model = tf.keras.models.Model(
        inputs=model.input,
        outputs=successive_outputs
    )
    img_path = random.choice(images)

    img = load_img(img_path, target_size=(300, 300))
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
    x /= 255

    successive_feature_maps = visualization_model.predict(x)
    layer_names = [layer.name for layer in model.layers]

    for layer_name, feature_map in zip(layer_names, successive_feature_maps):
        # do this for conv/maxpool layers but not the fully-connected layers
        if len(feature_map.shape) == 4:
            n_features = feature_map.shape[-1] # number of features in feature map
            #the feature map has shape (1, size, size, n_features)

            size = feature_map.shape[1]
            display_grid = np.zeros((size, size * n_features))
            for i in range(n_features):
                x = feature_map[0, :, :, i]
                x -= x.mean()
                x *= 64
                x += 128
                x = np.clip(x, 0, 255).astype('uint8')
                display_grid[:, i*size:(i+1) * size] = x
            scale = 20.0 / n_features
            plt.figure(figsize=(scale * n_features, scale))
            plt.title(layer_name)
            plt.grid(False)
            plt.imshow(display_grid)
    plt.show()

def show_dataset_examples(show: bool, number_of_images = 10):
    if not show:
        return
    horse_dir, human_dir, horse_dir_validation, human_dir_validation = get_data(unzipped=True)

    horse_names = os.listdir(horse_dir)
    human_names = os.listdir(human_dir)

    horse_pics = [os.path.join(horse_dir, name)
                  for name in get_random_items(horse_names, number_of_images)]
    human_pics = [os.path.join(human_dir, name)
                  for name in get_random_items(human_names, number_of_images)]

    show_images = horse_pics + human_pics

    print_images(show_images, "Random Training Images")

    # display some validation images
    horse_names = os.listdir(horse_dir_validation)
    human_names = os.listdir(human_dir_validation)
    horse_pics = [os.path.join(horse_dir_validation, name)
                  for name in get_random_items(horse_names, number_of_images)]

    human_pics = [os.path.join(human_dir_validation, name)
                  for name in get_random_items(human_names, number_of_images)]

    show_images = horse_pics + human_pics

    print_images(show_images, "Random Validation Images")

