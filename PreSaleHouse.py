# -*- coding:utf-8 -*-
import json
import re
import urllib2
from urllib import quote

import MySQLdb as mdb
from bs4 import BeautifulSoup

# 网页主页
herf_host = "http://61.142.120.214:9000/web/"
# 第一层
allherf_content_1 = herf_host + "salepermit.jsp?page={0}"
# 第二层
allherf_content_2 = herf_host + "realestate_presale.jsp?licenceCode=#&ProjectCode=DYW00121014"
# 第三层
allherf_content_3 = herf_host + "salestable.jsp?buildingcode=DYW0012101401&projectcode=DYW00121014"
# 第四层
allherf_content_4 = herf_host + "House.jsp?id={0}&lcStr={1}"

house_list_all = []
progress_all = 0
conn = None
cursor = None
have_create_table = False


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
    # url-->house id
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


def insert_db(dic):
    global conn, cursor, have_create_table

    if not have_create_table:
        sql_create_table = get_sql_create_table(dic)
        cursor.execute(sql_create_table)
        have_create_table = True

    sql_insert_value = get_sql_insert_table(dic)
    cursor.execute(sql_insert_value)
    conn.commit()


def get_table_conent_house_detail(url, dic_time_open):
    ##第四层 house_table-->dic
    global sql_key
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
                key = colth[i].encode("utf-8").replace("：", "").decode("utf-8")
                value = coltd[i].encode("utf-8").replace("：", "").decode("utf-8")
                value = "\"" + value + "\""
                if u"价目表" in colth[i]:
                    key = u"总价"
                    housePrice = float(coltd[i].encode("utf-8"))
                if u"总面积" in colth[i]:
                    housemm = float(coltd[i].encode("utf-8"));
                dic.update({key: value})
    mprice = housePrice // housemm
    dic.update({u"单价": "\"" + str(mprice) + "\""})
    dic.update(dic_time_open)
    # print json.dumps(dic, ensure_ascii=False, encoding="utf-8")
    insert_db(dic)
    return dic;


def get_herf_three(url, progress_3, dic_time_open):
    # 第三层
    global progress_all
    list_dic = []
    list = get_house_id_list(url)
    if len(list) == 0:
        progress_4 = progress_3
        return
    else:
        progress_4 = float(progress_3) / len(list)
    for i in list:
        url_house_detail = allherf_content_4.format(i, "0")
        list_dic.append(get_table_conent_house_detail(url_house_detail, dic_time_open))
        progress_all = progress_all + progress_4
        # print random.randint(0, 1),
        # if len(list_dic) % 50 == 0:
        #     print ""
        # print "当前进度:", progress_all
    return list_dic


def get_code_url(str):
    # realestate_presale.jsp?licenceCode=惠湾房预许字【2018】第108号&ProjectCode=DYW00403004
    #                                   |||
    # realestate_presale.jsp?licenceCode=%BB%DD%CD%E5%B7%BF%D4%A4%D0%ED%D7%D6%A1%BE2018%A1%BF%B5%DA108%BA%C5&ProjectCode=DYW00403004
    searchObj0 = re.finditer("=.*&", str)
    part = ""
    for match in searchObj0:
        part = match.group().replace("=", "").replace("&", "")
        part_utf_8 = part.encode('gbk')
    part_quote = quote(part_utf_8)
    str = str.replace(part, part_quote)
    return str


# 第三层
def get_three(url_3, progress_3, dic_time_open):
    # 楼栋信息
    print "\t\t\turl_3-->", url_3
    # house_list = get_herf_three(allherf_content_3)
    house_list = get_herf_three(url_3, progress_3, dic_time_open)
    print "\t\t\t共收录", len(house_list), "套房子信息"
    house_list_all.extend(house_list)
    # for item in house_list:
    #     print json.dumps(item, ensure_ascii=False, encoding='UTF-8')


def get_time_open(url_2):
    soup = get_soupform_url(url_2)
    dic = {}
    table_body = soup.find('table', attrs={'width': '900'})
    # print table_body
    rows = table_body.find_all('tr')
    try:
        for row in rows:
            colth = row.find_all('th')
            colth = [ele.text.strip() for ele in colth]
            coltd = row.find_all('td')
            coltd = [ele.text.strip() for ele in coltd]
            if (len(colth) == 0):
                pass
            else:
                for i in range(0, len(colth)):
                    key = colth[i]
                    value = coltd[i]
                    value = "\"" + value + "\"";
                    if u"开盘时间" in colth[i]:
                        dic = {key: value}
                        break
    except Exception:
        pass
    return dic


# 第二层
def get_two(house_name, url_2, progress_2):
    global progress_all
    # 项目页面（第几栋）
    print "\t\turl_2:", house_name, "-->", url_2
    progress = 0
    list_buildingCode = []
    list_herf_two = get_allherf_content(url_2)
    dic_time_open = get_time_open(url_2)
    for item in list_herf_two:
        href_buildingCode = item['href']
        if "buildingcode" in href_buildingCode:
            list_buildingCode.append(href_buildingCode)

    if len(list_buildingCode) == 0:
        progress_3 = progress
        return
    else:
        progress_3 = float(progress_2) / len(list_buildingCode)

    for item in list_buildingCode:
        url_3 = herf_host + item
        progress_all = progress_all + progress_3
        get_three(url_3, progress_3, dic_time_open)
        # print "当前进度:", progress_all


# 第一层 当前页
def get_one(url_1, progress):
    global progress_all
    # 预售证页面
    print "\turl_1-->", url_1
    list_herf_one = get_allherf_content(url_1)
    list_licenceCode = []
    list_licenceCode_house = []
    progress_2 = 0
    for item in list_herf_one:
        href_licenceCode = item['href']
        if "licenceCode" in href_licenceCode:
            list_licenceCode.append(get_code_url(href_licenceCode))
            list_licenceCode_house.append(item.text)

    if len(list_licenceCode) == 0:
        progress_2 = progress
        return
    else:
        progress_2 = float(progress) / len(list_licenceCode)

    # 第二层
    for item in list_licenceCode:
        url_2 = herf_host + item
        progress_all = progress_all + progress_2
        house_name = list_licenceCode_house[list_licenceCode.index(item)]
        get_two(house_name, url_2, progress_2)
        # print "当前进度:", progress_all,progress_2


# 第一层,下一页
def get_all_persell_house():
    global progress_all
    progress_1 = 100 / 20
    for i in range(1, 21):
        allherf_content_pager = allherf_content_1.format(i, "0")
        get_one(allherf_content_pager, progress_1)
        progress_all = progress_all + progress_1 * i
        # print "当前进度:", progress_all,progress_1
    print "一共收录", len(house_list_all), "套房子信息"


def get_sql_create_table(dict):
    keys_list = " CHAR(100),".join(dict.keys()).encode("utf-8")
    sql = """CREATE TABLE house ({0} CHAR(100))""".format(keys_list)
    return sql


def get_sql_insert_table(dict):
    # sql = """INSERT INTO house (id, 单价) VALUES (1,"15779" )"""
    keys_list = ",".join(dict.keys()).encode("utf-8")
    value_list = ",".join(dict.values()).encode("utf-8")
    sql = """INSERT INTO house ({0}) VALUES ({1})""".format(keys_list, value_list)
    return sql


def read_and_save():
    global conn, cursor
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'db': 'housedb',
        'passwd': 'timaimee',
        'charset': 'utf8'
    }
    conn = mdb.connect(**config)
    cursor = conn.cursor()
    get_all_persell_house()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    read_and_save()
