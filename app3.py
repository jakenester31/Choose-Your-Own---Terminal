class run:
    def __init__(self,obj,start):
        current = obj[start]
        print(current[0])
    
def listToString(items,human = False):
    string = ''
    if human:
        string += 'a'
        if items[0][0] in 'euioa': string += 'n'
        string += ' '
    for index,item in enumerate(items):
        if human and index == len(items) - 1:
            string += 'and '
        
        string += str(item)
        
        if index < len(items) - 1:
            string += ', '
    return string

# def stringFormatter(string:str,map:dict):
    
class f_string:
    def __init__(self,string:str,map:dict):
        self.string = string
        self.map = map
    
    def __str__(self): return self.using()
    def using(self,*args):
        for i in self.map:
            insert = self.map[i]
            if callable(insert):
                insert = insert(*args)
        return self.string[: self.string.find(i) - 1] + insert + self.string[self.string.find(i) + len(i) :]

items = ['apple','knife','blender','table']
story = {
    'start':[
            f_string('You look at the kitchen table, and on it, you see $items.',{'items':listToString(items,True)}),
            {{tuple(items):{'ktt':items}}} 
        ]
}

run(story,'start')

# branch: string, connections, before/after
# string, before

# connections:
#   simple: a:b, the simplest connection. an option leads you to a branch
#   multi: (a,b...c):d, multiple options lead to a branch. parsed into multiple simple connections
#   counter: 