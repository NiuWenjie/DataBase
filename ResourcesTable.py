# 资源管理需求，组织sql后传向底层sql.py
import uuid
from datetime import datetime, timedelta
from sql import MySQLBaseHandle

class UserTable():
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

    

class ResourcesTable():
    ''' 数据集管理表 '''
    def __init__(self, host, user, pwd, database):
        ''' 数据库连接 '''
        try:
            self.host, self.user, self.pwd, self.database = host, user, pwd, database
            self.DBHandle = MySQLBaseHandle(host = self.host, user = self.user, pwd = self.pwd, database = self.database)
            print("Connect success!")
        except:
            print("Connect failed!")

    def upload_dataset(self, dataset, type, format, modal, size, tag, uploader, path, file, task, model):
        ''' 上传数据集（上传数据-模型关系） '''
        sql = 'select * from datasets where dataset = "{}"'.format(dataset)
        num, data_set = self.DBHandle.selectDb(sql)
        if num == 0:
            sql = 'INSERT INTO datasets (dataset, type, format, modal, size, tag, uploader, path, file) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(dataset, type, format, modal, size, tag, uploader, path, file)
            tt = self.DBHandle.insertDB(sql)
            print("数据集上传成功！") if tt else print("数据集上传失败！")

            # 插入数据-模型关系
            if len(model)!=0:
                sql = 'select * from datasets where dataset = "{}"'.format(dataset)
                num, data_set = self.DBHandle.selectDb(sql)
                dataset_id = data_set[num-1]["id"]
                for m in model:
                    sql = 'select * from models where model = "{}"'.format(m)
                    num, model_set = self.DBHandle.selectDb(sql)
                    model_id = model_set[num-1]["id"]

                    sql = 'INSERT into data_model_relation (dataset_id, model_id) VALUES ("{}","{}")'.format(dataset_id, model_id)
                    tt = self.DBHandle.insertDB(sql)
                    print("{}-{}关系添加成功！".format(data_set[num-1]["dataset"], model_set[num-1]["model"])) if tt else print("{}-{}关系添加失败！".format(data_set[num-1]["dataset"], model_set[num-1]["model"]))

            else:
                print("无关系需要添加！")
 
        else:
            print("请勿重复命名！")

            
    def edit_dataset(self, dataset, rename, type, format, modal, size, tag, uploader, path, file, task, model):
        ''' 编辑数据集信息 '''
        ''' 需要更新数据集、模型关系 '''

        # 判断修改的是否为model：如果是model，更新数据-模型关系；如果不是model，直接更新数据集信息
        sql = 'select * from datasets where dataset = "{}"'.format(dataset)
        num, data_set = self.DBHandle.selectDb(sql)
        dataset_id = data_set[num-1]["id"]

        # 通过关系表，找出数据集适用的模型
        model_ori = []
        if model == model_ori:
            sql = 'update datasets set dataset = "{}", type = "{}", format = "{}", modal = "{}", size = "{}", tag = "{}", uploader = "{}", path = "{}", file = "{}" where dataset = "{}"'.format(rename, type, format, modal, size, tag, uploader, path, file, dataset)
            self.DBHandle.updateDb(sql)
        else:
            for m in model:
                if m in model_ori:
                    model_ori.remove(m)
                else:
                    sql = 'select * from models where model = "{}"'.format(m)
                    num, model_set = self.DBHandle.selectDb(sql)
                    model_id = model_set[num-1]["id"]

                    sql = 'INSERT into data_model_relation (dataset_id, model_id) VALUES ("{}","{}")'.format(dataset_id, model_id)
                    tt = self.DBHandle.insertDB(sql)
                    print("{}-{}关系添加成功！".format(data_set[num-1]["dataset"], model_set[num-1]["model"])) if tt else print("{}-{}关系添加失败！".format(data_set[num-1]["dataset"], model_set[num-1]["model"]))
            
            if model_ori != []:
                for m in model_ori:
                    sql = 'select * from models where model = "{}"'.format(m)
                    num, model_set = self.DBHandle.selectDb(sql)
                    model_id = model_set[num-1]["id"]

                    sql = 'delete from data_model_relation where dataset_id = "{} and model_id = {}"'.format(dataset_id, model_id)
                    self.DBHandle.deleteDB(sql)
                    model_ori.remove(m)

    def show_datasets(self, start, pageSize):
        ''' 展示数据集详情 '''
        sql = "select * from datasets limit {} offset {}".format(pageSize, start)
        num, data_set = self.DBHandle.selectDb(sql)
        return num, data_set

    def delete_dataset(self, dataset):
        ''' 删除数据集 '''
        sql = 'select * from datasets where dataset = "{}"'.format(dataset)
        _, data_set = self.DBHandle.selectDb(sql)
        if _ != 0:
            sql = 'delete from datasets where dataset = "{}"'.format(dataset)
            _ = self.DBHandle.deleteDB(sql)
            print("数据集已删除！")
        else:
            print("数据集不存在，请核实！")

    def upload_model(self, model, type, format, modal, size, task, net, tag, uploader, path):
        ''' 上传模型 '''
        sql = 'select * from models where model = "{}"'.format(model)
        num, model_set = self.DBHandle.selectDb(sql)
        if num == 0:
            sql = 'INSERT INTO models (model, type, format, modal, size, task, net, tag, uploader, path) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(model, type, format, modal, size, task, net, tag, uploader, path)
            tt = self.DBHandle.insertDB(sql)
            print("模型上传成功！") if tt else print("模型名上传失败！")
        else:
            print("请勿重复命名！")

    def edit_model(self, model, rename, type, format, modal, size, task, net, tag, uploader, path):
        ''' 编辑模型信息 '''
        sql = 'update models set model = "{}", type = "{}", format = "{}", modal = "{}", size = "{}", task = "{}", net = "{}", tag = "{}", uploader = "{}", path = "{}" where model = "{}"'.format(rename, type, format, modal, size, task, net, tag, uploader, path, model)
        self.DBHandle.updateDb(sql) 
    
    def show_models(self, start, pageSize):
        ''' 展示模型详情 '''
        sql = "select * from models limit {} offset {}".format(pageSize, start)
        num, model_set = self.DBHandle.selectDb(sql)
        return num, model_set

    def delete_model(self, model):
        ''' 删除模型 '''
        sql = 'select * from models where model = "{}"'.format(model)
        _, data_set = self.DBHandle.selectDb(sql)
        if _ != 0:
            sql = 'delete from models where model = "{}"'.format(model)
            _ = self.DBHandle.deleteDB(sql)
            print("模型已删除！")
        else:
            print("模型不存在，请核实！")

    def __del__(self):
        self.DBHandle.closeDb()

class AlgorithsTable():
    def __init__(self) -> None:
        pass

class ResultsTable():
    def __init__(self) -> None:
        pass