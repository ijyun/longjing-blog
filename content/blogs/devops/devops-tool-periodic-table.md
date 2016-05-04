Title: DevOps元素周期表解读
Date: 2016-04-26 11:30
Modified: 2016-04-26 11:30
Category: DevOps
Tags: DevOps, 持续集成, 持续交付, 自动化测试, 自动化部署,云计算,Docker, 2016
Slug: devops-tool-periodic-table
Authors: 龙井
Summary: DevOps元素周期表是XebiaLabs整理发布的，2015年发布了V1版本，后续应该会持续更新，DevOps涉及持续交付、技术运营、云计算、组织协作等等方方面面，所以相关工具也会很多，工具也是大家在实践DevOps过程中最容易入手的，但是DevOps绝不仅仅是自动化工具而已，高效协作的组织、责任共担的文化才是DevOps真正要解决的问题。
Image: /devops/devops-tool-periodic-table/devops-tool-periodic-table.png


### 整体介绍

我之前将DevOps能力划分为四个领域：**组织文化、持续交付、技术运营、可视化**：

**组织文化**：交付是团队每个人的目标和责任，DevOps强调团队之间的沟通、协作与尊重，在组织与文化方面，让所有人就目标达成一致，一切都以更快更好地交付有价值的服务为目标。这其中包含了特性团队、自动化、内建质量、快速反馈、持续改进等实践能力

**持续交付**：持续交付是DevOps能力建设的突破口和基础，从代码提交到部署上线，持续交付架设起了从开发到技术运营之间的桥梁

**技术运营**：DevOps比持续交付更进一步的地方就在于它开始关注技术运营，并提倡开发团队与技术运营团队之间的有效协作，提倡开发能力、测试能力、持续交付能力、技术运营能力的相互延伸和服务。

**可视化**：可视化的意义在于通过数据分析度量DevOps能力、推动持续改进、便于团队基于全过程的数据分析与协作、帮助定位故障等。

DevOps工具元素周期表中的工具则是这四项能力的具体实现，如：自动化构建、持续集成、版本控制工具都是持续交付能力的实现；云计算、容器技术、发布管理、分析与监控、日志管理则是技术运营能力的实现。

![图片](/images/devops/devops-tool-periodic-table/devops-tool-periodic-table.png)

下面就每个工具进行简单介绍，便于大家在选型工具时作为参考：

### 1. 数据库

##### Oracle
Oracle在数据库领域依然是最牛的，12c提供了基于云的部署方式。就一个字，贵的伤人。

##### MySQL
MySQL是非常流行的开源关系型数据库，现在也支持NoSQL特性，随着Java和LAMP技术栈的普及，MySQL的普及度还是非常高的。

##### MSSQL

微软的关系型数据库

##### PostgreSQL
在国外非常流行的开源关系型数据库，也支持NoSQL

##### MongoDB
最流行的NoSQL数据库

##### DB2

##### Cassandra

关于数据库，我了解的不多，随着云计算的普及，我建议中小型团队可以采用云数据库，比如AWS和阿里云的RDS产品等，能极大的降低大家对数据库的投入，从而专注于核心业务。

### 2. 版本控制

##### Git

Git是一款分布式版本控制系统，具有如下特点：速度快、数据完整性强、分布式、多分支的工作流。Git由Linus Torvalds于2005年为管理Linux Kernel而开发。之后它迅速的成为了最受欢迎的版本控制系统。

我个人认为**Git最大的优势就是它解放了程序员**。

**相关工具：**

Repo：Google封装的Git管理工具，适用于大批量的操作Git库，用户Android代码管理

Gerrit：Google开源的代码审查工具，用于Android代码管理

Phabricator：Facebook开源的代码审查工具

Gitlab：和Github类似的开源Git托管工具，基于Ruby On Rails开发，个人认为是目前最好用的Git托管工具，分为社区版和企业版，开源中国的git.oschina.net就是基于Gitlab定制的，对于搭建Gitlab而言，难点在于存储。


**推荐书籍：**

《Git权威指南》——蒋鑫

##### Subversion
Apache Subversion(别名SVN)是基于Apache License分发的免费的软件版本控制系统。开发者用SVN管理代码、网页、文档的版本。SVN目前仍然很流行，因为它简单，集中式的管理模式易于管理，权限能控制到目录级别（Git可以通过拆分仓库完成权限的细粒度控制）。另外，SVN在存储二进制文件方面比Git强（存储方式不同，Git不压缩二进制文件，这也是快的原因），更容易处理大文件，所以SVN常备用作文档共享工具或者二进制成品库，运维团队常使用SVN管理部署软件包，需求团队常使用SVN管理需求文档。

##### Mercurial
简称Hg(水银)，也是分布式版本控制系统，和Git很类似，我没用过Mercurial，很多人反馈Mercurial更简单，跨平台更好，没有Git那么陡峭的学习曲线。但是Git功能会更强大。我觉得这个跟理念有关，Git是从文件系统演化而来。

