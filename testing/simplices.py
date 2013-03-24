# Simplex class

class Simplex:

    def __init__(self):
        self._points = []

    def add(self, item):
##        # TODO: Should be something like this in order 
##        # to not try add points that already are in the simplex. 
##        # Must edit GJK to handle this scenario to to add this.
##        if item in self._points:
##            return False
##        else:
##            self._points.append(item)
        self._points.append(item)

    def remove(self, index):
##        # TODO: Should be something like this in order 
##        # to not try to remove points that doesn't exist. 
##        # Must edit GJK to handle this scenario to to add this.
##        if item in self._points:        
##            self._points.remove(item)
##        else:
##            return False
        #self._points.remove(item)
        del self._points[-index]

    def get(self, index):
        ''' Returns the point in the simplex at position 'index' from the end '''
        return self._points[-index][0]

    def get_all(self, index):
        ''' Returns the point in the simplex at position 'index' from the end,
            aswell as the corresponding points in the two shapes. '''
        return self._points[-index]

    def get_points(self):
        return self._points

    def get_all_points(self, index):
        out = []
        for i in range(len(self._points)):
            out.append(self._points[-i][index])
        return out
    
