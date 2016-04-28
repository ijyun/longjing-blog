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

我之前将DevOps划分为四个能力领域：组织文件、持续交付、技术运营、可视化：

**组织文化**：交付是团队每个人的责任，DevOps强调团队之间的沟通、协作与尊重，在组织与文化方面，让所有人就目标达成一致，一切都以更快更好地交付有价值的服务为目标。这其中包含了特性团队、自动化、内建质量、快速反馈、持续改进等实践能力

**持续交付**：持续交付是DevOps能力建设的突破口和基础，从代码提交到部署上线，持续交付架设起了从开发到技术运营之间的桥梁

**技术运营**：DevOps比持续交付更进一步的地方就在于它开始关注技术运营，并提倡开发团队与技术运营团队之间的有效协作，提倡开发能力、测试能力、持续交付能力、技术运营能力的相互延伸和服务。

**可视化**：可视化的意义在于通过数据分析度量DevOps能力、推动持续改进、便于团队基于全过程的数据分析与协作、帮助定位故障等。

DevOps工具元素周期表中的工具则是这四项能力的具体实现，如：自动化构建、持续集成、版本控制工具都是持续交付能力的实现；云计算、容器技术、发布管理、分析与监控、日志管理则是技术运营能力的实现。

![图片](/images/devops/devops-tool-periodic-table/devops-tool-periodic-table.png)

下面就每个工具进行简单介绍，便于大家在选型工具时作为参考：

### 1. 数据库

##### 12c

##### MySQL

##### MSSQL

##### PostgreSQL

##### MongoDB

##### DB2

##### Cassandra

### 2. 版本控制

##### Git

Git是一款分布式版本控制系统，具有如下特点：速度快、数据完整性强、分布式、多分支的工作流。Git由Linus Torvalds于2005年为管理Linux Kernel而开发。之后它迅速的成为了最受欢迎的版本控制系统。
Git实质是一套文件系统
通过不同的分支策略适应不同的开发、测试与发布的模式。

##### Subversion

##### Github

##### Bitbucket

##### Mercurial

##### Helix


### 3. 自动化构建

##### Maven

##### Gradle

##### ANT

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