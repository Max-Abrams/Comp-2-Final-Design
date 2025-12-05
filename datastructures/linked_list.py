#base class taken from lab 4


class linked_list:
    class node:
        def __init__(self,data=None,next=None):
            self.data = data
            self.next = next
    
    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = self.node(data=value, next=self.head)
        self.head = new_node

    def lookup(self,target=None,field=None,disp=False):
        curr_ptr = self.head
        ret_val = []

        while (curr_ptr is not None):
            if hasattr(curr_ptr.data,field) and \
                getattr(curr_ptr.data,field) == target:
                    ret_val.append(curr_ptr.data)
            curr_ptr = curr_ptr.next

        if disp and ret_val:
            for r in ret_val:
                r.display()
        elif disp and not ret_val:
            print(field, "=" , target, " not found")

        return ret_val
