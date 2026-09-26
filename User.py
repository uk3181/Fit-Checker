from pickle import *
from Person import *
from DateData import *

class User(Person): # 실제로 프로그램에서 사용하게 될 사용자 클래스
    def __init__(self, name = '홍길동', age = 20, gender = '남', id = 'uk3181', pw = '1234', height = 170.0, weight = 60.0):
        super().__init__(name, age, gender)
        self.__id = id
        self.__pw = pw
        self.__height = height
        self.__weight = weight
        self.__bmi = calcBmi(self.__height, self.__weight)

        self.__aerobicTime = 0
        self.__anaerobicTime = 0
        self.__walkCount = 0
        self.__walkDistance = 0
        self.__sleepTime = 0

        self.__friendList = [] # 친구는 최대 5명까지만 추가 가능하도록!

        # 초기로 설정한 키, 몸무게, BMI도 데이터 변화 추이 그래프에 반영해야 함.
        # 아래에 표기된 리스트에는 날짜 정보까지 함께 저장됨.
        self.__heightList = []
        self.__heightList.append(DateData(self.__height))

        self.__weightList = []
        self.__weightList.append(DateData(self.__weight))

        self.__bmiList = []
        self.__bmiList.append(DateData(self.__bmi))

        self.__aerobicTimeList = []
        self.__aerobicTimeList.append(DateData(self.__aerobicTime))

        self.__anaerobicTimeList = []
        self.__anaerobicTimeList.append(DateData(self.__anaerobicTime))

        self.__walkCountList = []
        self.__walkCountList.append(DateData(self.__walkCount))

        self.__walkDistanceList = []
        self.__walkDistanceList.append(DateData(self.__walkDistance))

        self.__sleepTimeList = []
        self.__sleepTimeList.append(DateData(self.__sleepTime))

        self.__notificationList = [] # 알림은 최대 6개까지만 저장 가능함.
        if self.__bmi >= 23:
            self.__notificationList.append(DateData('BMI 수치가 높습니다. 체중 관리에 신경쓰세요.'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)
        elif self.__bmi < 18.5:
            self.__notificationList.append(DateData('BMI 수치가 낮습니다. 무산소 운동을 좀 더 열심히 하세요!'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)

    def setId(self, id):
        self.__id = id
    
    def setPw(self, pw):
        self.__pw = pw
    
    def setHeight(self, height):
        self.__height = height
        prevBmi = self.__bmi
        self.__bmi = calcBmi(self.__height, self.__weight) # BMI 계산은 항상 자동적으로 실행되어야 함.

        # BMI 수치에 유의미한 변동이 있을 경우 알림 목록에 해당 사항을 추가해야 한다.
        if self.__bmi >= 23 and prevBmi < 23:
            self.__notificationList.append(DateData('BMI 수치가 높습니다. 체중 관리에 신경쓰세요.'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)
        elif (self.__bmi >= 18.5 and self.__bmi < 23) and (not (prevBmi >= 18.5 and prevBmi < 23)):
            self.__notificationList.append(DateData('축하합니다! BMI 수치가 정상 범위 내에 있습니다.'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)
        elif self.__bmi < 18.5 and prevBmi >= 18.5:
            self.__notificationList.append(DateData('BMI 수치가 낮습니다. 무산소 운동을 좀 더 열심히 하세요!'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)

        # 키를 새로 설정할 때마다 데이터 변화 추이 그래프에 반영
        self.__appendBodyDatasList(DateData(self.__height), DateData(self.__weight), DateData(self.__bmi),
                DateData(self.__aerobicTime), DateData(self.__anaerobicTime), DateData(self.__walkCount),\
                DateData(self.__walkDistance), DateData(self.__sleepTime))
    
    def setWeight(self, weight):
        self.__weight = weight
        prevBmi = self.__bmi
        self.__bmi = calcBmi(self.__height, self.__weight) # BMI 계산은 항상 자동적으로 실행되어야 함.

        # BMI 수치에 유의미한 변동이 있을 경우 알림 목록에 해당 사항을 추가해야 한다.
        if self.__bmi >= 23 and prevBmi < 23:
            self.__notificationList.append(DateData('BMI 수치가 높습니다. 체중 관리에 신경쓰세요.'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)
        elif (self.__bmi >= 18.5 and self.__bmi < 23) and (not (prevBmi >= 18.5 and prevBmi < 23)):
            self.__notificationList.append(DateData('축하합니다! BMI 수치가 정상 범위 내에 있습니다.'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)
        elif self.__bmi < 18.5 and prevBmi >= 18.5:
            self.__notificationList.append(DateData('BMI 수치가 낮습니다. 무산소 운동을 좀 더 열심히 하세요!'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)

        # 몸무게를 새로 설정할 때마다 데이터 변화 추이 그래프에 반영
        self.__appendBodyDatasList(DateData(self.__height), DateData(self.__weight), DateData(self.__bmi),
                DateData(self.__aerobicTime), DateData(self.__anaerobicTime), DateData(self.__walkCount),\
                DateData(self.__walkDistance), DateData(self.__sleepTime))

    def setAerobicTime(self, aerobicTime):
        self.__aerobicTime = aerobicTime

        # 유산소 운동 시간을 저장할 때마다 데이터 변화 추이 그래프에 반영
        self.__appendBodyDatasList(DateData(self.__height), DateData(self.__weight), DateData(self.__bmi),
                DateData(self.__aerobicTime), DateData(self.__anaerobicTime), DateData(self.__walkCount),\
                DateData(self.__walkDistance), DateData(self.__sleepTime))

    def setAnaerobicTime(self, anaerobicTime):
        self.__anaerobicTime = anaerobicTime

        # 무산소 운동 시간을 저장할 때마다 데이터 변화 추이 그래프에 반영
        self.__appendBodyDatasList(DateData(self.__height), DateData(self.__weight), DateData(self.__bmi),
                DateData(self.__aerobicTime), DateData(self.__anaerobicTime), DateData(self.__walkCount),\
                DateData(self.__walkDistance), DateData(self.__sleepTime))

    def setWalkCount(self, walkCount):
        prevWalkCount = self.__walkCount
        self.__walkCount = walkCount

        # 만 보 이상 걸었을 경우 축하 메시지를 알림 목록에 추가한다.
        if self.__walkCount >= 10000 and prevWalkCount < 10000:
            self.__notificationList.append(DateData('축하합니다! 만 보 걷기에 성공하셨습니다!'))
            if len(self.__notificationList) >= 7:
                self.__notificationList.pop(0)

        # 걸음 수를 저장할 때마다 데이터 변화 추이 그래프에 반영
        self.__appendBodyDatasList(DateData(self.__height), DateData(self.__weight), DateData(self.__bmi),
                DateData(self.__aerobicTime), DateData(self.__anaerobicTime), DateData(self.__walkCount),\
                DateData(self.__walkDistance), DateData(self.__sleepTime))

    def setFriendList(self, friendList):
        self.__friendList = friendList

    def setWalkDistance(self, walkDistance):
        self.__walkDistance = walkDistance

        # 걸기 거리를 저장할 때마다 데이터 변화 추이 그래프에 반영
        self.__appendBodyDatasList(DateData(self.__height), DateData(self.__weight), DateData(self.__bmi),
                DateData(self.__aerobicTime), DateData(self.__anaerobicTime), DateData(self.__walkCount),\
                DateData(self.__walkDistance), DateData(self.__sleepTime))

    def setSleepTime(self, sleepTime):
        self.__sleepTime = sleepTime

        # 수면 시간을 저장할 때마다 데이터 변화 추이 그래프에 반영
        self.__appendBodyDatasList(DateData(self.__height), DateData(self.__weight), DateData(self.__bmi),
                DateData(self.__aerobicTime), DateData(self.__anaerobicTime), DateData(self.__walkCount),\
                DateData(self.__walkDistance), DateData(self.__sleepTime))

    def getId(self):
        return self.__id
    
    def getPw(self):
        return self.__pw
    
    def getHeight(self):
        return self.__height

    def getHeightList(self):
        return self.__heightList
    
    def getWeight(self):
        return self.__weight

    def getWeightList(self):
        return self.__weightList
    
    def getBmi(self):
        return self.__bmi

    def getBmiList(self):
        return self.__bmiList

    def getAerobicTime(self):
        return self.__aerobicTime

    def getAerobicTimeList(self):
        return self.__aerobicTimeList

    def __getAerobicTimeFor30Days(self): # 최대 지난 30일 동안의 총 유산소 운동 시간 합계를 반환해주는 메소드
        totalAerobicTime = 0
        for i in range(min(len(self.__aerobicTimeList), 30)):
            totalAerobicTime += self.__aerobicTimeList[i].getData()
        return totalAerobicTime

    def getAnaerobicTime(self):
        return self.__anaerobicTime

    def getAnaerobicTimeList(self):
        return self.__anaerobicTimeList

    def __getAnaerobicTimeFor30Days(self): # 최대 지난 30일 동안의 총 무산소 운동 시간 합계를 반환해주는 메소드
        totalAnaerobicTime = 0
        for i in range(min(len(self.__anaerobicTimeList), 30)):
            totalAnaerobicTime += self.__anaerobicTimeList[i].getData()
        return totalAnaerobicTime
    
    def getExerciseTimeFor30Days(self): # 최대 지난 30일 동안의 총 운동 시간 합계를 반환해주는 메소드
        return self.__getAerobicTimeFor30Days() + self.__getAnaerobicTimeFor30Days()

    def getWalkCount(self):
        return self.__walkCount

    def getWalkCountList(self):
        return self.__walkCountList

    def getWalkDistance(self):
        return self.__walkDistance

    def getWalkDistanceList(self):
        return self.__walkDistanceList

    def getSleepTime(self):
        return self.__sleepTime

    def getSleepTimeList(self):
        return self.__sleepTimeList

    def getFriendList(self):
        return self.__friendList

    def getNotificationList(self):
        return self.__notificationList

    def addNotification(self, notification):
        self.__notificationList.append(DateData(notification))
        if len(self.__notificationList) >= 7:
            self.__notificationList.pop(0)

    def resetNotificationList(self):
        popCount = len(self.__notificationList)
        for i in range(popCount):
            self.__notificationList.pop()

    def addFriend(self, friendUser): # 친구 추가 함수
        self.__friendList.append(friendUser) # 1. 자신의 친구 목록에 상대방 추가
        friendUser.__friendList.append(self) # 2. 상대방의 친구 목록에 자기 자신을 추가

        # A 사용자가 B사용자를 친구로 추가하였을 경우, B 사용자는 해당 사실을 알 수 있도록 알림을 받아야 한다.
        friendUser.addNotification('{}님이 친구로 추가되었습니다.'.format(self.__id))

    def deleteFriend(self, friendUser): # 친구 삭제 함수
        for i in range(len(self.__friendList)): # 1. 자신의 친구 목록에서 상대방 삭제
            if self.__friendList[i].getId() == friendUser.__id:
                self.__friendList.pop(i)
                break

        for i in range(len(friendUser.__friendList)): # 2. 상대방의 친구 목록에서 자기 자신을 삭제
            if friendUser.__friendList[i].getId() == self.__id:
                friendUser.__friendList.pop(i)
                break

    def isFriend(self, friendUser): # 서로 친구 관계인지 확인하는 함수
        friendRelation = True

        # 1. 자신의 친구 목록에 상대방이 있는지 확인
        if len(self.__friendList) == 0:
            friendRelation = False
        else:
            for i in range(len(self.__friendList)):
                if self.__friendList[i].getId() == friendUser.__id:
                    break
                if i == len(self.__friendList) - 1:
                    friendRelation = False

        # 2. 상대방의 친구 목록에 자기 자신이 있는지 확인
        if friendRelation:
            if len(friendUser.__friendList) == 0:
                friendRelation = False
            else:
                for i in range(len(friendUser.__friendList)):
                    if friendUser.__friendList[i].getId() == self.__id:
                        break
                    if i == len(friendUser.__friendList) - 1:
                        friendRelation = False

        return friendRelation


    # 키, 몸무게, BMI 데이터, 각종 운동 데이터 등을 그래프로 나타내기 위해, 각종 데이터를 리스트로 추가하는 메소드
    def __appendBodyDatasList(self, heightDateData, weightDateData, bmiDateData,\
            aerobicTimeDateData, anaerobicTimeDateData, walkCountDateData, walkDistanceDateData,\
            sleepTimeDateData):
        addedHeightDateData = heightDateData
        addedWeightDateData = weightDateData
        addedBmiDateData = bmiDateData

        addedAerobicTimeDateData = aerobicTimeDateData
        addedAnaerobicTimeDateTata = anaerobicTimeDateData
        addedWalkCountDateData = walkCountDateData
        addedWalkDistanceDateData = walkDistanceDateData
        addedSleepTimeDateData = sleepTimeDateData

        # 1. 만약 같은 날짜에 데이터 변경이 여러 번 일어날 경우, 가장 마지막으로 변경된 데이터만 저장되어야 한다.
        # 2. 각 데이터들은 5000개를 넘지 않도록 하며, 리스트가 꽉 찼을 경우 가장 오래된 데이터를 삭제하도록 한다.
        # 키
        if self.__heightList[len(self.__heightList) - 1].isDateEqual(addedHeightDateData):
            self.__heightList[len(self.__heightList) - 1] = addedHeightDateData
        else:
            self.__heightList.append(addedHeightDateData)
            
            if len(self.__heightList) > 5000:
                self.__heightList.pop(0)

        # 몸무게
        if self.__weightList[len(self.__weightList) - 1].isDateEqual(addedWeightDateData):
            self.__weightList[len(self.__weightList) - 1] = addedWeightDateData
        else:
            self.__weightList.append(addedWeightDateData)
            
            if len(self.__weightList) > 5000:
                self.__weightList.pop(0)

        # BMI
        if self.__bmiList[len(self.__bmiList) - 1].isDateEqual(addedBmiDateData):
            self.__bmiList[len(self.__bmiList) - 1] = addedBmiDateData
        else:
            self.__bmiList.append(addedBmiDateData)
            
            if len(self.__bmiList) > 5000:
                self.__bmiList.pop(0)

        # 유산소 운동 시간
        if self.__aerobicTimeList[len(self.__aerobicTimeList) - 1].isDateEqual(addedAerobicTimeDateData):
            self.__aerobicTimeList[len(self.__aerobicTimeList) - 1] = addedAerobicTimeDateData
        else:
            self.__aerobicTimeList.append(addedAerobicTimeDateData)

            if len(self.__aerobicTimeList) > 5000:
                self.__aerobicTimeList.pop(0)

        # 무산소 운동 시간
        if self.__anaerobicTimeList[len(self.__anaerobicTimeList) - 1].isDateEqual(addedAnaerobicTimeDateTata):
            self.__anaerobicTimeList[len(self.__anaerobicTimeList) - 1] = addedAnaerobicTimeDateTata
        else:
            self.__anaerobicTimeList.append(addedAnaerobicTimeDateTata)

            if len(self.__anaerobicTimeList) > 5000:
                self.__anaerobicTimeList.pop(0)

        # 걸음 수
        if self.__walkCountList[len(self.__walkCountList) - 1].isDateEqual(addedWalkCountDateData):
            self.__walkCountList[len(self.__walkCountList) - 1] = addedWalkCountDateData
        else:
            self.__walkCountList.append(addedWalkCountDateData)

            if len(self.__walkCountList) > 5000:
                self.__walkCountList.pop(0)

        # 걷기 거리
        if self.__walkDistanceList[len(self.__walkDistanceList) - 1].isDateEqual(addedWalkDistanceDateData):
            self.__walkDistanceList[len(self.__walkDistanceList) - 1] = addedWalkDistanceDateData
        else:
            self.__walkDistanceList.append(addedWalkDistanceDateData)

            if len(self.__walkDistanceList) > 5000:
                self.__walkDistanceList.pop(0)

        # 수면 시간
        if self.__sleepTimeList[len(self.__sleepTimeList) - 1].isDateEqual(addedSleepTimeDateData):
            self.__sleepTimeList[len(self.__sleepTimeList) - 1] = addedSleepTimeDateData
        else:
            self.__sleepTimeList.append(addedSleepTimeDateData)

            if len(self.__sleepTimeList) > 5000:
                self.__sleepTimeList.pop(0)

    def updateDatas(self): # 날짜가 지남에 따라, 데이터들은 변화가 없더라도 각종 데이터 리스트에 흘러간 날짜만큼 채워져야 함.
        currentDay = date.today() # 현재 날짜 정보를 가져옴.
        lastDayInList = self.__heightList[len(self.__heightList) - 1].getDate() # 마지막으로 리스트에 저장된 데이터의 날짜를 가져옴.
        dayGap = currentDay - lastDayInList # 날짜 차이 계산

        # 리스트에서 마지막으로 저장된 각종 데이터들
        lastHeightDateData = self.__heightList[len(self.__heightList) - 1].getData()
        lastWeightDateData = self.__weightList[len(self.__weightList) - 1].getData()
        lastBmiDateData = self.__bmiList[len(self.__bmiList) - 1].getData()

        for i in range(dayGap.days):
            appendedLastHeightDateData = DateData(lastHeightDateData, lastDayInList + timedelta(days = i + 1))
            appendedLastWeightDateData = DateData(lastWeightDateData, lastDayInList + timedelta(days = i + 1))
            appendedLastBmiDateData = DateData(lastBmiDateData, lastDayInList + timedelta(days = i + 1))

            # 각종 운동 데이터는 날짜 차이 만큼 별도로 기록이 없으면 전부 0으로 설정해준다.
            appendedAerobicTimeDateData = DateData(0, lastDayInList + timedelta(days = i + 1))
            appendedAnaerobicTimeDateData = DateData(0, lastDayInList + timedelta(days = i + 1))
            appendedWalkCountDateData = DateData(0, lastDayInList + timedelta(days = i + 1))
            appendedWalkDistanceDateData = DateData(0, lastDayInList + timedelta(days = i + 1))
            appendedSleepTimeDateData = DateData(0, lastDayInList + timedelta(days = i + 1))

            self.__appendBodyDatasList(appendedLastHeightDateData, appendedLastWeightDateData, appendedLastBmiDateData,\
                    appendedAerobicTimeDateData, appendedAnaerobicTimeDateData, appendedWalkCountDateData,
                    appendedWalkDistanceDateData, appendedSleepTimeDateData)

        # 날짜가 지나면 각종 운동 데이터는 모두 0으로 초기화해야 한다.
        self.__aerobicTime = self.__aerobicTimeList[len(self.__aerobicTimeList) - 1].getData()
        self.__anaerobicTime = self.__anaerobicTimeList[len(self.__anaerobicTimeList) - 1].getData()
        self.__walkCount = self.__walkCountList[len(self.__walkCountList) - 1].getData()
        self.__walkDistance = self.__walkDistanceList[len(self.__walkDistanceList) - 1].getData()
        self.__sleepTime = self.__sleepTimeList[len(self.__sleepTimeList) - 1].getData()






def calcBmi(height, weight): # BMI 계산 함수
    return weight / (height / 100) ** 2

def findUserById(usersList, findId): # id를 기준으로 특정 사용자 찾기
    for user in usersList:
        if findId == user.getId():
            return True # 사용자 찾음.
    return False # 사용자 찾지 못함.

def editUsersFile(editedUser): # 특정 사용자 정보를 변경하게 되면 사용자 리스트를 수정하여 다시 파일로 저장하기
                               # 특정 사용자의 친구 사용자가 존재할 경우, 친구 사용자에 저장된 친구 목록에서 자기 자신의 정보도 같이
                               # 업데이트될 수 있도록 설정해야 한다.
    usersFile = open('users.bin', 'rb')
    usersList = load(usersFile)
    usersFile.close()

    friendList = editedUser.getFriendList()

    for i in range(len(usersList)):
        if editedUser.getId() == usersList[i].getId():
            usersList[i] = editedUser
            break

    usersFile = open('users.bin', 'wb')
    dump(usersList, file = usersFile)
    usersFile.close()

    for i in range(len(friendList)):
        editedFriendUser = friendList[i] # 수정될 친구 사용자 객체를 나타내는 변수

        friendListInEditedFriendUser = editedFriendUser.getFriendList() # 수정될 친구 사용자의 친구 목록
        for j in range(len(friendListInEditedFriendUser)):
            if editedUser.getId() == friendListInEditedFriendUser[j].getId():
                friendListInEditedFriendUser[j] = editedUser
                break

        editedFriendUser.setFriendList(friendListInEditedFriendUser)

        usersFile = open('users.bin', 'rb')
        usersList = load(usersFile)
        usersFile.close()

        for j in range(len(usersList)):
            if editedFriendUser.getId() == usersList[j].getId():
                usersList[j] = editedFriendUser
                break

        usersFile = open('users.bin', 'wb')
        dump(usersList, file = usersFile)
        usersFile.close()

def deleteUserInUsersFile(deletedUser): # 특정 사용자를 사용자 리스트에서 삭제한 후 다시 파일로 저장하는 함수
                                        # 특정 사용자의 친구 사용자가 존재할 경우, 각 친구 사용자에 저장된 친구 리스에서 자기 자신을 삭제해야 한다.
    usersFile = open('users.bin', 'rb')
    usersList = load(usersFile)
    usersFile.close()

    friendList = deletedUser.getFriendList()
    for i in range(len(friendList)):
        editedFriendList = friendList[i].getFriendList()
        for j in range(len(editedFriendList)):
            if deletedUser.getId() == editedFriendList[j].getId():
                editedFriendList.pop(j)
                break
        friendList[i].setFriendList(editedFriendList)

    for i in range(len(usersList)):
        if deletedUser.getId() == usersList[i].getId():
            usersList.pop(i)
            break

    usersFile = open('users.bin', 'wb')
    dump(usersList, file = usersFile)
    usersFile.close()

    for i in range(len(friendList)):
        usersFile = open('users.bin', 'rb')
        usersList = load(usersFile)
        usersFile.close()

        for j in range(len(usersList)):
            if friendList[i].getId() == usersList[j].getId():
                usersList[j] = friendList[i]
                break

        usersFile = open('users.bin', 'wb')
        dump(usersList, file = usersFile)
        usersFile.close()