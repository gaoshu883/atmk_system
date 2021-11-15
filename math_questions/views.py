from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from math_questions.models import Knowledge, Content
from atmk_system.utils import response_success, response_error, collect


def questions(request):
    page = int(request.GET.get('page', default='1'))
    size = int(request.GET.get('size', default='0'))
    data, count = collect(Content, page=page, size=size)
    return response_success(data={
        'data': data,
        'count': count
    })


@login_required
def labels(request):
    data, count = collect(Knowledge)
    return response_success(data=data)
