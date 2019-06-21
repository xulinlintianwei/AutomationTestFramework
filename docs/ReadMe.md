## 环境
- Python 3.6.4
- selenium 2.53
- PyYaml
- xlrd
- requests
- JMESPath
- Faker
## 框架工程目录说明
1、config 目录：存放全局的配置文件，如框架中的：config.yaml
2、utils 目录：存放公共封装好的库，如处理日志相关的模块（）、操作mysql数据库的模块（）、读写excel的模块等
3、data 目录：用来存放数据驱动框架以及关键字驱动框架要用的数据文件
4、log 目录：存放框架运行日志文件的目录
5、report：用来存放运行生成HTML格式报告的目录
6、pom：用来存放根据项目需要封装的页面操作的包目录
7、actionword：用来存放根据项目需要封装好的关键字的包目录
8、testsuite：用来存放项目测试套需要的包目录
9、runner：最后用来整体运行项目的包目录
10、docs：用来存放跟此框架相关的文档介绍的目录

11、testtempdir：调试框架相关技术写的临时代码目录
12、basic：要熟悉此框架需要具备的基础知识相关代码存放目录
13、interfacetest：接口测试相关框架与代码目录
14、performancetest：性能测试相关框架与代码目录
16、andriod：android测试相关框架与代码目录
17、kdd_ddt_bdd：关键字驱动-数据驱动-业务流程驱动整合框架包目录
