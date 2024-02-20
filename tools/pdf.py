import jinja2
import pdfkit
import os
# os.chdir('..')
def create(context, folder_to_save, file_template):

    # template_loader = jinja2.FileSystemLoader('./')
    # template_env = jinja2.Environment(loader=template_loader)

    # template = template_env.get_template('task.html')
    # output_text = template.render(context)

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template(file_template)
    output_text = template.render(context)
    # print(output_text)
    # print(output_text)
    # C:\Users\HP\Desktop\phyton\Lib 1132
                    # import codecs
                    # with codecs.open('pdf_generated.pdf', 'rb') as f:
                    #     print(f.read())
    try:
        file_num = os.listdir(folder_to_save)[-1][3:-4]
    except IndexError: file_num = '0'
    # /home/user/Документы/folder/wkhtmltox/bin/wkhtmltopdf
    # config = pdfkit.configuration(wkhtmltopdf='/home/user/Документы/folder/wkhtmltox/bin/wkhtmltopdf') # C:\Program Files\wkhtmltopdf\bin 
    config = pdfkit.configuration(wkhtmltopdf='D:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe') # C:\Program Files\wkhtmltopdf\bin 
    # pdfkit.from_string(output_text, output_path=f'{folder_to_save}/gen{int(file_num)+1}.pdf', configuration=config, css='files/templates/math.css')
    pdfkit.from_string(output_text, output_path=f'{folder_to_save}\\gen{int(file_num)+1}.pdf', configuration=config, css='files\\templates\\math.css')
    # return f'{folder_to_save}/gen{int(file_num)+1}.pdf'
    return f'{folder_to_save}\\gen{int(file_num)+1}.pdf'
    # pdfkit.pdfkit.io.

# def separate(text):
#     text = text.split('=')
#     # text = text.replace(' ', '')
#     # # text = text.split('/')
#     # # (?<![)(]),(?![)(])    (?<!\(.)\/(?!.\))
#     # print(re.split('(?<!\(.)\/(?!.\))', text))
#     # print(text)
#     # print(list(csv.reader(text, delimiter='/')))



#     data = []
#     lines = ['Название;"Дат;а";Человек;', 'Грив;22,14;"Пе;тя"']

#     for line in lines:
#         result = re.findall(r'(".+?"|[^;]+)', line)
#         result = [re.sub(r'"(.+)"', r'\1', x) for x in result]
#         data.append(result) # посмотрите какой вывод при использовании функции append
#     print(data)
#     separate_text = ''
    # for sep, i in zip(text, range(len(text))):
        # if i:
        #     separate_text += f'''
        #     <p style="padding-left: 25px;">
        #         7&nbsp;
        #         <span class="frac">
        #             <sup>42</sup>
        #             <span>/</span>
        #             <sub>73</sub>
        #         </span>
        #     </p>'''
        # else:
        #     separate_text += f'''
        #     <p>{sep}</p>'''
        # separate_text = f'''{separate_text}
        # <p>{sep if i else ''}</p>
        # <p style="padding-left: 25px;">
        #     7&nbsp;
        #     <span class="frac">
        #         <sup>42</sup>
        #         <span>/</span>
        #         <sub>73</sub>
        #     </span>
        # </p>'''








#     return separate_text

# print(separate('(11*X/8)+44'))


# import re

# my_str = r"a/b/c/(test1/2/3)/g/h/test(2/4/6)"

# print(re.split('(?<!\(.)\/(?!.\))', my_str))

# import re

# data = []
# lines = ['Название;"Дат;а";Человек;', 'Грив;22,14;"Пе;тя"']

# for line in lines:
#     result = re.findall(r'(".+?"|[^;]+)', line)
#     result = [re.sub(r'"(.+)"', r'\1', x) for x in result]
#     data.append(result) # посмотрите какой вывод при использовании функции append

# print(data) # [['Название', 'Дат;а', 'Человек'], ['Грив', '22,14', 'Пе;тя']]