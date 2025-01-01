import os, logging, yaml, time, allure , cv2 ,numpy as np ,difflib
import pytest, sys, random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
from PIL import Image
import imagehash
from io import BytesIO

class Elements:

    def __init__(self):
        '''啟動時自動導入'''
        self.LoadData()

    def InIDiver(self, driver):
        '''透過外部參數導入 driver'''
        self.driver = driver

    def LoadData(self):
        '''读取指定目录下的 Frontend.yaml，并合并数据'''

        # 创建一个空字典用于存储所有数据
        all_data = {}

        paths = [
            os.path.abspath(os.path.join(os.getcwd(), 'data', 'Web', 'Frontend.yaml'))
        ]

        for path in paths:
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    # 合并数据到all_data字典中
                    all_data.update(data)
            except FileNotFoundError:
                continue  # 如果文件不存在，继续下一个文件的搜索
            except yaml.YAMLError as e:
                logging.error(e)
                break  # 如果在读取过程中出现了错误，就退出循环

        if not all_data:
            logging.error("未找到 Frontend.yaml")
            raise FileNotFoundError("未找到 Frontend.yaml")

        # 将合并后的数据赋值给 self.elementsData
        self.elementsData = all_data

    def data_yaml(self):
        '''讀取指定目錄下的 data.yaml'''
        yaml_path = os.path.abspath(os.path.join(os.getcwd(), "data", "Web", "data.yaml"))
        with open(yaml_path, encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                logging.error(e)
        return yaml_path, data


    def env(self, url):
        '''讀取指定目錄下的 env.yaml'''
        config_path = os.path.abspath(os.path.join(os.getcwd(), "data", "env.yaml"))
        with open(config_path, encoding="utf-8") as f:
            try:
                env = yaml.safe_load(f)[url]
            except yaml.YAMLError as e:
                logging.error(e)
        return env
    
    def imageDict(self):
        imageDict = os.path.abspath(os.path.join(os.getcwd(), "image"))
        if not os.path.isdir(imageDict):
            os.mkdir(imageDict)
        return imageDict


# selenium element trigger 
# ====================================================================================================
    def ClickEle(self, eleName, img=True):
        '''click'''
        ele, dealError, ele_info = self.GetElement(*eleName)  # 取得元素
        sleepTime = ele_info['time']  # 取得sleep time

        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('ClickEle', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                ele.click()
                time.sleep(int(sleepTime))
                logging.info(f'{eleName} - ClickEle Success')
            except Exception as e:
                # 有找到物件但無法點擊
                self.exc('ClickEle', eleName, e, img)

    def WaitClickEle(self, eleName, img=True):
        '''隱式等待 + click'''
        ele, dealError,  = self.GetEleExceptionEle(*eleName)

        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('WaitClickEle', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                # click Success 時觸發
                ele.click()
                time.sleep(2)
                logging.info(f'{eleName} - WaitClickEle Success')
            except Exception as e:
                # 有找到物件但無法點擊
                self.exc('WaitClickEle', eleName, e, img)

    def exc(self, module, eleName, e, img):
        '''該 Module 沒有正常執行！'''
        if img == True:
            self.Screenshot(f'{module} - {eleName} - except')
        logging.error(f'{module} - {eleName} - {e}，except！')
        raise Exception(f'{module} - {eleName}，except！')
    
    def dealError(self, module, eleName, img):
        '''dealError == True'''
        if img == True:
            self.Screenshot(f'{module} - {eleName} - dealError')
        logging.error(f'{module} - {eleName}，dealError！')
        raise Exception(f'{module} - {eleName}，dealError！')




# selenium element read 
# ====================================================================================================
    def GetElesExceptionEles(self, *ele_name, sleep_time=5):
        '''隱式等待 + 讀取多個物件設定(elements)'''
        try:
            try:
                ele_info = self.elementsData
                for arg in ele_name:
                    ele_info = ele_info[arg]
            except (KeyError, TypeError, IndexError):
                # 如果在elementsData中找不到對應的值，或者試圖對非字典類型的對象進行索引，則拋出異常
                raise KeyError("Element '{}' not found in elementsData".format(ele_name))

            ele_type = ele_info['type']
            ele_value = ele_info['value']
            deal_error = ele_info.get('dealError', False)
        except KeyError:
            logging.error(f"{ele_name} Incorrect setting!")
            raise Exception(f"{ele_name} Incorrect setting!")

        try:
            locator_dict = {"id":By.ID, "xpath":By.XPATH, "link":By.LINK_TEXT, "partial":By.PARTIAL_LINK_TEXT, "name":By.NAME, "tag":By.TAG_NAME, "class":By.CLASS_NAME, "css":By.CSS_SELECTOR}
            elements = WDW(self.driver, sleep_time).until(EC.presence_of_all_elements_located((locator_dict[ele_type], ele_value)))
            return elements, deal_error
        except Exception as e:
            logging.error(f"{ele_name} - {str(e)}")
            return None, deal_error

    def GetEleExceptionEle(self, *ele_name, sleep_time=10):
        '''隱式等待 + 讀取物件設定(element)'''
        try:
            try:
                ele_info = self.elementsData
                for arg in ele_name:
                    ele_info = ele_info[arg]
            except (KeyError, TypeError, IndexError):
                # 如果在elementsData中找不到對應的值，或者試圖對非字典類型的對象進行索引，則拋出異常
                raise KeyError("Element '{}' not found in elementsData".format(ele_name))

            ele_type = ele_info['type']
            ele_value = ele_info['value']
            deal_error = ele_info.get('dealError', False)
        except KeyError:
            logging.error(f"{ele_name} Incorrect setting!")
            raise Exception(f"{ele_name} Incorrect setting!")

        try:
            locator_dict = {"id":By.ID, "xpath":By.XPATH, "link":By.LINK_TEXT, "partial":By.PARTIAL_LINK_TEXT, "name":By.NAME, "tag":By.TAG_NAME, "class":By.CLASS_NAME, "css":By.CSS_SELECTOR}
            element = WDW(self.driver, sleep_time).until(EC.presence_of_element_located((locator_dict[ele_type], ele_value)))
            return element, deal_error
        except Exception as e:
            logging.error(f"{ele_name} - {str(e)}")
            return None, deal_error

    def GetElement(self, *ele_name):
        '''讀取物件設定(element)'''
        try:
            try:
                ele_info = self.elementsData
                for arg in ele_name:
                    ele_info = ele_info[arg]
            except (KeyError, TypeError, IndexError):
                # 如果在elementsData中找不到對應的值，或者試圖對非字典類型的對象進行索引，則拋出異常
                raise KeyError("Element '{}' not found in elementsData".format(ele_name))

            ele_type = ele_info['type']
            ele_value = ele_info['value']
            deal_error = ele_info.get('dealError', False)
        except KeyError:
            logging.error(f"{ele_name} Incorrect setting!")
            raise Exception(f"{ele_name} Incorrect setting!")

        try:
            locator_dict = {"id":By.ID, "xpath":By.XPATH, "link":By.LINK_TEXT, "partial":By.PARTIAL_LINK_TEXT, "name":By.NAME, "tag":By.TAG_NAME, "class":By.CLASS_NAME, "css":By.CSS_SELECTOR}
            element = self.driver.find_element(locator_dict[ele_type], ele_value)
            return element, deal_error, ele_info
        except Exception as e:
            logging.error(f"{ele_name} - {str(e)}")
            return None, deal_error
              
# function element
# ====================================================================================================

    def screenshot_local(self, filename):
        '''截圖到 local + 全屏截圖'''
        filenameTime = os.path.join(self.imageDict(), filename + '.png')
        self.driver.get_screenshot_as_file(filenameTime)

    def Screenshot(self, name):
        '''截圖到 local + 全屏截圖 + Allure'''
        image = name + self.GetTimeStr()
        self.screenshot_local(image)
        self.Allure(image)
        logging.info(image + ' - Screenshot Success')

    def WaitScreenShot(self, eleName, text, img=True):
        '''隱式等待 + 全屏截圖 + Allure'''
        ele, dealError,  = self.GetEleExceptionEle(*eleName)

        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('WaitScreenShot', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                Screenshot(text)
                logging.info(f'{eleName} - WaitClickEle Success')
            except Exception as e:
                Screenshot('有找到物件但無法點擊，請查看')
                self.exc('WaitClickEle', eleName, e, img)

    def screenshot_ele(self, filename, ele):
        '''直接傳入ele + 截圖特定元素 + Allure'''
        filenameTime = os.path.join(self.imageDict(), filename + '.png')
        screenshot_div = ele.screenshot_as_png
        img = Image.open(BytesIO(screenshot_div))
        img.save(filenameTime)
        self.Allure(filename)

    def WaitScreenshot_ele(self, eleName, name):
        '''隱式等待 + 截圖特定元素 + Allure'''
        ele, dealError = self.GetEleExceptionEle(*eleName)
        image = name + self.GetTimeStr()
        self.screenshot_ele(image,ele)
        logging.info(image + ' - Screenshot Success')

    def Allure(self, filename):
        '''Allure 上傳圖片'''
        filenameTime = os.path.join(self.imageDict(), filename +'.png')
        allure.attach.file(filenameTime, attachment_type=allure.attachment_type.PNG, name=filename)


    def GetTimeStr(self):
        '''取得當前日期'''
        time.sleep(1)
        now = time.strftime(r"_%Y-%m-%d")
        return now
    

    def Wait_CheckItems_Numbers(self, eleName):
        '''隱式等待 + 計算元數數量'''
        ele, dealError = self.GetElesExceptionEles(*eleName)

        return len(ele)

    def Return_element(self, eleName):
        '''隱式等待 + 選定元素'''
        try:
            ele, dealError = self.GetEleExceptionEle(*eleName)
            logging.info(f'{eleName} - 選定成功')
            return ele
        except Exception as e:
            logging.error(f'{eleName} - {str(e)}')

    def Search_elements(self, ele, class_name="", name= ""):
        '''Return_element + 用class搜索下面物件'''
        try:
            # 用 CSS 選擇器搜尋包含多個類別名稱的元素
            elements = ele.find_elements(By.CSS_SELECTOR, class_name)
            logging.info(f"找到 {len(elements)} 个符合条件的元素")
            for index, element in enumerate(elements):
                image = name + str(index+1)+ self.GetTimeStr()
                self.screenshot_ele(image, element)
            return elements
        except Exception as e:
            logging.error(f"错误: {str(e)}")
            return None

    def GoToWindow(self, url):
        '''開啟當前視窗'''
        try:
            self.driver.get(url)
            logging.info(f'{url}，GoToWindow Success')
        except Exception as e:
            logging.error(str(e))


    def Swipe_Down(self, eleName, scrollAmount=None):
        '''網頁滑動'''
        ele, dealError = self.GetEleExceptionEle(*eleName)  # 找到彈出式視窗中的固定 <div> 元素 > ele

        # 動態改變元素的 overflow 屬性
        self.driver.execute_script("arguments[0].style.overflow = 'auto';", ele)

        if scrollAmount is not None:
            # 滾動指定量
            self.driver.execute_script(f"arguments[0].scrollTop += {scrollAmount};", ele)
            logging.info(f'script Swipe_Down by {scrollAmount} pixels Success')
        else:
            # 滾動到底部
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", ele)
            logging.info('script Swipe_Down to Bottom Success')



# Elements()
# ====================================================================================================
ele = Elements()
yaml_path, data = ele.data_yaml()
InIDiver = ele.InIDiver
env = ele.env
GoToWindow = ele.GoToWindow
imageDict = ele.imageDict
elementsData = ele.elementsData
WaitClickEle = ele.WaitClickEle
ClickEle = ele.ClickEle
Allure = ele.Allure
GetElement = ele.GetElement
GetTimeStr = ele.GetTimeStr
eleScreenshot = ele.screenshot_local
Screenshot = ele.Screenshot
WaitScreenshot_ele = ele.WaitScreenshot_ele
WaitScreenShot = ele.WaitScreenShot
Swipe_Down = ele.Swipe_Down
Wait_CheckItems_Numbers = ele.Wait_CheckItems_Numbers
Return_element = ele.Return_element
Search_elements = ele.Search_elements
