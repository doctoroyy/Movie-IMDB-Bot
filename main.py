# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re
import traceback
from time import sleep

import requests
from lxml import etree
from vika import Vika
import os

def get_html_doc(url):
    head = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }
    resopnse = requests.get(url, headers=head)

    resopnse.encoding = 'utf-8'
    html_doc = resopnse.text
    return html_doc


def find_all_by_pat(pat, string):
    res = re.findall(pat, string)
    return res


def search_fields_by_xpath(html):
    def func(__xpath):
        res = html.xpath(__xpath)
        try:
            return res[0].strip()
        except:
            return 'not found'

    return func


def get_chinese_name(html):
    chinese_name_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a/text()'
    return search_fields_by_xpath(html)(chinese_name_xpath)


def get_director_name(html):
    director_name_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/div/span[4]/text()'
    res = search_fields_by_xpath(html)(director_name_xpath)
    if res != 'not found':
        return res.split(' / ')[1]
    return res


def get_desc(html):
    desc_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/p/text()'
    return search_fields_by_xpath(html)(desc_xpath)


def get_douban_info(query_name):
    url = 'https://www.douban.com/search?cat=1002&q=%s' % query_name
    douban_doc = get_html_doc(url)
    html = etree.HTML(douban_doc)
    return {
        'chineseName': get_chinese_name(html),
        'directorName': get_director_name(html),
        'desc': get_desc(html)
    }


if __name__ == '__main__':
    vika = Vika(os.environ['API_TOKEN'])
    # 通过 datasheetId 来指定要从哪张维格表操作数据。
    datasheet = vika.datasheet(os.environ['DATASHEET_ID'], field_key="name")
    # 返回所有的记录
    records = datasheet.records.all()

    url = "https://www.imdb.com/chart/top"
    imdb_doc = get_html_doc(url)
    pat = r'<td class="titleColumn">\s*(.*)..*\s*.*\s<a\s.*href="/title/(.*)/.*"\s.*title="(.*)\s.*\(dir\.\).*" >(.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span>'
    movie_tuples = find_all_by_pat(pat, imdb_doc)

    movie_list = [{
        'rank': _[0],
        'id': _[1],
        'director': _[2],
        'eng_name': _[3],
        'year': _[4],
        'chi_name': ''
    } for _ in movie_tuples]

    for record in records:
        record.update({
            'rank': None
        })
        sleep(0.6)

    for movie in movie_list:
        if records.filter(id=movie['id']).count() == 0:
            info = get_douban_info(movie['id'])
            if info['chineseName'] != 'not found':
                print('ready to insert: ', info['chineseName'])
                try:
                    datasheet.records.create({
                        "id": movie['id'],
                        "chi_name": info['chineseName'],
                        "eng_name": movie['eng_name'],
                        "director": info['directorName'],
                        "director_name_en": movie['director'],
                        "year": movie['year'],
                        'rank': int(movie['rank'])
                    })


                except Exception as e:
                    traceback.print_exc()
            else:
                print('not fount')
            sleep(8)
        else:
            row = records.filter(id=movie['id'])[0]
            row.update({
                'rank': int(movie['rank'])
            })
            sleep(0.02)
