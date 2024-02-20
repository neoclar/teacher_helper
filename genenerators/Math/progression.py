# Места в кинотеатре/театре/амфитеатре/цирке
# червяк ползёт по дереву
# дальнобойщик едет из Москвы в Пекин
# грузовик перевозит грузы
# приседания/отжимания/подтягивания/бег/прыжки на скакалке

from random import choice, randint, shuffle

def randints(*periods):
    return choice([randint(beg, end) for beg, end in zip(periods[::2], periods[1::2])])

def sign(number, with_one=True):
    if number>=0:
        if with_one: return 1
        else: return ''
    if number<0:
        if with_one: return -1
        else: return '-'

formsa = {
'sn': [['a1', 'd'], ['a1', 'an'], ['a1', 'an+w'], ['an', 'an+w']],
'an': [['a1', 'd'], ['an-w', 'an+w'], ['an+w', 'd'], ['an+w', 'a1']], 
'd': [['a1', 'an'], ['an+w', 'an'], ['sn', 'a1'], ['sn', 'an+w']], 
'a1': [['sn', 'an'], ['sn', 'd'], ['sn', 'an+w'], ['an', 'd'], ['an+w', 'an']]
}

formsg = {
'sn': [['a1', 'd'], ['a1', 'an'], ['a1', 'an+w'], ['an', 'an+w']],
'an': [['a1', 'd'], ['an-w', 'an+w'], ['an+w', 'd'], ['an+w', 'a1']], 
'd': [['a1', 'an'], ['an+w', 'an'], ['sn', 'a1'], ['sn', 'an+w']], 
'a1': [['sn', 'an'], ['sn', 'd'], ['sn', 'an+w'], ['an', 'd'], ['an+w', 'an']]
}

texts_condition_a = {
    'cinema': {
        'beg': [''],
        'sn': ['в первых {!n} рядах {place[1]+" " if len(text_need)==0 else""}{s!n} мест{"о" if s!n%10==1 and s!n//10%10!=1 else "а" if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else ""}'], #  or (n>9 and n%10==0)
        'n': ['в {place[0]} {!n} ряд{"" if n%10==1 and n//10%10!=1 else "а" if n%10<5 and !n%10>1 and n//10%10!=1 else "ов"}'],
        'an': ['в {!n} ряду {place[1]+" " if len(text_need)==0 else""}{a!n} мест{"о" if a!n%10==1 and a!n//10%10!=1 else "а" if a!n%10<5 and a!n%10>1 and a!n//10%10!=1 else ""}'],
        'd': ['каждый следующий ряд {place[1]+" " if len(text_need)==0 else""}количество мест увеличивается на {d}'],
        'a1': ['в первом ряду {place[1]+" " if len(text_need)==0 else""}{a1} мест{"о" if a1%10==1 and a1//10%10!=1 else "а" if a1%10<5 and a1%10>1 and a1//10%10!=1 else ""}']
    },
    'exercises': {
        'beg': ['{name[1]} решил{"а" if name[0]=="ж" else ""} {"заняться спортом" if randint(0, 1) else "похудеть"}. ', 'Доктор посоветовал {name[2]} {"заняться спортом" if randint(0, 19) else "похудеть"}. '],
        'sn': ['за {!n} {"день" if s!n%10==1 and s!n//10%10!=1 else "дня" if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else "дней"} {name[1]+" " if not randint(0, 3) else ""}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} {s!n}{" "+place[0 if s!n%10==1 and s!n//10%10!=1 else 1 if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else 2] if place[1]!="бег" else (" километр" if s!n%10==1 and s!n//10%10!=1 else " километра" if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else " километров") if len(text_need)==0 else""}'], #  or (n>9 and n%10==0)
        # 'n': ['в {place[0]} {!n} ряд{"" if n%10==1 and n//10%10!=1 else "а" if n%10<5 and n%10>1 and n//10%10!=1 else "ов"}'],
        'an': ['в {!n} день {name[1]+" " if not randint(0, 3) else ""}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} {a!n}{" "+place[0 if a!n%10==1 and a!n//10%10!=1 else 1 if a!n%10<5 and a!n%10>1 and a!n//10%10!=1 else 2] if place[1]!="бег" else (" километр" if a!n%10==1 and a!n//10%10!=1 else " километра" if a!n%10<5 and a!n%10>1 and a!n//10%10!=1 else " километров") if len(text_need)==0 else""}'],
        'd': ['каждый следующий день {"количество "+place[1] if place[1]!="бег" else "расстояние"} увеличивается на {d}{(" километр" if d%10==1 and d//10%10!=1 else " километра" if d%10<5 and d%10>1 and d//10%10!=1 else " километров") if place[1]=="бег" else ""}'],
        'a1': ['в первый день {name[1]+" " if not randint(0, 3) else ""}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} {a1}{" "+place[0 if a1%10==1 and a1//10%10!=1 else 1 if a1%10<5 and a1%10>1 and a1//10%10!=1 else 2] if place[1]!="бег" else (" километр" if a1%10==1 and a1//10%10!=1 else " километра" if a1%10<5 and a1%10>1 and a1//10%10!=1 else " километров") if len(text_need)==0 else""}']
    }
}

