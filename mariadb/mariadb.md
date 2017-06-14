


# 配置文件
读取多处的多个配置文件，而且会以指定的次序的进行；

```
# my_print_defaults
Default options are read from the following files in the given order:
/etc/mysql/my.cnf  /etc/my.cnf ~/.my.cnf
```

不同的配置文件中出现同一参数且拥有不同值时，后读取将为最终生效值；

修改默认读取的配置文件（mysqld_safe命令）：`--defaults-file=file_name`

于读取的默认配置文件之外再加载一个文件：	`--defaults-extra-file=path`

配置文件格式：ini风格的配置文件，能够为mysql的各种应用程序提供配置信息：

```
[mysqld]
[mysqld_safe]
[mysqld_multi]
[server]
[mysql]
[mysqldump]
[client]
...

PARAMETER = VALUE

PARAMETER：
innodb_file_per_table
innodb-file-per-table
```

# mysql命令

mysql [options] db_name

常用选项：

```
--host=host_name, -h host_name：服务端地址；
--user=user_name, -u user_name：用户名；
--password[=password], -p[password]：用户密码；
--port=port_num, -P port_num：服务端端口；
--protocol={TCP|SOCKET|PIPE|MEMORY}：
本地通信：基于本地回环地址进行请求，将基于本地通信协议；
Linux：SOCKET
Windows：PIPE，MEMORY
非本地通信：使用非本地回环地址进行的请求； TCP协议；
--socket=path, -S path
--database=db_name, -D db_name：
--compress, -C：数据压缩传输
--execute=statement, -e statement：非交互模式执行SQL语句；
--vertical, -E：查询结果纵向显示；
```

mysql命令的使用帮助：`man mysql` `mysql  --help  --verbose`

sql脚本运行：`mysql [options] [DATABASE] < /PATH/FROM/SOME_SQL_SCRIPT`

# mysqld服务器程序：

服务器参数/变量：显示MySQL的运行特性；`mysql> SHOW [GLOBAL | SESSION] VARIABLES [like_or_where];`

状态（统计）参数/变量：保存MySQL运行过程中的统计数据或状态数据；`mysql> SHOW [GLOBAL | SESSION] STATUS [like_or_where];`

显示单个变量设定值的方法：`mysql> SELECT @@[global.|session.]system_var_name`

```
%：匹配任意长度的任意字符；
_：匹配任意单个字符；

变量/参数级别：
全局：为所有会话设定默认；
会话：跟单个会话相关；会话建立会从全局继承；
```

## 服务器变量的调整方式：

运行时修改：

global：仅对修改后新建立的会话有效；session：仅对当前会话有效，且立即生效；

通过配置文件修改：

重启后生效；

运行时修改服务器变量值操作方法：

```
mysql> HELP SET

SET [GLOBAL | SESSION] system_var_name = expr
SET [@@global. | @@session. | @@]system_var_name = expr
```

安装完成后的安全初始化：`mysql_secure_installation`

运行前常修改的参数：

```
innodb_file_per_table=ON
skip_name_resolve=ON
sql_safe_updates=ON
...
```

# MySQL的数据类型：

## 字符型：

