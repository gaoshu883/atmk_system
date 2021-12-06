from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from math_questions.models import Knowledge, Content, KnowledgeTag
from atmk_system.utils import response_success, response_error, collect
from django.forms.models import model_to_dict
from .const import CACHE_FILE_PICKLE, CACHE_FINAL_PICKLE

from .utils import clean_html, remove_same

from MathByte.embeddings import Embeddings


import json
import time
import pickle
import os
import random


@login_required
@require_POST
def questions(request):
    data = json.loads(request.body)
    page = data.get('page')
    size = data.get('size')
    cond = data.get('cond')
    data, count = collect(Content, page=page, size=size, conditions=cond)
    for u in data:
        query_set = KnowledgeTag.objects.filter(qid=u['id'])
        ret = []
        for query in query_set:
            temp = model_to_dict(query)
            ret.append(temp['label_id'])
        u['labels'] = ret
        u['clean_text'], a, b, c, d = clean_html(
            u['text'], u['id'])
    return response_success(data={
        'data': data,
        'count': count
    })


@login_required
def labels(request):
    data, count = collect(Knowledge)
    return response_success(data=data)


@login_required
@require_POST
def tag(request):
    data = json.loads(request.body)
    qid = data.get('id')
    labels = data.get('labels')
    query_set = KnowledgeTag.objects.filter(qid=qid).values('label_id')
    label_ids = []
    for query in list(query_set):
        id = query['label_id']
        label_ids.append(id)
        if id not in labels:
            label = KnowledgeTag.objects.get(qid=qid, label_id=id)
            label.delete()
    for id in labels:
        if id not in label_ids:
            KnowledgeTag.objects.create(qid=qid, label_id=id)
        else:
            label = KnowledgeTag.objects.get(qid=qid, label_id=id)
            label.updated_at = int(time.time())
            label.save()
    return response_success(data={})


@login_required
@require_POST
def clean(request):
    '''
    从数据库读取题目，清洗、去重、提取公式、分析后保存到文件
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
    '''
    query_set = Content.objects.all().values('text', 'id')
    temp = []
    for u in list(query_set):
        ret = {}
        qid = u['id']
        label_list = []
        label_set = KnowledgeTag.objects.filter(
            qid=qid).values('label_id').distinct()
        for query in list(label_set):
            label_list.append(query['label_id'])
        # 排除无标签数据
        if label_list:
            ret['id'] = qid
            ret['label_list'] = label_list
            ret['text'], ret['formulas'], ret['math_text'], \
                ret['char_list'], ret['word_list'] = clean_html(
                u['text'], qid)
            temp.append(ret)

    clean_list = remove_same(temp)

    try:
        with open(CACHE_FILE_PICKLE, 'wb') as target_file:
            pickle.dump(clean_list, target_file)
    except:
        return response_error('clean error')
    return response_success(data={
        'file_name': CACHE_FILE_PICKLE,
        'updated_at': int(time.time()),
        'demo_data': clean_list[0],
    })


@login_required
def cleaned_data(request):
    try:
        updated_at = os.path.getmtime(CACHE_FILE_PICKLE)
        with open(CACHE_FILE_PICKLE, 'rb') as data_f_pickle:
            temp = pickle.load(data_f_pickle)
            count = len(temp)
            idx = random.randint(0, count - 1)
        return response_success(data={
            'file_name': CACHE_FILE_PICKLE,
            'updated_at': int(updated_at),
            'demo_data': temp[idx],
        })
    except:
        return response_success(data={})


@login_required
def data_summary(request):
    # 分析平衡后的数据
    try:
        with open(CACHE_FILE_PICKLE, 'rb') as data_f_pickle:
            questions = pickle.load(data_f_pickle)
            MAX_INT = 100000

            total_char = 0
            min_char = MAX_INT
            max_char = 0
            avg_char = 0
            total_word = 0
            min_word = MAX_INT
            max_word = 0
            avg_word = 0
            total_formula = 0
            min_formula = MAX_INT
            max_formula = 0
            avg_formula = 0
            total_label = 0
            min_label = MAX_INT
            max_label = 0
            avg_label = 0
            label_set = set()
            for u in questions:
                char_list_len = len(u['char_list'])
                total_char += char_list_len
                min_char = min(char_list_len, min_char)
                max_char = max(char_list_len, max_char)
                word_list_len = len(u['word_list'])
                total_word += word_list_len
                min_word = min(word_list_len, min_word)
                max_word = max(word_list_len, max_word)
                formula_len = len(u['formulas'])
                total_formula += formula_len
                min_formula = min(formula_len, min_formula)
                max_formula = max(formula_len, max_formula)
                label_len = len(u['label_list'])
                total_label += label_len
                min_label = min(label_len, min_label)
                max_label = max(label_len, max_label)
                # 用于统计不重复label数
                label_set.update(u['label_list'])

            l_count = len(label_set)
            q_count = len(questions)
            avg_char = round(total_char / q_count, 2)
            avg_word = round(total_word / q_count, 2)
            avg_formula = round(total_formula / q_count, 2)
            avg_label = round(total_label / q_count, 2)

            ret = {}
            total_tag = 0
            min_tag = MAX_INT
            max_tag = 0
            avg_tag = 0
            for label_id in label_set:
                query_set = KnowledgeTag.objects.filter(
                    label_id=label_id).values('qid').distinct()
                tag_len = len(list(query_set))
                ret[str(label_id)] = tag_len
                total_tag += tag_len
                min_tag = min(tag_len, min_tag)
                max_tag = max(tag_len, max_tag)
            avg_tag = round(total_tag / l_count, 2)

        return response_success(data={
            'question': {
                'count': q_count,  # 题目数量
                'min_char': min_char,  # 最小字符数
                'max_char': max_char,  # 最大字符数
                'avg_char': avg_char,  # 平均字符数
                'min_word': min_word,  # 最小词数
                'max_word': max_word,  # 最大词数
                'avg_word': avg_word,  # 平均词数
                'min_formula': min_formula,  # 最小公式数
                'max_formula': max_formula,  # 最大公式数
                'avg_formula': avg_formula,  # 平均公式数
                'min_label': min_label,  # 最小标签数
                'max_label': max_label,  # 最大标签数
                'avg_label': avg_label,  # 平均标签数
            },
            'label': {
                'count': l_count,  # 标签数
                'min_tag': min_tag,  # 标记最小数
                'max_tag': max_tag,  # 标记最大数
                'avg_tag': avg_tag,  # 平均标记数
            },
            'label_tags': ret  # 每个标签对应的标记数
        })
    except Exception as e:
        print(e)
        return response_success(data={})


@login_required
@require_POST
def read_vector(request):
    '''
    读取字、数学公式向量
    '''
    data = json.loads(request.body)
    type_id = data.get('type')
    result = {}
    system = Embeddings()
    if type_id == 'char':
        char_list = ''.join(data.get('value').split())  # 按字切分
        for char in char_list:
            result[char] = system.read_char_vec(query_char=char).tolist()
    elif type_id == 'formula':
        query_formula = data.get('value')
        result[data.get('key')] = system.read_formula_vec(
            query_formula=query_formula).tolist()
    else:
        pass

    return response_success(data=result)
