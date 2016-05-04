#-*- coding:utf-8 -*-
#if rs has some new goods that I am interested in
#the program will send emails to my mobile
import urllib2
import time,os
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


def gettid():
    with open('Desktop/test','r') as f:
        tid = int(f.read())
        f.close()
    return tid
def storetid(tid):
    with open('Desktop/test','w') as f:
        f.write(str(tid))
        f.close()

class rs_remind():
    def __init__(self):
        self.base_url = 'http://rs.xidian.edu.cn/forum.php?mod=ajax&action=forumchecknew&fid=110&time='
        self.end_url = '&uncheck=2&inajax=yes&inajax=1&ajaxtarget=forumnew'
        self.pattern = re.compile(r'.*?{\'tid\':(.*?),.*?}')
        self.max_tid = gettid()
        self.find_list = ['移动硬盘','鼠标','计算机','罗技','雷蛇','流量卡','Python','python','Mac']

    def get_new(self):
        start_time = time.time()
        url = self.base_url + str(int(start_time)) + self.end_url
        # print url
        while 1:
            try:
                response = urllib2.urlopen(url).read()
                if re.findall(self.pattern,response):
                    tid = re.findall(self.pattern,response)[0]
                    self.judge_new(int(tid))
            except urllib2.URLError:
                os.system('python Documents/py_project/rs_trade-reminder.py')
                # print tid
            finally:
                time.sleep(3)

    def judge_new(self,tid):  #
        if int(tid) > self.max_tid :
            print "发现新主题……"
            self.max_tid = tid
            storetid(tid)
            item_url = 'http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=' + str(tid)
            response = urllib2.urlopen(item_url).read()
            self.get_info(response)
        else:
            self.get_new()

    def get_info(self,response):  # 搜索关键词 找到页面信息，否则跳转get_new
        global type,title,info
        soup = BeautifulSoup(response)
        info = soup.find(id=re.compile(r'postmessage.*?')).text
        for i in self.find_list:
            if re.search(i,info.encode('utf-8')):
                print "符合搜索条件信息……"
                type = soup.find(href=re.compile(r'.*?typeid.*?')).text  # 新校区还是老校区
                title = soup.find(id='thread_subject').text  # 标题
                print "找到所需信息……"
                self.send_mail()  # 详细信息
                self.get_new()
        print "不符合搜索条件……"
        self.get_new()
        # self.get_new()

    def send_mail(self):
        print "正在发送邮件……"
        from_addr = '' # 发送方地址
        passwd = '' # 密码
        to_addr = '' # 接收方地址
        smtp_server = 'smtp.qq.com' # 需要开启服务
        # msg = MIMEText('%s/n/n%s/n/n%s/n'%(type,title,info),'plain','utf-8')
        msg = MIMEText('%s\n%s\n%s'%(type,title,info),'plain','utf-8')
        msg['Subject'] = Header(u'RS 提醒')
        server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
        server.login(from_addr, passwd)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        print "发送完毕……"
        server.quit()

if __name__ == '__main__':
    s = rs_remind()
    s.get_new()
