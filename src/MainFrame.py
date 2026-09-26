DEBUG = False

from tkinter import *
from tkinter import messagebox
from tkinter.font import *
from pickle import *
from User import *
from GraphImage import *
import webbrowser as wb
import random as rd

import Fitness # 운동 추천 관련 모듈
import Login # 로그인 처리 관련 모듈

loginedUser = User() # 로그인한 사용자 정보






def openFrame(frame):
    frame.tkraise()

def loginCommand(): # 로그인 처리 함수
    usersFile = open('users.bin', 'rb')

    usersList = load(file = usersFile)
    inputId = idEntry.get()
    inputPw = pwEntry.get()

    usersFile.close()

    loginPassedUser = Login.loginPass(usersList, inputId, inputPw) # 로그인한 사용자 정보 (None이면 로그인 실패)
    if loginPassedUser != None: # 로그인 성공!
        global loginedUser
        loginedUser = loginPassedUser
        loginedUser.updateDatas()

        pwEntry.delete(0, END)
        insertEditEntries(loginedUser)

        goMainScreen()
    else:
        messagebox.showinfo('로그인 오류', 'ID/PW가 올바르지 않습니다.')

def assignCommand(): # 회원가입 화면으로 이동하는 함수
    assignFrame.lift()

def cancelAssignCommand(): # 회원가입 취소 함수
    inputNameEntry.delete(0, END)
    inputAgeEntry.delete(0, END)
    inputGenderEntry.delete(0, END)
    inputIdEntry.delete(0, END)
    inputPwEntry.delete(0, END)
    inputHeightEntry.delete(0, END)
    inputWeightEntry.delete(0, END)
    
    loginFrame.lift()

def saveUserInfoCommand(): # 회원가입 완료 처리 함수
    # 1. 먼저 users.bin에서 사용자 정보가 담긴 리스트를 읽어온다.
    usersFile = open('users.bin', 'rb')

    usersList = []
    usersList = load(file = usersFile)

    usersFile.close()

    # 2. 그 후, 리스트에 새로운 사용자를 추가한 후, 수정된 리스트를 다시 해당 파일에 덮어쓰기한다.
    isAssigned = True # 회원 가입 성공 여부 (각각의 정보 입력 값에 올바르게 입력되었는지 확인 여부)


    savedName = inputNameEntry.get()
    if savedName == '':
        isAssigned = False
    if isAssigned:
        try:
            savedAge = int(inputAgeEntry.get())
            if savedAge <= 0:
                isAssigned = False
        except ValueError:
            isAssigned = False
        
        if isAssigned:
            savedGender = inputGenderEntry.get()
            if savedGender != '남' and savedGender != '여':
                isAssigned = False
            if isAssigned:
                savedId = inputIdEntry.get()
                savedPw = inputPwEntry.get()
                if savedId == '' or savedPw == '':
                    isAssigned = False
                if isAssigned:
                    try:
                        savedHeight = float(inputHeightEntry.get())
                    except ValueError:
                        isAssigned = False
                    if isAssigned:
                        try:
                            savedWeight = float(inputWeightEntry.get())
                        except ValueError:
                            isAssigned = False

    if isAssigned:
        if findUserById(usersList, savedId): # ID 중복 체크
            messagebox.showinfo('입력 오류', '이미 가입된 ID입니다.')
        else:
            if len(savedName) > 10: # 이름은 최대 10자까지만 설정 가능
                messagebox.showinfo('입력 오류', '이름은 최대 10자까지만 설정 가능합니다.')
            else:
                if savedAge > 150: # 나이는 최대 150세까지만 설정 가능
                    messagebox.showinfo('입력 오류', '나이는 최대 150세까지만 설정 가능합니다.')
                else:
                    if len(savedId) > 10 or len(savedPw) > 10: # ID/PW는 최대 10자까지만 설정 가능
                        messagebox.showinfo('입력 오류', 'ID/PW는 최대 10자리까지만 설정 가능합니다.')
                    else:
                        if len(savedPw) < 4: # PW는 최소 4자리부터 설정 가능
                            messagebox.showinfo('입력 오류', 'PW는 최소 4자리부터 설정 가능합니다.')
                        else:
                            alphabetCount = 0; nonalphabetCount = 0; digitCount = 0
                            for i in range(len(savedPw)):
                                if savedPw[i] >= 'A' and savedPw[i] <= 'Z' or savedPw[i] >= 'a' and savedPw[i] <= 'z':
                                    alphabetCount += 1
                                elif savedPw[i] >= '0' and savedPw[i] <= '9':
                                    digitCount += 1
                                else:
                                    nonalphabetCount += 1
                            if alphabetCount == 0 or nonalphabetCount == 0 or digitCount == 0: # PW에는 최소 영문자 1개, 특수 문자 1개, 숫자 1개 이상 넣어야 함.
                                messagebox.showinfo('입력 오류', 'PW에는 최소 영문자 1개, 특수 문자 1개, 숫자 1개 이상 넣어야 합니다.')
                            else:
                                if savedHeight < 50 or savedHeight > 250: # 키는 최소 50cm부터 250cm까지만 설정 가능
                                    messagebox.showinfo('입력 오류', '키는 최소 50cm부터 250cm까지만 설정 가능합니다.')
                                else:
                                    if savedWeight < 10 or savedWeight > 150: # 몸무게는 최소 10kg부터 150kg까지만 설정 가능
                                        messagebox.showinfo('입력 오류', '몸무게는 최소 10kg부터 150kg까지만 설정 가능합니다.')
                                    else:
                                        usersFile = open('users.bin', 'wb')

                                        savedUser = User(savedName, savedAge, savedGender, savedId, savedPw, savedHeight, savedWeight)

                                        usersList.append(savedUser)

                                        dump(usersList, file = usersFile)

                                        usersFile.close()

                                        messagebox.showinfo(message = '회원 가입이 정상적으로 완료되었습니다.')

                                        inputNameEntry.delete(0, END)
                                        inputAgeEntry.delete(0, END)
                                        inputGenderEntry.delete(0, END)
                                        inputIdEntry.delete(0, END)
                                        inputPwEntry.delete(0, END)
                                        inputHeightEntry.delete(0, END)
                                        inputWeightEntry.delete(0, END)

                                        loginFrame.lift()
    else:
        messagebox.showinfo('입력 오류', '입력 정보를 다시 확인하세요.')

# ----------------------------------------------------- 각종 페이지 전환 버튼 함수 ----------------------------------------------------------
def goMainScreen():
    insertEditEntries(loginedUser)
    setMainScreen()
    mainScreenFrame.lift()
    inbodyFrameInMainScreenFrame.lift()

def goNotificationScreen():
    showNotificationList()
    notificationFrame.lift()

def goEditTodaysExerciseFrame(): # 메인 (홈) 화면에서 그날의 운동 기록을 수정하는 페이지로 이동하는 함수
    summaryButton.config(bg = 'white', command = goMainScreen)
    editTodaysExerciseButton.config(bg = '#B4FFFC', command = None)

    editTodaysExerciseFrame.lift()

def goInbodyFrameInMainScreenFrame(): # 메인 (홈) 화면에서 인바디 그래프를 확인할 수 있도록 화면 전환하는 함수
    insertEditEntries(loginedUser)
    inbodyFrameInMainScreenFrame.lift()

def goExerciseTimeFrameInMainScreenFrame(): # 메인 (홈) 화면에서 운동 시간 그래프를 확인할 수 있도록 화면 전환하는 함수
    insertEditEntries(loginedUser)
    exerciseTimeFrameInMainScreenFrame.lift()

def goRankFrameInMainScreenFrame(): # 메인 (홈) 화면에서 순위 그래프를 확인할 수 있도록 화면 전환하는 함수
    insertEditEntries(loginedUser)
    rankFrameInMainScreenFrame.lift()

def goExerciseScreen():
    insertEditEntries(loginedUser)
    setExerciseScreen()
    exerciseScreenFrame.lift()

def goCalendarScreen():
    global dataTypeInCalendarScreen
    global markInCalendarScreen
    dataTypeInCalendarScreen = 'inbody'
    markInCalendarScreen = 'day'
    insertEditEntries(loginedUser)
    setCalendarScreen(dataTypeSet = dataTypeInCalendarScreen, optionSet = markInCalendarScreen)

    daysInCalendarScreenButton.config(bg = '#B4FFFC')
    monthsInCalendarScreenButton.config(bg = 'white')
    yearsInCalendarScreenButton.config(bg = 'white')

    inbodyInCalendarScreenButton.config(bg = '#B4FFFC')
    exerciseTimeInCalendarScreenButton.config(bg = 'white')
    walkCountInCalendarScreenButton.config(bg = 'white')
    walkDistanceInCalendarScreenButton.config(bg = 'white')
    sleepTimeInCalendarScreenButton.config(bg = 'white')

    calendarScreenFrame.lift()

def goMypageScreen():
    showBadgeInfo()
    insertEditEntries(loginedUser)
    mypageScreenFrame.lift()

def goFriendsScreen():
    insertEditEntries(loginedUser)
    showFriendListInFriendsScreenFrame()
    friendsScreenFrame.lift()
# -------------------------------------------------------------------------------------------------------------------------------------------

def insertEditEntries(user): # 마이페이지 및 운동 기록 페이지에서, 로그인한 사용자의 정보를 수정하기 전 각종 엔트리에 필드값을 미리 보여주기 위한 함수
    # 마이페이지
    editNameEntry.delete(0, END); editNameEntry.insert(0, user.getName())
    editAgeEntry.delete(0, END); editAgeEntry.insert(0, str(user.getAge()))
    editGenderEntry.delete(0, END); editGenderEntry.insert(0, user.getGender())
    editPwEntry.delete(0, END); editPwEntry.insert(0, user.getPw())
    editHeightEntry.delete(0, END); editHeightEntry.insert(0, str(user.getHeight()))
    editWeightEntry.delete(0, END); editWeightEntry.insert(0, str(user.getWeight()))

    # 운동 기록 페이지
    editAerobicTimeEntry.delete(0, END); editAerobicTimeEntry.insert(0, user.getAerobicTime())
    editAnaerobicTimeEntry.delete(0, END); editAnaerobicTimeEntry.insert(0, user.getAnaerobicTime())
    editWalkCountEntry.delete(0, END); editWalkCountEntry.insert(0, user.getWalkCount())
    editWalkDistacneEntry.delete(0, END); editWalkDistacneEntry.insert(0, user.getWalkDistance())
    editSleepTimeEntry.delete(0, END); editSleepTimeEntry.insert(0, user.getSleepTime())







