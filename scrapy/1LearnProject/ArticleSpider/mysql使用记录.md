【背景】使用阿里云的香港服务器

1. 创建article_spider数据库
2. 按照items.py中JobBoleArticleItem的字段来建立表格
3. 安装连接mysql的包`pip install mysqlclient`

# 错误集
【版本】https://github.com/PasserQi/CrawlerForPython/commit/51bc98292364247e0dc5c1c84337f3b83d9b1610
【错误1】`MySQLdb._exceptions.OperationalError: (1366, "Incorrect string value: '\\xF0\\x9F\\x8C\\xB0\\xE3\\x80...' for column 'content' at row 1")`

【错误2】`MySQLdb._exceptions.OperationalError: (2006, 'MySQL server has gone away')`
【解决】python与数据库的连接失败了，失败原因有多种，可能是提前关闭了连接，也有可能是由于超时连接而失败。最简单的方法就是多连几次数据库。
【原因】
1. 在使用scrapy异步插入时，由于错误1编码问题没有解决，所以导致插入错误，之后超时退出

# 基础操作
```
# 查看本机IP
ipconfig
# 安装
sudo apt-get install mysql-server
apt-get install mysql-client
sudo apt-get install libmysqlclient-dev
# 查看mysql安装目录
whereis mysql
# 查看mysql的进程
ps aux|grep mysqld
# 登录
mysql -uroot -p
# 重启
sudo service mysql restart
# 权限设置命令：只有设置这个，外部IP才能进来（阿里云的服务器还需要配置安全组）
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'IDENTIFIED BY '密码' WITH GRANT OPTION; #所有IP通过root账号、root密码进来的，享有所有表的所有权限
    # *.* 所有的表都赋权限
    # 'root' 通过root连进来
    # '%' 所有IP
    # 'root'密码
flush privileges; #刷新
```

# Navicat for MySQL
```
字符集：utf8 -- UTF-8 Unicode
排序规则：utf8_general_ci
```

数据库复制
1. 把数据库A全部传输到数据库B，B中右键'数据传输'
2. 导出->导出


# 配置文件

```
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf # 配置文件
bind-address = 127.0.0.1 #默认为127.0.0.1（本机地址）
    # 设置为0.0.0.0，对外部IP地址进行监听
user = mysql
    # 通过mysql来启动
datadir = /var/lib/mysql #数据文件存放的目录
```

# SQL
```sql
show database #显示数据库
exit;         #退出
```