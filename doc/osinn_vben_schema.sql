
DROP TABLE IF EXISTS `apscheduler_jobs`;
CREATE TABLE `apscheduler_jobs` (
  `id` varchar(191) NOT NULL,
  `next_run_time` double DEFAULT NULL,
  `job_state` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `tbl_job_group`;
CREATE TABLE `tbl_job_group` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) NOT NULL COMMENT '任务组名称',
  `created_by` bigint(20) NOT NULL COMMENT '创建人',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标记 0-存在；1-删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='任务调度任务组表';

DROP TABLE IF EXISTS `tbl_job_scheduler`;
CREATE TABLE `tbl_job_scheduler` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `job_group_id` bigint(20) DEFAULT NULL COMMENT '任务组ID',
  `job_id` varchar(100) NOT NULL COMMENT '任务唯一ID',
  `job_status` tinyint(1) NOT NULL DEFAULT '2' COMMENT '任务调度状态，1-运行，2-暂停',
  `trigger_type` tinyint(2) NOT NULL COMMENT '触发器类型：1-date、2-interval、3-cron',
  `trigger_condition` varchar(255) NOT NULL COMMENT '触发器触发条件',
  `remarks` varchar(255) NOT NULL DEFAULT '' COMMENT '备注',
  `author` varchar(64) NOT NULL DEFAULT '' COMMENT '作者',
  `alarm_email` varchar(255) DEFAULT NULL COMMENT '报警邮件',
  `executor_handler` varchar(255) NOT NULL COMMENT '执行器任务handler(调用函数名称)',
  `executor_param` varchar(512) DEFAULT NULL COMMENT '执行器任务参数',
  `created_by` bigint(20) NOT NULL COMMENT '创建人',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标记 0-存在；1-删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `idx_ job_id` (`job_id`)
) ENGINE=InnoDB COMMENT='任务调度信息组表';

DROP TABLE IF EXISTS `tbl_sys_config`;
CREATE TABLE `tbl_sys_config` (
  `id` bigint(20) NOT NULL COMMENT '主键',
  `config_group_name` varchar(255) NOT NULL DEFAULT '默认组' COMMENT '配置组名称',
  `config_name` varchar(128) DEFAULT NULL COMMENT '参数名称',
  `config_key` varchar(128) DEFAULT NULL COMMENT '参数键名',
  `config_value` varchar(512) DEFAULT NULL COMMENT '参数键值',
  `remarks` varchar(512) DEFAULT '' COMMENT '备注',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1正常；2-禁用',
  `is_default` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否系统默认账号1-默认，2-非默认',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标记 0-存在；1-删除',
  `created_by` bigint(20) DEFAULT NULL COMMENT '创建人',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='系统参数';

DROP TABLE IF EXISTS `tbl_sys_dept`;
CREATE TABLE `tbl_sys_dept` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `parent_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '父部门ID',
  `name` varchar(32) DEFAULT NULL COMMENT '部门名称',
  `ancestors` varchar(1024) DEFAULT NULL COMMENT '祖级列表',
  `org_type` tinyint(2) NOT NULL DEFAULT '1' COMMENT '机构类型 1公司；2部门；3小组；4其他',
  `leader` varchar(32) DEFAULT NULL COMMENT '负责人',
  `leader_phone` varchar(32) DEFAULT NULL COMMENT '负责人电话',
  `phone` varchar(32) DEFAULT NULL COMMENT '办公电话',
  `email` varchar(128) DEFAULT NULL COMMENT '邮箱',
  `post_code` varchar(32) DEFAULT NULL COMMENT '邮政编码',
  `address` varchar(512) DEFAULT NULL COMMENT '联系地址',
  `sort` int(11) DEFAULT NULL COMMENT '排序',
  `remarks` varchar(512) DEFAULT NULL COMMENT '备注',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1正常；2停用',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `created_by` bigint(20) DEFAULT NULL COMMENT '创建人',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='部门表';

DROP TABLE IF EXISTS `tbl_sys_dept_leader`;
CREATE TABLE `tbl_sys_dept_leader` (
  `id` bigint(20) NOT NULL COMMENT '主键',
  `dept_id` bigint(20) NOT NULL COMMENT '部门IDID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='部门领导关联表';

DROP TABLE IF EXISTS `tbl_sys_dept_post`;
CREATE TABLE `tbl_sys_dept_post` (
  `id` bigint(20) NOT NULL COMMENT '主键Id',
  `dept_id` bigint(20) NOT NULL COMMENT '部门Id',
  `post_id` bigint(20) NOT NULL COMMENT '岗位Id',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `created_by` bigint(20) NOT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_post_id` (`post_id`) USING BTREE,
  KEY `idx_dept_id` (`dept_id`) USING BTREE
) ENGINE=InnoDB COMMENT='部门岗位表';

