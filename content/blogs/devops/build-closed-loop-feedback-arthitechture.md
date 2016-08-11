Title: 构建闭环反馈架构（整理自中生代分享）
Date: 2016-08-11 9:30
Modified: 2016-08-11 9:30
Category: DevOps
Tags: DevOps, 2016
Slug: build-closed-loop-feedback-arthitechture
Authors: 龙井
Summary: DevOps元素周期表是XebiaLabs整理发布的，2015年发布了V1版本，后续应该会持续更新，DevOps涉及持续交付、技术运营、云计算、组织协作等等方方面面，所以相关工具也会很多，工具也是大家在实践DevOps过程中最容易入手的，但是DevOps绝不仅仅是自动化工具而已，高效协作的组织、责任共担的文化才是DevOps真正要解决的问题。


本文整理自中生代技术群的分享，由拍拍贷基础框架研发总监――杨波老师带来的《构建闭环反馈架构》。

首先申明下，今天的主题虽然叫“构建闭环反馈架构”，但主要是面向技术管理的主题，可能会让一些技术和业务视角的同学有一点点失望。

本分享总结软件研发型组织在产品、组织、流程和架构方面经常需要关注的一些反馈环(feedback loop)，以及强化这些反馈环需要哪些支撑性的技术和架构手段，希望对组织在这些方面改进提升有一定的指导价值。另外，本分享希望对研发工程师和架构师建立闭环反馈和DevOps意识有一定的指导意义。

本分享假设针对提供SAAS服务的软件研发型组织，其它类型涉及IT系统的组织也可从中获得借鉴。

### 第一部分，系统提升的一般性方法和反馈环
IT运维管理畅销书《凤凰项目》的作者Gene Kim在调研了众多高性能IT组织后总结了支持DevOps运作的三个原理(The Three Ways: The Principles Underpinning DevOps)，见下图

![image](/images/devops/build-closed-loop-feedback-arthitechture/the-three-ways.png)

虽然这三个原理是针对DevOps提出的，但我认为它们也是系统提升的一般性原理，其核心是反馈环：

#### 原理一、系统思考(Systems Thinking)
开发驱动的组织，其能力不是制作软件，而是持续的交付客户价值。价值从业务需求开始，经过研发测试，到部署运维，依次流动，并最终以服务形式交付到客户手中。整个价值流速并不依赖单个部门（团队或个人）的杰出工作，而是受整个价值链最薄弱环节的限制，所以局部优化通常是无效的，反而常常导致全局受损。

#### 原理二、强化反馈环(Amplify Feedback Loops)
过程改进常常通过加强和缩短反馈环来达成，原理二强调强化企业和客户之间，企业组织团队间，流程上和系统内的反馈环。没有测量就没有提升，反馈要以测量和数据作为基础，通过反馈数据来优化和改进系统。

#### 原理三、持续试验和学习的文化(Culture of Continual Experimentation And Learning)
在企业文化层面强调勇于试错和持续试验的文化，让企业内部自发涌现更多创新和系统提升的反馈环。


简言之，技术研发型组织（尤其是领导层）要从全局视角审视整个IT价值流，改善瓶颈和短板，强化系统内外的反馈环，鼓励试错试验文化，让价值在整个系统内更快、更好和更平滑的流动。

在构建闭环反馈进行系统提升方面，组织普遍存在的两个问题是：

1. 反馈环不封闭。一个常见的例子是，因为没有构建有效的数据收集、分析和监控体系，也就没有反馈数据，决策主要依靠猜测（拍脑袋）。另外，组织部门之间如果隔阂严重，缺乏信任和沟通，也容易造成反馈环不封闭；


2. 反馈比较慢，或者说迟反馈。设想一个场景，你踩下刹车之后，你的车要过10秒后才有反应，结果会怎样？再如你的客户报告了严重的bug，但是你的系统修复再上线需要花上几周甚至更长的时间，你觉得客户会有耐心等吗？迟反馈会让客户和股东蒙受损失，有时还是灾难性的。

	![image](/images/devops/build-closed-loop-feedback-arthitechture/cost-of-bugfix.png)

上图反映缺陷在软件生命周期过程中的修复成本，越靠近上游或者源头捕获并修复，成本越低，越到下游，成本呈指数级上升。本质上是说，缺陷反馈越迟，修复成本越高。

