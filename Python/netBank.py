# coding=utf-8
'''
湖南移动流量银行自动获取流量脚本
'''

import urllib2
import urllib
from datetime import datetime
import time
import random

# 流量银行主页地址 需要先请求该地址以更新cookies
URL_INDEX = 'http://wap.hn.10086.cn/wap/weixin/netBank/index.jsp'

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
        return False
    return True


def do():
    ''' 抢流量 '''
    resp = opener.open(URL_DO, DATA_DO)
    content = resp.read().decode('utf-8')
    if -1 == content.find(u'流量银行余额'):
        now = datetime.now()
        filename = 'do ' + now.strftime('%Y-%m-%d %H_%M_%S') + '.html'
        save_content_to_file(content, filename)

    # 抢流量失败时的提示
    pos = content.find('<div class="e_redBtn">')
    if -1 != pos:
        start = pos + len('<div class="e_redBtn">')
        end = content.find('</div>', start)
        if -1 != end:
            print content[start:end]

    # 当前流量余额
    pos = content.find('<span class="f_green">')
    if -1 != pos:
        start = pos + len('<span class="f_green">')
        end = content.find('</span>', start)
        if -1 != end:
            print u'当前流量余额：' + content[start:end]


if __name__ == '__main__':
    index()
    random_secs = random.randint(1, 5)
    time.sleep(random_secs)
    do()
