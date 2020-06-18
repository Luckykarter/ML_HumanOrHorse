import os
import random
import zipfile

# Helper functions for getting
def getRandomItems(lst, number=1):
    return [random.choice(lst) for _ in range(number)]

def unZipAll(dir):
    for path in os.listdir(dir):
        s_path = os.path.splitext(path)
        if s_path[1].lower() == '.zip':
            local_zip = os.path.join(dir, path)
            zip_ref = zipfile.ZipFile(local_zip, 'r')
            new_dir = os.path.join(dir, s_path[0])
            zip_ref.extractall(new_dir)
            zip_ref.close()

# load images of humans and horses from ZIP-file
def getData(unzipped = False):
    base_dir = 'resources'
    name_dir = 'horse-or-human'
    if not unzipped:
        unZipAll(base_dir)

    train_dir = os.path.join(base_dir, name_dir)
    validation_dir = os.path.join(base_dir, 'validation-' + name_dir)

    horse_dir_train = os.path.join(train_dir, 'horses')
    human_dir_train = os.path.join(train_dir, 'humans')

    horse_dir_validation = os.path.join(validation_dir, 'horses')
    human_dir_validation = os.path.join(validation_dir, 'humans')

    return (horse_dir_train, human_dir_train,
            horse_dir_validation, human_dir_validation)

# import tkinter as tk
# from tkinter import filedialog
import easygui

def getUserFile():
# this does not work well - hangs the script
#     root = tk.Tk()
#     root.withdraw()
#     filename = filedialog.askopenfilename()
#     return filename

# easygui works better

     return easygui.fileopenbox(
          msg="Horse or human",
          title="Choose image(s)",
          multiple=True
     )

