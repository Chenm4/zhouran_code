'''prompt:Classify the text into neutral, negative, or positive'''
import os
import pandas as pd
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI()

def classify_text(prompt, text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"{prompt}\nText: {text}\nSentiment:\n"
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message['content'].strip()

def process_excel_files(excel_folder, prompt):
    for filename in os.listdir(excel_folder):
        if filename.endswith('.xlsx'):
            excel_path = os.path.join(excel_folder, filename)
            df = pd.read_excel(excel_path)

            sentiments = []
            for text in df.iloc[1:, 0]:  # 从第二行开始遍历第一列
                sentiment = classify_text(prompt, text)
                sentiments.append(sentiment)

            df['Sentiment'] = [''] + sentiments  # 第一行为空，后面是情感分析结果
            output_path = os.path.join(excel_folder, f"processed_{filename}")
            df.to_excel(output_path, index=False)
            print(f"Processed {filename} and saved to {output_path}")

if __name__ == '__main__':
    excel_folder = 'excel_folder_sentence'  # 替换为你的Excel文件夹路径
    prompt = "Classify the text into neutral, negative, or positive"
    process_excel_files(excel_folder, prompt)