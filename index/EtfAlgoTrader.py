import ctypes
import win32com.client

#CREON Plus 공통 Object
cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')        #시스템 상태 정보
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')  #주문관련도구

#CREON Plus 시스템 점검 함수
def check_creon_system():
    #관리자 권한으로 프로세스 실행여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('check_creon_system() : admin user -> FAILED')
        return False

    #연결 여부 체크
    if(cpStatus.IsConnect == 0):
        print('check_creon_system() : connect to server -> FAILED')
        return False

    #주문관련 초기화
    if(cpTradeUtil.TradeInit(0) != 0):
        print('check_creon_system() : init trade -> FAILED')
        return False

    return True
