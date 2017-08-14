# 编程环境准备

编辑用户目录下pip/pip.conf
```
[global]
timeout = 6000
index-url = https://mirrors.aliyun.com/pypi/simple/
```

VSCode“自动格式化代码”的快捷键是“Alt+Shift+F”。要格式化Python代码，需要安装Python包yapf（或autopep8、等）

`pip install yapf`

VSCode使用python的语言分析(写python代码的时候，编辑器会提示哪里出错，哪里的代码格式不规范)，可以安装flake8（或pylint、等）

`pip install flake8`

"文件"->"首选项"->"设置"添加如下配置
```
"python.linting.flake8Enabled": true
"python.formatting.provider": "yapf"
```