# 优雅地在Windows上使用运行在Docker中的Alas连接到BlueStacks5模拟器

Alas是[AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript)  
只有看一眼标题就知道本项目意义的人才可能有使用本项目的需求,所以没有任何释义  

## setup

**你蓝叠5HyperV不是喜欢变端口吗,劳资给你固定下来**  
由于[wsl2+docker的严重内存泄漏](https://github.com/microsoft/WSL/issues/8725),我在最近重建了我的alas映像,提供了我自己的Dockerfile和相关文件,~~相较于Alas官方历史提供的都具有小得多的磁盘占用,将其覆盖掉`AzurLaneAutoScript/deploy/docker/Dockerfile`然后原地照文件开头注释操作来构建映像~~x86的Dockerfile已合并入Alas中  
在powershell中`echo $profile`查看启动脚本位置,然后把类似于下面的内容追加进去  

``` PowerShell
function alas {
    netsh interface portproxy delete v4tov4 55555
    netsh interface portproxy add v4tov4 55555 127.0.0.1 (python PATH_TO_getBs5Port.py MULTIINSTANCE_ID)
    cd PATH_TO_ALAS
    docker run -v ${PWD}:/alas -p 22267:22267 --name alas -it --rm hgjazhgj/alas
    # ssh -t hgjazhgj@raspberrypi "sudo docker run -v PATH_TO_ALAS:/alas -p 22267:22267 --name alas -it --rm hgjazhgj/alas"
}
```  

此函数将模拟器的adb监听与0.0.0.0:55555建立了tcp全双工转发,因此Alas中「模拟器 Serial」填写`host.docker.internal:55555`  
$inst是模拟器多开id  
按实际情况替换`PATH_TO_getBs5Port.py`  
当Alas在另一设备上运行时,你可能需要为转发的端口设置防火墙入站规则  

## run

先启动模拟器,然后以管理员身份开powershell运行`alas`命令(netsh需要管理员权限)  
或者创建一个快捷方式,命令里写`powershell -Command "alas; start http://localhost:22267/"`,然后勾选「以管理员身份运行」  

p.s.事实上,我有一块带宏按键的键盘,我以设置计划任务的方式使键盘驱动以管理员身份开机自启~~不然原神不认鼠标宏~~,然后把其中一个宏按键设置为启动Windows Terminal,这样Windows Terminal就继承了键盘驱动的管理员权限,我觉得这已经是最极限最优雅的方案了,只要我愿意,我甚至可以让那个键一键启动alas...  
