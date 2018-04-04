from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytz import timezone
import datetime , json, sys
sys.path.insert(0, "inhun_discord_chat_bot_2 경로")
from parser import *

api_info = '__인헌고 알리미 정보__\n개발자 : '
_else = "[*]현재 챗봇과 연결되어 있습니다.\n 상담을 원하시면 '상담원로 전환하기' 버튼을 누르시고 메세지를 보내주세요."
PlzStopIt = "[*]연속동일요청입니다. 나중에 다시 시도해주세요."

#2018.04.04 추가
#동일 유저에 대해 연속동일요청 방지를 구현한 코드
#동일 유저가 연속으로 동일한 요청을 하였을 경우 작업을 진행하지 않고, 메세지 전송
#같은 함수에 대해 다른 유저의 요청이 있을 때까지 기다려야 하는 구조
#진행시간이 비교적 긴 함수(카카오톡에서는 버튼)에만 적용
#user_key값을 사용함 / 함수 각각에 적용하기 위해 class 사용
#프로그램을 재실행 할 경우 pre_key값 초기화.
class user_chk():

    def __init__(self):
        self.pre_key = "" #이전 user_key값
        self.now_key = "" #현재 user_key값

    def check(self, key):
        self.now_key = key # now_key값에 현재 user_key값 대입

        if self.pre_key == self.now_key : # 비교 하여 같으면 1을 반환
            passcode = 1
        else :
            self.pre_key = self.now_key # 다를 경우 pre_key값에 now_key값을 덮어쓰고 0 반환
            passcode = 0
        return passcode

#필요한 개수만큼 생성해둠.
u0 = user_chk()
u1 = user_chk()
u2 = user_chk()
u3 = user_chk()
u4 = user_chk()


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
            lunch = local_date + " 중식\n" + l_l + "\n"
            dinner = local_date + " 석식\n" + d_d

    return lunch + dinner

def ret_proc(output):
    return JsonResponse({
            'message': {
                'text': output
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘 급식', '내일 급식', '내일 모레 급식', '중간 고사', '여름 방학', 'BOT 정보']
            }
        })

def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['오늘 급식', '내일 급식', '내일 모레 급식', '중간 고사', '여름 방학', 'BOT 정보']
    })

@csrf_exempt
def answer(request):

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']
    user_key = received_json_data['user_key']

    print(datacontent)

    if datacontent == '오늘 급식':
        if u0.check(user_key):
            return ret_proc(PlzStopIt)
        dt = datetime.datetime.today()
        diet = get_meal(dt)
        return ret_proc(diet)

    elif datacontent == '내일 급식':
        if u1.check(user_key):
            return ret_proc(PlzStopIt)
        dt = datetime.datetime.today() + datetime.timedelta(days=1)
        diet = get_meal(dt)
        return ret_proc(diet)

    elif datacontent == '내일 모레 급식':
        if u2.check(user_key):
            return ret_proc(PlzStopIt)
        dt = datetime.datetime.today() + datetime.timedelta(days=2)
        diet = get_meal(dt)
        return ret_proc(diet)

    elif datacontent == '중간 고사':
        if u3.check(user_key):
            return ret_proc(PlzStopIt)
        td = datetime.date.today()
        sd = datetime.date(2018, 4, 26)

        delta = sd - td
        int(delta.days)
        dday = "[-]중간고사까지 %d일 남았습니다." % (delta.days)
        return ret_proc(dday)


    elif datacontent == '여름 방학':
        if u4.check(user_key):
            return ret_proc(PlzStopIt)
        td = datetime.date.today()
        sd = datetime.date(2018, 7, 20)

        delta = sd - td
        int(delta.days)
        dday = "[-]방학식까지 %d일 남았습니다." % (delta.days)
        return ret_proc(dday)

    elif datacontent == 'BOT 정보':
        return ret_proc(api_info)

    else:
        return ret_proc(_else)
