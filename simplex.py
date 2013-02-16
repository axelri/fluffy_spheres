# Simplex class

class Simplex:

    def __init__(self):
        self._points = []

    def add(self, item):
        self._points.append(item)

    def remove(self, item):
        #Check if the item is there first?
        self._points.remove(item)

    def get(self, index):
        ''' Returns the point at position 'index' from the end '''
        return self._points[-index]

    def get_points(self):
        return self._points
    
