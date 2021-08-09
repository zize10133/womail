# -*- coding: utf8 -*-
import json
import os
import random
import re
import time

import requests


class MiMotion:
    def __init__(self, check_item):
        self.check_item = check_item
        self.headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/20.6.18)"}

    def get_time(self):
        url = "http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp"
        response = requests.get(url, headers=self.headers).json()
        t = response["data"]["t"]
        return t

    def get_app_token(self, login_token):
        url = f"https://account-cn.huami.com/v1/client/app_tokens?app_name=com.xiaomi.hm.health&dn=api-user.huami.com%2Capi-mifit.huami.com%2Capp-analytics.huami.com&login_token={login_token}"
        response = requests.get(url=url, headers=self.headers).json()
        app_token = response["token_info"]["app_token"]
        return app_token

    @staticmethod
    def login(phone, password):
        url1 = f"https://api-user.huami.com/registrations/+86{phone}/tokens"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "User-Agent": "MiFit/4.6.0 (iPhone; iOS 14.0.1; Scale/2.00)",
        }
        data1 = {
            "client_id": "HuaMi",
            "password": f"{password}",
            "redirect_uri": "https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html",
            "token": "access",
        }
        r1 = requests.post(url=url1, data=data1, headers=headers, allow_redirects=False)
        location = r1.headers["Location"]
        try:
            code_pattern = re.compile("(?<=access=).*?(?=&)")
            code = code_pattern.findall(location)[0]
        except Exception as e:
            print(e)
            return 0, 0
        url2 = "https://account.huami.com/v2/client/login"
        data2 = {
            "app_name": "com.xiaomi.hm.health",
            "app_version": "4.6.0",
            "code": f"{code}",
            "country_code": "CN",
            "device_id": "2C8B4939-0CCD-4E94-8CBA-CB8EA6E613A1",
            "device_model": "phone",
            "grant_type": "access_token",
            "third_name": "huami_phone",
        }
        r2 = requests.post(url=url2, data=data2, headers=headers).json()
        login_token = r2["token_info"]["login_token"]
        userid = r2["token_info"]["user_id"]
        return login_token, userid

    def main(self):
        phone = str(self.check_item.get("mimotion_phone"))
        password = str(self.check_item.get("mimotion_password"))
        try:
            min_step = int(self.check_item.get("mimotion_min_step", 10000))
        except Exception as e:
            print("初始化步数失败: 已将最小值设置为 19999", e)
            min_step = 10000
        try:
            max_step = int(self.check_item.get("mimotion_max_step", 19999))
        except Exception as e:
            print("初始化步数失败: 已将最大值设置为 19999", e)
            max_step = 19999
        step = str(random.randint(min_step, max_step))
        login_token, userid = self.login(phone, password)
        if login_token == 0:
            msg = f"帐号信息: {phone}\n修改状态: 登陆失败"
        else:
            t = self.get_time()
            app_token = self.get_app_token(login_token)
            today = time.strftime("%F")
            data_json="%5B%7B%22data_hr%22%3A%22%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F9L%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2FVv%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F0v%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F9e%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F0n%5C%2Fa%5C%2F%5C%2F%5C%2FS%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F0b%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F1FK%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2FR%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F9PTFFpaf9L%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2FR%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F0j%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F9K%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2FOv%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2Fzf%5C%2F%5C%2F%5C%2F86%5C%2Fzr%5C%2FOv88%5C%2Fzf%5C%2FPf%5C%2F%5C%2F%5C%2F0v%5C%2FS%5C%2F8%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2FSf%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2Fz3%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F0r%5C%2FOv%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2FS%5C%2F9L%5C%2Fzb%5C%2FSf9K%5C%2F0v%5C%2FRf9H%5C%2Fzj%5C%2FSf9K%5C%2F0%5C%2F%5C%2FN%5C%2F%5C%2F%5C%2F%5C%2F0D%5C%2FSf83%5C%2Fzr%5C%2FPf9M%5C%2F0v%5C%2FOv9e%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2FS%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2F%5C%2Fzv%5C%2F%5C%2Fz7%5C%2FO%5C%2F83%5C%2Fzv%5C%2FN%5C%2F83%5C%2Fzr%5C%2FN%5C%2F86%5C%2Fz%5C%2F%5C%2FNv83%5C%2Fzn%5C%2FXv84%5C%2Fzr%5C%2FPP84%5C%2Fzj%5C%2FN%5C%2F9e%5C%2Fzr%5C%2FN%5C%2F89%5C%2F03%5C%2FP%5C%2F89%5C%2Fz3%5C%2FQ%5C%2F9N%5C%2F0v%5C%2FTv9C%5C%2F0H%5C%2FOf9D%5C%2Fzz%5C%2FOf88%5C%2Fz%5C%2F%5C%2FPP9A%5C%2Fzr%5C%2FN%5C%2F86%5C%2Fzz%5C%2FNv87%5C%2F0D%5C%2FOv84%5C%2F0v%5C%2FO%5C%2F84%5C%2Fzf%5C%2FMP83%5"
            finddate = re.compile(r".*?date%22%3A%22(.*?)%22%2C%22data.*?")
            findstep = re.compile(r".*?ttl%5C%22%3A(.*?)%2C%5C%22dis.*?")
            data_json = re.sub(finddate.findall(data_json)[0], today, str(data_json))
            data_json = re.sub(findstep.findall(data_json)[0], step, str(data_json))
            url = f"https://api-mifit-cn.huami.com/v1/data/band_data.json?&t={t}"
            headers = {"apptoken": app_token, "Content-Type": "application/x-www-form-urlencoded"}
            data = f"userid={userid}&last_sync_data_time=1597306380&device_type=0&last_deviceid=DA932FFFFE8816E7&data_json={data_json}"
            response = requests.post(url=url, data=data, headers=headers).json()
            msg = f"帐号信息: {phone}\n修改状态: {response['message']}\n修改步数: {step}"
        return msg


if __name__ == "__main__":
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/config.json"), "r", encoding="utf-8"
    ) as f:
        datas = json.loads(f.read())
    _check_item = datas.get("MIMOTION_ACCOUNT_LIST", [])[0]
    print(MiMotion(check_item=_check_item).main())
