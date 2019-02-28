# coding:utf8
import requests

# 将从浏览器上复制的cookie字符串转化为python的Dict
def stringToDict(cookie):
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        itemDict[key] = value
    return itemDict


# 复制你获得cookie值
cookie_str = '''_xsrf=Epn8I8ylilBwdsWtg1AmSCFQtS8XL35n; _zap=1001ee80-19ef-4805-987e-573664cee092; d_c0="AABkXPjs6A6PThNkL_tXvs86oU_w9jqqRPE=|1548929545"; tst=r; q_c1=1d44866d10234479a892195d1c0c4431|1548929585000|1548929585000; l_cap_id="MjYyZTZlZGI5MTkzNDA0NzgyMjg5ZWZjNjNkYTZlY2M=|1548989365|bcac05c60e956f7bd1c0e39b0504c48e8c04ab83"; r_cap_id="NjJhNGM2ODBlYjc5NDM5N2FjYTA3ZjVlODNiZDc2ZWI=|1548989365|8a2a498bc44710c867cddc394e8265b0338f3917"; cap_id="MDY3ZTQ5ZDNjNTFjNDRmZmFmMTg1OGM5ZDkxZDk4N2U=|1548989365|c597dce0fef3471f2e1a84234e4c8ae1382cfd55"; __utma=51854390.652816207.1548989368.1548989368.1549017246.2; __utmz=51854390.1549017246.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20160508=1^3=entry_date=20160508=1; capsion_ticket="2|1:0|10:1549017293|14:capsion_ticket|44:OGRhMTc1NTVkMDcxNDQzZDkyZGZjZmI1OTViZGZhNmI=|2a41ed665192de1ca0ff8dddad71796109ebdea65d6c45b7b15b12161e057184"; z_c0="2|1:0|10:1549017310|4:z_c0|92:Mi4xck9MX0FnQUFBQUFBQUdSYy1Pem9EaVlBQUFCZ0FsVk4zbTVCWFFETExwSUxuQlhUQ2l1d21hRlRuNGxROHhIVGdB|b77515ec6f93c6325343ae6666896a2137927f1ff191580f157c5a0b835ca6c3"; tgw_l7_route=116a747939468d99065d12a386ab1c5f'''
url = "https://www.zhihu.com/"


if __name__ == "__main__":

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language' : 'zh-CN,zh;q=0.9'
    }

    cookies = stringToDict(cookie_str)
    r = requests.sessions(url, headers=headers, cookies = cookies, allow_redirects=True)
    print(r.status_code)
    with open("zhihu.html", "wb") as f:
        f.write(r.text.encode("utf8"))