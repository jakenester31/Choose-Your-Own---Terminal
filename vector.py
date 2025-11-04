from functools import partialmethod
from opers import binaryOperators

class Vector:
    def __init__(self,x:float,y:float):
        self.pos = [0,0]
        self.x = x
        self.y = y
    
    @property
    def x(self): return self.pos[0]
    @property
    def y(self): return self.pos[1]
    
    @x.setter
    def x(self,val): self.pos[0] = float(val)
    @y.setter
    def y(self,val): self.pos[1] = float(val)
    
    def __round__(self):
        return Vector(round(self.x),round(self.y))
    
    def __repr__(self):
        return f'<{type(self).__name__} ({self.x},{self.y})>'
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def op(self,other,operator):
        print('try operator')
        try: 
            if isinstance(other,str): other = float(other)
        except: pass
        match other:
            case Vector() | IntVector():
                x = operator(self.x,other.x)
                y = operator(self.y,other.y)
            case int() | float():
                x = operator(self.x,other)
                y = operator(self.y,other)
            case str():
                raise TypeError(f"could not convert string to float: '{other}' when attempting operand conversion")
            case _: return NotImplemented
        return Vector(x,y)
[ setattr(Vector,f'__{i.__name__}__', partialmethod(lambda self,other,i: self.op(other,i),i = i)  ) for i in binaryOperators ]

class IntVector(Vector):
    def __init__(self,x,y):
        super().__init__(x,y)
    
    @Vector.x.setter
    def x(self,val): self.pos[0] = round(float(val))    
    @Vector.y.setter
    def y(self,val): self.pos[1] = round(float(val))
    
    def op(self,other,operator):
        val = super().op(other,operator)
        if val is NotImplemented: return NotImplemented 
        return val # IntVector(*val)

a = Vector(123.523,134)

print(Vector(1,1.10) ** a)