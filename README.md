# ATMK研究平台


## development

### 拉起服务

```bash
python manage.py runserver 9000
```

### 检测对模型文件的修改，并且把修改的部分储存为一次迁移
```bash
python manage.py makemigrations math_questions
```
### 执行数据库迁移并同步管理数据库结构
```bash
python manage.py migrate
```

### 数据清洗
+ 所有的空字符，包括空格、换行(\n)、制表符(\t)等
+ 题号、选项序号：1、(1)、A、
+ 用于显示答案位置的括号（）
+ 一些标签：table、input、img、.exam-foot

```bash
cd math_questions
python clean_data.py
```

### 公式学习

```bash
cd formula_embedding
python train_model.py
```

公式学习时待处理数据的数据结构：

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
