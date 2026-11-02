"""Exact percentage arithmetic used by the authored lesson and assessment banks."""
from fractions import Fraction

def fmt(x):
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def percent(x):
    d=x.denominator
    while d%2==0:d//=2
    while d%5==0:d//=5
    if d!=1:return fmt(x)
    k=0
    while 10**k%x.denominator:k+=1
    scale=10**k
    scaled=x*scale
    whole,decimal=divmod(scaled.numerator,scale)
    return str(whole)+(f".{decimal:0{k}d}".rstrip("0") if decimal else "")

def answer(kind,values):
    a=Fraction(values[0]);b=Fraction(values[1]) if len(values)>1 else None
    if kind=='convert':return percent(a*100)+'%'
    if kind=='of':return fmt(a*b/100)
    if kind=='part':return percent(a/b*100)+'%'
    if kind=='increase':return fmt(b*(100+a)/100)
    if kind=='decrease':return fmt(b*(100-a)/100)
    if kind=='change':return fmt(abs(a-b)/b*100)+'% '+('increase' if a>b else 'decrease' if a<b else 'no change')
    raise ValueError('Unknown percentage operation')
