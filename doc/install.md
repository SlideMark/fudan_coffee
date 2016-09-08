## 服务器安装指南

### 前期准备

* 阿里云购买服务器
* 系统选择centos6.5
* 填写hostname

### 机器配置

#### 创建新用户

```bash
ssh root@xxx.xxx.xxx.xx(ip)

useradd deploy
```

#### 修改hostname

```bash
vim /etc/sysconfig/network
```

* 修改配置例子

```bash
NETWORKING=yes
HOSTNAME=peiwo-test3
NETWORKING_IPV6=no
PEERNTP=no
GATEWAY=120.24.243.247(这里不用修改)
```

* 不重启修改hostname

```bash
hostname peiwo-test3
```

* 从git拉取安装所需软件(包含python环境，turnserver以及postgres)

```bash
git clone git@code.peiwoapi.com:dev_all/open_software.git
#需要在code.peiwoapi.com上的个人账户中加入peiwo-test3服务器生成的id_rsa.pub文件
```
### python以及虚拟环境的安装

#### 1。安装python2.7.8

```bash
yum groupinstall "Development tools"
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel python-devel
```

```bash
tar xf Python-2.7.8.tar.xz
cd Python-2.7.8
./configure --enable-shared --prefix=/usr/local --enable-unicode=ucs4

make && make altinstall #su
```

* 安装pip2.7

```bash
python2.7 ez_setup.py
easy_install-2.7 pip
```

* 安装virtualenv虚拟环境

```bash
pip2.7 install virtualenv

# 在home/deploy/下新建fudan_coffee目录，将虚拟环境安装到fudan_coffee下
su deploy
cd ~
mkdir fudan_coffee
cd peiwo
virtualenv env
```

#### 安装postgres9.3（如果原来有postgres低于9.3的版本，请先卸载）

* 卸载旧版本postgres

```bash
# 如果存在低版本的postgres，请卸载
# 确认postgres的安装包
rpm -qa | grep postgres

# 例如
postgresql-libs-8.4.18-1.el6_4.x86_64
postgresql-8.4.18-1.el6_4.x86_64
postgresql-devel-8.4.18-1.el6_4.x86_64

# 卸载安装包
rpm -e postgresql-libs-8.4.18-1.el6_4.x86_64 postgresql-8.4.18-1.el6_4.x86_64 postgresql-devel-8.4.18-1.el6_4.x86_64
```

* 安装postgres

```bash
rpm -ihv postgresql93-*

# 修改postgres用户密码
passwd postgres

# 修改配置
echo 'export PATH=$PATH:/usr/pgsql-9.3/bin' >> /var/lib/pgsql/.bash_profile #su

# 将postgres的可执行加到环境变量之中
echo 'export PATH=$PATH:/usr/pgsql-9.3/bin' >> /home/deploy/.bash_profile #su

# 用postgres用户运行
su - postgres
-bash-4.1$ initdb --encoding=UTF8 --no-locale --auth=ident
```

* 修改安全配置，修改/var/lib/pgsql/9.3/data/pg\_hba.conf

```
# "local" is for Unix domain socket connections only
local   all             all                                     trust
# # # IPv4 local connections:
host    all         all         127.0.0.1/32          md5
host    all         all         0.0.0.0/0          md5
# #   # # IPv6 local connections:
host    all         all         ::1/128               md5
host    fudan_coffee         fudan_coffee         115.28.7.144/32               md5
host    fudan_coffee         fudan_coffee         115.28.47.66/32               md5
```

```
# 启动postgres
su postgres
pg_ctl -D /var/lib/pgsql/9.3/data start

```



* 启动postgres

```bash
pg_ctl -D /var/lib/pgsql/9.3/data/ start
```

#### 配置数据库

* postgres用户进入

```bash
psql -U postgres postgres
```

* 创建角色和数据库

```sql
create user fudan_coffee with password '*******'
create database fudan_coffee with owner fudan_coffee

# 导入数据库的schema，导入用户表
```