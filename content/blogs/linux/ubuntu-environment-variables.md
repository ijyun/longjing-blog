Title: Linux环境变量
Date: 2016-05-25 20:40
Modified: 2016-05-25 14:21
Category: Linux
Tags: Linux, Ubuntu, 环境变量,Jenkins
Slug: ubuntu-environment-variables
Authors: 龙井
Summary: Linux环境变量供了一种在系统上改变软件行为的方式，在Shell编程和Linux日常操作中应用很广泛，有一些团队在做应用部署时，所有参数配置也都采用环境变量来进行配置，和环境无依赖。





### 简介
环境变量提供了一种在系统上改变软件行为的方式，比如，环境变量“LANG”决定了软件程序和用户交互的语言类型、
环境变量以Key-Value的形式存在，比如在美国的操作系统中，我们一般设置“LANG”变量的值为“en_US.UTF-8”
这意味着环境变量以及其值得格式都有使用环境变量的应用程序决定

#### 修改环境变量和值
很多图形化系统配置工具实际上也是在后台修改环境变量，通过命令行的方式可以更方便的修改环境变量。Ubuntu上的默认命令行工具Shell包括sh、ksh和bash，命令的格式可能和其他shell有差异，比如和csh。

#### 为环境变量赋值

如果环境变量存在，则直接赋值，如：LANG=he_IL.UTF-8
如果环境变量不存在，直接赋值时，会生成一个shell变量(non-exported shell variables)，其不是环境变量，并不影响其他应用的行为。如果需要将其转换为环境变量，可以使用export命令，比如：

1. 先赋值，创建shell变量：EDITOR=nano
2. 在转换为环境变量：export EDITOR

简化的创建一个新的环境变量的方式：export EDITOR=nano


#### 查看环境变量
printenv：点引出当前所有已经定义的环境变量，比如要查看一个特定的环境变量，可以直接printenv PATH或者echo $PATH，env命令也可以用于查看环境变量


美元符加上环境变量的Key可以代表Value，比如$PATH代表具体的值。可以和其他字符串联合使用，比如ls $HOME/desktop

如果要查看所有的环境变量和Shell变量，可以使用命令：( set -o posix ; set ) | less


#### 清除环境变量

将环境变量值设为空：export LC_ALL=

彻底的清除环境变量：unset LC_ALL

将环境变量转换为Shell变量：export -n LC_ALL

### 环境变量的运行原理

#### 进程局部
环境变量的值是局部的，也就是说环境变量的值是为特定的进程服务的。如果我们打开两个终端窗口（将会有两个终端进程），当在其中一个终端窗口中修改环境变量的值时，另一个终端窗口中的环境变量是不会变化的。

#### 继承

当父进程启动一个子进程是，子进程会继承父进程的所有环境变量及其值。但是子进程修改的环境变量不会影响父进程。比如，在终端中设置LANG之后，在终端中启动gedit，gedit将会继承LANG的值。

#### 大小写敏感
推荐使用大写英文字母和_（下划线）命名

#### Bash Shell快速分配和假继承
命令：LANGUAGE=he FOO=bar gedit，子进程gedit会采用分配的环境变量值，但是其实没有修改父进程的环境变量值，其他子进程并不会受影响


### 持久化环境变量

#### 会话级环境变量
只影响特定用户的环境变量修改时，可以修改~/.pam_environment 和 ~/.profile。修改后需要重新登录才能初始化环境变量。

**~/.pam_environment **

示例：

	:::shell
	FOO=bar
	PATH DEFAULT=${PATH}:/home/@{PAM_USER}/MyPrograms

该文件并不是脚本文件

**~/.profile**

该文件在会在启动桌面会话时被DisplayManager自动执行，在通过文本控制台登录时也会被自动执行

示例：

	:::shell
	export FOO=bar
	export PATH="$PATH:$HOME/MyPrograms"

~/.profile在~/.pam_environment 之后执行


**其他文件**

~/.bashrc, ~/.bash_profile, and ~/.bash_login

#### 系统级环境变量

系统环境变量包括：/etc/environment或者/etc/profile.d目录

**/etc/environment**（系统的环境变量）

该文件不是脚本文件，只是配置了环境变量信息，默认只包含了PATH
示例：

	:::shell
	FOO=bar

**/etc/profile.d/*.sh**

在/etc/profile.d 目录下的所有sh文件会在控制台登录或者SSH登录时被执行，在桌面会话启动时DisplayManager也会去执行这些sh文件
示例：

	:::shell
	/etc/profile.d/myenvvars.sh 
	
	export JAVA_HOME=/usr/lib/jvm/jdk1.7.0
	export PATH=$PATH:$JAVA_HOME/bin

**其他文件**

**/etc/profile**（所有用户的环境变量）

常常用来作为系统级别的环境变量配置文件，/etc/profile也是根据/etc/profile.d 下的文件生成的(Files in /etc/profile.d are sourced by /etc/profile.)

**/etc/default/locale **用户设置本地化相关的环境变量

**/etc/bash.bashrc**,只对Bash shell启动的程序有效，在图形化环境中无法使用

### 对比环境变量配置文件

#### 系统级
**/etc/profile**（所有用户的环境变量）

此文件为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行。并从/etc/profile.d目录的配置文件中搜集shell的设置.

**/etc/bashrc**

为每一个运行bash shell的用户执行此文件.当bash shell被打开时,该文件被读取.

#### 用户级

**~/.profile**

每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该文件仅仅执行一次!默认情况下,他设置一些环境变量,执行用户的.bashrc文件。不同系统该文件可能不同。

**~/.bashrc**

该文件包含专用于你的bash shell的bash信息,当登录时以及每次打开新的shell时,该文件被读取.

~/.bashrc中设定的变量(局部)只能继承/etc/profile中的变量

<!-- 个人理解，系统级在用户级之前加载，而系统级中/etc/profile先于/etc/environment执行 -->

#### 总结

**/etc/environment是登录系统读取的第一个文件，是整个系统包括所有进程的环境变量，与登录用户无关。以后才是/etc/profile, .profile等等**

### 附：

#### 为什么Jenkins中的Slave系统信息中环境变量的PATH和登录后的Shell下的PATH不同（相同用户）？
Jenkins的Slave系统信息读取的环境变量信息是Slave服务器的Jenkins进程环境变量信息，位置：

系统启动后会执行/etc/environment，/etc/profile由于用户为登录，无法加载，在Jenkins进程启动时，生成/proc/processid/environ的值不包含/etc/profile定义的环境变量
通过SSH登录，Shell打开后，会再去加载所有用户的环境变量，则正常获取用户的环境变量



格式化输出进程的环境变量信息：

	:::shell		

	cat /proc/2279/environ | tr '\0' '\n'
	
	LC_CTYPE=UTF-8
	USER=vagrant
	LOGNAME=vagrant
	HOME=/home/vagrant
	PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/jdk1.8.0_91
	MAIL=/var/mail/vagrant
	SHELL=/bin/bash
	SSH_CLIENT=10.0.2.2 54629 22
	SSH_CONNECTION=10.0.2.2 54629 10.0.2.15 22
	SSH_TTY=/dev/pts/0
	TERM=xterm-256color
	XDG_SESSION_ID=6
	XDG_RUNTIME_DIR=/run/user/1000
	LANG=en_US.UTF-8




参考资料:

[https://help.ubuntu.com/community/EnvironmentVariables](https://help.ubuntu.com/community/EnvironmentVariables)

[http://www.cnblogs.com/xmkk/p/3582336.html](https://help.ubuntu.com/community/EnvironmentVariables)