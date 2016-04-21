Title: Pelican初体验
Date: 2016-04-20 20:40
Modified: 2016-04-20 20:40
Category: 杂文
Tags: Pelican, Python, 博客, 2016
Slug: use-pelican-note
Authors: 龙井
Summary: Pelican是基于Python的静态页面生成工具，结合Github Page用来搭建个人的技术博客很棒，这篇文章记录了我开始使用Pelican的过程和配置


## 1. 介绍
Pelican是基于Python的静态页面生成工具，支持博客（Markdown、reStructuredText）、评论、主题、语法高亮等等。Pelican是法国工程师写的，Pelican也是法语中notebook的音译。

#### Github地址

[https://github.com/getpelican/pelican](https://github.com/getpelican/pelican)

#### 官方文档

[http://docs.getpelican.com](http://docs.getpelican.com/)

#### 架构
##### 架构示意图
![图片](/images/essay/use-pelican-note/overall.png)
##### UML设计图
![图片](/images/essay/use-pelican-note/uml.jpg )

  
## 2. 安装
安装pelican和markdown，markdown是我选择的文档编写工具（语言），pelican还支持reStructuredText和AsciiDoc格式

	:::shell
	pip install pelican markdown

升级pelican	

	:::shell
	pip install --upgrade pelican
	
## 3. 使用

### 3.1 过程

#### 创建目录
	:::shell
	mkdir -p ~/projects/yoursite
	cd ~/projects/yoursite
		yourproject/
		├── content
		│   └── (pages)
		├── output
		├── develop_server.sh
		├── fabfile.py
		├── Makefile
		├── pelicanconf.py       # Main settings file
		└── publishconf.py       # Settings to use when ready to publish
		
#### 快速创建博客站点
	:::shell
	pelican-quickstart

#### 创建博客文章
	
	Title: My First Review
	Date: 2010-12-03 10:20
	Category: Review
	
	Following is a review of my favorite mechanical keyboard.
#### 生成站点
	pelican content
#### 预览站点
	cd ~/projects/yoursite/output
	python -m pelican.server
	
地址：http://localhost:8000/

### 3.2 编写技巧

#### 目录结构
	content/
	├── blogs
	├── downloads
	├── images
	├── pages
	└── pdfs
		blogs
			文章目录
		downloads
			zip文件目录
		images
			图片目录，根据分类和文章可以再拆分
		pages
			about.MD页面路径
			存储不常变化的内容
		pdfs
			pdf文件目录
#### 文章配置
	Title: 凤凰项目
	Date: 2016-04-23 19:40
	Modified: 2016-04-24 19:40
	Category: 读书笔记
	Tags: DevOps, 读书笔记, 凤凰项目,专业书籍, 2016
	Slug: phoenix-project-2016-04-23 #在url中显示的地址
	Authors: 龙井  #多位作者逗号分隔
	Summary: 简介  #会作为简介显示在首页中
#### 图片
	
	![图片](/images/booknotes/cross-boundary/cross-boudary-cover.jpg)
#### 链接
	文件
		[下载文件](/downloads/archive.zip)
	URL
		[打开网页](http://192.168.33.15:8000/)
#### 语法高亮
	不显示行
		:::python
		print("The triple-colon syntax will *not* show line numbers.")
			
	显示行
		#!python
		print("The path-less shebang syntax *will* show line numbers.")
			
	注意：代码块一定要缩进
#### 自定义404页面
#### 注意
	Pelican中文章按照时间排序

### 3.2 发布

### Github Page

[Github Page](https://pages.github.com/)是Github为用户免费提供的静态站点托管平台，只要在Github中创建仓库“username.github.io”，则会在地址http://username.github.io中显示仓库的内容。

#### 手动更新
1. 创建仓库

	git@github.com:ijyun/ijyun.github.com.git

2. 推送内容

	将output的内容推送到仓库中

3. 访问地址
	
	http://ijyun.github.io/

#### 自动更新
##### 创建仓库
1. 源文件仓库

	git@github.com:ijyun/longjing-blog.git

2. 生成网站仓库

	git@github.com:ijyun/ijyun.github.com.git

##### 配置Travis-CI

#### 其他方式
1. fabric
2. make

### 3.3 主题
#### 主题下载地址
[http://www.pelicanthemes.com/](http://www.pelicanthemes.com/)
#### 选用主题
1. 我选择的主题：nice-blog
2. 配置方式：THEME = "/vagrant/longjing/nice-blog"


## 配置
配置文件：pelicanconf.py

1. 配置静态文件目录 
	
	STATIC_PATHS = ['images', 'pdfs','blog', 'downloads']
	
2. 配置文章存储路径和URL显示
	
	ARTICLE_SAVE_AS = '{date:%Y/%m/%d}/{slug}.html'
	
	ARTICLE_URL = '{date:%Y/%m/%d}/{slug}.html'

3. 配置文章目录
	
	ARTICLE_PATHS = ['blogs']

4. 配置主题
	
	THEME = "/vagrant/longjing/nice-blog"

5. 摘要显示长度配置
	
	SUMMARY_MAX_LENGTH

6. pages目录下的文章是否在导航菜单中显示
	
	DISPLAY_PAGES_ON_MENU # 缺省值为True	

7. 社交网站	
	
	SOCIAL = (('github', 'https://github.com/ijyun'),)

参考文档：[https://github.com/getpelican/pelican/wiki/Tutorials](https://github.com/getpelican/pelican/wiki/Tutorials)

## 附：
Continue reading the other documentation sections for more detail, and check out the Pelican wiki’s [Tutorials](https://github.com/getpelican/pelican/wiki/Tutorials) page for links to community-published tutorials.


