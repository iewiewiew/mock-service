-- mysql -h127.0.0.1 -uroot -p123456
-- 创建数据库 drop database test_platform;
CREATE DATABASE IF NOT EXISTS test_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建数据表
-- truncate `test_platform`.`mock`;  drop table `test_platform`.`mock`
-- truncate `test_platform`.`alembic_version`;  drop table `test_platform`.`alembic_version`;
CREATE TABLE `test_platform`.`mock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `path` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `method` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `response_status` int NOT NULL,
  `response_body` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建数据表 truncate test_platform.projects; drop table test_platform.projects;
CREATE TABLE `projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入示例数据
INSERT INTO test_platform.project (name,description,created_at,updated_at) VALUES
	 ('示例项目1','',NOW(),NOW()),
	 ('示例项目2','',NOW(),NOW());

-- 插入示例数据
INSERT INTO test_platform.mock (name,`path`,`method`,response_status,response_body,description,project_id,created_at,updated_at) VALUES
 ('GET接口示例','/api/users','GET',200,'{"users": [{"id": 1}]}','','1',NOW(),NOW()),
 ('POST接口示例','/api/users','POST',201,'{"request_id":"{request.json.id}","req_str":"{request.json.req_str}","action":"{request.args.action}","email":"${email}","example":"示例"}','','1',NOW(),NOW()),
 ('PUT接口示例','/api/users/1','PUT',200,'{"request_id":"{request.json.id}","req_str":"{request.json.req_str}","action":"{request.args.action}","email":"${email}","example":"示例"}','','1',NOW(),NOW()),
 ('DELETE接口示例','/api/users/1','DELETE',204,'"delete success"','','1',NOW(),NOW()),
 ('随机数接口示例','/api/example','GET',200,'{"user":{"id":"${uuid}","name":"${name}","email":"${email}","phone":"${phone}","birthday":"${date[%Y-%m-%d,1990-01-01,2000-12-31]}","salary":"${float[5000,20000,2]}","address":"${address}","company":"${company}","avatar":"${image_url}"},"current_time":"${now}","current_date":"${now[%Y-%m-%d]}","timestamp":"${now[%Y%m%d%H%M%S]}"}','','1',NOW(),NOW());

-- 插入示例数据
INSERT INTO test_platform.mock (name,`path`,`method`,response_status,response_body,description,project_id,created_at,updated_at) VALUES
 ('获取用户列表','/api/users','GET',200,'{"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}','获取所有用户列表','1',NOW(),NOW()),
 ('创建新用户','/api/users','POST',201,'{"id": 3, "name": "New User"}','创建新用户','1',NOW(),NOW()),
 ('更新用户信息','/api/users/1','PUT',200,'{"id": 1, "name": "Updated Name"}','更新指定用户信息','1',NOW(),NOW()),
 ('删除用户','/api/users/1','DELETE',204,'','删除指定用户','1',NOW(),NOW()),
 ('获取产品列表','/api/products','GET',200,'{"products": [{"id": 101, "name": "Laptop"}]}','获取所有产品','1',NOW(),NOW()),
 ('创建新产品','/api/products','POST',201,'{"id": 102, "name": "Phone"}','创建新产品','1',NOW(),NOW()),
 ('更新产品信息','/api/products/101','PUT',200,'{"id": 101, "name": "Updated Laptop"}','更新指定产品信息','1',NOW(),NOW()),
 ('删除产品','/api/products/101','DELETE',204,'','删除指定产品','1',NOW(),NOW()),
 ('获取订单','/api/orders/1','GET',200,'{"id": 1, "total": 99.99}','获取指定订单详情','1',NOW(),NOW()),
 ('创建订单','/api/orders','POST',201,'{"id": 2, "status": "processing"}','创建新订单','1',NOW(),NOW()),
 ('更新订单状态','/api/orders/1','PATCH',200,'{"id": 1, "status": "shipped"}','更新订单状态','1',NOW(),NOW()),
 ('取消订单','/api/orders/1','DELETE',204,'','取消指定订单','1',NOW(),NOW()),
 ('用户登录','/api/auth/login','POST',200,'{"token": "abc123", "expires": 3600}','用户登录接口','1',NOW(),NOW()),
 ('用户登出','/api/auth/logout','POST',200,'{"message": "Logged out"}','用户登出接口','1',NOW(),NOW()),
 ('获取用户资料','/api/profile','GET',200,'{"name": "John Doe", "email": "john@example.com"}','获取当前用户资料','1',NOW(),NOW());

-- 插入示例数据
INSERT INTO test_platform.environment (id, name, base_url, description, parameter_count, created_at, updated_at, is_deleted) VALUES (1, 'Dev环境', 'http://www.dev.com', '开发环境', 0, NOW(), NOW(), 0);
INSERT INTO test_platform.environment (id, name, base_url, description, parameter_count, created_at, updated_at, is_deleted) VALUES (2, 'Test环境', 'http://www.test.com', '测试环境', 0, NOW(), NOW(), 0);

-- 插入示例数据
INSERT INTO test_platform.linux_info (id, server_name,host,port,username,password,private_key,description,created_at,updated_at) VALUES(1, '服务器示例','127.0.0.1',22,'root','123456','','',NOW(),NOW());

-- 插入示例数据 truncate test_platform.sql_templates;
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(1, '查询数据库', '显示所有数据库', 'show databases;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(2, '查询数据表', '显示当前数据库的所有表', 'show tables;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(3, '查询表结构', '显示表的字段信息', 'desc table_name;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(4, '查询表数据', '查询表中的所有数据', 'select * from table_name;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(5, '条件查询', '带条件的查询语句', 'select * from table_name where condition;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(6, '分页查询', '分页查询数据', 'select * from table_name limit 10 offset 0;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(7, '排序查询', '按字段排序查询', 'select * from table_name order by column_name desc;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(8, '插入数据', '插入单条数据', 'insert into table_name (col1, col2) values (value1, value2);', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(9, '批量插入', '批量插入多条数据', 'insert into table_name (col1, col2) values (value1, value2), (value3, value4);', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(10, '更新数据', '更新表中的数据', 'update table_name set column1 = value1 where condition;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(11, '删除数据', '删除表中的数据', 'delete from table_name where condition;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(12, '创建数据库', '创建新的数据库', 'create database db_name;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(13, '创建数据表', '创建新的数据表', 'create table table_name (id int primary key, name varchar(50));', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(14, '添加字段', '为表添加新字段', 'alter table table_name add column new_column varchar(100);', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(15, '删除表', '删除数据表', 'drop table table_name;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(16, '表连接查询', '多表连接查询', 'select a.*, b.* from table_a a join table_b b on a.id = b.a_id;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(17, '分组统计', '分组统计查询', 'select column, count(*) from table_name group by column;', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(18, '子查询', '使用子查询', 'select * from table_name where id in (select id from other_table);', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(19, '创建索引', '为表创建索引', 'create index idx_name on table_name(column_name);', '示例模板SQL', NOW(),NOW());
INSERT INTO test_platform.sql_templates (id, name, description, sql_content, category, created_at, updated_at) VALUES(20, '查询执行计划', '查看SQL执行计划', 'explain select * from table_name;', '示例模板SQL', NOW(),NOW());

INSERT INTO test_platform.examples (id, name, description, status, created_at, updated_at) VALUES(1, '示例名称1', '描述1', 'active', NOW(),NOW());
INSERT INTO test_platform.examples (id, name, description, status, created_at, updated_at) VALUES(2, '示例名称2', '描述2', 'inactive', NOW(),NOW());