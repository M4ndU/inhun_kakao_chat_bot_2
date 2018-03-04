from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytz import timezone
import datetime , json
import sys
sys.path.insert(0, "inhun_discord_chat_bot_2 경로")
from parser import *


#api info
api_info =(
            '[인헌고 알리미 정보]\n'
            '개발자 : '
            )


def get_meal(dt):

    local_date = dt.strftime("%Y.%m.%d")
    local_weekday = dt.weekday()
    
    l_l = get_diet(2, local_date, local_weekday)

    if len(l_l) == 1:
        lunch = "급식이 없습니다."
        return lunch

    else:
        d_d = get_diet(3, local_date, local_weekday)
        print('hi5')
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
                'buttons':['오늘 급식','내일 급식','API 정보']
            }
        })


def keyboard(request):

    return JsonResponse({
        'type':'buttons',
        'buttons':['오늘 급식','내일 급식','API 정보']
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

    elif datacontent == 'API 정보':
        return ret_proc(api_info)
