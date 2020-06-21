from tensorflow.keras.callbacks import Callback

class StopTraining(Callback):
    def __init__(self, accuracy):
        super().__init__()
        self.accuracy = accuracy
    def on_epoch_end(self, epoch, logs={}):
        accuracy = logs.get('acc')
        if accuracy is None:
            accuracy = logs.get('accuracy')
        if accuracy > self.accuracy:
            print("\nReached accuracy {}% - stopped training".
                  format(accuracy*100))
            self.model.stop_training = True
