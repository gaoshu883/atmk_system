from typing import Union
from django.http import JsonResponse


def response_success(data: Union[dict, str], msg: str = "") -> JsonResponse:
    return JsonResponse({"status": 1, "msg": msg, "data": data})


def response_error(error_msg: str = "") -> JsonResponse:
    return JsonResponse({"status": 0, "msg": error_msg})
