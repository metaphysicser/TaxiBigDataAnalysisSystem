import pickle

def saveObj(obj, path):

    '''Save the object as pkl format.

    :param obj: The object to save.
    :type obj: FileStorage
    :param path: The path of the file to save
    :type path: str
    '''

    with open(path + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def loadObj(path):

    '''Load the object from pkl format.

    :param path: The path of the file to load.
    :type path: str
    :returns: The object loaded.
    :rtype: object
    '''

    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)