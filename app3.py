# The main, finished, working product. future updates coming.
class run:
    def __init__(self,obj,start):
        current = obj[start]
        res = ''
        while True:
            # before func
            valid = isinstance(current,list) and len(current) > 2
            if valid and 'before' in current[2] and callable(current[2]['before']):
                current[2]['before'](res)
            # input
            res = self.option(current,res)
            # after func
            if valid and 'after' in current[2] and callable(current[2]['after']):
                current[2]['after'](res)
            
            if res is False: break
            if res in current[1]:
                keys = [*current[1]]
                if isinstance(keys[keys.index(res)],counter):
                    keys[keys.index(res)].use()
                current = obj[current[1][res]]
            
    
    def option(self,current,res):
        print()        
        if isinstance(current,branch):
            for i in [*current[1]]:
                if isinstance(i,counter) and i.lifespan == 0:
                    del current[1][i]
            if isinstance(current[0],f_string):
                nar = current[0].using(res)
            else: nar = current[0]
            res = input(str(nar) + f' ( {listToString([*current[1]])} ) >> ')
        else: 
            nar = current
            if isinstance(current,f_string):
                nar = current.using(res)
            print(nar)
            return False
        return res
        

def unpack(obj,value = True):
    if not isinstance(obj,dict): return False
    temp = type(obj)()
    for i in obj:
        if isinstance(i,tuple):
            for index,item in enumerate(i):
                if value and isinstance(obj[i],tuple):
                    if len(obj[i]) > index: temp[item] = obj[i][index]
                else: temp[item] = obj[i]
        else: temp[i] = obj[i]
    return temp
            
class branch(list):
    def __init__(self,text,options,functions = {}):
        super().__init__([text,unpack(options,value=True),functions])

class counter:
    def __init__(self,key,lifespan):
        self.key = key
        self.lifespan = lifespan
        self._original_lifespan = lifespan
    def __str__(self):
        if self.lifespan > 0:
            return self.key
        return '!LIFESPAN'

    def use(self):
        if self.lifespan > 0:
            self.lifespan -= 1
            return self.key
    
    def __repr__(self):
        return f'<Counter: {self.key}, {self.lifespan}>'
    
    def __hash__(self):
        return hash(self.key)
    
    def __eq__(self, other):
        if isinstance(other, counter):
            return self.key == other.key
        elif isinstance(other, str):
            return self.key == other
        return NotImplemented
    
class f_string:
    def __init__(self,string:str,map:dict):
        self.string = string
        self.map = map
    
    def __str__(self): return self.using()
    def using(self,*args):
        string = self.string
        for i in self.map:
            insert = self.map[i]
            if callable(insert):
                insert = str(insert(*args))
            string = string[: string.find('$' + i)] + insert + string[string.find('$' + i) + len(i) + 1 :]
        return string

def listToString(items,human = False):
    string = ''
    if human:
        string += 'a'
        if items and items[0] and items[0][0].lower() in 'euioa': string += 'n'
        string += ' '
    for index,item in enumerate(items):
        if human and index == len(items) - 1 and len(items) > 1:
            string += 'and '
        
        string += str(item)
        
        if index < len(items) - 1:
            if len(items) > 2 or not human:
                string += ','
            string += ' '
    if string == 'a ': return ''
    return string

items = ['apple','knife','blender','gun','bazooka','banana']
inventory = []
story = {
    'start':branch(
        f_string('On the kitchen table you see $items. Take...',{'items':lambda _: listToString(items,True)}),
        {tuple([counter(i,1) for i in items]):'ktt','nothing':'end'},
        {'after':lambda res: (items.remove(res), inventory.append(res)) if res in items else None}
    ),
    
    'ktt':branch(
        f_string('You took $item',{'item':lambda res: res}),
        {'again':'start', 'finish':'end'}
    ),
    
    'end':f_string('you have $items',{'items':lambda _: listToString(inventory,True)})
}

story2 = {
    'take': branch(
        f_string(
            '$takeYou look at the table $againand see $items. Take...', {
                'take':lambda res: f'You took {listToString([res],True)}. ' if res in inventory else '',
                'again':lambda res: 'again ' if res in inventory else '',
                'items':lambda _: listToString(items,True) or 'nothing'
            }
        ),
        {tuple([counter(i,1) for i in items]):'take','nothing':'end'},
        {'after':lambda res: (items.remove(res), inventory.append(res)) if res in items else None}
    ),
    
    'end': f_string('you have $items',{'items':lambda _: listToString(inventory,True)})
}
# plan to add:
# conditional option: check if condition true then reroute from chosen branch elsewhere

run(story2,'take')