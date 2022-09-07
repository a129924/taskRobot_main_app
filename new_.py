# %%
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import configparser, requests
import time

from dataclasses import dataclass
from urllib3.exceptions import NewConnectionError

class NoneTypeError(Exception):
    def __init__(self, message):
        message = "參數不得為None"
        super().__init__(message)

class MyTaskRobot():
    def __init__(self, account:str = None, password:str = None, tasks:int = 2):
        parser = configparser.ConfigParser()
        parser.read("login_info.ini")
        parser.read(r".\task.url.ini")
        
        login_info = parser["login_infomation"]
        
        self._account = account if account else login_info["account"]
        self._password = password if password else login_info["password"]
        self._tasks = tasks

        self._login_url = "https://backend.asteroom.com/Login/Index"
        self._home_url = "https://backend.asteroom.com/Home/Index"
        self._dolltask_url = "https://backend.asteroom.com/DollTask/Index"
        
        self._SetWebDriver()
    
    def _SetWebDriver(self):
        opt = webdriver.ChromeOptions()
        
        self.TaskRobot = webdriver.Chrome(executable_path=r".\chrome_driver\chromedriver.exe", options=opt)
        
    def _WaitTheElement(self, wait:WebDriverWait, locator:By, element:str) :# bool
        try:
            wait.until(EC.presence_of_all_elements_located((locator,element)))
        except Exception as error:
            print(error)
            print(f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}] 等候愈時 目前網址: {self.TaskRobot.current_url} find_element: {element}")
            return False
            
        return True
        
    def main(self): # bool
        while True:
            try:
                if requests.get(self._login_url).status_code != 200:break
                # 執行過久會出現的問題
                # raise NewConnectionError(
                # TimeoutError
                # requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(10054, '遠端主機已強制關閉一個現存的連線。', None, 10054, None))
            except NewConnectionError as error:
                print(f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}] 網頁載入愈時 \n {error}")
                time.sleep(3600)
            
            # 去登入頁
            TaskRobot = self.TaskRobot
            
            TaskRobot.get(self._login_url)
            
            wait = WebDriverWait(TaskRobot, 10)
            
            try:   
                print(f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}] 找尋登入畫面") 
                # 找尋帳號欄位
                if self._WaitTheElement(wait, By.ID,"inputUserAccount"):
                    # 點選帳號 填入帳號
                    TaskRobot.find_element(by = By.XPATH, value = '//*[@id="inputUserAccount"]').send_keys(self._account)
                    # 點選帳號 填入密碼
                    TaskRobot.find_element(by = By.XPATH, value = '//*[@id="inputPassword"]').send_keys(self._password)
                    # 點選登入
                    TaskRobot.find_element(by = By.XPATH, value = '//*[@class="form-control btn btn-primary"]').click()
                    # 
                    time.sleep(15)
                    
                    print(f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}] 以找尋登入畫面") 
                else:
                    raise Exception
            except Exception as error:
                print(f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}]{error}找尋不到登入畫面")
            
            try:
                print(f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}] 找尋TASK下拉") 
                # 找尋TASK下拉
                if self._WaitTheElement(wait, By.XPATH, '//*[@id="accordionSidebar"]/li[2]/a'):
                    TaskRobot.get(self._dolltask_url)
                    #   //*[@id="dt-accepted_paginate"]
                    print(f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}] 以找尋TASK下拉")
                else:
                    raise Exception            

            except Exception as error:
                print(f"{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}{error}找尋不到LOGO") 

            # ID: //*[@id="dt-accepted"]/thead/tr/th[1]
            if self._WaitTheElement(wait, By.XPATH, '//*[@id="dt-accepted"]/thead/tr/th[1]'):
                time.sleep(0.1)
                case:str = TaskRobot.find_elements(by = By.XPATH, value ='//*[@id="dt-accepted"]/tbody')[0].text
            
            print("開始執行...")
            print("##########################")
            while True:
                try:
                    # //*[@id="dt-accepted"]/tbody
                    # wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="dt-accepted"]/tbody')))
                    # self._WaitTheElement(wait, By.XPATH, '//*[@id="dt-accepted"]/tbody') 
                    if self._WaitTheElement(wait, By.XPATH, '//*[@id="dt-accepted"]/tbody'): # 等元素出來
                        time.sleep(1)
                        now_case:str = TaskRobot.find_elements(by = By.XPATH, value ='//*[@id="dt-accepted"]/tbody')[0].text 
                        if len(now_case) == 0:
                            now_case = case
                            
                        now_case_number:str = now_case.split()[0]
                        print(f"now:{now_case_number}")
                    elif self._WaitTheElement(wait, By.XPATH, '//*[@id="dt-feedback"]/thead/tr'):
                        break
                    else:
                        print("找不到元素")
                        break
                    
                    case_number:str = case.split()[0]
                    print(case_number, now_case_number)
                    
                    # if (now_case != case):
                    if (now_case_number != case_number):
                        time.sleep(0.1)
                        TaskRobot.find_element(by=By.XPATH, value='//*[@class="btn btn-info"]').click()
                        case = now_case
                        case_number = now_case_number
                        # //*[@id="dt-accepted"]/tbody/tr[1]/td[7]/button
                        # //*[@id="dt-accepted"]/tbody/tr[1]/td[7]/button
                        # or self._WaitTheElement(wait, By.XPATH, '//*[@class="btn btn-info"]')
                        # //*[@id="dt-accepted"]/tbody/tr[2]/td[7]/button
                
                except NoSuchElementException:
                    print("找不到任務接受按鈕!")
                    case = now_case
                    case_number = now_case_number
                    
                except NoneTypeError as error:
                    print(f"引發異常: {repr(error)}")
                    break
                
                except Exception as e:
                    print(e)
                    print(now_case)
                    break
                
                finally:
                    print(f"[{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}] now_case: {now_case_number} case: {case_number}")
                    # dt_ms = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    time.sleep(28.3)
                    TaskRobot.refresh()
                    
        return False                    
    # %%
if __name__ == "__main__":
    task_robot = MyTaskRobot()
    task_robot.main()
            


# %%
