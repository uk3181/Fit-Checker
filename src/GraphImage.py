DEBUG = False

# --------------------------- 각종 그래프 관련 도구를 사용할 수 있도록 만든 파이썬 파일 ----------------------------

import matplotlib.pyplot as plt

def makeInbodyGraphImage(user, option = 'day', dpiSet = 75): # option은 년도 단위인지, 월 단위인 지 등을 결정함.
    heightList = user.getHeightList()
    weightList = user.getWeightList()
    bmiList = user.getBmiList()

    # ---------- 각 기준점에 해당하는 각종 데이터를 정해진 개수만큼 저장하여 그래프에 표시하기 위한 리스트 ----------
    heightMarkList = []
    weightMarkList = []
    bmiMarkList = []
    # -------------------------------------------------------------------------------------------------------

    if option == 'year':
        yearMarkList = [] # 7개의 년도별 기준점을 표시하기 위한 리스트

        for i in range(7): # 7개의 년도별 기준점을 설정함.
            yearMarkList.append('{} years\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함. (그래프의 가독성 고려)
            heightMarkList.append(0)
            weightMarkList.append(0)
            bmiMarkList.append(0)
        
        lastYear = heightList[len(heightList) - 1].getDate().year
        dataCount = 0 # 7개의 데이터 중 몇 개를 그래프에 표시하였는 지 체크하기 위한 변수
        for i in range(len(heightList)):
            if lastYear == heightList[len(heightList) - 1 - i].getDate().year:
                heightMarkList[6 - dataCount] = heightList[len(heightList) - 1 - i].getData()
                weightMarkList[6 - dataCount] = weightList[len(weightList) - 1 - i].getData()
                bmiMarkList[6 - dataCount] = bmiList[len(bmiList) - 1 - i].getData()
                lastYear -= 1
                dataCount += 1
            if dataCount >= 6: # 7개까지만 데이터 저장 가능
                break

        ##### 그래프 그리기 #####
        plt.figure(dpi = dpiSet)
        plt.plot(yearMarkList, heightMarkList, 'bo-', label = 'Height (cm)')
        plt.plot(yearMarkList, weightMarkList, 'ro-', label = 'Weight (kg)')
        plt.plot(yearMarkList, bmiMarkList, 'yo-', label = 'BMI')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        plt.savefig('TempGraphs\\inbodyGraphPerYears.png')
    elif option == 'month':
        monthMarkList = [] # 7개의 월별 기준점을 표시하기 위한 리스트

        for i in range(7): # 7개의 월별 기준점을 설정함.
            monthMarkList.append('{} months\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함. (그래프의 가독성 고려)
            heightMarkList.append(0)
            weightMarkList.append(0)
            bmiMarkList.append(0)
        
        lastMonth = heightList[len(heightList) - 1].getDate().month
        dataCount = 0 # 7개의 데이터 중 몇 개를 그래프에 표시하였는 지 체크하기 위한 변수
        for i in range(len(heightList)):
            if lastMonth == heightList[len(heightList) - 1 - i].getDate().month:
                heightMarkList[6 - dataCount] = heightList[len(heightList) - 1 - i].getData()
                weightMarkList[6 - dataCount] = weightList[len(weightList) - 1 - i].getData()
                bmiMarkList[6 - dataCount] = bmiList[len(bmiList) - 1 - i].getData()
                lastMonth -= 1
                if lastMonth == 0:
                    lastMonth = 12
                dataCount += 1
            if dataCount >= 6: # 7개까지만 데이터 저장 가능
                break

        ##### 그래프 그리기 #####
        plt.figure(dpi = dpiSet)
        plt.plot(monthMarkList, heightMarkList, 'bo-', label = 'Height (cm)')
        plt.plot(monthMarkList, weightMarkList, 'ro-', label = 'Weight (kg)')
        plt.plot(monthMarkList, bmiMarkList, 'yo-', label = 'BMI')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        plt.savefig('TempGraphs\\inbodyGraphPerMonths.png')
    elif option == 'day':
        dayMarkList = [] # 7개의 날짜 기준점을 표시하기 위한 리스트

        for i in range(7): # 7개의 날짜 기준점을 설정함.
            dayMarkList.append('{} days\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함. (그래프의 가독성 고려)
            heightMarkList.append(0)
            weightMarkList.append(0)
            bmiMarkList.append(0)

        for i in range(len(heightList)):
            heightMarkList[6 - i] = heightList[len(heightList) - 1 - i].getData()
            weightMarkList[6 - i] = weightList[len(weightList) - 1 - i].getData()
            bmiMarkList[6 - i] = bmiList[len(bmiList) - 1 - i].getData()
            if i >= 6: # 7개까지만 데이터 저장 가능
                break

        ##### 그래프 그리기 #####
        plt.figure(dpi = dpiSet)
        plt.plot(dayMarkList, heightMarkList, 'bo-', label = 'Height (cm)')
        plt.plot(dayMarkList, weightMarkList, 'ro-', label = 'Weight (kg)')
        plt.plot(dayMarkList, bmiMarkList, 'yo-', label = 'BMI')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        plt.savefig('TempGraphs\\inbodyGraphPerDays.png')

    plt.close()

# 전체 운동 시간 = 유산소 운동 시간 + 무산소 운동 시간
def makeExerciseTimeGraphImage(user, option = 'day', dpiSet = 75): # option은 년도 단위인지, 월 단위인 지 등을 결정함.
    aerobicTimeList = user.getAerobicTimeList()
    anaerobicTimeList = user.getAnaerobicTimeList()

    exerciseTimeMarkList = [] # 각 기준점에 해당하는 각종 데이터를 정해진 개수만큼 저장하여 그래프에 표시하기 위한 리스트

    if option == 'year':
        yearMarkList = [] # 7개의 년도별 기준점을 표시하기 위한 리스트

        for i in range(7):
            yearMarkList.append('{} years\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함.
            exerciseTimeMarkList.append(0);

        lastYear = aerobicTimeList[len(aerobicTimeList) - 1].getDate().year
        dataCount = 0 # 7개의 데이터 중 몇 개를 그래프에 표시하였는지 체크하기 위한 변수
        for i in range(len(aerobicTimeList)):
            if lastYear == aerobicTimeList[len(aerobicTimeList) - 1 - i].getDate().year:
                exerciseTimeMarkList[6 - dataCount] += aerobicTimeList[len(aerobicTimeList) - 1 - i].getData()\
                        + anaerobicTimeList[len(anaerobicTimeList) - 1 - i].getData()
            else:
                dataCount += 1
                if dataCount >= 7: # 7개까지만 데이터 저장 가능
                    break
                lastYear -= 1

                exerciseTimeMarkList[6 - dataCount] += aerobicTimeList[len(aerobicTimeList) - 1 - i].getData()\
                        + anaerobicTimeList[len(anaerobicTimeList) - 1 - i].getData()
                
            if i == len(anaerobicTimeList) - 1: # 리스트의 모든 원소를 탐색 완료하였을 경우
                pass

        plt.figure(dpi = dpiSet)
        plt.bar(yearMarkList, exerciseTimeMarkList, color = '#1ED4EF', label = 'Exercise Time')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        plt.savefig('TempGraphs\\exerciseTimeGraphPerYears.png')
    elif option == 'month':
        monthMarkList = [] # 7개의 월별 기준점을 표시하기 위한 리스트

        for i in range(7): # 7개의 월별 기준점을 설정함.
            monthMarkList.append('{} months\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함.
            exerciseTimeMarkList.append(0)

        lastMonth = aerobicTimeList[len(aerobicTimeList) - 1].getDate().month
        dataCount = 0 # 7개의 데이터 중 몇 개를 그래프에 표시하였는지 체크하기 위한 변수
        for i in range(len(aerobicTimeList)):
            if lastMonth == aerobicTimeList[len(aerobicTimeList) - 1 - i].getDate().month:
                exerciseTimeMarkList[6 - dataCount] += aerobicTimeList[len(aerobicTimeList) - 1 - i].getData()\
                        + anaerobicTimeList[len(anaerobicTimeList) - 1 - i].getData()
            else:
                dataCount += 1
                if dataCount >= 7: # 7개까지만 데이터 저장 가능
                    break
                lastMonth -= 1
                if lastMonth == 0:
                    lastMonth = 12

                exerciseTimeMarkList[6 - dataCount] += aerobicTimeList[len(aerobicTimeList) - 1 - i].getData()\
                        + anaerobicTimeList[len(anaerobicTimeList) - 1 - i].getData()
            
            if i == len(aerobicTimeList) - 1: # 리스트 모든 원소를 탐색 완료하였을 경우
                pass
            
        ##### 그래프 그리기 #####
        plt.figure(dpi = dpiSet)
        plt.bar(monthMarkList, exerciseTimeMarkList, color = '#1ED4EF', label = 'Exercise Time')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        plt.savefig('TempGraphs\\exerciseTimeGraphPerMonths.png')
    elif option == 'day':
        dayMarkList = [] # 7개의 날짜 기준점을 표시하기 위한 리스트

        for i in range(7): # 7개의 날짜 기준점을 설정함.
            dayMarkList.append('{} days\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함. (그래프의 가독성 고려)
            exerciseTimeMarkList.append(0)

        for i in range(len(aerobicTimeList)):
            exerciseTimeMarkList[6 - i] = aerobicTimeList[len(aerobicTimeList) - 1 - i].getData()\
                    + anaerobicTimeList[len(anaerobicTimeList) - 1 - i].getData()
            if i >= 6: # 7개까지만 데이터 저장 가능
                break

        ##### 그래프 그리기 #####
        plt.figure(dpi = dpiSet)
        plt.bar(dayMarkList, exerciseTimeMarkList, color = '#1ED4FF', label = 'Exercise Time')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        plt.savefig('TempGraphs\\exerciseTimeGraphPerDays.png')

    plt.close()

def makeExerciseDataGraphImage(user, dataType, option = 'day', dpiSet = 75): # 운동 시간을 제외한 나머지 운동 기록 데이터를 그래프로 나타내기 위한 함수
    exerciseDataList = []
    if dataType == 'walk count':
        exerciseDataList = user.getWalkCountList()
    elif dataType == 'walk distance':
        exerciseDataList = user.getWalkDistanceList()
    elif dataType == 'sleep time':
        exerciseDataList = user.getSleepTimeList()

    exerciseDataMarkList = [] # 각 기준점에 해당하는 각종 데이터를 정해진 개수만큼 저장하여 그래프에 표시하기 위한 리스트

    if option == 'year':
        yearMarkList = [] # 7개의 년도별 기준점을 표시하기 위한 리스트

        for i in range(7):
            yearMarkList.append('{} years\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함.
            exerciseDataMarkList.append(0);

        lastYear = exerciseDataList[len(exerciseDataList) - 1].getDate().year
        dataCount = 0 # 7개의 데이터 중 몇 개를 그래프에 표시하였는지 체크하기 위한 변수
        for i in range(len(exerciseDataList)):
            if lastYear == exerciseDataList[len(exerciseDataList) - 1 - i].getDate().year:
                exerciseDataMarkList[6 - dataCount] += exerciseDataList[len(exerciseDataList) - 1 - i].getData()
            else:
                dataCount += 1
                if dataCount >= 7: # 7개까지만 데이터 저장 가능
                    break
                lastYear -= 1

                exerciseDataMarkList[6 - dataCount] += exerciseDataList[len(exerciseDataList) - 1 - i].getData()
                
            if i == len(exerciseDataList) - 1: # 리스트의 모든 원소를 탐색 완료하였을 경우
                pass

        plt.figure(dpi = dpiSet)
        if dataType == 'walk count':
            plt.bar(yearMarkList, exerciseDataMarkList, color = '#1ED4EF', label = 'Walk Count')
        elif dataType == 'walk distance':
            plt.bar(yearMarkList, exerciseDataMarkList, color = '#1ED4EF', label = 'Walk Distance')
        elif dataType == 'sleep time':
            plt.bar(yearMarkList, exerciseDataMarkList, color = '#1ED4EF', label = 'Sleep Time')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        if dataType == 'walk count':
            plt.savefig('TempGraphs\\walkCountGraphPerYears.png')
        elif dataType == 'walk distance':
            plt.savefig('TempGraphs\\walkDistanceGraphPerYears.png')
        elif dataType == 'sleep time':
            plt.savefig('TempGraphs\\sleepTimeGraphPerYears.png')
    elif option == 'month':
        monthMarkList = [] # 7개의 월별 기준점을 표시하기 위한 리스트

        for i in range(7): # 7개의 월별 기준점을 설정함.
            monthMarkList.append('{} months\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함.
            exerciseDataMarkList.append(0)

        lastMonth = exerciseDataList[len(exerciseDataList) - 1].getDate().month
        dataCount = 0 # 7개의 데이터 중 몇 개를 그래프에 표시하였는지 체크하기 위한 변수
        for i in range(len(exerciseDataList)):
            if lastMonth == exerciseDataList[len(exerciseDataList) - 1 - i].getDate().month:
                exerciseDataMarkList[6 - dataCount] += exerciseDataList[len(exerciseDataList) - 1 - i].getData()
            else:
                dataCount += 1
                if dataCount >= 7: # 7개까지만 데이터 저장 가능
                    break
                lastMonth -= 1
                if lastMonth == 0:
                    lastMonth = 12

                exerciseDataMarkList[6 - dataCount] += exerciseDataList[len(exerciseDataList) - 1 - i].getData()
            
            if i == len(exerciseDataList) - 1: # 리스트 모든 원소를 탐색 완료하였을 경우
                pass
            
        ##### 그래프 그리기 #####
        plt.figure(dpi = dpiSet)
        if dataType == 'walk count':
            plt.bar(monthMarkList, exerciseDataMarkList, color = '#1ED4EF', label = 'Walk Count')
        elif dataType == 'walk distance':
            plt.bar(monthMarkList, exerciseDataMarkList, color = '#1ED4EF', label = 'Walk Distance')
        elif dataType == 'sleep time':
            plt.bar(monthMarkList, exerciseDataMarkList, color = '#1ED4EF', label = 'Sleep Time')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        if dataType == 'walk count':
            plt.savefig('TempGraphs\\walkCountGraphPerMonths.png')
        elif dataType == 'walk distance':
            plt.savefig('TempGraphs\\walkDistanceGraphPerMonths.png')
        elif dataType == 'sleep time':
            plt.savefig('TempGraphs\\sleepTimeGraphPerMonths.png')
    elif option == 'day':
        dayMarkList = [] # 7개의 날짜 기준점을 표시하기 위한 리스트

        for i in range(7): # 7개의 날짜 기준점을 설정함.
            dayMarkList.append('{} days\nago'.format(6 - i))
        for i in range(7): # 먼저 각종 데이터 7개를 모두 0으로 초기화함. (그래프의 가독성 고려)
            exerciseDataMarkList.append(0)

        for i in range(len(exerciseDataList)):
            exerciseDataMarkList[6 - i] = exerciseDataList[len(exerciseDataList) - 1 - i].getData()
            if i >= 6: # 7개까지만 데이터 저장 가능
                break

        ##### 그래프 그리기 #####
        plt.figure(dpi = dpiSet)
        if dataType == 'walk count':
            plt.bar(dayMarkList, exerciseDataMarkList, color = '#1ED4FF', label = 'Walk Count')
        elif dataType == 'walk distance':
            plt.bar(dayMarkList, exerciseDataMarkList, color = '#1ED4FF', label = 'Walk Distance')
        elif dataType == 'sleep time':
            plt.bar(dayMarkList, exerciseDataMarkList, color = '#1ED4FF', label = 'Sleep Time')
        plt.legend(loc = 'upper left')
        plt.ylim(0)
        if dataType == 'walk count':
            plt.savefig('TempGraphs\\walkCountGraphPerDays.png')
        elif dataType == 'walk distance':
            plt.savefig('TempGraphs\\walkDistanceGraphPerDays.png')
        elif dataType == 'sleep time':
            plt.savefig('TempGraphs\\sleepTimeGraphPerDays.png')

    plt.close()

def makeRankOfFriendsGraphImage(user, dpiSet = 75): # 최대 5명까지의 친구들과의 운동 시간 순위를 정하여 그래프로 만들어주는 함수
    userForRankList = user.getFriendList().copy() # 순위를 매기기 위해 사용자 객체를 담을 리스트를 사용해야 한다.
    userForRankList.append(user) # 자기 자신까지 포함하여 총 6명의 사용자에게 순위를 매긴다.

    # 각 사용자들의 "운동 시간"을 기준으로 정렬해야 한다.
    for i in range(len(userForRankList) - 1):
        for j in range(i + 1, len(userForRankList)):
            if userForRankList[i].getExerciseTimeFor30Days() < userForRankList[j].getExerciseTimeFor30Days():
                userForRankList[i], userForRankList[j] = userForRankList[j], userForRankList[i]
            
    nameAndRankMarkList = []
    exerciseTimeList = []
    rankMarkNameList = ['1st\nplace', '2nd\nplace', '3rd\nplace', '4th\nplace', '5th\nplace', '6th\nplace']
    barColorList = []
    curRankIndex = 0
    for i in range(len(userForRankList)):
        if i != 0:
            if userForRankList[i].getExerciseTimeFor30Days() != userForRankList[i - 1].getExerciseTimeFor30Days():
                curRankIndex = i
                barColorList.append('#1ED4FF')
            else:
                if barColorList[len(barColorList) - 1] == '#FFFB00':
                    barColorList.append('#FFFB00')
                else:
                    barColorList.append('#1ED4FF')
        else:
            barColorList.append('#FFFB00')
        nameAndRank = '{}: {}'.format(rankMarkNameList[curRankIndex], userForRankList[i].getId())
        nameAndRankMarkList.append(nameAndRank)
    for i in range(len(userForRankList)):
        exerciseTimeList.append(userForRankList[i].getExerciseTimeFor30Days())

    ##### 그래프 그리기 #####
    plt.figure(dpi = dpiSet)
    plt.bar(nameAndRankMarkList, exerciseTimeList, color = barColorList)
    plt.title('Rank of Exercise Time for 30 Days', fontdict = {'family': 'Arial', 'size': 18, 'weight': 'bold'})
    plt.ylim(0)
    plt.savefig('TempGraphs\\rankOfExerciseTimeFor30Days.png')

    plt.close()

if DEBUG:
    from User import *
    testUser = User()
    testUser.setAerobicTime(100)
    testUser.setAnaerobicTime(40)
    testUser.updateDatas()
    makeRankOfFriendsGraphImage(testUser)