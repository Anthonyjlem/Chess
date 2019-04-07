class minHeap:

    def __init__(self):
        """
        Initialize storage for the minHeap.
        """
        self.children = []
    
    def add_child(self, move, value):
        """
        Takes in move as a two-list where the first value is the starting
        position and the second value is the position to move to value, and
        value, which is a float value of the board state.
        Adds the move and value to the minHeap according by value.
        Returns True upon successful completion.
        """
        if self.children == []:
            self.children = [[move, value]]
        else:
            #Add and reheapify
            index = len(self.children)
            self.children += [[move, value]]
            if index%2 == 0:
                parent = index/2-1
            else:
                parent = int(index/2-0.5)
            while value < ((self.children)[int(parent)])[1]:
                temp = (self.children)[int(parent)]
                (self.children)[int(parent)] = (self.children)[int(index)]
                (self.children)[int(index)] = temp
                if parent == 0:
                    return True
                index = parent
                if index%2 == 0:
                    parent = index/2-1
                else:
                    parent = int(index/2-0.5)
        return True

    def get_min(self):
        """
        Returns the a two-list of the move followed by value that is the
        minimum value of the heap (the move that results in the lowest board
        state value.
        """
        if self.children == []:
            return [[], 400]
        else:
            return self.children[0]


class maxHeap:

    def __init__(self):
        """
        Initialize storage for the maxHeap.
        """
        self.children = []
    
    def add_child(self, move, value):
        """
        Takes in move as a two-list where the first value is the starting
        position and the second value is the position to move to value, and
        value, which is a float value of the board state.
        Adds the move and value to the maxHeap according by value.
        Returns True upon successful completion.
        """
        if self.children == []:
            self.children = [[move, value]]
        else:
            #Add and reheapify
            index = len(self.children)
            self.children += [[move, value]]
            if index%2 == 0:
                parent = index/2-1
            else:
                parent = int(index/2-0.5)
            while value > ((self.children)[int(parent)])[1]:
                temp = (self.children)[int(parent)]
                (self.children)[int(parent)] = (self.children)[int(index)]
                (self.children)[int(index)] = temp
                if parent == 0:
                    return True
                index = parent
                if index%2 == 0:
                    parent = index/2-1
                else:
                    parent = int(index/2-0.5)
        return True

    def get_max(self):
        """
        Returns the a two-list of the move followed by value that is the
        maximum value of the heap (the move that results in the greatest board
        state value.
        """
        if self.children == []:
            return [[], -400]
        else:
            return self.children[0]
