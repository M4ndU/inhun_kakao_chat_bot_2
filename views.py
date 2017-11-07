from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytz import timezone
import datetime , json
import sys
sys.path.insert(0, "/home/mandu/project/discord_bot/")
#sys.path.insert(0, "inhun_discord_bot 경로")
from scrapture import *
from datematch import *
#


#api info
api_info = ""
api_info += '[인헌고 알리미 정보]\n'
api_info += '급식을 알려드립니다.\n'
api_info += '2017년 11월 2일 V1.0.0\n'
api_info += '개발자 : 인헌고등학교 10810 성민규\n'
api_info += '자율동아리 WH0a 부장\n'
api_info += '후원 받습니다'

def lunch(l_date):
    l_date = lunch_match(l_date)
    if (lunch != 0 and dinner != 0):
        ll_diet = ""
        ll_diet = get_diet(l_date)
    else:
        ll_diet = "급식 정보가 없습니다."
    return ll_diet

def dinner(d_date):
    d_date = dinner_match(d_date)
    if (lunch != 0 and dinner != 0):
        dd_diet = ""
        dd_diet = get_diet(d_date)
    else:
        dd_diet = ":("
    return dd_diet

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
    local_date1 = dt1.strftime("%m%d")
    local_date2 = dt2.strftime("%m%d")

    if datacontent == '오늘 급식':
        meal_date = int(local_date1)
        l_l = lunch(meal_date)
        d_d = dinner(meal_date)
        return JsonResponse({
                'message': {
                    'text': l_l + "\n\n" + d_d
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['오늘 급식','내일 급식','API 정보']
                }

            })
    elif datacontent == '내일 급식':
        meal_date = int(local_date2)
        l_l = lunch(meal_date)
        d_d = dinner(meal_date)
        return JsonResponse({
                'message': {
                    'text': l_l + "\n\n" + d_d
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
