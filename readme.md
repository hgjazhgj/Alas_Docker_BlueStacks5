# 优雅地在Windows上使用运行在Docker中的Alas连接到BlueStacks5模拟器

Alas是[AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript)  
只有看一眼标题就知道本项目意义的人才可能有使用本项目的需求,所以没有任何释义  

# setup

**你蓝叠5HyperV不是喜欢变端口吗,劳资给你固定下来**  
在powershell中`echo $profile`查看启动脚本位置,然后把下面的内容追加进去  

``` PowerShell
function alas {
    netsh interface portproxy delete v4tov4 55555
    netsh interface portproxy add v4tov4 55555 127.0.0.1 (python PATH_TO_getBs5Port.py MULTIINSTANCE_ID)
    docker start alas
    docker exec -it alas alas
}
```  

`portproxy delete`没有东西可清理时会有一条报错,忽略就行  
模拟器的adb监听与127.0.0.1:55555建立了全双工转发,因此Alas中「模拟器 Serial」填写`host.docker.internal:55555`  
按实际情况替换`PATH_TO_getBs5Port.py`和`MULTIINSTANCE_ID`,如果没有多开,就不写`MULTIINSTANCE_ID`参数  
由于我在大约半年前就完全在docker中运行Alas了,这个容器是使用以下方式手动创建的,相较于Alas官方历史提供的都具有小得多的磁盘占用,这很有可能与你的不同,你需要按需修改上述docker命令,本项目的意义在于展示一个解决方案  

``` bash
git clone git@github.com:LmeSzinc/AzurLaneAutoScript.git
docker run -it \
    --name alas \
    -v $PWD/AzurLaneAutoScript:/alas \
    -p 22267:22267 \
    python:3.7-slim bash
...install dependencies manually...
cat > /bin/alas << EOF
#!/bin/bash

cd /alas
python gui.py

EOF
```

# run

先启动模拟器,然后以管理员身份开powershell运行`alas`命令(netsh需要管理员权限)  
或者创建一个快捷方式,命令里写`powershell -Command "alas; start http://localhost:22267/"`,然后勾选「以管理员身份运行」  

p.s.事实上,我有一块带宏按键的键盘,我以设置计划任务的方式使键盘驱动以管理员身份开机自启~~不然原神不认鼠标宏~~,然后把其中一个宏按键设置为启动Windows Terminal,这样Windows Terminal就继承了键盘驱动的管理员权限,我觉得这已经是最极限最优雅的方案了,只要我愿意,我甚至可以让那个键一键启动alas...  