*Git、Subversion、Mercurial是目前主流的三款版本控制工具，其他还有CVS、Rational Clearcase（IBM出品，复杂但是控制严格，金融行业用的比较多）下边要介绍的准确讲都不能成为版本控制工具，他们都是基于版本控制工具提供的版本控制服务。*

##### Github
准确的说Github不能算版本控制系统，Github是基于Web的Git托管服务，提供了仓库管理、Fork、权限控制、团队协作等特性，Github无疑是最大的代码托管服务，拥有大量的开源代码和周边工具。Github中Public（公开）项目不收费，Private（私有）私有项目收费，另外Github也有企业版，不过和虚拟技术绑定的比较紧密。

**相关工具：**

Travis-CI：基于Github的持续集成SaaS服务

##### Bitbucket
Bitbucket也是代码托管服务，支持Mercurial和Git，Atlassian公司出品，和JIRA等工具集成性更好。

##### Helix

国外的基于Git的代码托管服务，小众。


### 3. 自动化构建

##### Maven

Maven是Java项目的主流自动化构建工具之一，Maven主要包括：项目管理、构建、依赖管理三方面的功能，其和Ant最大的不同在于设计哲学：约定大于配置。

示例：

pom.xml
		
	:::xml
	<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
		xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
		<modelVersion>4.0.0</modelVersion>
		<parent>
			<groupId>com.juvenxu.mvnbook.account</groupId>
			<artifactId>account-parent</artifactId>
			<version>1.0.0-SNAPSHOT</version>
		</parent>
		
		<artifactId>account-persist</artifactId>
		<name>Account Persist</name>
	
	  <properties>
	  	<dom4j.version>1.6.1</dom4j.version>
	  </properties>
	
		<dependencies>
			<dependency>
				<groupId>dom4j</groupId>
				<artifactId>dom4j</artifactId>
				<version>${dom4j.version}</version>
			</dependency>
			<dependency>
				<groupId>org.springframework</groupId>
				<artifactId>spring-core</artifactId>
			</dependency>
			<dependency>
				<groupId>org.springframework</groupId>
				<artifactId>spring-beans</artifactId>
			</dependency>
			<dependency>
				<groupId>org.springframework</groupId>
				<artifactId>spring-context</artifactId>
			</dependency>
			<dependency>
				<groupId>junit</groupId>
				<artifactId>junit</artifactId>
			</dependency>
		</dependencies>
	
		<build>
			<testResources>
				<testResource>
					<directory>src/test/resources</directory>
					<filtering>true</filtering>
				</testResource>
			</testResources>
		</build>
	</project>

**相关工具：**

Nexus：Maven需要从远程仓库中获取插件、依赖，在团队内搭建Nexus可以缓存外部仓库，能提高效率，并且为基于组件的协作提供基础。

**推荐书籍：**

《Maven实战》——许晓斌

*另外：Maven也可以作为ASP.NET项目的构建工具*

##### Gradle

Gradle是比Ant和Maven更进一步，基于Groovy的DSL替换XML描述项目配置与构建过程。Gradle采用DAG(有向无环图，任意一条边有方向，且不存在环路的图)决定构建任务的执行顺序。

示例：

build.gradle

	:::groovy
	apply plugin: 'java'
	apply plugin: 'eclipse'
	apply plugin: 'application'
	
	mainClassName = 'hello.HelloWorld'
	
	// tag::repositories[]
	repositories {
	   mavenCentral()
	}
	// end::repositories[]
	
	// tag::jar[]
	jar {
	   baseName = 'gs-gradle'
	   version =  '0.1.0'
	}
	// end::jar[]
	
	// tag::dependencies[]
	sourceCompatibility = 1.8
	targetCompatibility = 1.8
	
	dependencies {
	   compile "joda-time:joda-time:2.2"
	}
	// end::dependencies[]
	
	// tag::wrapper[]
	task wrapper(type: Wrapper) {
	   gradleVersion = '2.3'
	}
	// end::wrapper[]

##### ANT

**相关工具：**
Ivy：和Ant配合使用管理依赖

##### Rake

##### Buildr

##### QuickBuild

##### MSBuild


##### UrbanCode Build

##### Meister

##### BuildMaster

##### Visual Build

##### LuntBuild

### 4. 持续集成

##### Jenkins

##### Bamboo

##### Travis CI

##### Snap CI

### 制品库

### 自动化测试

### 自动化部署

### 自动化配置

### 容器技术

### 云计算

### 发布管理

### 协作

### 分析与监控

### 日志管理

### 安全


[下载元素周期表](/images/devops/devops-tool-periodic-table/devops-tool-periodic-table.png)

原文地址：[https://xebialabs.com/periodic-table-of-devops-tools/](https://xebialabs.com/periodic-table-of-devops-tools/)