### 第二部分，产品创新闭环

Netflix云架构师Adrian Cockcroft在2014年的一次演讲中分享了Netflix持续规模化产品创新的概念模型―基于OODA环的持续交付，如下图所示，

![image](/images/devops/build-closed-loop-feedback-arthitechture/ooda.png)

1. 观察（Observe）：表示观察现状以发现潜在的创新点。Netflix鼓励员工勇于创新，任何人发现机会都可发起项目进行创新。比如，上图提到“客户痛点”，如果员工发现很多客户在网站上操作到某一步的时候都放弃了注册流程，那么他/她就可以调查其中原因，主动发起项目修复这个问题。

2. 判断（Orient）: 表示通过分析测量数据，来理解之前观察到的现象的背后原因。通常这涉及分析大量的数据（例如日志文件分析），通常也称为大数据分析。

3. 决策（Decide）: 指的是开发和执行一个项目计划。公司文化在决策一块是很重要的因素，在Netflix，公司鼓励自由和责任文化，员工将计划公开分享(Share plans)，不需要层层管理审批，就能主动发起变更项目。上图的JFDI表示Just F*cking Do It，强调推进力和执行力。

4. 行动（Act）: 指的是测试解决方案并将其部署到生产环境。Netflix采用基于云的微服务架构(MicroServices Architecture)，员工将包含增量功能的微服务发布到云环境，并开启A/B测试和之前版本做比对，基于数据判断新版本是否解决老版本的问题。

Netflix采用微服务架构体系，团队独立开发和维护各自负责的微服务，相互不干扰，一个微服务团队用1~2周的时间就可以完成一次OODA循环，可以说在业界是非常高的水平。

基于数据的闭环反馈是OODA环的核心，Cockcroft是这样说的：如果你的每一步都是基于充分的测量数据做出的行动，而你的竞争对手主要靠需要好几个月才能验证的猜测，那么你想不赢都难("it's hard not to win")。

在技术层面，Netflix通过大数据、微服务、云计算、自动化部署和A/B测试等手段，支持快速的创新和闭环反馈。


### 第三部分，组织闭环

大部分的研发型组织，主要基于专业分工和成本利用率考量，会采用如下图所示的严格职能型组织架构。

![image](/images/devops/build-closed-loop-feedback-arthitechture/functional-organization.png)

一个标准的软件研发流程，从产品经理先和用户体验/开发团队讨论新功能想法开始。开发团队再将想法实现为代码，之后代码被移交给测试团队和数据库管理团队，这中间涉及沟通和协调。最后产品上线又涉及和运维团队(系统、网络和存储等)的沟通和协调。

严格职能型组织很容易产生孤岛(silo)效应，或者说竖井效应，每个职能团队都想成为舞台中央的明星团队，各团队易各自为政和局部优化，所以严格职能组织有沟通开销大、研发流程缓慢和反馈效率低下问题。

有一些公司会更进一步，组建所谓基于产品线的跨职能团队负责整个端到端的研发活动，见下图：


![image](/images/devops/build-closed-loop-feedback-arthitechture/cross-funtion-organization.jpg)

跨职能团队有助于提升效率和强化反馈环，这个也是目前国内外主流互联网公司采用的组织模型。但只要团队基于单块(monolithic)应用的开发和交付模式，就难免产生跨团队间的移交、沟通和协调活动，整体效率仍然受限。


下面是Netflix所采用的基于微服务和PaaS平台的DevOps组织模型：

![image](/images/devops/build-closed-loop-feedback-arthitechture/netflix-devops-organization.png)

跨职能的产品团队基于可独立开发、测试和部署的微服务而组建，支持端到端的研发活动；平台团队则在AWS云的基础上提供PaaS基础服务平台，将微服务基础设施，发布和监控等基础能力封装在平台内，支持开发团队进行微服务的自助式(self-service)部署。

这个组织模型减少了组织间的孤岛，强化了团队内的反馈闭环，最大化了研发和交付的效率。当然，这个组织模型对技术能力和基础设施的要求更高，需要微服务架构体系、自动化部署和PaaS平台等技术手段的支撑。


### 第四部分，研发流程闭环

