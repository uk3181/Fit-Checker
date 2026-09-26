def loginPass(usersList, inputId, inputPw): # 로그인 통과 여부 확인
    for user in usersList:
        if inputId == user.getId():
            if inputPw == user.getPw():
                return user # 로그인 통과
            else:
                return None # 비밀번호 틀림.
    return None # 등록된 사용자 없음.