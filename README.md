# DYWHouse
最近关注大亚湾房产，正好学习python中，就使用BeautifulSoup+Mysql,爬了10W+条的房产登记数据

# 涉及的url

## 网页主页
herf_host = "http://61.142.120.214:9000/web/"
## 第一层
allherf_content_1 = herf_host + "salepermit.jsp?page={0}"
## 第二层
allherf_content_2 = herf_host + "realestate_presale.jsp?licenceCode=#&ProjectCode=DYW00121014"
## 第三层
allherf_content_3 = herf_host + "salestable.jsp?buildingcode=DYW0012101401&projectcode=DYW00121014"
## 第四层
allherf_content_4 = herf_host + "House.jsp?id={0}&lcStr={1}"

# 示例图片
![示例1](http://7pn5vy.com1.z0.glb.clouddn.com/%E5%A4%A7%E4%BA%9A%E6%B9%BE_all.png)
![示例2](http://7pn5vy.com1.z0.glb.clouddn.com/%E7%8E%96%E9%BE%99%E6%B9%BE_2.png)
![示例3](http://7pn5vy.com1.z0.glb.clouddn.com/%E7%8E%96%E9%BE%99%E6%B9%BE_8.png)
![示例3](http://7pn5vy.com1.z0.glb.clouddn.com/%E7%8E%96%E9%BE%99%E6%B9%BE_5.png)
