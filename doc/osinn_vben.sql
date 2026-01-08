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

 Date: 08/01/2026 14:49:09
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
-- Table structure for tbl_role
-- ----------------------------
DROP TABLE IF EXISTS `tbl_role`;
CREATE TABLE `tbl_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='演示表';

-- ----------------------------
-- Records of tbl_role
-- ----------------------------
BEGIN;
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
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态 0-正常；1-停用',
  `auth_code` varchar(128) DEFAULT NULL COMMENT '权限标识',
  `sort` int(11) NOT NULL DEFAULT '1' COMMENT '排序',
  `remarks` varchar(512) DEFAULT NULL COMMENT '备注',
  `meta` text,
  `created_by` bigint(20) NOT NULL COMMENT '创建人',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1406063931784179716 DEFAULT CHARSET=utf8mb4 COMMENT='菜单表 ';

-- ----------------------------
-- Records of tbl_sys_menu
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1406063931784179714, 'menu', '首页', 0, '/analytics', NULL, '/dashboard/analytics/index', 0, 'demo', 1, NULL, NULL, 1401043674048851970, '2026-01-08 09:23:10', NULL, NULL);
INSERT INTO `tbl_sys_menu` (`id`, `type`, `name`, `parent_id`, `path`, `redirect`, `component`, `status`, `auth_code`, `sort`, `remarks`, `meta`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1406063931784179715, 'menu', '控制台', 0, '/analytics', NULL, '/dashboard/analytics/index', 0, 'demo', 1, NULL, NULL, 1401043674048851970, '2026-01-08 09:23:10', NULL, NULL);
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
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '状态 0-正常；1-停用',
  `is_default` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否系统默认角色',
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
INSERT INTO `tbl_sys_role` (`id`, `role_code`, `name`, `remarks`, `sort`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1401043545271136258, 'admin', '超级管理员', '', 1, 0, 0, 0, 1401043674048851970, '2026-01-08 09:20:14', NULL, NULL);
INSERT INTO `tbl_sys_role` (`id`, `role_code`, `name`, `remarks`, `sort`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1401043545271136259, 'demo', '演示', '', 1, 0, 0, 0, 1401043674048851970, '2026-01-08 09:20:14', NULL, NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='角色菜单表';

-- ----------------------------
-- Records of tbl_sys_role_menu
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_role_menu` (`id`, `role_id`, `menu_id`) VALUES (1, 1401043545271136258, 1406063931784179714);
INSERT INTO `tbl_sys_role_menu` (`id`, `role_id`, `menu_id`) VALUES (2, 1401043545271136259, 1406063931784179715);
INSERT INTO `tbl_sys_role_menu` (`id`, `role_id`, `menu_id`) VALUES (3, 1401043545271136258, 1406063931784179715);
COMMIT;

-- ----------------------------
-- Table structure for tbl_sys_user
-- ----------------------------
DROP TABLE IF EXISTS `tbl_sys_user`;
CREATE TABLE `tbl_sys_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `account` varchar(128) DEFAULT NULL COMMENT '账号',
  `password` varchar(128) DEFAULT NULL COMMENT '密码',
  `psw_modified` tinyint(1) NOT NULL DEFAULT '0' COMMENT '修改密码标记 0未修改；1已修改',
  `nickname` varchar(128) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(128) DEFAULT NULL COMMENT '头像',
  `email` varchar(128) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(32) DEFAULT NULL COMMENT '手机号',
  `staff_number` varchar(32) DEFAULT NULL COMMENT '工号',
  `birthday` datetime DEFAULT NULL COMMENT '生日',
  `sex` tinyint(4) DEFAULT NULL COMMENT '性别 1-男；2-女；3未知',
  `dept_id` bigint(20) DEFAULT NULL COMMENT '部门ID',
  `lock_account` tinyint(4) NOT NULL DEFAULT '0' COMMENT '锁定标记 0正常；1锁定',
  `sort` int(11) NOT NULL DEFAULT '0' COMMENT '排序',
  `remarks` varchar(512) DEFAULT NULL COMMENT '备注',
  `status` tinyint(1) DEFAULT '0' COMMENT '状态 0正常；1停用',
  `is_default` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否系统默认账号',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标记 0-存在；1-删除',
  `created_by` bigint(20) DEFAULT NULL COMMENT '创建人',
  `created_time` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1401043674048851974 DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ----------------------------
-- Records of tbl_sys_user
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_user` (`id`, `account`, `password`, `psw_modified`, `nickname`, `avatar`, `email`, `phone`, `staff_number`, `birthday`, `sex`, `dept_id`, `lock_account`, `sort`, `remarks`, `status`, `is_default`, `is_deleted`, `created_by`, `created_time`, `updated_by`, `updated_time`) VALUES (1401043674048851970, 'admin', '$argon2id$v=19$m=65536,t=3,p=4$HPRMWMxZYbj8jLi0tgVY1Q$qyMHicNy+TWuUq7B4kcJT+03QTkwshKqkrlj8Mdd6R8', 1, '超级管理员', 'https://vxeui.com/resource/avatarImg/avatar20.jpeg', '', '18888888888', '', NULL, 1, 1406957570110562306, 1, 1, 'qwqwqqwqwqqwqwqqwqwqqwqwqqwqwqqwqwqqwqwqqwqwq', 1, 1, 0, 1401043674048851970, '2022-01-01 00:00:00', 1401043674048851970, '2025-06-10 00:00:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COMMENT='用户角色表';

-- ----------------------------
-- Records of tbl_sys_user_role
-- ----------------------------
BEGIN;
INSERT INTO `tbl_sys_user_role` (`id`, `user_id`, `role_id`) VALUES (1, 1401043674048851970, 1401043545271136258);
INSERT INTO `tbl_sys_user_role` (`id`, `user_id`, `role_id`) VALUES (2, 1401043674048851970, 1401043545271136259);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
