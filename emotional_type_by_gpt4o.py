
import pandas as pd
import openai
import os
def call_gpt4(prompt, api_key, base_url):
    # 设置 API 密钥
    openai.api_key = api_key

    # 设置 API 基础URL
    openai.api_base = base_url

    try:
        # 调用 GPT-4o 模型
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            request_timeout=30  # 设置请求超时时间
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def process_excel_with_gpt4(input_excel, output_excel, prompt, api_key, base_url):
    # 读取输入的 Excel 文件
    df = pd.read_excel(input_excel)

    # 创建一个新的列用于存储 GPT-4o 的返回结果
    results = []

    # 遍历第一列的每个文本
    for text in df.iloc[:, 0]:# 这个 0 代表第 1 列
        full_prompt = f"{prompt} {text}"
        result = call_gpt4(full_prompt, api_key, base_url)
        print("text == ",text,"      result == ",result)
        results.append(result)# 储存gpt的返回结果

    # 将结果写入到第二列
    df['GPT-4o Response'] = results

    # 保存输出的 Excel 文件
    df.to_excel(output_excel, index=False)

    print(f"Processed {input_excel} and saved to {output_excel}")

# # 使用示例
# input_excel = 'input.xlsx'  # 替换为你的输入 Excel 文件路径
# output_excel = 'output.xlsx'  # 替换为你的输出 Excel 文件路径
# prompt = "You are an emotional expert.Classify the text into anger,disgust,fear,joy,neutral,sadness,surprise.Just choose to answer one of these three words and don't answer anything else: "
# api_key = "sk-gye4A9twoI4UdJO90b9153F8327541F981F0C3999309F9Fb"
#
# base_url = "https://www.gptapi.us/v1"
#
# process_excel_with_gpt4(input_excel, output_excel, prompt, api_key, base_url)




def process_all_excels_with_gpt4(excel_folder, output_folder, prompt, api_key, base_url):
    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历excel文件夹
    for filename in os.listdir(excel_folder):
        if filename.endswith('.xlsx'):
            input_excel = os.path.join(excel_folder, filename)
            output_excel = os.path.join(output_folder, filename)
            process_excel_with_gpt4(input_excel, output_excel, prompt, api_key, base_url)

if __name__ == '__main__':
    # 使用示例
    excel_folder = 'excel_emotion_output_sentence'  # 替换为你的输入 Excel 文件夹路径
    output_folder = 'excel_emotion_output_sentence_gpt4o'  # 替换为你的输出 Excel 文件夹路径
    prompt = "You are an emotional expert.Classify the text into anger,disgust,fear,joy,neutral,sadness,surprise.Just choose to answer one of these three words and don't answer anything else: "
    api_key = "sk-gye4A9twoI4UdJO90b9153F8327541F981F0C3999309F9Fb"
    base_url = "https://www.gptapi.us/v1"

    process_all_excels_with_gpt4(excel_folder, output_folder, prompt, api_key, base_url)