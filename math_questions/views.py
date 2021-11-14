from django.http import HttpResponse, JsonResponse


def questions(request):
    return HttpResponse("获取列表数据")


def labels(request):
    return JsonResponse({'status': 0, 'url': ''})
