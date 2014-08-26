# coding utf-8

import MySQLdb
import MyLogger
from Item import FilmItem

log = MyLogger.log


def init_conn(hostVal='localhost', userVal='root', passwdVal = '123456', portVal = 3306):
	try :
		conn = MySQLdb.connect(host=hostVal, user=userVal, passwd=passwdVal, port=portVal, charset='utf8')
		cur = conn.cursor()
		cur.execute("SET NAMES utf8")
		return conn
	except MySQLdb.Error,e:
		log.error(e)


connection = init_conn()
cursor = connection.cursor()
database = 'film_new'
table = 'films'
crawled_table = 'pop_crawled'

def insert_film(item, dbName=database, film_tableName=table, crawled_tableName=crawled_table, conn=connection, cur=cursor):
	insert_filmItem(item, dbName=database, tableName=film_tableName, conn=connection, cur=cursor)
	insert_crawled(item['sub_id'], dbName=database, tableName=crawled_table, conn=connection, cur=cursor)

def insert_crawled(id, dbName=database, tableName=crawled_table, conn=connection, cur=cursor):
	sql = 'insert into ' + tableName + ' (sub_id) values (\'' + id + '\')'
	log.debug(sql)
	execute_sql(sql, dbName, conn, cur)

def insert_filmItem(item, dbName=database, tableName=table, conn=connection, cur=cursor):
	sql = 'insert into ' + tableName + ' (name, director, scenarist, actors, type, area, language, releaseDate, length, alias, rate, description, img) values (' + '\'' + item['name'] + '\',' + '\'' + item['director'] + '\','+ '\'' + item['scenarist'] + '\','+ '\'' + item['actors'] + '\',' + '\'' + item['type'] + '\',' + '\'' + item['area'] + '\',' + '\'' + item['language'] + '\',' + '\'' + item['releaseDate'] + '\',' + '\'' + item['length'] + '\','+ '\'' + item['alias'] + '\','+ item['rate'] + ',\'' + item['description'] + '\',\'' + item['sub_id'] + '\')'
	log.debug(sql)
	execute_sql(sql, dbName, conn, cur)

def execute_sql(sql, dbName=database, conn=connection, cur=cursor):
	if conn == None:
		return
	if dbName != None:
		conn.select_db(dbName)
	if cur == None:
		cur = conn.cursor()
	
	try :
		cur.execute(sql)
	except MySQLdb.Error,e:
		log.error(e)

def execute_sql_query(sql, dbName=database, tableName=table, conn=connection, cur=cursor):
	if conn == None:
		return
	if dbName != None:
		conn.select_db(dbName)
	if cur == None:
		cur = conn.cursor()
	
	try :
		cur.execute(sql)
		return cur.fetchall()
	except MySQLdb.Error,e:
		log.error(e)



def is_url_not_crawled(sub_id):
	sql = 'select * from ' + crawled_table  + ' where sub_id = \'' + sub_id + '\''
	log.debug(sql)
	result = execute_sql_query(sql)
	return result==()

