Title: OpenStack持续集成实践
Date: 2016-05-13 10:20
Modified: 2015-05-13 19:30
Category: 持续集成
Tags: 持续集成, OpenStack,Gerrit,Jenkins
Slug: openstack-ci-case
Authors: 龙井
Summary: OpenStack是云计算领域当之无愧的红人，在Docker还没出现时，大家谈论的都是OpenStack。大多数企业在自建私有云平台时首选的都是OpenStack，对云计算的普及，作为开源软件的OpenStack影响意义深远。OpenStack这么大型的项目，模块众多，参与人数众多。如何帮助开发者更容易的参与到开源项目中来，如何降低持续集成的复杂度和管理难度都是摆在OpenStack团队面前的问题。
Image: /ci/openstack-ci-case/openstack-software-diagram.png

<link rel="stylesheet" href="http://yandex.st/highlightjs/6.2/styles/googlecode.min.css">
 
<script src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
<script src="http://yandex.st/highlightjs/6.2/highlight.min.js"></script>
 
<script>hljs.initHighlightingOnLoad();</script>
<script type="text/javascript">
 $(document).ready(function(){
      $("h1,h2,h3,h4,h5,h6").each(function(i,item){
        var tag = $(item).get(0).localName;
        if ($(this).text()!="目录") {
        
          
        $(item).attr("id","wow"+i);
        $("#category").append('<font class="new'+tag+'" >'+$(this).text()+'</font></br>');
        $(".newh1").css("margin-left",0);
        $(".newh1").css("font-size",22);
        $(".newh2").css("margin-left",20);
        
        $(".newh2").css("font-size",20);
        $(".newh3").css("margin-left",40);
        $(".newh3").css("font-size",18);
        $(".newh4").css("margin-left",60);
        $(".newh4").css("font-size",16);
        $(".newh5").css("margin-left",80);
        $(".newh5").css("font-size",14);
        $(".newh6").css("margin-left",100);
       
        
        }
 
      });
 });
</script>
<div id="category"></div>

<div style="height:300px"></div>

### 一、OpenStack介绍
OpenStack是一个旨在为公共及私有云的建设与管理提供软件的开源项目，属于云计算（IaaS）平台，其包含众多子项目，有大量的机构与厂商和开发者参与到OpenStack的生态中。

