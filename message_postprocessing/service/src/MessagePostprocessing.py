

from message_postprocessing.service.src.PhraseCleaner import PhraseCleaner


class MessagePostprocessing():
    def __init__(self, confidence = 0.5):
        self.__phraseCleaner = PhraseCleaner()
    
    def cleanMessage(self, options):
        pass