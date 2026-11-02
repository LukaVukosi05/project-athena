"""Exact decimal place arithmetic and half-up rounding for Grade 8."""
from decimal import Decimal,ROUND_HALF_UP
PLACES={'tenths':1,'hundredths':2,'thousandths':3}
def dec(raw):
    value=Decimal(raw)
    if not value.is_finite() or value<0 or value>1000 or -value.as_tuple().exponent>5:raise ValueError('Unsupported Grade 8 decimal')
    return value
def render(value,places=None):
    if places is not None:return f'{value:.{places}f}'
    return format(value.normalize(),'f')
def rounded(raw,places):return dec(raw).quantize(Decimal(1).scaleb(-places),rounding=ROUND_HALF_UP)
def solution(kind,values):
    if kind=='place':
        a,place=values
        if place not in PLACES:raise ValueError('Invalid place')
        digit=(a.partition('.')[2]+'000')[PLACES[place]-1]
        answer=digit
        problem=f'In {a}, what digit is in the {place} place?'
        rows=[f'Align {a} in ones, tenths, hundredths and thousandths columns.',f'Count {PLACES[place]} position(s) to the right of the decimal point.',f'The digit in the {place} column is {digit}.']
        check=f'Read the digits of {a} again from the decimal point; the {place} column contains {digit}.'
    elif kind=='compare':
        a,b=values;x,y=dec(a),dec(b);answer='<' if x<y else '>' if x>y else '='
        problem=f'Compare {a} and {b}. Write <, > or =.'
        width=max(len(a.partition('.')[2]),len(b.partition('.')[2]),3)
        rows=[f'Align decimal points: {x:.{width}f} and {y:.{width}f}.',f'Read place-value columns from left to right until the first different digit.',f'{a} {answer} {b}.']
        check=f'On a number line, {a} lies {"left of" if answer=="<" else "right of" if answer==">" else "at the same point as"} {b}.'
    elif kind=='order':
        if len(values)!=3:raise ValueError('Ordering needs three values')
        a,b,c=values;nums=[dec(v) for v in values]
        if len(set(nums))!=3:raise ValueError('Ordering values must be distinct')
        answer=', '.join(v for v in sorted(values,key=dec))
        problem=f'Order {a}, {b} and {c} from least to greatest.'
        width=max(3,*(len(v.partition('.')[2]) for v in values))
        rows=[f'Align all decimal points and pad with zeroes to {width} decimal places.',f'Compare columns from left to right, then place the three numbers on one number line.',f'From left to right: {answer}.']
        check=f'The ordered values satisfy {" < ".join(sorted(values,key=dec))}.'
    elif kind=='round':
        a,p=values;places=int(p)
        if places not in (1,2,3):raise ValueError('Unsupported rounding place')
        x=dec(a);step=Decimal(1).scaleb(-places);lower=x//step*step;upper=lower+step;mid=lower+step/2
        answer=render(rounded(a,places),places)
        problem=f'Round {a} to {places} decimal place{"s" if places!=1 else ""}.'
        rows=[f'Neighbouring marks at {places} decimal place(s) are {render(lower,places)} and {render(upper,places)}.',f'The midpoint is {render(mid,places+1)}. Place {a} relative to it; a midpoint rounds upward.',f'Round to {answer}, retaining {places} decimal place(s).']
        check=f'{a} is at or beyond the midpoint {render(mid,places+1)}' if x>=mid else f'{a} is below the midpoint {render(mid,places+1)}'
    elif kind=='estimate':
        a,b,p=values;places=int(p)
        if places not in (1,2):raise ValueError('Unsupported estimate place')
        x,y=rounded(a,places),rounded(b,places);answer=render(x+y,places)
        problem=f'Estimate {a} + {b} by first rounding each number to {places} decimal place{"s" if places!=1 else ""}.'
        rows=[f'Round the first number: {a} → {render(x,places)}.',f'Round the second number: {b} → {render(y,places)}.',f'Add rounded quantities: {render(x,places)} + {render(y,places)} = {answer}.']
        check=f'Exact sum is {render(dec(a)+dec(b))}; the estimate {answer} uses separately rounded inputs.'
    else:raise ValueError('Unsupported decimal task')
    return answer,rows,problem,check

