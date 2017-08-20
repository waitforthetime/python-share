#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
from email.mime import text
import smtplib
from email.header import Header
from email.utils import parseaddr, formataddr

logging.basicConfig(level=logging.INFO)

__smtp_server = 'smtp.163.com'
__smtp_port = 25
__from_addr = '313799398@163.com'
__password = 'wangY061504'


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send(txt, to_addr, subject, type='plain'):
    try:
        msg = getmsg(txt=txt, from_addr=__from_addr, to_addr=to_addr, subject=subject, type=type)
        server = smtplib.SMTP(host=__smtp_server, port=__smtp_port)
        server.login(user=__from_addr, password=__password)
        server.sendmail(from_addr=__from_addr, to_addrs=[to_addr], msg=msg.as_string())
        server.quit()
    except smtplib.SMTPDataError as e:
        logging.error(e)


def getmsg(txt, to_addr, subject, from_addr=__from_addr, type='plain'):
    msg = text.MIMEText(txt, type, 'utf-8')
    msg['From'] = _format_addr('王元 <%s>' % from_addr)
    msg['To'] = _format_addr('王元 <%s>' % to_addr)
    msg['Subject'] = Header(subject, 'utf-8').encode()
    return msg


def main():
    txt = '<h1>周末过来玩</h1>'
    to_addr = '313799398@qq.com'
    subject = '最近分红股票'
    send(txt=txt, to_addr=to_addr, subject=subject, type='html')

if __name__ == '__main__':
    main()



