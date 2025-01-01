import time

import allure
import pytest
from .Base import *

case = os.path.basename(__file__)


class Test(Base):

    @allure.title(case)
    # 整個.py測試前執行程式碼
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, newDriver):
        pass

    @staticmethod
    def teardown_method():
        logging.info("teardown_method: 每个用例结束后执行")

    @allure.description('''進入官網後等QuickLink出現後截圖''')
    def test_fistpage_screenshot(self, newDriver):
        allure.attach.file(yaml_path, 'data', allure.attachment_type.YAML)
        logging.info('starting ' + case)

        # 隱式等待 + 全屏截圖
        WaitScreenShot(['Frontend', 'QuickLink'],'國泰世華銀行官網')
        logging.info('end ' + case)

    @allure.description('''點選左上角選單，進入 個人金融 > 產品介紹 > 信用卡列表，需計算有幾個項目並將畫面截圖''')
    def test_count_creditcard_items(self, newDriver):
        allure.attach.file(yaml_path, 'data', allure.attachment_type.YAML)
        logging.info('starting ' + case)

        # ------點選左上角選單------
        WaitClickEle(['Frontend', 'BankTypeMenu'])
        # ------點選個人金融------
        WaitClickEle(['Frontend', 'BankTypeMenu_item1'])
        # ------點選產品介紹------
        WaitClickEle(['Frontend', 'ProductIntroduceMenu'])
        # ------信用卡選單截圖------
        WaitScreenshot_ele(['Frontend', 'CreditCardMenu'], '信用卡選單截圖')
        # ------計算有幾個項目, 針對menu中有幾個<a>來做計算------
        numbers = Wait_CheckItems_Numbers(['Frontend', 'CreditCardMenu_a'])
        logging.info(f'有{numbers}項目在信用卡選單下面')
        logging.info('end ' + case)

    @allure.description('''個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有(停發)信用卡數量並截圖''')
    def test_count_stop_creditcard_items(self, newDriver):
        allure.attach.file(yaml_path, 'data', allure.attachment_type.YAML)
        logging.info('starting ' + case)

        # ------點選左上角選單------
        WaitClickEle(['Frontend', 'BankTypeMenu'])
        # ------點選個人金融------
        WaitClickEle(['Frontend', 'BankTypeMenu_item1'])
        # ------點選產品介紹------
        WaitClickEle(['Frontend', 'ProductIntroduceMenu'])
        # ------點選卡片介紹------
        WaitClickEle(['Frontend', 'CardIntroduce'])
        # ------滑到頁面底部------
        Swipe_Down(['Frontend', 'Html'])
        # ------選定停發卡的整個清單------
        CardStop_Menu = Return_element(['Frontend', 'CardStop_Menu'])
        # ------針對清單元素找下面幾張卡片並截圖------
        Search_elements(CardStop_Menu, '.cubre-m-compareCard.-credit', '信用卡停發卡截圖')
        logging.info('end ' + case)


    if __name__ == '__main__':
        pytest.main(['-s', __file__])