# ----------------------------------------------- 메인 (홈) 화면 설정 함수 -----------------------------------------------------------

def setMainScreen():
    makeInbodyGraphImage(loginedUser)
    makeExerciseTimeGraphImage(loginedUser)
    makeRankOfFriendsGraphImage(loginedUser)
    inbodyGraphImage.config(file = 'TempGraphs\\inbodyGraphPerDays.png')
    exerciseTimeGraphImage.config(file = 'TempGraphs\\exerciseTimeGraphPerDays.png')
    rankGraphImage.config(file = 'TempGraphs\\rankOfExerciseTimeFor30Days.png')

    summaryButton.config(bg = '#B4FFFC', command = None)
    editTodaysExerciseButton.config(bg = 'white', command = goEditTodaysExerciseFrame)

    if DEBUG:
        lst = loginedUser.getAerobicTimeList()
        print(len(lst))
        for i in range(len(lst)):
            print(lst[i].getData(), end = ' ')
        print()
        lst = loginedUser.getAnaerobicTimeList()
        for i in range(len(lst)):
            print(lst[i], end = ' ')
        print()

####### 그날의 운동 기록을 저장하는 페이지에서, 각종 운동 데이터를 저장하는 버튼과 관련된 함수 #######
def editAerobicTimeCommand(): # 1. 유산소 운동 데이터 저장
    try:
        editedAerobicTime = int(editAerobicTimeEntry.get())
        if editedAerobicTime >= 0:
            loginedUser.setAerobicTime(editedAerobicTime)
            editUsersFile(loginedUser)
            messagebox.showinfo(message = '저장되었습니다.')
        else:
            messagebox.showinfo('입력 오류', '유산소 운동 시간을 다시 입력하세요.')
            insertEditEntries(loginedUser)
    except ValueError:
        messagebox.showinfo('입력 오류', '유산소 운동 시간을 다시 입력하세요.')
        insertEditEntries(loginedUser)

def editAnaerobicTimeCommand(): # 2. 무산소 운동 데이터 저장
    try:
        editedAnaerobicTime = int(editAnaerobicTimeEntry.get())
        if editedAnaerobicTime >= 0:
            loginedUser.setAnaerobicTime(editedAnaerobicTime)
            editUsersFile(loginedUser)
            messagebox.showinfo(message = '저장되었습니다.')
        else:
            messagebox.showinfo('입력 오류', '무산소 운동 시간을 다시 입력하세요.')
            insertEditEntries(loginedUser)
    except ValueError:
        messagebox.showinfo('입력 오류', '무산소 운동 시간을 다시 입력하세요.')
        insertEditEntries(loginedUser)

def editWalkCountCommand(): # 3. 걸음 수 데이터 저장
    try:
        editedWalkCount = int(editWalkCountEntry.get())
        if editedWalkCount >= 0:
            loginedUser.setWalkCount(editedWalkCount)
            editUsersFile(loginedUser)
            messagebox.showinfo(message = '저장되었습니다.')
        else:
            messagebox.showinfo('입력 오류', '걸음 수를 다시 입력하세요.')
            insertEditEntries(loginedUser)
    except ValueError:
        messagebox.showinfo('입력 오류', '걸음 수를 다시 입력하세요.')
        insertEditEntries(loginedUser)

def editWalkDistanceCommand(): # 4. 걸음 거리 데이터 저장
    try:
        editedWalkDistance = float(editWalkDistacneEntry.get())
        if editedWalkDistance >= 0:
            loginedUser.setWalkDistance(editedWalkDistance)
            editUsersFile(loginedUser)
            messagebox.showinfo(message = '저장되었습니다.')
        else:
            messagebox.showinfo('입력 오류', '걷기 거리를 다시 입력하세요.')
            insertEditEntries(loginedUser)
    except ValueError:
        messagebox.showinfo('입력 오류', '걷기 거리를 다시 입력하세요.')
        insertEditEntries(loginedUser)

def editSleepTimeCommand(): # 5. 수면 시간 데이터 저장
    try:
        editedSleepTime = float(editSleepTimeEntry.get())
        if editedSleepTime >= 0:
            loginedUser.setSleepTime(editedSleepTime)
            editUsersFile(loginedUser)
            messagebox.showinfo(message = '저장되었습니다.')
        else:
            messagebox.showinfo('입력 오류', '수면 시간을 다시 입력하세요.')
            insertEditEntries(loginedUser)
    except ValueError:
        messagebox.showinfo('입력 오류', '수면 시간을 다시 입력하세요.')
        insertEditEntries(loginedUser)
####################################################################################################

##################################### 알림 목록과 관련된 함수 ######################################
notificationCardFrameList = [] # 알림 목록을 나타내기 위한 작은 프레임
deleteNotificationsButton = None
noNotificationsMessageLabel = None

def showNotificationList(): # 알림 목록을 보여주는 함수
    for i in range(len(notificationCardFrameList)):
        notificationCardFrameList[i].place_forget()

    framePopCount = len(notificationCardFrameList)
    for i in range(framePopCount):
        notificationCardFrameList.pop()

    lastPositionY = 100
    for i in range(len(loginedUser.getNotificationList())):
        notificationCardFrame = Frame(notificationFrame, bg = 'white', width = 570, height = 65)
        notificationCardFrameList.append(notificationCardFrame)
        notificationCardFrame.place(x = 60, y = 100 + 80 * i)
        lastPositionY += 80

        notificationDataInCard = loginedUser.getNotificationList()[i].getData()
        notificationDateInCard = loginedUser.getNotificationList()[i].getDate()

        notificationDataLabel = Label(notificationCardFrame, text = notificationDataInCard,\
                font = ('Arial', 12, 'bold'), bg = 'white')
        notificationDateLabel = Label(notificationCardFrame, text = '· {}/{}/{}'\
                .format(notificationDateInCard.year, notificationDateInCard.month, notificationDateInCard.day),\
                font = ('Arial', 13, 'bold'), bg = 'white')

        notificationDataLabel.place(x = 10, y = 20)
        notificationDateLabel.place(x = 465, y = 20)

    global deleteNotificationsButton, noNotificationsMessageLabel
    if deleteNotificationsButton != None:
        deleteNotificationsButton.place_forget()
    if noNotificationsMessageLabel != None:
        noNotificationsMessageLabel.place_forget()

    if lastPositionY > 100:
        deleteNotificationsButton = Button(notificationFrame, bg = '#EDFFFB', text = '모두 삭제',\
                font = ('Arial', 10, 'bold'), command = removeAllNotifications)
        deleteNotificationsButton.place(x = 327, y = lastPositionY)
    else:
        noNotificationsMessageLabel = Label(notificationFrame, text = '알림이 없습니다.',\
                font = ('Arial', 15, 'bold'), bg = '#EDFFFB')
        noNotificationsMessageLabel.place(x = 285, y = 350)

def removeAllNotifications():
    loginedUser.resetNotificationList()
    editUsersFile(loginedUser)
    showNotificationList()
####################################################################################################

# ----------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------- 추천 운동 스크린 설정 관련 함수 ---------------------------------------------
exerciseVideoUrl = 'https://www.youtube.com/watch?v=VNQpP6C1fJg'

def setExerciseScreen():
    global exerciseVideoUrl

    fitnessType = Fitness.recommandExercise(loginedUser)
    if fitnessType == Fitness.AEROBIC:
        videoTitleLabel.config(text = '오늘 하루는\n유산소 운동으로 시작해보세요!')

        randData = rd.randint(0, 4)
        if randData == 0:
            exerciseVideoUrl = 'https://www.youtube.com/watch?v=VNQpP6C1fJg'
            videoThumbnailImage.config(file = 'Thumbnails\\aerobicThumbnail1.png')
            videoCommantLabel.config(text = '집에서 하는 유산소운동 다이어트 [칼소폭]')
        elif randData == 1:
            exerciseVideoUrl = 'https://www.youtube.com/watch?v=lKwZ2DU4P-A'
            videoThumbnailImage.config(file = 'Thumbnails\\aerobicThumbnail2.png')
            videoCommantLabel.config(text = '집에서 칼로리 불태우는 최고의 유산소운동[칼소폭\n매운맛]')
        elif randData == 2:
            exerciseVideoUrl = 'https://www.youtube.com/watch?v=t70t-sklypk'
            videoThumbnailImage.config(file = 'Thumbnails\\aerobicThumbnail3.png')
            videoCommantLabel.config(text = '집에서 칼로리 불태우는 걷기 유산소운동 [칼소폭\n순한맛]')
        elif randData == 3:
            exerciseVideoUrl = 'https://www.youtube.com/watch?v=MWnD6DhLjyc'
            videoThumbnailImage.config(file = 'Thumbnails\\aerobicThumbnail4.png')
            videoCommantLabel.config(text = '집에서 칼로리 소모 폭탄 걷기 운동 [칼소폭3]')
        elif randData == 4:
            exerciseVideoUrl = 'https://www.youtube.com/watch?v=wrLlzn5TjLY'
            videoThumbnailImage.config(file = 'Thumbnails\\aerobicThumbnail5.png')
            videoCommantLabel.config(text = '집에서 하는 유산소운동 다이어트 [칼소폭 플러스]')
    elif fitnessType == Fitness.ANAEROBIC:
        videoTitleLabel.config(text = '오늘 하루는\n무산소 운동으로 시작해보세요!')

        # 무산소 운동의 경우 남성용 운동과 여성용 운동을 구분하여 추천해야 한다.
        if loginedUser.getGender() == '남':
            randData = rd.randint(0, 4)
            if randData == 0:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=CKDYo5CeX9E'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForManThumbnail1.png')
                videoCommantLabel.config(text = '집에서 하는 30분 전신 덤벨 운동 - 근육 강화')
            elif randData == 1:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=o-9ZuMtC8MA'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForManThumbnail2.png')
                videoCommantLabel.config(text = '[상체] 집에서 근성장 가능한 덤벨운동 프로그램')
            elif randData == 2:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=xK68FIFWdnI'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForManThumbnail3.png')
                videoCommantLabel.config(text = '집에서 10kg 덤벨로 하는 팔 운동루틴')
            elif randData == 3:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=OtRzXcSLFXQ'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForManThumbnail4.png')
                videoCommantLabel.config(text = '맨몸하체운동 1편(5가지 스쿼트 동작) [5분홈트]')
            elif randData == 4:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=Lts-ddUgSFQ'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForManThumbnail5.png')
                videoCommantLabel.config(text = '하루10분! 어깨 근육을 키우는 덤벨운동 (어깨운동,\n벤치없이)')
        elif loginedUser.getGender() == '여':
            randData = rd.randint(0, 4)
            if randData == 0:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=DWYDL-WxF1U'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForWomanThumbnail1.png')
                videoCommantLabel.config(text = '하체 날, 딱 10분 밖에 없다면 - 스쿼트 10가지 동작\n- 하체운동 홈트 루틴')
            elif randData == 1:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=aKzE3NNFEi4'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForWomanThumbnail2.png')
                videoCommantLabel.config(text = '하루 한 번! 꼭 해야하는 10분 기본 전신근력 운동 홈트\n(층간소음 X)')
            elif randData == 2:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=9zLD6cSgHdY'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForWomanThumbnail3.png')
                videoCommantLabel.config(text = '하루 한 번! 꼭 해야하는 15분 기본 덤벨운동 홈트\n(상체편)')
            elif randData == 3:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=gpTYMAxN0CM'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForWomanThumbnail4.png')
                videoCommantLabel.config(text = '10분 덤벨 서서하는 복근운동 홈트')
            elif randData == 4:
                exerciseVideoUrl = 'https://www.youtube.com/watch?v=C4_2puAkxfs'
                videoThumbnailImage.config(file = 'Thumbnails\\anaerobicForWomanThumbnail5.png')
                videoCommantLabel.config(text = '하루 한 번! 꼭 해야하는 10분 기본 하체근력 운동 홈트\n(층간소음 X)')

