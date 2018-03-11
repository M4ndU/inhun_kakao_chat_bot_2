from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytz import timezone
import datetime , json
import sys
sys.path.insert(0, "inhun_discord_chat_bot_2 경로")
from parser import *

api_info = '__인헌고 알리미 정보__\n개발자 : '
_else = "[*]현재 챗봇과 연결되어 있습니다.\n 상담을 원하시면 '상담원로 전환하기' 버튼을 누르시고 메세지를 보내주세요."

def get_meal(dt):

    local_date = dt.strftime("%Y.%m.%d")
    local_weekday = dt.weekday()

    l_l = get_diet(2, local_date, local_weekday)

    if len(l_l) == 1:
        lunch = "급식이 없습니다."
        return lunch

    else:
        d_d = get_diet(3, local_date, local_weekday)
        if len(d_d) == 1:
            lunch = local_date + " 중식\n" + l_l
            dinner = ""
        else:
            lunch = local_date + " 중식\n" + l_l
            dinner = local_date + " 석식\n" + d_d

    return lunch + dinner



def ret_proc(output):
    return JsonResponse({
            'message': {
                'text': output
            },
            'keyboard': {
                'type':'buttons',
                'buttons':['오늘 급식','내일 급식','여름 방학','API 정보']
            }
        })


def keyboard(request):

    return JsonResponse({
        'type':'buttons',
        'buttons':['오늘 급식','내일 급식','여름 방학','API 정보']
    })

@csrf_exempt
def answer(request):

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']

    print(datacontent)

    if datacontent == '오늘 급식':
        dt = datetime.datetime.today()
        diet = get_meal(dt)
        return ret_proc(diet)

    elif datacontent == '내일 급식':
        dt = datetime.datetime.today() + datetime.timedelta(days=1)
        diet = get_meal(dt)
        return ret_proc(diet)

    elif datacontent == '여름 방학':
        td = datetime.date.today()
        sd = datetime.date(2018, 7, 20)

        delta = sd - td
        int(delta.days)
        dday = "[-]개학식까지 %d일 남았습니다." % (delta.days)
        return ret_proc(dday)

    elif datacontent == 'API 정보':
        return ret_proc(api_info)

    else:
        return ret_proc(_else)