DROP TABLE IF EXISTS `tbl_sys_dict`;
CREATE TABLE `tbl_sys_dict` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `dict_code` varchar(128) NOT NULL COMMENT '字典编码',
  `dict_name` varchar(128) NOT NULL COMMENT '字典名称',
  `remarks` varchar(512) DEFAULT NULL COMMENT '备注',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1-正常；2-停用',
  `is_default` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否默认：1-不是：2-默认',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `created_by` bigint(20) DEFAULT NULL COMMENT '创建人',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='字典表';

DROP TABLE IF EXISTS `tbl_sys_dict_item`;
CREATE TABLE `tbl_sys_dict_item` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `dict_id` bigint(20) NOT NULL COMMENT '字典ID',
  `dict_item_code` varchar(128) NOT NULL COMMENT '字典项编码',
  `dict_item_name` varchar(128) NOT NULL COMMENT '字典项名称',
  `sort` int(11) NOT NULL DEFAULT '0' COMMENT '排序',
  `remarks` varchar(512) NOT NULL DEFAULT '' COMMENT '备注',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1-启用；2-禁用',
  `is_default` tinyint(1) NOT NULL DEFAULT '2' COMMENT '是否默认，1-默认，2-非默认',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `created_by` bigint(20) NOT NULL COMMENT '创建人',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='字典项';

DROP TABLE IF EXISTS `tbl_sys_http_log`;
CREATE TABLE `tbl_sys_http_log` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL COMMENT '当前登录用户id',
  `account` varchar(20) DEFAULT NULL COMMENT '当前登录用户账号',
  `nickname` varchar(255) DEFAULT NULL COMMENT '当前登录用户昵称',
  `ip_address` varchar(50) DEFAULT NULL COMMENT 'IP地址',
  `ip_address_attr` varchar(100) DEFAULT NULL COMMENT 'IP地址归属地',
  `request_uri` varchar(255) DEFAULT NULL COMMENT '请求资源',
  `request_headers` varchar(30) DEFAULT NULL COMMENT '请求头',
  `request_params` text COMMENT '请求参数',
  `result_data` text COMMENT '响应数据',
  `request_method` varchar(30) NOT NULL COMMENT '请求类型：POST/GET',
  `class_method` varchar(255) DEFAULT NULL COMMENT '被调方法',
  `business_module` varchar(50) NOT NULL COMMENT '业务模块：业务模块主要是用在业务中台，区分业务，例如车辆模块、商城模块',
  `module_name` varchar(255) NOT NULL COMMENT '日志模块名称 业务模块下面的具体模块菜单-例如-用户管理',
  `source` varchar(50) NOT NULL COMMENT '日志来源',
  `log_type` varchar(50) NOT NULL COMMENT '日志类型',
  `action_desc` varchar(255) NOT NULL DEFAULT '' COMMENT '动作描述',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态,1-成功，2-失败',
  `operate_type` varchar(30) NOT NULL DEFAULT 'OTHER' COMMENT '操作类型，例如增删改查、登录',
  `execution_time` varchar(100) NOT NULL DEFAULT '0' COMMENT '执行耗时(毫秒单位)',
  `exception_msg` text COMMENT '异常信息',
  `browser` varchar(100) NOT NULL DEFAULT '' COMMENT '浏览器',
  `os` varchar(100) NOT NULL DEFAULT '' COMMENT '操作系统',
  `mobile` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否是移动端请求，1-是，2-不是',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `index_log` (`user_id`,`account`,`nickname`,`business_module`,`source`,`log_type`,`module_name`,`status`)
) ENGINE=InnoDB COMMENT='系统请求日志';