texts_question_a = {
    'cinema': {
        'sn': ['Сколько мест в первых {!n} рядах?'],
        'an': ['Сколько мест в {!n} ряду?'],
        'd': ['На какое количество мест увеличивается ряд?'],
        'a1': ['Сколько мест в первом ряду?']
    },
    'exercises': {
        'sn': ['Cколько{" "+place[2] if place[1]!="бег" else ""} {name[1]+" "}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} за первые {!n} {"день" if s!n%10==1 and s!n//10%10!=1 else "дня" if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else "дней"}?'],
        # 'n': ['Error!'*1000],
        'an': ['Cколько{" "+place[2] if place[1]!="бег" else ""} {name[1]+" "}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} в {!n} день?'],
        'd': ['Насколько каждый следующий день сложнее предыдущего?', 'Насколько {name[1]} увеличивает {"количество "+place[2] if place[1]!="бег" else "расстояние"}?'],
        'a1': ['Cколько{" "+place[2] if place[1]!="бег" else ""} {name[1]+" "}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""}{" километров" if place[1]!="бег" else ""}?']
    }
}

texts_condition_g = {
    'cinema': {
        'beg': [''],
        'sn': ['в первых {!n} рядах {place[1]+" " if len(text_need)==0 else""}{s!n} мест{"о" if s!n%10==1 and s!n//10%10!=1 else "а" if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else ""}'], #  or (n>9 and n%10==0)
        'n': ['в {place[0]} {!n} ряд{"" if n%10==1 and n//10%10!=1 else "а" if n%10<5 and !n%10>1 and n//10%10!=1 else "ов"}'],
        'an': ['в {!n} ряду {place[1]+" " if len(text_need)==0 else""}{a!n} мест{"о" if a!n%10==1 and a!n//10%10!=1 else "а" if a!n%10<5 and a!n%10>1 and a!n//10%10!=1 else ""}'],
        'd': ['каждый следующий ряд {place[1]+" " if len(text_need)==0 else""}количество мест увеличивается в {d} раз'],
        'a1': ['в первом ряду {place[1]+" " if len(text_need)==0 else""}{a1} мест{"о" if a1%10==1 and a1//10%10!=1 else "а" if a1%10<5 and a1%10>1 and a1//10%10!=1 else ""}']
    },
    'exercises': {
        'beg': ['{name[1]} решил{"а" if name[0]=="ж" else ""} {"заняться спортом" if randint(0, 1) else "похудеть"}, а каждый день увеличивать объём тренировки в {"определённое количество" if not "d" in needs else d} раз. ', 'Доктор посоветовал {name[2]} {"заняться спортом" if randint(0, 19) else "похудеть"} и каждый день увеличивать объем тренировки в {"определённое количество" if not "d" in needs else d} раз. '],
        'sn': ['за {!n} {"день" if s!n%10==1 and s!n//10%10!=1 else "дня" if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else "дней"} {name[1]+" " if not randint(0, 3) else ""}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} {s!n}{" "+place[0 if s!n%10==1 and s!n//10%10!=1 else 1 if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else 2] if place[1]!="бег" else (" километр" if s!n%10==1 and s!n//10%10!=1 else " километра" if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else " километров") if len(text_need)==0 else""}'], #  or (n>9 and n%10==0)
        # 'n': ['в {place[0]} {!n} ряд{"" if n%10==1 and n//10%10!=1 else "а" if n%10<5 and n%10>1 and n//10%10!=1 else "ов"}'],
        'an': ['в {!n} день {name[1]+" " if not randint(0, 3) else ""}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} {a!n}{" "+place[0 if a!n%10==1 and a!n//10%10!=1 else 1 if a!n%10<5 and a!n%10>1 and a!n//10%10!=1 else 2] if place[1]!="бег" else (" километр" if a!n%10==1 and a!n//10%10!=1 else " километра" if a!n%10<5 and a!n%10>1 and a!n//10%10!=1 else " километров") if len(text_need)==0 else""}'],
        'd': ['каждый следующий день {"количество "+place[1] if place[1]!="бег" else "расстояние"} увеличивается в {d} раз'],
        'a1': ['в первый день {name[1]+" " if not randint(0, 3) else ""}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} {a1}{" "+place[0 if a1%10==1 and a1//10%10!=1 else 1 if a1%10<5 and a1%10>1 and a1//10%10!=1 else 2] if place[1]!="бег" else (" километр" if a1%10==1 and a1//10%10!=1 else " километра" if a1%10<5 and a1%10>1 and a1//10%10!=1 else " километров") if len(text_need)==0 else""}']
    }
}

