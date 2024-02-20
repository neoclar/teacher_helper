# Линейное уравнение!
# x=0
# x = 5-5
# equation - уравнение
# output=f'Решите уравнение: equation}.'
from random import randint, choice, sample
# from math import gcd
from sympy import expand, simplify, init_printing, pprint # Rational, Symbol, 
from sympy.abc import X
import re
from math import gcd

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

# print(Rationalfor i in range(100, 1000):
#     num = str(i)
#     if int(str(max(int(num[0])*int(num[1]), int(num[1])*int(num[2])))+str(min(int(num[0])*int(num[1]), int(num[1])*int(num[2]))))==123:
#         print(num)('(0.2)'))
# print(Rational(eval('(0.25)/2')))
def equation():
    actions = {'brackets': ['/', '*'], 'without': ['-', '+'], 'add': 1}
    answer = randint(-25, 25)
    # print(answer)
    # x = answer
    left = X
    right = str(answer)
    # print(f'{left} = {right}')
    complete = []
    for iteration in range(1, randint(5, 7)):
        brack = choice(list(actions))
        if brack=='brackets' or randint(0, 2 if len(complete)>2 else 0):
            brack='brackets'
            try:
                if max(map(int, [e for e in re.split("[^0-9]", f'{left} = {right}') if e != '']))>250:
                    action = '/'
                else:
                    action = choice(actions[brack])
            except ValueError: action = choice(actions[brack])
            # if left.split():
            randomnum = randints(-13, -2, 2, 13)
            # if randomnum==0 or abs(randomnum)==1: randomnum+=randint(4, 7)
            # print(action, randomnum)
            left = f'({left}) {action} {randomnum if randomnum<=0 else f"({randomnum})"}'
            right = f'({right}) {action} {randomnum if randomnum<=0 else f"({randomnum})"}'
            # if not randint(0, 3):
            #     if iteration<4:
            #         print('simpl')
            #         left = simplify(left)
            #         right = simplify(right)

        elif brack=='without':
            action = choice(actions[brack])
            complete.append(0)
            randomnum = randints(-24, -1, 1, 24) 
            # print(action, randomnum)
            left = f'{left} {action} {randomnum if randomnum<=0 else f"({randomnum})"}'
            right = f'{right} {action} {randomnum if randomnum<=0 else f"({randomnum})"}'
            left = expand(left)
            right = expand(right)
        
        elif brack=='add' or len(complete)>3:
            brack='add'
            action_in = choice(('+', '-', '*', '/'))
            action_out = choice(('+', '-'))
            complete.append(0)
            randomnum = randints(-13, -1, 1, 13)
            left = f'{left} {action_out} ({X} {action_in} {randomnum if randomnum<=0 else f"({randomnum})"})'
            right = f'{right} {action_out} ({X} {action_in} {randomnum if randomnum<=0 else f"({randomnum})"})'
        # print(f'{left} = {right}')

    # reduction = [left, right]
    if randint(0, 1):
        expleft = expand(left)
        try:
            if max(map(int, [e for e in re.split("[^0-9]", str(expleft)) if e != '']))>300:
                expleft = expand(left, deep=False)
        except ValueError: pass
        left = expleft
    else:
        expright = expand(right)
        try:
            if max(map(int, [e for e in re.split("[^0-9]", str(expright)) if e != '']))>300:
                expright = expand(right, deep=False)
        except ValueError: pass
        right = expright


    if len(f'{left} = {right}')>55 or len(f'{left} = {right}')<10 or max(map(int, [e for e in re.split("[^0-9]", f'{left} = {right}') if e != '']))>175:
        # print(f'{left} = {right}')
        return equation()
    # return [left, right, answer]
    return f'{left}={right}'.replace(' ', ''), answer
    # return f'{left} = {right}   answer: {answer}'
    # print(Rational(right))

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
        # return [a, b, c, x]
        return normalize(a, b, c), x
    elif countx==0:
        z = randints(-4, 1, 1, 4)
        c+=a*z
        # return [a, b, c, None]
        return normalize(a, b, c), None
    else:
        z = randint(1, 4)
        c-=a*z*z
        x1 = x+z
        x2 = x-z
        # return [a, b, c, x1, x2]
        return normalize(a, b, c), [x1, x2]

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
        # return [a, b, c, x]
        return normalize(a, b, c), None
    elif countx==1:
        x = 0
        a = randints(-8, -1, 1, 8)
        b = randint(0, 8)*sign(a)
        c = 0
        # return [a, b, c, None]
        return normalize(a, b, c), x
    elif countx==2:
        if randint(0, 2):
            x = randint(1, 4)
            a = randints(-4, -1, 1, 4)
            b = randint(0, 8)*sign(a)
            z = randint(1, 4)
            c = -a*(z**4)-b*(z**2)
            # return [a, b, c, None]
            return normalize(a, b, c), [-x, x]
        else:
            x = randint(1, 4)
            a = choice((-1, 1))
            b = (x**2)*-a
            c = (x**4)*a
            return normalize(a, b, c), [-x, x]
    elif countx==3:
        x = randint(1, 4)
        a = randints(-4, -1, 1, 4)
        b = -a*(x**2)
        c = 0
        # return [a, b, c, None]
        return normalize(a, b, c), [-x, 0, x]
    else: # countx==4:
        t = sample([i**2 for i in range(1, 6)], k=2)
        a = randints(-4, -1, 1, 4)
        b = -sum(t)*a
        c = (b**2-(max(t)*2*a+b)**2)/4/a
        # return [a, b, c, x1, x2]
        return normalize(a, b, c), [int(-(max(t)**0.5)), int(-(min(t)**0.5)), int(min(t)**0.5), int(max(t)**0.5)]


TASKLIB = {'Линейные': equation, 'Квадратные': equation_degree, 'Биквадратные': equation_degree_bi}
TASKDES = {equation: 'Решите уравнение:', equation_degree: 'Решите квадратное уравнение:', equation_degree_bi: 'Решите биквадратное уравнение:'}


# for i in range(10):
#     print(equation_degree())


# import time
# beg = time.time()
# for i in range(100):
#     # eq = equation_degree()
#     # if len(eq[1])==1 and eq[1]:

#     print(f'{i+1}. {equation_degree_bi()}')
# end = time.time()
# print(end-beg)


    # else:
        
    #     if countx==0:
    #         return 0
    #     else:
    #         return 0






# beg = time.time()
# for i in range(1, 10000+1):
#     print(f'{i}. {equation()}')
# end = time.time()
# print(end-beg)
# eq = equation()
# # print(str(eq[0])[1:-1].replace("'", "").split(", "), f'         {eq[0][0]} = {eq[0][1]}   answer: {eq[1]}')

# left = eq[0]

# print(left)

# <p>{{first}}</p>
# <p style="padding-left: 25px;">
#     7&nbsp;
#     <span class="frac">
#         <sup>42</sup>
#         <span>/</span>
#         <sub>73</sub>
#     </span>
# </p>


# print(f'''<p>{{first}}</p>
# <p style="padding-left: 25px;">
#     7&nbsp;
#     <span class="frac">
#         <sup>42</sup>
#         <span>/</span>
#         <sub>73</sub>
#     </span>
# </p>''')




# init_printing()
# pprint(str(equation())[1:-1].replace(',', ''))