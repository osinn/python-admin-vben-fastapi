/*
 Navicat Premium Dump SQL

 Source Server         : 50-3306
 Source Server Type    : MySQL
 Source Server Version : 50744 (5.7.44)
 Source Host           : 192.168.1.50:3306
 Source Schema         : osinn_vben

 Target Server Type    : MySQL
 Target Server Version : 50744 (5.7.44)
 File Encoding         : 65001

 Date: 20/01/2026 18:12:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for apscheduler_jobs
-- ----------------------------
DROP TABLE IF EXISTS `apscheduler_jobs`;
CREATE TABLE `apscheduler_jobs` (
  `id` varchar(191) NOT NULL,
  `next_run_time` double DEFAULT NULL,
  `job_state` blob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of apscheduler_jobs
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tbl_job_group
-- ----------------------------
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务调度任务组表';

-- ----------------------------
-- Records of tbl_job_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tbl_job_scheduler
-- ----------------------------
DROP TABLE IF EXISTS `tbl_job_scheduler`;
CREATE TABLE `tbl_job_scheduler` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `job_group_id` bigint(20) DEFAULT NULL COMMENT '任务组ID',
  `job_id` varchar(100) NOT NULL COMMENT '任务唯一ID',
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
) ENGINE=InnoDB AUTO_INCREMENT=3124187126015553543 DEFAULT CHARSET=utf8mb4 COMMENT='任务调度信息组表';

-- ----------------------------
-- Records of tbl_job_scheduler
-- ----------------------------
BEGIN;
INSERT INTO `tbl_job_scheduler` (`id`, `job_group_id`, `job_id`, `trigger_type`, `trigger_condition`, `remarks`, `author`, `alarm_email`, `executor_handler`, `executor_param`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (3122738231347605510, 1, 'apps.modules.sys.scheduler.job.demo_job.sync_job', 3, '{\n  \"cron_expr\": \"*/1 * * * *\"\n}', '', 'Default author', '', 'sync_job', '{\n  \"x\": 3\n}', 1401043674048851970, '2026-01-13 01:01:45', NULL, '2026-01-14 01:01:03', 0);
INSERT INTO `tbl_job_scheduler` (`id`, `job_group_id`, `job_id`, `trigger_type`, `trigger_condition`, `remarks`, `author`, `alarm_email`, `executor_handler`, `executor_param`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (3124187126015553542, NULL, 'apps.modules.sys.scheduler.job.demo_job2.sync_job', 2, '{\n  \"seconds\": 3\n}', '', 'Default author', '', 'sync_job', '{\n  \"x\": 3\n}', -1, '2026-01-14 01:01:05', NULL, NULL, 0);
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_config
-- ----------------------------
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统参数';

-- ----------------------------
-- Records of tbl_sys_config
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_config` (`id`, `config_group_name`, `config_name`, `config_key`, `config_value`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3121727503891263494, '默认', '系统默认密码', 'password', '123456', 'asd', 1, 1, 0, 1401043674048851970, '2026-01-12 08:17:41', 1401043674048851970, '2026-01-16 06:24:58');
INSERT INTO `tbl_sys_config` (`id`, `config_group_name`, `config_name`, `config_key`, `config_value`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3127412782383853574, '默认', 'demo', 'vn', '11', 'as', 1, 2, 0, 1401043674048851970, '2026-01-16 06:25:30', 1401043674048851970, '2026-01-16 08:37:40');
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_dept
-- ----------------------------
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
) ENGINE=InnoDB AUTO_INCREMENT=3131966756525010951 DEFAULT CHARSET=utf8mb4 COMMENT='部门表';

-- ----------------------------
-- Records of tbl_sys_dept
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_dept` (`id`, `parent_id`, `name`, `ancestors`, `org_type`, `leader`, `leader_phone`, `phone`, `email`, `post_code`, `address`, `sort`, `remarks`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1406955981362733058, 0, '总部', '0', 1, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, 1, 0, 1401043674048851970, '2022-01-01 00:00:00', NULL, '2021-08-03 16:54:12');
INSERT INTO `tbl_sys_dept` (`id`, `parent_id`, `name`, `ancestors`, `org_type`, `leader`, `leader_phone`, `phone`, `email`, `post_code`, `address`, `sort`, `remarks`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1406957304434958338, 1406955981362733058, '科技公司', '0,1406955981362733058', 1, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, 1, 0, 1401043674048851970, '2022-01-01 00:00:00', NULL, '2021-08-03 16:54:12');
INSERT INTO `tbl_sys_dept` (`id`, `parent_id`, `name`, `ancestors`, `org_type`, `leader`, `leader_phone`, `phone`, `email`, `post_code`, `address`, `sort`, `remarks`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1406957570110562306, 1406957304434958338, '研发部研发部研发部研发部研发部研发部', '0,1406955981362733058,1406957304434958338', 2, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, 1, 0, 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2022-01-01 00:00:00');
INSERT INTO `tbl_sys_dept` (`id`, `parent_id`, `name`, `ancestors`, `org_type`, `leader`, `leader_phone`, `phone`, `email`, `post_code`, `address`, `sort`, `remarks`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1406957672636129281, 1406957304434958338, '测试部', '0,1406955981362733058,1406957304434958338', 2, '张三', NULL, NULL, NULL, NULL, NULL, 1, NULL, 1, 0, 1401043674048851970, '2022-01-01 00:00:00', NULL, '2021-08-03 16:54:12');
INSERT INTO `tbl_sys_dept` (`id`, `parent_id`, `name`, `ancestors`, `org_type`, `leader`, `leader_phone`, `phone`, `email`, `post_code`, `address`, `sort`, `remarks`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1918556212432396290, 0, '演示13', '0', 1, NULL, NULL, NULL, NULL, NULL, NULL, 2, 'asddsd', 1, 0, 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2026-01-19 09:28:20');
INSERT INTO `tbl_sys_dept` (`id`, `parent_id`, `name`, `ancestors`, `org_type`, `leader`, `leader_phone`, `phone`, `email`, `post_code`, `address`, `sort`, `remarks`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3131966756525010950, 0, '演示2', NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, 1, 'as', 1, 1, 1401043674048851970, '2026-01-19 09:49:28', 1401043674048851970, '2026-01-19 09:52:26');
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_dept_leader
-- ----------------------------
DROP TABLE IF EXISTS `tbl_sys_dept_leader`;
CREATE TABLE `tbl_sys_dept_leader` (
  `id` bigint(20) NOT NULL COMMENT '主键',
  `dept_id` bigint(20) NOT NULL COMMENT '部门IDID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='部门领导关联表';

-- ----------------------------
-- Records of tbl_sys_dept_leader
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_dept_leader` (`id`, `dept_id`, `user_id`) VALUES (3131945483988201478, 1918556212432396290, 1401043674048851970);
INSERT INTO `tbl_sys_dept_leader` (`id`, `dept_id`, `user_id`) VALUES (3131945484021755910, 1918556212432396290, 3115958858976161798);
INSERT INTO `tbl_sys_dept_leader` (`id`, `dept_id`, `user_id`) VALUES (3131966929900761094, 3131966756525010950, 1401043674048851970);
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_dept_post
-- ----------------------------
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='部门岗位表';

-- ----------------------------
-- Records of tbl_sys_dept_post
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_dept_post` (`id`, `dept_id`, `post_id`, `created_time`, `created_by`) VALUES (1931740559339597825, 1406955981362733059, 1407222184903786498, '2025-06-08 23:50:14', 1401043674048851970);
INSERT INTO `tbl_sys_dept_post` (`id`, `dept_id`, `post_id`, `created_time`, `created_by`) VALUES (1931740559339597826, 1406955981362733059, 1407219533063471106, '2025-06-08 23:50:14', 1401043674048851970);
INSERT INTO `tbl_sys_dept_post` (`id`, `dept_id`, `post_id`, `created_time`, `created_by`) VALUES (1931757388086779906, 1406955981362733058, 1407222184903786498, '2025-06-09 00:57:06', 1401043674048851970);
INSERT INTO `tbl_sys_dept_post` (`id`, `dept_id`, `post_id`, `created_time`, `created_by`) VALUES (1932074911617421314, 1406957570110562306, 1407222184903786498, '2025-06-09 21:58:50', 1401043674048851970);
INSERT INTO `tbl_sys_dept_post` (`id`, `dept_id`, `post_id`, `created_time`, `created_by`) VALUES (1932074911630004225, 1406957570110562306, 1407219533063471106, '2025-06-09 21:58:50', 1401043674048851970);
INSERT INTO `tbl_sys_dept_post` (`id`, `dept_id`, `post_id`, `created_time`, `created_by`) VALUES (3131958255895539718, 1918556212432396290, 1407222184903786498, '2026-01-19 09:41:01', 1401043674048851970);
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_dict
-- ----------------------------
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
) ENGINE=InnoDB AUTO_INCREMENT=1401570456897892355 DEFAULT CHARSET=utf8mb4 COMMENT='字典表';

-- ----------------------------
-- Records of tbl_sys_dict
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_dict` (`id`, `dict_code`, `dict_name`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1401570456897892354, 'sys_del_flag', '删除标志', NULL, 2, 2, 1, 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2026-01-19 03:14:55');
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_dict_item
-- ----------------------------
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
) ENGINE=InnoDB AUTO_INCREMENT=3131547569293979655 DEFAULT CHARSET=utf8mb4 COMMENT='字典项';

-- ----------------------------
-- Records of tbl_sys_dict_item
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_dict_item` (`id`, `dict_id`, `dict_item_code`, `dict_item_name`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1401571842909888513, 1401570456897892354, '2', '存在', 2, '', 1, 2, 1, 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2026-01-19 02:57:59');
INSERT INTO `tbl_sys_dict_item` (`id`, `dict_id`, `dict_item_code`, `dict_item_name`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3131547569293979654, 1401570456897892354, '2', 'demo', 1, '', 1, 2, 1, 1401043674048851970, '2026-01-19 02:53:02', NULL, '2026-01-19 02:57:02');
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_http_log
-- ----------------------------
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统请求日志';

-- ----------------------------
-- Records of tbl_sys_http_log
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_http_log` (`id`, `user_id`, `account`, `nickname`, `ip_address`, `ip_address_attr`, `request_uri`, `request_headers`, `request_params`, `result_data`, `request_method`, `class_method`, `business_module`, `module_name`, `source`, `log_type`, `action_desc`, `status`, `operate_type`, `execution_time`, `exception_msg`, `browser`, `os`, `mobile`, `created_time`) VALUES (3133418673658753030, NULL, 'admin', NULL, '127.0.0.1', NULL, '/api/auth/login', NULL, NULL, NULL, 'POST', NULL, '用户登录', '用户登录', 'WEB', 'LOGIN', '用户登录', 2, '用户登录', '0:2.3', NULL, 'Chrome', 'Mac OS X', 0, '2026-01-20 09:51:49');
INSERT INTO `tbl_sys_http_log` (`id`, `user_id`, `account`, `nickname`, `ip_address`, `ip_address_attr`, `request_uri`, `request_headers`, `request_params`, `result_data`, `request_method`, `class_method`, `business_module`, `module_name`, `source`, `log_type`, `action_desc`, `status`, `operate_type`, `execution_time`, `exception_msg`, `browser`, `os`, `mobile`, `created_time`) VALUES (3133420233704960006, NULL, 'admin', NULL, '127.0.0.1', NULL, '/api/auth/login', NULL, NULL, NULL, 'POST', NULL, '用户登录', '用户登录', 'WEB', 'LOGIN', '用户登录', 2, '用户登录', '0:2.54', NULL, 'Chrome', 'Mac OS X', 0, '2026-01-20 09:53:22');
INSERT INTO `tbl_sys_http_log` (`id`, `user_id`, `account`, `nickname`, `ip_address`, `ip_address_attr`, `request_uri`, `request_headers`, `request_params`, `result_data`, `request_method`, `class_method`, `business_module`, `module_name`, `source`, `log_type`, `action_desc`, `status`, `operate_type`, `execution_time`, `exception_msg`, `browser`, `os`, `mobile`, `created_time`) VALUES (3133425353624743942, NULL, 'admin', NULL, '127.0.0.1', NULL, '/api/auth/login', NULL, NULL, NULL, 'POST', NULL, '用户登录', '用户登录', 'WEB', 'LOGIN', '用户登录', 1, '用户登录', '0:0.28', NULL, 'Chrome', 'Mac OS X', 0, '2026-01-20 09:58:27');
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_menu
-- ----------------------------
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
) ENGINE=InnoDB AUTO_INCREMENT=3133052898641014791 DEFAULT CHARSET=utf8mb4 COMMENT='菜单表 ';

-- ----------------------------
-- Records of tbl_sys_menu
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1406063931784179714, 'menu', '首页', 0, '/analytics', NULL, '/dashboard/analytics/index', 1, NULL, 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"首页\",\"keepAlive\":true,\"affixTab\":false,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2025-09-11 08:41:09', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1406064334403878913, 'catalog', '系统管理', 0, '/system', NULL, '', 1, '', 19, NULL, '{\"title\":\"系统管理\",\"icon\":\"carbon:settings\",\"activeIcon\":\"carbon:settings\",\"keepAlive\":true}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040627847168, 'menu', '菜单管理', 1406064334403878913, '/system/sysMenu', NULL, '/basis/system/menu/list', 1, NULL, 1, NULL, '{\"title\":\"菜单管理\",\"icon\":\"carbon:menu\",\"activeIcon\":\"carbon:menu\",\"keepAlive\":true}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040627847169, 'button', '全部树形菜单列表', 1411332040627847168, '', NULL, NULL, 1, 'system:sysMenu:menuTreeAll', 1, NULL, '{\"title\":\"全部树形菜单列表\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":false,\"affixTab\":false,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040627847170, 'button', '新增菜单', 1411332040627847168, '', NULL, NULL, 1, 'system:menu:add', 2, NULL, '{\"title\":\"新增菜单\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":true,\"affixTab\":true,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040627847171, 'button', '编辑菜单', 1411332040627847168, '', NULL, NULL, 1, 'system:menu:edit', 3, NULL, '{\"title\":\"编辑菜单\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":true,\"affixTab\":true,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040627847172, 'button', '删除菜单', 1411332040627847168, '', NULL, NULL, 1, 'system:menu:delete', 4, NULL, '{\"title\":\"删除菜单\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":true,\"affixTab\":true,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040627847173, 'button', '查看菜单详情', 1411332040627847168, '', NULL, NULL, 1, 'system:menu:details', 5, NULL, '{\"title\":\"查看菜单详情\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":false,\"affixTab\":false,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040627847174, 'button', '导出菜单', 1411332040627847168, '', NULL, NULL, 1, 'system:menu:export', 6, NULL, '{\"title\":\"导出菜单\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":false,\"affixTab\":false,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040669790215, 'menu', '角色管理', 1406064334403878913, '/sysRole', NULL, '/basis/system/role/list', 1, 'system:role:page', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"角色管理\",\"badge\":\"\",\"keepAlive\":true,\"affixTab\":false,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2025-06-02 15:05:05', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040669790217, 'button', '新增角色', 1411332040669790215, '', NULL, NULL, 1, 'system:role:add', 2, NULL, '{\"title\":\"新增角色\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":true,\"affixTab\":true,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040669790218, 'button', '编辑角色', 1411332040669790215, '', NULL, NULL, 1, 'system:role:edit', 3, NULL, '{\"title\":\"编辑角色\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":true,\"affixTab\":true,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040669790219, 'button', '删除角色', 1411332040669790215, '', NULL, NULL, 1, 'system:role:delete', 4, NULL, '{\"title\":\"删除角色\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":false,\"affixTab\":false,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040669790220, 'button', '查看角色详情', 1411332040669790215, '', NULL, NULL, 1, 'system:role:details', 5, NULL, '{\"title\":\"查看角色详情\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":false,\"affixTab\":false,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1411332040669790221, 'button', '导出角色', 1411332040669790215, '', NULL, '', 2, 'system:role:export', 6, NULL, '{\"title\":\"导出角色\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"badge\":\"\",\"keepAlive\":false,\"affixTab\":false,\"hideInMenu\":false,\"hideChildrenInMenu\":false,\"hideInBreadcrumb\":false,\"hideInTab\":false}', 1401043674048851970, '2022-01-01 00:00:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1918491328990572545, 'menu', '部门管理', 1406064334403878913, '/system/sysDept', NULL, '/basis/system/dept/list', 1, 'system:dept:page', 1, NULL, '{\"title\":\"部门管理\",\"icon\":\"carbon:load-balancer-network\",\"activeIcon\":\"carbon:load-balancer-network\",\"keepAlive\":true}', NULL, NULL, NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1918494111974191105, 'button', '新增部门', 1918491328990572545, '', NULL, NULL, 1, 'system:dept:add', 1, NULL, '{\"title\":\"新增部门\",\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\"}', NULL, NULL, NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1918497951637204994, 'button', '编辑部门', 1918491328990572545, '', NULL, NULL, 1, 'system:dept:edit', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"编辑部门\"}', NULL, NULL, NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1918498103886245890, 'button', '删除部门', 1918491328990572545, '', NULL, NULL, 1, 'system:dept:delete', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"删除部门\"}', NULL, NULL, NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1918498261986340865, 'button', '查看部门详情', 1918491328990572545, '', NULL, NULL, 1, 'system:dept:details', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"查看部门详情\"}', NULL, NULL, NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1918721234106269697, 'menu', '用户管理', 1406064334403878913, '/system/user', NULL, '/basis/system/user/list', 1, 'system:user:page', 1, NULL, '{\"icon\":\"carbon:user-avatar\",\"activeIcon\":\"carbon:user-avatar\",\"title\":\"用户管理\",\"keepAlive\":true}', 1401043674048851970, '2025-05-04 01:36:05', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1919301498629103618, 'menu', '岗位管理', 1406064334403878913, '/system/post', NULL, '/basis/system/post/list', 1, NULL, 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"岗位管理\",\"keepAlive\":true}', 1401043674048851970, '2025-05-05 16:01:51', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1919404076020686849, 'menu', '权限分配', 1406064334403878913, '/system/permission', NULL, '/basis/system/permission/list', 1, 'system:permission:assignment', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"权限分配\",\"keepAlive\":true}', 1401043674048851970, '2025-05-05 22:49:27', 1401043674048851970, '2025-05-05 22:58:04', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1920046598040711169, 'menu', '字典管理', 1406064334403878913, '/system/dict', NULL, '/basis/system/dict/list', 1, 'system:dict:page', 1, NULL, '{\"icon\":\"carbon:ibm-cloud-direct-link-1-dedicated-hosting\",\"activeIcon\":\"carbon:ibm-cloud-direct-link-1-dedicated-hosting\",\"title\":\"字典管理\",\"keepAlive\":true}', 1401043674048851970, '2025-05-07 17:22:36', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1927989639623860226, 'menu', '在线用户', 1406064334403878913, '/monitor/onlineUser', NULL, '/basis/monitor/online/user/list', 1, 'login:user:online', 1, NULL, '{\"icon\":\"carbon:user-online\",\"activeIcon\":\"carbon:user-online\",\"title\":\"在线用户\",\"keepAlive\":true}', 1401043674048851970, '2025-05-29 15:25:25', 1401043674048851970, '2025-05-29 16:45:56', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1927989847896219649, 'button', '在线用户下线', 1927989639623860226, NULL, NULL, NULL, 1, 'login:user:offline', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"在线用户下线\"}', 1401043674048851970, '2025-05-29 15:26:15', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1928392716264714242, 'catalog', '日志管理', 1406064334403878913, '/basis/monitor/log', NULL, NULL, 1, NULL, 1, NULL, '{\"icon\":\"carbon:flow-logs-vpc\",\"activeIcon\":\"carbon:flow-logs-vpc\",\"title\":\"日志管理\"}', 1401043674048851970, '2025-05-30 18:07:06', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1928393172273639425, 'menu', '操作日志', 1928392716264714242, '/basis/monitor/log/operate', NULL, '/basis/monitor/log/operate/list', 1, 'sys:log:operate', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"操作日志\",\"keepAlive\":true}', 1401043674048851970, '2025-05-30 18:08:55', 1401043674048851970, '2025-05-31 16:49:13', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1928735855693172737, 'menu', '登录日志', 1928392716264714242, '/basis/monitor/log/login', NULL, '/basis/monitor/log/login/list', 1, NULL, 1, NULL, '{\"icon\":\"carbon:cloud-logging\",\"activeIcon\":\"carbon:cloud-logging\",\"title\":\"登录日志\",\"keepAlive\":true}', 1401043674048851970, '2025-05-31 16:50:37', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1928822491399475201, 'catalog', '系统工具', 0, '/tool', NULL, NULL, 1, NULL, 1, NULL, '{\"icon\":\"carbon:tool-kit\",\"activeIcon\":\"carbon:tool-kit\",\"title\":\"系统工具\"}', 1401043674048851970, '2025-05-31 22:34:52', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1928822772258459650, 'menu', '代码生成', 1928822491399475201, '/tool/genCode', NULL, '/basis/tool/gen/index', 1, NULL, 1, NULL, '{\"icon\":\"carbon:code\",\"activeIcon\":\"carbon:code\",\"title\":\"代码生成\",\"keepAlive\":true}', 1401043674048851970, '2025-05-31 22:35:59', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1929418394443497474, 'menu', '修改生成配置', 1928822491399475201, '/tool/gen/edit-gen/:tableId(\\d+)', NULL, '/basis/tool/gen/edit-gen/index', 1, NULL, 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改生成配置\",\"keepAlive\":true,\"hideInMenu\":true}', 1401043674048851970, '2025-06-02 14:02:47', 1401043674048851970, '2025-06-04 22:25:10', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1929834412332630018, 'menu', '系统参数', 1406064334403878913, '/system/config', NULL, '/basis/system/config/list', 1, NULL, 1, NULL, '{\"icon\":\"carbon:cloud-satellite-config\",\"activeIcon\":\"carbon:cloud-satellite-config\",\"title\":\"系统参数\",\"keepAlive\":true}', 1401043674048851970, '2025-06-03 17:35:53', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930280646977437698, 'menu', '表单设计', 1928822491399475201, '/tool/dynamicFormDesign', NULL, '/basis/tool/dynamic-form-design/list', 1, NULL, 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"表单设计\",\"keepAlive\":true}', 1401043674048851970, '2025-06-04 23:09:04', 1401043674048851970, '2025-06-05 00:15:11', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930792576809029634, 'button', '刷新在线用户权限', 1927989639623860226, NULL, NULL, NULL, 1, 'login:user:refreshPermission', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"刷新在线用户权限\"}', 1401043674048851970, '2025-06-06 09:03:17', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930903890885656577, 'button', '新增系统参数', 1929834412332630018, NULL, NULL, NULL, 1, 'system:sysConfig:add', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"新增系统参数\"}', 1401043674048851970, '2025-06-06 16:25:37', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930903989393080321, 'button', '修改系统参数', 1929834412332630018, NULL, NULL, NULL, 1, 'system:sysConfig:edit', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改系统参数\"}', 1401043674048851970, '2025-06-06 16:26:00', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930904139993759745, 'button', '删除系统参数', 1929834412332630018, NULL, NULL, NULL, 1, 'system:sysConfig:delete', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"删除系统参数\"}', 1401043674048851970, '2025-06-06 16:26:36', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930904311507238913, 'button', '更改系统参数状态', 1929834412332630018, NULL, NULL, NULL, 1, 'system:sysConfig:changeStatus', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"更改系统参数状态\"}', 1401043674048851970, '2025-06-06 16:27:17', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930910481139748865, 'button', '更改部门状态', 1918491328990572545, NULL, NULL, NULL, 1, 'system:dept:changeStatus', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"更改部门状态\"}', 1401043674048851970, '2025-06-06 16:51:48', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930913016206446593, 'button', '新增字典', 1920046598040711169, NULL, NULL, NULL, 1, 'system:dict:add', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"新增字典\"}', 1401043674048851970, '2025-06-06 17:01:52', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930915099945062402, 'button', '修改字典', 1920046598040711169, NULL, NULL, NULL, 1, 'system:dict:edit', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改字典\"}', 1401043674048851970, '2025-06-06 17:10:09', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930915199475896321, 'button', '删除字典', 1920046598040711169, NULL, NULL, NULL, 1, 'system:dict:delete', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"删除字典\"}', 1401043674048851970, '2025-06-06 17:10:33', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930915323170115585, 'button', '修改字典状态', 1920046598040711169, NULL, NULL, NULL, 1, 'system:dict:changeStatus', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改字典状态\"}', 1401043674048851970, '2025-06-06 17:11:02', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930915741841346562, 'button', '新增字典项', 1920046598040711169, NULL, NULL, NULL, 1, 'system:dictItem:add', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"新增字典项\"}', 1401043674048851970, '2025-06-06 17:12:42', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930915875706753026, 'button', '修改字典项', 1920046598040711169, NULL, NULL, NULL, 1, 'system:dictItem:edit', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改字典项\"}', 1401043674048851970, '2025-06-06 17:13:14', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930915966299525122, 'button', '删除字典项', 1920046598040711169, NULL, NULL, NULL, 1, 'system:dictItem:delete', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"删除字典项\"}', 1401043674048851970, '2025-06-06 17:13:36', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930916364368334849, 'button', '修改菜单排序', 1411332040627847168, NULL, NULL, NULL, 1, 'system:menu:changeSort', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改菜单排序\"}', 1401043674048851970, '2025-06-06 17:15:11', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930916506114838529, 'button', '新增岗位', 1919301498629103618, NULL, NULL, NULL, 1, 'system:post:add', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"新增岗位\"}', 1401043674048851970, '2025-06-06 17:15:44', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930916609030475777, 'button', '修改岗位', 1919301498629103618, NULL, NULL, NULL, 1, 'system:post:edit', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改岗位\"}', 1401043674048851970, '2025-06-06 17:16:09', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930916698000052225, 'button', '删除岗位', 1919301498629103618, NULL, NULL, NULL, 1, 'system:post:delete', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"删除岗位\"}', 1401043674048851970, '2025-06-06 17:16:30', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930916806045323266, 'button', '修改岗位状态', 1919301498629103618, NULL, NULL, NULL, 1, 'system:post:changeStatus', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改岗位状态\"}', 1401043674048851970, '2025-06-06 17:16:56', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930917031099092994, 'button', '修改角色状态', 1411332040669790215, NULL, NULL, NULL, 1, 'system:role:changeStatus', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改角色状态\"}', 1401043674048851970, '2025-06-06 17:17:50', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930917488747991041, 'button', '新增用户', 1918721234106269697, NULL, NULL, NULL, 1, 'system:user:add', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"新增用户\"}', 1401043674048851970, '2025-06-06 17:19:39', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930917616447770625, 'button', '编辑用户', 1918721234106269697, NULL, NULL, NULL, 1, 'system:user:edit', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"编辑用户\"}', 1401043674048851970, '2025-06-06 17:20:09', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930917694017228802, 'button', '删除用户', 1918721234106269697, NULL, NULL, NULL, 1, 'system:user:delete', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"删除用户\"}', 1401043674048851970, '2025-06-06 17:20:28', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930917780688326658, 'button', '重置用户密码', 1918721234106269697, NULL, NULL, NULL, 1, 'system:user:resetPwd', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"重置用户密码\"}', 1401043674048851970, '2025-06-06 17:20:48', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1930917864624738305, 'button', '修改用户状态', 1918721234106269697, NULL, NULL, NULL, 1, 'system:user:changeStatus', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"修改用户状态\"}', 1401043674048851970, '2025-06-06 17:21:08', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1932012222044237825, 'catalog', '系统监控', 0, '/monitor', NULL, NULL, 1, NULL, 1, NULL, '{\"icon\":\"carbon:ibm-cloud-backup-service-vpc\",\"activeIcon\":\"carbon:ibm-cloud-backup-service-vpc\",\"title\":\"系统监控\"}', 1401043674048851970, '2025-06-09 17:49:43', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1932012486109229057, 'menu', '服务监控', 1932012222044237825, '/monitor/server', NULL, '/basis/monitor/server/index', 1, NULL, 1, NULL, '{\"icon\":\"carbon:ibm-cloud-bare-metal-server\",\"activeIcon\":\"carbon:ibm-cloud-bare-metal-server\",\"title\":\"服务监控\",\"keepAlive\":true}', 1401043674048851970, '2025-06-09 17:50:46', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1933698093986365441, 'button', '查看字典项列表', 1920046598040711169, NULL, NULL, NULL, 1, 'system:dictItem:list', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"查看字典项列表\"}', 1401043674048851970, '2025-06-14 09:28:47', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1941148851010527234, 'button', '部门关联岗位', 1918491328990572545, NULL, NULL, NULL, 1, 'system:dept:post:add', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"部门关联岗位\"}', 1401043674048851970, '2025-07-04 22:55:26', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1954720741071618050, 'catalog', 'AI管理', 0, '/ai', NULL, NULL, 1, NULL, 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"AI管理\"}', 1401043674048851970, '2025-08-11 09:45:16', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1954721042608521218, 'menu', '模型管理', 1954720741071618050, '/ai/model', NULL, '/ai/model/list', 1, 'ai:model:list', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"模型管理\",\"keepAlive\":true}', 1401043674048851970, '2025-08-11 09:46:28', 1401043674048851970, '2025-09-04 11:45:02', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1954722276576952322, 'button', '新增模型', 1954721042608521218, NULL, NULL, NULL, 1, 'ai:model:add', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"新增模型\"}', 1401043674048851970, '2025-08-11 09:51:22', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1954722342976978946, 'button', '编辑模型', 1954721042608521218, NULL, NULL, NULL, 1, 'ai:model:edit', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"编辑模型\"}', 1401043674048851970, '2025-08-11 09:51:38', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1954722420286390273, 'button', '删除模型', 1954721042608521218, NULL, NULL, NULL, 1, 'ai:model:delete', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"删除模型\"}', 1401043674048851970, '2025-08-11 09:51:57', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1963449802404999169, 'menu', '模型参数', 1954720741071618050, '/ai/model/option', NULL, '/ai/model-option/list', 1, 'ai:model:option:list', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"模型参数\",\"keepAlive\":true}', 1401043674048851970, '2025-09-04 11:51:27', 1401043674048851970, '2025-09-04 18:01:50', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1963450203489513473, 'button', '新增参数', 1963449802404999169, NULL, NULL, NULL, 1, 'ai:model:option:add', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"新增参数\"}', 1401043674048851970, '2025-09-04 11:53:02', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1963450286234742785, 'button', '编辑参数', 1963449802404999169, NULL, NULL, NULL, 1, 'ai:model:option:edit', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"编辑参数\"}', 1401043674048851970, '2025-09-04 11:53:22', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1963450416157503489, 'button', '删除参数', 1963449802404999169, NULL, NULL, NULL, 1, 'ai:model:option:delete', 1, NULL, '{\"icon\":\"carbon:security\",\"activeIcon\":\"carbon:security\",\"title\":\"删除参数\"}', 1401043674048851970, '2025-09-04 11:53:53', NULL, NULL, 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (1964898813045444610, 'button', '知识库1', 1954720741071618050, '/knowledge', NULL, '/ai/knowledge/list', 1, 'sssssss', 1, '', '{\"icon\":\"carbon:security\",\"active_icon\":\"carbon:security\",\"title\":\"知识库1\",\"badge_type\":\"normal\",\"badge\":\"asd\",\"badge_variants\":\"warning\",\"keep_alive\":true,\"affix_tab\":true,\"hide_in_menu\":true,\"hide_children_in_menu\":true,\"hide_in_breadcrumb\":true,\"hide_in_tab\":true}', 1401043674048851970, '2025-09-08 11:49:18', 1401043674048851970, '2026-01-20 03:42:34', 0);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`, `is_deleted`) VALUES (3133052898641014790, 'menu', '演示', 1954720741071618050, '/knowledge2', NULL, '/ai/knowledge/list', 1, 'sssssss', 1, '', '{\"icon\":\"carbon:security\",\"active_icon\":\"carbon:security\",\"title\":\"演示\",\"badge_type\":\"dot\",\"badge_variants\":\"destructive\",\"keep_alive\":true,\"affix_tab\":true,\"hide_in_menu\":false,\"hide_children_in_menu\":false}', 1401043674048851970, '2026-01-20 03:48:27', 1401043674048851970, '2026-01-20 03:50:11', 1);
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_post
-- ----------------------------
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
) ENGINE=InnoDB AUTO_INCREMENT=3131603565131427847 DEFAULT CHARSET=utf8mb4 COMMENT='岗位表';

-- ----------------------------
-- Records of tbl_sys_post
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_post` (`id`, `post_code`, `name`, `remarks`, `sort`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1407219533063471106, '000001', '董事长', NULL, 1, 1, 0, 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2022-01-01 00:00:00');
INSERT INTO `tbl_sys_post` (`id`, `post_code`, `name`, `remarks`, `sort`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1407222184903786498, '000002', '普通员工', '', 3, 1, 0, 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2026-01-19 03:50:47');
INSERT INTO `tbl_sys_post` (`id`, `post_code`, `name`, `remarks`, `sort`, `status`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3131603565131427846, '000003', 'demo', '12', 2, 1, 1, 1401043674048851970, '2026-01-19 03:48:40', 1401043674048851970, '2026-01-19 03:48:51');
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_role
-- ----------------------------
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
) ENGINE=InnoDB AUTO_INCREMENT=1401043545271136260 DEFAULT CHARSET=utf8mb4 COMMENT='角色表';

-- ----------------------------
-- Records of tbl_sys_role
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_role` (`id`, `role_code`, `name`, `remarks`, `sort`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1401043545271136258, 'admin', '超级管理员', '', 1, 1, 1, 0, 1401043674048851970, '2026-01-08 09:20:14', NULL, NULL);
INSERT INTO `tbl_sys_role` (`id`, `role_code`, `name`, `remarks`, `sort`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1401043545271136259, 'demo', '演示', '', 1, 1, 2, 0, 1401043674048851970, '2026-01-08 09:20:14', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `tbl_sys_role_menu`;
CREATE TABLE `tbl_sys_role_menu` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `menu_id` bigint(20) NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3133224360479911943 DEFAULT CHARSET=utf8mb4 COMMENT='角色菜单表';

-- ----------------------------
-- Records of tbl_sys_role_menu
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_role_menu` (`id`, `role_id`, `menu_id`) VALUES (1, 1401043545271136258, 1406063931784179714);
INSERT INTO `tbl_sys_role_menu` (`id`, `role_id`, `menu_id`) VALUES (3, 1401043545271136258, 1406063931784179715);
INSERT INTO `tbl_sys_role_menu` (`id`, `role_id`, `menu_id`) VALUES (3133224360479911942, 1401043545271136259, 1406063931784179714);
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_user
-- ----------------------------
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ----------------------------
-- Records of tbl_sys_user
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (48686830226862086, 'demo', '', 1, '张三', NULL, '935415486qq@gmail.com', '13600000000', '001', '2026-01-16 00:00:00', 1, 1406955981362733058, 1, 2, 'asd', 1, 2, 0, 1401043674048851970, '2026-01-08 08:45:20', 1401043674048851970, '2026-01-16 02:22:10');
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1401043674048851970, 'admin', '$argon2id$v=19$m=65536,t=3,p=4$HPRMWMxZYbj8jLi0tgVY1Q$qyMHicNy+TWuUq7B4kcJT+03QTkwshKqkrlj8Mdd6R8', 2, '超级管理员', 'https://vxeui.com/resource/avatarImg/avatar20.jpeg', '', '18888888888', '', NULL, 1, 1406957570110562306, 1, 1, 'qwqwqqwqwqqwqwqqwqwqqwqwqqwqwqqwqwqqwqwqqwqwq', 1, 1, 0, 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2025-06-10 00:00:00');
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3115958858976161798, 'demo1', '$argon2id$v=19$m=65536,t=3,p=4$6NWBgszIVo/8S3DqPF+Pow$C0ueDUt7TUXk359qYOMhIsX28dfaKtwmeJc1GzE60JA', 1, '张三', NULL, NULL, NULL, NULL, NULL, 3, NULL, 1, 0, NULL, 1, 2, 0, 1401043674048851970, '2026-01-08 08:47:03', NULL, NULL);
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3115958901909057542, 'demo2', '$argon2id$v=19$m=65536,t=3,p=4$tv0vKgaJs71wPEfvXDD9ig$NebdUy/0LlgfOcrsG6DNUpEY1mdxikmqfKkzemlG7Zk', 1, '张三', NULL, NULL, NULL, NULL, NULL, 3, NULL, 1, 0, NULL, 1, 2, 0, 1401043674048851970, '2026-01-08 08:47:05', NULL, NULL);
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3115958950680424454, 'demo3', '$argon2id$v=19$m=65536,t=3,p=4$7nQ6Wpg+BU9p9Y6uZmErUA$WNverpCoCIyg26fF9CM9Nx0NQXsPvXBrlCGDFSDXI+E', 1, '张三', NULL, NULL, NULL, NULL, NULL, 3, NULL, 1, 0, NULL, 1, 2, 0, 1401043674048851970, '2026-01-08 08:47:08', NULL, NULL);
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3127353201792217094, 'osinn', '', 1, '开源客栈', NULL, '617474214@qq.com', '13600000000', '002', '2026-01-16 00:00:00', 1, 1918556212432396290, 1, 2, 'sa', 2, 2, 0, 1401043674048851970, '2026-01-16 05:26:18', 1401043674048851970, '2026-01-20 03:05:24');
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3127359471555276806, 'osinn1', '', 1, '开源客栈1', NULL, '617474211@qq.com', '13600000000', '003', '2026-01-16 00:00:00', 1, 1918556212432396290, 1, 2, 'sa', 1, 2, 0, 1401043674048851970, '2026-01-16 05:32:32', 1401043674048851970, '2026-01-16 05:42:54');
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (3127371352793772038, 'osinn4', '', 1, '开源客栈4', NULL, NULL, NULL, NULL, NULL, 1, 1406955981362733058, 1, 1, NULL, 1, 2, 0, 1401043674048851970, '2026-01-16 05:44:20', 1401043674048851970, '2026-01-16 08:29:13');
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_user_post
-- ----------------------------
DROP TABLE IF EXISTS `tbl_sys_user_post`;
CREATE TABLE `tbl_sys_user_post` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `post_id` bigint(20) NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3127537335160369159 DEFAULT CHARSET=utf8mb4 COMMENT='用户岗位表';

-- ----------------------------
-- Records of tbl_sys_user_post
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1420592919731150850, 1401043674048851971, 1407222184903786498);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1420631281447989249, 1420631092897247234, 1407222184903786498);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1920318940859961345, 1920318823696273409, 1407219533063471106);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1920318940864155649, 1920318823696273409, 1407222184903786498);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1932253589756469249, 1401043674048851970, 1407219533063471106);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1932371817006653442, 1919275057237495810, 1407222184903786498);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1932371817015042050, 1919275057237495810, 1407219533063471106);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1932632287752032258, 1422026532410515457, 1407222184903786498);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (1932681689791270914, 1422030869111136258, 1407222184903786498);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (3127167801626816518, 48686830226862086, 1407222184903786498);
INSERT INTO `tbl_sys_user_post` (`id`, `user_id`, `post_id`) VALUES (3127537335160369158, 3127371352793772038, 1407222184903786498);
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `tbl_sys_user_role`;
CREATE TABLE `tbl_sys_user_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3127537340663296007 DEFAULT CHARSET=utf8mb4 COMMENT='用户角色表';

-- ----------------------------
-- Records of tbl_sys_user_role
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_user_role` (`id`, `user_id`, `role_id`) VALUES (1, 1401043674048851970, 1401043545271136258);
INSERT INTO `tbl_sys_user_role` (`id`, `user_id`, `role_id`) VALUES (2, 1401043674048851970, 1401043545271136259);
INSERT INTO `tbl_sys_user_role` (`id`, `user_id`, `role_id`) VALUES (3127167801710702598, 48686830226862086, 1401043545271136259);
INSERT INTO `tbl_sys_user_role` (`id`, `user_id`, `role_id`) VALUES (3127369913325416454, 3127359471555276806, 1401043545271136259);
INSERT INTO `tbl_sys_user_role` (`id`, `user_id`, `role_id`) VALUES (3127370011606347782, 3127353201792217094, 1401043545271136259);
INSERT INTO `tbl_sys_user_role` (`id`, `user_id`, `role_id`) VALUES (3127537340663296006, 3127371352793772038, 1401043545271136259);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
