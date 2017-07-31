
# CREATE

示例`create database test`

```
CREATE [TEMPORARY] TABLE [IF NOT EXISTS] tbl_name

   [(create_definition,...)]

   [table_options] [select_statement]
```

示例`create table test.aaa(id int(8),name char(20));`


# INSERT
```
INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name [(col_name,...)]
    VALUES ({expr | DEFAULT},...),(...),...
    [ ON DUPLICATE KEY UPDATE col_name=expr, ... ]
或：

INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    SET col_name={expr | DEFAULT}, ...
    [ ON DUPLICATE KEY UPDATE col_name=expr, ... ]
或：

INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name [(col_name,...)]
    SELECT ...
    [ ON DUPLICATE KEY UPDATE col_name=expr, ... ]
```

示例`insert into test.aaa values (1,"bigking");`

## UPDATE
```
UPDATE [LOW_PRIORITY] [IGNORE] tbl_name  
SET col_name1=expr1 [, col_name2=expr2 ...]  
[WHERE where_definition]  
[ORDER BY ...]  
[LIMIT row_count]
```

示例`update update test.aaa set name='Bigking' where id=1;`

# 查看权限
示例`show grants for 'abc'@'def'`