texts_question_g = {
    'cinema': {
        'sn': ['Сколько мест в первых {!n} рядах?'],
        'an': ['Сколько мест в {!n} ряду?'],
        'd': ['Во сколько раз увеличивается количество мест в ряду?'],
        'a1': ['Сколько мест в первом ряду?']
    },
    'exercises': {
        'sn': ['Cколько{" "+place[2] if place[1]!="бег" else ""} {name[1]+" "}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} за первые {!n} {"день" if s!n%10==1 and s!n//10%10!=1 else "дня" if s!n%10<5 and s!n%10>1 and s!n//10%10!=1 else "дней"}?'],
        # 'n': ['Error!'*1000],
        'an': ['Cколько{" "+place[2] if place[1]!="бег" else ""} {name[1]+" "}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""} в {!n} день?'],
        'd': ['Во сколько раз каждый следующий день сложнее предыдущего?', 'Во сколько раз {name[1]} увеличивает {"количество "+place[2] if place[1]!="бег" else "расстояние"}?'],
        'a1': ['Cколько{" "+place[2] if place[1]!="бег" else ""} {name[1]+" "}{("выполнил" if randint(0, 1) else "сделал") if place[1]!="бег" else "пробежал"}{"а" if name[0]=="ж" else ""}{" километров" if place[1]=="бег" else ""}?']
    }
}

# /отжимания/подтягивания/бег/прыжки на скакалке
places = {
    'cinema': [['кино', 'кино'], ['кинотеатре', 'кинотеатра'], ['театре', 'театра'], ['амфитеатре', 'амфитеатра'], ['цирке', 'цирка']],
    'names': [['м', 'Ваня', 'Ване'], ['ж', 'Наташа', 'Наташе'], ['м', 'Борис', 'Борису'], ['ж', 'Настя', 'Насте']],
    'exercises': [['приседание', 'приседания', 'приседаний'], ['отжимание', 'отжимания', 'отжиманий'], ['подтягивание', 'отжимания', 'отжиманий'], ['бег', 'бег', 'бег']]
}


def progression():
    pass

