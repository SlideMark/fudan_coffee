## 复旦咖啡项目

复旦咖啡馆微信项目，基于flask实现。采用js+restapi实现。

api文档在[这里](doc/api.md)。

### 功能

* 手机号注册/登录
* 查看商品
* 直接购买
* 加入购物车购买
* 充值
* 查看消费记录
* 微信登录
* 微信充值（TODO）
* 微信支付（TODO）

### 安装

* 参考[安装指南](doc/install.md)安装postgres，python，virtualenv等组件
* 安装pip软件包

```
pip install -r doc/requirements.txt
```

### 初始化

```
# 初始化数据库
python script/migration.py
```

### 运行

* 配置~/.fudan_coffee.yaml配置文件，可以参考[配置例子](doc/fudan_coffee.yaml.sample)

```
python manager.py
```

### 部署

* 部署采用capistrano+supervisor部署

```
cap production deploy
```