上十年，敏捷(agile)研发方法学得到长足进步和大范围推广，几乎每家技术型组织都在讲敏捷。

考虑到大部分同学已经对敏捷方法学耳熟能详，所以我这里不打算再多费口舌，只想强调一点：敏捷，不管是项目管理方面流行的scrum方法学，还是编码和质量方面的单元测试、持续集成等最佳实践，本质上是关于反馈的，不管采用哪种方法和实践，其核心是强化反馈闭环。

下图反映不同敏捷实践的反馈周期:

![image](/images/devops/build-closed-loop-feedback-arthitechture/agile-practice-feedback-cycle.png)

近期，随着沟通协作工具的兴起，比如知名的slack，出现了所谓chatops等新的DevOps实践，其核心是构建Dev和Ops之间的沟通反馈闭环，如下图所示：

![image](/images/devops/build-closed-loop-feedback-arthitechture/chatops.png)


上图中，整个软件交付生命周期过程中的重要事件，如代码提交，构建的成功和失败，构建包的上传/部署，生产系统的告警等，都被push到slack工具的不同渠道(channel)中，不同职责的DevOps成员通过关注不同的渠道来实时掌握和沟通研发进程和生产系统的健康状况。

该实践通过事件可视化和沟通反馈闭环让Dev和Ops更密切地协作，进一步提升研发效率。

### 第五部分，系统架构闭环

系统架构层面的闭环主要体现在系统监控方面，系统监控主要分为三个层次：

1. 系统层监控，监控底层硬件如CPU、网络和存储等的性能状况；

2. 应用层监控，监控应用性能如页面/服务调用计数，调用延迟，错误计数等；

3. 业务层监控，监控重要的业务指标如PV/UV，用户登录数和订单量等。

![image](/images/devops/build-closed-loop-feedback-arthitechture/ec-demo.png)



上图是一个假想的电商网站的分层架构图，

1. 底层第0层是运维基础设施层，可以基于私有云或者公有云，右边对应系统层次的监控反馈闭环；

2. 第1层是技术基础平台（中间件+框架）层，通常称为技术PaaS(Platform as a Service)；

3. 第2层是应用服务平台(SOA)层，通常也称为业务PaaS，第1和2层右边对应业务/应用/服务监控和大数据分析闭环反馈。

4. 第3层是用户体验和渠道，右边对应端用户体验监控和网站分析闭环反馈。

通过在每一层次构建监控和大数据分析等闭环反馈机制，整个系统可以在反馈数据的基础上不断地优化和改进。


### 第六部分，云计算、PaaS和微服务

互联网时代，企业在瞬息万变的市场赢得和保持竞争优势的核心在于持续创新。Netflix的成功实践告诉我们，一方面企业战略，文化，组织/团队，流程，架构对持续创新至关重要；另一方面像微服务，云计算和PaaS等技术手段，对持续创新和快速闭环起到基础性的支撑作用。

![image](/images/devops/build-closed-loop-feedback-arthitechture/traditional-development-model.png)

上图是典型的传统开发模式，其中硬件资源的审批、采购和安装配置，花上几周甚至几个月都是非常普遍的，造成研发效率低下，反馈速度缓慢。

![image](/images/devops/build-closed-loop-feedback-arthitechture/based-on-iaas-development-model-01.png)

![image](/images/devops/build-closed-loop-feedback-arthitechture/based-on-iaas-development-model-02.png)

上面两个图分别是基于IaaS的开发模式，和在IaaS开发模式下的团队协作模式，IaaS云支持硬件资源的快速自助式提供，可以将研发和反馈效率提升一个量级。但是，在中间件的安装配置、测试、发布和监控运维等环节仍然需要很多协调、移交和手工的重复性工作，研发和反馈的效率仍然受限。
![image](/images/devops/build-closed-loop-feedback-arthitechture/based-on-paas-development-model-01.png)

![image](/images/devops/build-closed-loop-feedback-arthitechture/based-on-paas-development-model-02.png)

上面两个图分别是基于PaaS的开发模式，和对应的团队协作模式，该模式将中间件、持续集成、发布和监控运维等基础能力自动化并封装在PaaS云平台中，可以支持研发人员的快速自助式部署，理想情况下研发人员可以做到想发就发，即达成快速的产品创新闭环。


