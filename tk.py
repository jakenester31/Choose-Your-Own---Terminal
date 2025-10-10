import tkinter as tk
from tkinter import ttk
import threading
from types import UnionType, GenericAlias
from typing import Any, ForwardRef, TypeVar
from functools import partial
import operator
from typeguard import check_type, TypeCheckError

class classproperty:
    def __init__(self, get): self.get = get
    def __get__(self,_,cls): return self.get(cls)

class ns: 
    """Namespace"""
    def __init__(self,**kwargs): 
        for name in kwargs: 
            object.__setattr__(self, name, kwargs[name])
    def __setattr__(self,name,val) -> None:
        object.__setattr__(self, name, val)
    def __getattribute__(self, name: str) -> Any:
        return object.__getattribute__(self,name)

class Singleton:
    _instance:'Singleton'
    _initialized:bool = False
    
    @classproperty
    def main(cls):
        return cls._instance
      
    def __new__(cls):
        if not hasattr(cls,'_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Singleton._initialized:
            Singleton._initialized = True
            return False
        return True

class App(Singleton):
    def __init__(self):
        if super().__init__(): return
        self.threads:dict[str,threading.Thread] = {}
        self.threads['gui'] = threading.Thread(target=self.mainloop)
        self.threads['gui'].start()
        
    def mainloop(self):
        self.root = tk.Tk()
        def close_func(self):
            self.close.event.set()
            self.root.quit()
        self.close = ns(event=threading.Event(), function = partial(close_func,self))
        del close_func
        self.root.protocol('WM_DELETE_WINDOW',self.close.function)
        
        self.setup()
        self.root.mainloop()
             
    def setup(self):
        ##y Root
        self.root.title('Choose Your Own Adventure')
        self.root.geometry('400x400')
        self.root.overrideredirect(True)
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        ##y Header
        self.header = tk.Frame(self.root,bg='black',height=30)
        self.header.pack(side=tk.TOP,fill=tk.X)
        self.header.pack_propagate(False)
        self.header.bind('<Button-1>',self.drag)
        self.header.bind('<B1-Motion>',self.drag)
        ##y Title
        self.title = tk.Label(
            self.header,
            text='Choose Your Own Adventure',
            bg='black',
            fg='white',
            font=('Arial',10)
        )
        self.title.pack(side=tk.LEFT,padx=30)
        self.title.bind('<Button-1>',self.drag)
        self.title.bind('<B1-Motion>',self.drag)
        ##y Close Button
        self.style.configure(
            'root_close.TButton',
            background='black',
            width=2,
            height=2,
            font=('Arial',12),
            foreground='grey',
            darkcolor='black',
            lightcolor='grey',
            relief='flat',
            borderwidth=0,
            # padding=(0,0),
            takefocus=0,
        )
        # self.style.map(
        #     'root_close.TButton',
        #     background=[
        #         ('pressed','darkred'),
        #         ('active','red'),
                
        #     ],
        #     foreground=[
        #         ('active','white')
        #     ]
        # )
        self.close.button = ttk.Button(
            self.header,
            text='✕',
            command=self.close.function,
            style='root_close.TButton'
        )
        self.close.button.pack(side=tk.RIGHT)
        self.close.transition = 0
        def transition_start(e = None):
            val = hex(self.close.transition, 0, 0)
            print(val)
            self.style.configure(
                'root_close.TButton',
                background=val
            )
            if self.close.transition < 255:
                self.close.button.after(100,transition_start)
                self.close.transition += 10
        self.close.button.bind('<Enter>',transition_start)
        
    def drag(self,e):
        if e.type == tk.EventType.ButtonPress:
            self.dragOffset = Vector(e.x,e.y)
        root = Vector(self.root.winfo_x(),self.root.winfo_y())
        res = root - self.dragOffset + Vector(e.x,e.y)
        self.root.geometry(f'+{res.x}+{res.y}')

##y typechecker
GENERALTYPES = ( type, GenericAlias, UnionType, ForwardRef, TypeVar )

class metaTypechecker(type):
    def __new__(cls,name,bases,namespace):
        return super().__new__(cls,name,bases,namespace)

class typechecker:
    rules:dict
    
    def __setattr__(self, name: str, val: Any):
        if not hasattr(self,'rules'):
            super().__setattr__(name,val)
            print("WARNING, class extending 'typechecker' has no 'rules' attribute ")
            return
        if name in self.rules:
            try:
                super().__setattr__(name,check_type(val,self.rules[name]))
            except TypeCheckError as e:
                if ('#mode' in self.rules and self.rules['#mode'] != 'strict') or not '#mode' in self.rules:
                    print(f"TYPECHECKER_ERR: Cannot set attribute '{name}' to '{val}' of class '{self.__class__.__name__}', Attribute must follow signature: {self.rules[name]} ")
                else: raise e

##y vector
class Vector(typechecker):
    rules = {
        '#mode':'strict',
        'x':int,
        'y':int
    }
    
    
    def __init__(self,x:int, y:int):
        self.x = x
        self.y = y
        
    
    def __repr__(self): return f'<Vector ({self.x},{self.y})>'
    
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '**': operator.pow,
    }
    
    def _operation(self,operator,other) -> 'Vector':
        if isinstance(other,Vector):
            x = Vector.ops[operator](self.x, other.x)
            y = Vector.ops[operator](self.y, other.y)
            return Vector(round(x),round(y))
        if isinstance(other,tuple) and len(other) == 2:
            x = Vector.ops[operator](self.x, other[0])
            y = Vector.ops[operator](self.y, other[1])
            return Vector(round(x),round(y))
        if isinstance(other,int):
            x = Vector.ops[operator](self.x, other)
            y = Vector.ops[operator](self.y, other)
            return Vector(round(x),round(y))
        return NotImplemented
    
    def __add__(self,other:'Vector | int | tuple[int,int]') -> 'Vector': return self._operation('+',other)
    def __sub__(self,other:'Vector | int | tuple[int,int]') -> 'Vector': return self._operation('-',other)
    def __mul__(self,other:'Vector | int | tuple[int,int]') -> 'Vector': return self._operation('*',other)
    def __truediv__(self,other:'Vector | int | tuple[int,int]') -> 'Vector': return self._operation('/',other)
    def __pow__(self,other:'Vector | int | tuple[int,int]') -> 'Vector': return self._operation('**',other)
    
    
    def __radd__(self,other): return self + other
    def __rsub__(self,other): return self - other
    def __rmul__(self,other): return self * other
    def __rtruediv__(self, other): return self / other
    def __rpow__(self,other): return self ** other
    
    def __iadd__(self,other): return self + other
    
    def __round__(self,place = None):
        return Vector(round(self.x,place),round(self.y,place))
    
    def __iter__(self):
        yield self.x
        yield self.y


def clamp(minimum:int,target:int | tuple[int,...],maximum:int):
    if isinstance(target,tuple):
        return tuple(max(minimum,min(i,maximum)) for i in target)
    return max(minimum,min(target,maximum))

def hex(r,g,b):
    return "#%02x%02x%02x" % (clamp(0,r,255),clamp(0,g,255),clamp(0,b,255))