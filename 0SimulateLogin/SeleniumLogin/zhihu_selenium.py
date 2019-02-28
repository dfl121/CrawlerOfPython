# coding:utf-8
import re
import requests
from selenium import webdriver
import time

url = "https://www.zhihu.com/signup?next=%2F"
username = "18759073625"
password = "qiqi730899$%."

MIN = 60*60

def get_cookies(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element_by_css_selector('.SignContainer-switch > span').click() #切换到登录窗口
    # <input name="username" type="text" class="Input" placeholder="手机号或邮箱" value="">
    driver.find_element_by_css_selector('.Input[name="username"]').send_keys(username) #账号
    # <input name="password" type="password" class="Input" placeholder="密码" value="">
    driver.find_element_by_css_selector('.Input[name="password"]').send_keys(password) #密码
    # <button type="submit" class="Button SignFlow-submitButton Button--primary Button--blue">登录</button>
    login_btn = driver.find_element_by_css_selector('.SignFlow-submitButton')  # 登录
    login_btn.click()
    # ## 【input】 <input name="captcha" type="text" tabindex="0" class="Input" placeholder="验证码" value="">
    try:
        captcha = driver.find_element_by_css_selector('.Input[name="captcha"]')
    except Exception as e:
        print("需要点击倒立的文字")
        input("输入任意字符完成\n>")  # 输入验证码
    else:
        print("需要填写验证码")
        captcha_str = input("输入验证码\n>")  # 输入验证码
        captcha.send_keys(captcha_str)
        login_btn.click()  # 登录
    cookies = driver.get_cookies()
    time.sleep(1*MIN)
    driver.close()
    return cookies

def get_captcha(self, lang, headers):
    """
    请求验证码的 API 接口，无论是否需要验证码都需要请求一次
    如果需要验证码会返回图片的 base64 编码
    根据 lang 参数匹配验证码，需要人工输入
    :param lang: 返回验证码的语言(en/cn)
    :param headers: 带授权信息的请求头部
    :return: 验证码的 POST 参数
    """
    if lang == 'cn':
        api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
    else:
        api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    resp = self.session.get(api, headers=headers)
    show_captcha = re.search(r'true', resp.text)

    if show_captcha:
        put_resp = self.session.put(api, headers=headers)
        json_data = json.loads(put_resp.text)
        img_base64 = json_data['img_base64'].replace(r'\n', '')
        with open('./captcha.jpg', 'wb') as f:
            f.write(base64.b64decode(img_base64))
        img = Image.open('./captcha.jpg')
        if lang == 'cn':
            plt.imshow(img)
            print('点击所有倒立的汉字，按回车提交')
            points = plt.ginput(7)
            capt = json.dumps({'img_size': [200, 44],
                               'input_points': [[i[0]/2, i[1]/2] for i in points]})
        else:
            img.show()
            capt = input('请输入图片里的验证码：')
        # 这里必须先把参数 POST 验证码接口
        self.session.post(api, data={'input_text': capt}, headers=headers)
        return capt
    return ''

def add_cookies(cookies):
    u"往session添加cookies"
    c = requests.cookies.RequestsCookieJar()
    for i in cookies:    #添加cookie到CookieJar
        c.set(i["name"], i["value"])
    s.cookies.update(c)     #更新session里的cookie

if __name__ == "__main__":
    # 新建session
    s = requests.session()
    cookies = get_cookies(url)
    print(cookies)
    add_cookies(cookies)
    home = s.get(url)
    with open("home.html", "wb") as f:
        f.write(home.text.encode("utf8"))
        f.close()