def arithmetic():
    def find_s(n):
        return a1*n+(n-1)*d*n/2
    def find_a(n):
        return a1+(n-1)*d
    ques = choice(list(formsa))
    need = choice(formsa[ques])
    # need = form[0]
    # form = form[1]
    d = randint(1, 5)
    a1 = randint(1, 25)
    n = randint(7, 20)
    w = randints(-4, -1, 1, 4)
    ques = ques.replace('n', str(n))
    try:
        answer = eval(ques)
    except NameError:
        answer = eval(f"find_{ques[0]}({eval(ques[1:-1]+ques[-1])})")


    needs = {}
    shuffle(need)
    for v in need:
        try:
            if v!='w' and v!='n':
                needs[v] = eval(v)
        except NameError:
            needs[f"{v[0]}{eval(v[1:-1]+v[-1])}"] = int(eval(f"find_{v[0]}({eval(v[1:-1]+v[-1])})"))
    locals().update(needs)
    condition = choice(list(texts_condition_a))
    place = choice(places[condition])
    name = choice(places['names'])
    text_need = []
    for v in needs:
        try:
            text_need.append(eval("f'"+choice(texts_condition_a[condition][v])+"'"))
        except KeyError:
            text_need.append(eval("f'"+choice(texts_condition_a[condition][v[0]+'n']).replace('!n', str(v[1:-1]+v[-1]))+"'"))
    try:
        text_need.append(eval("f'"+choice(texts_question_a[condition][ques])+"'"))
    except KeyError as e:
        exec(f'{str(e)[1:-1]} = find_{str(e)[1]}({str(e)[2:-1]})')
        text_need.append(eval("f'"+choice(texts_question_a[condition][ques[0]+'n']).replace('!n', str(ques[1:-1]+ques[-1]))+"'"))

    text_ques = text_need.pop(-1)
    text = eval("f'"+choice(texts_condition_a[condition]['beg'])+"'") + text_need[0][0].upper() + text_need[0][1:-1] + text_need[0][-1] + f", {'а ' if randint(1, 10)%2 else ''}"
    text_need.pop(0)
    for t, i in zip(text_need, range(1, len(text_need)+1)):
        if i==len(text_need) and i>1:
            text+=text_ques[0:-1]+', если '+t+'?'
        elif i==len(text_need):
            text+=t+'. '+text_ques
        elif i%2==0:
            text+=t[0].upper()+t[1:-1]+t[-1]+f", {'а ' if randint(1, 10)%2 else ''}"
        else:
            text+=t+'. '


    return text, int(answer)
    # for varneed in need:
        # try:
        #     need.append(formsa[varneed])
        # except:
        #     exec(f"{varneed} = {randint(1, 5)}")
    # print(ques, need, form)

def geometric():
    def find_s(n):
        return a1*(d**n-1)/(d-1)
    def find_a(n):
        return a1*(d**(n-1))
    ques = choice(list(formsa))
    need = choice(formsa[ques])
    # need = form[0]
    # form = form[1]
    d = randint(2, 4)
    n = randint(3, 5)
    a1 = randint(1, 7) if n<5 else randint(1, 4)
    w = randints(-2, -1, 1, 2) if n<5 else (-1 if randint(0, 1) else 1)
    ques = ques.replace('n', str(n))
    try:
        answer = eval(ques)
    except NameError:
        answer = eval(f"find_{ques[0]}({eval(ques[1:-1]+ques[-1])})")