def playExerciseVideo(): # 영상 재생 버튼을 눌렀을 경우 운동 유튜브 영상으로 연결되도록 하는 함수
    wb.open_new(exerciseVideoUrl)
# -------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------- 캘린더 스크린 설정 관련 함수 ---------------------------------------------------
def setCalendarScreen(dataTypeSet, optionSet):
    if dataTypeSet == 'inbody':
        makeInbodyGraphImage(loginedUser, option = optionSet, dpiSet = 55)
        if optionSet == 'day':
            exerciseDataGraphImage.config(file = 'TempGraphs\\inbodyGraphPerDays.png')
        elif optionSet == 'month':
            exerciseDataGraphImage.config(file = 'TempGraphs\\inbodyGraphPerMonths.png')
        elif optionSet == 'year':
            exerciseDataGraphImage.config(file = 'TempGraphs\\inbodyGraphPerYears.png')
    elif dataTypeSet == 'exercise time':
        makeExerciseTimeGraphImage(loginedUser, option = optionSet, dpiSet = 55)
        if optionSet == 'day':
            exerciseDataGraphImage.config(file = 'TempGraphs\\exerciseTimeGraphPerDays.png')
        elif optionSet == 'month':
            exerciseDataGraphImage.config(file = 'TempGraphs\\exerciseTimeGraphPerMonths.png')
        elif optionSet == 'year':
            exerciseDataGraphImage.config(file = 'TempGraphs\\exerciseTimeGraphPerYears.png')
    else:
        makeExerciseDataGraphImage(loginedUser, dataType = dataTypeSet, option = optionSet, dpiSet = 55)
        if dataTypeSet == 'walk count':
            if optionSet == 'day':
                exerciseDataGraphImage.config(file = 'TempGraphs\\walkCountGraphPerDays.png')
            elif optionSet == 'month':
                exerciseDataGraphImage.config(file = 'TempGraphs\\walkCountGraphPerMonths.png')
            elif optionSet == 'year':
                exerciseDataGraphImage.config(file = 'TempGraphs\\walkCountGraphPerYears.png')
        elif dataTypeSet == 'walk distance':
            if optionSet == 'day':
                exerciseDataGraphImage.config(file = 'TempGraphs\\walkDistanceGraphPerDays.png')
            elif optionSet == 'month':
                exerciseDataGraphImage.config(file = 'TempGraphs\\walkDistanceGraphPerMonths.png')
            elif optionSet == 'year':
                exerciseDataGraphImage.config(file = 'TempGraphs\\walkDistanceGraphPerYears.png')
        elif dataTypeSet == 'sleep time':
            if optionSet == 'day':
                exerciseDataGraphImage.config(file = 'TempGraphs\\sleepTimeGraphPerDays.png')
            elif optionSet == 'month':
                exerciseDataGraphImage.config(file = 'TempGraphs\\sleepTimeGraphPerMonths.png')
            elif optionSet == 'year':
                exerciseDataGraphImage.config(file = 'TempGraphs\\sleepTimeGraphPerYears.png')

def setGraphFrameDays():
    global markInCalendarScreen
    markInCalendarScreen = 'day'
    setCalendarScreen(dataTypeInCalendarScreen, markInCalendarScreen)

    daysInCalendarScreenButton.config(bg = '#B4FFFC')
    monthsInCalendarScreenButton.config(bg = 'white')
    yearsInCalendarScreenButton.config(bg = 'white')

def setGraphFrameMonths():
    global markInCalendarScreen
    markInCalendarScreen = 'month'
    setCalendarScreen(dataTypeInCalendarScreen, markInCalendarScreen)

    daysInCalendarScreenButton.config(bg = 'white')
    monthsInCalendarScreenButton.config(bg = '#B4FFFC')
    yearsInCalendarScreenButton.config(bg = 'white')

def setGraphFrameYears():
    global markInCalendarScreen
    markInCalendarScreen = 'year'
    setCalendarScreen(dataTypeInCalendarScreen, markInCalendarScreen)

    daysInCalendarScreenButton.config(bg = 'white')
    monthsInCalendarScreenButton.config(bg = 'white')
    yearsInCalendarScreenButton.config(bg = '#B4FFFC')

def setGraphFrameInbody():
    global dataTypeInCalendarScreen
    dataTypeInCalendarScreen = 'inbody'
    setCalendarScreen(dataTypeInCalendarScreen, markInCalendarScreen)

    inbodyInCalendarScreenButton.config(bg = '#B4FFFC')
    exerciseTimeInCalendarScreenButton.config(bg = 'white')
    walkCountInCalendarScreenButton.config(bg = 'white')
    walkDistanceInCalendarScreenButton.config(bg = 'white')
    sleepTimeInCalendarScreenButton.config(bg = 'white')

def setGraphFrameExerciseTime():
    global dataTypeInCalendarScreen
    dataTypeInCalendarScreen = 'exercise time'
    setCalendarScreen(dataTypeInCalendarScreen, markInCalendarScreen)

    inbodyInCalendarScreenButton.config(bg = 'white')
    exerciseTimeInCalendarScreenButton.config(bg = '#B4FFFC')
    walkCountInCalendarScreenButton.config(bg = 'white')
    walkDistanceInCalendarScreenButton.config(bg = 'white')
    sleepTimeInCalendarScreenButton.config(bg = 'white')

def setGraphFrameWalkCount():
    global dataTypeInCalendarScreen
    dataTypeInCalendarScreen = 'walk count'
    setCalendarScreen(dataTypeInCalendarScreen, markInCalendarScreen)

    inbodyInCalendarScreenButton.config(bg = 'white')
    exerciseTimeInCalendarScreenButton.config(bg = 'white')
    walkCountInCalendarScreenButton.config(bg = '#B4FFFC')
    walkDistanceInCalendarScreenButton.config(bg = 'white')
    sleepTimeInCalendarScreenButton.config(bg = 'white')

def setGraphFrameWalkDistance():
    global dataTypeInCalendarScreen
    dataTypeInCalendarScreen = 'walk distance'
    setCalendarScreen(dataTypeInCalendarScreen, markInCalendarScreen)

    inbodyInCalendarScreenButton.config(bg = 'white')
    exerciseTimeInCalendarScreenButton.config(bg = 'white')
    walkCountInCalendarScreenButton.config(bg = 'white')
    walkDistanceInCalendarScreenButton.config(bg = '#B4FFFC')
    sleepTimeInCalendarScreenButton.config(bg = 'white')

def setGraphFrameSleepTime():
    global dataTypeInCalendarScreen
    dataTypeInCalendarScreen = 'sleep time'
    setCalendarScreen(dataTypeInCalendarScreen, markInCalendarScreen)

    inbodyInCalendarScreenButton.config(bg = 'white')
    exerciseTimeInCalendarScreenButton.config(bg = 'white')
    walkCountInCalendarScreenButton.config(bg = 'white')
    walkDistanceInCalendarScreenButton.config(bg = 'white')
    sleepTimeInCalendarScreenButton.config(bg = '#B4FFFC')
# -----------------------------------------------------------------------------------------------------------------------------------------




# ---------------------------------------------- 회원 정보 수정 - 각종 버튼 기능 함수 --------------------------------------------------------
def editNameCommand():
    editedName = editNameEntry.get()
    if editedName == '':
        messagebox.showinfo('입력 오류', '이름을 다시 입력하세요.')
        insertEditEntries(loginedUser)
    else:
        if len(editedName) > 10:
            messagebox.showinfo('입력 오류', '이름은 최대 10자까지만 설정 가능합니다.')
            insertEditEntries(loginedUser)
        else:
            loginedUser.setName(editedName)
            editUsersFile(loginedUser)
            messagebox.showinfo(message = '회원 정보가 정상적으로 변경되었습니다.')

def editAgeCommand():
    try:
        editedAge = int(editAgeEntry.get())
        if editedAge >= 0:
            if editedAge > 150:
                messagebox.showinfo('입력 오류', '나이는 최대 150세까지만 설정 가능합니다.')
                insertEditEntries(loginedUser)
            else:
                loginedUser.setAge(editedAge)
                editUsersFile(loginedUser)
                messagebox.showinfo(message = '회원 정보가 정상적으로 변경되었습니다.')
        else:
            messagebox.showinfo('입력 오류', '나이를 다시 입력하세요.')
            insertEditEntries(loginedUser)
    except ValueError:
        messagebox.showinfo('입력 오류', '나이를 다시 입력하세요.')
        insertEditEntries(loginedUser)

