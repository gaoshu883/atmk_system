from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from math_questions.models import Knowledge, Content, KnowledgeTag
from atmk_system.utils import response_success, response_error, collect
from django.forms.models import model_to_dict
from .const import CACHE_FILE_PICKLE

from .utils import clean_html, remove_same

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
        u['clean_text'], math_dict, math_text = clean_html(
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
    '''从数据库读取题目，清洗、去重、提取公式、分析后保存到文件'''
    query_set = Content.objects.all().values('text', 'id')
    temp = []
    for u in list(query_set):
        ret = {}
        ret['id'] = u['id']
        ret['text'], ret['formulas'], ret['math_text'] = clean_html(
            u['text'], u['id'])
        temp.append(ret)

    clean_list = remove_same(temp)
    # 分析数据
    label_set = set()
    for u in clean_list:
        query_set = KnowledgeTag.objects.filter(qid=u['id']).values('label_id')
        for query in list(query_set):
            label_set.add(query['label_id'])
    l_count = len(label_set)  # 知识点数量
    q_count = len(clean_list)  # 题目数量
    try:
        with open(CACHE_FILE_PICKLE, 'wb') as target_file:
            pickle.dump(clean_list, target_file)
    except:
        return response_error('clean error')
    return response_success(data={
        'file_name': CACHE_FILE_PICKLE,
        'updated_at': int(time.time()),
        'demo_data': clean_list[0],
        'analysis': {
            'q_count': q_count,
            'l_count': l_count
        }
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
            'analysis': {
                'q_count': count
            }
        })
    except:
        return response_success(data={})


@login_required
@require_POST
def content_ayalysis():
    return response_success(data={})
