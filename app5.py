from inspect import CO_VARARGS
from typing import Callable, Any

class f_string:
    def __init__(self,string: str,map: dict): self.string, self.map = string, map
    def __repr__(self) -> str: return f'<"{self.string}", {self.map}>'
    def __str__(self) -> str: return self.using()
    def using(self,**kargs: tuple[Any,...] | list[Any] | Any):
        temp = self.string
        return str([ temp := temp.replace(f'{{{i}}}',str(safeCall(self.map[i],*(kargs.get(i) or ())))) for i in self.map][-1:-1] or temp)

def safeCall(func:Callable[...,Any] | Any,*args:Any) -> Any: 
    if not callable(func): return func
    return func(*args[:(None if (e := func.__code__).co_flags & CO_VARARGS else e.co_argcount)])

test = f_string('test {a}, {b}',{'a':1,'b':2})
print(test)
test.map['a'] = 3
test.map['b'] = 4
print(test)