def editGenderCommand():
    editedGender = editGenderEntry.get()
    if editedGender == '남' or editedGender == '여':
        loginedUser.setGender(editedGender)
        editUsersFile(loginedUser)
        messagebox.showinfo(message = '회원 정보가 정상적으로 변경되었습니다.')
    else:
        messagebox.showinfo('입력 오류', '성별을 다시 입력하세요.')
        insertEditEntries(loginedUser)

def editPwCommand():
    editedPw = editPwEntry.get()
    if editedPw == '':
        messagebox.showinfo('입력 오류', 'PW를 다시 입력하세요.')
        insertEditEntries(loginedUser)
    else:
        if len(editedPw) > 10:
            messagebox.showinfo('입력 오류', 'PW는 최대 10자리까지만 설정 가능합니다.')
            insertEditEntries(loginedUser)
        else:
            if len(editedPw) < 4:
                messagebox.showinfo('입력 오류', 'PW는 최소 4자리부터 설정 가능합니다.')
                insertEditEntries(loginedUser)
            else:
                alphabetCount = 0; nonalphabetCount = 0; digitCount = 0
                for i in range(len(editedPw)):
                    if editedPw[i] >= 'A' and editedPw[i] <= 'Z' or editedPw[i] >= 'a' and editedPw[i] <= 'z':
                        alphabetCount += 1
                    elif editedPw[i] >= '0' and editedPw[i] <= '9':
                        digitCount += 1
                    else:
                        nonalphabetCount += 1
                if alphabetCount == 0 or nonalphabetCount == 0 or digitCount == 0:
                    messagebox.showinfo('입력 오류', 'PW에는 최소 영문자 1개, 특수 문자 1개, 숫자 1개 이상 넣어야 합니다.')
                    insertEditEntries(loginedUser)
                else:
                    loginedUser.setPw(editedPw)
                    editUsersFile(loginedUser)
                    messagebox.showinfo(message = '회원 정보가 정상적으로 변경되었습니다.')

def editHeightCommand():
    try:
        editedHeight = float(editHeightEntry.get())
        if editedHeight > 0:
            if editedHeight >= 50 and editedHeight <= 250:
                loginedUser.setHeight(editedHeight)
                editUsersFile(loginedUser)
                messagebox.showinfo(message = '회원 정보가 정상적으로 변경되었습니다.')
            else:
                messagebox.showinfo('입력 오류', '키는 최소 50cm부터 250cm까지만 설정 가능합니다.')
                insertEditEntries(loginedUser)
        else:
            messagebox.show('입력 오류', '키를 다시 입력하세요.')
            insertEditEntries(loginedUser)
    except ValueError:
        messagebox.showinfo('입력 오류', '키를 다시 입력하세요.')
        insertEditEntries(loginedUser)

def editWeightCommand():
    try:
        editedWeight = float(editWeightEntry.get())
        if editedWeight > 0:
            if editedWeight >= 10 and editedWeight <= 150:
                loginedUser.setWeight(editedWeight)
                editUsersFile(loginedUser)
                messagebox.showinfo(message = '회원 정보가 정상적으로 변경되었습니다.')
            else:
                messagebox.showinfo('입력 오류', '몸무게는 최소 10kg부터 150kg까지만 설정 가능합니다.')
        else:
            messagebox.show('입력 오류', '몸무게를 다시 입력하세요.')
            insertEditEntries(loginedUser)
    except ValueError:
        messagebox.showinfo('입력 오류', '몸무게를 다시 입력하세요.')
        insertEditEntries(loginedUser)
# -------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------- 뱃지 보유 여부를 사용자에게 보여주는 함수 ------------------------------------------
def showBadgeInfo():
    exerciseTimeFor30DaysList = []
    friendList = loginedUser.getFriendList()
    for i in range(len(friendList)):
        exerciseTimeFor30DaysList.append(friendList[i].getExerciseTimeFor30Days())
    exerciseTimeFor30DaysList.append(loginedUser.getExerciseTimeFor30Days())

    if loginedUser.getExerciseTimeFor30Days() == max(exerciseTimeFor30DaysList):
        # badgeIcon = PhotoImage('Icons\\BadgeIcon.png')
        badgeInfoLabel.config(text = '🏆', font = ('Arial', 80, 'bold'), fg = '#E8C710')
        badgeInfoLabel.place_forget()
        badgeInfoLabel.place(x = 280, y = 380)
    else:
        badgeInfoLabel.config(text = '보유한 뱃지가 없습니다.', font = ('Arial', 15, 'bold'), fg = 'black')
        badgeInfoLabel.place_forget()
        badgeInfoLabel.place(x = 238, y = 440)
# -------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------ 로그아웃, 탈퇴 관련 각종 함수 -------------------------------------------------------
def logoutCommand():
    select = messagebox.askquestion(message = '정말로 로그아웃하시겠습니까?')
    if select == 'yes':
        loginFrame.lift()

def deleteUserCommand():
    select = messagebox.askquestion('중요', '정말로 탈퇴를 진행하시겠습니까?\n이 작업은 취소할 수 없습니다.')
    if select == 'yes':
        messagebox.showinfo(message = '탈퇴가 완료되었습니다.\n그동안 우리 프로그램을 사용해주셔서 감사합니다.')
        deleteUserInUsersFile(loginedUser)
        idEntry.delete(0, END)
        loginFrame.lift()
# --------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------- 친구 목록 페이지 및 관련 각종 함수 ---------------------------------------------------------------
def addFriendCommand(): # 친구 추가
    usersFile = open('users.bin', 'rb')
    usersList = load(usersFile)
    usersFile.close()

    addedFriendUserId = findUserByIdEntry.get()
    if addedFriendUserId == loginedUser.getId(): # 본인의 아이디를 입력할 수 없도록 해야 함.
        messagebox.showinfo('경고', '자기 자신의 ID는 입력할 수 없습니다.')
    else:
        if findUserById(usersList, addedFriendUserId): # 추가할 친구의 아이디가 사용자 목록에 존재하는 경우
            addedFriendUser = None # 추가하게 될 친구 사용자의 객체를 나타내는 변수
            for i in range(len(usersList)):
                if addedFriendUserId == usersList[i].getId():
                    addedFriendUser = usersList[i]
                    break

            if loginedUser.isFriend(addedFriendUser): # 이미 친구 관계인 경우 친구 추가 기능은 작동하지 않아야 한다.
                messagebox.showinfo(message = '이미 친구로 등록된 ID입니다.')
            else: # 아직 서로 친구 관계가 아닌 경우 친구 추가 기능을 작동시킨다.
                if len(loginedUser.getFriendList()) >= 5 or len(addedFriendUser.getFriendList()) >= 5: # 최대 5명까지만 친구 등록 가능!
                    messagebox.showinfo(message = '친구는 최대 5명까지만 등록 가능합니다.')
                else:
                    loginedUser.addFriend(addedFriendUser)
                    editUsersFile(loginedUser)
                    showFriendListInFriendsScreenFrame()
                    messagebox.showinfo(message = '친구 등록이 완료되었습니다.')
        else: # 추가할 친구의 아이디가 사용자 목록에 존재하지 않는 경우 - 친구 추가 기능이 제대로 작동될 수 없음.
            messagebox.showinfo(message = '해당 ID는 존재하지 않습니다.')

    findUserByIdEntry.delete(0, END)

def deleteFriendCommand():
    usersFile = open('users.bin', 'rb')
    usersList = load(usersFile)
    usersFile.close()

    deletedFriendUserId = findUserByIdEntry.get()
    if deletedFriendUserId == loginedUser.getId():
        messagebox.showinfo('경고', '자기 자신의 ID는 입력할 수 없습니다.') # 본인의 아이디를 입력할 수 없도록 해야 함.
    else:
        if findUserById(usersList, deletedFriendUserId):
            deletedFriendUser = None # 삭제하게 될 친구 사용자의 객체를 나타내는 함수
            for i in range(len(usersList)):
                if deletedFriendUserId == usersList[i].getId():
                    deletedFriendUser = usersList[i]
                    break

            if loginedUser.isFriend(deletedFriendUser): # 친구 관계인 경우에만 친구 삭제 기능이 작동해야 한다.
                loginedUser.deleteFriend(deletedFriendUser)
                editUsersFile(loginedUser)
                editUsersFile(deletedFriendUser)
                showFriendListInFriendsScreenFrame()
                messagebox.showinfo(message = '친구 삭제가 완료되었습니다.')
            else:
                messagebox.showinfo(message = '친구로 등록되지 않는 ID입니다.')
        else: # 삭제할 친구의 아이디가 사용자 목록에 존재하지 않는 경우 - 친구 삭제 기능이 제대로 작동될 수 없음.
            messagebox.showinfo(message = '해당 ID는 존재하지 않습니다.')

    findUserByIdEntry.delete(0, END)



friendCardFrameList = [] # 친구 목록을 나타내기 위한 작은 프레임
noFriendsMessageLabel = None


