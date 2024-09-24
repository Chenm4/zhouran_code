import os
import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize

''' 该代码文件实现了将指定文件夹中的所有txt文件按句子分割，并将结果保存到对应的Excel文件的第一列。'''

def spiltBySentence():
    # 下载punkt数据
    nltk.download('punkt')
    # 文件夹路径
    txt_folder = 'txt_folder'
    excel_folder = 'excel_folder_sentence'

    # 确保输出目录存在
    os.makedirs(excel_folder, exist_ok=True)

    # 遍历txt文件夹
    for filename in os.listdir(txt_folder):
        if filename.endswith('.txt'):
            txt_path = os.path.join(txt_folder, filename)

            # 读取txt文件
            with open(txt_path, 'r', encoding='utf-8') as file:
                text = file.read()

            # 分割为句子
            sentences = sent_tokenize(text)

            # 创建DataFrame
            df = pd.DataFrame(sentences, columns=['Sentences'])

            # 保存到Excel文件
            excel_filename = f"{os.path.splitext(filename)[0]}.xlsx"
            excel_path = os.path.join(excel_folder, excel_filename)
            df.to_excel(excel_path, index=False)

            print(f"Processed {filename} and saved to {excel_filename}")




if __name__ == '__main__':
    spiltBySentence()
