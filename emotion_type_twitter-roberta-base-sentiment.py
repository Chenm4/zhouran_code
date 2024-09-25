import os
import pandas as pd
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

# 本地模型地址
model_path = 'models/twitter-roberta-base-sentiment'

# 加载本地模型
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# 标签映射
label_mapping = {
    'LABEL_0': 'negative',
    'LABEL_1': 'neutral',
    'LABEL_2': 'positive'
}

def emotion_type(excel_folder, excel_emotion_output):
    # 确保输出目录存在
    os.makedirs(excel_emotion_output, exist_ok=True)

    def classify_emotions(text):
        results = classifier(text)
        # 只有一个最可能的结果
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
            subjectivities = []
            subjective_or_objective = []

            # 对第一列的每个文本进行情感分类
            for text in df.iloc[:, 0]:
                result = classify_emotions(text)
                emotion = label_mapping[result['label']]
                score = result['score']

                # 对于主观性，你可以使用一个简单的规则：
                # 如果情感强烈（score高），那么主观性也会高
                if score > 0.5:
                    sub_or_obj = 'subjective'
                else:
                    sub_or_obj = 'objective'

                emotions.append(emotion)
                scores.append(score)
                subjectivities.append(score)  # 这里假设score高表示更主观
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
    excel_emotion_output = 'excel_emotion_output_sentence_twitter-roberta-base-sentiment'
    emotion_type(excel_folder, excel_emotion_output)

    excel_folder = 'excel_folder_paragraph'  # 替换为你的Excel文件夹路径
    excel_emotion_output = 'excel_emotion_output_paragraph_twitter-roberta-base-sentiment'
    emotion_type(excel_folder, excel_emotion_output)