def operation(kind,values):
    """Return exact answer and one legal operation per teaching row."""
    if kind not in {'multiply','divide'} or len(values)!=2:raise ValueError('Two decimal operands required')
    a,b=values;x,y=dec(a),dec(b)
    if not y:raise ValueError('Decimal divisor cannot be zero')
    if '.' not in a or '.' not in b:raise ValueError('Both operands must be decimal fractions')
    p,q=len(a.split('.')[1]),len(b.split('.')[1])
    if kind=='multiply':
        left=int(a.replace('.',''));right=int(b.replace('.',''))
        rows=[f'Rewrite {a} as {left} ÷ 10^{p}; the decimal point sets the first scale.',
              f'Rewrite {b} as {right} ÷ 10^{q}; both scales combine to 10^{p+q}.']
        partials=[]
        for position,digit in enumerate(reversed(str(right))):
            part=left*int(digit)*10**position;partials.append(part)
            rows.append(f'Multiply {left} × {digit} × 10^{position} = {part}; align this partial product in its place-value column.')
        integer=sum(partials);answer=render(x*y)
        rows.extend((f'Add the aligned partial products: {" + ".join(map(str,partials))} = {integer}.',
                     f'Divide {integer} by 10^{p+q}; place the decimal point {p+q} digits from the right: {answer}.'))
        check=f'{answer} ÷ {b} = {a}, so the product agrees with both original decimal factors.'
        return answer,rows,f'Calculate {a} × {b}. Show each partial product and check the decimal point.',check
    scale=max(p,q);factor=10**scale
    numerator=x*factor;denominator=y*factor
    if numerator!=int(numerator) or denominator!=int(denominator):raise ValueError('Common decimal scale must create integers')
    N,D=int(numerator),int(denominator)
    rows=[f'Choose 10^{scale} so multiplying BOTH original operands clears both decimal points.',
          f'Apply the same factor: {a} ÷ {b} = {N} ÷ {D}. The quotient is unchanged.']
    remainder=0;whole_digits=[]
    for digit in str(N):
        brought=remainder*10+int(digit);qdigit,remainder=divmod(brought,D);whole_digits.append(str(qdigit))
        rows.append(f'Bring down {digit}: {brought} ÷ {D} gives digit {qdigit}; subtract {qdigit} × {D} to leave remainder {remainder}.')
    places=[];seen=set()
    while remainder:
        if remainder in seen or len(places)>=6:raise ValueError('Use terminating decimal quotients of at most six places')
        seen.add(remainder);brought=remainder*10;qdigit,remainder=divmod(brought,D);places.append(str(qdigit))
        rows.append(f'Add a decimal zero: {brought} ÷ {D} gives digit {qdigit}; subtract {qdigit} × {D} to leave remainder {remainder}.')
    answer=render(x/y)
    rows.append(f'Read the quotient digits with the decimal point: {answer}.')
    check=f'{answer} × {b} = {a}, so division reverses to the original dividend.'
    return answer,rows,f'Divide {a} by {b}. Show the equal scaling and quotient digits.',check


def power_root(kind,values):
    """Exact bounded powers and principal roots; reject non-perfect decimal radicands."""
    if kind not in {'power','root'} or len(values)!=2:raise ValueError('Expected power/root and degree')
    raw,degree=values;degree=int(degree)
    if degree not in (2,3):raise ValueError('Only square and cube supported')
    x=dec(raw)
    if '.' not in raw:raise ValueError('Decimal input required')
    if kind=='power':
        from decimal import Decimal
        if x**degree>1000:raise ValueError('Power exceeds range')
        a=raw
    else:
        from decimal import Decimal
        candidates=[]
        for k in range(4):
            scaled=x*(10**(k*degree))
            if scaled!=int(scaled):continue
            target=int(scaled);low,high=0,10000
            while low<=high:
                mid=(low+high)//2
                if mid**degree==target:
                    candidates.append(Decimal(mid).scaleb(-k));break
                if mid**degree<target:low=mid+1
                else:high=mid-1
        if not candidates:raise ValueError('Radicand has no bounded terminating root')
        a=render(min(candidates))
        if '.' not in a:a+='.0'
    from decimal import Decimal
    base=Decimal(a);answer=render(base**degree) if kind=='power' else render(base)
    scale=len(a.partition('.')[2]);integer=int(a.replace('.',''));name='square' if degree==2 else 'cube'
    if kind=='power':
        factors=' × '.join([a]*degree)
        rows=[f'Identify the base {a} and the exponent {degree}; a {name} repeats the same factor {degree} times.',
              f'Expand the power: ({a})^{degree} = {factors}.',
              f'Each factor has {scale} decimal place(s), so the product has {degree} × {scale} = {degree*scale} decimal places before removing trailing zeros.',
              f'Compute the integer product: {" × ".join([str(integer)]*degree)} = {integer**degree}.']
        if degree==3:rows.append(f'Group the first two factors: {a} × {a} = {render(base*base)}; multiply that by the third factor.')
        rows.append(f'Place the decimal point {degree*scale} positions from the right: {answer}.')
        return answer,rows,f'Calculate ({a})^{degree}. Show the repeated factors and decimal scale.',f'{factors} = {answer}; repeated multiplication checks the original power.'
    rad=raw
    rows=[f'Identify the {name} root: find the non-negative decimal that gives {rad} when multiplied {degree} times.',
          f'Estimate between neighbouring whole numbers, then look at the decimal places of {rad}.',
          f'Test {a} as a candidate; write it as {integer} ÷ 10^{scale}.',
          f'Expand the check: {" × ".join([a]*degree)}.',
          f'The integer factors give {integer**degree}, and {degree} × {scale} = {degree*scale} decimal places give {rad}.',
          f'Since the candidate is non-negative and its {name} is {rad}, the principal root is {answer}.']
    problem=f'Find the principal {degree}rd root of {rad}.' if degree==3 else f'Find the principal square root of {rad}.'
    return answer,rows,problem,f'{answer}^{degree} = {rad}; this returns the original radicand.'
