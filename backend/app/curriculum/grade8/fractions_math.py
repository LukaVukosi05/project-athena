"""Exact Grade 8 fraction arithmetic shared by validators and assessment banks."""
from fractions import Fraction
from math import lcm

def value(text):
    if not isinstance(text,str):raise ValueError('Fraction must be text')
    text=text.strip()
    if ' ' in text:
        whole,part=text.split()
        if not whole.isdigit():raise ValueError('Mixed number needs a positive whole part')
        fraction=Fraction(part)
        if not 0<fraction<1:raise ValueError('Mixed number fraction must be proper')
        return int(whole)+fraction
    return Fraction(text)

def simple(number):
    return str(number.numerator) if number.denominator==1 else f'{number.numerator}/{number.denominator}'

def mixed(number):
    whole,remainder=divmod(number.numerator,number.denominator)
    return str(whole) if remainder==0 else f'{whole} {remainder}/{number.denominator}' if whole else simple(number)

def answer(kind,values,operators=None):
    numbers=[value(x) for x in values]
    if kind=='equivalent':return 'yes' if numbers[0]==numbers[1] else 'no'
    if kind=='compare':return '<' if numbers[0]<numbers[1] else '>' if numbers[0]>numbers[1] else '='
    if kind=='order':return ' < '.join(values[i] for i in sorted(range(len(numbers)),key=lambda j:numbers[j]))
    if kind=='convert':return simple(numbers[0]) if ' ' in values[0] else mixed(numbers[0])
    if kind=='multiply':return mixed(numbers[0]*numbers[1]) if numbers[0]*numbers[1]>=1 else simple(numbers[0]*numbers[1])
    if kind=='divide':
        if numbers[1]==0:raise ValueError('Cannot divide by zero')
        quotient=numbers[0]/numbers[1]
        return mixed(quotient) if quotient>=1 else simple(quotient)
    if kind in {'square','cube','root'}:
        if len(numbers)!=1 or operators not in (2,3):raise ValueError('Power or root requires one fraction and an index')
        index=operators
        if kind=='square' and index!=2 or kind=='cube' and index!=3:raise ValueError('Power index mismatch')
        if kind=='root':
            def integer_root(n):
                approx=round(n**(1/index))
                for candidate in range(max(0,approx-2),approx+3):
                    if candidate**index==n:return candidate
                raise ValueError('Fraction has no exact integer root')
            result=Fraction(integer_root(numbers[0].numerator),integer_root(numbers[0].denominator))
        else:result=numbers[0]**index
        return mixed(result) if result>=1 else simple(result)
    if kind=='context':
        if len(numbers)!=2 or operators not in {'multiply','divide','add','subtract'}:raise ValueError('Context needs two values and a supported operation')
        a,b=numbers
        if operators=='divide' and not b:raise ValueError('Cannot divide by zero')
        result={'multiply':lambda:a*b,'divide':lambda:a/b,'add':lambda:a+b,'subtract':lambda:a-b}[operators]()
        if result<0:raise ValueError('Context result must be nonnegative')
        return mixed(result) if result>=1 else simple(result)
    if kind=='arithmetic':
        result=numbers[0]
        for op,number in zip(operators or [],numbers[1:],strict=True):result=result+number if op=='+' else result-number
        return mixed(result) if result>=1 else simple(result)
    raise ValueError('Unknown fraction task')

def common_denominator(values):return lcm(*(value(v).denominator for v in values))