def showFriendListInFriendsScreenFrame(): # 친구 페이지에서 친구 목록을 보여주는 함수
    exerciseTimeFor30DaysList = []
    friendList = loginedUser.getFriendList()
    for i in range(len(friendList)):
        exerciseTimeFor30DaysList.append(friendList[i].getExerciseTimeFor30Days())
    exerciseTimeFor30DaysList.append(loginedUser.getExerciseTimeFor30Days())

    for i in range(len(friendCardFrameList)):
        friendCardFrameList[i].place_forget()

    framePopCount = len(friendCardFrameList)
    for i in range(framePopCount):
        friendCardFrameList.pop()

    global noFriendsMessageLabel
    if noFriendsMessageLabel != None:
        noFriendsMessageLabel.place_forget()

    if len(friendList) > 0:
        for i in range(len(loginedUser.getFriendList())):
            friendCardFrame = Frame(friendsScreenFrame, bg = 'white', width = 570, height = 65)
            friendCardFrameList.append(friendCardFrame)
            friendCardFrame.place(x = 60, y = 150 + 80 * i)

            friendIdInCard = loginedUser.getFriendList()[i].getId()
            friendNameInCard = loginedUser.getFriendList()[i].getName()
            friendHeightInCard = '{:.1f}cm'.format(loginedUser.getFriendList()[i].getHeight())
            friendWeightInCard = '{:.1f}kg'.format(loginedUser.getFriendList()[i].getWeight())
            friendBmiInCard = 'BMI: {:.2f}'.format(loginedUser.getFriendList()[i].getBmi())

            friendIdLabel = Label(friendCardFrame, text = friendIdInCard, font = ('Arial', 12, 'bold'), bg = 'white')
            friendIdLabel.place(x = 10, y = 5)

            friendNameLabel = Label(friendCardFrame, text = friendNameInCard, font = ('Arial', 12, 'bold'), bg = 'white')
            friendNameLabel.place(x = 10, y = 35)

            friendHeightLabel = Label(friendCardFrame, text = friendHeightInCard, font = ('Arial', 15, 'bold'), bg = 'white')
            friendHeightLabel.place(x = 165, y = 20)

            seperatorLabel = Label(friendCardFrame, text = '|', font = ('Arial', 15, 'bold'), bg = 'white')
            seperatorLabel.place(x = 265, y = 20)

            friendWeightLabel = Label(friendCardFrame, text = friendWeightInCard, font = ('Arial', 15, 'bold'), bg = 'white')
            friendWeightLabel.place(x = 295, y = 20)

            friendBmiLabel = Label(friendCardFrame, text = friendBmiInCard, font = ('Arial', 15, 'bold'), bg = 'white')
            friendBmiLabel.place(x = 400, y = 20)

            # 운동 시간이 1등인 사용자에게는 뱃지를 부여해야 한다.
            if loginedUser.getFriendList()[i].getExerciseTimeFor30Days()\
                    == max(exerciseTimeFor30DaysList):
                badgeLabel = Label(friendCardFrame, text = '🏆', font = ('Arial', 30, 'bold'), bg = 'white', fg = '#E8C710')
                badgeLabel.place(x = 520, y = 1)
    else:
        noFriendsMessageLabel = Label(friendsScreenFrame, text = '친구 목록이 없습니다.', bg = '#EDFFFB',\
                font = ('Arial', 15, 'bold'))
        noFriendsMessageLabel.place(x = 245, y = 285)
# --------------------------------------------------------------------------------------------------------------------------------------------















window = Tk()
window.title('Fit Checker')
window.geometry('700x700')



fitCheckerBackground = PhotoImage(file = 'Icons\\FitChecker.png')
# fitnessBackground = PhotoImage(file = 'Icons\\FitnessBackground.png')

# ---------------------------------------------------- 로그인 화면 -------------------------------------------------------------

loginFrame = Frame(window, bg = '#EDFFFB', width = 800, height = 800)
backgroundInLoginFrame = Label(loginFrame, image = fitCheckerBackground, width = 800, height = 800)
backgroundInLoginFrame.place(x = -50, y = -50)
loginFrame.place(x = 0, y = 0)
openFrame(loginFrame)

# 1. 타이틀 레이블
programLabel = Label(loginFrame, text = '운동 관리 프로그램', font = ('Arial', 30, 'bold'), bg = '#EDFFFB')
# programLabel.place(x = 175, y = 130)

# 2. id, pw 입력
idLabel = Label(loginFrame, text = 'ID', font = ('Arial', 20, 'bold'), bg = '#EDFFFB', width = 3)
pwLabel = Label(loginFrame, text = 'PW', font = ('Arial', 20, 'bold'), bg = '#EDFFFB', width = 3)

idLabel.place(x = 140, y = 320)
pwLabel.place(x = 140, y = 400)

idEntry = Entry(loginFrame, font = ('Arial', 20))
pwEntry = Entry(loginFrame, show = '●', font = ('Arial', 20))

idEntry.place(x = 220, y = 320)
pwEntry.place(x = 220, y = 400)

# 3. 로그인 / 회원가입
loginButton = Button(loginFrame, text = '로그인', font = ('Arial', 17, 'bold'), bg = '#B4FFFC', width = 8, command = loginCommand)
assignButton = Button(loginFrame, text = '회원가입', font = ('Arial', 17, 'bold'), bg = '#B4FFFC', width = 8, command = assignCommand)

loginButton.place(x = 210, y = 500)
assignButton.place(x = 360, y = 500)

# -------------------------------------------------------------------------------------------------------------------------------









# -------------------------------------- 회원가입 화면 --------------------------------------------------------------------------
assignFrame = Frame(window, bg = '#EDFFFB', width = 800, height = 800)
assignFrame.place(x = 0, y = 0)

assignLabel = Label(assignFrame, text = '회원가입', font = ('Arial', 35, 'bold'), bg = '#EDFFFB')
assignLabel.place(x = 250, y = 80)

# 1. 회원 정보 입력 필드 요소
inputNameLabel = Label(assignFrame, text = '이름', font = ('Arial', 18, 'bold'), bg = '#EDFFFB')
inputAgeLabel = Label(assignFrame, text = '나이(만)', font = ('Arial', 18, 'bold'), bg = '#EDFFFB')
inputGenderLabel = Label(assignFrame, text = '성별(남/여)', font = ('Arial', 18, 'bold'), bg = '#EDFFFB')
inputIdLabel = Label(assignFrame, text = 'ID', font = ('Arial', 18, 'bold'), bg = '#EDFFFB')
inputPwLabel = Label(assignFrame, text = 'PW', font = ('Arial', 18, 'bold'), bg = '#EDFFFB')
inputHeightLabel = Label(assignFrame, text = '키(cm)', font = ('Arial', 18, 'bold'), bg = '#EDFFFB')
inputWeightLabel = Label(assignFrame, text = '몸무게(kg)', font = ('Arial', 18, 'bold'), bg = '#EDFFFB')

inputNameEntry = Entry(assignFrame, font = ('Arial', 18), width = 23)
inputAgeEntry = Entry(assignFrame, font = ('Arial', 18), width = 23)
inputGenderEntry = Entry(assignFrame, font = ('Arial', 18), width = 23)
inputIdEntry = Entry(assignFrame, font = ('Arial', 18), width = 23)
inputPwEntry = Entry(assignFrame, show = '●', font = ('Arial', 18), width = 23)
inputHeightEntry = Entry(assignFrame, font = ('Arial', 18), width = 23)
inputWeightEntry = Entry(assignFrame, font = ('Arial', 18), width = 23)

inputNameLabel.place(x = 120, y = 200); inputNameEntry.place(x = 250, y = 200)
inputAgeLabel.place(x = 120, y = 250); inputAgeEntry.place(x = 250, y = 250)
inputGenderLabel.place(x = 120, y = 300); inputGenderEntry.place(x = 250, y = 300)
inputIdLabel.place(x = 120, y = 350); inputIdEntry.place(x = 250, y = 350)
inputPwLabel.place(x = 120, y = 400); inputPwEntry.place(x = 250, y = 400)
inputHeightLabel.place(x = 120, y = 450); inputHeightEntry.place(x = 250, y = 450)
inputWeightLabel.place(x = 120, y = 500); inputWeightEntry.place(x = 250, y = 500)

# 2. 회원 정보 저장 요소
cancelAssignButton = Button(assignFrame, text = '취소', font = ('Arial', 17, 'bold'), bg = '#B4FFFC', width = 8, command = cancelAssignCommand)
saveUserInfoButton = Button(assignFrame, text = '저장', font = ('Arial', 17, 'bold'), bg = '#B4FFFC', width = 8, command = saveUserInfoCommand)

cancelAssignButton.place(x = 210, y = 570)
saveUserInfoButton.place(x = 360, y = 570)

# -------------------------------------------------------------------------------------------------------------------------------









# ----------------------------------------------------------------- 각종 아이콘 -------------------------------------------------
# 1. 선택되지 않은 상태의 아이콘
homeIcon = PhotoImage(file = 'Icons\\HomeIcon.png')
exerciseIcon = PhotoImage(file = 'Icons\\ExerciseIcon.png')
calendarIcon = PhotoImage(file = 'Icons\\CalendarIcon.png')
myIcon = PhotoImage(file = 'Icons\\MyIcon.png')
friendsIcon = PhotoImage(file = 'Icons\\FriendsIcon.png')

# 2. 선택된 상태의 아이콘
selectedHomeIcon = PhotoImage(file = 'Icons\\SelectedHomeIcon.png')
selectedExerciseIcon = PhotoImage(file = 'Icons\\SelectedExerciseIcon.png')
selectedCalendarIcon = PhotoImage(file = 'Icons\\SelectedCalendarIcon.png')
selectedMyIcon = PhotoImage(file = 'Icons\\SelectedMyIcon.png')
selectedFriendsIcon = PhotoImage(file = 'Icons\\SelectedFriendsIcon.png')
# -------------------------------------------------------------------------------------------------------------------------------








# ------------------------------------------------ 1. 메인(홈) 화면 ---------------------------------------------------------
mainScreenFrame = Frame(window, bg = '#EDFFFB', width = 800, height = 800)
mainScreenFrame.place(x = 0, y = 0)



mainTitleLabel = Label(mainScreenFrame, text = '홈', font = ('Arial', 25, 'bold'), bg = '#EDFFFB')
mainTitleLabel.place(x = 325, y = 20)

iconsFrameInMainScreen = Frame(mainScreenFrame, width = 650, height = 145, bg = '#E6F7F3')
iconsFrameInMainScreen.place(x = 25, y = 535)

