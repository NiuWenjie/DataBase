from UserTable import UserTable

# 非root用户登录，已具备所有权限
db = UserTable(host="localhost",user='user1',pwd='123456',database="aicert_database")

# 增加用户邀请码
# code = db.generate_invitation_code('root', "2025-07-11 16:05:00")
# 用户注册
# db.register(username='test3', password='112233', mobile='00000000000', email='', invitation_code=code)

# 测试root登录
# account = "root"
# password = "zjuicsr123"

# 已过期普通用户登录
# account = "test3"
# password = "112233"
# db.login(account=account, password= password)


# 用户删除
# db.delete(username='test3')

# 更新用户邀请码失效时间
db.update(account='test3', valid_time='2026-07-11 14:45:00')

# 用户列表展示
# num, res = db.show(0, 10)

db.DBHandle.closeDb()