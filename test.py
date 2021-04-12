from AI.logger import logger
import pickle

an_obj = logger()
_file = open("logger.pickle", "wb")
pickle.dump(an_obj, _file)
_file.close()
