Title: Jenkins性能提升妙招
Date: 2016-09-06 10:300
Modified: 2016-09-06 10:300
Category: 持续集成
Tags: Jenkins
Slug: jenkins-performance-hints
Authors: 龙井
Summary: Jenkins CI Server的可扩展性存在很大局限性。但是对大多数应用场景，Jenkins的性能已经足够使用。可以参考文章 installations with hundreds of slaves running about 10k builds daily。虽然Jenkins配置很简单，但是也有一些方法帮助搭建和维护压力较大的Jenkins。如下有一些建议，包括Master配置、Slave配置、Job配置和一些多Master配置，可以帮助我们保持Jenkins高效运行。


Jenkins CI Server的可扩展性存在很大局限性。但是对大多数应用场景，Jenkins的性能已经足够使用。可以参考文章 installations with hundreds of slaves running about 10k builds daily。虽然Jenkins配置很简单，但是也有一些方法帮助搭建和维护压力较大的Jenkins。如下有一些建议，包括Master配置、Slave配置、Job配置和一些多Master配置，可以帮助我们保持Jenkins高效运行。

### 1. Jenkins Master Configuration

#### 插件数量
插件会导致构建（因为hook）和UI（插件会添加界面元素到UI中）加载时的性能问题，不要添加过多的插件，一定要充分评估插件后再安装。

#### Job数量
当Job数量达到1000+时，Jenkins（UI）会变慢。通过手工静态分区的方式将Job分散到多个Master上可以有效提升性能。比如，一台Master用于构建，一台Master用于测试。功能分离可以有效简化Jenkins配置并减少插件的数量。然后将一个大的Master拆分为两个类似的Master只会导致两个Master都同样复杂。

> 多台Jenkins Master插件与系统配置是否有必要保持一致，保持一致则并没有减少插件的优势，如果存在差异化，运维怎么做？

保持激活状态的Job处在合理的数量，将无用的Job删除

利用Git和Gerrit Trigger插件配置一组Job来支持多分支的情况

#### 禁止在Master上运行Job
Master上不应该运行Job，或者只能运行对Jenkins管理至关重要的内部轻量级任务（Jenkins备份、Job清理等），绝对不能运行业务Job。

> 需要形成规范，Job必须通过Restrict where this project can be run指定Slave，最好是采用标签来指定一类Slave

> 禁用Master作为Slave可以断开连接或者在系统设置中将【执行者数量】设置为0

#### 减少在Master上轮询SCM
针对Git或者Perforce的SCM轮询需要为每个Job的每次轮询运行CLI程序。如果想要可靠的轮询，则应该运行在Master上，不建议在Slave上轮询，因为Slave是不可靠的。

建议使用push hooks代替轮询，Git可以在大多情况下使用Gerrit Trigger的“Ref update”事件来代替SCM轮询，针对Perforce，可以将轮询时间间隔设置的长一些，使用“H”或者“@hourly”来配置计划任务，至于Subversion则使用的是SVNkit而不是CLI程序，所以其不受影响。

#### Build延迟加载

当JVM的minimum和maximum heap sizes不同时，WeakReferences（延迟加载时使用）会在JVM尝试扩展heap之前进行垃圾回收。这会导致Build在重新加载时产生额外的加载，某些情况下还会导致Build记录丢失。

服务器的JVM配置必须保证minimum和maximum值相同

#### 权限控制

认证用户应该允许拥有出系统管理员以外的所有权限，“相信用户都是善意的，别想要用户不会做愚蠢的事，要么阅读文档，要么有充分的单元测试”。信任可以鼓励大家，并且可以节约权限认证配置。负责的认证模型（比如： Role Strategy plugin）会导致UI和API的性能都下降。


