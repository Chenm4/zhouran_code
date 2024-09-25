import os
import pandas as pd
from textblob import TextBlob


def emotion_type(excel_folder, excel_emotion_output):
    # 确保输出目录存在
    os.makedirs(excel_emotion_output, exist_ok=True)

    def classify_emotions(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        return polarity, subjectivity

    # 遍历excel文件夹
    for filename in os.listdir(excel_folder):
        if filename.endswith('.xlsx'):
            excel_path = os.path.join(excel_folder, filename)

            # 读取Excel文件
            df = pd.read_excel(excel_path)

            # 创建新的列用于存储情感分类、极性和主观性
            emotions = []
            scores = []
            subjectivities = []
            subjective_or_objective = []

            # 对第一列的每个文本进行情感分类
            for text in df.iloc[:, 0]:
                polarity, subjectivity = classify_emotions(text)
                if polarity > 0:
                    emotion = 'positive'
                elif polarity < 0:
                    emotion = 'negative'
                else:
                    emotion = 'neutral'

                # 主观性判断
                if subjectivity > 0.5:
                    sub_or_obj = 'subjective'
                else:
                    sub_or_obj = 'objective'

                emotions.append(emotion)
                scores.append(polarity)
                subjectivities.append(subjectivity)
                subjective_or_objective.append(sub_or_obj)

            # 添加到DataFrame
            df['Emotion'] = emotions
            df['Score'] = scores
            df['Subjectivity'] = subjectivities
            # 添加主观性或客观性判断
            df['Subjective_or_Objective'] = subjective_or_objective

            # 保存到新的Excel文件
            output_path = os.path.join(excel_emotion_output, filename)
            df.to_excel(output_path, index=False)

            print(f"Processed {filename} and saved to {output_path}")

if __name__ == '__main__':
    excel_folder = 'excel_folder_sentence'  # 替换为你的Excel文件夹路径
    excel_emotion_output = 'excel_emotion_output_sentence_textblob'
    emotion_type(excel_folder, excel_emotion_output)

    excel_folder = 'excel_folder_paragraph'  # 替换为你的Excel文件夹路径
    excel_emotion_output = 'excel_emotion_output_paragraph_textblob'
    emotion_type(excel_folder, excel_emotion_output)
