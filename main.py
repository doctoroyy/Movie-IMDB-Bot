# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re
from time import sleep
import requests
from lxml import etree
from vika import Vika

from sync_to_sharing_sheet import sync_to_sharing_sheet
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
      return None

  return func


def get_chinese_name(html):
  chinese_name_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/h3/a/text()'
  return search_fields_by_xpath(html)(chinese_name_xpath)


def get_director_name(html):
  director_name_xpath = '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div/div/span[4]/text()'
  res = search_fields_by_xpath(html)(director_name_xpath)
  if res is not None:
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


def reset_all_rank_to_none(records):
  for record in records:
    record.update({
      'rank': None
    })
    sleep(0.6)
  print('Reset Done!❤')


if __name__ == '__main__':
  vika = Vika(os.environ['VIKA_API_TOKEN'])

  # 影视数据库
  dst_imdb = vika.datasheet(os.environ['DATASHEET_ID'], field_key="name")

  # 分享给外部的 top 250 数据表
  dst_sharing = vika.datasheet(os.environ['SHARING_DST_ID'], field_key="id")

  records = dst_imdb.records.all()

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

  reset_all_rank_to_none(records)

  for movie in movie_list:
    rows = records.filter(id=movie['id'])
    if rows.count() == 0:
      info = get_douban_info(movie['id'])  # {'chineseName': '', 'directorName': '','desc': ''}
      print('ready to insert: ', info['chineseName'])
      try:
        dst_imdb.create_records({
          "id": movie['id'],
          "chi_name": info['chineseName'],
          "eng_name": movie['eng_name'],
          "director": info['directorName'],
          "director_name_en": movie['director'],
          "year": movie['year'],
          'rank': int(movie['rank'])
        })
        sleep(8)
      except:
        raise Exception

    else:
      rows[0].update({
        'rank': int(movie['rank'])
      })
      sleep(0.02)

  print('All Done!❤')

  sync_to_sharing_sheet(dst_imdb=dst_imdb, dst_sharing=dst_sharing)
