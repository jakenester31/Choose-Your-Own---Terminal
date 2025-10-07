import tkinter as tk
from tkinter import ttk
import threading

class classproperty:
    def __init__(self, get): self.get = get
    def __get__(self,_,cls): return self.get(cls)

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
        self.closeEvent = threading.Event()
        self.root.protocol('WM_DELETE_WINDOW',self.close)
        self.setup()
        self.root.mainloop()
             
    def setup(self):
        ##y Root
        self.root.title('Choose Your Own Adventure')
        self.root.geometry('400x400')
        self.root.overrideredirect(True)
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
        self.close_button = HoverButton(
            self.header,
            text='✕',
            command=self.close,
            bg='black',
            fg='white',
            bd=0,
            activebackground='darkred',
            activeforeground='white',
            hoverbg='red',
            width=3,
            height=3,
            font=('Arial',12),
        )
        self.close_button.pack(side=tk.RIGHT)
        ##y Attributes
        
    def drag(self,e):
        if e.type == tk.EventType.ButtonPress:
            self.dragOffset = vector(e.x,e.y)
        root = vector(self.root.winfo_x(),self.root.winfo_y())
        res = root - self.dragOffset + vector(e.x,e.y)
        self.root.geometry(f'+{res.x}+{res.y}')
        
    
    def close(self):
        self.closeEvent.set()
        self.root.quit()

class HoverButton(tk.Button):
    def __init__(self,*args,hoverbg='',**kwargs):
        super().__init__(*args,**kwargs)
        self.bind('<Enter>',self.hover)
        self.bind('<Leave>',self.leave)
        # self.bind('<B1-Motion>',self.down)
        self.bind('<Button-1>',self.down)
        self.props = kwargs
        self.props['hoverbg'] = hoverbg

    def hover(self,e): self.config(background=self.props['hoverbg'])
    def leave(self,e): self.config(background=self.props['bg'])
            
    def down(self,e):
        self.config(relief=tk.FLAT)
        
class vector:
    def __init__(self,x:int | None,y:int | None):
        if not x is None:
            self.x: int = x
        if not y is None:
            self.y: int = y
    
    def __repr__(self): return f'<vector ({self.x if not self.x is None else '[ERR]'},{self.y if not self.y is None  else '[ERR]'})>'
    
    def __sub__(self,other:'vector | int') -> 'vector':
        x = 0
        y = 0
        if isinstance(other,vector):
            x = self.x - other.x
            y = self.y - other.y
        if isinstance(other,int):
            x = self.x - other
            y = self.y - other
        return vector(x,y)
    
    def __add__(self,other:'vector | int') -> 'vector':
        x = 0
        y = 0
        if isinstance(other,vector):
            x = self.x + other.x
            y = self.y + other.y
        if isinstance(other,int):
            x = self.x + other
            y = self.y + other
        return vector(x,y)

App()