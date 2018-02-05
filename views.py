from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytz import timezone
import datetime , json
import sys
sys.path.insert(0, "inhun_discord_chat_bot_2 경로")
from web3 import *


#api info
api_info =(
            '[인헌고 알리미 정보]\n'
            '개발자 : '
            )


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

    #date
    dt1 = datetime.datetime.today()
    dt2 = datetime.datetime.today() + datetime.timedelta(days=1)
    local_date1 = dt1.strftime("%Y.%m.%d")
    local_date2 = dt2.strftime("%Y.%m.%d")
    local_weekday1 = dt1.weekday()
    local_weekday2 = dt2.weekday()

    print(datacontent)

    if datacontent == '오늘 급식':
        meal_date = str(local_date1)
        l_wkday = int(local_weekday1)
        l_l = get_diet(2, meal_date, l_wkday)
        d_d = get_diet(3, meal_date, l_wkday)

        if len(l_l) == 1:
            lunch = "급식이 없습니다."
            dinner = ""
        elif len(d_d) == 1:
            lunch = meal_date + " 중식\n" + l_l
            dinner = ""
        else:
            lunch = meal_date + " 중식\n" + l_l
            dinner = meal_date + " 석식\n" + d_d

        return JsonResponse({
                'message': {
                    'text': lunch + dinner
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['오늘 급식','내일 급식','API 정보']
                }

            })
    elif datacontent == '내일 급식':
        meal_date = str(local_date2)
        l_wkday = int(local_weekday2)
        l_l = get_diet(2, meal_date, l_wkday)
        d_d = get_diet(3, meal_date, l_wkday)

        if len(l_l) == 1:
            lunch = "급식이 없습니다."
            dinner = ""
        elif len(d_d) == 1:
            lunch = meal_date + " 중식\n" + l_l
            dinner = ""
        else:
            lunch = meal_date + " 중식\n" + l_l
            dinner = meal_date + " 석식\n" + d_d

        return JsonResponse({
                'message': {
                    'text': lunch + dinner
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['오늘 급식','내일 급식','API 정보']
                }

            })
    elif datacontent == 'API 정보':
        return JsonResponse({
                'message': {
                    'text': api_info
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['오늘 급식','내일 급식','API 정보']
                }


            })
