import random

def decimal_to_base(n, base):
    """Преобразует десятичное число в строку в заданной системе счисления."""
    if n < 0 or base < 2 or base > 36:
        return ''
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if n == 0:
        return '0'
    digits = []
    while n > 0:
        digits.append(alphabet[n % base])
        n = n // base
    return ''.join(reversed(digits))

def convertions(difficulty=1):
    """Генерирует задачу и ответ для перевода между системами счисления."""
    # Выбираем диапазон чисел
    num = random.randint(10, 255) if difficulty in (1, 2) else random.randint(100, 5000)
    
    # Определяем системы счисления
    if difficulty == 1:
        if random.choice([True, False]):
            src, dst = 10, random.choice([2, 8, 16])
        else:
            src, dst = random.choice([2, 8, 16]), 10
            
    elif difficulty == 2:
        src, dst = random.sample([2, 8, 16], 2)
        
    elif difficulty == 3:
        other_bases = [b for b in range(3, 37) if b not in {2, 8, 10, 16}]
        if random.choice([True, False]):
            src, dst = 10, random.choice(other_bases)
        else:
            src, dst = random.choice(other_bases), 10
            
    elif difficulty == 4:
        other_bases = [b for b in range(3, 37) if b not in {2, 8, 10, 16}]
        src, dst = random.sample(other_bases, 2)
        
    else:
        raise ValueError("Допустимые уровни сложности: 1-4")

    # Генерируем представления чисел
    src_str = decimal_to_base(num, src)
    answer = decimal_to_base(num, dst).upper()
    
    # Форматируем вопрос
    if dst == 10:
        question = f"Переведите число {src_str}<sub>{src}</sub> в десятичную систему счисления"
    else:
        question = f"Переведите число {src_str}<sub>{src}</sub> в систему счисления с основанием {dst}"
        
    return question, answer
