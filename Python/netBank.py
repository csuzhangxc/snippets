# coding=utf-8
'''
湖南移动流量银行自动获取流量脚本
'''

import urllib2
import urllib
import time
import random
from datetime import datetime

# 流量银行主页地址 需要先请求该地址以更新cookies
URL_INDEX = 'http://wap.hn.10086.cn/wap/weixin/netBank/index.jsp'

# 抢流量页面地址 通过该页面可以判断当前是否已整点开放抢流量
URL_GAIN_NET = 'http://wap.hn.10086.cn/wap/weixin/netBank/gainNet.jsp'

# 抢流量操作的地址
URL_DO = 'http://wap.hn.10086.cn/wap/weixin/netBank/netBank.do'


# 访问主页时需要携带的POST表单数据
DATA_INDEX = urllib.urlencode({
    'key': '通过抓包获取',
    'msisdn': '已登记手机号',
})

# 执行抢流量操作时需要携带的POST表单数据
DATA_DO = urllib.urlencode({
    'operation': 'operation',
    'busiId': 'netBank',
    'subId': 'redPkgHq',
    'ecbBusiCode': 'FLOWBANK001',
    'operType': '2',
    'url': '/wap/weixin/netBank/gainNetRs.jsp',
})


# HTTP操作相关对象
cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)


def save_content_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content.encode('utf-8'))


def index():
    ''' 访问主页 '''
    resp = opener.open(URL_INDEX, DATA_INDEX)
    content = resp.read().decode('utf-8')
    if -1 == content.find(u'购流量') or -1 == content.find(u'赚流量')\
            - 1 == content.find(u'送流量') or -1 == content.find(u'我的红包'):
        now = datetime.now()
        filename = 'index ' + now.strftime('%Y-%m-%d %H_%M_%S') + '.html'
        save_content_to_file(content, filename)
        return (False, u'访问主页时发生了错误，可能原因为相关参数已失效')
    return (True, u'成功访问了主页')


def gainNet():
    ''' 访问抢流量页面 '''
    resp = opener.open(URL_GAIN_NET)
    content = resp.read().decode('utf-8')
    if -1 == content.find(u'拼手气，抢红包'):
        # 当前不可抢流量
        msg = u'当前不可抢流量'
        pos = content.find('<div class="grey_btn marginL_10 marginR_10">')
        if -1 != pos:
            start = pos + len('<div class="grey_btn marginL_10 marginR_10">')
            end = content.find('</div>', start)
            if -1 != end:
                msg = content[start:end]
        return (False, msg)
    return (True, u'成功访问了主页')


def do():
    ''' 抢流量 '''
    resp = opener.open(URL_DO, DATA_DO)
    content = resp.read().decode('utf-8')
    if -1 == content.find(u'流量银行余额'):
        now = datetime.now()
        filename = 'do ' + now.strftime('%Y-%m-%d %H_%M_%S') + '.html'
        save_content_to_file(content, filename)
        return (False, u'抢流量时发生了错误，可能原因为相关参数已失效')

    # 抢流量失败时的提示
    pos = content.find('<div class="e_redBtn">')
    if -1 != pos:
        msg = u'抢流量失败'
        start = pos + len('<div class="e_redBtn">')
        end = content.find('</div>', start)
        if -1 != end:
            msg = content[start:end]
        return (False, msg)

    msg = u'没有获取到失败提示，成没成功不知道'

    # 成功抢到了流量
    pos = content.find('<p class="f_grey tAlign_c">')
    if -1 != pos:
        msg = u'成功抢到了流量'
        start = pos + len('<p class="f_grey tAlign_c">')
        end = content.find('<font class="f_red">', start)
        if -1 != end:
            msg = content[start:end]
            start = end + len('<font class="f_red">')
            end = content.find('</font>', start)
            if -1 != end:
                msg += content[start:end]

    # 当前流量余额
    pos = content.find('<span class="f_green">')
    if -1 != pos:
        start = pos + len('<span class="f_green">')
        end = content.find('</span>', start)
        if -1 != end:
            msg += '\n' + u'当前流量余额：' + content[start:end]
    return (True, msg)


def netBank():
    ''' 上面几个函数的组合调用 '''
    # 访问流量银行主页
    succsss, msg = index()
    if not succsss:
        print msg
        return

    # 访问抢流量页面
    succsss, msg = gainNet()
    if not succsss:
        print msg
        return

    # 随机延迟几秒后抢流量
    random_secs = random.randint(1, 3)
    time.sleep(random_secs)
    succsss, msg = do()
    print msg

if __name__ == '__main__':
    netBank()
