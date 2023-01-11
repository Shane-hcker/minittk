# -*- encoding: utf-8 -*-
from ttkbootstrap.dialogs.dialogs import Messagebox
from os import startfile
from time import sleep
from typing import *
import pyautogui

from minittk.support.cfgparser import MyConfigParser


class UIAutomation:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UIAutomation, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def __waitForLocate(target):
        continue_waiting = 0
        while (locate_result := pyautogui.locateCenterOnScreen(target)) is None:
            if continue_waiting >= 15:
                raise LookupError('Location not found')
            continue_waiting += 1
            sleep(1)
            print(f'waiting for location... {continue_waiting}s')
        return locate_result

    @staticmethod
    def openwithTX(login_content: Tuple[str, int]):
        if not login_content:
            Messagebox.show_error(message='你未选择任何数据', title='错误')
            return

        def openLangTX(app_lang=None):
            print(f'switched to {app_lang} mode')
            meetingid, password = login_content
            pyautogui.typewrite(meetingid)
            sleep(1.5)
            pyautogui.leftClick(UIAutomation.__waitForLocate(f'./meetingapps/tx/join_{app_lang}.png'))
            if password == 'None':
                print(f'{app_lang} version ran')
                return
            UIAutomation.__waitForLocate('./meetingapps/tx/hide_pwd.png')
            pyautogui.typewrite(password)
            pyautogui.press('enter')
            print(f'{app_lang} version ran')
            return

        startfile(MyConfigParser().get('Launch', 'tencentmeeting'))
        try:
            join = UIAutomation.__waitForLocate('./meetingapps/tx/join.png')
            pyautogui.leftClick(join)
            down = UIAutomation.__waitForLocate('./meetingapps/tx/down.png')
            pyautogui.leftClick(down)
            sleep(1)
            pyautogui.leftClick(down)
            pyautogui.hotkey('ctrl', 'a')  # ensure that no code history remained
            pyautogui.press('backspace')
            print('pending to decide language options...')
            if pyautogui.locateCenterOnScreen('./meetingapps/tx/disabled_ch.png') is not None:
                openLangTX('ch')
                return
            if pyautogui.locateCenterOnScreen('./meetingapps/tx/disabled_en.png') is not None:
                openLangTX('en')
                return
            raise LookupError
        except LookupError as e:
            print(f'{e}: failed to locate. Error.')

    @staticmethod
    def openwithZoom(login_content: Tuple[str, int]):
        if not login_content:
            Messagebox.show_error(message='你未选择任何数据', title='错误')
            return

        meetingid, password = login_content
        startfile(MyConfigParser().get('Launch', 'zoom'))
        pyautogui.leftClick(UIAutomation.__waitForLocate('./meetingapps/zoom/join_meeting_zh.png'))
        pyautogui.typewrite(meetingid)
        pyautogui.leftClick(UIAutomation.__waitForLocate('./meetingapps/zoom/join_zh.png'))
