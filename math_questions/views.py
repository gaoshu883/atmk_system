from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from math_questions.models import Knowledge, Content, KnowledgeTag
from atmk_system.utils import response_success, response_error, collect
from django.forms.models import model_to_dict
import json
import time


def questions(request):
    page = int(request.GET.get('page', default='1'))
    size = int(request.GET.get('size', default='0'))
    data, count = collect(Content, page=page, size=size)
    for u in data:
        query_set = KnowledgeTag.objects.filter(qid=u['id'])
        ret = []
        for query in query_set:
            temp = model_to_dict(query)
            ret.append(temp['label_id'])
        u['labels'] = ret
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
