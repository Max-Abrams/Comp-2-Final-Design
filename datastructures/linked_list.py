#base class taken from lab 4. Supplied to us. 

class linked_list:
    class node:
        def __init__(self,data=None,next=None):
            #Data holds info
            self.data = data
            #next is our pointer to next node
            self.next = next
    
    #Init the linked list. Head is first node
    def __init__(self):
        self.head = None

    #Add new node to begining of list by making it the head
    def insert(self, value):
        new_node = self.node(data=value, next=self.head)
        self.head = new_node

    #Method to find elements
    def lookup(self,target=None,field=None,disp=False):
        #start at head
        curr_ptr = self.head
        #stores all data that matches
        ret_val = []

    # traverse the list to find matches
        while (curr_ptr is not None):
            if hasattr(curr_ptr.data,field) and \
                getattr(curr_ptr.data,field) == target:
                    ret_val.append(curr_ptr.data)
            curr_ptr = curr_ptr.next
            
        #Display results if requested
        if disp and ret_val:
            for r in ret_val:
                r.display()
        elif disp and not ret_val:
            print(field, "=" , target, " not found")

        return ret_val
