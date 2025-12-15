#Creating a class to represent space group information for use later
class SpaceGroup:
    def __init__(self, data_row):
        #Pulling the attributes we need
        self._symbol = data_row["spg_symbol"]
        self._number = data_row["spg_number"]
        self._crystal_system = data_row["crys"]
    
    #We added protections after testing
    #So now we need these decorators to avoid errors when accessing missing data
    @property
    def symbol(self):
        return self._symbol
    
    @property
    def number(self):
        return self._number
    
    @property
    def crystal_system(self):
        return self._crystal_system

    #print/display function that we can call each time 
    def display(self):
        return f"[SpaceGroup: {self._symbol} (#{self._number}), System: {self._crystal_system}]"
