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
  `dept_id` varchar(32) DEFAULT NULL COMMENT '部门ID',
  `lock_account` tinyint(4) NOT NULL DEFAULT '0' COMMENT '锁定标记 0正常；1锁定',
  `sort` int(11) NOT NULL DEFAULT '0' COMMENT '排序',
  `remarks` varchar(512) DEFAULT NULL COMMENT '备注',
  `status` tinyint(1) DEFAULT '0' COMMENT '状态 0正常；1停用',
  `is_default` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否系统默认账号',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标记 0-存在；1-删除',
  `created_by` bigint(20) NOT NULL COMMENT '创建人',
  `created_time` datetime NOT NULL COMMENT '创建时间',
  `updated_by` bigint(20) DEFAULT NULL COMMENT '更新人',
  `updated_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='用户表';

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
) ENGINE=InnoDB COMMENT='角色表';

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
) ENGINE=InnoDB COMMENT='菜单表 ';

CREATE TABLE `tbl_sys_role_menu` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `menu_id` bigint(20) NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='角色菜单表';

CREATE TABLE `tbl_sys_user_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB COMMENT='用户角色表';