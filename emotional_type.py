import os
import pandas as pd
from transformers import pipeline

# 加载情感分析模型
classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base',
                      return_all_scores=True)
def emotion_type(excel_folder, excel_emotion_output):
    # 确保输出目录存在
    os.makedirs(excel_emotion_output, exist_ok=True)
    def classify_emotions(text):
        results = classifier(text)
        return results[0]

    # 遍历excel文件夹
    for filename in os.listdir(excel_folder):
        if filename.endswith('.xlsx'):
            excel_path = os.path.join(excel_folder, filename)

            # 读取Excel文件
            df = pd.read_excel(excel_path)

            # 创建新的列用于存储情感分类和极性
            emotions = []
            scores = []

            # 对第一列的每个文本进行情感分类
            for text in df.iloc[:, 0]:
                result = classify_emotions(text)
                # 找分数最大的情感标签
                emotion = max(result, key=lambda x: x['score'])
                emotions.append(emotion['label'])
                scores.append(emotion['score'])

            # 添加到DataFrame
            df['Emotion'] = emotions
            df['Score'] = scores

            # 保存到新的Excel文件
            output_path = os.path.join(excel_emotion_output, filename)
            df.to_excel(output_path, index=False)

            print(f"Processed {filename} and saved to {output_path}")

if __name__ == '__main__':
    excel_folder = 'excel_folder_sentence'  # 替换为你的Excel文件夹路径
    excel_emotion_output = 'excel_emotion_output_sentence'
    emotion_type(excel_folder, excel_emotion_output)

    excel_folder = 'excel_folder_paragraph'  # 替换为你的Excel文件夹路径
    excel_emotion_output = 'excel_emotion_output_paragraph'
    emotion_type(excel_folder, excel_emotion_output)