DROP TABLE IF EXISTS `tbl_sys_menu`;
CREATE TABLE `tbl_sys_menu` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `type` varchar(32) DEFAULT NULL COMMENT '菜单类型 dir目录；menu菜单；button按钮',
  `name` varchar(128) DEFAULT NULL COMMENT '菜单名称',
  `parent_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '上级菜单',
  `path` varchar(512) DEFAULT NULL COMMENT '路由地址',
  `redirect` varchar(255) DEFAULT NULL,
  `component` varchar(512) DEFAULT NULL COMMENT '组件路径',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1正常；2停用',
  `auth_code` varchar(128) DEFAULT NULL COMMENT '权限标识',
  `sort` int(11) NOT NULL DEFAULT '1' COMMENT '排序',
  `remarks` varchar(512) DEFAULT NULL COMMENT '备注',
  `meta` text,
  `created_by` bigint(20) DEFAULT NULL COMMENT '创建人',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='菜单表 ';

DROP TABLE IF EXISTS `tbl_sys_post`;
CREATE TABLE `tbl_sys_post` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `post_code` varchar(128) DEFAULT NULL COMMENT '岗位编码',
  `name` varchar(128) DEFAULT NULL COMMENT '岗位名称',
  `remarks` varchar(512) DEFAULT NULL COMMENT '备注',
  `sort` int(11) NOT NULL DEFAULT '1' COMMENT '排序',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态 0正常；1停用',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `created_by` bigint(20) DEFAULT NULL COMMENT '创建人',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='岗位表';

DROP TABLE IF EXISTS `tbl_sys_role`;
CREATE TABLE `tbl_sys_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_code` varchar(128) NOT NULL COMMENT '角色编码',
  `name` varchar(128) NOT NULL COMMENT '角色名称',
  `remarks` varchar(512) NOT NULL DEFAULT '' COMMENT '备注',
  `sort` int(11) NOT NULL DEFAULT '1' COMMENT '排序',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1-正常；2-停用',
  `is_default` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否系统默认角色，1-默认，2-非默认',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除',
  `created_by` bigint(20) NOT NULL COMMENT '创建人',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='角色表';

DROP TABLE IF EXISTS `tbl_sys_role_menu`;
CREATE TABLE `tbl_sys_role_menu` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `menu_id` bigint(20) NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='角色菜单表';

DROP TABLE IF EXISTS `tbl_sys_user`;
CREATE TABLE `tbl_sys_user` (
  `id` bigint(20) NOT NULL COMMENT '主键',
  `account` varchar(128) DEFAULT NULL COMMENT '账号',
  `password` varchar(128) DEFAULT NULL COMMENT '密码',
  `psw_modified` tinyint(1) NOT NULL DEFAULT '0' COMMENT '修改密码标记 1未修改；2已修改',
  `nickname` varchar(128) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(128) DEFAULT NULL COMMENT '头像',
  `email` varchar(128) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(32) DEFAULT NULL COMMENT '手机号',
  `staff_number` varchar(32) DEFAULT NULL COMMENT '工号',
  `birthday` datetime DEFAULT NULL COMMENT '生日',
  `sex` tinyint(4) DEFAULT NULL COMMENT '性别 1-男；2-女；3未知',
  `dept_id` bigint(20) DEFAULT NULL COMMENT '部门ID',
  `lock_account` tinyint(4) NOT NULL DEFAULT '0' COMMENT '锁定标记 1正常；2锁定',
  `sort` int(11) NOT NULL DEFAULT '0' COMMENT '排序',
  `remarks` varchar(512) DEFAULT NULL COMMENT '备注',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态1正常；2停用',
  `is_default` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否系统默认账号，1-默认，2-非默认',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标记 0-存在；1-删除',
  `created_by` bigint(20) DEFAULT NULL COMMENT '创建人',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='用户表';

DROP TABLE IF EXISTS `tbl_sys_user_post`;
CREATE TABLE `tbl_sys_user_post` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `post_id` bigint(20) NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='用户岗位表';

DROP TABLE IF EXISTS `tbl_sys_user_role`;
CREATE TABLE `tbl_sys_user_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='用户角色表';