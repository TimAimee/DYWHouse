# -*- coding:utf-8 -*-
import random

from bs4 import BeautifulSoup
import json
import re
import urllib2

# 网页主页
herf_home = "http://61.142.120.214:9000/web"
allherf_content_1 = herf_home + "/salepermit.jsp"
allherf_content_2 = herf_home + "/web/realestate_presale.jsp?licenceCode=#&ProjectCode=DYW00121014"
allherf_content_3 = herf_home + "/salestable.jsp?buildingcode=DYW0012101401&projectcode=DYW00121014"
allherf_content_4 = herf_home + "/House.jsp?id={0}&lcStr={1}"


def get_soupform_url(url):
    """
    获取soup网页对象 \n
    :param url: 主机的地址\n
    :return: soup对象\n
    """
    # 加载网页的对象
    try:
        resp = urllib2.urlopen(url)
    except Exception:
        return None
    # 获取网页的对象
    html = resp.read()
    # BeautifulSoup
    soup = BeautifulSoup(html, "html.parser", from_encoding="GBK")
    return soup


def get_allherf_content(url):
    """
    获取所有超链接的内容 \n
    :param url: 主机的地址\n
    :return: 所有超链接的内容\n
    """
    nameList = []
    soup = get_soupform_url(url)
    if soup == None:
        return nameList
    # 获取网页中所有的超链接
    nameList = soup.findAll("a")
    return nameList


def get_house_id_list(url):
    list = []
    soup = get_soupform_url(url)
    table_body = soup.findAll('div', attrs={'style': 'cursor:hand'})
    for item in table_body:
        onclick_ = str(item.attrs['onclick'])
        list.append(get_list_id(onclick_))
    return list


def get_list_id(str):
    # openContent(377321,0)-->377321;
    id = ""
    searchObj0 = re.finditer(r"\d{6}", str)
    for match in searchObj0:
        id = match.group()
    return id


def get_table_conent_house_detail(url):
    dic = {};
    housePrice = 0;
    housemm = 1;
    soup = get_soupform_url(url)
    table_body = soup.find('table', attrs={'width': '862'})
    # print table_body
    rows = table_body.find_all('tr')
    for row in rows:
        colth = row.find_all('th')
        colth = [ele.text.strip() for ele in colth]
        coltd = row.find_all('td')
        coltd = [ele.text.strip() for ele in coltd]
        if (len(colth) == 0):
            for i in range(0, len(coltd)):
                # 单行的title
                pass
        else:
            for i in range(0, len(colth)):
                if u"价目表" in colth[i]:
                    housePrice = float(coltd[i].encode("utf-8"))
                if u"总面积" in colth[i]:
                    housemm = float(coltd[i].encode("utf-8"));
                dic.update({colth[i]: coltd[i]})
    mprice = housePrice / housemm
    dic.update({"单价": int(mprice)})
    return dic;


def get_herf(url):
    list_dic = []
    list = get_house_id_list(url)
    for i in list:
        url_house_detail = allherf_content_4.format(i, "0")
        list_dic.append(get_table_conent_house_detail(url_house_detail))
        print random.randint(0,1),
        if len(list_dic) % 50 == 0:
            print ""
    return list_dic


if __name__ == "__main__":
    house_list = get_herf(allherf_content_3)
    print "\n共收录", len(house_list), "套房子信息"
    for item in house_list:
        print json.dumps(item, ensure_ascii=False, encoding='UTF-8')
