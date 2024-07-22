from ResourcesTable import UserTable, ResourcesTable
# 数据库连接
# db = UserTable(host="localhost",user='user1',pwd='123456',database="aicert_database")

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
# db.update(account='test3', valid_time='2026-07-11 14:45:00')

# 用户列表展示
# num, res = db.show(0, 10)

# db.DBHandle.closeDb()


# 加载 npz文件测试
import numpy as np
import os.path as osp

# 创建一个简单的numpy数组
# array = np.array([1, 2, 3, 4, 5])
# 将数组保存为二进制文件 .npz
# np.savez('./test.npz', my_array=array)

file_path = './test.npz'
with np.load(file_path) as data:
    binary_data = data["my_array"].tobytes()
    data.close()

# 文件单位转换
def convert_size(size):
    power = 2 ** 10
    n = 0
    power_labels = {0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}"

file_size = convert_size(osp.getsize(file_path))

# dataset_input_json = {
#     "dataset": "MNIST",
#     "type": "Built-in",
#     "format": "ubyte",
#     "modal": "Image",
#     "size": file_size,
#     "tag": "内置MNIST数据集",
#     "uploader": "root",
#     "path": file_path,
#     "file": binary_data,
    
#     "task": "图像分类",
#     "model":["VGG16", "VGG19"]
# }

dataset_input_json = {
    "dataset": "ImageNet",
    "type": "Built-in",
    "format": "ubyte",
    "modal": "Image",
    "size": file_size,
    "tag": "内置ImageNet数据集",
    "uploader": "root",
    "path": file_path,
    "file": binary_data,

    "task": "图像分类",
    "model":["VGG16", "VGG19"]
}

# model_input_json = {
#     "model": "VGG16",
#     "type": "Built-in",
#     "format": "pt",
#     "modal": "Image",
#     "size": file_size,
#     "task":"图像分类",
#     "net": "VGG",
#     "tag": "内置VGG16模型",
#     "uploader": "root",
#     "path": file_path
# }

model_input_json = {
    "model": "VGG19",
    "type": "Built-in",
    "format": "pt",
    "modal": "Image",
    "size": file_size,
    "task":"图像分类",
    "net": "VGG",
    "tag": "内置VGG19模型",
    "uploader": "root",
    "path": file_path
}


# 数据库连接
db = ResourcesTable(host="localhost",user='user1',pwd='123456',database="aicert_database")

# 上传数据集
# db.upload_dataset(dataset=dataset_input_json["dataset"], type=dataset_input_json["type"], format=dataset_input_json["format"], modal=dataset_input_json["modal"], size=dataset_input_json["size"], tag=dataset_input_json["tag"], uploader=dataset_input_json["uploader"], path=dataset_input_json["path"], file=dataset_input_json["file"], task=dataset_input_json["task"], model=dataset_input_json["model"])

# 删除数据集
# db.delete_dataset(dataset=dataset_input_json["dataset"])

# 展示数据集列表，含翻页
# num, res = db.show_datasets(0, 10)

# 编辑数据集（修改信息）
db.edit_dataset(rename=dataset_input_json["dataset"], dataset="test", type=dataset_input_json["type"], format=dataset_input_json["format"], modal=dataset_input_json["modal"], size=dataset_input_json["size"], tag=dataset_input_json["tag"], uploader=dataset_input_json["uploader"], path=dataset_input_json["path"], file=dataset_input_json["file"], task=dataset_input_json["task"], model=dataset_input_json["model"])

# 上传模型
# db.upload_model(model=model_input_json["model"], type=model_input_json["type"], format=model_input_json["format"], modal=model_input_json["modal"], size=model_input_json["size"], task=model_input_json["task"], net=model_input_json["net"], tag=model_input_json["tag"], uploader=model_input_json["uploader"], path=model_input_json["path"])

# 删除模型
# db.delete_model(model="test")

# 展示模型列表
# num, res = db.show_models(0, 10)

# 编辑模型（修改信息）
# db.edit_model(model=model_input_json["model"], rename= "test",type=model_input_json["type"], format=model_input_json["format"], modal=model_input_json["modal"], size=model_input_json["size"], task=model_input_json["task"], net=model_input_json["net"], tag=model_input_json["tag"], uploader=model_input_json["uploader"], path=model_input_json["path"])
