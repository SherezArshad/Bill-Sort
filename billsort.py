


import re, os 


class Node:

    def __init__(self, datum = None):
        self.datum = datum
        self.children = []

    def get_child(self, datum=None):
        for child in self.children:
            if child.datum == datum:
                return child


    def __eq__(self, other):
        if len(self.children) != len(other.children):
            return False
        if not self.children:
            return True
        equal = True
        for child in self.children:
            other_child = other.get_child(child.datum)
            if not other_child:
                return False
            equal = equal and child == other_child
        return equal



class WatchListLinked:

    def __init__(self, fname = ''):
        self.root = Node()
        self.root.children = [Node('5'), Node('10'), Node('20'), Node('50'), Node('100')]

        if fname != '':
            for line in open(fname):
                line = line.split()
                self.insert(line[0],line[1])


        self.validator = re.compile(r'^[A-M][A-L](?!0{8})\d{8}[A-NP-Y]$')

        
    def insert(self, serial_number, denom):
        current =  self.root.get_child(denom)
        for ch in serial_number:
            next = current.get_child(ch)
            if not next:
                next = Node(ch)
                current.children.append(next)
            current = next
        if not current.get_child():
            current.children.append(Node())



    def search(self, serial_number, denom):
        current = self.root.get_child(denom)
        for ch in serial_number:
            next =  current.get_child(ch)
            if not next:
                return False
            current = next
        if not current.get_child():
            return False
        return True


class WatchListDict:

    def __init__(self, fname = ''):
        self.root = {'5':{}, '10':{}, '20':{}, '50':{}, '100':{}}

        self.validator = re.compile(r'^[A-M][A-L](?!0{8})\d{8}[A-NP-Y]$')



        if fname:
            fname = open(fname, 'r')
            for line in fname:
                line = line.split()
                serial = line[0]
                denom = line[1]
                self.insert(serial, denom)




    def insert(self, serial_number, denom):
        current =  self.root[denom]
        for child in serial_number:
            if child not in current:
                current[child] = {}
            current = current[child]
        if None not in current:
            current[None] = None 




    def search(self, serial_number, denom):
        current =  self.root[denom]
        for child in serial_number:
            if child not in current:
                return False
            current = current[child]
        if None not in current:
            return False
        return True



def check_bills(watch_lst, fname):
    bad_bills = []
    open_file = open(fname, 'r')

    for line in open_file:
        strip_line = line.strip()
        serial_number = strip_line.split()[0]
        denom = strip_line.split()[1]

        if watch_lst.search(serial_number, denom):
            bad_bills.append(strip_line)
        elif not watch_lst.validator.search(serial_number):
            bad_bills.append(strip_line)
            watch_lst.insert(serial_number, denom)

            

    return bad_bills

        

    