在Netflix的微服务架构模式下，微服务是一个独立的开发，测试，发布和扩容单位，不同的团队可以互不干扰，独立的演化各自的微服务，这是一种自适应的和支持持续业务创新的架构风格。


微服务架构需要基础PaaS平台的支撑：将微服务管理(服务发现，配置，路由，容错和负载均衡)，持续集成和发布，监控和自动化运维等基础核心能力抽象、下沉并封装在平台内，让研发人员可以专注于微服务业务逻辑的实现，支持微服务的独立自助式部署，达成快速迭代和闭环反馈。
上图中，Gartner把这个基础平台称为外架构(Outer Architecture)，把居住在这个平台内的微服务架构称为内架构(Inner Architecture)。


![image](/images/devops/build-closed-loop-feedback-arthitechture/gartner-architechture.png)

### 第七部分，总结

1. 互联网以快制胜(speed wins in the marketplace)，企业的成功很大程度上取决于企业对客户需求的快速响应，换句话说，就是企业和客户之间能否形成良性正向和快速的闭环反馈，这个最大的反馈环又由众多子反馈环组成，包括产品创新、组织、流程和架构等各个环节，每一个子反馈环最终会直接或者间接的影响到企业和客户之间的闭环反馈。

2. 对闭环反馈的关注和投入，可以作为衡量一个优秀软件研发型公司的重要指标。同样，是否具备充分的闭环反馈意识，也是衡量一个优秀架构师的重要指标。

3. Lord Kelvin曾指出：如果你无法度量，你就无法提升，见下图：

	![image](/images/devops/build-closed-loop-feedback-arthitechture/lord-kelvin.png)

	在《架构即未来》一书中，作者马丁L.罗伯特也强调：管理意味着度量，失败的度量意味着失败的管理。同样，反馈必须基于测量数据，有反馈数据才能学习，有学习才能有提升。

4. 微服务，云计算和PaaS是支持持续业务创新和快速闭环反馈的支撑性技术架构手段。DevOps和持续交付是提升企业内外反馈机制的最佳实践，我常用下图来展示DevOps：

	![image](/images/devops/build-closed-loop-feedback-arthitechture/devops.png)

最后，所有的模型都是错误的，但是有一些是有用的。闭环反馈模型和意识非常重要和强大，但是在实践过程中要根据企业实际上下文(业务模式，规模，发展阶段，人才密度等等)灵活应用。



下面是本次分享引用的一些参考资料：

1. 凤凰项目：一个IT运维的传奇故事

2. [The Three Ways: The Principles Underpinning DevOps](http://itrevolution.com/the-three-ways-principles-underpinning-devops/)


3. 精益企业：高效能组织如何规模化创新

4. [Adopting microservices at Netflix: Lessons for team and process design](https://www.nginx.com/blog/adopting-microservices-at-netflix-lessons-for-team-and-process-design/)


5. [Adopting microservices at Netflix: Lessons for team and process design](https://www.nginx.com/blog/adopting-microservices-at-netflix-lessons-for-team-and-process-design/)


6. [MicroServices: Building services with guts on the outside](http://blogs.gartner.com/gary-olliffe/2015/01/30/microservices-guts-on-the-outside/)


7. [Agile Metrics in Action: Measuring and Enhancing the Performance of Agile Teams](https://www.amazon.com/Agile-Metrics-Action-Measuring-Performance/dp/1617292486/ref=pd_bxgy_14_img_2?ie=UTF8&psc=1&refRID=ZSED7D48J9JZ2WPSCC4B)


8. [架构即未来：现代企业可扩展的Web架构、流程和组织（原书第2版）](https://www.amazon.cn/%E6%9E%B6%E6%9E%84%E5%8D%B3%E6%9C%AA%E6%9D%A5-%E7%8E%B0%E4%BB%A3%E4%BC%81%E4%B8%9A%E5%8F%AF%E6%89%A9%E5%B1%95%E7%9A%84Web%E6%9E%B6%E6%9E%84-%E6%B5%81%E7%A8%8B%E5%92%8C%E7%BB%84%E7%BB%87-%E9%A9%AC%E4%B8%81L-%E9%98%BF%E4%BC%AF%E7%89%B9/dp/B01DXW29IM)