#### 磁盘IO性能
为Job配置（启动时）和Build记录（延迟加载）使用更快的磁盘，Master采用SSD会很有帮助，分离配置、BUild记录、构件存储。可插拔的构件转移和存储会值得研究（[JENKINS-17236](https://issues.jenkins-ci.org/browse/JENKINS-17236)）。

#### 使用外部API/UI作为Jenkins前端

Jenkins并不擅长UI性能，UI插件会导致UI性能变的更糟。外部的UI面板或前端系统可以作为替代方案，引发性能问题的插件：

- Dashboard view plugin 会引发延迟加载问题
- Nested View plugin 会引发多次针对每个Job的权限重复认证问题，使用正则表达式过滤Job会变的更糟。可以尝试使用明确的Job list，而不是正则表达式。可以使用 Cloudbees Folders Plugin 代替，这个插件可能有效，但是需要评估。

#### HTTP缓存

使用快速的HTTP代理以缓存静态数据可以帮助提升性能，但是需要进一步平涂

> 使用Nginx除了代理端口转发之外，还可以缓存静态文件，比如图片、CSS等，即动静分离，是Web应用的常见方法

#### Servlet容器

Jenkins 1.535版本之前的Winstone，1.535版本之后的Jetty8都是Jenkins内嵌的Web容器，比之于Tomcat，Jetty在持续的吞吐量和资源消耗方面由于Tomcat。但是最近的Jetty 8-9和Tomcat 7并没有明显的证据显示存在差距


### 2. Jenkins Slave Configuration

#### Slave数量

Jenkins开发团队与一个目标叫“X1K initiative”，即保证Jenkins Master能支持所有Slave共1000个执行器的平滑运行，到目前为止，这依然是一个挑战。有时候当Slave在250台左右出现大量Slave连接在构建过程中中断的情况。有证据显示当Slave过百时，Jenkins会出现Slave连接丢失的情况。因为在Jenkins core 1.521和SSH Slave Plugin 0.27中针对Jenkins remoting做的线程使用改进不应该出现这样的问题，但是并没有得到证实。

#### 单个Slave的执行器数量

超过Slave容量的情况下，增加执行器数量会因为崩溃、IO阻塞、RAM交换导致整体的吞吐量下降，合理配置 RAM, CPU cores and build 类型。关于RAM的配置，Slave的maximum memory setting配置需要能够支持最大了的Build。CPU应该足够使用，不会达到100%使用率。考虑IO时，IO会释放一些CPU时间，针对单线程的Build，每个CPU核心配置应少于1个执行器。考虑到IOPS限制，为了避免磁盘IO成为瓶颈，一般情况下，如果15分钟内，平均负载超过了CPU核心数量，则执行器数量应该降低。建议，每个Slave配置1个执行器以便实现隔离。基于云的Slave可以很方便的实现隔离，如果是基于专用硬件，可以通过轻量级容器实现同样的隔离。


### 3. Job Design

#### 清理Workspace
在Build之前删除Job的Workspace，以便获取干净的Build，或者在Build之后删除Job的Workspace，以便节约磁盘空间。这会导致重新签出代码，对Maven下载依赖而言可能时间更长，最终的Build耗时可能会翻倍。

应该在构建系统中明确，在构建脚本中明确使用可靠的目标“clean”，禁止在临时构建目录以外创建文件。永远不要修改版本控制下的文件。对于发布构建而言，如果构建正确性优于构建速度，可以经常定期的清理workspace。

#### 构件指纹

大型的指纹数据库可能会导致Jenkins Master性能下降。Copy Artifact plugin 总是会检查指纹。Maven构建会无条件地记录文件的指纹。

因此，阻止code review(Gerrit) build在Maven2/3构建时记录指纹，也许可以禁用Maven存档构件。对于自由风格的Job也同样适用。

#### 构建后操作
限制构建后步骤，它会引发并发构建变成串行（[JENKINS-9913](https://issues.jenkins-ci.org/browse/JENKINS-9913)）。将工作移到构建步骤中去，比如，使用定制的构件存档操作，如mvn deploy。

#### Maven Job vs Freestyle jobs
使用自由风格的Job，Maven Job尤其慢，并且有一些Bug.设置Jenkins核心贡献者都认为Maven job类型并不好

#### 大型构建日志
构建历史日志会加载到Jenkins Master的内存中，如果构建日志过大，由此会引发内存溢出错误。使用Log File Size Checker plugin 以便在控制台输出log超出限制时让Job失败

#### Sonar分析
在每次Build是使用Sonar分析会导致2-3倍的耗时。Sonar是一个监控和代码检查工具，不是守门人，在晚上执行Sonar，而不是在每次Build。

#### Reference repository for Git SCM

本地文件系统的Git仓库可以当做引用，只下载更新的代码，其他代码都是硬链接。

### 4. Multi Master

目前还没有多Master Jenkins 集群，在可预见的未来也不会有。在不定制Jenkins的情况下，唯一能够实现负载在Master之间共享的，只能是搭建多个master，分别支持不同的Job。
[Jenkins Enterprise by Cloudbees](http://www.cloudbees.com/jenkins/enterprise) 仅仅实现了故障容灾，它是一个“主备结构”，而不是负载均衡。
[Jenkins Operations Center by Cloudbees](http://www.cloudbees.com/joc)可以简化多master和slave的管理。但是并没有提供多master实例和单一入口。
OpenStack/HP 多master定制软件（Zuul+German）和基于其上的特定的标准化工作流。其并没有使用Jenkins UI，仅仅提供了Zuul和Gerrit的构建链接。构建临时，分析和趋势也是通过外部的搜索引擎收集的。

> 作者提到的外部搜索引擎是指OpenStack持续集成方案中的ELK（ElasticSearch+LogStash+Kibana）用于收集和分析日志

### General & Cultural tips

Follow [Keep it simple, stupid](http://en.wikipedia.org/wiki/KISS_principle) and [You aren't gonna need it](http://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it) principles.


### References

1. “Keynotes”. Kohsuke Kawaguchi, Cloudbees. Jenkins User Conference 2013 - Palo Alto.

	Slides: http://www.cloudbees.com/sites/default/files/juc/juc2013/2013-1023-JUC-PaloAlto-Kohsuke-Keynote.pptx

	Video: http://www.youtube.com/watch?v=FaMoiVpKUvQ

2. “Multiple Jenkins Master Support” Khai Do, Hewlett Packard. Jenkins User Conference 2013 - Palo Alto.
	
	Slides: http://docs.openstack.org/infra/publications/gearman-plugin/
	Video: http://www.youtube.com/watch?v=pLQddm85fPQ
3. “Maintaining Huge Jenkins Clusters - Have We Reached the Limit of Jenkins?” Robert Sandell, Sony Mobile Communications. Jenkins User Conference 2013 - Palo Alto.
	
	Slides: http://www.cloudbees.com/sites/default/files/juc/juc2013/2013-1023-Palo-Alto-Robert_Sandell-Maintaining-Huge-Jenkins-Clusters.pdf
	Video: http://www.youtube.com/watch?v=LRonDiXUx1U
4. "To Infinity & Beyond the Small Team" James Nord, Cisco
	
	Slides: http://www.cloudbees.com/sites/default/files/JUC_Palo_Alto_2013_TIaBTST.pdf
	Video: http://www.youtube.com/watch?v=CGjgS16dVUc
5. “Scaling Jenkins Horizontally with Jenkins Operations Center by Cloudbees”. Cloudbees blog: http://blog.cloudbees.com/2013/12/scaling-jenkins-horizontally-with.html
6. “Jenkins at Three Years: Becomes Literate, Does Mobile in the Cloud and Handles Multi-Branch”. Harpreet Singh & Kohsuke Kawaguchi, CloudBees. Jenkins User Conference 2013 - Palo Alto.
	
	Slides: http://www.slideshare.net/kohsuke/jenkins-user-conference-2013-literate-multibranch-mobile-and-more
	Video: http://www.youtube.com/watch?v=AKcQuOROFlI
7. “Jenkins Scalability Summit notes”. Jenkins Scalability Summit, Oct 2013 - Los Altos. https://docs.google.com/document/d/1GqkWPnp-bvuObGlSe7t3k76ZOD2a8Z2M1avggWoYKEs/edit#
8. “Kohsuke with OSS hat / Core improvements”. Jenkins Scalability Summit, Oct 2013 - Los Altos.
	
	Slides: https://wiki.jenkins-ci.org/download/attachments/68747344/Kohsuke.pptx
9. “Sony Mobile list to Santa Claus”. Robert Sandell, Sony Mobile. Jenkins Scalability Summit, Oct 2013 - Los Altos.

	Slides: https://wiki.jenkins-ci.org/download/attachments/68747344/Sony+Mobile.pptx
10. “Reducing the # of threads in Jenkins: SSH slaves”. Kohsuke Kawaguchi, Cloudbees. Jenkins CI blog: http://jenkins-ci.org/content/reducing-threads-jenkins-ssh-slaves
11. “High availability”. Jenkins Enterprise: http://www.cloudbees.com/jenkins-enterprise-cloudbees-features-high-availability-plugin.cb
12. “Jenkins' Maven job type considered evil”. Stephen Connolly. Stephen's Java Adventures. http://javaadventure.blogspot.ru/2013/11/jenkins-maven-job-type-considered-evil.html







