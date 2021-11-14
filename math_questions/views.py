from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from math_questions.models import Knowledge
from atmk_system.utils import response_success, response_error


def questions(request):
    return HttpResponse("获取列表数据")


@login_required
def labels(request):
    obj = Knowledge.objects.all().values('name', 'uuid', 'parent_uuid')
    return response_success(data=list(obj))
