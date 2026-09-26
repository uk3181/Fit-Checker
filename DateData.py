from datetime import *

class DateData: # 날짜별로 각종 데이터를 저장하기 위한 클래스
    def __init__(self, data, date = date.today()):
        self.__data = data
        self.__date = date

    def setData(self, data):
        self.__data = data
    
    def getData(self):
        return self.__data

    def getDate(self):
        return self.__date

    def isDateEqual(self, dateData): # 두 DateDate 객체의 날짜를 비교하는 메소드
        return self.__date.year == dateData.__date.year and self.__date.month == dateData.__date.month\
                and self.__date.day == dateData.__date.day