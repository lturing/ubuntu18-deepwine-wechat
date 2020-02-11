## ubuntu 18 利用deepin-wine安装微信
* 参照模板，根据url前缀下载相应的deb
```
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine/deepin-wine_2.18-20_all.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine/deepin-wine32_2.18-20_i386.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine/deepin-wine32-preloader_2.18-20_i386.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine/deepin-fonts-wine_2.18-20_all.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine/deepin-libwine_2.18-20_i386.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine/deepin-libwine-dbg_2.18-20_i386.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine/deepin-libwine-dev_2.18-20_i386.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine/deepin-wine-binfmt_2.18-20_all.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine-helper/deepin-wine-helper_1.2deepin8_i386.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine-plugin/deepin-wine-plugin_1.0deepin2_amd64.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine-plugin/deepin-wine-plugin_1.0deepin2_i386.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine-plugin-virtual/deepin-wine-plugin-virtual_1.0deepin3_all.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/d/deepin-wine-uninstaller/deepin-wine-uninstaller_0.1deepin2_i386.deb
wget http://mirrors.aliyun.com/deepin/pool/non-free/u/udis86/udis86_1.72-2_i386.deb
wget https://mirrors.aliyun.com/deepin/pool/main/libj/libjpeg-turbo/libjpeg62-turbo_1.5.1-2_amd64.deb
wget https://mirrors.aliyun.com/deepin/pool/main/libj/libjpeg-turbo/libjpeg62-turbo_1.5.1-2_i386.deb
```

*  安装 deepin-wine和微信
```
git clone  https://github.com/lturing/ubuntu18-deepwine-wechat.git
cd ubuntu18-deepwine-wechat
sudo chmod a+x ./install-deepin-wine.sh
sudo bash ./install-deepin-wine.sh
sudo dpkg -i --force-overwrite deepin.com.wechat_2.6.2.31deepin0_i386.deb
# 卸载微信
sudo apt remove deepin.com.wechat
sudo dpkg -P deepin.com.wechat
sudo dpkg --configure -a
```

* 解决微信中文乱码
```
将 /opt/deepinwine/apps/Deepin-WeChat/run.sh中的export LANG="UTF-8" 改为 export LANG="zh_CN.UTF-8"
将 /opt/deepinwine/tools/run.sh 中的WINE_CMD="LC_ALL=zh_CN.UTF-8 deepin-wine"   
cp msyh.ttc ~/.deepinwine/Deepin-WeChat/drive_c/windows/Fonts
gedit ~/.deepinwine/Deepin-WeChat/system.reg
更改以下两行为
"MS Shell Dlg"="msyh"
"MS Shell Dlg 2"="msyh"

cd ~/.deepinwine/Deepin-WeChat
gedit msyh_config.reg
重写为：
REGEDIT4
[HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\FontLink\SystemLink]
"Lucida Sans Unicode"="msyh.ttc"
"Microsoft Sans Serif"="msyh.ttc"
"MS Sans Serif"="msyh.ttc"
"Tahoma"="msyh.ttc"
"Tahoma Bold"="msyhbd.ttc"
"msyh"="msyh.ttc"
"Arial"="msyh.ttc"
"Arial Black"="msyh.ttc"

deepin-wine regedit msyh_config.reg


```


* 解决微信无法发图片
```
sudo apt install libjpeg62:i386
```

* 删除微信小黑框以及ChatContactMenu窗口
```bash
sudo apt install xdotool
```

创建/opt/deepinwine/apps/Deepin-WeChat/runrun.sh
```bash
sudo vim /opt/deepinwine/apps/Deepin-WeChat/runrun.sh

#!/bin/bash

"/opt/deepinwine/apps/Deepin-WeChat/run.sh">/dev/null 2>&1

start_succ=false

for i in {1..5}
do
	xdotool search --onlyvisible --classname "wechat.exe"
	if [ $? == 0 ]
	then
		start_succ=true
		break
	fi
	sleep 1
done

if [ $start_succ == false ]
then
	exit 1
fi

windowclose=false

while :
do
	retval=$(xdotool search --onlyvisible --classname "wechat.exe")
	
	if [ $? != 0 ]
	then
		exit 0
	fi
	
	login=true
	
	for id in $retval
	do
		windowname=$(xdotool getwindowname $id)
		if [ "$windowname" == "Log In" ] || [ "$windowname" == "登录" ]
		then
			login=false
		fi
		
		if [ $windowclose == true ] && ([ "$windowname" == "" ] || [ "$windowname" == "ChatContactMenu" ])
		then
			xdotool windowclose $id
		fi
	done
	
	if [ $windowclose == true ]
	then
		exit 0
	fi
	
	if [ $login == true ]
	then
		windowclose=true
	fi
	
	sleep 0.1
done
```
```bash
sudo chmod +x /opt/deepinwine/apps/Deepin-WeChat/runrun.sh
```
修改desktop文件
```bash 
sudo vim /usr/share/applications/deepin.com.wechat.desktop
找到Exec那一行，替换为

Exec="/opt/deepinwine/apps/Deepin-WeChat/runrun.sh"
```

* 安装托盘(消息来了，闪烁提醒)
```bash
sudo apt install gnome-shell-extension-top-icons-plus
#/usr/share/gnome-shell/extensions
```


* ubuntu 部分中文跟简体中文有区别(ubuntu 18)
```
sudo vim /etc/fonts/conf.d/64-language-selector-prefer.conf 
修改成以下：
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
        <alias>
                <family>sans-serif</family>
                <prefer>
                        <family>Noto Sans CJK SC</family>
                        <family>Noto Sans CJK TC</family>
                        <family>Noto Sans CJK HK</family>
                        <family>Noto Sans CJK KR</family>
                        <family>Noto Sans CJK JP</family>
                </prefer>
        </alias>
        <alias>
                <family>serif</family>
                <prefer>
                        <family>Noto Serif CJK SC</family>
                        <family>Noto Serif CJK TC</family>
                        <family>Noto Serif CJK KR</family>
                        <family>Noto Serif CJK JP</family>
                </prefer>
        </alias>
        <alias>
                <family>monospace</family>
                <prefer>
                        <family>Noto Sans Mono CJK SC</family>
                        <family>Noto Sans Mono CJK TC</family>
                        <family>Noto Sans Mono CJK HK</family>
                        <family>Noto Sans Mono CJK KR</family>
                        <family>Noto Sans Mono CJK JP</family>
                </prefer>
        </alias>
</fontconfig>

```
> 以上 <family>Noto Sans Mono CJK **</family>中的SC、TC、HK、KR、JP为文字的搜索顺序(sc, simplied chinese)

* ubuntu 安装微软雅黑、mac下的Monaco字体
```
sudo mkdir /usr/share/fonts/micro-yahei 
cd ./msyh.ttc  /usr/share/fonts/micro-yahei 
cd /usr/share/fonts/micro-yahei  
sudo chmod 744 *
sudo mkfontscale
sudo mkfontdir

sudo mkdir /usr/share/fonts/monaco 
cp ./monaco.ttf /usr/share/fonts/monaco 
cd /usr/share/fonts/monaco 
sudo chmod 744 *
sudo mkfontscale
sudo mkfontdir

sudo fc-cache -fv

```

