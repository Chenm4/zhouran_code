from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig

# 模型名
model_name = 'cardiffnlp/twitter-roberta-base-sentiment'

# 下载模型文件
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
config = AutoConfig.from_pretrained(model_name)

# 保存模型和tokenizer
output_dir = './offline_model'
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
config.save_pretrained(output_dir)
