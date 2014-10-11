# coding=utf-8

'''
湖南移动流量银行自动获取流量脚本 - 托盘程序
启动后最小化到托盘运行
有消息时以托盘消息进行通知
'''

import time
import random
from datetime import datetime
from PyQt4 import QtCore, QtGui
import netBank


class NetBankThread(QtCore.QThread):
    ''' 获取流量的线程类 '''
    optResultSignal = QtCore.pyqtSignal(str, str)

    def gainNet(self):
        self.start()

    def run(self):
        ''' 实际执行获取流量操作 '''
        while True:
            try:
                # 访问首页
                success, msg = netBank.index()
                if not success:
                    self.optResultSignal.emit(u'获取流量失败', msg)
                    self.sleep(False)
                    continue
                # 访问抢流量页面
                success, msg = netBank.gainNet()
                if not success:
                    self.optResultSignal.emit(u'获取流量失败', msg)
                    self.sleep(False)
                    continue
                # 抢流量
                success, msg = netBank.do()
                if not success:
                    self.optResultSignal.emit(u'获取流量失败', msg)
                    self.sleep(False)
                else:
                    self.optResultSignal.emit(u'获取流量成功', msg)
                    self.sleep(True)
            except Exception,e:
                self.optResultSignal.emit(u'程序异常', str(e))
                self.sleep(False)

    def sleep(self, success):
        ''' 暂停线程一段时间 '''
        now = datetime.now()
        if (now.minute < 59 and now.minute > 5) or success:
            # 未到抢流量时间 或 过了抢流量时间 或 本次抢成功了
            min_sleep = 60 * (60-now.minute) + (60-now.second)
            random_secs = random.randint(min_sleep, min_sleep+30)
        else:
            # 大约在抢流量的时间范围内
            random_secs = random.randint(10, 50)
        time.sleep(random_secs)


class NetBankWindow(QtGui.QMainWindow):

    def __init__(self):
        super(NetBankWindow, self).__init__()
        # 设置托盘图标与提示信息
        icon = QtGui.QIcon('netBank.ico')
        self.setWindowIcon(icon)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(icon)
        self.trayIcon.show()
        self.trayIcon.setToolTip(u'流量银行-自动获取流量')
        self.setMenu()  # 显示上下文菜单
        # 创建用于获取流量的线程 前连接信号槽
        self.thread = NetBankThread()
        self.thread.optResultSignal.connect(self.showMessage)
        self.thread.gainNet()

    def setMenu(self):
        ''' 当前上下文菜单只用于退出程序 '''
        closeAction = QtGui.QAction(u"退出", self, triggered=self.close)
        trayIconMenu = QtGui.QMenu(self)
        trayIconMenu.addAction(closeAction)
        self.trayIcon.setContextMenu(trayIconMenu)

    def showMessage(self, title, msg, msecs=5000, icon=QtGui.QSystemTrayIcon.Information):
        ''' msecs 似乎有问题 '''
        icon = QtGui.QSystemTrayIcon.Information
        self.trayIcon.showMessage(title, msg, icon, msecs)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wnd = NetBankWindow()
    wnd.hide()  # 默认隐藏窗口
    sys.exit(app.exec_())
