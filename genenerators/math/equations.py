import random
from random import randint, choice, sample
from sympy import symbols, Eq, Rational, Integer, sstr, parse_expr, sympify
from sympy.abc import x
import re
from sympy.abc import X
from math import gcd
x_sym = symbols('x')




def sign(number, with_one=True):
    if number>=0:
        if with_one: return 1
        else: return ''
    if number<0:
        if with_one: return -1
        else: return '-'

def randints(*periods):
    return choice([randint(beg, end) for beg, end in zip(periods[::2], periods[1::2])])

def randipercent(dictionary):
    if sum(dictionary.values())!=100:
        raise ValueError('please, sum of percentage must be 100.')
    _choice = randint(0, 99)
    _i = 0
    for key, value in zip(dictionary.keys(), dictionary.values()):
        if _choice<value+_i:
            return key
        _i+=value

def clean_generated_string(str_to_clean):
    """
    Cleans up a string.
    """
    cleaned_str = re.sub(r"x1\/", "x/", re.sub(r"\/1[^\d]|\)1[^\d]|[^\d]1\(", "", re.sub(r'\.0+ |\.0+$|0+ |0+$', '', str_to_clean)))
    return cleaned_str
def equation_line(num_actions, answer_difficulty):
    # Generate x based on answer_difficulty
    if answer_difficulty == 1:
        x_val = Integer(random.randint(-10, 10))
        while x_val == 0:
            x_val = Integer(random.randint(-10, 10))
    elif answer_difficulty == 2:
        denominator = random.choice([2, 4, 5, 8, 10])
        numerator = random.randint(-20, 20)
        x_val = Rational(numerator, denominator).evalf()
    elif answer_difficulty == 3:
        numerator = random.randint(-10, 10)
        denominator = random.randint(1, 10)
        while numerator % denominator == 0:
            numerator = random.randint(-10, 10)
            denominator = random.randint(1, 10)
        x_val = Rational(numerator, denominator)
    # elif answer_difficulty == 4:
    #     k = random.choice([2, 3, 5, 6, 7, 8, 10])
    #     n = random.randint(2, 5)
    #     x_val = sqrt(k) / n
    else:
        raise ValueError("Invalid answer difficulty")

    # Start with x = x_val
    lhs = str(x_sym)
    rhs = str(x_val)

    # Apply num_actions operations to build the equation
    operations = ['add', 'subtract', 'multiply', 'divide']*(num_actions//3+1)
    for i in range(num_actions):
        operation = operations.pop(random.randint(0,len(operations)-1))
        operand = random.randint(1, 10)
        # last_operation = operation
        if operation == 'add':
            lhs += f" + {operand}"
            rhs += f" + {operand}"
        elif operation == 'subtract':
            lhs += f" - {operand}"
            rhs += f" - {operand}"
        elif operation == 'multiply':
            lhs = f"({lhs}) * {operand}"
            rhs = f"({rhs}) * {operand}"
        elif operation == 'divide':
            lhs = f"({lhs}) / {operand}"
            rhs = f"({rhs}) / {operand}"
        
        if num_actions//2==i:
            if random.randint(0, 1):
                lhs=sstr(parse_expr(lhs))
        if num_actions//3*2==i:
            if random.randint(0, 1):
                rhs=sstr(parse_expr(rhs))

    # Create the equation
    equation = Eq(parse_expr(lhs, evaluate=(not (len(rhs)>35 and len(lhs)>35)) and len(lhs)>35), sympify(parse_expr(rhs, evaluate=len(rhs)>35 and len(lhs)>35)))

    # Convert equation to string
    lhs_str = sstr(equation.lhs).replace('*', '')
    rhs_str = sstr(equation.rhs).replace('*', '')
    equation_str = f"{lhs_str} = {rhs_str}"


    
    # Format answer
    if answer_difficulty == 1:
        answer = int(x_val)
    elif answer_difficulty == 2:
        answer = float(x_val)
    elif answer_difficulty == 3:
        answer = f"{x_val.numerator}/{x_val.denominator}"
    # elif answer_difficulty == 4:
    #     answer = sstr(x_val).replace('*', '')
    else:
        raise ValueError("Invalid answer difficulty")

    return 'Решите уравнение:', clean_generated_string(equation_str), answer

def equation_degree():
    # 25% - D=0
    # 15% - D<0
    # 60% - D>0
    def normalize(a, b, c):
        c = int(c)
        nod = gcd(a, b, c)
        a//=nod
        b//=nod
        c//=nod
        if c!=0:
            right = c-randint(4, c//3 if c//3>16 else 16)
        else:
            right = 0
        return f"""{sign(a, False)}{abs(a) if abs(a)!=1 else ''}x<sup>2</sup>{f"{'+' if b>=0 else '-'}{abs(b)}x" if b!=0 else ''}{f"{'+' if c-right>=0 else '-'}{abs(c-right)}" if c-right!=0 else ''}={right}"""
    def d0():
        x = randint(-4, 4)
        a = randints(-4, -1, 1, 4)
        b = -2*x*a
        c = b**2/(4*a)
        return a, b, c, x
    a, b, c, x= d0()

    countx = randipercent({0: 15, 1: 25, 2: 60})
    if countx==1:
        # return 'Решите квадратное уравнение:', [a, b, c, x]
        return 'Решите квадратное уравнение:', normalize(a, b, c), x
    elif countx==0:
        z = randints(-4, 1, 1, 4)
        c+=a*z
        # return 'Решите квадратное уравнение:', [a, b, c, None]
        return 'Решите квадратное уравнение:', normalize(a, b, c), None
    else:
        z = randint(1, 4)
        c-=a*z*z
        x1 = x+z
        x2 = x-z
        # return 'Решите квадратное уравнение:', [a, b, c, x1, x2]
        return 'Решите квадратное уравнение:', normalize(a, b, c), [x1, x2]

def equation_degree_bi():
    # c=0 -> 1 корень
    # sign(a)==sign(b) ->
                        # sign(a*b)==sign(c) -> 0 корней
                        # sign(a*b)!=sign(c) -> 2 корня
    # sign(a)==sign(b) ->
                        # sign(a*b)==sign(c) -> 4 корня
                        # sign(a*b)!=sign(c) -> 0 корней
    # 25% - D=0
    # 15% - D<0
    # 60% - D>0
    def normalize(a, b, c):
        c = int(c)
        nod = gcd(a, b, c)
        a//=nod
        b//=nod
        c//=nod
        return f"""{sign(a, False)}{abs(a) if abs(a)!=1 else ''}x<sup>4</sup>{f"{'+' if b>=0 else '-'}{abs(b)}x<sup>2</sup>" if b!=0 else ''}{f"{'+' if c>=0 else '-'}{abs(c)}" if c!=0 else ''}=0"""

    countx = randipercent({0: 13, 1: 7, 2: 27, 3: 24, 4: 29})
    if countx==0:
        x = randint(1, 4)
        a = randints(-4, -1, 1, 4)
        b = randint(0, 8)*sign(a)
        z = randint(1, 4)
        c = -a*(z**4)-b*(z**2)+z*a
        # return 'Решите биквадратное уравнение:', [a, b, c, x]
        return 'Решите биквадратное уравнение:', normalize(a, b, c), None
    elif countx==1:
        x = 0
        a = randints(-8, -1, 1, 8)
        b = randint(0, 8)*sign(a)
        c = 0
        # return 'Решите биквадратное уравнение:', [a, b, c, None]
        return 'Решите биквадратное уравнение:', normalize(a, b, c), x
    elif countx==2:
        if randint(0, 2):
            x = randint(1, 4)
            a = randints(-4, -1, 1, 4)
            b = randint(0, 8)*sign(a)
            z = randint(1, 4)
            c = -a*(z**4)-b*(z**2)
            # return 'Решите биквадратное уравнение:', [a, b, c, None]
            return 'Решите биквадратное уравнение:', normalize(a, b, c), [-x, x]
        else:
            x = randint(1, 4)
            a = choice((-1, 1))
            b = (x**2)*-a
            c = (x**4)*a
            return 'Решите биквадратное уравнение:', normalize(a, b, c), [-x, x]
    elif countx==3:
        x = randint(1, 4)
        a = randints(-4, -1, 1, 4)
        b = -a*(x**2)
        c = 0
        # return 'Решите биквадратное уравнение:', [a, b, c, None]
        return 'Решите биквадратное уравнение:', normalize(a, b, c), [-x, 0, x]
    else: # countx==4:
        t = sample([i**2 for i in range(1, 6)], k=2)
        a = randints(-4, -1, 1, 4)
        b = -sum(t)*a
        c = (b**2-(max(t)*2*a+b)**2)/4/a
        # return 'Решите биквадратное уравнение:', [a, b, c, x1, x2]
        return 'Решите биквадратное уравнение:', normalize(a, b, c), [int(-(max(t)**0.5)), int(-(min(t)**0.5)), int(min(t)**0.5), int(max(t)**0.5)]

