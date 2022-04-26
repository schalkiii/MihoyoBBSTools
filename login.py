import config
import setting
from request import http
from loghelper import log
from error import CookieError


def login():
    if config.cookies == '':
        log.error("请填入Cookies!")
        config.clear_cookies()
        raise CookieError('No cookie')
    # 判断Cookie里面是否有login_ticket 没有的话直接退了
    if "login_ticket" in config.cookies:
        temp_cookies = config.cookies.split(";")
        for i in temp_cookies:
            if i.split("=")[0] == " login_ticket":
                config.login_ticket = i.split("=")[1]
                break
        # 这里获取Stuid，但是实际是可以直接拿cookie里面的Uid
        data = http.get(url=setting.bbs_Cookie_url.format(config.login_ticket)).json()
        if "成功" in data["data"]["msg"]:
            config.stuid = str(data["data"]["cookie_info"]["account_id"])
            data = http.get(url=setting.bbs_Cookie_url2.format(
                config.login_ticket, config.stuid)).json()
            config.stoken = data["data"]["list"][0]["token"]
            log.info("登录成功！")
            log.info("正在保存Config！")
            config.save_config()
        else:
            log.error("cookie已失效,请重新登录米游社抓取cookie")
            config.clear_cookies()
            raise CookieError('Cookie expires')
    else:
        log.error("cookie中没有'login_ticket'字段,请重新登录米游社，重新抓取cookie!")
        config.clear_cookies()
        raise CookieError('Cookie lost login_ticket')
