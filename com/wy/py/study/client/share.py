#!/usr/bin/env python3
# -*-  coding:utf-8  -*-
from urllib import request, parse, error
import json
import datetime
import time
import logging

logging.basicConfig(level=logging.INFO)


def req(url, headers={}, data={}):

    try:
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, data=data, headers=headers)
        resp = request.urlopen(req)
        # logging.info('status:%s, reason:%s', *(resp.status, resp.reason))
        if resp.status == 200:
            page = resp.read()
            page = page.decode('utf-8')
            return page
    except error.URLError as e:
        logging.error('error code:%s, reason:%s', *(e.code, e.reason))
    return ''


def getreq(url, headers={}, data={}, charset='utf-8'):
    data = parse.urlencode(data).encode('utf-8')
    try:
        req = request.Request(url+str(data), headers=headers)
        resp = request.urlopen(req)
        # logging.info('status:%s, reason:%s', *(resp.status, resp.reason))
        if resp.status == 200:
            page = resp.read()
            page = page.decode(charset)
            return page
        else:
            logging.info('http no response')
    except error.URLError as e:
        logging.error('error code:%s, reason:%s', *(e.code, e.reason))
    return ''


def search(page_size=100, record_data=datetime.datetime.now().strftime('%Y')):
    url = 'http://query.sse.com.cn/commonQuery.do'
    rfurl = 'http://www.sse.com.cn/market/stockdata/dividends/dividend/'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Referer': rfurl,
        'Connection': 'keep-alive'
    }
    data = {
        # 'jsonCallBack': 'jsonpCallback44840',
        'isPagination': 'true',
        'sqlId': 'COMMON_SSE_GP_SJTJ_FHSG_AGFH_L_NEW',
        'pageHelp.pageSize': page_size,
        'pageHelp.pageNo': '1',
        'pageHelp.beginPage': '1',
        'pageHelp.endPage': '5',
        'pageHelp.cacheSize': '1',
        'record_date_a': record_data ,
        'security_code_a': '',
        '_': '1503147831077'
    }
    page = req(url=url, headers=headers, data=data)
    return parse_info(page, 'pageHelp', 'data')


def query(company):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/51.0.2704.63 Safari/537.36',
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/info/price/index.shtml?COMPANY_CODE='+company,
        'Connection': 'keep-alive'
    }

    url = 'http://yunhq.sse.com.cn:32041/v1/sh1/snap/' + company + '?'
    data = {
        'select': 'name, last, chg_rate, change, amount, volume, open, prev_close, ask, bid, high, low, tradephase',
        '-': int(time.time())
    }
    page = getreq(url=url, headers=headers, data=data, charset='gb2312')
    return parse_info(page, 'snap')


class HttpNoResponseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def parse_info(page, *args):
    info = json.loads(page)
    if len(args) != 0:
        for key in args:
            if key in info.keys():
                info = info[key]
            else:
                return ''
    return info


def main():
    logging.info('start')
    data = search()
    logging.info('1111')
    logging.info(data)
    today = str(datetime.date.today())
    for i in data:
        if i['DIVIDEND_DATE'] >= today:
            page = query(i['COMPANY_CODE'])
            price = page[5]
            rate = i['DIVIDEND_PER_SHARE1_A']
            per = float(str(rate))/float(price)
            per = float('%.02f' % (per*100))
            if per > 1:
                # logging.info('price:%s, rate:%s', price, rate)
                logging.info('code:{dict[COMPANY_CODE]},\tname:{dict[SECURITY_ABBR_A]},'
                             '\t红利:{dict[DIVIDEND_PER_SHARE1_A]},'
                             '\t当前价格:{price},\t股息率:{per}%'
                             '\t登记日:{dict[DIVIDEND_DATE]},\t除息日:{dict[EX_DIVIDEND_DATE_A]}'
                             .format(dict=i, price=price, per=per))

if __name__ == '__main__':
    main()