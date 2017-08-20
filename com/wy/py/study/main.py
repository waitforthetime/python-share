#!/usr/bin/env python3
# -*-  coding:utf-8  -*-
import logging
import datetime
from com.wy.py.study.client.share import search, query
from com.wy.py.study.mail.sendmail import send
# from jinja2 import Environment, FileSystemLoader, PackageLoader
import os
from mako import template

logging.basicConfig(level=logging.INFO)


def recent_share_info():
    data = search()
    logging.info(data)
    today = str(datetime.date.today())
    result = list()
    for i in data:
        if i['DIVIDEND_DATE'] >= today:
            page = query(i['COMPANY_CODE'])
            price = page[5]
            rate = i['DIVIDEND_PER_SHARE1_A']
            per = float(str(rate)) / float(price)
            per = float('%.02f' % (per * 100))
            msg = 'code:{dict[COMPANY_CODE]},\tname:{dict[SECURITY_ABBR_A]},' \
                  '\t红利:{dict[DIVIDEND_PER_SHARE1_A]},\t当前价格:{price},' \
                  '\t股息率:{per}%,\t登记日:{dict[DIVIDEND_DATE]},\t除息日:{dict[EX_DIVIDEND_DATE_A]}' \
                .format(dict=i, price=price, per=per)
            i['rate'] = per
            i['price'] = price
            result.append(i)
            if per > 1:
                logging.info(msg)
    dd = sorted(result, key=lambda x: x['rate'] if 'rate' in x else -1, reverse=True)
    return dd

# 使用Jinja2 好像不太支持python3
# def data2temp(name, data):
#     env = Environment(autoescape=True, loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
#     template = env.get_template(name)
#     rs = template.render(data=data)
#     return rs


def data2temp(name, data):
    t = template.Template(filename=name)
    return t.render(data=data)


def main():
    # page = data2temp(name='templates/dic_test.html', data='')
    # logging.info(page)
    data = recent_share_info()
    page = data2temp(name='templates/share_rate.html', data=data)
    logging.info(page)
    send(txt=page, to_addr='ss@qq.com', subject='ss', type='html')

if __name__ == '__main__':
    main()
