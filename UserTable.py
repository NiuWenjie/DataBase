# 用户管理需求，传sql
import uuid
from datetime import datetime, timedelta
from sql import MySQLBaseHandle

class UserTable(object):
    ''' 用户管理表 '''

    def __init__(self, host, user, pwd, database):
        ''' 数据库连接 '''
        try:
            self.host, self.user, self.pwd, self.database = host, user, pwd, database
            self.DBHandle = MySQLBaseHandle(host = self.host, user = self.user, pwd = self.pwd, database = self.database)
            print("Connect success!")
        except:
            print("Connect failed!")

    def register(self, username, password, email, mobile, invitation_code):
        ''' 用户注册 
            STEP1：检查用户是否注册过，且获得合法邀请码
            STEP2：非注册用户，在用户表中插入新用户
        '''
        sql = 'select * from users where username = "{}" or mobile = "{}"'.format(username, mobile)
        _, user_set = self.DBHandle.selectDb(sql)
        if _ != 0:
            print("该用户已注册！")
            return
        
        if self.check_code(invitation_code)==0:
            print("邀请码已失效，请联系管理员！")
            return
        
        try:
            sql = 'insert into users (username, mobile, email, password, invitation_code) values("{}", "{}", "{}", "{}", "{}")'.format(username, mobile, email, password, invitation_code)
            self.DBHandle.insertDB(sql)
            print("用户注册成功！")
        except:
            print("用户注册失败！")

    def login(self, account, password):
        ''' 用户登录 
            STEP1：检查用户名/密码是否匹配
            STEP2：检查邀请码是否在有效期
        '''
        sql = 'select * from users where username = "{}" or mobile = "{}"'.format(account, account)
        _, user_set = self.DBHandle.selectDb(sql)
        if _ == 0:
            print("用户不存在！即将进入注册界面")
            return
        elif user_set[0]["password"]!=password:
            print("密码错误！")
            return
        else:
            sql = 'select expire_time from invitation_code where code="{}"'.format(user_set[0]["invitation_code"])
            _, res = self.DBHandle.selectDb(sql)
            if str(res[0]["expire_time"]) < datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                print("邀请码已过期，请联系管理员更新！")
                return
            print("登录成功！")

    def delete(self, username):
        ''' 用户删除（仅管理员） 
            STEP1：检查用户是否存在
            STEP2：删除对应用户
        '''
        sql = 'select * from users where username = "{}"'.format(username)
        _, user_set = self.DBHandle.selectDb(sql)
        if _ != 0:
            sql = 'delete from users where username = "{}"'.format(username)
            _ = self.DBHandle.deleteDB(sql)
            print("用户已删除！")
        else:
            print("用户不存在，请核实！")

    def update(self, account, valid_time):
        ''' 邀请码更新（仅管理员）  
            STEP1：获取用户邀请码
            STEP2：延长邀请码失效时间
        '''
        # 查询用户邀请码
        sql = 'select invitation_code from users where username = "{}" or mobile = "{}"'.format(account, account)
        _, user_set = self.DBHandle.selectDb(sql)

        if _!=0:
            # 查询邀请码信息
            sql = 'select * from invitation_code where code="{}"'.format(user_set[0]["invitation_code"])
            _, res = self.DBHandle.selectDb(sql)

            # 更新邀请码有效期
            sql = 'update invitation_code set expire_time = "{}", status = "{}" where code = "{}"'.format(valid_time, 2, user_set[0]["invitation_code"])
            self.DBHandle.updateDb(sql)
            print("邀请码有效期由{}调整至{}。".format(res[0]["expire_time"], valid_time))
        else:
            print("用户不存在")
        # if user_set[0]["expire_time"]< datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
        #     sql = 'update invitation_code set expire_time = "{}" status = "{}" where code = "{}"'.format((datetime.now() + timedelta(days=valid_time)).strftime('%Y-%m-%d %H:%M:%S'), 1, user_set[0]["invitation_code"])
        #     print("邀请码已更新！")
        # else:
        #     print("邀请码在有效期内，失效时间为{}".format(user_set[0]["expire_time"]))

    def show(self, start, pageSize):
        ''' 用户列表  
            STEP1：确认每页数量pageSize，起始位置start+1
            STEP2：查询每页内容
        '''
        sql = "select username, mobile, email from users limit {} offset {}".format(pageSize, start)
        _, user_set = self.DBHandle.selectDb(sql)
        return _, user_set
    
    def generate_invitation_code(self, inviter, valid_time): # 
        ''' 生成邀请码
        '''
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # expire_time = (datetime.now() + timedelta(days=valid_time)).strftime('%Y-%m-%d %H:%M:%S')
        expire_time = valid_time
        code = str(uuid.uuid4()).replace('-', '').upper()
        status = str(1)
        try:
            sql = 'select * from users where username = "{}"'.format(inviter)
            _, res = self.DBHandle.selectDb(sql)
            if _ != 0:
                sql = 'insert into invitation_code (code, creator_id, status, create_time, expire_time) values("{}","{}","{}","{}","{}")'.format(code, inviter, status, create_time, expire_time)
                self.DBHandle.insertDB(sql)
                print("邀请码申请成功，{}".format(code))    
            else:
                print("用户不存在，无法申请邀请码")
        except:
            print("邀请码申请失败，请重试！")
        return code
    
    def check_code(self, invitation_code):
        ''' 检查邀请码是否合法  
            STEP1：检查邀请码状态 有效/失效
            STEP2：将有效状态码更新为失效
        '''

        sql = 'select * from invitation_code where code = "{}" and status = "1"'.format(invitation_code)
        _, data = self.DBHandle.selectDb(sql)

        # 方案一：使用立即失效
        # if _ > 0:
        #     expire_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     sql = 'update invitation_code set status = "{}",  expire_time = "{}" where code = "{}"'.format(2, expire_time, invitation_code)
        #     self.DBHandle.updateDb(sql)
        # return _

        # 方案二：申请时设置有效期
        return str(data[0]["expire_time"]) > datetime.now().strftime('%Y-%m-%d %H:%M:%S')