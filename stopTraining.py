from tensorflow.keras.callbacks import Callback

class stopTraining(Callback):
    def __init__(self, accuracy):
        super().__init__()
        self.accuracy = accuracy
    def on_epoch_end(self, epoch, logs={}):
        accuracy = logs.get('acc')
        if accuracy is None:
            accuracy = logs.get('accuracy')
        if accuracy > self.accuracy:
            print("Reached accuracy {}% - stopped training".
                  format(self.accuracy*100))
            self.model.stop_training = True