exerciseButton = Button(mainScreenFrame, image = exerciseIcon, width = 85, height = 85, bg = 'white', command = goExerciseScreen)
exerciseButtonTitle = Label(mainScreenFrame, text = '운동', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

exerciseButton.place(x = 55, y = 545)
exerciseButtonTitle.place(x = 55, y = 645)

calendarButton = Button(mainScreenFrame, image = calendarIcon, width = 85, height = 85, bg = 'white', command = goCalendarScreen)
calendarButtonTitle = Label(mainScreenFrame, text = '캘린더', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

calendarButton.place(x = 180, y = 545)
calendarButtonTitle.place(x = 180, y = 645)

selectedHomeButton = Button(mainScreenFrame, image = selectedHomeIcon, width = 85, height = 85, bg = 'white')
selectedHomeButtonTitle = Label(mainScreenFrame, text = '홈', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

selectedHomeButton.place(x = 305, y = 545)
selectedHomeButtonTitle.place(x = 305, y = 645)

myButton = Button(mainScreenFrame, image = myIcon, width = 85, height = 85, bg = 'white', command = goMypageScreen)
myButtonTitle = Label(mainScreenFrame, text = 'My', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

myButton.place(x = 430, y = 545)
myButtonTitle.place(x = 430, y = 645)

friendsButton = Button(mainScreenFrame, image = friendsIcon, width = 85, height = 85, bg = 'white', command = goFriendsScreen)
friendsButtonTitle = Label(mainScreenFrame, text = '친구', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

friendsButton.place(x = 555, y = 545)
friendsButtonTitle.place(x = 555, y = 645)

############################# 알림 창으로 넘어갈 수 있는 버튼 ##################################
notificationIcon = PhotoImage(file = 'Icons\\Notificationicon.png')
notificationButton = Button(mainScreenFrame, image = notificationIcon,\
        width = 40, height = 40, bg = 'white', command = goNotificationScreen)
notificationButton.place(x = 25, y = 15)
###############################################################################################

############### 메인 (홈) 화면에는 알림 목록을 볼 수 있는 프레임이 필요하다. ###################
notificationFrame = Frame(window, bg = '#EDFFFB', width = 800, height = 800)
notificationFrame.place(x = 0, y = 0)

notificationTitleLabel = Label(notificationFrame, text = '알림', font = ('Arial', 25, 'bold'), bg = '#EDFFFB')
notificationTitleLabel.place(x = 325, y = 20)

backToMainScreenFrame = Button(notificationFrame, text = '< 홈', font = ('Arial', 14, 'bold'), bg = '#EDFFFB', command = goMainScreen)
backToMainScreenFrame.place(x = 25, y = 15)
###############################################################################################




############################# 요약 페이지로 넘어갈 수 있는 버튼 ################################
summaryButton = Button(mainScreenFrame, text = '요약',\
        font = ('Arial', 16, 'bold'), width = 7, bg = '#B4FFFC')
summaryButton.place(x = 455, y = 20)
###############################################################################################
############################# 운동 기록 페이지로 넘어갈 수 있는 버튼 ###########################
editTodaysExerciseButton = Button(mainScreenFrame, text = '운동 기록'\
        , font = ('Arial', 16, 'bold'), bg = 'white', width = 7, command = goEditTodaysExerciseFrame)
editTodaysExerciseButton.place(x = 565, y = 20)
###############################################################################################

######### 메인 (홈) 화면에는 각종 그래프 및 기타 데이터를 표시하기 위한 프레임임과, 그날의 운동을 기록할 수 있는 프레임임이 별도로 필요함. ########
# 1. 인바디 프레임
inbodyFrameInMainScreenFrame = Frame(mainScreenFrame, bg = 'white', width = 650, height = 450)
inbodyFrameInMainScreenFrame.place(x = 25, y = 75)

inbodyInMainScreenButton = Button(inbodyFrameInMainScreenFrame, text = '인바디', width = 10\
        , font = ('Arial', 14, 'bold'), bg = '#B4FFFC')
exerciseTimeInMainScreenButton = Button(inbodyFrameInMainScreenFrame, text = '운동 시간', width = 10\
        , font = ('Arial', 14, 'bold'), bg = 'white', command = goExerciseTimeFrameInMainScreenFrame)
rankInMainScreenButton = Button(inbodyFrameInMainScreenFrame, text = '순위', width = 10\
        , font = ('Arial', 14, 'bold'), bg = 'white', command = goRankFrameInMainScreenFrame)

inbodyInMainScreenButton.place(x = 110, y = 20)
exerciseTimeInMainScreenButton.place(x = 260, y = 20)
rankInMainScreenButton.place(x = 410, y = 20)

makeInbodyGraphImage(loginedUser)
inbodyGraphImage = PhotoImage(file = 'TempGraphs\\inbodyGraphPerDays.png')
inbodyGraphLabel = Label(inbodyFrameInMainScreenFrame,\
        image = inbodyGraphImage, width = 480, height = 360, bg = 'white')
inbodyGraphLabel.place(x = 82, y = 70)

# 2. 운동 시간 프레임
exerciseTimeFrameInMainScreenFrame = Frame(mainScreenFrame, bg = 'white', width = 650, height = 450)
exerciseTimeFrameInMainScreenFrame.place(x = 25, y = 75)

inbodyInMainScreenButton = Button(exerciseTimeFrameInMainScreenFrame, text = '인바디', width = 10\
        , font = ('Arial', 14, 'bold'), bg = 'white', command = goInbodyFrameInMainScreenFrame)
exerciseTimeInMainScreenButton = Button(exerciseTimeFrameInMainScreenFrame, text = '운동 시간', width = 10\
        , font = ('Arial', 14, 'bold'), bg = '#B4FFFC')
rankInMainScreenButton = Button(exerciseTimeFrameInMainScreenFrame, text = '순위', width = 10\
        , font = ('Arial', 14, 'bold'), bg = 'white', command = goRankFrameInMainScreenFrame)

inbodyInMainScreenButton.place(x = 110, y = 20)
exerciseTimeInMainScreenButton.place(x = 260, y = 20)
rankInMainScreenButton.place(x = 410, y = 20)

makeExerciseTimeGraphImage(loginedUser)
exerciseTimeGraphImage = PhotoImage(file = 'TempGraphs\\exerciseTimeGraphPerDays.png')
exerciseTimeGraphLabel = Label(exerciseTimeFrameInMainScreenFrame,\
        image = exerciseTimeGraphImage, width = 480, height = 360, bg = 'white')
exerciseTimeGraphLabel.place(x = 82, y = 70)

# 3. 순위 프레임
rankFrameInMainScreenFrame = Frame(mainScreenFrame, bg = 'white', width = 650, height = 450)
rankFrameInMainScreenFrame.place(x = 25, y = 75)

inbodyInMainScreenButton = Button(rankFrameInMainScreenFrame, text = '인바디', width = 10\
        , font = ('Arial', 14, 'bold'), bg = 'white', command = goInbodyFrameInMainScreenFrame)
exerciseTimeInMainScreenButton = Button(rankFrameInMainScreenFrame, text = '운동 시간', width = 10\
        , font = ('Arial', 14, 'bold'), bg = 'white', command = goExerciseTimeFrameInMainScreenFrame)
rankInMainScreenButton = Button(rankFrameInMainScreenFrame, text = '순위', width = 10\
        , font = ('Arial', 14, 'bold'), bg = '#B4FFFC')

inbodyInMainScreenButton.place(x = 110, y = 20)
exerciseTimeInMainScreenButton.place(x = 260, y = 20)
rankInMainScreenButton.place(x = 410, y = 20)

makeRankOfFriendsGraphImage(loginedUser)
rankGraphImage = PhotoImage(file = 'TempGraphs\\rankOfExerciseTimeFor30Days.png')
rankGraphLabel = Label(rankFrameInMainScreenFrame,\
        image = rankGraphImage, width = 480, height = 360, bg = 'white')
rankGraphLabel.place(x = 82, y = 70)

# 4. 그날의 운동을 기록할 수 있는 프레임
editTodaysExerciseFrame = Frame(mainScreenFrame, bg = 'white', width = 650, height = 450)
editTodaysExerciseFrame.place(x = 25, y = 75)

editAerobicTimeLabel = Label(editTodaysExerciseFrame, text = '유산소 운동 시간(min)'\
        , font = ('Arial', 16, 'bold'), bg = 'white')
editAnaereobicTimeLabel = Label(editTodaysExerciseFrame, text = '무산소 운동 시간(min)'\
        , font = ('Arial', 16, 'bold'), bg = 'white')
editWalkCountLabel = Label(editTodaysExerciseFrame, text = '걸음 수'\
        , font = ('Arial', 16, 'bold'), bg = 'white')
editWalkDistacneLabel = Label(editTodaysExerciseFrame, text = '걷기 거리(km)'\
        , font = ('Arial', 16, 'bold'), bg = 'white')
editSleepTimeLabel = Label(editTodaysExerciseFrame, text = '수면 시간(hour)'\
        , font = ('Arial', 16, 'bold'), bg = 'white')

editAerobicTimeEntry = Entry(editTodaysExerciseFrame, font = ('Arial', 16), width = 18)
editAnaerobicTimeEntry = Entry(editTodaysExerciseFrame, font = ('Arial', 16), width = 18)
editWalkCountEntry = Entry(editTodaysExerciseFrame, font = ('Arial', 16), width = 18)
editWalkDistacneEntry = Entry(editTodaysExerciseFrame, font = ('Arial', 16), width = 18)
editSleepTimeEntry = Entry(editTodaysExerciseFrame, font = ('Arial', 16), width = 18)

editAerobicTimeButton = Button(editTodaysExerciseFrame, text = '저장', font = ('Arial', 11, 'bold')\
        ,bg = '#B4FFFC', command = editAerobicTimeCommand)
editAnaereobicTimeButton = Button(editTodaysExerciseFrame, text = '저장', font = ('Arial', 11, 'bold')\
        , bg = '#B4FFFC', command = editAnaerobicTimeCommand)
editWalkCountButton = Button(editTodaysExerciseFrame, text = '저장', font = ('Arial', 11, 'bold')\
        , bg = '#B4FFFC', command = editWalkCountCommand)
editWalkDistanceButton = Button(editTodaysExerciseFrame, text = '저장', font = ('Arial', 11, 'bold')\
        , bg = '#B4FFFC', command = editWalkDistanceCommand)
editSleepTimeButton = Button(editTodaysExerciseFrame, text = '저장', font = ('Arial', 11, 'bold')\
        , bg = '#B4FFFC', command = editSleepTimeCommand)

editExerciseDataTitle = Label(editTodaysExerciseFrame, text = '오늘의 운동 데이터를 저장해보세요!',\
        font = ('Arial', 20, 'bold'), bg = 'white')
editExerciseDataTitle.place(x = 95, y = 45)

# 각종 운동 기록 데이터를 반영한 총 칼로리 소모량을 표시하기 위한 레이블
editAerobicTimeLabel.place(x = 55, y = 130); editAerobicTimeEntry.place(x = 285, y = 130); editAerobicTimeButton.place(x = 530, y = 130)
editAnaereobicTimeLabel.place(x = 55, y = 190); editAnaerobicTimeEntry.place(x = 285, y = 190); editAnaereobicTimeButton.place(x = 530, y = 190)
editWalkCountLabel.place(x = 55, y = 250); editWalkCountEntry.place(x = 285, y = 250); editWalkCountButton.place(x = 530, y = 250)
editWalkDistacneLabel.place(x = 55, y = 310); editWalkDistacneEntry.place(x = 285, y = 310); editWalkDistanceButton.place(x = 530, y = 310)
editSleepTimeLabel.place(x = 55, y = 370); editSleepTimeEntry.place(x = 285, y = 370); editSleepTimeButton.place(x = 530, y = 370)
#################################################################################################

# -------------------------------------------------------------------------------------------------------------------------







# ------------------------------------------------ 2. 운동 페이지 화면 ---------------------------------------------------------
exerciseScreenFrame = Frame(window, bg = '#EDFFFB', width = 800, height = 800)
exerciseScreenFrame.place(x = 0, y = 0)

exerciseTitleLabel = Label(exerciseScreenFrame, text = '추천 운동', font = ('Arial', 25, 'bold'), bg = '#EDFFFB')
exerciseTitleLabel.place(x = 270, y = 20)

iconsFrameInExerciseScreen = Frame(exerciseScreenFrame, width = 650, height = 145, bg = '#E6F7F3')
iconsFrameInExerciseScreen.place(x = 25, y = 535)

selectedExerciseButton = Button(exerciseScreenFrame, image = selectedExerciseIcon, width = 85, height = 85, bg = 'white')
selectedExerciseButtonTitle = Label(exerciseScreenFrame, text = '운동', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

selectedExerciseButton.place(x = 55, y = 545)
selectedExerciseButtonTitle.place(x = 55, y = 645)

calendarButton = Button(exerciseScreenFrame, image = calendarIcon, width = 85, height = 85, bg = 'white', command = goCalendarScreen)
calendarButtonTitle = Label(exerciseScreenFrame, text = '캘린더', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

calendarButton.place(x = 180, y = 545)
calendarButtonTitle.place(x = 180, y = 645)

homeButton = Button(exerciseScreenFrame, image = homeIcon, width = 85, height = 85, bg = 'white', command = goMainScreen)
homeButtonTitle = Label(exerciseScreenFrame, text = '홈', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

homeButton.place(x = 305, y = 545)
homeButtonTitle.place(x = 305, y = 645)

myButton = Button(exerciseScreenFrame, image = myIcon, width = 85, height = 85, bg = 'white', command = goMypageScreen)
myButtonTitle = Label(exerciseScreenFrame, text = 'My', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

myButton.place(x = 430, y = 545)
myButtonTitle.place(x = 430, y = 645)

friendsButton = Button(exerciseScreenFrame, image = friendsIcon, width = 85, height = 85, bg = 'white', command = goFriendsScreen)
friendsButtonTitle = Label(exerciseScreenFrame, text = '친구', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

friendsButton.place(x = 555, y = 545)
friendsButtonTitle.place(x = 555, y = 645)



videoFrameInExerciseScreenFrame = Frame(exerciseScreenFrame, width = 650, height = 450, bg = 'white')
videoFrameInExerciseScreenFrame.place(x = 25, y = 75)

videoTitleLabel = Label(videoFrameInExerciseScreenFrame, text = '오늘 하루는\n유산소 운동으로 시작해보세요!',\
        font = ('Arial', 20, 'bold'), bg = 'white')
videoTitleLabel.place(x = 130, y = 10)

videoThumbnailImage = PhotoImage(file = 'Thumbnails\\aerobicThumbnail1.png')
videoThumbnailLabel = Label(videoFrameInExerciseScreenFrame, image = videoThumbnailImage,\
        width = 480, height = 240)
videoThumbnailLabel.place(x = 80, y = 80)

videoCommantLabel = Label(videoFrameInExerciseScreenFrame, text = '집에서 하는 유산소운동 다이어트 [칼소폭]',\
        justify = 'left', font = ('Arial', 14, 'bold'), bg = 'white')
videoCommantLabel.place(x = 80, y = 330)

playExerciseVideoButton = Button(videoFrameInExerciseScreenFrame, text = '시작', font = ('Arial', 17, 'bold'),\
        bg = '#B4FFFC', width = 7, command = playExerciseVideo)
playExerciseVideoButton.place(x = 269, y = 385)
# -------------------------------------------------------------------------------------------------------------------------






# ------------------------------------------------ 3. 캘린더 페이지 화면 ---------------------------------------------------------
calendarScreenFrame = Frame(window, bg = '#EDFFFB', width = 800, height = 800)
calendarScreenFrame.place(x = 0, y = 0)


calendarTitleLabel = Label(calendarScreenFrame, text = '캘린더', font = ('Arial', 25, 'bold'), bg = '#EDFFFB')
calendarTitleLabel.place(x = 298, y = 20)

iconsFrameInCalendarScreen = Frame(calendarScreenFrame, width = 650, height = 145, bg = '#E6F7F3')
iconsFrameInCalendarScreen.place(x = 25, y = 535)

exerciseButton = Button(calendarScreenFrame, image = exerciseIcon, width = 85, height = 85, bg = 'white', command = goExerciseScreen)
exerciseButtonTitle = Label(calendarScreenFrame, text = '운동', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

exerciseButton.place(x = 55, y = 545)
exerciseButtonTitle.place(x = 55, y = 645)

selectedCalendarButton = Button(calendarScreenFrame, image = selectedCalendarIcon, width = 85, height = 85, bg = 'white')
selectedCalendarButtonTitle = Label(calendarScreenFrame, text = '캘린더', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

selectedCalendarButton.place(x = 180, y = 545)
selectedCalendarButtonTitle.place(x = 180, y = 645)

homeButton = Button(calendarScreenFrame, image = homeIcon, width = 85, height = 85, bg = 'white', command = goMainScreen)
homeButtonTitle = Label(calendarScreenFrame, text = '홈', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

homeButton.place(x = 305, y = 545)
homeButtonTitle.place(x = 305, y = 645)

myButton = Button(calendarScreenFrame, image = myIcon, width = 85, height = 85, bg = 'white', command = goMypageScreen)
myButtonTitle = Label(calendarScreenFrame, text = 'My', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

myButton.place(x = 430, y = 545)
myButtonTitle.place(x = 430, y = 645)

friendsButton = Button(calendarScreenFrame, image = friendsIcon, width = 85, height = 85, bg = 'white', command = goFriendsScreen)
friendsButtonTitle = Label(calendarScreenFrame, text = '친구', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

friendsButton.place(x = 555, y = 545)
friendsButtonTitle.place(x = 555, y = 645)



###### 캘린데 페이지 화면에는 일별, 월별, 년도별 각종 데이터를 표시하기 위한 각각의 페이지가 존재해야 하며, ######
######                       해당 페이지는 전환할 수 있도록 구현되어야 한다.                               ######
markInCalendarScreen = 'day' # 날짜, 월, 년도 중 어떤 기준값을 설정할 것인지 결정
dataTypeInCalendarScreen = 'inbody' # 어떤 종류의 운동 데이터를 나타낼 것인지 결정

# 캘린더 페이지 한에 흰색 프레임을 덧대기 위해 설정할 Frame 객체
whiteFrameInCalendarScreenFrame = Frame(calendarScreenFrame, bg = 'white', width = 650, height = 450)
whiteFrameInCalendarScreenFrame.place(x = 25, y = 75)

daysInCalendarScreenButton = Button(whiteFrameInCalendarScreenFrame, text = '일별', width = 10,\
        font = ('Arial', 14, 'bold'), bg = '#B4FFFC', command = setGraphFrameDays)
monthsInCalendarScreenButton = Button(whiteFrameInCalendarScreenFrame, text = '월별', width = 10,\
        font = ('Arial', 14, 'bold'), bg = 'white', command = setGraphFrameMonths)
yearsInCalendarScreenButton = Button(whiteFrameInCalendarScreenFrame, text = '년도별', width = 10,\
        font = ('Arial', 14, 'bold'), bg = 'white', command = setGraphFrameYears)

inbodyInCalendarScreenButton = Button(whiteFrameInCalendarScreenFrame, text = '인바디', width = 7,\
        font = ('Arial', 12, 'bold'), bg = '#B4FFFC', command = setGraphFrameInbody)
exerciseTimeInCalendarScreenButton = Button(whiteFrameInCalendarScreenFrame, text = '운동 시간', width = 7,\
        font = ('Arial', 12, 'bold'), bg = 'white', command = setGraphFrameExerciseTime)
walkCountInCalendarScreenButton = Button(whiteFrameInCalendarScreenFrame, text = '걸음 수', width = 7,\
        font = ('Arial', 12, 'bold'), bg = 'white', command = setGraphFrameWalkCount)
walkDistanceInCalendarScreenButton = Button(whiteFrameInCalendarScreenFrame, text = '걷기 거리', width = 7,
        font = ('Arial', 12, 'bold'), bg = 'white', command = setGraphFrameWalkDistance)
sleepTimeInCalendarScreenButton = Button(whiteFrameInCalendarScreenFrame, text = '수면 시간', width = 7,\
        font = ('Arial', 12, 'bold'), bg = 'white', command = setGraphFrameSleepTime)

daysInCalendarScreenButton.place(x = 110, y = 20)
monthsInCalendarScreenButton.place(x = 260, y = 20)
yearsInCalendarScreenButton.place(x = 410, y = 20)

inbodyInCalendarScreenButton.place(x = 105, y = 400)
exerciseTimeInCalendarScreenButton.place(x = 195, y = 400)
walkCountInCalendarScreenButton.place(x = 285, y = 400)
walkDistanceInCalendarScreenButton.place(x = 375, y = 400)
sleepTimeInCalendarScreenButton.place(x = 465, y = 400)

makeInbodyGraphImage(loginedUser, option = 'day', dpiSet = 55)

exerciseDataGraphImage = PhotoImage(file = 'TempGraphs\\inbodyGraphPerDays.png')
inbodyPerDaysGraphLabel = Label(whiteFrameInCalendarScreenFrame,\
        image = exerciseDataGraphImage, width = 352, height = 264, bg = 'white')
inbodyPerDaysGraphLabel.place(x = 145, y = 85)
# -------------------------------------------------------------------------------------------------------------------------







# ------------------------------------------------ 4. 마이 페이지 화면 ---------------------------------------------------------
mypageScreenFrame = Frame(window, bg = '#EDFFFB', width = 800, height = 800)
mypageScreenFrame.place(x = 0, y = 0)


mypageTitleLabel = Label(mypageScreenFrame, text = '마이페이지', font = ('Arial', 25, 'bold'), bg = '#EDFFFB')
mypageTitleLabel.place(x = 260, y = 20)

iconsFrameInMypageScreen = Frame(mypageScreenFrame, width = 650, height = 145, bg = '#E6F7F3')
iconsFrameInMypageScreen.place(x = 25, y = 535)

exerciseButton = Button(mypageScreenFrame, image = exerciseIcon, width = 85, height = 85, bg = 'white', command = goExerciseScreen)
exerciseButtonTitle = Label(mypageScreenFrame, text = '운동', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

exerciseButton.place(x = 55, y = 545)
exerciseButtonTitle.place(x = 55, y = 645)

calendarButton = Button(mypageScreenFrame, image = calendarIcon, width = 85, height = 85, bg = 'white', command = goCalendarScreen)
calendarButtonTitle = Label(mypageScreenFrame, text = '캘린더', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

calendarButton.place(x = 180, y = 545)
calendarButtonTitle.place(x = 180, y = 645)

homeButton = Button(mypageScreenFrame, image = homeIcon, width = 85, height = 85, bg = 'white', command = goMainScreen)
homeButtonTitle = Label(mypageScreenFrame, text = '홈', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

homeButton.place(x = 305, y = 545)
homeButtonTitle.place(x = 305, y = 645)

selectedMyButton = Button(mypageScreenFrame, image = selectedMyIcon, width = 85, height = 85, bg = 'white')
selectedMyButtonTitle = Label(mypageScreenFrame, text = 'My', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

selectedMyButton.place(x = 430, y = 545)
selectedMyButtonTitle.place(x = 430, y = 645)

friendsButton = Button(mypageScreenFrame, image = friendsIcon, width = 85, height = 85, bg = 'white', command = goFriendsScreen)
friendsButtonTitle = Label(mypageScreenFrame, text = '친구', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

friendsButton.place(x = 555, y = 545)
friendsButtonTitle.place(x = 555, y = 645)






editNameLabel = Label(mypageScreenFrame, text = '이름', font = ('Arial', 17, 'bold'), bg = '#EDFFFB')
editAgeLabel = Label(mypageScreenFrame, text = '나이(만)', font = ('Arial', 17, 'bold'), bg = '#EDFFFB')
editGenderLabel = Label(mypageScreenFrame, text = '성별', font = ('Arial', 17, 'bold'), bg = '#EDFFFB')
editPwLabel = Label(mypageScreenFrame, text = 'PW', font = ('Arial', 17, 'bold'), bg = '#EDFFFB')
editHeightLabel = Label(mypageScreenFrame, text = '키(cm)', font = ('Arial', 17, 'bold'), bg = '#EDFFFB')
editWeightLabel = Label(mypageScreenFrame, text = '몸무게(kg)', font = ('Arial', 17, 'bold'), bg = '#EDFFFB')

editNameEntry = Entry(mypageScreenFrame, font = ('Arial', 17), width = 25);
editAgeEntry = Entry(mypageScreenFrame, font = ('Arial', 17), width = 25);
editGenderEntry = Entry(mypageScreenFrame, font = ('Arial', 17), width = 25);
editPwEntry = Entry(mypageScreenFrame, show = '●', font = ('Arial', 17), width = 25);
editHeightEntry = Entry(mypageScreenFrame, font = ('Arial', 17), width = 25);
editWeightEntry = Entry(mypageScreenFrame, font = ('Arial', 17), width = 25);

editNameButton = Button(mypageScreenFrame, text = '수정', font = ('Arial', 11, 'bold'), bg = '#B4FFFC', command = editNameCommand)
editAgeButton = Button(mypageScreenFrame, text = '수정', font = ('Arial', 11, 'bold'), bg = '#B4FFFC', command = editAgeCommand)
editGenderButton = Button(mypageScreenFrame, text = '수정', font = ('Arial', 11, 'bold'), bg = '#B4FFFC', command = editGenderCommand)
editPwButton = Button(mypageScreenFrame, text = '수정', font = ('Arial', 11, 'bold'), bg = '#B4FFFC', command = editPwCommand)
editHeightButton = Button(mypageScreenFrame, text = '수정', font = ('Arial', 11, 'bold'), bg = '#B4FFFC', command = editHeightCommand)
editWeightButton = Button(mypageScreenFrame, text = '수정', font = ('Arial', 11, 'bold'), bg = '#B4FFFC', command = editWeightCommand)

editNameLabel.place(x = 45, y = 80); editNameEntry.place(x = 170, y = 80); editNameButton.place(x = 515, y = 80)
editAgeLabel.place(x = 45, y = 130); editAgeEntry.place(x = 170, y = 130); editAgeButton.place(x = 515, y = 130)
editGenderLabel.place(x = 45, y = 180); editGenderEntry.place(x = 170, y = 180); editGenderButton.place(x = 515, y = 180)
editPwLabel.place(x = 45, y = 230); editPwEntry.place(x = 170, y = 230); editPwButton.place(x = 515, y = 230)
editHeightLabel.place(x = 45, y = 280); editHeightEntry.place(x = 170, y = 280); editHeightButton.place(x = 515, y = 280)
editWeightLabel.place(x = 45, y = 330); editWeightEntry.place(x = 170, y = 330); editWeightButton.place(x = 515, y = 330)

badgeInfoLabel = Label(mypageScreenFrame, text = '보유한 뱃지가 없습니다.', image = None, font = ('Arial', 15, 'bold'), bg = '#EDFFFB')
badgeInfoLabel.place(x = 238, y = 440)






# 로그아웃, 회원 탈퇴 등의 기능도 구현하기!
logoutButton = Button(mypageScreenFrame, text = '로그\n아웃', font = ('Arial', 15, 'bold'), width = 5, bg = '#B4FFFC', command = logoutCommand)
deleteUserButton = Button(mypageScreenFrame, text = '회원\n탈퇴', font = ('Arial', 15, 'bold'), width = 5, bg = '#FF8888', command = deleteUserCommand)

logoutButton.place(x = 575, y = 80)
deleteUserButton.place(x = 575, y = 155)
# -------------------------------------------------------------------------------------------------------------------------







# ------------------------------------------------ 5. 친구 목록 페이지 화면 ---------------------------------------------------------
friendsScreenFrame = Frame(window, bg = '#EDFFFB', width = 800, height = 800)
friendsScreenFrame.place(x = 0, y = 0)


friendsTitleLabel = Label(friendsScreenFrame, text = '친구', font = ('Arial', 25, 'bold'), bg = '#EDFFFB')
friendsTitleLabel.place(x = 305, y = 20)

iconsFrameInFriendsScreen = Frame(friendsScreenFrame, width = 650, height = 145, bg = '#E6F7F3')
iconsFrameInFriendsScreen.place(x = 25, y = 535)

exerciseButton = Button(friendsScreenFrame, image = exerciseIcon, width = 85, height = 85, bg = 'white', command = goExerciseScreen)
exerciseButtonTitle = Label(friendsScreenFrame, text = '운동', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

exerciseButton.place(x = 55, y = 545)
exerciseButtonTitle.place(x = 55, y = 645)

calendarButton = Button(friendsScreenFrame, image = calendarIcon, width = 85, height = 85, bg = 'white', command = goCalendarScreen)
calendarButtonTitle = Label(friendsScreenFrame, text = '캘린더', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

calendarButton.place(x = 180, y = 545)
calendarButtonTitle.place(x = 180, y = 645)

homeButton = Button(friendsScreenFrame, image = homeIcon, width = 85, height = 85, bg = 'white', command = goMainScreen)
homeButtonTitle = Label(friendsScreenFrame, text = '홈', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

homeButton.place(x = 305, y = 545)
homeButtonTitle.place(x = 305, y = 645)

myButton = Button(friendsScreenFrame, image = myIcon, width = 85, height = 85, bg = 'white', command = goMypageScreen)
myButtonTitle = Label(friendsScreenFrame, text = 'My', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

myButton.place(x = 430, y = 545)
myButtonTitle.place(x = 430, y = 645)

selectedFriendsButton = Button(friendsScreenFrame, image = selectedFriendsIcon, width = 85, height = 85, bg = 'white')
selectedFriendsButtonTitle = Label(friendsScreenFrame, text = '친구', font = ('Arial', 14, 'bold'), bg = '#E6F7F3', width = 7)

selectedFriendsButton.place(x = 555, y = 545)
selectedFriendsButtonTitle.place(x = 555, y = 645)




findUserByIdLabel = Label(friendsScreenFrame, text = 'ID로 친구 찾기', font = ('Arial', 15, 'bold'), bg = '#EDFFFB')
findUserByIdLabel.place(x = 60, y = 80)

findUserByIdEntry = Entry(friendsScreenFrame, font = ('Arial', 15), width = 25)
findUserByIdEntry.place(x = 210, y = 80)

addFriendButton = Button(friendsScreenFrame, text = '추가', font = ('Arial', 10, 'bold'), width = 6, bg = '#B4FFFC', command = addFriendCommand)
addFriendButton.place(x = 500, y = 80)

deleteFriendButton = Button(friendsScreenFrame, text = '삭제', font = ('Arial', 10, 'bold'), width = 6, bg = '#FF8888', command = deleteFriendCommand)
deleteFriendButton.place(x = 567, y = 80)
# -------------------------------------------------------------------------------------------------------------------------

loginFrame.lift()
window.mainloop()