import inspect, operator

# Unary > one
# Binary > two

def check(func): 
    try: return len(inspect.signature(func).parameters) 
    except: return None

all = [ getattr(operator,i) for i in dir(operator) if i[0:2] != '__' and not i in ['attrgetter','itemgetter','methodcaller'] ]
binaryOperators = [i for i in all if check(i) == 2]
unaryOperators = [i for i in all if check(i) == 1]

__all__ = [
    'all', 'binaryOperators', 'unaryOperators'
]