#     if randint(0, 1):
#         d = randint(2, 4)
#         a1 = randint(1, 10)
#         n = randint(4, 10)
#         w = randints(-3, -1, 1, 3)
#         ques = ques.replace('n', str(n))
#         try:
#             answer = eval(ques)
#         except NameError:
#             answer = eval(f"find_{ques[0]}({eval(ques[1:-1]+ques[-1])})")
#     else:
#         d = randint(2, 4)
#         n = randint(4, 10)
#         w = randints(-3, -1, 1, 3)
#         if True in ['w' in i for i in need]:
#             plmiw = -1 if True in ['-w' in i for i in need] else 1
#             if plmiw*sign(w)==1:
#                 exec(f"""a{n+abs(w)} = randint(1, 8)
# a1 = eval(f"a{n+abs(w)}")*(d**(n+abs(w)-1))""")
#             else:
#                 exec(f"""a{n} = randint(1, 8)""")
#                 a1 = eval(f"a{n}")*(d**(n-1))
#         else:
#             exec(f"""a{n} = randint(1, 8)""")
#             a1 = eval(f"a{n}")*(d**(n-1))
#         d = 1/d
#         try:
#             answer = eval(ques)
#         except NameError:
#             answer = eval(f"find_{ques[0]}({eval(ques[1:-1]+ques[-1])})")



    needs = {}
    shuffle(need)
    for v in need:
        try:
            if v!='w' and v!='n':
                needs[v] = eval(v)
        except NameError:
            needs[f"{v[0]}{eval(v[1:-1]+v[-1])}"] = int(eval(f"find_{v[0]}({eval(v[1:-1]+v[-1])})"))
    locals().update(needs)
    condition = choice(list(texts_condition_g))
    place = choice(places[condition])
    name = choice(places['names'])
    text_need = []
    for v in needs:
        try:
            text_need.append(eval("f'"+choice(texts_condition_g[condition][v])+"'"))
        except KeyError:
            text_need.append(eval("f'"+choice(texts_condition_g[condition][v[0]+'n']).replace('!n', str(v[1:-1]+v[-1]))+"'"))
    try:
        text_need.append(eval("f'"+choice(texts_question_g[condition][ques])+"'"))
    except KeyError as e:
        exec(f'{str(e)[1:-1]} = find_{str(e)[1]}({str(e)[2:-1]})')
        text_need.append(eval("f'"+choice(texts_question_g[condition][ques[0]+'n']).replace('!n', str(ques[1:-1]+ques[-1]))+"'"))
    except SyntaxError as e:
        text_need.append(eval("f'"+choice(texts_question_g[condition][ques[0]+'n']).replace('!n', str(ques[1:-1]+ques[-1]))+"'"))

    text_ques = text_need.pop(-1)
    text = eval("f'"+choice(texts_condition_a[condition]['beg'])+"'") + text_need[0][0].upper() + text_need[0][1:-1] + text_need[0][-1] + f", {'а ' if randint(1, 10)%2 else ''}"
    text_need.pop(0)
    for t, i in zip(text_need, range(1, len(text_need)+1)):
        if i==len(text_need) and i>1:
            text+=text_ques[0:-1]+', если '+t+'?'
        elif i==len(text_need):
            text+=t+'. '+text_ques
        elif i%2==0:
            text+=t[0].upper()+t[1:-1]+t[-1]+f", {'а ' if randint(1, 10)%2 else ''}"
        else:
            text+=t+'. '


    return text, int(answer)


TASKLIB = {'Арифметическая': arithmetic, 'Геометрическая': arithmetic}
TASKDES = {arithmetic: '', geometric: ''}

# import time
# beg = time.time()
# for i in range(1000):
#     print(f'{i+1}. ', *geometric())
# end = time.time()
# print(end-beg)



# formsa = {
# 'sn': [[['a1', 'an', 'n'], '(a1+an)*n/2']],
# 'an': [[['a1', 'd', 'n'], 'a1+(n-1)*d'], [['an-q', 'an+q'], '(an-q+an+q)/2'], [['an+q', 'd'], 'an+q-q*d'], [['an-q', 'd'], 'an-q+q*d']], 
# 'd': [[['an', 'a1', 'n'], '(an-a1)/(n-1)'], [['an+q', 'an', 'q'], '(an+q-an)/q'], [['an', 'an-q', 'q'], '(an-an-q)/q']], 
# 'a1': [[['sn', 'n', 'an'], 'sn*2/n-an'], [['an', 'n', 'd'], 'an-(n-1)*d']]
# }
    


# 'sn': [['a1', 'd'], ['a1', 'an'], ['an', 'an-w'], ['an', 'a1'], ['an', 'd'], ['an-w', 'a1']],
# 'an': [['a1', 'd'], ['an-w', 'an+w'], ['an+w', 'd'], ['a1', 'an+w']], 
# 'd': [['a1', 'an'], ['an+w', 'an']], 
# 'a1': [['sn', 'an'], ['an', 'd'], ['an', 'an+w']]


