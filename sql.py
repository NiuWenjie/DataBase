# mysql底层，增、删、查、改命令
import pymysql

class MySQLBaseHandle(object):
    def __init__(self, host, user, pwd, database):
        '''初始化数据库信息并创建数据库连接'''
        self.host, self.user, self.pwd, self.database = host, user, pwd, database
        self.conn = pymysql.connect(host = self.host, user = self.user, password = self.pwd, database = self.database, charset='utf8')
        
    def insertDB(self, sql):
        ''' 插入数据库操作 '''
        self.cursor = self.conn.cursor()

        try:
            # self.cursor.execute(sql)
            tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
        finally:
            self.cursor.close()
            return tt if 'tt' in dir() else 0

    def deleteDB(self,sql):
        ''' 操作数据库数据删除 '''
        self.cursor = self.conn.cursor()

        try:
            # self.cursor.execute(sql)
            tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            print(tt)
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
        finally:
            self.cursor.close()
            return tt

    def updateDb(self,sql):
        ''' 更新数据库操作 '''
        self.cursor = self.conn.cursor()

        try:
            # self.cursor.execute(sql)
            tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            print(tt)
            self.conn.commit()
        except:
            # 发生错误时回滚
            self.conn.rollback()
        finally:
            self.cursor.close()

    def selectDb(self,sql):
        ''' 数据库查询 '''
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

        try:
            # self.cursor.execute(sql) # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            data = self.cursor.fetchall() # 返回所有记录列表
            print(tt, data)
        except:
            tt, data = 0, None
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()
            return tt, data


    def closeDb(self):
        ''' 数据库连接关闭 '''
        self.conn.close()
        print("关闭数据库！")