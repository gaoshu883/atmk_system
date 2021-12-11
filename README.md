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

保存的数据格式：

```json
    [
        {
            "id": 1,
            "text":"题目文本",
            "math_text": "题目文本 with formulas",
            "char_list": [],
            "word_list": [],
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

## 鸣谢
+ [TangentCFT](https://github.com/BehroozMansouri/TangentCFT)
+ [Embedding/Chinese-Word-Vectors](https://github.com/Embedding/Chinese-Word-Vectors)
