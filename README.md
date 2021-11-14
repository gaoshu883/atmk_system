# ATMK研究平台


## development

### 拉起服务

```bash
python manage.py runserver 9000
```

### 检测对模型文件的修改，并且把修改的部分储存为一次迁移
```bash
ython manage.py makemigrations math_questions
```
### 执行数据库迁移并同步管理数据库结构
```bash
python manage.py migrate
```