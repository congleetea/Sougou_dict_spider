# 搜狗词库爬虫(sougou_dict_spider)
[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org)

> 把人类从重复的劳动中解放出来，去创造新的事物。


## 简介(Introduction)

搜狗输入法的词库可能是目前比较容易获取的开放下载的中文词库了，其中涵盖的内容也是非常的广泛。
包含如下12个大类：

**城市信息，  自然科学，  社会科学，  工程应用，  农林渔畜，  医学医药，  电子游戏，  艺术设计，  生活百科，  运动休闲，  人文科学，  娱乐休闲**

在这个大类之中还由非常多的小类。如果要去一一手动下载，将花费非常多的时间。

所以这个项目诞生了😋!

## 分析


[Python 搜狗词库的批量下载分析](https://www.quanquanting.com/blog/article/?id=13465787 "Python 搜狗词库的批量下载分析")


## 快速开始(Quick start)

#### 环境要求(Requirements):

* Python 3.x (2.x is not supported)
* requests
* bs4

#### 操作步骤(Steps):

1. Git本项目到您的电脑上，或是直接Fork到您自己的仓库

        git clone https://github.com/StuPeter/Sougou_dict_spider.git

2. 目录结构如下：

        .
        ├── main.py
        ├── SougouSpider.py
        ├── Scel2Txt.py
        ├── requirements.txt
        └── Readme.md

    + main.py为主程序，用于下载搜狗词库；
    + SougouSpider.py为解析和下载的类，供main.py调用；
    + Scel2Txt.py为.scel文件转.txt程序；

3. 要下载搜狗词库文件，需要先打开 main.py

        # 下载类别
        Categories = ['城市信息:167', '自然科学:1', '社会科学:76', '工程应用:96', '农林渔畜:127', '医学医药:132',
              '电子游戏:436', '艺术设计:154', '生活百科:389', '运动休闲:367', '人文科学:31', '娱乐休闲:403']
        # Scel保存路径
        SavePath = r"f:\Users\Documents\zTemp Files\scel1"
        
        # TXT保存路径
        txtSavePath = r"f:\Users\QQT\Documents\zTemp Files\txt"
        
        # 开始链接
        startUrl = "https://pinyin.sogou.com/dict/cate/index/436"

    + 下载类别：为12个大类，默认就是全下载；如果要选择性下载，就请删掉您不要的类目。请保证每个类目名称冒号后的Id不被删除，否则无法下载哦！
    + Scel保存路径：这个自己指定,下载的默认都是.scel文件无法直接使用；
    + TXT保存路径：这个自己指定；
    + 开始链接：这个建议默认；

4. 如上设置设置完毕后，直接运行main.py即可。ps:由于是单线程下载，可能需要较长时间。

5. 当显示“任务结束...”表示下载和转化完毕，最后的词库文件路径为上面设置的 **txtSavePath**

## 合并txt文件

生成的txt文件是分类存放，需要将它合并成一个文件进行词库转换，可以运行Mergetxt.py文件。

```
# 指定文件夹路径和输出文件路径
folder_path = 'path/to/file.txt'  # 替换为你的文件夹路径
output_file = 'path/to/output.txt'  # 替换为你的输出文件路径
```

* 注意修改输入输出文件路径
* 当任务结束，会输出`Concatenation completed.`


## 使用fcitx5批量导入搜狗词库

新增的`transfer_to_dict.py`脚本实现了批量将.scel文件转换为fcitx5拼音输入法可用的.dict格式的功能，集成了文件收集（find）和转换步骤。

### 安装依赖
需要安装 `fcitx5-chinese-addons` 包提供 `scel2org5` 命令和 `libime` 包提供 `libime_pinyindict` 命令：
```bash
# Ubuntu/Debian
sudo apt install fcitx5-chinese-addons libime-bin

# Fedora/RHEL
sudo dnf install fcitx5-chinese-addons libime

# Arch Linux
sudo pacman -S fcitx5-chinese-addons libime
```

### 使用方法
```bash
# 基本用法（使用main.py中定义的默认路径，与教程保持一致）
python transfer_to_dict.py

# 指定源目录
python transfer_to_dict.py --source-dir /path/to/scel/files

# 指定自定义输出目录
python transfer_to_dict.py --source-dir /path/to/scel/files --dict-dir /path/to/output/dict

# 跳过收集步骤，仅执行转换（如果.scel文件已经收集好了）
python transfer_to_dict.py --no-collect --collect-target /path/to/already/collected/scel
```

参数说明：
- `--source-dir`: 搜索.scel文件的源目录（默认：/home/xuancong/sogou/ciku，与main.py中的SavePath一致）
- `--collect-target`: 收集.scel文件的目标目录（默认：scel/）
- `--txt-dir`: 中间.txt文件的目录（默认：txt/）
- `--dict-dir`: 最终.dict文件的目录（默认：dict/）
- `--exclude-patterns`: 要排除的路径模式（默认：['/436/', '/403/']，对应电子游戏和娱乐休闲类别）
- `--no-collect`: 跳过收集步骤，仅执行转换

转换完成后，将生成的.dict文件复制到 `~/.local/share/fcitx5/pinyin/dictionaries/` 目录下即可在fcitx5中使用。

### 与K4YT3X教程的对应关系
根据[K4YT3X教程](https://k4yt3x.com/post/fcitx5-pinyin-import-sougou-dict/)，此脚本实现了以下步骤：
1. 批量收集.scel文件（对应教程中的find命令步骤）
2. 使用scel2org5将.scel转为.txt格式
3. 使用libime_pinyindict将.txt转为.dict格式

## 许可(License)
[MIT license](https://github.com/StuPeter/Sougou_dict_spider/blob/master/LICENSE "MIT license")
    

