## 复旦咖啡项目

复旦咖啡馆微信项目，基于flask实现

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

```
python manager.py
```
