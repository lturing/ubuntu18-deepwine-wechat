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
