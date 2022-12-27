# -*- encoding: utf-8 -*-
from minittk import *


class UIAutomation:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UIAutomation, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def __waitForLocate(target):
        t = 0
        while pyautogui.locateCenterOnScreen(target) is None:
            t += 1
            if t >= 15:
                raise LookupError('Location not found')
            sleep(1)
            print(f'going {t}')
        return pyautogui.locateCenterOnScreen(target)

    @staticmethod
    def openwithTX(selectionCode: Tuple[str, int]):
        if not selectionCode:
            Messagebox.show_error(message='你未选择任何数据', title='错误')
            return

        def openLangTX(lang=None):
            print(f'goto {lang} v')
            code, pwd = selectionCode
            pyautogui.typewrite(code)
            sleep(1)
            pyautogui.leftClick(UIAutomation.__waitForLocate(f'./meetingapps/tx/join_{lang}.png'))
            if pwd == 'None':
                print(f'{lang} ui runned')
                return
            UIAutomation.__waitForLocate('./meetingapps/tx/hide_pwd.png')
            pyautogui.typewrite(pwd)
            pyautogui.press('enter')
            print(f'{lang} ui runned')
            return

        startfile(r"C:\Program Files (x86)\Tencent\WeMeet\wemeetapp.exe")
        try:
            join = UIAutomation.__waitForLocate('./meetingapps/tx/join.png')
            pyautogui.leftClick(join)
            down = UIAutomation.__waitForLocate('./meetingapps/tx/down.png')
            pyautogui.leftClick(down)
            sleep(.5)
            pyautogui.leftClick(down)
            pyautogui.hotkey('ctrl', 'a')  # ensure that no code history remained
            pyautogui.press('backspace')
            print('ok')
            if pyautogui.locateCenterOnScreen('./meetingapps/tx/disabled_ch.png') is not None:
                openLangTX(lang='ch')
            elif pyautogui.locateCenterOnScreen('./meetingapps/tx/disabled_en.png') is not None:
                openLangTX(lang='en')
        except LookupError:
            raise LookupError('failure you mother fucker.')

    @staticmethod
    def openwithZoom(selectionCode: Tuple[str, int]):
        code, pwd = selectionCode
        startfile(r'C:\Users\shane\AppData\Roaming\Zoom\bin\Zoom.exe')
        pyautogui.leftClick(UIAutomation.__waitForLocate('./meetingapps/zoom/join_meeting_zh.png'))
        pyautogui.typewrite(code)
        pyautogui.leftClick(UIAutomation.__waitForLocate('./meetingapps/zoom/join_zh.png'))
