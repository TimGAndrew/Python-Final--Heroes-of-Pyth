import winsound
import threading
import queue


class Sound():
    def __init__(self, path):
        self.path = path

    def play(self):
        threading.Thread(target=winsound.PlaySound(self.path, winsound.SND_FILENAME))
