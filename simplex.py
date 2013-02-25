# Simplex class

class Simplex:

    def __init__(self):
        self._points = []

    def add(self, item):
        if item in self._points:
            return False
        else:
            self._points.append(item)

    def remove(self, item):
        if item in self._points:        
            self._points.remove(item)
        else:
            return False

    def get(self, index):
        ''' Returns the point at position 'index' from the end '''
        return self._points[-index]

    def get_points(self):
        return self._points
    
