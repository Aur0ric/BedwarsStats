# BedwarsStat
一个简易的Hypixel Bedwars数据查询脚本，旨在让Android用户快速查询对局内各玩家的床战数据。/A simple Hypixel Bedwars data query script, designed to enable Android users to quickly obtain the battle data of each player in the game.

 - **Hypixel API Key**
 该脚本的数据源为Hypixel官方提供的公共API，API KEY获取教程详见[Hypixel Public API](https://api.hypixel.net/)。
 
 - **日志自动读取**
 该脚本可以通过日志自动读取Hypixel服务器内的/who指令以实现自动查询
 预设的PojavLauncher启动器的读取路径为/storage/emulated/0/Android/data/net.kdt.pojavlaunch.debug/files/latestlog.txt
 预设的ZalithLauncher启动器的读取路径为/storage/emulated/0/Android/data/com.movtery.zalithlauncher/files/latestlog.txt
（由于谷歌在Android11+引入了data文件夹加密，所以该路径的读取可能需要用到Shizuku或root权限）
同时也支持自定义日志路径


 - **手动输入ID**
 可实现多玩家同时查询，输入格式为：
> 玩家1, 玩家2, 玩家3, ..., 玩家n



该脚本实测可在Pydroid 3和Termux上完美运行。
