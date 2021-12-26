# ATMK研究平台


## Web服务

### 拉起服务

```bash
python manage.py runserver 9000 # 后台服务
cd frontend
npm run serve # 前端开发服务
```

### 检测对模型文件的修改，并且把修改的部分储存为一次迁移
```bash
python manage.py makemigrations math_questions
```
### 执行数据库迁移并同步管理数据库结构
```bash
python manage.py migrate
```

## 数据清洗

详见【ATMK研究平台-数据清洗】页面

保存的原始数据格式：

数据文件：`file_data\math_questions_content.pkl`

```json
    [
        {
            "id": 1,
            "text":"题目HEL_45293_WLDOR_1_OL文本",
            "math_text": "题目文本 with formulas",
            "char_formula_list": [],
            "word_list": [],
            "word_formula_list": [],
            "label_list": [],
            "formulas": {
                "HEL_45293_WLDOR_1_OL": "mathML"
            }
        }
    ]

```

## 公式学习

```bash
cd formula_embedding
python train_model.py
```

公式学习时待处理数据的数据格式：

```json
    [
        {
            "content": "<math></math>",
            "key": "HEL_45293_WLDOR_1_OL"
        }
    ]

```

## 数据预处理

可视化操作见【ATMK研究平台-模型训练】页面，代码实现见： `MathByte\preprocess.py`

数据文件：`file_data\math_data.h5` 和 `file_data\vocab_label.pkl` 和 `file_data\embeddings.pkl`


## 分类模型训练

```bash
cd MathByte
python main.py -h # 查看命令参数
python main.py
```

## 鸣谢
+ [TangentCFT](https://github.com/BehroozMansouri/TangentCFT)
+ [Embedding/Chinese-Word-Vectors](https://github.com/Embedding/Chinese-Word-Vectors)
+ [brightmart/text_classification](https://github.com/brightmart/text_classification)
