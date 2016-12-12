#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from MySQLdb.cursors import DictCursor  
from DBUtils.PooledDB import PooledDB 

www_con = PooledDB(creator=MySQLdb, mincached=1, maxcached=20, host='10.101.1.127', port=3306 , user='root', passwd='s6r(2wSrySoj', db='www_com',use_unicode=False,charset="utf8", cursorclass=DictCursor)
www_qianyilc_com = www_con.connection()

st_con = PooledDB(creator=MySQLdb, mincached=1, maxcached=20, host='10.101.1.127', port=3306 , user='root', passwd='s6r(2wSrySoj', db='statistics_com',use_unicode=False,charset="utf8", cursorclass=DictCursor)
statistics_qianyilc_com = st_con.connection()

credits_con = PooledDB(creator=MySQLdb, mincached=1, maxcached=20, host='10.101.1.127', port=3306 , user='root', passwd='s6r(2wSrySoj', db='credits_com',use_unicode=False,charset="utf8", cursorclass=DictCursor)
credits_qianyilc_com = credits_con.connection()

con = PooledDB(creator=MySQLdb, mincached=1, maxcached=20, host='127.0.0.1', port=3306 , user='shang', passwd='132132', db='gy',use_unicode=False,charset="utf8", cursorclass=DictCursor)
gy = con.connection()
