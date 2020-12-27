### Python 环境搭建

#### 搭建虚拟环境：

根据Python的设置，使用python或python3

```shell
python -m venv .
python3 -m venv .
``` 

#### 激活虚拟环境[注意：只有激活之后，才算进入该虚拟环境，否则安装包时，依然是安装在全局环境之下]

- 激活
```shell
activate
``` 

- 退出

```shell
deactivate
``` 

### 启动

- 前提

> 需要安装第三方模块fastapi

#### 安装方法：

1.可视化界面安装：打开Pycharm  找到设置-搜索框输入：Python interpreter，打开界面，右侧，点击加号添加即可
2.命令行安装

根据环境使用pip或pip3

```shell
pip install -r requirements.txt
pip3 install -r requirements.txt
```

3.启动

```shell
uvicorn main:app --reload
```