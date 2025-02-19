import random
from random import randint, sample, choice
from math import gcd

small_alphabet_10 = "ABCDEFGHIJ"
def convert_to_decimal(number: str, base: int) -> int:
    number = number.replace(f"({base})", "")
    result = 0
    for i,a in zip(range(len(number)),number[::-1]):
        result+=int(a)*(base**i)
    return result
def generate_template(difficulty):
    max_len = 5
    def generate_number():
        number = ""
        x_positions = sample(range(0,max_len-1),randint(1,2))
        for i in range(randint(4,max_len)):
            number+="x" if i in x_positions else choice(small_alphabet_10)
        return number
    while True:
        operations = [' + ', ' - ', ' * ']
        q = randint(37 if difficulty else 11, 62 if difficulty else 36)
        answer = randint(1,9)
        template = generate_number()+f"({q})"
        non_null = {template[0]}
        if not randint(0, 3):
            operation = choice(operations)
            template+=operation
            number = generate_number()+f"({q})"
            non_null.add(number[0])
            template+=number
        operations.pop(-1)
        template+=choice(operations)
        for a in small_alphabet_10:
            template = template.replace(a, str(randint(1 if a in non_null else 0, 9)))
        template_split = template.split(" ")
        result=convert_to_decimal(template_split[0].replace("x", str(answer)), q)
        for n in range(2, len(template_split)-1, 2):
            if template_split[n-1] == "+":
                result+=convert_to_decimal(template_split[n].replace("x", str(answer)), q)
            elif template_split[n-1] == "-":
                result-=convert_to_decimal(template_split[n].replace("x", str(answer)), q)
            elif template_split[n-1] == "*":
                result*=convert_to_decimal(template_split[n].replace("x", str(answer)), q)
        last_number = str(randint(1,9))+"".join(map(str,sample(range(0, 9),randint(3, max_len-1))))
        grow = 1 if int(last_number[0])<5 else 0
        last_number = int(last_number)
        c=0
        while (abs((result+convert_to_decimal(str(last_number),q)) if template_split[-2]=="+" else (result-convert_to_decimal(str(last_number),q)))%(q-1)!=0) or str(answer) not in str(last_number):
            last_number+=1 if grow else -1
            c+=1
            if c==400:
                break
        else:
            
            template+=str(last_number).replace(str(answer), "x")+f"({q})"
            return template



def type1(difficulty):
    template = generate_template(difficulty)
    find_min = randint(0, 1)
    template_split = template.split(" ")
    q=int(template_split[0].split("(")[1][:-1])
    for x in range(1 if find_min else 9, 10 if find_min else 0, 1 if find_min else -1):
        result=convert_to_decimal(template_split[0].replace("x", str(x)), q)
        for n in range(2, len(template_split), 2):
            if template_split[n-1] == "+":
                result+=convert_to_decimal(template_split[n].replace("x", str(x)), q)
            elif template_split[n-1] == "-":
                result-=convert_to_decimal(template_split[n].replace("x", str(x)), q)
            elif template_split[n-1] == "*":
                result*=convert_to_decimal(template_split[n].replace("x", str(x)), q)
        if not abs(result)%(q-1):
            break
    task = f'В выражении {template.replace("(", "<sub>").replace(")", "</sub>")} x — цифра системы счисления с основанием {q}. '
    task += f'Определите {"наименьшее" if find_min else "наибольшее"} значение x, при котором выражение кратно {q-1}. '
    task += f'Запишите частное от деления на {q-1} в десятичной системе.'
    
    return task, result//(q-1)