![openstack](http://docs.openstack.org/infra/publications/overview/images/openstack-software-diagram.png)


#### 0. 架构图

![architecture](/images/ci/openstack-ci-case/openstack-logical-arch-folsom.png)

#### 1. 项目列表
* nova (compute)
* swift (object storage)
* glance (image service)
* keystone (identity service)
* neutron (network service)
* cinder (volume service)
* heat (orchestration)
* ceilometer (measurement)
* horizon (dashboard)
* trove (databases)
* sahara (hadoop)

详细项目列表：[http://www.openstack.org/software/project-navigator](http://www.openstack.org/software/project-navigator)



#### 2. 发布管理
* 基于时间发布（Time Based Releases）
* 发布周期6个月
* 基于主干开发
* 内部里程碑发布
* 发布稳定版本

#### 3. 贡献者

* 独立个人
* 商业组织
* 非盈利机构
* 国家或地区政府机构

![contributor](http://docs.openstack.org/infra/publications/overview/images/contributor-pie-chart.png)

#### 4. CI规模
1. 500+ Git仓库
2. 5000+ Jenkins Jobs
3. 10+ Jenkins Masters
4. 1000+ Slaves
5. 24000+ Jobs per day
6. 300+ Developer

#### 5. CI挑战

1. 项目多、Git仓库多、分支多（master、stable、cinder...）
2. Job巨多（pep8、doc、test、deploy...）
3. Job配置麻烦（multiple backends, multiple clouds, multiple deploy sites, etc..）
4. CI Pipeline复杂/多（check、gate、release、periodic...）

#### 6. 当前持续集成的问题

1. XML难以维护
2. 经常复制和粘贴Job
3. divergent jobs（不一致）
4. Job配置没有版本化
5. 无法保证类似Job的相同配置
6. 一个Job就得对应一个XML文件
7. **创建、维护、自动化都很复杂**


### 二、持续集成实践

#### 1. 开发基础设施
![tools](/images/ci/openstack-ci-case/develop-infrastructure.png)

持续集成系统主要的工具：

1. Storyboard
2. Gerrit（Code Review，Git）
3. Zuul（CI gate keeper,Build Triggering）
4. German(CI gate keeper)
5. Jenkins（CI，Automation，Jenkins-job-builder[CI Project creator]，gearman-plugin）
6. Devstack(Cloud Test VMs)
7. Nodepool(Cloud VM Manager)
8. ELK(日志管理)
9. Launchpad（Bugs、Releases）
10. Blueprints（Launchpad Blueprints用于跟踪重大特性的实现）
11. IRC
12. Python tox（Python打包、测试、发布工具）
13. VirtualEnv（在一台机器上创建多个独立的Python运行环境）

其中：Zuul、Jenkins-job-builder、gearman-plugin、Devstack、Nodepool都是OpenStack Infrastructure team出品。

#### 2. 标准化工具

* Minimize meta-development最小化元开发
* 流程差异==浪费开发者时间
* 减少上手时间
* Consolidate tool development
* Minimize project-specific weird build crud

##### 开发环境

**Python**

* Ubuntu LTS (2.7, 3.4, pypy)
* PEP-8 standards
* Oslo (common libraries)
* virtualenv/pip/tox

**Freenode IRC (#openstack-dev, #openstack-meeting)**

**DevStack**

**Tests run on all newly submitted changes**

**Code merges are gated on tests**



#### 3. 核心理念
##### 项目门禁
代码提交和代码合并都设置有相应的门禁

**作用**

1. 保证代码质量
2. 保护开发者，开发总是从可工作的代码开始
3. 保证代码始终可集成，有问题的代码不会被集成到主干
4. 持续进行测试
5. 人人平等	
  	1. 流程相同
	2. 流程透明
	3. 流程自动化


##### 自动化一切

#### 4. 工作流
##### 持续集成工作流

![CI Workflow](http://docs.openstack.org/infra/publications/overview/images/openstack-ci-workflow.png)

##### 开发流程
![Process Flow](http://docs.openstack.org/infra/publications/overview/images/contribution-path.png)

#### 5. 代码审查-Gerrit
OpenStack采用Gerrit进行代码审查，主要的配置内容包括：project、group、users、acl（访问控制列表）。与Gerrit集成主要通过hooks、event-stream、REST API。
##### States of a Patch

1. Code Submitted
2. Code Verified
3. Code Reviewed
4. Code Accepted
5. Code Merged

##### Gerrit Triggers类型

1. Patchset uploaded
2. Change merged
3. Comment added (review state)
4. Ref updated (branches, tags, etc)

##### Gerrit与Jenkins集成
在Gerrit评论中显示Jenkins的Job执行结果和耗时，作为审查的依据

##### Gerrit辅助配置工具Jeepyb
Jeepyb是一组帮助简化Gerrit管理的工具集，可以很简便的管理project并和Launchpad/Github进行集成。在Jeepyb中采用YAML文件进行项目定义：

	:::python
	- project: example/gerrit
	  description: Fork of Gerrit used by Example
	- project: openstack/project-name
	  acl-config: /home/gerrit2/acls/project-name.config
	  upstream: git://github.com/awesumsauce/project-name.git
Jeepyb基于Gerrit的分组：Administrators,Registered Users,Anonymous Users划分每个项目的项目，针对每个项目都有一个ACL的配置文件。Jeepyb描述项目和分值的权限采用git refs的语法格式。

	:::python
	[access "refs/heads/*"]
	label-Code-Review = -2..+2 group project-name-core
	label-Workflow = -1..+1 group project-name-core
	
	[access "refs/heads/proposed/*"]
	label-Code-Review = -2..+2 group project-name-milestone
	label-Workflow = -1..+1 group project-name-milestone
	
	[receive]
	requireChangeId = true
	requireContributorAgreement = tree
	
	[submit]
	mergeContent = true	

##### Gerrit和Launchpad集成

修改etc/gerrit.config

	:::python
	[commentlink "launchpad"]  
	  match = "([Bb]ug\\s+#?)(\\d+)"  
	  link = https://bugs.launchpad.net/mahara/+bug/$2

[Jeepyb参考文档](http://docs.openstack.org/infra/system-config/jeepyb.html)

[Gerrit项目配置文档](https://gerrit-review.googlesource.com/Documentation/config-project-config.html)

#### 6. 持续集成-Jenkins
在OpenStack的实践中，Jenkins使用Zuul和Gearman进行管理。
Jenkins中的Job类型包括：
##### Gate tests
* unit tests
* integraton tests
* code style

##### Post-merge automation
* docs
* tarballs
* pypi

##### Jobs under development
* experimental
* silent
* non-voting

##### Periodic jobs
* bitrot checks
* image updates
* very long tests

#### 7. 任务配置管理-Jenkins Job Builder
Jenkins Job Builder基于YAML格式来定义Job内容，采用命令行创建和管理Jenkins Job，JJB文件采用版本控制进行管理。JJB使用Jenkins的API操作Jenkins的功能，支持Python 2.7~3.4。

##### 效果

1. 一次定义，多处使用，5859个Job只有87个定义文件JJB
2. 参数化Job配置，易于维护
3. 版本化Job定义，易追溯
4. 更加高效和容易对阅读、创建和维护Job
5. Developers empowered to own their Jenkins jobs

##### OpenStack的使用方式

1. 所有Job都是以JJB（Jenkins只是用来查看的）
2. 使用YAML定义Job文件
3. 使用Gerrit管理Job定义的创建和变更
4. 使用一个JJB定义创建多个Jobs
5. 使用Puppet推送JJB进行部署、更新Jenkins的Job

##### 示例
Job模板

	:::python
	- job-template:
	    name: 'gate-{name}-docs'
	    builders:
	      - shell: 'git checkout {branch_name}'
	
JJB项目定义
	
	:::python
	- project:
	    name: project-name
	    branch_name: new_branch
	    jobs:
	      - gate-{name}-docs
	      
Job分组管理
	
	:::python
	- job-group:
	    name: '{name}-tests'
	    jobs:
	      - '{name}-unit-tests'
	      - '{name}-perf-tests'
	
Job定义
	
	:::python
	- job:
	    name: foo-test
	    project-type: freestyle
	    builders:
	      - make-test
	    publishers:
	      - archive
可以在Job中增加模块，比如：builder、publisher等
使用宏来定义Jenkins中的Action

	:::python
	- builder:
	  name: make-test
	  builders:
	  	- shell: 'make test'	     

安装与使用Demo

	:::python
    1. Install
        1. pip install jenkins-job-builder
    2. Run
        1. jenkins-jobs --conf my_jenkins.ini update simple.yaml

    
simple.yaml：

	:::python
	# a simple job
	- job:
	     name: simple
	     node: centos
	     builders:
		- shell: ‘echo this is my job’	
demo.yaml
	
	:::python
	# demo using JJB templates
	- job-template:
	    name: '{name}-{pyver}-{tests}-{branch}'
	    builders:
	      - shell: 'git checkout {branch_name}'
	    publishers:
	      - email:
	      	  recipients: '{mail-to}'	
	 - project:
	 	name:nova
	 	pyver:
	 	  - py26:
	 	  	 branch: stable-1.0
	 	  - py27:
	 	  	 branch: master
	 	tests:
	 	  - unit:
	 	  	 mail-to: developer@nowhere.net
	 	  - perf:
	 	  	 mail-to: tester@nowhere.net	 	
	 	jobs:
	 	  - '{name}-{pyver}-{tests}-{branch}'  	
server.ini
	
	:::python
	# JJB configuration
	[jenkins]
	user=USERNAME
	password=PASSWORD
	url=http://localhost:8080
	  
执行

	:::python
	
	# Test JJB yaml to xml transform
	jenkins-jobs test -o output demo.yaml
	# Upload to Jenkins server
	jenkins-jobs --conf server.ini update demo.yaml
	将会一次性创建多个到output下
	

##### 特性

* Works with Jenkins REST Api
* Default definitions to reuse parameters
* Macro definitions to reuse plugins
* Template definitions to reuse jobs
* Projects to group related jobs
* Job groups to organize related job templates
* Test jobs before deploying
* Automated job removal
* Cache for idempotent job updates
* Unit tests (84% coverage)
* Documented




##### Nodepool构建资源池

* Service used to deploy and manage a pool of devstack images on the cloud
* Works with any OpenStack provider
* Once per day a new image is generated with cached devstack content
* Spins instances based on desired image on demand
* Can use disk-image-builder to build images
* Communicates with Zuul using gearman-servers for getting realtime demand
* Communicates with Jenkins to attach nodes using Jenkins API

	


  
针对Jenkins Job Builer的单独介绍：[http://docs.openstack.org/infra/publications/jenkins-job-builder/](http://docs.openstack.org/infra/publications/jenkins-job-builder/)
Jenkins Job BUilder配置实例[:http://git.openstack.org/cgit/openstack-infra/project-config/tree/jenkins/jobs](http://git.openstack.org/cgit/openstack-infra/project-config/tree/jenkins/jobs)





#### 8. 流水线配置-Zuul
Zuul是面向流水线的项目主干门禁与自动化系统。和Gerrit与Jenkins有接口，配置灵活（layout.yaml），适合多种项目的自动化，可以并行执行一系列变更的测试。
Zuul的两个主要组件：scheduler和merger。Zuul保证合并进入源代码库的变更都是通过测试的。


OpenStack的Zuul Pipelines类型包括：check、gate、release、silent、experimental、periodic...
Zuul会监测Gerrit的事件以触发相应的Pipeline及其对应的Job。


##### 组件

* Connection（Gerrit，SMTP）
* Trigger（Gerrit，Timer，Zuul）
* Reporters（Gerrit，SMTP）
* Zuul Cloner
* Launchers（Gearman Jenkins Plugin）
* Statsd reporting（Metrics）
* Zuul Client


* [文档资料](http://docs.openstack.org/infra/zuul/)
* [源代码](https://github.com/openstack-infra/zuul)

**Zuul Project Configuration**

	:::python
	projects:
	  - name: openstack/nova
	    check: 
	      - gate-nova-pep8
	      - gate-nova-docs
	      - gate-nova-python27
	      - gate-tempest-devstack-vm-full
	    gate: 
	      - gate-nova-pep8
	      - gate-nova-docs
	      - gate-nova-python27
	      - gate-tempest-devstack-vm-full
	    experimental: 
	      - gate-devstack-vm-cells 
	    slient: 
	      - gate-tempest-devstack-vm-large-ops
	    post: 
	      - nova-branch-tarball
	      - nova-coverage
	      - nova-docs
	      - nova-upstream-translation-update
	    pre-release:
	      - nova-tarball     
	    release:
	      - nova-tarball  
	      - nova-docs
	    periodic:
	      - nova-propose-translation-update
	      - periodic-nova-python27-stable-folsom     
	      - periodic-nova-python27-stable-grizzly  

##### Project Gating
Preemptive CI


##### Speculative Execution（预测执行）
* Serialize changes across all projects
* Speculative execution of tests
* Run in parallel in order triggered
* Assume success
* Start over on failure

[**预测执行**](https://en.wikipedia.org/wiki/Speculative_execution)会预测并提前执行可能需要的任务，以便加速整个处理过程，在流水线中广泛使用以提高整体效率！

##### Check Pipeline

	:::python
	pipelines:
	  - name: check
	    manager: IndependentPiplelineManager
	    precedence: low
	    trigger:
	      gerrit:
	      	- event: patchset-created
	    success:
	      gerrit:
	        verified: 1
	    failure:
	      gerrit:
	        verified: -1
	    
##### Gate Pipeline

	:::python
	pipelines:
	  - name: name
	    manager: DependentPiplelineManager
	    precedence: high
	    trigger:
	      gerrit:
	      	- event: comment-added
	      	  approval:
	      	    - approved: 1
	    start:
	      gerrit:
	        verified: 0    	    
	    success:
	      gerrit:
	        verified: 2
	        submit: true
	    failure:
	      gerrit:
	        verified: -2

##### Post-Merge Pipeline

	:::python
	pipelines:
	  - name: post
	    manager: IndependentPiplelineManager
	    trigger:
	      gerrit:
	      	- event: ref-updated
	  	      ref: ^(?!refs/).*$

##### Experimental Pipeline

	:::python
	pipelines:
	  - name: experimental
	    precedence: low
	    trigger:
	      gerrit:
	      	- event: comment-added
	      	  comment_filter: (?i)^\s*check experimental\s*$
	    success:
	      gerrit:
	        force-message: true    	    
	    failure:
	      gerrit:
	        force-message: true

##### Slient Pipeline

	:::python
	pipelines:
	  - name: slient
	    manager: IndependentPiplelineManager
	    trigger:
	      gerrit:
	      	- event: patchset-created
	      	
##### Release Pipeline

	:::python
	pipelines:
	  - name: release
	    manager: IndependentPiplelineManager
	    precedence: high
	    trigger:
	      gerrit:
	      	- event: ref-updated
	  	      ref: ^refs/tags/([0-9]+\.)+[0-9]+$
	  - name: pre-release
	    manager: IndependentPiplelineManager
	    precedence: high
	    trigger:
	      gerrit:
	      	- event: ref-updated
	  	      ref: ^refs/tags/([0-9]+\.)+[0-9]*(alpha|beta|candidate|rc|a|b|c|r|g)[0-9]*$

##### Periodic Pipeline

	:::python
	pipelines:
	  - name: peiodic-stable
	    description: Periodic checks of the stable branches
	    manager: IndependentPiplelineManager
	    precedence: low
	    trigger:
	      timer:
	      	- time: '1 6 * * *'
	    failure:
	      smtp:
	        from: jenkins@openstack.org
	        to: openstack-stable-maint@lists.openstack.org
	        subject: 'Stable check of {change.project} failed'
	         
	      
##### Zuul Change Queue

	:::python
	projects:
	  - name: openstack/nova
	    gate: 
	      - gate-nova-python27
	      - gate-tempest-devstack-vm
	  - name: openstack/glance
	    gate:
	      - gate-glance-python27
	      - gate-tempest-devstack-vm


##### Zuul执行状态视图

![Zuul Status View](http://docs.openstack.org/infra/publications/zuul/images/status.png)

#### 9. 任务分发（集群）-Gearman

##### Gearman介绍

Gearman是分布式队列系统，分发合适的任务到多台计算机上，以便快速完成大型任务

###### Gearman架构图

![Architecture](http://docs.openstack.org/infra/publications/gearman-plugin/images/GearmanOverview.gif)

###### Gearman-Jenkins插件架构图

![gearman_plugin_architecture](http://docs.openstack.org/infra/publications/gearman-plugin/images/gearman_plugin_architecture1.png)

作用：消息系统，分发来自Zuul的工作，Gearman将job server的job发送到job workers上。
流程：

1. Worker注册到Gearman中
2. Zuul提交构建请求到Gearman
3. Gearman分发Job到Workers

###### Gearman Client示例

Python Client：[https://github.com/zaro0508/gearman-plugin-client](https://github.com/zaro0508/gearman-plugin-client)

Java Client：[https://git.openstack.org/cgit/openstack-infra/gearman-plugin/tree/src/main/java/hudson/plugins/gearman/example](https://git.openstack.org/cgit/openstack-infra/gearman-plugin/tree/src/main/java/hudson/plugins/gearman/example)

Zuul Client：[http://git.openstack.org/cgit/openstack-infra/zuul](http://git.openstack.org/cgit/openstack-infra/zuul)

###### 特性

* Gearman plugin reloads on jenkins restart: meaning that when jenkins restarts the gearman worker threads are automatically restarted and reconnect to a gearman server.
* High availability(ish). When one master goes down the other master(s) will continue to execute builds however the in flight jobs on the down master will be lost.
* Horizontal scalability. Just continue to add more jenkins masters to distribute the load between masters
* Slaves are always shared between masters. Offline or disconnect a slave will un-share it
* Gearman jobs can start a jenkins build
* Gearman jobs can stop or abort a jenkins build
* Gearman jobs can change a build description
* Gearman jobs can pass in parameters to jenkins builds
* Gearman jobs can automatically set a slave to offline after running a build
* Gearman plugin is aware of Jenkins project status: meaning that gearman will register/unregister projects when the project is enabled or disabled.
* Gearman plugin is aware of slave status: meaning that gearman will register/unregister slaves when a slave is set online/offline and connected/disconnected.

###### Jenkins Master集群化的好处

* 水平扩展
* 冗余、稳定性
* 弹性Node


##### 水平扩展

![horizontal scaling](http://docs.openstack.org/infra/publications/gearman-plugin/images/gearman_plugin_architecture2.png)


##### Jenkins集群化（冗余）

![redundant jenkins](/images/ci/openstack-ci-case/gearman-flow1.png)

##### Gearman-Jenkins集成

![Gearman-Jenkins Integration](/images/ci/openstack-ci-case/gearman-flow3.png)

![Jenkins Buildables as Gearman Functions](http://docs.openstack.org/infra/publications/gearman-plugin/images/gearman-flow4.png)
Meta-jobs：

* stop job
* set description
     
#### 工具集成

Bug Integration - Launchpad

#### 测试分类

##### 代码风格检测



##### Unit tests
1. 测试代码
2. 快速失败
3. 开发者易于执行，可在虚拟环境中执行

##### Functional tests
1. 测试服务功能
2. 开发者易于执行

##### Integration tests

1. 测试系统
2. 在真实环境中测试
3. 执行耗时

其他：
Test Repository 框架，实现并行测试
Zuul可以实现测试并行执行，又能保持测试顺序不变

一个Jenkins master带100个slave之后就会遇到问题

自动化解决的问题不是今天的问题，而是三个月之后的问题。

#### Devstack-Gate
开发者工具，结合云
http://docs.openstack.org/infra/publications/devstack-tutorial/

Git Review





#### 日志管理

![日志管理架构](http://docs.openstack.org/infra/publications/overview/images/logstash-diagram-small.png)

Design

* Jenkins ZeroMQ Event Publisher
* Gearman, process logs in batches one job per file
* Filter extensively





### 相关资料

1. [Scaling OpenStack Development: Continuous Integration Overview](http://docs.openstack.org/infra/publications/overview)
2. [How OpenStack Improves Code Quality with Project Gating and Zuul](http://docs.openstack.org/infra/publications/zuul)
3. [Continuous integration automation: An outline of OpenStack CI components](http://docs.openstack.org/infra/publications/ci-automation)
4. [Scaling Your Jenkins Jobs：Jenkins Job Builder](http://docs.openstack.org/infra/publications/jenkins-job-builder)
5. [Multiple Jenkins Masters：with Jenkins Gearman Plugin](http://docs.openstack.org/infra/publications/gearman-plugin)
6. [Interview-openstack-ci-test-automation](http://www.infoq.com/cn/articles/interview-openstack-ci-test-automation)
7. [Processing-ci-log-events](http://docs.openstack.org/infra/publications/processing-ci-log-events)