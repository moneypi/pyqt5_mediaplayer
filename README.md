# pyqt5_mediaplayer
# 安装依赖
代码依赖pyqt5和opencv  
```bash
pip install PyQt5
pip install opencv-python
```
Windows下需要安装[Lavfilter解码器](https://github.com/Nevcairiel/LAVFilters/releases)  
Ubuntu下需要安装gstreamer1.0-plugins-ugly
```bash
sudo apt install gstreamer1.0-plugins-ugly -y
```
# 快捷键  
在最开始启动、或播放结束时，按空格键，打开媒体文件  
播放时，空格键切换暂停和播放  
数字0、1、2、3、4、5、6，分别对画面进行0.5倍、1倍、1.5倍、2倍、2.5倍、3倍、4倍等比例缩放  
向右键，前进10s  
向左键，后退5s  
向上键，音量上调5，最高值100  
向下键，音量下调5，最小值0  
Esc键，退出程序

# 鼠标
可以拖动进度条调整播放进度  


# 其他
功能极简  
不支持全屏，最大化等功能  
不支持鼠标拖动缩放画面  
不支持鼠标双击功能