import pymysql

class Utility(object):

    # 构造方法（实例化时初始调用的方法）
    def __init__(self,database='woniucbt'):
        #self.db = pymysql.connect('localhost', 'root', '', 'woniucbt', charset='utf8')
        self.db = pymysql.connect(host='localhost', user='root', password='', database=database, charset='utf8')
        self.cursor = self.db.cursor()

    def query_one(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def query_all(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def update_data(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        #self.db.rollback()

    # 析构方法（收尾工作），什么时候收尾：Python高兴的时候
    def __del__(self):
        self.cursor.close()
        self.db.close()
        # print("清理工作完成...")

#
if __name__ == '__main__':
    u = Utility()
    # r1 = u.query_one('select * from report where userid = 100')
    r2 = u.query_one("SELECT * FROM report WHERE VERSION='1.3.1' limit 1,1")
    print(type(r2))
    print(f'r2={r2}')
