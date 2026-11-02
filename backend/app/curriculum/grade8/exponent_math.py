"""Exact Grade 8 exponent arithmetic, bounded to nonnegative exponent outcomes."""
import re
def solve(kind,v):
 expected={'expand':2,'negative':2,'compare':3,'science':1,'zero':1,'product':3,'quotient':3,'power_product':3,'mixed':4}
 if kind not in expected or len(v)!=expected[kind] or any(not isinstance(x,str) or len(x)>9 or not x.lstrip('-').isdigit() for x in v):
  raise ValueError('Unsupported exponent task')
 if kind=='science':
  if len(v[0])>9 or int(v[0])<1000:raise ValueError('Scientific notation input out of range')
 elif kind in ('expand','negative'):
  if abs(int(v[0]))>30 or not 2<=int(v[1])<=4:raise ValueError('Base or exponent out of range')
 elif kind=='zero':
  if not 1<=int(v[0])<=30:raise ValueError('Zero exponent requires nonzero bounded base')
 elif kind=='compare':
  if not 1<=int(v[0])<=30 or not 2<=int(v[1])<=9 or not 1<=int(v[2])<=1000:raise ValueError('Comparison input out of range')
 else:
  if not 1<=int(v[0])<=30 or any(not 1<=int(x)<=9 for x in v[1:]):raise ValueError('Base or exponent out of range')
  if kind=='mixed' and int(v[1])+int(v[2])>12:raise ValueError('Combined exponent out of range')
 if kind in ('expand','negative'):
  b,e=map(int,v);assert 2<=e<=4;result=b**e
  problem=f'Evaluate ({b})^{e} by showing every factor.' if b<0 else f'Evaluate {b}^{e} by showing every factor.'
  factors=' × '.join([f'({b})' if b<0 else str(b)]*e)
  rows=[f'Identify the base {b} and exponent {e}; the exponent counts equal factors.',f'Expand into exactly {e} factors: {factors}.']
  if b<0:rows.append(f'Count {e} negative factors: the product is {"positive" if e%2==0 else "negative"}.')
  rows += [f'Multiply the first two factors: {b} × {b} = {b*b}.',f'Multiply by each remaining factor in order to get {result}.',f'The value of the original expression is {result}.']
  check=f'{factors} = {result}; repeated multiplication checks the original power.';answer=str(result)
 elif kind=='compare':
  b,e,c=map(int,v);left=b**e;answer='>' if left>c else '<' if left<c else '='
  problem=f'Compare {b}^{e} with {c}. Write <, > or =.';factors=' × '.join([str(b)]*e)
  rows=[f'Identify the whole base {b} and exponent {e}.',f'Expand {b}^{e} into {factors}.',f'Multiply the first two factors: {b} × {b} = {b*b}.',f'Complete the multiplication to obtain {left}.',f'On the number line, {left} lies to the {"right" if left>c else "left" if left<c else "same position"} of {c}.',f'Write {b}^{e} {answer} {c}.']
  check=f'{b}^{e} = {left}, and {left} {answer} {c} is true.'
 elif kind=='science':
  raw=v[0];assert raw.isdigit() and int(raw)>=1000 and raw[0]!='0';k=len(raw)-1;coeff=raw[0]+'.'+raw[1:].rstrip('0') if raw[1:].rstrip('0') else raw[0];ans=f'{coeff} × 10^{k}';answer=ans
  problem=f'Write {raw} in scientific notation with a positive power of 10.'
  rows=[f'Locate the decimal point immediately after the last digit of {raw}.',f'The decimal point moves {k} places left while the digits stay in their original order.',f'The leading number is {coeff}, which is at least 1 and less than 10.',f'Each move left requires one factor of ten to preserve the value.',f'Write {raw} = {ans}.',f'Test the notation by shifting the decimal point {k} places to the right.']
  check=f'{coeff} × 10^{k} = {raw}; the original whole number is restored.'
 elif kind=='zero':
  b=int(v[0]);answer='1';problem=f'Use an exponent law to evaluate {b}^0.'
  rows=[f'Start with a nonzero base {b}.',f'Write {b}^2 ÷ {b}^2; equal nonzero quantities divide to 1.',f'Apply the quotient law to the same expression: {b}^(2−2) = {b}^0.',f'The exponent difference is 0, so {b}^0 = 1.',f'Do not mistake the zero exponent for multiplication by zero.']
  check=f'{b}^2 ÷ {b}^2 = 1; the original base is nonzero.'
 else:
  b=int(v[0]);m=int(v[1]);n=int(v[2]);assert b>0
  if kind=='product':
   problem=f'Evaluate {b}^{m} × {b}^{n} using an exponent law.';exp=m+n;answer=str(b**exp)
   rows=[f'Identify the common base {b}; the two powers have exponents {m} and {n}.',f'Expand {b}^{m} into {m} copies of {b}.',f'Expand {b}^{n} into another {n} copies of {b}.',f'Together there are {m}+{n}={exp} equal factors.',f'Apply the product law: {b}^{m} × {b}^{n} = {b}^{exp}.',f'Evaluate {b}^{exp} = {answer}.']
   check=f'{b**m} × {b**n} = {answer}; multiplying the original powers agrees.'
  elif kind=='quotient':
   assert m>=n;exp=m-n;answer=str(b**exp);problem=f'Evaluate {b}^{m} ÷ {b}^{n} using an exponent law.'
   rows=[f'Identify the same nonzero base {b} in numerator and denominator.',f'Expand the numerator into {m} factors of {b}.',f'Expand the denominator into {n} factors of {b}.',f'Cancel {n} matching nonzero factor pairs; {exp} factors remain.',f'Apply the quotient law: {b}^{m} ÷ {b}^{n} = {b}^{exp}.',f'Evaluate {b}^{exp} = {answer}.']
   check=f'{b**m} ÷ {b**n} = {answer}; division of the original powers agrees.'
  elif kind=='power_product':
   base=b*m;answer=str(base**n);problem=f'Use a power-of-a-product law to evaluate {base}^{n} by factoring {base} as {b} × {m}.'
   rows=[f'Factor the original base {base} as {b} × {m}.',
         f'Rewrite the original power: {base}^{n} = ({b} × {m})^{n}.',
         f'Expand into {n} copies of ({b} × {m}); this is multiplication, not addition.',
         f'Regroup equal factors to give {b}^{n} × {m}^{n}.',
         f'Evaluate both smaller powers: {b}^{n} = {b**n} and {m}^{n} = {m**n}.',
         f'Multiply {b**n} × {m**n} = {answer}.']
   check=f'{base}^{n} = {answer}; raising the original whole base gives the same result.'
  elif kind=='mixed':
   denominator=int(v[3]);assert m+n>=denominator and denominator>0
   remaining=m+n-denominator;answer=str(b**remaining)
   problem=f'Simplify and evaluate {b}^{m} × {b}^{n} ÷ {b}^{denominator}. Show each exponent law.'
   rows=[f'All three powers share nonzero base {b}; the exponents are {m}, {n} and {denominator}.',
         f'Combine the numerator factors first: {b}^{m} × {b}^{n} = {b}^{m+n}.',
         f'Divide by {b}^{denominator}; cancel {denominator} matching factors from numerator and denominator.',
         f'Subtract only now: ({m}+{n})−{denominator} = {remaining}.',
         f'The expression becomes {b}^{remaining}.',
         f'Evaluate {b}^{remaining} = {answer}.']
   check=f'({b**m} × {b**n}) ÷ {b**denominator} = {answer}; the original expression agrees.'
  else:raise ValueError(kind)
 def pretty(text):
  superscript=str.maketrans('0123456789','⁰¹²³⁴⁵⁶⁷⁸⁹')
  return re.sub(r'\^(\d+)',lambda match:match.group(1).translate(superscript),text)
 return answer,[pretty(row) for row in rows],pretty(problem),pretty(check)
