#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'龙井'
SITENAME = u'雨前龙井'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh'

# 配置主题
# 配置使用的主题名称及路径
THEME = "nice-blog"
# 配置该主题的边栏显示内容
SIDEBAR_DISPLAY = ['about', 'categories', 'tags']

SIDEBAR_ABOUT = "这里是龙井的博客，内容包括开发技术、持续集成、读书笔记、DevOps、互联网思维、精益、Linux等等"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
STATIC_PATHS = ['images', 'pdfs','blogs', 'downloads']

# 配置文章目录
ARTICLE_PATHS = ['blogs']

# 配置文章存储路径和URL显示
ARTICLE_SAVE_AS = '{date:%Y/%m/%d}/{slug}.html'
ARTICLE_URL = '{date:%Y/%m/%d}/{slug}.html'



# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/ijyun'),)

FEED_RSS = None


DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
