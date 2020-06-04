import mysql.connector
from cfg.config import MYSQL_CONFIG

mydb = mysql.connector.connect(
    host=MYSQL_CONFIG["host"],
    user=MYSQL_CONFIG["user"],
    passwd=MYSQL_CONFIG["passwd"],
    database=MYSQL_CONFIG["database"]
)
mycursor = mydb.cursor()

def get_all_stock_ticket():
    mycursor.execute("SELECT * FROM stock")
    results = mycursor.fetchall()
    return [result[0] for result in results]

def get_keywords_by_stock_ticket(stock_ticket:str):
    mycursor.execute("SELECT keyword.keyWord from keyword,crawlkey where crawlkey.keywordId = keyword.keywordId and crawlkey.stockTicket = '{}'".format(stock_ticket))
    results = mycursor.fetchall()
    return [result[0] for result in results]
