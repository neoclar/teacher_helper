from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))  # Для Windows путь может быть 'times.ttf'
pdfmetrics.registerFont(TTFont('Times-Bold', 'timesbd.ttf')) 

def generate(variants):
    styles = getSampleStyleSheet()
    
    # Стили с кириллическими шрифтами
    task_title_style = ParagraphStyle(
        'TaskTitle',
        parent=styles['Title'],
        fontSize=20,
        textColor=colors.HexColor('#1F497D'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Times-Bold'
    )
    variant_title_style = ParagraphStyle(
        'VariantTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#4F81BD'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Times-Bold'
    )
    task_text_style = ParagraphStyle(
        'TaskText',
        parent=styles['BodyText'],
        fontSize=12,
        textColor=colors.black,
        leading=14,
        spaceAfter=12,
        fontName='Times-Roman'
    )
    answer_title_style = ParagraphStyle(
        'AnswerTitle',
        parent=styles['Title'],
        fontSize=20,
        textColor=colors.HexColor('#C00000'),
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Times-Bold'
    )
    answer_text_style = ParagraphStyle(
        'AnswerText',
        parent=styles['BodyText'],
        fontSize=12,
        textColor=colors.black,
        leading=14,
        spaceAfter=12,
        fontName='Times-Roman'
    )
    # Создание буферов для PDF
    tasks_buffer = BytesIO()
    answers_buffer = BytesIO()

    doc_tasks = SimpleDocTemplate(tasks_buffer, pagesize=letter)
    doc_answers = SimpleDocTemplate(answers_buffer, pagesize=letter)

    tasks_elements = []
    answers_elements = []

    # Генерация tasks.pdf
    for variant_num, variant in enumerate(variants, 1):
        tasks_elements.append(Paragraph("ЗАДАНИЯ", task_title_style))
        tasks_elements.append(Paragraph(f"Вариант {variant_num}", variant_title_style))
        for task_num, task_tuple in enumerate(variant, 1):
            if len(task_tuple) == 2:
                task, answer = task_tuple
                description = None
            else:
                description, task, answer = task_tuple
            parts = [f'<b><font color="#1F497D">{task_num}.</font></b> ']
            if description:
                parts.append(f'<b><font color="#1F497D">{description}</font></b><br/>')
            parts.append(f'{task}<br/><b><font color="#1F497D">Ответ:</font></b> __________________')
            tasks_elements.append(Paragraph(''.join(parts), task_text_style))
        if variant_num < len(variants):
            tasks_elements.append(PageBreak())

    # Генерация answers.pdf
    for variant_num, variant in enumerate(variants, 1):
        answers_elements.append(Paragraph("ОТВЕТЫ", answer_title_style))
        answers_elements.append(Paragraph(f"Вариант {variant_num}", variant_title_style))
        for task_num, task_tuple in enumerate(variant, 1):
            answer = task_tuple[1] if len(task_tuple) == 2 else task_tuple[2]
            answer_line = f'<b><font color="#1F497D">{task_num}.</font></b> Ответ: {answer}'
            answers_elements.append(Paragraph(answer_line, answer_text_style))
        if variant_num < len(variants):
            answers_elements.append(PageBreak())

    # Построение документов
    doc_tasks.build(tasks_elements)
    doc_answers.build(answers_elements)

    return tasks_buffer.getvalue(), answers_buffer.getvalue()

# Пример использования
if __name__ == "__main__":
    example_variants = [
        [
            ('Решите уравнение:', '4x/15 - 2168/15 = (-11 - 321/4)8', '5/4'),
            ('Доктор посоветовал Наташе заняться спортом и каждый день увеличивать объем тренировки в 3 раз. Каждый следующий день количество отжимания увеличивается в 3 раз, в 5 день сделала 324 отжимания. Сколько отжиманий Наташа выполнила в 4 день?', 108)
        ]
    ]
    tasks_pdf, answers_pdf = generate(example_variants)
    # Для сохранения в файлы можно использовать:
    with open('tasks.pdf', 'wb') as f: f.write(tasks_pdf)
    with open('answers.pdf', 'wb') as f: f.write(answers_pdf)