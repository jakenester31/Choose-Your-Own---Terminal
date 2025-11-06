from functools import partialmethod
from opers import unaryOperators, binaryOperators

class Vector():
    def __init__(self,x:float,y:float):
        self.pos: list[float] = [0,0]
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
    
    def binaryOperation(self,other,operator):
        try: other = float(other) if isinstance(other,str) else other
        except: raise TypeError(f"Failed to convert string literal '{other}' to float during operand conversion") from None
        match other:
            case Vector() | IntVector():
                x = operator(self.x,other.x)
                y = operator(self.y,other.y)
            case int() | float():
                x = operator(self.x,other)
                y = operator(self.y,other)
            case _: return NotImplemented
        return Vector(x,y)
    
    def unaryOperation(self,operator):
        return Vector(operator(self.x),operator(self.y))
[ setattr(Vector,f'__{i.__name__}__', partialmethod(lambda self, i: self.unaryOperation(i),i = i) ) for i in unaryOperators ]
[ setattr(Vector,f'__{i.__name__}__', partialmethod(lambda self,other,i: self.binaryOperation(other,i),i = i)  ) for i in binaryOperators ]

class IntVector(Vector):
    def __init__(self,x,y): super().__init__(x,y)
    
    @Vector.x.setter
    def x(self,val): self.pos[0] = round(float(val))    
    @Vector.y.setter
    def y(self,val): self.pos[1] = round(float(val))
    
    def binaryOperation(self,other,operator):
        val = super().binaryOperation(other,operator)
        if val is NotImplemented: return NotImplemented 
        return val if isinstance(self,IntVector) and isinstance(other,IntVector) else IntVector(*val)

a = Vector(123.523,134)
print(Vector(1,1) + 1)
