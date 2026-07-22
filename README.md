# BedwarsStat
一个简易的Hypixel Bedwars数据查询脚本，旨在让Android用户快速查询对局内各玩家的床战数据。/A simple Hypixel Bedwars data query script, designed to enable Android users to quickly obtain the battle data of each player in the game.

# 准备工作
该脚本需要运行在[Termux](https://github.com/termux/termux-app)上，用到的第三方库有requests和pexpect。
如果您是首次使用Termux，您需要分别输入pkg install android-tools, pkg install python, pip install requests, pip install pexpect 以完成所有库的安装


# Hypixel API Key
该脚本的数据源为Hypixel官方提供的公共API，API KEY获取教程详见[Hypixel Public API](https://api.hypixel.net/)。

# Urchin API Key
一个Hypixel的黑客黑名单查询API，获取教程详见https://discord.gg/urchin

# 日志自动读取
该脚本可以通过日志自动读取Hypixel服务器内的/who指令以实现自动查询
- 预设的[PojavLauncher](https://github.com/PojavLauncherTeam/PojavLauncher)启动器的读取路径为/storage/emulated/0/Android/data/net.kdt.pojavlaunch.debug/files/latestlog.txt
- 预设的[ZalithLauncher](https://github.com/ZalithLauncher/ZalithLauncher)启动器的读取路径为/storage/emulated/0/Android/data/com.movtery.zalithlauncher/files/latestlog.txt
- 支持自定义日志路径
- 由于Android11+的data文件夹访问限制，该脚本内置了无线调试的配对，以adb shell cat的方式读取日志，如果您的运行环境为Android11+且日志文件在/storage/emulated/0/Android/data中，需要进行无线调试的配对以正常读取日志


# 手动输入ID
 可实现多玩家同时查询，输入格式为：
> 玩家1, 玩家2, 玩家3, ..., 玩家n
