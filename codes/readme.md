选择对应自己微信客户端版本的wxauto进行调用

# 如何打包py为exe
https://www.cnblogs.com/bbiu/p/13209612.html


pyinstaller -F F03Remind.py
修改spec
I:\workspace\python\wxauto\codes>pyinstaller

- 1.执行命令，xxx.py为程序入口文件
    
      pyinstall -F xxx.py 
      pyinstaller -F F03Remind.py

- 2.删除生成的bulid和dist文件夹,仅保留xxx.spec文件

  - 3.修改xxx.spec文件

- 4.执行命令

      pyinstaller -F xxx.spec
      pyinstaller -F F03Remind.spec

- 5.去dist文件夹下找xxx.exe文件

- 6.运行成功，删除临时文件目录build；dist目录为打包的结果，可执行文件和其它程序运行的关联文件都在这个目录下
