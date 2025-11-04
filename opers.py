import inspect

# registry = {}
# def register(functype):
#     def decorator(func):
#         if (not functype in registry):
#             registry[functype] = {}
#         registry[functype][func.__name__] = func
#         return func
#     return decorator

def add(a,b): return a + b
def iadd(a,b):
    a += b
    return a

def sub(a,b): return a - b
def isub(a,b):
    a -= b
    return a

def mul(a,b): return a * b
def imul(a,b):
        a *= b
        return a
    
def pow(a,b): return a ** b
def ipow(a,b):
    a **= b
    return a

def truediv(a,b): return a / b
def itruediv(a,b):
    a /= b
    return a

def floordiv(a,b): return a // b
def ifloordiv(a,b):
    a //= b
    return a

def lshift(a,b): return a << b
def ilshift(a,b):
    a <<= b
    return a

def rshift(a,b): return a >> b
def irshift(a,b):
    a >>= b
    return a

def mod(a,b): return a % b
def imod(a,b): 
    a %= b
    return a

def matmul(a,b): return a @ b
def imatmul(a,b):
    a @= b
    return a

def or_(a,b): return a | b
def ior(a,b):
    a |= b
    return a

def xor(a,b): return a ^ b
def ixor(a,b):
    a ^= b
    return a

def and_(a,b): return a & b
def iand(a,b):
    a &= b
    return a

def simple(oneArg):
    print('i am not a binary operator')

all = [globals()[i] for i in globals() if i[0 : 2] != '__' and i != 'inspect']
binaryOperators = [i for i in all if len(inspect.signature(i).parameters) == 2]
unaryOperators = [i for i in all if len(inspect.signature(i).parameters) == 1]

# Unary operators use one operand
# Binary operators use two operands

__all__ = all