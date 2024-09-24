import os
import pandas as pd
'''该代码文件实现了将指定文件夹中的所有txt文件按段落分割，并将结果保存到对应的Excel文件的第一列。'''

def spiltByParagraph():
    # 文件夹路径
    txt_folder = 'txt_folder'
    excel_folder_paragraph = 'excel_folder_paragraph'

    # 确保输出目录存在
    os.makedirs(excel_folder_paragraph, exist_ok=True)

    # 遍历txt文件夹
    for filename in os.listdir(txt_folder):
        if filename.endswith('.txt'):
            txt_path = os.path.join(txt_folder, filename)

            # 读取txt文件
            with open(txt_path, 'r', encoding='utf-8') as file:
                text = file.read()

            # 分割为段落（假设段落以两个换行符隔开）
            paragraphs = [para.strip() for para in text.split('\n') if para.strip()]

            # 创建DataFrame
            df = pd.DataFrame(paragraphs, columns=['Paragraphs'])

            # 保存到Excel文件
            excel_filename = f"{os.path.splitext(filename)[0]}.xlsx"
            excel_path = os.path.join(excel_folder_paragraph, excel_filename)
            df.to_excel(excel_path, index=False)

            print(f"Processed {filename} and saved to {excel_filename}")


if __name__ == '__main__':
    spiltByParagraph()
