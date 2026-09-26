# 사용자에게 맞는 운동을 추천해주는 함수를 작성할 파이썬 파일

import random as rd

AEROBIC = 0
ANAEROBIC = 1

def recommandExercise(user):
    # ----- 함수 알고리즘 -----
    # 1. BMI 수치가 정상 범위 초과이면 (과체중 이상) 유산소 운동 추천
    # 2. BMI 수치가 정상 범위 이내이면 유산소 운동, 무산소 운동 시간을 비교해 적은 쪽을 추천
    #       => 만약 유산소 운동, 무산소 운동 시간이 같다면 랜덤으로 어떤 운동을 추천할 지 정한다.
    # 3. BMI 수치가 정상 범위 미만이면 (저체중) 무산소 운동 추천
    # * BMI 수치에 따른 분류는 "2018년 비만진료지침"에서 정한 기준을 바탕으로 정한다.
    
    if user.getBmi() >= 23:
        return AEROBIC
    elif user.getBmi() >= 18.5 and user.getBmi() < 23:
        if user.getAerobicTime() < user.getAnaerobicTime():
            return AEROBIC
        elif user.getAerobicTime() == user.getAnaerobicTime():
            randData = rd.randint(0, 1)
            if randData == 0:
                return AEROBIC
            else:
                return ANAEROBIC
        else:
            return ANAEROBIC
    else:
        return ANAEROBIC