CHAR(#)， BINARY(#)：定长型；CHAR不区分字符大小写，而BINARY区分；

VARCHAR(#)， VARBINARY(#)：变长型

TEXT：TINYTEXT，TEXT，MEDIUMTEXT，LONGTEXT

BLOB：TINYBLOB，BLOB，MEDIUMBLOB， LONGBLOB

Binary Large OBject

## 数值型：

### 浮点型：近似

FLOAT

DOUBLE

REAL

BIT

### 整型：精确
INTEGER：TINYINT，SMALLINT，MEDIUMINT，INT，BIGINT
DECIMAL

## 日期时间型：
日期：DATE

时间：TIME

日期j时间：DATETIME

时间戳：TIMESTAMP

年份：YEAR(2), YEAR(4)

## 内建：
ENUM：枚举`ENUM('Sun','Mon','Tue','Wed')`

SET：集合

# 类型修饰符：
字符型：NOT NULL，NULL，DEFALUT ‘STRING’，CHARACET SET ‘CHARSET’，COLLATION ‘collocation'

整型：NOT NULL， NULL， DEFALUT value, AUTO_INCREMENT, UNSIGNED

日期时间型：NOT NULL， NULL， DEFAULT `help 'Data Types'`

# SQL MODE：定义mysqld对约束等违反时的响应行为等设定；

常用的MODE：

```
TRADITIONAL
STRICT_TRANS_TABLES
STRICT_ALL_TABLES
```

修改方式：

```
mysql> SET GLOBAL sql_mode='MODE';
mysql> SET @@global.sql_mode='MODE';
```

# SQL：DDL，DML
DDL：Data Defination Language`mysql> HELP Data Definition`

```
CREATE, ALTER, DROP
DATABASE, TABLE
INDEX, VIEW, USER
FUNCTION, FUNCTION UDF, PROCEDURE, TABLESPACE, TRIGGER, SERVER
```

DML: Data Manipulation Language`mysql> HELP Data Manipulation`

```
INSERT/REPLACE, DELETE, SELECT, UPDATE
```

## 数据库：

CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name CHARACTER SET [=] charset_name  COLLATE [=] collation_name

ALTER {DATABASE | SCHEMA} [db_name] CHARACTER SET [=] charset_name  COLLATE [=] collation_name

DROP {DATABASE | SCHEMA} [IF EXISTS] db_name

## 表：

### CREATE

  * CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name (create_definition,...) [table_options] [partition_options]

  CREATE TABLE [IF NOT EXISTS] tble_name (col_name  data_typ|INDEX|CONSTRAINT);

  table_options：
  ENGINE [=] engine_name

  查看支持的所有存储引擎：`mysql> SHOW ENGINES;`

  查看指定表的存储引擎：`mysql> SHOW TABLE STATUS LIKE clause;`

  ROW_FORMAT [=] {DEFAULT|DYNAMIC|FIXED|COMPRESSED|REDUNDANT|COMPACT}

* CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name [(create_definition,...)] [table_options] [partition_options] select_statement

  直接创建表，并将查询语句的结果插入到新创建的表中；

* (3) CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name { LIKE old_tbl_name | (LIKE old_tbl_name) }

  复制某存在的表的结构来创建新的空表；

### DROP
DROP [TEMPORARY] TABLE [IF EXISTS] tbl_name [, tbl_name];

### ALTER
ALTER  TABLE tbl_name
[alter_specification [, alter_specification] ...]

可修改内容：

* table_options
* 添加定义：ADD
字段、字段集合、索引、约束
* 修改字段：
	CHANGE [COLUMN] old_col_name new_col_name column_definition [FIRST|AFTER col_name]
	MODIFY [COLUMN] col_name column_definition [FIRST | AFTER col_name]
* 删除操作：DROP
	字段、索引、约束

### 表重命名
RENAME [TO|AS] new_tbl_name

查看表结构定义：`DESC tbl_name;`

查看表定义：`SHOW CREATE TABLE tbl_name`

查看表属性信息：`SHOW TABLE STATUS [{FROM | IN} db_name] [LIKE 'pattern' | WHERE expr]`

## 索引：数据结构
创建：`CREATE [UNIQUE|FULLTEXT|SPATIAL] INDEX index_name [index_type] ON tbl_name (index_col_name,...)`

查看：`SHOW {INDEX | INDEXES | KEYS} {FROM | IN} tbl_name [{FROM | IN} db_name] [WHERE expr]`

删除：`DROP  INDEX index_name ON tbl_name`

索引类型：

```
聚集索引、非聚集索引：索引是否与数据存在一起；
主键索引、辅助索引
稠密索引、稀疏索引：是否索引了每一个数据项；
BTREE（B+）、HASH、R Tree、FULLTEXT
BTREE：左前缀；
```

EXPLAIN：分析查询语句的执行路径；

## 视图：VIEW
虚表：存储下来的SELECT语句；

创建：`CREATE  VIEW view_name [(column_list)] AS select_statement`

修改：
`ALTER  VIEW view_name [(column_list)] AS select_statement`

删除：`DROP VIEW [IF EXISTS] view_name [, view_name] ...`

# DML
INSERT/REPLACE，DELETE，UPDATE，SELECT

## INSERT：
单行插入,批量插入

INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
[INTO] tbl_name [(col_name,...)]
{VALUES | VALUE} ({expr | DEFAULT},...),(...),...
[ ON DUPLICATE KEY UPDATE
col_name=expr
[, col_name=expr] ... ]

示例`insert classes (Class,NumOfStu) value ('Taiji Men',6);`

Or:

INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
[INTO] tbl_name
SET col_name={expr | DEFAULT}, ...
[ ON DUPLICATE KEY UPDATE
col_name=expr
[, col_name=expr] ... ]

示例`insert classes set Class='Qitian',NumOfStu=10;`

Or:

INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
[INTO] tbl_name [(col_name,...)]
SELECT ...
[ ON DUPLICATE KEY UPDATE
col_name=expr
[, col_name=expr] ... ]

示例`INSERT INTO db1_name (field1,field2) SELECT field1,field2 FROM db2_name;`

## DELETE

DELETE  FROM tbl_name [WHERE where_condition] [ORDER BY ...] [LIMIT row_count]		

示例`delete from classes where Class='Taiji Men' and NumOfStu='6';`

注意：一定要有限制条件，否则将清空整个表；

限制条件：

[WHERE where_condition]

[ORDER BY ...] [LIMIT row_count]

## UPDATE：

UPDATE table_reference SET col_name1={expr1|DEFAULT} [, col_name2={expr2|DEFAULT}] ...
[WHERE where_condition]
[ORDER BY ...]
[LIMIT row_count]				

示例`update classes set NumOfStu='5' where class='Shaolin Pai';`

***注意：一定要有限制条件，否则将修改整个表中指定字段的数据***

限制条件：

[WHERE where_condition]

[ORDER BY ...] [LIMIT row_count]


注意：sql_safe_updates变量可阻止不带条件更新操作；

## SELECT：

Query Cache：缓存查询的执行结果；

key：查询语句的hash值；

value：查询语句的执行结果；

SQL语句的编写方式：`SELECT name FROM tbl2;` `select name from tbl2;`

查询执行路径：

```
请求-->查询缓存：命中后返回；
请求-->查询缓存-->解析器-->预处理器-->优化器-->查询执行引擎-->存储引擎-->缓存-->响应
```

SELECT语句的执行流程：

```
FROM  --> WHERE --> Group By --> Having --> Order BY --> SELECT --> Limit
```

### 单表查询：

SELECT
[ALL | DISTINCT | DISTINCTROW ]
[SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
select_expr [, select_expr ...]
[FROM table_references
[WHERE where_condition]
[GROUP BY {col_name | expr | position}
[ASC | DESC], ... [WITH ROLLUP]]
[HAVING where_condition]
[ORDER BY {col_name | expr | position}
[ASC | DESC], ...]
[LIMIT {[offset,] row_count | row_count OFFSET offset}]

用法：

SELECT col1, col2, ... FROM tble_name；

SELECT col1, col2, ... FROM tble_name WHERE clause；

SELECT col1, col2, ... FROM tble_name  [WHERE clause] GROUP BY col_name [HAVING clause]；

分组的目的在于聚合计算：avg, max, min, count, sum,

`DISTINCT`数据去重；

`SQL_CACHE`显式指定缓存查询语句的结果；

`SQL_NO_CACHE`显式指定不缓存查询语句的结果；

query_cache_type服务器变量有三个值：

```
ON：启用；
SQL_NO_CACHE：不缓存；默认符合缓存条件都缓存；
OFF：关闭；
DEMAND：按需缓存；
SQL_CACHE：缓存；默认不缓存；
```

字段可以使用别名 ：`col1 AS alias1, col2 AS alias2, ...`

* WHERE子句：指明过滤条件以实现“选择”功能；

  过滤条件：布尔型表达式；`[WHERE where_condition]``

  算术操作符：`+, -, *, /, %`

  比较操作符：`=, <>, !=, <=>, >, >=, <, <=`

  IS NULL， IS NOT NULL

  区间：BETWEEN min AND max

  IN：列表；

  LIKE：模糊比较，%和_；

  RLIKE或REGEXP

逻辑操作符：`AND， OR， NOT， XOR`

GROUP BY：根据指定的字段把查询的结果进行“分组”以用于“聚合”运算；`avg(), max(), min(), sum(), count()`

`HAVING`对分组聚合后的结果进行条件过滤；

`ORDER BY`根据指定的字段把查询的结果进行排序；升序：`ASC`；`降序：DESC`

`LIMIT`对输出结果进行数量限制`[LIMIT {[offset,] row_count | row_count OFFSET offset}]`


## 多表查询
连接操作：

```
交叉连接：笛卡尔乘积；
内连接：
等值连接：让表之间的字段以等值的方式建立连接；
不等值连接：
自然连接
自连接
外连接：
左外连接：`FROM tb1 LEFT JOIN tb2 ON tb1.col = tb2.col`
右外连接：`FROM tb1 RIGHT JOIN tb2 ON tb1.col = tb2.col`
```

# 子查询：在查询中嵌套查询

用于WHERE子句中的子查询；

* 用于比较表达式中的子查询：子查询仅能返回单个值；
* 用于IN中的子查询：子查询可以返回一个列表值；
* 用于EXISTS中的子查询：

用于FROM子句中的子查询；`SELECT tb_alias.col1, ... FROM (SELECT clause) AS tb_alias WHERE clause;`

## 联合查询：将多个查询语句的执行结果相合并

UNION`SELECT clause UNION SELECT cluase；`
