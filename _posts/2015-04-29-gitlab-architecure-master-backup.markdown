---
layout: post
title:  "Gitlab主-从集群搭建方案"
date:   2015-04-29 14:28:06
categories: gitlab architectue
---

##背景

###1.为什么要做高可用
1. 降低故障的影响，提高应用的可靠性和数据安全性，最大化服务在线时间
2. 保障性能（目前影响较小，主要性能瓶颈在IO）
3. 奠定基于Gitlab的服务交付平台的基础



###2.故障来源
1. Gitlab应用程序问题，如Nginx宕机等
2. 数据损坏，如数据库文件损坏，仓库文件损坏或丢失等
3. 服务器故障，如Gitlab服务器宕机或损坏，无法启动等
4. 基础设施平台故障，如云平台、VMWare、实体机故障，导致服务器宕机，损坏丢失等

###3.Gitlab架构图
![Alt](http://doc.gitlab.com/ce/development/gitlab_diagram_overview.png)

###4.Gitlab社区推荐的高可用方案对比

| 方案名称 | 优点 | 缺点 |
| :------------ | :------------- | :------------ |
| 点击备份与还原| 简单，成本低  | 备份时间差造成数据丢失 |
| 单机快照 | 简单，成本低，恢复时间快 <br/>要配置的内容较少  | 备份实践差造成数据丢失<br/>云平台快照机制不完善<br/>还原造成服务停止 |
|应用集群|应用可靠性高<br/>应用层性能高<br/>更新程序不停服务|文件和数据库需要单独保障可用性|
|主-从架构|应用可靠性高<br/>恢复时间短（非IPSAN）|需要主机以保障性能<br/>需要完善稳定的复制机制保障<br/>更新程序需要停止服务|
|应用集群+主-从存储|可靠性高|复杂度高，维护成本大|
|应用集群+主-主存储|可靠性高|复杂度高|

… you can [get the PDF]({{ site.url }}/assets/mydoc.pdf) directly.

###1.架构图

![架构图](https://github.com/ijyun/ijyun.github.com/blob/master/_images/gitlab_architecture/gitlab_master_backup_archet.png?raw=true)


<iframe width="640" height="360" src="http://www.youtube.com/embed/TSU1jQoGIqo" frameborder="0"> </iframe>


###2.工具箱
[Keepalived](http://www.oschina.net/p/keepalived)：主-从关系配置、监控、自动切换
###3.搭建过程
`重点：实现Gitlab应用站点的无状态,自动切换数据挂载`	
`目标：Master宕机自动切换到Backup，并挂载数据，对使用者无影响`

####1.安装Gitlab

#####0.Gitlab应用安装
采用源码安装，官方资料请[参考](http://doc.gitlab.com/ce/install/installation.html)

1. Git
2. Ruby
3. DataBae
4. Redis
5. Gitlab
	1. Gitlab-Rails
	2. Gitlab-Shell
6. Nginx

#####1.连接数据库

![Alt](https://github.com/ijyun/ijyun.github.com/blob/master/_images/gitlab_architecture/gitlab_db_config.png)

![Alt](http://172.16.50.111/download/attachments/32965578/gitlab_db_config.png)

#####2.连接Redis
![image](/Users/jingyun1/Documents/gitlab_redis_config.png)


####2.配置Gitlab
1. 配置LDAP
	官网[参考](http://doc.gitlab.com/ce/integration/ldap.html)	
	修改gitlab/config/gitlab.yml中关于LDAP的配置	
	![Alt](/Users/jingyun1/Documents/gitlab_ldap_config.png)

2. 配置邮件服务器
	1. 修改gitlab/config/gitlab.yml	
	![Alt text](/Users/jingyun1/Documents/gitlab_email_config.png)
	2. 修改gitlab/config/initializers/smtp_settings.rb	
	![Alt text](/Users/jingyun1/Documents/gitlab_email_rb_config.png)
	
	`注：注意确认telnet mail.yonyou.com 25端口是否能通`

####3.文件分离
>要做到Gitlab应用服务器的无状态，则需要将数据从服务器上剥离，包括数据库、缓存、文件，Gitlab对文件的依赖主要包括用户上传的公钥，一般存储在/home/git/.ssh/authorized_keys中；另外还有Gitlab中的附件，如用户头像等

1. authorized_keys分离		
	将authorized_keys存储到IPSAN磁盘中即可实现切换Gitlab服务器后，依然能够正常找到sshkey	
	1. 修改gitlab-shell/config	
	auth_file: "/home/git/gitlab-data/.ssh/authorized_keys"
	2. 修改服务器SSH配置	
	文件位置：/etc/ssh/sshd_config	
	修改内容：AuthorizedKeysFile      %h/gitlab-data/.ssh/authorized_keys<br/>
	`注：此配置表示通过ssh连接时都需要去当前用户的home目录下的gitlab-data下找密钥，如此修改后，会导致出git账户外的其他账户不能使用ssh免密码登录，因为原来的配置是去当前用户的.ssh目录下找，默认情况下密码都存在这个位置`
2. 附件分离		
	附件存储位置是gitlab/public/uploads，通过建立软连接，实现附件存储在IPSAN，应用程序通过gitlab/public/uploads目录访问的文件实际存储在IPSAN中	
	1. 删除public下的uploads
	2. 执行命令，在public下创建一个符号链接（软连接）：ln -s /home/git/gitlab-data/uploads uploads
	如此则等同于将public下的uploads放到了IPSAN中



###4.Keepalived配置过程

#####1.安装Keepalived
<pre>
$ wget http://www.keepalived.org/software/keepalived-1.2.2.tar.gz</a> 
$ tar -zxvf keepalived-1.2.2.tar.gz
$ cd keepalived-1.2.2
$ ./configure --prefix=/usr/local/keepalived
$ make && make install
</pre>

<pre>
$ cp /usr/local/keepalived/etc/rc.d/init.d/keepalived /etc/init.d/keepalived 
$ cp /usr/local/keepalived/sbin/keepalived /usr/sbin/
$ cp /usr/local/keepalived/etc/sysconfig/keepalived /etc/sysconfig/
$ mkdir -p /etc/keepalived/
$ cp /usr/local/etc/keepalived/keepalived.conf /etc/keepalived/keepalived.conf 
</pre>
`/etc/keepalived/keepalived.conf是默认配置文件`
#####2.配置Master节点
配置路径在/etc/keepalived下<br/>

1. keepalived.conf
	<pre>
	! Configuration File for keepalived
	global_defs {
   		notification_email {
     	jingyun1@yonyou.com
   		}
   		notification_email_from plansrv@yonyou.com
   		smtp_server 127.0.0.1
   		smtp_connect_timeout 30
   		router_id nginx_master
	}
	\#Define the script used to check if haproxy is still working
	vrrp_script chk_http_port {
	    script /etc/keepalived/check_nginx.sh # check Nginx is alive or not
	    interval 2
	    weight 2
	}
	vrrp_instance VI_1 {
	    state MASTER
	    interface eth0
	    virtual_router_id 51
	    priority 101
	    advert_int 1
	    notify /etc/keepalived/notify.sh
	    # Use the script above to check if we should fail over
	    track_script {
	      chk_http_port
	    }
	    authentication {
	        auth_type PASS
	        auth_pass 1111
	    }
	    virtual_ipaddress {
	       172.16.51.70
	    }
	}
</pre>

	`注意点：1.state需要设置为master;2.virtual_ipaddress需要配置为公共IP;3.chk_http_port表示每2s检查一次nginx是否正常，并执行配置好的脚本；4.notify表示监控keepalived集群中的状态`

2. check_nginx.sh
	<pre>
	\#!/bin/bash
	\# try to start nginx if nginx process is dead
	\# shutdonw keepalived process if start nginx failed 
	pid=`ps -C nginx --no-header |wc -l`
	if [ $pid -eq 0 ];then
    	echo $pid
    	service nginx start
    	sleep 3
    	if [ `ps -C nginx --no-header |wc -l` -eq 0 ];then
        	service keepalived stop
        	umount /home/git/gitlab-data
    	fi
	fi
	</pre>
	`检查nginx进程是否存储，不存在则关闭keepalived并且umount ipsan`
3. notify.sh
	<pre>
\#!/bin/bash
TYPE=$1
NAME=$2
STATE=$3
case $STATE in
        "MASTER")
                exit 0
                ;;
        "BACKUP")
                echo $(date +%Y-%m-%d" "%H:%M:%S) $"master is started,backup is stoping" >>/var/log/keepalived/keepalived_$(date +%Y_%m)
                #umount /home/git/gitlab-data
                mount /dev/mapper/mpath0-part1 /home/git/gitlab-data
                exit 0
                ;;
        *)
                echo 'unknown state'   >>/var/log/keepalived/keepalived_$(date +%Y_%m)
                exit 1
                ;;
esac    

</pre>
#####3.配置Backup节点

1. keepalived.conf
	<pre>
	! Configuration File for keepalived
	global_defs {
   		notification_email {
     	jingyun1@yonyou.com
   		}
   		notification_email_from plansrv@yonyou.com
   		smtp_server 127.0.0.1
   		smtp_connect_timeout 30
   		router_id nginx_master
	}
	\#Define the script used to check if haproxy is still working
	vrrp_script chk_http_port {
	    script /etc/keepalived/check_nginx.sh # check Nginx is alive or not
	    interval 2
	    weight 2
	}
	vrrp_instance VI_1 {
	    state BACKUP
	    interface eth0
	    virtual_router_id 51
	    priority 101
	    advert_int 1
	    notify /etc/keepalived/notify.sh
	    # Use the script above to check if we should fail over
	    track_script {
	      chk_http_port
	    }
	    authentication {
	        auth_type PASS
	        auth_pass 1111
	    }
	    virtual_ipaddress {
	       172.16.51.70
	    }
	}
</pre>

	`注意点：1.state需要设置为master;2.virtual_ipaddress需要配置为公共IP;3.chk_http_port表示每2s检查一次nginx是否正常，并执行配置好的脚本；4.notify表示监控keepalived集群中的状态`

2. check_nginx.sh
	<pre>
	\#!/bin/bash
	\# try to start nginx if nginx process is dead
	\# shutdonw keepalived process if start nginx failed 
	pid=`ps -C nginx --no-header |wc -l`
	if [ $pid -eq 0 ];then
    	echo $pid
    	service nginx start
    	sleep 3
    	if [ `ps -C nginx --no-header |wc -l` -eq 0 ];then
        	service keepalived stop
        	umount /home/git/gitlab-data
    	fi
	fi
	</pre>
	`检查nginx进程是否存储，不存在则关闭keepalived并且umount ipsan`
3. notify.sh
	<pre>
\#!/bin/bash
TYPE=$1
NAME=$2
STATE=$3
case $STATE in
        "MASTER")
                echo $(date +%Y-%m-%d" "%H:%M:%S) $"master is stopped,backup is starting" >>/var/log/keepalived/keepalived_$(date +%Y_%m)
                mount /dev/mapper/mpath0-part1 /home/git/gitlab-data
                exit 0
                ;;
        "BACKUP")
                echo $(date +%Y-%m-%d" "%H:%M:%S) $"master is started,backup is stoping" >>/var/log/keepalived/keepalived_$(date +%Y_%m)
                umount /home/git/gitlab-data
                exit 0
                ;;
        *)
                echo 'unknown state'    
                exit 1
                ;;
esac 
</pre>
`BACKUP监控到MASTER出现故障则mount IPSAN`
Keepalived配置的[参考资料](http://weizhifeng.net/using-keepalived.html)
###5.问题记录
1. LDAP的用户在IPSAN中的目录不能修改，权限列表出现问号，导致域登录的用户不能使用	
![Alt text](/Users/jingyun1/Documents/gitlab_ldap_badname.png)
> 修复记录：在服务器上执行命令fsck /dev/mapper/mpath0-part1，即对ipsan所在目录进行文件系统检查，发现lost+found目录重新被创建出来，目录显示正常了.
> <pre>
> fsck（file system check）用来检查和维护不一致的文件系统。若系统掉电或磁盘发生问题，可利用fsck命令对文件系统进行检查,可以使用fsck命令修复损坏的分区
> lost+found存放fsck恢复的一些文件，这些文件已经无法被直接访问，但是被某些进程占用着，概目录属于文件系统修复中产生的,恢复该目录的命令：mklost+found
> </pre>
2. Gitlab安装完成后Nginx无法启动，提示端口已被占用
修改/etc/nginx/sites-available/gitlab文件	
	<pre>## Normal HTTP host
server {
  listen 0.0.0.0:80 default_server;
  listen [::]:80 ipv6only=on default_server;
  server_name YOUR_SERVER_FQDN; ## Replace this with something like gitlab.example.com
  server_tokens off; ## Don't show the nginx version number, a security best practice
  root /home/git/gitlab/public;</pre>
[参考](http://stackoverflow.com/questions/14972792/nginx-nginx-emerg-bind-to-80-failed-98-address-already-in-use)	
3. 将sshkey存储到IPSAN中遇到的问题
	权限问题，通过挂载IPSAN生成的目录gitlab-data,的权限是lrwxrwxrwx,权限过大，需要调整为drwxr-xr-x，即chmod 755，目录的owner也需要修改为git，命令：chown git:git gitlab-data	


