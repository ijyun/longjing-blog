Title: OpenStack持续集成实践
Date: 2016-05-13 10:20
Modified: 2015-05-13 19:30
Category: 持续集成
Tags: 持续集成, OpenStack,Gerrit,Jenkins
Slug: openstack-ci-case
Authors: 龙井
Summary: OpenStack是云计算领域当之无愧的红人，在Docker还没出现时，大家谈论的都是OpenStack。大多数企业在自建私有云平台时首选的都是OpenStack，对云计算的普及，作为开源软件的OpenStack影响意义深远。OpenStack这么大型的项目，模块众多，参与人数众多。如何帮助开发者更容易的参与到开源项目中来，如何降低持续集成的复杂度和管理难度都是摆在OpenStack团队面前的问题。

### OpenStack介绍
OpenStack是开源的云计算（IaaS）平台

![](http://docs.openstack.org/infra/publications/overview/images/openstack-software-diagram.png)

#### 项目列表
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



#### 发布管理
* 基于时间发布（Time Based Releases）
* 发布周期6个月
* 基于主干开发
* 内部里程碑发布
* 发布稳定版本

#### 贡献者

* 独立个人
* 商业组织
* 非盈利机构
* 国家或地区政府机构

![](http://docs.openstack.org/infra/publications/overview/images/contributor-pie-chart.png)


#### 标准工具

* Minimize meta-development最小化元开发
* 流程差异==浪费开发者时间
* 减少上手时间
* Consolidate tool development
* Minimize project-specific weird build crud

#### 开发基础设施
![图片](/images/ci/openstack-ci-case/develop-infrastructure.png)



OpenStack公布的资料

1. [Scaling OpenStack Development: Continuous Integration Overview](http://docs.openstack.org/infra/publications/overview)

#### 开发环境

Python

* Ubuntu LTS (2.7, 3.4, pypy)
* PEP-8 standards
* Oslo (common libraries)
* virtualenv/pip/tox

Freenode IRC (#openstack-dev, #openstack-meeting)

DevStack

Tests run on all newly submitted changes

Code merges are gated on tests

#### 项目门禁

保证代码质量
保护开发者
保证代码始终可集成
人人平等
流程相同
流程透明
流程自动化

#### 自动化一切

#### 持续集成工作流

![](http://docs.openstack.org/infra/publications/overview/images/openstack-ci-workflow.png)

#### 开发流程
![](http://docs.openstack.org/infra/publications/overview/images/contribution-path.png)


### Zuul
Zuul是面向流水线的项目门禁与自动化系统。

