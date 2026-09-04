# 课小秘数据库完整物理数据字典

生成时间：2026-08-29T11:36:50+00:00

本字典只来自 MySQL `information_schema` 与部署分库配置，不读取业务数据。连接地址、账号、密码和连接串不会写入本文件。
字段的 `queryPolicy` 只是自动风险分类，不等于 Agent 已获授权；运行时仍必须使用服务端字段白名单、门店/租户注入、只读账号、条数和超时限制。

## 财务分库路由

- 优先匹配 TenantId 精确配置
- 其次匹配 MinTenantId <= tenantId <= MaxTenantId 的区间配置
- 仍未命中时使用 TenantData + (tenantId % 10)

| TenantId | 最小 TenantId | 最大 TenantId | 连接名 |
|---:|---:|---:|---|
| 0 | 0 | 10100000 | TenantData |
| 0 | 10100001 | 10200000 | TenantData0 |
| 0 | 10200001 | 10300000 | TenantData1 |

## 采集覆盖情况

全部配置目标均已有结构目录：未实时连通的 TenantData0-9 分片按运维方确认的同构约束继承自已实测模板库。结构覆盖完整不代表连接可用，运行时仍必须按目标租户路由并在连接失败时拒绝查询。

| 逻辑连接别名 | 配置数据库 | 结构覆盖 | 模板数据库 | 实时错误类型 | MySQL 错误码 |
|---|---|---|---|---|---:|
| TenantData0 | nutbooking_consumption_0 | 模板继承 | nutbooking_consumption | OperationalError | 1049 |
| TenantData1 | nutbooking_consumption_1 | 模板继承 | nutbooking_consumption | OperationalError | 1049 |
| TenantData2 | nutbooking_consumption_2 | 模板继承 | nutbooking_consumption | OperationalError | 2013 |
| TenantData3 | nutbooking_consumption_3 | 模板继承 | nutbooking_consumption | OperationalError | 2013 |
| TenantData4 | nutbooking_consumption_4 | 模板继承 | nutbooking_consumption | OperationalError | 2013 |
| TenantData5 | nutbooking_consumption_5 | 模板继承 | nutbooking_consumption | OperationalError | 2013 |
| TenantData6 | nutbooking_consumption_6 | 模板继承 | nutbooking_consumption | OperationalError | 2013 |
| TenantData7 | nutbooking_consumption_7 | 模板继承 | nutbooking_consumption | OperationalError | 2013 |
| TenantData8 | nutbooking_consumption_8 | 模板继承 | nutbooking_consumption | OperationalError | 2013 |

## 数据库概览

| 数据库 | 角色 | 结构证据 | 模板数据库 | 逻辑连接别名 | 表/视图 | 字段 | 索引 | 外键 |
|---|---|---|---|---|---:|---:|---:|---:|
| nutbooking | main | 实时采集 | nutbooking | LinkFitDataOnlyRead | 363 | 4992 | 491 | 0 |
| nutbooking_consumption | finance-shard | 实时采集 | nutbooking_consumption | TenantData, TenantData9 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_0 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData0 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_1 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData1 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_2 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData2 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_3 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData3 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_4 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData4 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_5 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData5 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_6 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData6 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_7 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData7 | 13 | 269 | 29 | 0 |
| nutbooking_consumption_8 | finance-shard | 同构模板继承 | nutbooking_consumption | TenantData8 | 13 | 269 | 29 | 0 |

## 数据库 `nutbooking`

角色：main；连接别名：LinkFitDataOnlyRead；结构证据：MySQL 实时元数据；结构来源：`nutbooking`；结构指纹：`4ffbd9ad5d32ef1461787f3fe62b06868492c9c7ffbfb3242a593529823e2a0a`。

### `activity`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 活动id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺Id | internal | store-scope | server-filter-only |
| 3 | `title` | `varchar(50)` | 否 |  |  | 活动标题 | internal | business-field | semantic-review-required |
| 4 | `activity_type` | `int(11)` | 否 |  |  | 0 新用户活动 | internal | business-field | semantic-review-required |
| 5 | `bg_img` | `varchar(100)` | 是 |  | 0 | 活动背景图 | internal | business-field | semantic-review-required |
| 6 | `is_one_reward` | `tinyint(1)` | 否 |  |  | 是否开启新客奖励 | internal | business-field | semantic-review-required |
| 7 | `is_two_reward` | `tinyint(1)` | 否 |  |  | 是否开启转发人奖励 | internal | business-field | semantic-review-required |
| 8 | `one_receive_limit` | `int(11)` | 否 |  | 0 | 新客奖励领取限制 0无限制 1新客 2老会员 | internal | business-field | semantic-review-required |
| 9 | `one_is_mobile` | `tinyint(1)` | 否 |  | 0 | 领取是否索要手机号码 | sensitive | business-field | masked-or-filter-only |
| 10 | `share_limit` | `int(11)` | 否 |  | 0 | 转发限制，0允许转发，1不允许转发 | internal | business-field | semantic-review-required |
| 11 | `two_receive_limit` | `int(11)` | 否 |  | 1 | 转发人奖励限制 0 只要转发就可以得到 1有人领取才可以得到 2使用卷后才可以得到 | internal | business-field | semantic-review-required |
| 12 | `two_receive_count` | `int(11)` | 否 |  |  | 转发人奖励数量 0 仅限一份 1满足限制条件 无限制 | internal | business-field | semantic-review-required |
| 13 | `two_is_mobile` | `tinyint(1)` | 否 |  | 0 | 转发是否索要手机号码 | sensitive | business-field | masked-or-filter-only |
| 14 | `activity_rules` | `varchar(500)` | 是 |  |  | 活动规则 | internal | business-field | semantic-review-required |
| 15 | `begin_date` | `date` | 否 |  |  | 活动开始时间 | internal | business-field | semantic-review-required |
| 16 | `end_date` | `date` | 否 |  |  | 活动结束时间 | internal | business-field | semantic-review-required |
| 17 | `is_top` | `tinyint(1)` | 否 |  | 0 | 是否首页弹窗提醒 | internal | business-field | semantic-review-required |
| 18 | `is_send_wechat` | `tinyint(1)` | 否 |  | 0 | 是否发送微信通知 | internal | business-field | semantic-review-required |
| 19 | `is_reward_unite` | `tinyint(1)` | 否 |  |  | 是否奖励统一 | internal | business-field | semantic-review-required |
| 20 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0暂停 1正常 2未开始 3结束 | internal | business-field | semantic-review-required |
| 21 | `end_reason` | `int(11)` | 否 |  |  | 结束原因 0默认 1到期 2优惠券发放完毕 | internal | business-field | semantic-review-required |
| 22 | `tenant_id` | `int(11)` | 否 |  |  | 租户Id | internal | tenant-scope | server-filter-only |
| 23 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 24 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 25 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 26 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `activity_coupon`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：活动优惠券关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `activity_id` | `int(11)` | 否 |  |  | 活动id | internal | relation-key | server-filter-only |
| 3 | `coupon_id` | `int(11)` | 否 |  |  | 优惠券id | internal | relation-key | server-filter-only |
| 4 | `ac_type` | `int(11)` | 否 |  |  | 类型 0活动主动领券，1分享后领券 | internal | business-field | semantic-review-required |
| 5 | `coupon_count` | `int(11)` | 否 |  | 0 | 已领取数量 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 0禁用 1启用 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `activity_link`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：活动连接

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `title` | `varchar(30)` | 否 |  |  | 链接标题 | internal | business-field | semantic-review-required |
| 3 | `link_type` | `int(11)` | 否 |  |  | 连接类型：0系统,1商家认证 | internal | business-field | semantic-review-required |
| 4 | `link_tag` | `varchar(10)` | 是 | MUL |  | 连接标记 | internal | business-field | semantic-review-required |
| 5 | `target_url` | `varchar(200)` | 是 |  |  | 目标url | internal | business-field | semantic-review-required |
| 6 | `param` | `varchar(50)` | 是 |  |  | 参数 | internal | business-field | semantic-review-required |
| 7 | `qrcode_url` | `varchar(100)` | 是 |  |  | 二维码路径 | internal | business-field | semantic-review-required |
| 8 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 9 | `state` | `int(11)` | 否 |  |  | 状态0禁用 1启用 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tag`：非唯一 BTREE（link_tag）

### `activity_log`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：活动相关日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `activity_id` | `int(11)` | 否 | MUL |  | 活动id | internal | relation-key | server-filter-only |
| 3 | `activity_type` | `int(11)` | 否 |  | 0 | 活动类型 0裂变 1抽奖 | internal | business-field | semantic-review-required |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `is_new_user` | `tinyint(1)` | 否 |  |  | 是否是新客 | internal | business-field | semantic-review-required |
| 6 | `recom_uid` | `int(11)` | 否 |  | 0 | 推荐者Id | internal | business-field | semantic-review-required |
| 7 | `log_type` | `int(11)` | 否 |  |  | 0 查看 1领券or抽奖 2分享 | internal | business-field | semantic-review-required |
| 8 | `request_ip` | `varchar(30)` | 否 |  |  | 用户ip | sensitive-unstructured | business-field | deny |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_aid`：非唯一 BTREE（activity_id）

### `activity_template`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键Id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `activity_type` | `int(11)` | 否 |  |  | 活动类型 0裂变 1抽奖 | internal | business-field | semantic-review-required |
| 4 | `img_url` | `varchar(255)` | 否 |  |  | 图片路径 | internal | business-field | semantic-review-required |
| 5 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `added_services`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `service_type` | `int(11)` | 否 |  | 0 | 类型 0短信，1物料，2硬件设备，3坚果币充值相关 | internal | business-field | semantic-review-required |
| 3 | `is_bind_device` | `int(11)` | 否 |  | 0 | 是否是可以绑定的设备；0-否，1-是 | internal | business-field | semantic-review-required |
| 4 | `title` | `varchar(100)` | 否 |  |  | 标题 | internal | business-field | semantic-review-required |
| 5 | `child_title` | `varchar(100)` | 否 |  |  | 子标题 | internal | business-field | semantic-review-required |
| 6 | `poster_id` | `int(11)` | 否 |  |  | 海报ID | internal | relation-key | server-filter-only |
| 7 | `service_unit` | `varchar(10)` | 否 |  |  | 单位 | internal | business-field | semantic-review-required |
| 8 | `service_img` | `varchar(100)` | 否 |  |  | 图片 | internal | business-field | semantic-review-required |
| 9 | `item_quantity` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 10 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 价格 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣价 | internal | business-field | semantic-review-required |
| 12 | `end_date` | `datetime` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 13 | `service_info` | `varchar(255)` | 否 |  |  | 介绍 | internal | business-field | semantic-review-required |
| 14 | `is_ship` | `tinyint(1)` | 否 |  | 0 | 是否需要发货 | internal | business-field | semantic-review-required |
| 15 | `is_soft_discount` | `tinyint(1)` | 否 |  | 0 | 是否参与软件购买打折 | internal | business-field | semantic-review-required |
| 16 | `soft_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 软件组合购买折扣价 | internal | business-field | semantic-review-required |
| 17 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 18 | `state` | `int(11)` | 否 |  |  | 0停用 1正常 | internal | business-field | semantic-review-required |
| 19 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 20 | `update_datetime` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 21 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `added_services_info`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `added_id` | `int(11)` | 否 |  |  | 增值id | internal | relation-key | server-filter-only |
| 3 | `added_img` | `varchar(100)` | 否 |  |  | 图片地址 | internal | business-field | semantic-review-required |
| 4 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 状态1 启用 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `admin_menu`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(4)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `root_id` | `int(4)` | 否 |  | 0 | 父级ID | internal | relation-key | server-filter-only |
| 3 | `name` | `varchar(100)` | 否 |  |  | 菜单名称 | internal | business-field | semantic-review-required |
| 4 | `url` | `varchar(255)` | 是 |  |  | 菜单导航路径 | internal | business-field | semantic-review-required |
| 5 | `icon` | `varchar(255)` | 是 |  |  | 菜单图标 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 1 |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `admin_user`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：管理员

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `ID` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `admin_name` | `varchar(20)` | 否 |  |  | 管理员名称 | internal | business-field | semantic-review-required |
| 3 | `admin_pass` | `varchar(35)` | 否 |  |  | 管理员密码 | internal | business-field | semantic-review-required |
| 4 | `admin_type` | `int(11)` | 否 |  |  | 权限0管理员 1技术，2客服 3运营，10销售主管 11销售 | internal | business-field | semantic-review-required |
| 5 | `admin_img` | `varchar(50)` | 否 |  |  | 头像 | internal | business-field | semantic-review-required |
| 6 | `user_id` | `int(11)` | 否 |  | 0 | 用户id | internal | subject-or-relation-key | server-filter-only |
| 7 | `open_id` | `varchar(100)` | 否 |  |  | 用于系统通知 | restricted | relation-key | deny |
| 8 | `State` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（ID）

### `admin_user_rights`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `admin_id` | `int(11)` | 否 |  |  | 管理员ID | internal | relation-key | server-filter-only |
| 3 | `admin_rights` | `varchar(255)` | 是 |  |  | 管理员权限，注：没有的权限才往此列里面存储，默认有所有权限 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `agency_matter`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：待办事项审核流程操作表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键自增ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 门店ID | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 是 |  |  | 会员卡Id | internal | subject-or-relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 是 |  |  | 用户Id | internal | subject-or-relation-key | server-filter-only |
| 5 | `tenant_id` | `int(11)` | 是 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 6 | `agency_type` | `int(11)` | 是 |  |  | 事项类型(扩展字段)：当前默认1为优惠券，2为会员卡,后续会根据业务进行增加 | internal | business-field | semantic-review-required |
| 7 | `handle_type` | `int(11)` | 是 |  |  | 处理人类型：1、发起   2、核销 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  | 0 | 0 待审核  1审核通过 -1 审核失败   | internal | business-field | semantic-review-required |
| 9 | `create_time` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `sponsor_uid` | `int(11)` | 是 |  |  | 发起人ID  | internal | business-field | semantic-review-required |
| 11 | `agent_uid` | `int(11)` | 是 |  |  | 审核人 | internal | business-field | semantic-review-required |
| 12 | `update_time` | `datetime` | 是 |  |  | 操作时间     | internal | business-field | semantic-review-required |
| 13 | `remarks` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 14 | `time_stamp` | `int(11)` | 否 |  |  | 时间戳，用于时间跨度查询用，格式为：20201212 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `agency_matter_items`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：代办事项 子类关联关系表


| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键自增ID | internal | relation-key | server-filter-only |
| 2 | `matter_id` | `int(11)` | 是 |  |  | agency_matter表主键ID | internal | relation-key | server-filter-only |
| 3 | `coupon_id` | `int(11)` | 是 |  |  | 优惠券ID | internal | relation-key | server-filter-only |
| 4 | `coupon_number` | `int(11)` | 是 |  |  | 优惠券数量 | internal | business-field | semantic-review-required |
| 5 | `create_time` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 6 | `update_Time` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 是 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `user_coupon_id` | `int(11)` | 是 |  |  | 用户优惠券id | internal | relation-key | server-filter-only |
| 9 | `handle_type` | `int(11)` | 是 |  |  | 类型：1、发起   2、核销 | internal | business-field | semantic-review-required |
| 10 | `prepaid_card_id` | `int(11)` | 是 |  |  | 【审核卡用】卡id(储值卡) | restricted | relation-key | deny |
| 11 | `card_price` | `decimal(10,2)` | 是 |  |  | 【审核卡用】余金额(次数) | internal | business-field | semantic-review-required |
| 12 | `validity_date` | `datetime` | 是 |  |  | 【审核卡用】到期时间 | internal | business-field | semantic-review-required |
| 13 | `Is_add_consumption` | `tinyint(1)` | 是 |  |  | 【审核卡用】是否新增财务流水 | internal | business-field | semantic-review-required |
| 14 | `pay_way` | `int(11)` | 是 |  |  | 【审核卡用】付款方式 1现金 2POS 3微信 4支付宝 | internal | business-field | semantic-review-required |
| 15 | `pay_date` | `datetime` | 是 |  |  | 【审核卡用】付款时间 | internal | business-field | semantic-review-required |
| 16 | `pay_price` | `decimal(10,2)` | 是 |  |  | 【审核卡用】付款金额 | internal | business-field | semantic-review-required |
| 17 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 【审核卡用】核销卡用，调整的数值 | internal | business-field | semantic-review-required |
| 18 | `consumption_tag` | `int(11)` | 是 |  |  |  【审核卡用】操作方式 2 核减，3返还，4赠送 | internal | business-field | semantic-review-required |
| 19 | `consumption_type` | `int(11)` | 是 |  |  |  【审核卡用】调整项：0 计次，1 金额，2积分，3印章 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `agency_matter_items_service`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：代办事项针对建卡核销卡的服务项目表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `Id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `agent_item_id` | `int(11)` | 是 |  |  | 代办事项明细表中，卡对应的服务项目 | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 是 |  |  | 项目ID | internal | relation-key | server-filter-only |
| 4 | `item_name` | `varchar(255)` | 是 |  |  | 项目名称 | internal | business-field | semantic-review-required |
| 5 | `item_unit` | `varchar(255)` | 是 |  |  | 项目单位 | internal | business-field | semantic-review-required |
| 6 | `operation_value` | `decimal(10,2)` | 是 |  |  | 调整的次数  创建会员子卡时， 如果卡类型是 2时限卡，那么非赠送项目默认值 前端传99999 | internal | business-field | semantic-review-required |
| 7 | `operation_price` | `decimal(10,2)` | 是 |  |  | 调整的金额 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（Id）

### `agent`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：代理

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 代理的UID | internal | subject-or-relation-key | server-filter-only |
| 3 | `agent_name` | `varchar(50)` | 是 |  |  | 代理名称 | internal | business-field | semantic-review-required |
| 4 | `agent_province` | `varchar(50)` | 是 |  |  | 所在省 | internal | business-field | semantic-review-required |
| 5 | `agent_city` | `varchar(50)` | 是 |  |  | 所在市 | internal | business-field | semantic-review-required |
| 6 | `agent_balance` | `decimal(10,2)` | 是 |  |  | 账户余额 | internal | business-field | semantic-review-required |
| 7 | `wechat_code` | `varchar(50)` | 是 |  |  | 微信号 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | 状态-1 删除 1正常 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `agent_matter_user_coupon`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `matter_id` | `int(11)` | 否 |  |  | 代办 事项ID | internal | relation-key | server-filter-only |
| 3 | `user_coupon_id` | `int(11)` | 否 | MUL |  | 用户优惠券ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `sponsor_uid` | `int(11)` | 否 |  |  | 发起人ID | internal | business-field | semantic-review-required |
| 6 | `agent_uid` | `int(11)` | 否 |  |  | 审核人ID | internal | business-field | semantic-review-required |
| 7 | `agent_state` | `int(11)` | 否 |  |  | 审核 状态0待审核 1审核成功 -1驳回 | internal | business-field | semantic-review-required |
| 8 | `handle_type` | `int(11)` | 否 |  |  | 代办事项类型，1发放审核，2核销审核 | internal | business-field | semantic-review-required |
| 9 | `create_time` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_couponId`：非唯一 BTREE（user_coupon_id）

### `agent_store`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id。
表注释：代理店铺关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `agent_id` | `int(11)` | 否 |  |  | 代理ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 | internal | business-field | semantic-review-required |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `Index_storeid`：非唯一 BTREE（store_id）
- `PRIMARY`：唯一 BTREE（id）

### `agent_store_record`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺的id | internal | store-scope | server-filter-only |
| 3 | `agent_id` | `int(11)` | 是 |  |  | 接口人id | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 是 |  |  | 状态 | internal | business-field | semantic-review-required |
| 5 | `now_agent_id` | `int(11)` | 是 |  |  | 当前接口人id | internal | relation-key | server-filter-only |
| 6 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `alipay_auth_info`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `tenant_id` | `int(11)` | 是 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 4 | `user_id` | `varchar(16)` | 是 |  |  | 支付宝用户的唯一标识。以2088开头的16位数字 | internal | subject-or-relation-key | server-filter-only |
| 5 | `access_token` | `varchar(255)` | 是 |  |  | 访问令牌。通过该令牌调用需要授权类接口 | restricted | business-field | deny |
| 6 | `expires_in` | `int(11)` | 是 |  |  | 访问令牌的有效时间，单位是秒。 | internal | business-field | semantic-review-required |
| 7 | `refresh_token` | `varchar(255)` | 是 |  |  | 刷新令牌。通过该令牌可以刷新access_token | restricted | business-field | deny |
| 8 | `re_expires_in` | `int(11)` | 是 |  |  | 刷新令牌的有效时间，单位是秒。 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 是 |  |  | 状态：0未授权 1已授权 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 14 | `auth_app_id` | `varchar(255)` | 是 |  |  | 支付宝三方小程序APPID | internal | relation-key | server-filter-only |
| 15 | `reject_reason` | `varchar(500)` | 是 |  |  | 拒绝的原因 | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `ant_shop_id` | `varchar(255)` | 是 |  |  | 蚂蚁门店ID | internal | relation-key | server-filter-only |
| 18 | `ant_shop_order_id` | `varchar(255)` | 是 |  |  | 蚂蚁门店审核单ID | internal | relation-key | server-filter-only |
| 19 | `ant_shop_reason` | `varchar(500)` | 是 |  |  | 蚂蚁门店审核失败原因 | internal | business-field | semantic-review-required |
| 20 | `current_version` | `varchar(20)` | 是 |  | 0.0.1 | 当前版本 | internal | business-field | semantic-review-required |
| 21 | `current_version_state` | `int(11)` | 是 |  | -1 | 当前版本审核状态  -3 已退回开发版；  -2 已撤销审核； -1 带上传模板；0 待提交审核；1 开发中； 2 审核中 ； 3 审核通过； 4 审核驳回； 5 已上架 ；6 灰度中； 7 已下架 | internal | business-field | semantic-review-required |
| 22 | `template_version` | `varchar(20)` | 是 |  | 0.0.1 | 模板版本 | internal | business-field | semantic-review-required |
| 23 | `app_template_name` | `varchar(50)` | 是 |  |  | 订购小程序模板名称 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `alipay_marketing_recruit_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：招商报名记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键自增 | internal | relation-key | server-filter-only |
| 2 | `enroll_id` | `varchar(50)` | 否 |  |  | 报名id 第三方返回 | internal | relation-key | server-filter-only |
| 3 | `out_no` | `varchar(50)` | 否 |  |  | 外部单号(活动id+MD5报名计划id) | internal | business-field | semantic-review-required |
| 4 | `coupon_center_id` | `varchar(50)` | 否 |  |  | 活动id | internal | relation-key | server-filter-only |
| 5 | `store_id` | `varchar(50)` | 否 |  |  | 商店id | internal | store-scope | server-filter-only |
| 6 | `plan_id` | `varchar(50)` | 否 |  |  | 招商方案id | internal | relation-key | server-filter-only |
| 7 | `material_name` | `varchar(50)` | 是 |  |  | 素材名称 | internal | business-field | semantic-review-required |
| 8 | `material_description` | `varchar(100)` | 是 |  |  | 素材描述 | internal | business-field | semantic-review-required |
| 9 | `material_data` | `varchar(500)` | 是 |  |  | 素材内容 json | internal | business-field | semantic-review-required |
| 10 | `status` | `int(11)` | 否 |  |  |  报名状态：1 审核中；2 通过；3 不通过；4 已取消；5 已下线； | internal | business-field | semantic-review-required |
| 11 | `remark` | `varchar(500)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `alipay_marketing_recruit_plan`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：无。
表注释：招商报名方案

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键自增 | internal | relation-key | server-filter-only |
| 2 | `plan_id` | `varchar(50)` | 否 |  |  | 方案id | internal | relation-key | server-filter-only |
| 3 | `plan_name` | `varchar(50)` | 否 |  |  | 方案名称 | internal | business-field | semantic-review-required |
| 4 | `description` | `varchar(500)` | 是 |  |  | 描述 | internal | business-field | semantic-review-required |
| 5 | `enroll_end_time` | `datetime` | 是 |  |  | 报名结束时间 | internal | business-field | semantic-review-required |
| 6 | `enroll_start_time` | `datetime` | 是 |  |  | 报名开始时间 | internal | business-field | semantic-review-required |
| 7 | `logo` | `varchar(500)` | 是 |  |  | logo | internal | business-field | semantic-review-required |
| 8 | `status` | `varchar(50)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 9 | `plan_detail` | `varchar(1000)` | 否 |  |  | 方案详情（json） | internal | business-field | semantic-review-required |
| 10 | `create_time` | `datetime` | 否 |  |  | 添加时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `alliance`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：店铺联盟

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 店铺联盟 | internal | relation-key | server-filter-only |
| 2 | `alliance_name` | `varchar(20)` | 是 |  |  | 名称 | internal | business-field | semantic-review-required |
| 3 | `alliance_type` | `int(11)` | 否 |  |  | 联盟类型：0异业推广 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  |  | -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 5 | `is_open_alliance_card` | `tinyint(1)` | 否 |  |  | 是否开启了联盟卡 | internal | business-field | semantic-review-required |
| 6 | `store_id` | `int(11)` | 否 |  |  | 发起店铺 | internal | store-scope | server-filter-only |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `alliance_card`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：联盟卡

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `alliance_id` | `int(11)` | 否 |  |  | 联盟id | internal | relation-key | server-filter-only |
| 3 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 4 | `card_type` | `int(11)` | 否 |  |  |  '类型：0计次，1储值 2时效卡 3权益卡 4安心充卡' | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 状态：0禁用 1启用 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `alliance_customer_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：联盟内顾客记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `alliance_id` | `int(11)` | 否 |  |  | 联盟id | internal | relation-key | server-filter-only |
| 3 | `to_store_id` | `int(11)` | 否 |  |  | 顾客到店id | internal | relation-key | server-filter-only |
| 4 | `for_store_id` | `int(11)` | 否 |  |  | 推荐店铺id | internal | relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 6 | `log_tag` | `int(11)` | 否 |  |  | 1购卡 5消费 | internal | business-field | semantic-review-required |
| 7 | `customer_source` | `int(11)` | 否 |  |  | 顾客来源：0卡 1券 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 1启用 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `area_mobile`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：手机号码归属地

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `pref` | `varchar(5)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 3 | `mobile_header` | `varchar(20)` | 否 | MUL |  | 前7位手机号 | sensitive | business-field | masked-or-filter-only |
| 4 | `isp` | `varchar(10)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 5 | `province` | `varchar(30)` | 是 |  |  | 省 | internal | business-field | semantic-review-required |
| 6 | `city` | `varchar(30)` | 是 |  |  | 市 | internal | business-field | semantic-review-required |
| 7 | `city_code` | `varchar(10)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `area_code` | `varchar(10)` | 是 |  |  | 区号 | internal | business-field | semantic-review-required |
| 9 | `area_simple` | `varchar(4)` | 是 |  |  | 简称 | internal | business-field | semantic-review-required |
| 10 | `email_code` | `varchar(10)` | 是 |  |  | 邮编 | sensitive | business-field | masked-or-filter-only |
| 11 | `state` | `int(11)` | 是 |  |  | 状态 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_mobileheader`：非唯一 BTREE（mobile_header）

### `article`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键唯一标识 | internal | relation-key | server-filter-only |
| 2 | `title` | `varchar(100)` | 否 |  |  | 标题 | internal | business-field | semantic-review-required |
| 3 | `article_type_id` | `int(11)` | 否 |  |  | 文章类型 | internal | relation-key | server-filter-only |
| 4 | `is_top` | `tinyint(1)` | 是 |  |  | 是否置顶 | internal | business-field | semantic-review-required |
| 5 | `keyword` | `varchar(200)` | 是 |  |  | 关键词 | internal | business-field | semantic-review-required |
| 6 | `article_describe` | `varchar(500)` | 是 |  |  | 描述 | internal | business-field | semantic-review-required |
| 7 | `author` | `varchar(20)` | 是 |  |  | 作者 | internal | business-field | semantic-review-required |
| 8 | `abstract` | `varchar(500)` | 是 |  |  | 摘要 | internal | business-field | semantic-review-required |
| 9 | `content` | `text` | 是 |  |  | 内容 | sensitive-unstructured | business-field | deny |
| 10 | `order_by` | `int(11)` | 是 |  | 0 | 排序字段 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 状态 -1 删除 0暂停 1开启 | internal | business-field | semantic-review-required |
| 12 | `url` | `varchar(255)` | 否 |  |  | 文章跳转的路径 | internal | business-field | semantic-review-required |
| 13 | `url_type` | `int(11)` | 否 |  |  | 标识当前文章状态；0-内容，1-url跳转 | internal | business-field | semantic-review-required |
| 14 | `store_type_id` | `varchar(10)` | 是 |  | 0 | 行业id | internal | relation-key | server-filter-only |
| 15 | `article_img` | `varchar(255)` | 是 |  |  | 文章图片 | internal | business-field | semantic-review-required |
| 16 | `article_pv` | `int(11)` | 是 |  | 0 | 文章浏览量 | internal | business-field | semantic-review-required |
| 17 | `is_synchro_wechat` | `tinyint(4)` | 是 |  | 0 | 是否同步微信；0-不同步，1-同步 | internal | business-field | semantic-review-required |
| 18 | `synchro_wechat_state` | `int(11)` | 是 |  | 2 | 公众号文章同步状态；0-失败，1-成功，2-未执行 | internal | business-field | semantic-review-required |
| 19 | `synchro_wechat_date` | `datetime` | 是 |  |  | 公众号文章同步时间 | internal | business-field | semantic-review-required |
| 20 | `synchro_wechat_type` | `varchar(20)` | 是 |  |  | 返回值-媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb），图文消息（news） | internal | business-field | semantic-review-required |
| 21 | `synchro_wechat_media_id` | `varchar(100)` | 是 |  |  | 返回值-媒体文件/图文消息上传后获取的唯一标识 | internal | relation-key | server-filter-only |
| 22 | `synchro_wechat_created_at` | `datetime` | 是 |  |  | 返回值-媒体文件上传时间 | internal | business-field | semantic-review-required |
| 23 | `synchro_wechat_thumb_media_id` | `varchar(100)` | 是 |  |  | 图文消息缩略图的media | internal | relation-key | server-filter-only |
| 24 | `synchro_wechat_show_cover_pic` | `tinyint(4)` | 是 |  | 1 | 是否显示封面，1为显示，0为不显示 | internal | business-field | semantic-review-required |
| 25 | `synchro_wechat_need_open_comment` | `tinyint(4)` | 是 |  | 0 | 是否打开评论，0不打开，1打开 | internal | business-field | semantic-review-required |
| 26 | `synchro_wechat_only_fans_can_comment` | `tinyint(4)` | 是 |  | 0 | 是否粉丝才可评论，0所有人可评论，1粉丝才可评论 | internal | business-field | semantic-review-required |
| 27 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 28 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 29 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 30 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `article_type`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 唯一标识 | internal | relation-key | server-filter-only |
| 2 | `type_name` | `varchar(30)` | 否 |  |  | 类型名称 | internal | business-field | semantic-review-required |
| 3 | `state` | `int(11)` | 否 |  |  | -1 删除 0停用 1正常 | internal | business-field | semantic-review-required |
| 4 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `ask_for_items`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键自增标识 | internal | relation-key | server-filter-only |
| 2 | `ask_for_type` | `int(11)` | 否 |  |  | 物料类别 0台牌 1合同 2 海报 3贴纸 | internal | business-field | semantic-review-required |
| 3 | `consignee` | `varchar(12)` | 是 |  |  | 收件人 | internal | business-field | semantic-review-required |
| 4 | `receive_mobile` | `varchar(20)` | 是 |  |  | 收件人电话 | sensitive | business-field | masked-or-filter-only |
| 5 | `receive_email` | `varchar(30)` | 是 |  |  | 收件人邮箱 | sensitive | business-field | masked-or-filter-only |
| 6 | `receive_povince` | `varchar(20)` | 是 |  |  | 收货省 | internal | business-field | semantic-review-required |
| 7 | `receive_city` | `varchar(20)` | 是 |  |  | 收货市 | internal | business-field | semantic-review-required |
| 8 | `receive_district` | `varchar(20)` | 是 |  |  | 收货区/县 | internal | business-field | semantic-review-required |
| 9 | `receive_address` | `varchar(100)` | 是 |  |  | 收货详细地址 | sensitive | business-field | masked-or-filter-only |
| 10 | `express_name` | `varchar(20)` | 是 |  |  | 快递名称 | internal | business-field | semantic-review-required |
| 11 | `express_no` | `varchar(20)` | 是 |  |  | 快递单号 | internal | business-field | semantic-review-required |
| 12 | `express_date` | `datetime` | 是 |  |  | 寄出时间 | internal | business-field | semantic-review-required |
| 13 | `express_state` | `int(11)` | 是 |  |  | 快递状态 0未发送 1已发送 | internal | business-field | semantic-review-required |
| 14 | `remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 15 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 16 | `tenant_id` | `int(11)` | 是 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 17 | `state` | `int(11)` | 否 |  | 0 | -1 删除 0 正常 1其它 | internal | business-field | semantic-review-required |
| 18 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 19 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 20 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 21 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `bank`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `bank_code` | `varchar(10)` | 否 |  |  | 银行编码 | internal | business-field | semantic-review-required |
| 3 | `bank_name` | `varchar(20)` | 否 |  |  | 银行名称 | internal | business-field | semantic-review-required |
| 4 | `other_name` | `varchar(50)` | 是 |  |  | 用于对接小微商户的银行名称 | internal | business-field | semantic-review-required |
| 5 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 1 | 状态 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `bank_branch`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `parent_bank_name` | `varchar(50)` | 否 |  |  | 父级银行名称 | internal | business-field | semantic-review-required |
| 3 | `parent_bank_code` | `varchar(30)` | 否 |  |  | 父级银行编码 | internal | business-field | semantic-review-required |
| 4 | `province_name` | `varchar(30)` | 否 |  |  | 支行所在省 | internal | business-field | semantic-review-required |
| 5 | `province_code` | `varchar(10)` | 否 |  |  | 支行所在省编码 | internal | business-field | semantic-review-required |
| 6 | `city_name` | `varchar(30)` | 否 |  |  | 支行所在市 | internal | business-field | semantic-review-required |
| 7 | `city_code` | `varchar(30)` | 否 |  |  | 支行编码 | internal | business-field | semantic-review-required |
| 8 | `bank_branch_name` | `varchar(100)` | 否 |  |  | 支行名称 | internal | business-field | semantic-review-required |
| 9 | `bank_branch_code` | `varchar(30)` | 否 |  |  | 支行编码 | internal | business-field | semantic-review-required |
| 10 | `bank_branch_simple_name` | `varchar(50)` | 否 |  |  | 支行名称简称 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `banner`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：banner

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `banner_type_id` | `int(11)` | 否 |  | 0 | banner_type的主键id | internal | relation-key | server-filter-only |
| 3 | `store_type_id` | `varchar(10)` | 否 |  |  | 店铺类型ID | internal | relation-key | server-filter-only |
| 4 | `name` | `varchar(100)` | 否 |  |  | banner名称 | internal | business-field | semantic-review-required |
| 5 | `img` | `varchar(255)` | 否 |  |  | 图片 | internal | business-field | semantic-review-required |
| 6 | `title` | `varchar(200)` | 否 |  |  | 标题 | internal | business-field | semantic-review-required |
| 7 | `describe` | `varchar(500)` | 否 |  |  | 描述 | internal | business-field | semantic-review-required |
| 8 | `link_type` | `int(11)` | 否 |  | 0 | 跳转类型；0-无，1-app内部，2-外链 | internal | business-field | semantic-review-required |
| 9 | `link_url` | `varchar(255)` | 否 |  |  | 跳转地址；link_type为1需要定义标识，为2则是跳转地址 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  | 1 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 11 | `order_by` | `int(11)` | 否 |  | 0 | 排序字段 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `banner_type`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 3 | `order_by` | `int(11)` | 否 |  | 0 | 排序字段，越小越在前 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  | 1 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 5 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 6 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `banner_user`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `Bid` | `int(11)` | 是 |  |  | Banner ID | internal | business-field | semantic-review-required |
| 3 | `Uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `Create_time` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `business_orders`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `tid` | `bigint(20)` | 否 |  |  | 订单id | internal | business-field | semantic-review-required |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `pid` | `int(11)` | 否 |  |  | 商品id | internal | business-field | semantic-review-required |
| 5 | `order_type` | `int(11)` | 否 |  |  | 订单类型 0短信包 1物料 ，2硬件，5坚果币 | internal | business-field | semantic-review-required |
| 6 | `poster_type` | `int(11)` | 否 |  |  | 类型：朋友圈海报，1物料（购卡送券）2抽奖 | internal | business-field | semantic-review-required |
| 7 | `poster_custom_title` | `varchar(30)` | 是 |  |  | 定制title | internal | business-field | semantic-review-required |
| 8 | `p_title` | `varchar(50)` | 是 |  |  | 商品名称 | internal | business-field | semantic-review-required |
| 9 | `p_pic` | `varchar(100)` | 否 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 10 | `price` | `decimal(10,2)` | 否 |  |  | 单价 | internal | business-field | semantic-review-required |
| 11 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 12 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 13 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 14 | `behind_nut_gold` | `int(11)` | 否 |  | 0 | 充值后的坚果币 | internal | business-field | semantic-review-required |
| 15 | `num` | `int(11)` | 否 |  |  | 购买数量 | internal | business-field | semantic-review-required |
| 16 | `state` | `int(11)` | 否 |  |  | 订单状态：0未付款，1已付款未发货，2已发货，3交易成功,4取消 | internal | business-field | semantic-review-required |
| 17 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 18 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 19 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `business_receive_address`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | UNI |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `receive_name` | `varchar(12)` | 否 |  |  | 收件人姓名 | internal | business-field | semantic-review-required |
| 4 | `receive_mobile` | `varchar(20)` | 否 |  |  | 收件人电话 | sensitive | business-field | masked-or-filter-only |
| 5 | `receive_email` | `varchar(50)` | 否 |  |  | 收件人邮箱 | sensitive | business-field | masked-or-filter-only |
| 6 | `receive_province` | `varchar(20)` | 否 |  |  | 收货省 | internal | business-field | semantic-review-required |
| 7 | `receive_city` | `varchar(20)` | 否 |  |  | 收货市 | internal | business-field | semantic-review-required |
| 8 | `receive_district` | `varchar(20)` | 否 |  |  | 收货区 | internal | business-field | semantic-review-required |
| 9 | `receive_address` | `varchar(100)` | 否 |  |  | 收货详细地址 | sensitive | business-field | masked-or-filter-only |
| 10 | `receiver_zip` | `varchar(20)` | 否 |  |  | 收货邮编 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1启用 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：唯一 BTREE（store_id）

### `business_trade`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：商家订单

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `order_type` | `int(11)` | 否 |  |  | 订单类型 0短信 1物料 3硬件 5坚果币 | internal | business-field | semantic-review-required |
| 5 | `poster_type` | `int(11)` | 否 |  |  | 类型：朋友圈海报，1物料（购卡送券）2抽奖 | internal | business-field | semantic-review-required |
| 6 | `soft_order_id` | `int(11)` | 否 |  | 0 | 软件订单ID | internal | relation-key | server-filter-only |
| 7 | `receive_name` | `varchar(12)` | 是 |  |  | 收件人姓名 | internal | business-field | semantic-review-required |
| 8 | `receive_mobile` | `varchar(20)` | 是 |  |  | 收件人电话 | sensitive | business-field | masked-or-filter-only |
| 9 | `receive_email` | `varchar(50)` | 是 |  |  | 收件人邮箱 | sensitive | business-field | masked-or-filter-only |
| 10 | `receive_province` | `varchar(20)` | 是 |  |  | 收货省 | internal | business-field | semantic-review-required |
| 11 | `receive_city` | `varchar(20)` | 是 |  |  | 收货市 | internal | business-field | semantic-review-required |
| 12 | `receive_district` | `varchar(20)` | 是 |  |  | 收货区/县 | internal | business-field | semantic-review-required |
| 13 | `receive_address` | `varchar(100)` | 是 |  |  | 收货详细地址 | sensitive | business-field | masked-or-filter-only |
| 14 | `receiver_zip` | `varchar(10)` | 是 |  |  | 收货人的邮编 | internal | business-field | semantic-review-required |
| 15 | `express_name` | `varchar(20)` | 是 |  |  | 快递名称 | internal | business-field | semantic-review-required |
| 16 | `express_no` | `varchar(20)` | 是 |  |  | 快递单号 | internal | business-field | semantic-review-required |
| 17 | `express_date` | `datetime` | 是 |  |  | 寄出时间 | internal | business-field | semantic-review-required |
| 18 | `express_state` | `int(11)` | 否 |  |  | 快递状态 0未发送 1已发送 2已送达 | internal | business-field | semantic-review-required |
| 19 | `total_price` | `decimal(10,2)` | 是 |  |  | 订单总金额 | internal | business-field | semantic-review-required |
| 20 | `discount_price` | `decimal(10,2)` | 否 |  |  | 优惠金额 | internal | business-field | semantic-review-required |
| 21 | `post_price` | `decimal(10,2)` | 否 |  |  | 邮费 | internal | business-field | semantic-review-required |
| 22 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 23 | `buyer_message` | `varchar(50)` | 否 |  |  | 买家留言 | sensitive-unstructured | business-field | deny |
| 24 | `seller_memo` | `varchar(50)` | 是 |  |  | 卖家备注 | internal | business-field | semantic-review-required |
| 25 | `p_num` | `int(11)` | 否 |  |  | 商品数量 | internal | business-field | semantic-review-required |
| 26 | `item_quantity` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 27 | `pay_type` | `int(11)` | 否 |  |  | 支付方式0预留 1微信 2支付宝 | internal | business-field | semantic-review-required |
| 28 | `state` | `int(11)` | 否 |  |  | 订单状态：0未付款，1已付款未发货，2已发货，3交易成功,4取消 | internal | business-field | semantic-review-required |
| 29 | `pay_date` | `datetime` | 是 |  |  | 付款时间 | internal | business-field | semantic-review-required |
| 30 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 31 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 32 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `bussiness_order_info`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `tid` | `bigint(20)` | 是 |  |  | 订单id | internal | business-field | semantic-review-required |
| 3 | `oid` | `bigint(20)` | 是 |  |  | 子订单id | internal | business-field | semantic-review-required |
| 4 | `pcard_id` | `int(11)` | 是 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 5 | `state` | `int(11)` | 是 |  |  | 状态 1正常 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `card_password`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 转让者id | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 转让者会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_type` | `int(11)` | 否 |  |  | 卡类型 0储值 1计次 | internal | business-field | semantic-review-required |
| 6 | `card_child_id` | `int(11)` | 否 |  |  | 转让者子卡ID | internal | relation-key | server-filter-only |
| 7 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 8 | `card_value` | `decimal(10,2)` | 否 |  |  | 转让数值 | internal | business-field | semantic-review-required |
| 9 | `random_param` | `varchar(40)` | 否 |  |  | 随机参数 | internal | business-field | semantic-review-required |
| 10 | `pass_type` | `int(11)` | 否 |  | 0 | 类型：0转让 1发送 | internal | business-field | semantic-review-required |
| 11 | `transferee_uid` | `int(11)` | 否 |  |  | 受让人id | internal | business-field | semantic-review-required |
| 12 | `transferee_card_id` | `int(11)` | 否 |  |  | 受让人卡id | internal | relation-key | server-filter-only |
| 13 | `transferee_card_child_id` | `int(11)` | 否 |  |  | 受让人子卡id | internal | relation-key | server-filter-only |
| 14 | `background_image` | `varchar(255)` | 是 |  |  | 背景图片 | internal | business-field | semantic-review-required |
| 15 | `message` | `varchar(100)` | 是 |  |  | 祝福语 | sensitive-unstructured | business-field | deny |
| 16 | `state` | `int(11)` | 否 |  |  | 状态 0未激活 1已使用 -1删除 -2转让失败 | internal | business-field | semantic-review-required |
| 17 | `state_reason` | `varchar(50)` | 是 |  |  | 失败原因 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 19 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 20 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 21 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `card_template`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：系统会员卡模板

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 | 店铺id | internal | store-scope | server-filter-only |
| 3 | `store_type_id` | `varchar(50)` | 否 |  |  | 店铺类型id | internal | relation-key | server-filter-only |
| 4 | `tag_id` | `int(11)` | 否 |  | 0 | 标签id | internal | relation-key | server-filter-only |
| 5 | `card_img` | `varchar(100)` | 否 |  |  | 底图 | internal | business-field | semantic-review-required |
| 6 | `wx_file_url` | `varchar(200)` | 是 |  |  | 微信图片路径 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(2)` | 否 |  | 1 | 状态 1启用 | internal | business-field | semantic-review-required |
| 8 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `card_template_copy`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：系统会员卡模板

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 | 店铺id | internal | store-scope | server-filter-only |
| 3 | `store_type_id` | `varchar(50)` | 否 |  |  | 店铺类型id | internal | relation-key | server-filter-only |
| 4 | `tag_id` | `int(11)` | 否 |  | 0 | 标签id | internal | relation-key | server-filter-only |
| 5 | `card_img` | `varchar(100)` | 否 |  |  | 底图 | internal | business-field | semantic-review-required |
| 6 | `wx_file_url` | `varchar(200)` | 是 |  |  | 微信图片路径 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  | 1 | 状态 1启用 | internal | business-field | semantic-review-required |
| 8 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `card_used_time`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 营业时间自增主键 | internal | relation-key | server-filter-only |
| 2 | `week_id` | `bigint(20)` | 否 |  |  | 可用星期id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `bigint(20)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `prepaid_card_id` | `bigint(20)` | 否 |  |  | 储值卡id | restricted | relation-key | deny |
| 5 | `begin_time` | `varchar(20)` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 6 | `end_time` | `varchar(20)` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1正常 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `card_used_week`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 营业时间自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `prepaid_card_id` | `bigint(20)` | 否 |  |  | 储值卡id | restricted | relation-key | deny |
| 4 | `week_info` | `varchar(20)` | 否 |  |  | 营业日期1,2,7 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `bigint(20)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1正常 | internal | business-field | semantic-review-required |
| 7 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `channel_store_relation`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `channel_id` | `int(11)` | 否 |  |  | 渠道的id | internal | relation-key | server-filter-only |
| 3 | `channel_users_id` | `int(11)` | 否 |  |  | 渠道用户的id | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 是 |  |  | 店铺的id | internal | store-scope | server-filter-only |
| 5 | `state` | `int(11)` | 是 |  |  | 状态；1-正常，0-关闭 | internal | business-field | semantic-review-required |
| 6 | `store_service_begin_date` | `datetime` | 是 |  |  | 店铺开始时间 | internal | business-field | semantic-review-required |
| 7 | `store_service_end_date` | `datetime` | 是 |  |  | 店铺结束时间 | internal | business-field | semantic-review-required |
| 8 | `now_soft_version` | `int(11)` | 是 |  |  | 当前的版本 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `child_card_trigger_log`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `child_card_id` | `int(11)` | 否 |  |  | 修改的子卡ID | internal | relation-key | server-filter-only |
| 3 | `old_card_price` | `decimal(10,2)` | 否 |  |  | 原有卡余额 | internal | business-field | semantic-review-required |
| 4 | `new_card_price` | `decimal(10,2)` | 否 |  |  | 修改后卡余额 | internal | business-field | semantic-review-required |
| 5 | `old_consumption_price` | `decimal(10,2)` | 否 |  |  | 修改前的消费金额 | internal | business-field | semantic-review-required |
| 6 | `new_consumption_price` | `decimal(10,2)` | 否 |  |  | 修改后的消费金额 | internal | business-field | semantic-review-required |
| 7 | `old_last_date` | `datetime` | 是 |  |  | 修改前最后消费时间 | internal | business-field | semantic-review-required |
| 8 | `new_last_date` | `datetime` | 是 |  |  | 修改后最后消费时间 | internal | business-field | semantic-review-required |
| 9 | `old_validity_date` | `date` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `new_validity_date` | `date` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 数据创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `cloud_store_customer_setting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `Id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `background_color` | `varchar(255)` | 是 |  |  | 背景颜色 | internal | business-field | semantic-review-required |
| 4 | `is_show_pay` | `tinyint(1)` | 否 |  | 0 | 是否展示支付按钮 | internal | business-field | semantic-review-required |
| 5 | `recharge_text` | `varchar(20)` | 是 |  | 充值 | 充值文字 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  | 1 |  | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（Id）

### `cloud_store_index_banner`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `Id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `img_url` | `varchar(500)` | 否 |  |  | 图片地址 | internal | business-field | semantic-review-required |
| 4 | `jump_url` | `varchar(500)` | 是 |  |  | 跳转链接 | internal | business-field | semantic-review-required |
| 5 | `app_id` | `varchar(50)` | 是 |  |  | 跳转小程序appid | internal | relation-key | server-filter-only |
| 6 | `type` | `int(11)` | 是 |  | 0 | 跳转类型 0-网页；1-内部小程序；2-外部小程序；-1-不跳转； | internal | business-field | semantic-review-required |
| 7 | `is_system` | `tinyint(1)` | 否 |  | 0 | 是否系统 | internal | business-field | semantic-review-required |
| 8 | `template_tag` | `int(11)` | 否 |  | 0 | 模板标记分类（用于区分模板头图） | internal | business-field | semantic-review-required |
| 9 | `img_type` | `int(11)` | 否 |  | 0 | 图片类型 0-banner图；1-advertise广告图 | internal | business-field | semantic-review-required |
| 10 | `product_img` | `varchar(255)` | 是 |  |  | 跳转餐品/商品的图片地址 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 15 | `state` | `int(11)` | 否 |  | 1 | 1正常 -1删除 | internal | business-field | semantic-review-required |
| 16 | `sort` | `int(11)` | 否 |  |  | 排序号 | internal | business-field | semantic-review-required |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（Id）

### `cloud_store_index_title`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `Id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `title` | `varchar(50)` | 否 |  | 点餐 | 标题 | internal | business-field | semantic-review-required |
| 4 | `child_title` | `varchar(50)` | 是 |  |  | 子标题 | internal | business-field | semantic-review-required |
| 5 | `shop_title` | `varchar(50)` | 是 |  |  | 商城标题 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 1 |  | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（Id）

### `commission_cashout_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：佣金提现记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 是 |  |  | 状态：0审核中，1通过，2驳回 | internal | business-field | semantic-review-required |
| 5 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 6 | `receiver` | `varchar(255)` | 是 |  |  | 收款人姓名 | internal | business-field | semantic-review-required |
| 7 | `receive_account` | `varchar(255)` | 是 |  |  | 收款账号 | internal | business-field | semantic-review-required |
| 8 | `receive_channel` | `varchar(255)` | 是 |  |  | 收款渠道 | internal | business-field | semantic-review-required |
| 9 | `cashout_price` | `decimal(10,2)` | 是 |  |  | 提现金额 | internal | business-field | semantic-review-required |
| 10 | `spare_price` | `decimal(10,2)` | 是 |  |  | 剩余可提现金额 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `common_reservation_controls`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `store_type` | `varchar(10)` | 否 |  |  | 店铺类型（仅对store=0有效） | internal | business-field | semantic-review-required |
| 4 | `control_name` | `varchar(50)` | 否 |  |  | 控件名称 | internal | business-field | semantic-review-required |
| 5 | `control_instructions` | `varchar(100)` | 否 |  |  | 控件说明 | internal | business-field | semantic-review-required |
| 6 | `control_type` | `varchar(20)` | 否 |  |  | 控件类型 input,radio,select.... | internal | business-field | semantic-review-required |
| 7 | `note` | `varchar(100)` | 否 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 8 | `is_must` | `tinyint(1)` | 否 |  |  | 是否必填项 | internal | business-field | semantic-review-required |
| 9 | `is_show` | `tinyint(1)` | 否 |  |  | 是否对C端展示 | internal | business-field | semantic-review-required |
| 10 | `order_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `common_reservation_controls_item`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `common_reservation_controls_id` | `int(11)` | 否 |  |  |  | internal | relation-key | server-filter-only |
| 4 | `item_name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 5 | `item_value` | `varchar(100)` | 否 |  |  | 值 | internal | business-field | semantic-review-required |
| 6 | `is_default` | `tinyint(1)` | 否 |  |  | 是否是默认 | internal | business-field | semantic-review-required |
| 7 | `is_show` | `tinyint(1)` | 否 |  |  | 是否对C端展示 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `complaint`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：投诉建议

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 | MUL |  | 投诉人id | internal | subject-or-relation-key | server-filter-only |
| 4 | `user_mobile` | `varchar(20)` | 是 |  |  | 投诉人手机 | sensitive | business-field | masked-or-filter-only |
| 5 | `complaint_type` | `int(11)` | 否 |  |  | 类型 0投诉，1建议 | internal | business-field | semantic-review-required |
| 6 | `complaint_reason` | `varchar(50)` | 是 |  |  | 投诉原因 | internal | business-field | semantic-review-required |
| 7 | `remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `state` | `int(11)` | 否 |  | 0 | 状态 -1删除 0未处理 2处理中 1处理完成  | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）
- `inx_uid`：非唯一 BTREE（uid）

### `complaint_img`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `complaint_id` | `bigint(20)` | 否 |  |  | 投诉id | internal | relation-key | server-filter-only |
| 3 | `complaint_info_id` | `bigint(20)` | 否 |  |  | 投诉详情id | internal | relation-key | server-filter-only |
| 4 | `img` | `varchar(100)` | 否 |  |  | 图片地址 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态 -1删除 1启用 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `complaint_info`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：投诉详细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `complaint_id` | `bigint(20)` | 否 |  |  | 投诉id | internal | relation-key | server-filter-only |
| 3 | `create_type` | `int(11)` | 否 |  |  | 发起类型 0顾客 1商家 3平台回复 | internal | business-field | semantic-review-required |
| 4 | `is_main` | `tinyint(1)` | 否 |  |  | 是否首次发起的回复 | internal | business-field | semantic-review-required |
| 5 | `is_img` | `tinyint(1)` | 否 |  |  | 是否包含图片文件 | internal | business-field | semantic-review-required |
| 6 | `complaint_content` | `varchar(255)` | 否 |  |  | 投诉或回复内容 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  | 0 | 状态 -1删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `cooperation_consult`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺主键 | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 | MUL |  | 用户主键 | internal | subject-or-relation-key | server-filter-only |
| 4 | `person_name` | `varchar(255)` | 是 |  |  | 姓名 | internal | business-field | semantic-review-required |
| 5 | `phone_number` | `varchar(20)` | 是 |  |  | 手机号 | sensitive | business-field | masked-or-filter-only |
| 6 | `source_type` | `int(11)` | 否 |  |  | 来源   0:小程序  1:官网  5:3980营销相关   7:官网-免费试用  8:官网-功能调研  9:官网-合作加盟  10:定制咨询 | internal | business-field | semantic-review-required |
| 7 | `intent_province` | `varchar(255)` | 是 |  |  | 意向省 | internal | business-field | semantic-review-required |
| 8 | `intent_city` | `varchar(255)` | 是 |  |  | 意向市 | internal | business-field | semantic-review-required |
| 9 | `team_user_num` | `int(11)` | 是 |  |  | 团队人数 | internal | business-field | semantic-review-required |
| 10 | `is_sales` | `int(11)` | 是 |  |  | 是否有销售经验 | internal | business-field | semantic-review-required |
| 11 | `is_manager` | `int(11)` | 是 |  |  | 是否有管理经验 | internal | business-field | semantic-review-required |
| 12 | `suggest` | `varchar(500)` | 是 |  |  | 建议 | internal | business-field | semantic-review-required |
| 13 | `costly_activity_id` | `int(11)` | 否 |  | 0 | 营销活动id | internal | relation-key | server-filter-only |
| 14 | `costly_activity_type` | `int(11)` | 否 |  | 0 | 营销类型；1-营销活动，2-会员卡宣传海报 | internal | business-field | semantic-review-required |
| 15 | `state` | `int(11)` | 否 |  |  | 状态：0 未联系，1 已联系 ，2 无需联系   | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(500)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 18 | `acc_source` | `varchar(100)` | 是 |  |  | 来源渠道 | internal | business-field | semantic-review-required |
| 19 | `user_ip` | `varchar(100)` | 是 |  |  | 访客请求IP | internal | business-field | semantic-review-required |
| 20 | `acc_medium` | `varchar(100)` | 是 |  |  | 推广方式 | internal | business-field | semantic-review-required |
| 21 | `acc_campaign` | `varchar(100)` | 是 |  |  | 推广计划 | internal | business-field | semantic-review-required |
| 22 | `acc_content` | `varchar(100)` | 是 |  |  | 推广 单元(业务标识) | sensitive-unstructured | business-field | deny |
| 23 | `semd` | `varchar(100)` | 是 |  |  | 访问的设备型号 | internal | business-field | semantic-review-required |
| 24 | `form_source` | `varchar(100)` | 是 |  |  | 表单来源 | internal | business-field | semantic-review-required |
| 25 | `acc_term` | `varchar(100)` | 是 |  |  | 推广关键词 | internal | business-field | semantic-review-required |
| 26 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 27 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `IX_STORE_ID`：非唯一 BTREE（store_id）
- `IX_UID`：非唯一 BTREE（uid）
- `PRIMARY`：唯一 BTREE（id）

### `cooperation_consult_record`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `consult_id` | `int(11)` | 是 | MUL |  | 咨询主键 | internal | relation-key | server-filter-only |
| 3 | `contact_user_id` | `int(11)` | 是 |  |  | 联系人ID（当前系统登陆人ID） | sensitive | relation-key | server-filter-only |
| 4 | `contact_user` | `varchar(255)` | 是 |  |  | 联系人 | sensitive | business-field | masked-or-filter-only |
| 5 | `contact_date` | `datetime` | 是 |  |  | 联系时间 | sensitive | business-field | masked-or-filter-only |
| 6 | `remark` | `varchar(500)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 7 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 是 |  |  | 本次状态：1 已联系 ，2 无需联系   | internal | business-field | semantic-review-required |

索引：
- `IX_CONSULT_ID`：非唯一 BTREE（consult_id）
- `PRIMARY`：唯一 BTREE（id）

### `copywriting`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：文案

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `writing_content` | `varchar(100)` | 否 |  |  | 内容 | sensitive-unstructured | business-field | deny |
| 3 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 4 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 5 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `copywriting_store_type`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：文案与店铺类型关联

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `copywriting_id` | `int(11)` | 否 |  |  | 文案ID | internal | relation-key | server-filter-only |
| 3 | `store_type_id` | `varchar(11)` | 否 |  |  | 店铺类型ID | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 5 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 6 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `costly_activity`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `name` | `varchar(255)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 3 | `describe` | `varchar(255)` | 否 |  |  | 描述 | internal | business-field | semantic-review-required |
| 4 | `nut_gold` | `int(11)` | 否 |  | 0 | 所需坚果币 | internal | business-field | semantic-review-required |
| 5 | `type` | `int(11)` | 否 |  | 0 | 类型；1-营销活动，2-会员宣传图 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 0 | 状态；0-无效，1-有效 | internal | business-field | semantic-review-required |
| 7 | `order_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `costly_activity_img`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `costly_activity_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 3 | `img` | `varchar(255)` | 否 |  |  | 地址 | internal | business-field | semantic-review-required |
| 4 | `order_by` | `int(11)` | 否 |  | 0 | 排序字段 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 6 | `update_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `costly_activity_tag`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `costly_activity_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 3 | `name` | `varchar(255)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 4 | `position` | `int(11)` | 否 |  | 0 | 标签位置；1-下方，2-右上角 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 7 | `update_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `coupon`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：优惠卷表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键Id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺Id | internal | store-scope | server-filter-only |
| 3 | `coupon_type` | `int(11)` | 否 |  |  | 类型 0代金券 1打折券 2服务券 3礼品券 | internal | business-field | semantic-review-required |
| 4 | `coupon_title` | `varchar(20)` | 否 |  |  | 标题 | internal | business-field | semantic-review-required |
| 5 | `coupon_img` | `varchar(70)` | 是 |  |  | 优惠券背景图 | internal | business-field | semantic-review-required |
| 6 | `coupon_icon` | `varchar(70)` | 是 |  |  | 图标 | internal | business-field | semantic-review-required |
| 7 | `coupon_bg_img` | `varchar(70)` | 是 |  |  | 卡包背景图 | internal | business-field | semantic-review-required |
| 8 | `is_use_vip` | `tinyint(1)` | 否 |  |  | 是否会员可用 | internal | business-field | semantic-review-required |
| 9 | `is_more` | `tinyint(1)` | 否 |  |  | 是否可以同时使用多张 | internal | business-field | semantic-review-required |
| 10 | `is_buy_card` | `tinyint(1)` | 否 |  |  | 是否只用于购买会员卡 | internal | business-field | semantic-review-required |
| 11 | `is_auditing` | `tinyint(1)` | 否 |  | 0 | 是否需要发放审核优惠券，默认是0(不需审核)，1为需要审核 | internal | business-field | semantic-review-required |
| 12 | `is_use_audit` | `tinyint(1)` | 否 |  | 0 | 使用优惠券是否需要审核，0 否 1是 | internal | business-field | semantic-review-required |
| 13 | `use_min_money` | `decimal(10,2)` | 否 |  | 0.00 | 最低消费限制 | internal | business-field | semantic-review-required |
| 14 | `coupon_value` | `decimal(10,2)` | 否 |  | 0.00 | 优惠卷面值（金额、折扣、现价） | internal | business-field | semantic-review-required |
| 15 | `original_price` | `decimal(10,2)` | 否 |  | 0.00 | 原价 | internal | business-field | semantic-review-required |
| 16 | `coupon_source` | `int(11)` | 是 |  |  | 创建源 来源 0其他 1活动 2 优惠中心 3店长赠送 | internal | business-field | semantic-review-required |
| 17 | `coupon_count` | `int(11)` | 否 |  |  | 优惠券数量   -1不限量 | internal | business-field | semantic-review-required |
| 18 | `coupon_remaining` | `int(11)` | 否 |  |  | 剩余数量  -1不限量 | internal | business-field | semantic-review-required |
| 19 | `used_count` | `int(11)` | 否 |  | 0 | 已使用数量 | internal | business-field | semantic-review-required |
| 20 | `coupon_description` | `varchar(500)` | 是 |  |  | 优惠卷说明 | internal | business-field | semantic-review-required |
| 21 | `valid_type` | `int(11)` | 是 |  |  | 时效:1绝对时效（领取后XXX-XXX时间段有效）  2相对时效（领取后N天有效） | internal | business-field | semantic-review-required |
| 22 | `begin_date` | `date` | 是 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 23 | `end_date` | `date` | 是 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 24 | `start_range_date` | `int(11)` | 是 |  | 0 | 领取后第N天生效 0立即生效 | internal | business-field | semantic-review-required |
| 25 | `range_date` | `int(11)` | 是 |  |  | 有效期 单位天 | internal | business-field | semantic-review-required |
| 26 | `range_type` | `int(11)` | 是 |  |  | 周期类型 0固定周期， 1 具体起止日期 | internal | business-field | semantic-review-required |
| 27 | `use_frequency_type` | `int(11)` | 否 |  |  | 使用频率限制 0每天 1每周 2每月 | internal | business-field | semantic-review-required |
| 28 | `use_frequency_quantity` | `int(11)` | 否 |  |  | 使用频率数量0不限 | internal | business-field | semantic-review-required |
| 29 | `wx_coupon_id` | `varchar(50)` | 是 |  |  | 微信券id | internal | relation-key | server-filter-only |
| 30 | `wx_coupon_state` | `int(11)` | 否 |  | -1 | 微信卡包卡样状态 -2 审核失败，-1未同步 0审核，1已同步 | internal | business-field | semantic-review-required |
| 31 | `al_coupon_id` | `varchar(50)` | 是 |  |  | 支付宝券id | internal | relation-key | server-filter-only |
| 32 | `al_coupon_state` | `varchar(2)` | 否 |  | -1 | 微信卡包卡样状态 -2 审核失败，-1未同步 0审核，1已同步 | internal | business-field | semantic-review-required |
| 33 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0暂停发放 1正常发放 2发放完毕  -2优惠券设置时间过期 | internal | business-field | semantic-review-required |
| 34 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 35 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 36 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 37 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 38 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）
- `idx_tenantId`：非唯一 BTREE（tenant_id）

### `coupon_center`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `coupon_center_type` | `int(11)` | 否 |  |  | 2续费送,3生日送,4满送，5群发,6营销活动，7节日祝福8放假 9老客户激活，10散客营销， 21 续费营销（新），22 联盟券，23，购卡送券，24 支付宝商家券  25 , 券包 | internal | business-field | semantic-review-required |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `template_id` | `int(11)` | 是 |  |  | 短信模板ID | internal | relation-key | server-filter-only |
| 5 | `is_by_user_level` | `tinyint(1)` | 否 |  |  | 是否按会员等级   1是0否 | internal | business-field | semantic-review-required |
| 6 | `pre_card_id` | `int(11)` | 是 |  |  | 按会员等级时必填 储值卡ID | internal | relation-key | server-filter-only |
| 7 | `is_only_one` | `int(11)` | 是 |  |  | 满赠券时必填  1单次 0累十 | internal | business-field | semantic-review-required |
| 8 | `consumption_type` | `int(11)` | 是 |  |  | 满赠券时必填  消费方式1仅付款2卡内消费 | internal | business-field | semantic-review-required |
| 9 | `meet_amount_min` | `decimal(10,2)` | 是 |  |  | 满赠券时必填  金额到达区间开始 | internal | business-field | semantic-review-required |
| 10 | `meet_amount_max` | `decimal(10,2)` | 是 |  |  | 预留字段  金额到达区间结束 | internal | business-field | semantic-review-required |
| 11 | `send_group_date` | `datetime` | 是 |  |  | 群发券必填 发放时间 | internal | business-field | semantic-review-required |
| 12 | `send_group` | `int(11)` | 是 |  |  | 群发券必填发放群体 0全部会员 | internal | business-field | semantic-review-required |
| 13 | `send_group_times` | `int(11)` | 是 |  |  | 群发券必填 群发次数 1只发一次2按月次数 3按年发送 | internal | business-field | semantic-review-required |
| 14 | `less_money` | `decimal(10,2)` | 是 |  |  | 续费送券 当余额低于多少时送券 (元) | internal | business-field | semantic-review-required |
| 15 | `less_times` | `int(11)` | 是 |  |  | 续费送券 当余额低于多少时送券（次） | internal | business-field | semantic-review-required |
| 16 | `send_count` | `int(11)` | 否 |  |  | 群发券 生日券   已发送的次数 | internal | business-field | semantic-review-required |
| 17 | `share_regular_count` | `int(11)` | 是 |  |  | 定向券时必填 微信分享限制几人领取 | internal | business-field | semantic-review-required |
| 18 | `alliance_day` | `int(11)` | 否 |  | 30 | 联盟券，多少天未在本店消费 | internal | business-field | semantic-review-required |
| 19 | `send_start_date` | `datetime` | 是 |  |  | 支付宝商家券发券时间 | internal | business-field | semantic-review-required |
| 20 | `send_end_date` | `datetime` | 是 |  |  | 支付宝商家券发券时间 | internal | business-field | semantic-review-required |
| 21 | `price` | `decimal(11,2)` | 是 |  |  | 价格 | internal | business-field | semantic-review-required |
| 22 | `discount_price` | `decimal(10,2)` | 是 |  |  | 折扣价 | internal | business-field | semantic-review-required |
| 23 | `max_send_count` | `int(11)` | 是 |  |  | 最大发送数量 | internal | business-field | semantic-review-required |
| 24 | `coupon_center_name` | `varchar(255)` | 是 |  |  | 活动名称 | internal | business-field | semantic-review-required |
| 25 | `state` | `int(11)` | 是 |  |  | 状态 -1删除 0停止使用 1正常 2已发送 | internal | business-field | semantic-review-required |
| 26 | `tenant_id` | `int(11)` | 是 | MUL |  | 租户Id | internal | tenant-scope | server-filter-only |
| 27 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 28 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 29 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 30 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）
- `idx_tenantId`：非唯一 BTREE（tenant_id）

### `coupon_center_coupon`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 标识ID | internal | relation-key | server-filter-only |
| 2 | `coupon_center_id` | `int(11)` | 否 | MUL |  | 优惠中心ID | internal | relation-key | server-filter-only |
| 3 | `coupon_id` | `int(11)` | 否 |  |  | 优惠券ID | internal | relation-key | server-filter-only |
| 4 | `coupon_sum` | `int(11)` | 否 |  | 1 | 优惠券数量 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  |  状态 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_couponCenterId`：非唯一 BTREE（coupon_center_id）

### `coupon_link`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：外部券

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `name` | `varchar(50)` | 否 |  |  | 券名称 | internal | business-field | semantic-review-required |
| 4 | `type` | `int(11)` | 否 |  | 0 | 类型(0:直领券  1: 售卖券) | internal | business-field | semantic-review-required |
| 5 | `face_value` | `decimal(10,2)` | 否 |  |  | 面额 | internal | business-field | semantic-review-required |
| 6 | `selling_price` | `decimal(10,2)` | 是 |  |  | 售价 | internal | business-field | semantic-review-required |
| 7 | `coupon_url` | `varchar(500)` | 是 |  |  | 领券链接 | internal | business-field | semantic-review-required |
| 8 | `image` | `varchar(255)` | 是 |  |  | 券图片 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  | 1 | 状态  1正常 -1删除 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `coupon_password`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 标识ID | internal | relation-key | server-filter-only |
| 2 | `coupon_center_id` | `int(11)` | 否 |  |  | 优惠中心ID | internal | relation-key | server-filter-only |
| 3 | `coupon_id` | `int(11)` | 否 |  |  | 用户ID | internal | relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  |  | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `receive_count` | `int(11)` | 否 |  | 1 | 单人可领取张数 | internal | business-field | semantic-review-required |
| 7 | `price` | `decimal(10,2)` | 否 |  | 0.00 | shou jia | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | 0未生效 1待领取 2已领完 | internal | business-field | semantic-review-required |
| 9 | `random_param` | `varchar(40)` | 否 |  |  | 随机参数GUID | internal | business-field | semantic-review-required |
| 10 | `remaining_coupons` | `int(11)` | 否 |  |  | 剩余几人领取  -1不限制 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `coupon_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：优惠券项目关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `coupon_id` | `int(11)` | 否 |  |  | 优惠券id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 服务项目id | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 状态0禁用 1启用 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `course_image`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：课程图片

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `image_type` | `int(11)` | 否 |  |  | 图片类型 0课程图片 1课表头图,2C端头图 3预约成功图片 | internal | business-field | semantic-review-required |
| 3 | `image_main` | `varchar(100)` | 否 |  |  | 主图 | internal | business-field | semantic-review-required |
| 4 | `image_style` | `int(11)` | 否 |  |  | 图片样式 0明亮 1暗黑 | internal | business-field | semantic-review-required |
| 5 | `image_url1` | `varchar(100)` | 否 |  |  | 图例1 | internal | business-field | semantic-review-required |
| 6 | `image_url2` | `varchar(100)` | 否 |  |  | 图例2 | internal | business-field | semantic-review-required |
| 7 | `image_url3` | `varchar(100)` | 否 |  |  | 图例3 | internal | business-field | semantic-review-required |
| 8 | `store_id` | `bigint(20)` | 否 |  | 0 | 店铺id | internal | store-scope | server-filter-only |
| 9 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `order_by` | `bigint(20)` | 否 |  | 0 | 排序倒序 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  | 1 | 状态 1启用 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `course_image_tag_relation`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `image_id` | `bigint(20)` | 否 |  | 0 | 课程id | internal | relation-key | server-filter-only |
| 3 | `tag_id` | `bigint(20)` | 否 |  | 0 | tagid | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  | 1 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `custom_controls`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：自定义控件

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 | 店铺id | internal | store-scope | server-filter-only |
| 3 | `store_type` | `varchar(10)` | 否 |  |  | 店铺类型（仅对store=0有效） | internal | business-field | semantic-review-required |
| 4 | `control_name` | `varchar(30)` | 否 |  |  | 控件名称 | internal | business-field | semantic-review-required |
| 5 | `control_instructions` | `varchar(20)` | 否 |  |  | 控件说明 | internal | business-field | semantic-review-required |
| 6 | `control_type` | `varchar(10)` | 否 |  |  | 控件类型 input,radio,select.... | internal | business-field | semantic-review-required |
| 7 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 8 | `is_must` | `int(11)` | 否 |  |  | 是否必填 1是 0否 | internal | business-field | semantic-review-required |
| 9 | `is_show` | `tinyint(1)` | 否 |  | 0 | 是否对C端客户显示 | internal | business-field | semantic-review-required |
| 10 | `is_private` | `tinyint(1)` | 否 |  | 0 | 是否是私有的 | internal | business-field | semantic-review-required |
| 11 | `is_default` | `tinyint(1)` | 否 |  | 0 | 是否是默认数据 | internal | business-field | semantic-review-required |
| 12 | `is_client_data` | `tinyint(1)` | 否 |  | 0 | 是否只由顾客添加 | internal | business-field | semantic-review-required |
| 13 | `order_by` | `int(5)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 14 | `state` | `int(11)` | 否 |  |  | 状态1启用 | internal | business-field | semantic-review-required |
| 15 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 16 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 17 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 18 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 19 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `custom_controls_item`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：用户自定义控件字内容

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `cid` | `int(11)` | 否 |  |  | 控件id | internal | business-field | semantic-review-required |
| 3 | `item_value` | `varchar(20)` | 否 |  |  | 控件值 | internal | business-field | semantic-review-required |
| 4 | `item_name` | `varchar(20)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 5 | `is_default` | `tinyint(2)` | 否 |  | 0 | 是否是默认 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 1启用 -1删除 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `custom_controls_store_type`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `controls_id` | `int(11)` | 否 |  |  | 控件id | internal | relation-key | server-filter-only |
| 3 | `store_type_id` | `varchar(4)` | 否 |  |  | 店铺类型 | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `custom_controls_validation`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：自定义控件验证规则

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `cid` | `int(11)` | 否 |  |  | 控件id | internal | business-field | semantic-review-required |
| 3 | `validation_formula` | `varchar(200)` | 否 |  |  | 验证公式 | internal | business-field | semantic-review-required |
| 4 | `validation_instructions` | `varchar(20)` | 否 |  |  | 不通过提示信息 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(1)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `custom_user_tag`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `name` | `varchar(50)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 4 | `type` | `int(11)` | 是 |  |  | 类型；1-红，2-蓝，3-绿，4-粉，0-灰 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 是 |  |  | 状态；1-正常 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `distribution_setting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `is_extend` | `tinyint(1)` | 否 |  | 0 | 是否开通了推广(已弃用) | internal | business-field | semantic-review-required |
| 4 | `is_promotion_code_visable` | `tinyint(1)` | 否 |  | 0 | 推广码是否可见 0 不可见 ； 1  可见 ; | internal | business-field | semantic-review-required |
| 5 | `is_promot_box_visable` | `tinyint(1)` | 否 |  | 0 | 分佣弹框是否提示  1提示  ； 0 不提示 ； | internal | business-field | semantic-review-required |
| 6 | `commission_valid_date` | `int(11)` | 否 |  | 0 | 分佣有效天数 | internal | business-field | semantic-review-required |
| 7 | `promotion_type` | `int(11)` | 否 |  | 1 | 推广类型 1 全员推广 ； 2指定推广； | internal | business-field | semantic-review-required |
| 8 | `commission_type` | `int(11)` | 否 |  | 1 | 分佣类型  0 单次分佣 ； 1 永久分佣 ； 2限时分佣 ； | internal | business-field | semantic-review-required |
| 9 | `extend_content` | `varchar(1000)` | 否 |  |  | 推广说明 | sensitive-unstructured | business-field | deny |
| 10 | `is_buy_commission` | `tinyint(1)` | 否 |  | 0 | 购卡分佣开关 | internal | business-field | semantic-review-required |
| 11 | `is_consume_commission` | `tinyint(1)` | 否 |  | 0 | 消费分佣开关 | internal | business-field | semantic-review-required |
| 12 | `commission_start_money` | `decimal(10,2)` | 否 |  | 0.00 | 分佣起始金额 | internal | business-field | semantic-review-required |
| 13 | `is_commission` | `tinyint(1)` | 否 |  |  | 佣金开关 | internal | business-field | semantic-review-required |
| 14 | `is_commission_consume` | `tinyint(1)` | 否 |  |  | 佣金消费开关 | internal | business-field | semantic-review-required |
| 15 | `is_commission_cash` | `tinyint(1)` | 否 |  |  | 佣金提现开关 | internal | business-field | semantic-review-required |
| 16 | `is_forever_commission` | `tinyint(1)` | 否 |  | 1 | 永久分佣开关 （已弃用） | internal | business-field | semantic-review-required |
| 17 | `commission_min_cash_money` | `decimal(10,2)` | 否 |  |  | 佣金提现最低金额 | internal | business-field | semantic-review-required |
| 18 | `commission_cash_count` | `int(11)` | 否 |  |  | 佣金每天提现次数 | internal | business-field | semantic-review-required |
| 19 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 20 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 21 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |
| 22 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 24 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `distribution_setting_child`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `distribution_setting_id` | `int(11)` | 否 |  |  | 分销设置id | internal | relation-key | server-filter-only |
| 4 | `level` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 5 | `buy_commission_rate` | `decimal(10,4)` | 否 |  |  | 购卡分佣比例 | internal | business-field | semantic-review-required |
| 6 | `extend_commission_rate` | `decimal(10,4)` | 否 |  |  | 推广分佣比例 | internal | business-field | semantic-review-required |
| 7 | `consume_commission_rate` | `decimal(10,4)` | 否 |  |  | 消费分佣比例 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `name` | `varchar(100)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 4 | `img` | `varchar(255)` | 否 |  |  | 图片 | internal | business-field | semantic-review-required |
| 5 | `describe` | `varchar(255)` | 否 |  |  | 描述 | internal | business-field | semantic-review-required |
| 6 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 价格 | internal | business-field | semantic-review-required |
| 7 | `vip_price` | `decimal(10,2)` | 否 |  | 0.00 | vip价格 | internal | business-field | semantic-review-required |
| 8 | `quantity` | `int(11)` | 否 |  | 0 | 库存 | internal | business-field | semantic-review-required |
| 9 | `sell_num` | `int(11)` | 否 |  | 0 | 售出数量 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  | 0 | 状态；0-下架，1-上架 | internal | business-field | semantic-review-required |
| 11 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 13 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `is_recommend` | `tinyint(1)` | 是 |  |  | 是否推荐位 | internal | business-field | semantic-review-required |
| 18 | `enjoy_vip_discount` | `tinyint(1)` | 是 |  | 1 | 享受会员折扣价 | internal | business-field | semantic-review-required |
| 19 | `ali_food_id` | `varchar(50)` | 是 |  |  | 支付宝id | internal | relation-key | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_cart`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `table_id` | `int(11)` | 是 |  |  | 餐台桌号 | internal | relation-key | server-filter-only |
| 5 | `type` | `int(11)` | 是 |  |  | 类型：0 一人一单，1 多人一单 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 是 |  |  | 更信人 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `food_cart_item`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `food_cart_id` | `int(11)` | 是 |  |  | 购物车ID | internal | relation-key | server-filter-only |
| 4 | `food_id` | `int(11)` | 是 |  |  | 菜品ID | internal | relation-key | server-filter-only |
| 5 | `food_count` | `int(11)` | 是 |  |  | 菜品数量 | internal | business-field | semantic-review-required |
| 6 | `sku_value` | `varchar(255)` | 是 |  |  | 规格 值 | internal | business-field | semantic-review-required |
| 7 | `sku_string` | `varchar(255)` | 是 |  |  | 规格 文本 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 是 |  |  | 状态 -1：删除，0：无效，1：有效 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 13 | `arr_uid` | `varchar(255)` | 是 |  |  | 关联用户数组 | internal | business-field | semantic-review-required |
| 14 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `food_category`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 5 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 7 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_category_relation`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `food_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `food_category_id` | `int(11)` | 否 |  | 0 | 分类id | internal | relation-key | server-filter-only |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_client_info`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `user_name` | `varchar(255)` | 是 |  |  | 用户名 | sensitive | business-field | masked-or-filter-only |
| 5 | `arrive_count` | `int(11)` | 是 |  |  | 到店次数 | internal | business-field | semantic-review-required |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 总消费值 | internal | business-field | semantic-review-required |
| 7 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_common_sku`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 4 | `is_signle` | `tinyint(1)` | 否 |  | 0 | 单选还是多选；0-单选，1-多选 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_common_sku_item`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `food_common_sku_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 价格 | internal | business-field | semantic-review-required |
| 6 | `vip_price` | `decimal(10,2)` | 否 |  | 0.00 | vip价格 | internal | business-field | semantic-review-required |
| 7 | `quantity` | `int(11)` | 否 |  | 0 | 库存 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 9 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 11 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_img`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `food_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `img` | `varchar(255)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 5 | `is_main` | `int(11)` | 否 |  | 0 | 是否是主图封面图；0-否，1-是 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 7 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 9 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_order`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 4 | `no` | `varchar(10)` | 是 |  |  | 流水号 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 是 |  |  | 状态： -2已退款 0待付款 1已付款 2已出餐 3 已配送 4已完成 5已取消 | internal | business-field | semantic-review-required |
| 6 | `order_state` | `int(11)` | 是 |  |  | 订单状态；0-待处理，1-已接单，2-已取消 | internal | business-field | semantic-review-required |
| 7 | `business_remark` | `varchar(255)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 8 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 9 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 付款人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `commission_deduct` | `decimal(10,2)` | 是 |  |  | 佣金扣除 | internal | business-field | semantic-review-required |
| 20 | `final_price` | `decimal(10,2)` | 是 |  |  | 商议价格 | internal | business-field | semantic-review-required |
| 21 | `people_count` | `int(11)` | 是 |  |  | 就餐人数 | internal | business-field | semantic-review-required |
| 22 | `table_id` | `int(11)` | 是 |  |  | 桌号 | internal | relation-key | server-filter-only |
| 23 | `preferential_type` | `int(11)` | 是 |  |  | 优惠类型：0不优惠 1折扣 2固定金额 | internal | business-field | semantic-review-required |
| 24 | `payment` | `decimal(10,2)` | 是 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 25 | `need_payment` | `decimal(10,2)` | 是 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 26 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 27 | `take_time` | `varchar(25)` | 是 |  |  | 取餐时间 | internal | business-field | semantic-review-required |
| 28 | `order_type` | `int(11)` | 是 |  |  | 0 堂食 ,1 外卖 2外带 | internal | business-field | semantic-review-required |
| 29 | `store_rider_id` | `int(11)` | 是 |  |  | 配送员\骑手 | internal | relation-key | server-filter-only |
| 30 | `user_address_id` | `int(11)` | 是 |  |  | 用户地址信息 | sensitive | relation-key | server-filter-only |
| 31 | `rider_name` | `varchar(255)` | 是 |  |  | 骑手姓名 | internal | business-field | semantic-review-required |
| 32 | `rider_mobile` | `varchar(255)` | 是 |  |  | 骑手电话 | sensitive | business-field | masked-or-filter-only |
| 33 | `rider_address` | `varchar(255)` | 是 |  |  | 骑手地址 | sensitive | business-field | masked-or-filter-only |
| 34 | `receiver_name` | `varchar(255)` | 是 |  |  | 收货人姓名 | internal | business-field | semantic-review-required |
| 35 | `receiver_mobile` | `varchar(255)` | 是 |  |  | 收货人手机号 | sensitive | business-field | masked-or-filter-only |
| 36 | `receiver_address` | `varchar(255)` | 是 |  |  | 收货人地址 | sensitive | business-field | masked-or-filter-only |
| 37 | `distance` | `int(11)` | 是 |  |  | 配送距离 | internal | business-field | semantic-review-required |
| 38 | `send_out_price` | `decimal(10,2)` | 是 |  |  | 配送费 | internal | business-field | semantic-review-required |
| 39 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `food_order_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `food_id` | `int(11)` | 是 |  |  | 菜品ID | internal | relation-key | server-filter-only |
| 4 | `food_order_id` | `int(11)` | 是 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 5 | `food_name` | `varchar(255)` | 是 |  |  | 菜品名称 | internal | business-field | semantic-review-required |
| 6 | `food_count` | `int(11)` | 是 |  |  | 菜品数量 | internal | business-field | semantic-review-required |
| 7 | `food_price` | `decimal(10,2)` | 是 |  |  | 菜品价格 | internal | business-field | semantic-review-required |
| 8 | `sku_value` | `varchar(255)` | 是 |  |  | 规格值 | internal | business-field | semantic-review-required |
| 9 | `sku_string` | `varchar(255)` | 是 |  |  | 规格文本 | internal | business-field | semantic-review-required |
| 10 | `food_img` | `varchar(255)` | 是 |  |  | 图片 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 状态：0禁用 1启用 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 16 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeIdAndOrderId`：非唯一 BTREE（store_id, food_order_id）

### `food_relation_user`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `food_cart_id` | `int(11)` | 是 |  |  | 购物车ID | internal | relation-key | server-filter-only |
| 5 | `food_cart_item_id` | `int(11)` | 是 |  |  | 购物车子项ID | internal | relation-key | server-filter-only |
| 6 | `food_order_id` | `int(11)` | 是 |  |  | 订单ID 默认为0 | internal | relation-key | server-filter-only |
| 7 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `food_right_tag`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `food_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `right_tag` | `varchar(20)` | 否 |  |  | 角标标签 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_setting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL | 0 | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `food_title` | `varchar(30)` | 否 |  | 点餐 | 点餐标题 | internal | business-field | semantic-review-required |
| 4 | `is_open` | `tinyint(1)` | 否 |  | 0 | 点单开关；0-关，1-开 | internal | business-field | semantic-review-required |
| 5 | `food_mode` | `int(11)` | 否 |  |  | 点餐模式：0 一人一单，1多人一单 | internal | business-field | semantic-review-required |
| 6 | `is_me_take` | `tinyint(1)` | 否 |  | 0 | 自取开关；0-关，1-开 | internal | business-field | semantic-review-required |
| 7 | `is_automatic_meal` | `tinyint(1)` | 否 |  |  | 出餐设置；0-关，1-开 | internal | business-field | semantic-review-required |
| 8 | `is_table` | `tinyint(1)` | 否 |  |  | 餐台设置；1-多餐台 | internal | business-field | semantic-review-required |
| 9 | `is_eat_here` | `tinyint(1)` | 否 |  |  | 是否是堂食 | internal | business-field | semantic-review-required |
| 10 | `is_take_out` | `tinyint(1)` | 否 |  |  | 是否是外卖 | internal | business-field | semantic-review-required |
| 11 | `send_out_range` | `decimal(10,2)` | 否 |  |  | 配送范围 | internal | business-field | semantic-review-required |
| 12 | `send_out_start_time` | `varchar(10)` | 否 |  |  | 配送开始时间 | internal | business-field | semantic-review-required |
| 13 | `send_out_end_time` | `varchar(10)` | 否 |  |  | 配送结束时间 | internal | business-field | semantic-review-required |
| 14 | `send_out_price` | `decimal(10,2)` | 否 |  |  | 配送费用 | internal | business-field | semantic-review-required |
| 15 | `start_price` | `decimal(10,2)` | 否 |  |  | 起送金额 | internal | business-field | semantic-review-required |
| 16 | `take_make_time` | `int(11)` | 否 |  |  | 自提冗余配货时长 分钟 | internal | business-field | semantic-review-required |
| 17 | `share_img` | `varchar(80)` | 否 |  |  | 分享图 | internal | business-field | semantic-review-required |
| 18 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 19 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户ID | internal | tenant-scope | server-filter-only |
| 21 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 24 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 25 | `is_subscribe` | `tinyint(1)` | 否 |  | 0 | 扫码点餐是否需要订阅 | internal | business-field | semantic-review-required |
| 26 | `except_finish_minute` | `int(11)` | 是 |  |  | 预计送达时间（分钟） | internal | business-field | semantic-review-required |
| 27 | `can_select_finish_time` | `tinyint(1)` | 否 |  |  | 是否可选送达时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `food_sku`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `food_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `food_common_sku_id` | `int(11)` | 否 |  | 0 | 公共规格id | internal | relation-key | server-filter-only |
| 5 | `name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 6 | `is_signle` | `tinyint(1)` | 否 |  | 0 | 单选还是多选；0-单选，1-多选 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 8 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 10 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_sku_item`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `food_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `food_sku_id` | `int(11)` | 否 |  | 0 | 规格id | internal | relation-key | server-filter-only |
| 5 | `name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 6 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 价格 | internal | business-field | semantic-review-required |
| 7 | `vip_price` | `decimal(10,2)` | 否 |  | 0.00 | vip价格 | internal | business-field | semantic-review-required |
| 8 | `quantity` | `int(11)` | 否 |  | 0 | 库存 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 10 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 12 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_tabel_qrcode`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `table_id` | `int(11)` | 是 |  |  | 桌台ID | internal | relation-key | server-filter-only |
| 4 | `code` | `varchar(255)` | 是 |  |  | 码值 | internal | business-field | semantic-review-required |
| 5 | `qrcode_url` | `varchar(255)` | 是 |  |  | 二维码Url | internal | business-field | semantic-review-required |
| 6 | `type` | `int(11)` | 是 |  |  | 类型：0 微信，1支付宝 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 是 |  |  | 状态 ：0 停用， 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_table`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `table_name` | `varchar(255)` | 是 |  |  | 名称 | internal | business-field | semantic-review-required |
| 4 | `table_no` | `int(11)` | 是 |  |  | 桌号 | internal | business-field | semantic-review-required |
| 5 | `people_num` | `int(11)` | 是 |  |  | 人数 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 是 |  |  | 状态 | internal | business-field | semantic-review-required |
| 7 | `last_use_time` | `datetime` | 是 |  |  | 最后使用时间 | internal | business-field | semantic-review-required |
| 8 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 9 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `table_qrcode` | `varchar(255)` | 是 |  |  | 桌号二维码 | internal | business-field | semantic-review-required |
| 14 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_tag`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 4 | `is_edit` | `tinyint(1)` | 否 |  | 0 | 是否允许修改、删除；0-不允许，1-允许 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `food_tag_relation`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `food_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `food_tag_id` | `int(11)` | 否 |  | 0 | 标签id | internal | relation-key | server-filter-only |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `image_category`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `iid` | `int(11)` | 否 |  |  | 图片id | internal | business-field | semantic-review-required |
| 3 | `cid` | `int(11)` | 否 |  |  | 分类id | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `image_gallery`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：图库表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `title` | `varchar(30)` | 否 |  |  | 图片标题 | internal | business-field | semantic-review-required |
| 3 | `img_url` | `varchar(100)` | 否 |  |  | 图片路径 | internal | business-field | semantic-review-required |
| 4 | `img_type` | `int(11)` | 否 |  | 0 | 图片类型：0报告底图  1用户头像 | internal | business-field | semantic-review-required |
| 5 | `remarks` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 添加时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `index_banner`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：首页Bannaer

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | Id | internal | relation-key | server-filter-only |
| 2 | `img_src` | `varchar(255)` | 是 |  |  | 图片路径 | internal | business-field | semantic-review-required |
| 3 | `link` | `varchar(255)` | 是 |  |  | 链接路径 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 是 |  |  | 状态 0停用 1启用 | internal | business-field | semantic-review-required |
| 5 | `location` | `int(11)` | 是 |  |  | 位置 0首页头部 1首页下部 2启动页 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 是 |  |  | 创建日期 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 是 |  |  | 修改日期 | internal | business-field | semantic-review-required |
| 8 | `order_by` | `int(11)` | 是 |  |  | 排序 | internal | business-field | semantic-review-required |
| 9 | `Action_Type` | `int(11)` | 是 |  |  | 动作类型 0-html,1-Activity | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `item_class`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `class_name` | `varchar(20)` | 否 |  |  | 分类名称 | internal | business-field | semantic-review-required |
| 3 | `class_id` | `varchar(20)` | 否 |  |  | 分类ID | internal | relation-key | server-filter-only |
| 4 | `root_id` | `varchar(20)` | 否 |  |  | 父级ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_admin_login`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：管理员登陆日志


| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 管理员id | internal | subject-or-relation-key | server-filter-only |
| 3 | `longin_ip` | `varchar(15)` | 否 |  |  | 登陆IP | internal | business-field | semantic-review-required |
| 4 | `login_type` | `int(11)` | 否 |  |  | 登陆方式 | internal | business-field | semantic-review-required |
| 5 | `login_area` | `varchar(10)` | 否 |  |  | 登陆地 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_admin_operation`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：管理员操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 管理员id | internal | subject-or-relation-key | server-filter-only |
| 3 | `operation_type` | `int(11)` | 否 |  |  | 操作类型 | internal | business-field | semantic-review-required |
| 4 | `operation_info` | `varchar(200)` | 否 |  |  | 操作详情 | internal | business-field | semantic-review-required |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_alliance`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：store_id。
表注释：联盟日志


| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `alliance_id` | `int(11)` | 否 |  |  | 联盟id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `log_type` | `int(11)` | 否 |  |  | 0创建联盟，1加入联盟，2退出联盟，3移出联盟，4解散联盟 | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `date` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_alliance_coupon`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `alliance_id` | `int(11)` | 否 |  |  | 联盟id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 展示店铺id | internal | store-scope | server-filter-only |
| 4 | `coupon_id` | `int(11)` | 否 |  |  | 优惠券id | internal | relation-key | server-filter-only |
| 5 | `log_type` | `int(11)` | 否 |  |  | 0 展示 1领取 | internal | business-field | semantic-review-required |
| 6 | `user_id` | `int(11)` | 否 |  |  | 当前用户id | internal | subject-or-relation-key | server-filter-only |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_export_user_data`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键标识 | internal | relation-key | server-filter-only |
| 2 | `export_email` | `varchar(30)` | 否 |  |  | 导出数据邮箱 | sensitive | business-field | masked-or-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 5 | `state` | `int(11)` | 否 |  |  | 导出状态 0 失败 1成功 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `type` | `int(11)` | 否 |  | 0 | 类型：0 会员导出 1 优惠券导出 2 流水导出 | internal | business-field | semantic-review-required |
| 9 | `condition` | `varchar(2000)` | 是 |  |  | 导出条件，JSON形式 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_file_resources`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：预备处理资源表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `file_path` | `varchar(200)` | 否 |  |  | 资源路径 | internal | business-field | semantic-review-required |
| 3 | `hash` | `varchar(32)` | 是 |  |  | Hash | internal | business-field | semantic-review-required |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 1图片 2视频 3文档 | internal | business-field | semantic-review-required |
| 6 | `file_source` | `int(11)` | 否 |  |  | 文件源：0头像，1运动周记录，2运动报告，3问答主题，4问答评论 | internal | business-field | semantic-review-required |
| 7 | `video_cover` | `varchar(100)` | 是 |  |  | 视频封面地址 | internal | business-field | semantic-review-required |
| 8 | `video_time_length` | `int(11)` | 是 |  |  | 视频长度 单位：秒 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  |  | 0预处理文件 1需处理文件 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_lessons_notice_time`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `nid` | `bigint(20)` | 否 |  |  | 通知id | internal | business-field | semantic-review-required |
| 3 | `time_id` | `bigint(20)` | 否 |  |  | 时间id | internal | relation-key | server-filter-only |
| 4 | `lessons_id` | `bigint(20)` | 否 |  |  | 课程id | internal | relation-key | server-filter-only |
| 5 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 6 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_qrcode`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `code_scene` | `varchar(10)` | 否 |  |  | 场景值 | internal | business-field | semantic-review-required |
| 3 | `code_type` | `int(11)` | 否 |  |  | 码用途 0推广 | internal | business-field | semantic-review-required |
| 4 | `open_id` | `varchar(30)` | 否 |  |  | 扫码的人 | restricted | relation-key | deny |
| 5 | `event` | `int(11)` | 否 |  |  | 场景0关注 1扫码 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_store_certification`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键唯一标识 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `platform` | `int(11)` | 否 |  |  | 平台 0所有 1微信 2支付宝 | internal | business-field | semantic-review-required |
| 4 | `store_type` | `int(11)` | 否 |  |  | 店铺状态 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 当前状态  0审核 1通过审核 -1 未填写 -2回退 -3未通过审核 | internal | business-field | semantic-review-required |
| 6 | `note` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 7 | `type` | `int(11)` | 是 |  | 0 | 类型；0-进件，1-换绑卡 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `log_trigger_open_uid`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `platform` | `int(11)` | 否 |  |  | 所属平台1 微信，2 QQ，3 支付宝 | internal | business-field | semantic-review-required |
| 3 | `client_type` | `int(11)` | 否 |  |  | 客户端  0=C端，1=B端 | internal | business-field | semantic-review-required |
| 4 | `union_id` | `varchar(50)` | 是 |  |  | 平台唯一ID | restricted | relation-key | deny |
| 5 | `old_uid` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `new_uid` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_trigger_openid`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `old_open_id` | `varchar(50)` | 否 |  |  | 旧id | restricted | relation-key | deny |
| 4 | `new_open_id` | `varchar(50)` | 否 |  |  | 新id | restricted | relation-key | deny |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_trigger_user_mobile`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `old_mobile` | `varchar(20)` | 否 |  |  | 旧手机 | sensitive | business-field | masked-or-filter-only |
| 4 | `new_mobile` | `varchar(20)` | 否 |  |  | 新手机 | sensitive | business-field | masked-or-filter-only |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_user_account`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `account_type` | `int(11)` | 否 |  |  | 账号类型 0手机 1微信 2QQ 3微博 | internal | business-field | semantic-review-required |
| 4 | `log_type` | `int(11)` | 否 |  |  | 日志类型 0解绑 1绑定 | internal | business-field | semantic-review-required |
| 5 | `account` | `varchar(50)` | 否 |  |  | 账号信息 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_user_card_cancel`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：删除会员卡日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 门店id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `cancel_type` | `int(11)` | 否 |  | 0 | 注销类型 0会员 1卡 | internal | business-field | semantic-review-required |
| 6 | `operation_type` | `int(11)` | 否 |  | 0 | 操作类型 0删除 1恢复 | internal | business-field | semantic-review-required |
| 7 | `is_recover` | `tinyint(1)` | 否 |  | 0 | 是否恢复 | internal | business-field | semantic-review-required |
| 8 | `remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 9 | `source_log_id` | `bigint(20)` | 否 |  |  | 删除记录ID | internal | relation-key | server-filter-only |
| 10 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 否 |  |  | 操作人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  |  | 操作时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `log_user_card_cancel_info`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `log_id` | `bigint(20)` | 否 |  |  | 日志id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `card_child_id` | `int(11)` | 否 |  |  | 子卡id | internal | relation-key | server-filter-only |
| 7 | `card_name` | `varchar(20)` | 否 |  |  | 卡名称 | internal | business-field | semantic-review-required |
| 8 | `card_info` | `varchar(100)` | 否 |  |  | 卡信息 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `state` | `int(11)` | 否 |  | 1 | 状态 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `log_user_login`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：store_id。
表注释：用户登陆日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 是 | MUL | 0 | 商家id | internal | store-scope | server-filter-only |
| 4 | `login_type` | `int(11)` | 否 |  |  | 登陆方式 0手机 1微信 2QQ 3微博 | internal | business-field | semantic-review-required |
| 5 | `login_method` | `int(11)` | 否 |  | 0 |  0:ios,1android ,2 pc,3 weixin,4 小程序,5 h5 | internal | business-field | semantic-review-required |
| 6 | `phone_brand` | `varchar(20)` | 是 |  |  | 手机品牌 | sensitive | business-field | masked-or-filter-only |
| 7 | `phone_model` | `varchar(50)` | 是 | MUL |  | 手机型号 | sensitive | business-field | masked-or-filter-only |
| 8 | `phone_nonce` | `varchar(200)` | 是 |  |  | 唯一标识 | sensitive | business-field | masked-or-filter-only |
| 9 | `user_token` | `varchar(50)` | 否 |  |  | 用户登录Token | restricted | business-field | deny |
| 10 | `ip` | `varchar(30)` | 是 |  |  | ip | internal | business-field | semantic-review-required |
| 11 | `client_type` | `int(11)` | 否 |  |  | 客户端类型 0顾客 1商家 2预约，3营销 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 | MUL |  | 时间 | internal | business-field | semantic-review-required |

索引：
- `Index_create_dates`：非唯一 BTREE（create_date, store_id）
- `PRIMARY`：唯一 BTREE（id）
- `index_create_dates_clumb`：非唯一 BTREE（phone_model, phone_nonce, create_date）
- `index_name`：非唯一 BTREE（store_id, uid）

### `lottery`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：抽奖活动表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `bg_img` | `varchar(100)` | 否 |  |  | 背景图 | internal | business-field | semantic-review-required |
| 4 | `title` | `varchar(20)` | 否 |  |  | 抽奖活动名称 | internal | business-field | semantic-review-required |
| 5 | `lottery_type` | `int(11)` | 否 |  |  | 抽奖类型 0进店，1积分，2消费后，3满额 | internal | business-field | semantic-review-required |
| 6 | `lottery_frequency_type` | `int(11)` | 是 |  |  | 抽奖频率限制 0每天 1累计（进店，积分） | internal | business-field | semantic-review-required |
| 7 | `lottery_frequency_quantity` | `int(11)` | 否 |  |  | 抽奖频率数量 必须大于0（进店，积分） | internal | business-field | semantic-review-required |
| 8 | `share_reward` | `int(11)` | 否 |  |  | 转发奖励次数）(进店) | internal | business-field | semantic-review-required |
| 9 | `money_set` | `decimal(10,2)` | 否 |  |  | 现金消费多少元抽一次（满额） | internal | business-field | semantic-review-required |
| 10 | `card_value_set` | `decimal(10,2)` | 否 |  |  | 卡消费多少元抽一次（满额） | internal | business-field | semantic-review-required |
| 11 | `is_add_up` | `tinyint(1)` | 否 |  |  | 是否累计次数（满额） | internal | business-field | semantic-review-required |
| 12 | `integral` | `int(11)` | 否 |  |  | 积分多少抽一次奖(积分) | internal | business-field | semantic-review-required |
| 13 | `win_probability` | `decimal(6,5)` | 否 |  |  | 中奖几率 | internal | business-field | semantic-review-required |
| 14 | `win_set` | `int(11)` | 否 |  |  | 中奖次数设置，0每次都有机会中奖，1有效期仅有一次中奖 | internal | business-field | semantic-review-required |
| 15 | `reward_price` | `decimal(10,2)` | 否 |  |  | 奖励金额 | internal | business-field | semantic-review-required |
| 16 | `is_pay` | `tinyint(1)` | 否 |  |  | 是否支付 | internal | business-field | semantic-review-required |
| 17 | `is_refund` | `tinyint(1)` | 否 |  |  | 是否退款 | internal | business-field | semantic-review-required |
| 18 | `refund_price` | `decimal(10,2)` | 否 |  |  | 退款金额 | internal | business-field | semantic-review-required |
| 19 | `lottery_rules` | `varchar(500)` | 否 |  |  | 活动规则 | internal | business-field | semantic-review-required |
| 20 | `lottery_count` | `int(11)` | 否 |  |  | 已抽奖次数 | internal | business-field | semantic-review-required |
| 21 | `begin_date` | `date` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 22 | `end_date` | `date` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 23 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 24 | `state` | `int(11)` | 否 |  |  | 状态 -2删除，-1未支付 0暂停 1正常 2未开始 3结束 | internal | business-field | semantic-review-required |
| 25 | `end_reason` | `int(11)` | 否 |  |  | 结束原因 0默认 1到期 2优惠券发放完毕 | internal | business-field | semantic-review-required |
| 26 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 27 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 28 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 29 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `lottery_coupon`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `lottery_id` | `int(11)` | 否 |  |  | 抽奖id | internal | relation-key | server-filter-only |
| 4 | `lottery_item_id` | `int(11)` | 否 |  |  | 抽奖项目id | internal | relation-key | server-filter-only |
| 5 | `coupon_id` | `int(11)` | 否 |  |  | 优惠券id | internal | relation-key | server-filter-only |
| 6 | `coupon_sum` | `int(11)` | 否 |  |  | 优惠券数量 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 1启用 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `lottery_item`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `lottery_id` | `int(11)` | 否 |  |  | 抽奖id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `item_index` | `int(11)` | 否 |  |  | 抽奖项位置1-8 | internal | business-field | semantic-review-required |
| 5 | `is_reward` | `tinyint(1)` | 否 |  |  | 是否包含奖励 | internal | business-field | semantic-review-required |
| 6 | `win_probability` | `decimal(6,5)` | 否 |  |  | 中奖几率 | internal | business-field | semantic-review-required |
| 7 | `reward_title` | `varchar(20)` | 是 |  |  | 奖品名称 | internal | business-field | semantic-review-required |
| 8 | `reward_level` | `int(11)` | 否 |  |  | 奖品级别 0特等奖，1-3等奖 4普通奖 | internal | business-field | semantic-review-required |
| 9 | `reward_type` | `int(11)` | 否 |  |  | 奖励类型0优惠券，1积分，2红包奖励，3实物奖励 | internal | business-field | semantic-review-required |
| 10 | `reward_value` | `decimal(10,2)` | 否 |  |  | 奖励之（积分，红包） | internal | business-field | semantic-review-required |
| 11 | `reward_count` | `int(11)` | 否 |  |  | 奖励数量-1不限 | internal | business-field | semantic-review-required |
| 12 | `reward_win_count` | `int(11)` | 否 |  |  | 中奖数量 | internal | business-field | semantic-review-required |
| 13 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 15 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 18 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `lottery_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `lottery_id` | `int(11)` | 否 |  |  | 抽奖id | internal | relation-key | server-filter-only |
| 5 | `is_win` | `tinyint(1)` | 否 |  |  | 是否中奖 | internal | business-field | semantic-review-required |
| 6 | `lottery_code` | `varchar(50)` | 否 |  |  | 抽奖编码 | internal | business-field | semantic-review-required |
| 7 | `lottery_item_id` | `int(11)` | 否 |  |  | 抽奖项目id | internal | relation-key | server-filter-only |
| 8 | `create_date` | `datetime` | 否 |  |  | 抽奖时间 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `lottery_user`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `lottery_id` | `int(11)` | 否 |  |  | 抽奖id | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `lottery_count` | `int(11)` | 否 |  |  | 抽奖次数 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_store`：唯一 BTREE（store_id, lottery_id, uid）

### `marketing_log`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：营销日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 营销日志 唯一主键 | internal | relation-key | server-filter-only |
| 2 | `marketing_id` | `int(11)` | 否 | MUL |  | 营销ID | internal | relation-key | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `is_vip` | `tinyint(1)` | 否 |  |  | 是否是会员 | internal | business-field | semantic-review-required |
| 5 | `recom_uid` | `int(11)` | 否 |  | 0 | 推荐人ID | internal | business-field | semantic-review-required |
| 6 | `log_type` | `int(11)` | 否 |  |  | 0 查看 1领券 | internal | business-field | semantic-review-required |
| 7 | `request_ip` | `varchar(30)` | 否 |  |  | 请求IP | sensitive-unstructured | business-field | deny |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 1正常 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `marketingId`：非唯一 BTREE（marketing_id）

### `marketing_user_where`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：营销筛选会员条件

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `marketing_id` | `int(11)` | 否 |  |  | 活动ID | internal | relation-key | server-filter-only |
| 4 | `balance_value_min` | `decimal(10,2)` | 否 |  |  | 剩余储值金额最小值  -1 表示不限制 | internal | business-field | semantic-review-required |
| 5 | `balance_value_max` | `decimal(10,2)` | 否 |  |  | 剩余储值金额最大值  -1 表示不限制 | internal | business-field | semantic-review-required |
| 6 | `validity_value` | `int(11)` | 否 |  |  | 所有会员卡在多少天之内过期  -1 表示不限制 | internal | business-field | semantic-review-required |
| 7 | `last_days` | `int(11)` | 否 |  |  | 所有会员卡在多少天之内未消费 -1表示不设置 | internal | business-field | semantic-review-required |
| 8 | `quantity_money` | `int(11)` | 否 |  | -1 | -1 不限制 0有余额会员  1无余额会员 | internal | business-field | semantic-review-required |
| 9 | `sex` | `int(11)` | 否 |  | -1 | -1 不限制 1男 2女 | internal | business-field | semantic-review-required |
| 10 | `open_card_date_start` | `varchar(30)` | 否 |  |  | 开卡日期开始 | internal | business-field | semantic-review-required |
| 11 | `open_card_date_end` | `varchar(30)` | 否 |  |  | 开卡日期结束 | internal | business-field | semantic-review-required |
| 12 | `consumption_date_start` | `varchar(30)` | 否 |  |  | 消费日期开始 | internal | business-field | semantic-review-required |
| 13 | `consumption_date_end` | `varchar(30)` | 否 |  |  | 消费日期结束 | internal | business-field | semantic-review-required |
| 14 | `state` | `int(11)` | 否 |  |  | 1正常 -1删除 | internal | business-field | semantic-review-required |
| 15 | `consumption_mony_min` | `decimal(10,2)` | 否 |  | -1.00 | 消费金额开始 | internal | business-field | semantic-review-required |
| 16 | `consumption_mony_max` | `decimal(10,2)` | 否 |  | -1.00 | 消费金额结束 | internal | business-field | semantic-review-required |
| 17 | `consumption_sum_min` | `decimal(10,2)` | 否 |  | -1.00 | 消费次数开始 | internal | business-field | semantic-review-required |
| 18 | `consumption_sum_max` | `decimal(10,2)` | 否 |  | -1.00 | 消费次数结束 | internal | business-field | semantic-review-required |
| 19 | `card_sum_min` | `decimal(10,2)` | 否 |  | -1.00 | 剩余次数开始 | internal | business-field | semantic-review-required |
| 20 | `card_sum_max` | `decimal(10,2)` | 否 |  | -1.00 | 剩余次数结束 | internal | business-field | semantic-review-required |
| 21 | `card_group_name` | `varchar(255)` | 否 |  |  | 卡分组名称 | internal | business-field | semantic-review-required |
| 22 | `group_name` | `varchar(255)` | 否 |  |  | 分组的名称 | internal | business-field | semantic-review-required |
| 23 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 24 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 25 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 26 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 27 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `marketing_user_where_service`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：营销筛选会员条件与项目关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `item_id` | `int(11)` | 否 |  |  | 项目ID | internal | relation-key | server-filter-only |
| 3 | `item_name` | `varchar(50)` | 否 |  |  | 项目名称 | internal | business-field | semantic-review-required |
| 4 | `marketing_user_where_id` | `int(11)` | 否 |  |  | 筛选条件 ID | internal | relation-key | server-filter-only |
| 5 | `item_value_min` | `int(11)` | 否 |  | -1 | 项目剩余次数 少于  -1不限制 | internal | business-field | semantic-review-required |
| 6 | `item_value_max` | `int(11)` | 否 |  | -1 | 项目剩余次数 多于  -1不限制 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  |  | 1正常 -1 删除 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `merger_card_log`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 卡id | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_child_id` | `int(11)` | 否 |  |  | 子卡id | internal | relation-key | server-filter-only |
| 5 | `new_card_child_id` | `int(11)` | 否 |  | 0 | 新卡ID | internal | relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 7 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `message`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `room_id` | `int(11)` | 是 |  |  |  | internal | relation-key | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  |  | internal | subject-or-relation-key | server-filter-only |
| 4 | `message_type` | `int(11)` | 是 |  |  |  | sensitive-unstructured | business-field | deny |
| 5 | `send_time` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `content` | `varchar(300)` | 是 |  |  |  | sensitive-unstructured | business-field | deny |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `notice`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `content` | `varchar(500)` | 否 |  |  | 内容 | sensitive-unstructured | business-field | deny |
| 3 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 4 | `level` | `int(11)` | 否 |  | 0 | 等级；0-默认，1-常规，2-优先，3-紧急 | internal | business-field | semantic-review-required |
| 5 | `link_type` | `int(11)` | 否 |  | 0 | 跳转类型；0-无，1-app内部，2-外链 | internal | business-field | semantic-review-required |
| 6 | `link_url` | `varchar(255)` | 否 |  |  | 跳转地址；link_type为1需要定义标识，为2则是跳转地址 | internal | business-field | semantic-review-required |
| 7 | `order_by` | `int(11)` | 否 |  | 0 | 排序字段 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `notice_center`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `platform` | `int(11)` | 否 |  |  | 平台  0=C端  1=B端 2yuyue 3线下 | internal | business-field | semantic-review-required |
| 5 | `message_type` | `int(11)` | 否 |  |  | 消息类型 0会员卡支付，1付款 2充值，3管理员操作卡余额，4会员卡到期提醒C，10预约提交通知C 11预约确认B，12预约已确认C，13预约提醒C 14预约提醒B 15预约变动C 16预约取消B ，20 收到优惠券C，21优惠券到期C ,30积分增加C，31积分到期C，40 运营消息 50软件到期提醒 50 佣金消息 500 异常消息 | sensitive-unstructured | business-field | deny |
| 6 | `card_id` | `int(11)` | 否 |  |  | 会员卡的ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单id | internal | relation-key | server-filter-only |
| 8 | `reservation_id` | `int(11)` | 否 |  |  | 预约id | internal | relation-key | server-filter-only |
| 9 | `coupon_ids` | `varchar(50)` | 是 |  |  | 优惠券id集合 | internal | business-field | semantic-review-required |
| 10 | `integral` | `int(11)` | 否 |  |  | 积分 | internal | business-field | semantic-review-required |
| 11 | `commission` | `decimal(10,2)` | 否 |  |  | 佣金 | internal | business-field | semantic-review-required |
| 12 | `send_date` | `datetime` | 否 |  |  | 发送时间 | internal | business-field | semantic-review-required |
| 13 | `expire_days` | `int(11)` | 是 |  |  | 到期天数（软件到期提醒的时候，将剩余的到期天数存放到这里） | internal | business-field | semantic-review-required |
| 14 | `service_end_date` | `datetime` | 是 |  |  | 软件服务到期时间（软件到期提醒的时候用，将软件的到期 日期存储在该字段里） | internal | business-field | semantic-review-required |
| 15 | `store_name` | `varchar(30)` | 是 |  |  | 店铺名称（发送店铺服务到期所用） | internal | business-field | semantic-review-required |
| 16 | `soft_version` | `int(11)` | 是 |  |  | 软件版本 1试用版、2基础版、3标准版、4预约版、5营销版、10高级版 | internal | business-field | semantic-review-required |
| 17 | `state` | `int(11)` | 否 |  |  | 消息状态0未发送 1已发送 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 19 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `notice_class`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `class_title` | `varchar(100)` | 否 |  |  | 分类标题 | internal | business-field | semantic-review-required |
| 3 | `order_by` | `int(11)` | 否 |  |  | 排序 倒序 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `notice_public_set`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `notice_class_id` | `int(11)` | 否 |  |  | 通知类型Id | internal | relation-key | server-filter-only |
| 3 | `notice_title` | `varchar(50)` | 否 |  |  | 通知标题 | internal | business-field | semantic-review-required |
| 4 | `notice_code` | `varchar(50)` | 否 |  |  | 通知code | internal | business-field | semantic-review-required |
| 5 | `notice_describe` | `varchar(500)` | 是 |  |  | 描述 | internal | business-field | semantic-review-required |
| 6 | `notice_type` | `int(11)` | 否 |  |  | 通知类型 0消费者通知 1商家通知 2预约教练通知 | internal | business-field | semantic-review-required |
| 7 | `is_wechat` | `tinyint(4)` | 否 |  |  | 是否支持微信通知 | internal | business-field | semantic-review-required |
| 8 | `wechat_is_default` | `tinyint(4)` | 否 |  |  | 微信通知是否默认打开 | internal | business-field | semantic-review-required |
| 9 | `wechat_temp_id` | `varchar(100)` | 是 |  |  | 微信消息模板id | internal | relation-key | server-filter-only |
| 10 | `wechat_demo` | `varchar(100)` | 是 |  |  | 示例图片 | internal | business-field | semantic-review-required |
| 11 | `is_sms` | `tinyint(4)` | 否 |  |  | 是否支持短信通知 | internal | business-field | semantic-review-required |
| 12 | `sms_is_default` | `tinyint(4)` | 否 |  |  | 短信通知是否默认打开 | internal | business-field | semantic-review-required |
| 13 | `sms_temp_id` | `varchar(30)` | 是 |  |  | 短信模板id | internal | relation-key | server-filter-only |
| 14 | `sms_demo` | `varchar(100)` | 是 |  |  | 短信示例 | internal | business-field | semantic-review-required |
| 15 | `order_by` | `int(11)` | 否 |  |  | 排序 倒序 | internal | business-field | semantic-review-required |
| 16 | `is_set_remind_time` | `tinyint(1)` | 否 |  | 0 | 是否可以提前设置通知时间 | internal | business-field | semantic-review-required |
| 17 | `state` | `int(11)` | 否 |  | 1 | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `pay_preferentia_review_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：审核日志


| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `experience_pay_limit` | `decimal(10,2)` | 是 |  |  | 收款额度 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  |  | 当前状态：-1拒绝 0待审核 1通过 | internal | business-field | semantic-review-required |
| 5 | `reason` | `varchar(50)` | 是 |  |  | 不通过原因 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 管理员id | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `pay_way_extend`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `pay_way_name` | `varchar(255)` | 是 |  |  | 支付渠道名称 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 是 |  | 1 |  | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `performance_export_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：绩效导出Excel记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键Id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 否 |  |  | 员工ID  0所有员工 | internal | subject-or-relation-key | server-filter-only |
| 4 | `export_email` | `varchar(30)` | 否 |  |  | 绩效导出的邮箱地址 | sensitive | business-field | masked-or-filter-only |
| 5 | `statistics` | `varchar(20)` | 否 |  |  | 绩效统计的月份 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 0 待发送 1 已发送 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：绩效方式类型表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `item_type` | `int(11)` | 否 |  |  | 绩效方式类型 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 3 | `item_name` | `varchar(20)` | 否 |  |  | 绩效方式名称 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  |  | 1正常 0暂停使用 -1  删除 | internal | business-field | semantic-review-required |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `platform_content_tag`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：平台内容标签表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 标签主键ID | internal | relation-key | server-filter-only |
| 2 | `tag_name` | `varchar(50)` | 否 |  |  | 标签名称 | internal | business-field | semantic-review-required |
| 3 | `sort_order` | `int(11)` | 否 |  | 0 | 排序值，数值越大越靠前 | internal | business-field | semantic-review-required |
| 4 | `state` | `tinyint(4)` | 否 |  | 1 | 状态：0已删除，1正常 | internal | business-field | semantic-review-required |
| 5 | `created_by` | `bigint(20)` | 否 |  | 0 | 创建人用户ID | internal | business-field | semantic-review-required |
| 6 | `created_at` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 7 | `updated_by` | `bigint(20)` | 否 |  | 0 | 最后修改人用户ID | internal | business-field | semantic-review-required |
| 8 | `updated_at` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 最后修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `platform_video_tag_relation`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：平台内容与标签关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 关联记录主键ID | internal | relation-key | server-filter-only |
| 2 | `video_id` | `bigint(20)` | 否 |  |  | 平台内容ID，对应platform_videos.id | internal | relation-key | server-filter-only |
| 3 | `tag_id` | `bigint(20)` | 否 |  |  | 标签ID，对应platform_content_tag.id | internal | relation-key | server-filter-only |
| 4 | `state` | `tinyint(4)` | 否 |  | 1 | 状态：0已取消关联，1正常关联 | internal | business-field | semantic-review-required |
| 5 | `created_by` | `bigint(20)` | 否 |  | 0 | 创建人用户ID | internal | business-field | semantic-review-required |
| 6 | `created_at` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 7 | `updated_by` | `bigint(20)` | 否 |  | 0 | 最后修改人用户ID | internal | business-field | semantic-review-required |
| 8 | `updated_at` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 最后修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `poster`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：海报

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `poster_title` | `varchar(50)` | 否 |  |  | 海报标题 | internal | business-field | semantic-review-required |
| 3 | `poster_img` | `varchar(100)` | 否 |  |  | 海报路径 | internal | business-field | semantic-review-required |
| 4 | `poster_default_img` | `varchar(100)` | 否 |  |  | 海报默认底图图 | internal | business-field | semantic-review-required |
| 5 | `poster_type` | `int(11)` | 否 |  |  | 类型：0朋友圈海报，1物料（购卡送券）2抽奖，3安心充，5物料（收款码） | internal | business-field | semantic-review-required |
| 6 | `materiel_type` | `int(11)` | 否 |  |  | 物料类型：0海报，1A4台牌 ，2哆啦宝， | internal | business-field | semantic-review-required |
| 7 | `materiel_material` | `varchar(20)` | 否 |  |  | 物料材质 | internal | business-field | semantic-review-required |
| 8 | `materiel_size` | `varchar(20)` | 否 |  |  | 规格大小 0X0 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 是 |  | 0.00 | 价格 | internal | business-field | semantic-review-required |
| 10 | `materiel_unit` | `varchar(10)` | 否 |  |  | 单位：张 | internal | business-field | semantic-review-required |
| 11 | `is_title` | `tinyint(1)` | 否 |  |  | 是否包含title | internal | business-field | semantic-review-required |
| 12 | `is_free` | `tinyint(1)` | 否 |  |  | 是否免费 | internal | business-field | semantic-review-required |
| 13 | `is_vip` | `tinyint(1)` | 否 |  |  | 是否vip | internal | business-field | semantic-review-required |
| 14 | `is_hot` | `tinyint(1)` | 否 |  |  | 是否热门 | internal | business-field | semantic-review-required |
| 15 | `used_sum` | `int(11)` | 否 |  |  | 使用次数 | internal | business-field | semantic-review-required |
| 16 | `card_sum` | `int(11)` | 否 |  |  | 购卡送券，显示卡数量 | internal | business-field | semantic-review-required |
| 17 | `order_by` | `int(11)` | 否 |  |  | 排序 | internal | business-field | semantic-review-required |
| 18 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 19 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 20 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 21 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `poster_copywriting`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：海报文案关联

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `poster_id` | `int(11)` | 否 |  |  | 海报ID | internal | relation-key | server-filter-only |
| 3 | `copywriting_id` | `int(11)` | 否 |  |  | 文案ID | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 5 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `poster_item`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：海报动态内容

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `poster_id` | `int(11)` | 否 |  |  | 海报ID | internal | relation-key | server-filter-only |
| 3 | `item_name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 4 | `item_type` | `int(11)` | 否 |  |  | 类型 0文字 1图片 2二维码 | internal | business-field | semantic-review-required |
| 5 | `item_code` | `varchar(100)` | 否 |  |  | code | internal | business-field | semantic-review-required |
| 6 | `item_default_value` | `varchar(50)` | 是 |  |  | 默认值 | internal | business-field | semantic-review-required |
| 7 | `item_x` | `int(11)` | 否 |  |  | 坐标X轴 | internal | business-field | semantic-review-required |
| 8 | `item_y` | `int(11)` | 否 |  |  | 坐标X轴 | internal | business-field | semantic-review-required |
| 9 | `item_w` | `int(11)` | 否 |  |  | 坐标X轴 | internal | business-field | semantic-review-required |
| 10 | `item_h` | `int(11)` | 否 |  |  | 坐标X轴 | internal | business-field | semantic-review-required |
| 11 | `font_name` | `varchar(20)` | 是 |  |  | 字体 | internal | business-field | semantic-review-required |
| 12 | `font_size` | `int(11)` | 否 |  |  | 字号 | internal | business-field | semantic-review-required |
| 13 | `font_color` | `varchar(10)` | 是 |  |  | 字体颜色 | internal | business-field | semantic-review-required |
| 14 | `row_height` | `int(11)` | 否 |  |  | 行间距 | internal | business-field | semantic-review-required |
| 15 | `line_padding` | `int(11)` | 否 |  |  | 字间距 | internal | business-field | semantic-review-required |
| 16 | `is_bold` | `tinyint(1)` | 否 |  |  | 是否加粗 | internal | business-field | semantic-review-required |
| 17 | `card_style` | `int(11)` | 否 |  |  | 卡样式 0单卡 1多卡 左右 | internal | business-field | semantic-review-required |
| 18 | `order_by` | `int(11)` | 否 |  | 0 | 排序字段  倒序排序 | internal | business-field | semantic-review-required |
| 19 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 20 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 21 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 22 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 23 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `poster_store_type`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：海报与店铺类型关联

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `poster_id` | `int(11)` | 否 |  |  | 海报ID | internal | relation-key | server-filter-only |
| 3 | `store_type_id` | `varchar(11)` | 否 |  |  | 店铺类型ID | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 5 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 6 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  |  创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `poster_tag`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：海报标签表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 标签Id | internal | relation-key | server-filter-only |
| 2 | `tag_name` | `varchar(50)` | 否 |  |  | 标签名称 | internal | business-field | semantic-review-required |
| 3 | `store_id` | `int(11)` | 否 |  | 0 | 店铺ID 默认0系统 | internal | store-scope | server-filter-only |
| 4 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 0停用 1正常 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `poster_tag_class`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：无。
表注释：标签与店铺行业关联

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `tag_id` | `int(11)` | 否 |  |  | 标签ID | internal | relation-key | server-filter-only |
| 3 | `store_class_id` | `varchar(10)` | 否 |  |  | 行业分类Id | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 | internal | business-field | semantic-review-required |
| 5 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 6 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `print_config`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 4 | `print_device_id` | `int(11)` | 否 |  | 0 | 打印设备表id | internal | relation-key | server-filter-only |
| 5 | `print_name` | `varchar(100)` | 否 |  |  | 设备名称 | internal | business-field | semantic-review-required |
| 6 | `print_sn` | `varchar(30)` | 否 |  |  | 设备编号 | internal | business-field | semantic-review-required |
| 7 | `print_key` | `varchar(30)` | 否 |  |  | 设备KEY | internal | business-field | semantic-review-required |
| 8 | `print_sum` | `int(11)` | 否 |  | 1 | 打印份数 | internal | business-field | semantic-review-required |
| 9 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编号 | internal | business-field | semantic-review-required |
| 10 | `equipment_brand` | `int(11)` | 否 |  |  | 设备品牌 0飞鹅，1ZKC | internal | business-field | semantic-review-required |
| 11 | `equipment_type` | `int(11)` | 否 |  |  | 设备类型 0打印机 1云喇叭 | internal | business-field | semantic-review-required |
| 12 | `is_consumption` | `tinyint(1)` | 否 |  | 1 | 是否打印支付、核销订单 | internal | business-field | semantic-review-required |
| 13 | `is_xiaofeidan` | `tinyint(1)` | 否 |  | 1 | 是否打印消费单；0-否，1-是 | internal | business-field | semantic-review-required |
| 14 | `is_yujiedan` | `tinyint(1)` | 否 |  | 1 | 是否打印预结单；0-否，1-是 | internal | business-field | semantic-review-required |
| 15 | `is_jiezhangdan` | `tinyint(1)` | 否 |  | 1 | 是否打印结账单；0-否，1-是 | internal | business-field | semantic-review-required |
| 16 | `is_chufangdan` | `tinyint(1)` | 否 |  | 1 | 是否打印厨房单；0-否，1-是 | internal | business-field | semantic-review-required |
| 17 | `food_print_sum` | `int(11)` | 否 |  | 1 | 食品相关打印份数 | internal | business-field | semantic-review-required |
| 18 | `is_youji` | `tinyint(1)` | 否 |  |  | 是否打印商城邮寄单 | internal | business-field | semantic-review-required |
| 19 | `is_ziti` | `tinyint(1)` | 否 |  |  | 是否打印商城自提单 | internal | business-field | semantic-review-required |
| 20 | `is_peisong` | `tinyint(1)` | 否 |  |  | 是否打印商城配送单 | internal | business-field | semantic-review-required |
| 21 | `shop_print_sum` | `int(11)` | 否 |  | 1 | 商品相关打印份数 | internal | business-field | semantic-review-required |
| 22 | `state` | `int(11)` | 否 |  | 0 | 状态 0暂停使用 -1 删除 1正常 | internal | business-field | semantic-review-required |
| 23 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 24 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 25 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 26 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `print_config_food_tag_relation`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `print_config_id` | `int(11)` | 否 |  | 0 | 打印设备id | internal | relation-key | server-filter-only |
| 4 | `food_tag_id` | `int(11)` | 否 |  | 0 | 标签id | internal | relation-key | server-filter-only |
| 5 | `print_num` | `int(11)` | 否 |  | 0 | 打印数量 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用，-1删除 | internal | business-field | semantic-review-required |
| 7 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 9 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `print_device`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `added_services_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 3 | `img` | `varchar(255)` | 否 |  |  | 图片 | internal | business-field | semantic-review-required |
| 4 | `name` | `varchar(255)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 5 | `equipment_brand` | `int(11)` | 否 |  | 0 | 设备品牌 0飞鹅，1ZKC | internal | business-field | semantic-review-required |
| 6 | `equipment_type` | `int(11)` | 否 |  | 0 | 设备类型 0打印机 1云喇叭 2标签机 | internal | business-field | semantic-review-required |
| 7 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `privilege_group`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：默认权限组

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `title` | `varchar(50)` | 否 |  |  | 权限组标题 | internal | business-field | semantic-review-required |
| 3 | `group_info` | `varchar(255)` | 否 |  |  | 权限组介绍 | internal | business-field | semantic-review-required |
| 4 | `order_by` | `int(11)` | 否 |  |  | 排序 倒序 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `privilege_group_permission`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：权限组 权限明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `group_id` | `bigint(20)` | 否 |  |  | 权限组id | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 权限id | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 0不可用 1可用 | internal | business-field | semantic-review-required |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：商品表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 商品ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `product_name` | `varchar(100)` | 否 |  |  | 商品名称 | internal | business-field | semantic-review-required |
| 4 | `product_unit` | `varchar(10)` | 是 |  |  | 商品单位 | internal | business-field | semantic-review-required |
| 5 | `product_img` | `varchar(100)` | 否 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `is_have_sku` | `tinyint(1)` | 否 |  |  | 是否包含SKU | internal | business-field | semantic-review-required |
| 7 | `is_exchange` | `tinyint(1)` | 否 |  | 0 | 是否是兑换商品 | internal | business-field | semantic-review-required |
| 8 | `exchange_integral` | `int(11)` | 否 |  | 0 | 兑换积分 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `vip_price` | `decimal(10,2)` | 否 |  |  | 会员价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣价 | internal | business-field | semantic-review-required |
| 12 | `product_info` | `varchar(1000)` | 是 |  |  | 商品信息 | internal | business-field | semantic-review-required |
| 13 | `quantity` | `int(11)` | 否 |  |  | 库存 | internal | business-field | semantic-review-required |
| 14 | `sell_num` | `int(11)` | 否 |  | 0 | 售出数量 | internal | business-field | semantic-review-required |
| 15 | `remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 16 | `detail` | `varchar(4000)` | 是 |  |  | 详情 | internal | business-field | semantic-review-required |
| 17 | `product_class` | `varchar(10)` | 否 |  |  | 商品分类 | internal | business-field | semantic-review-required |
| 18 | `is_express` | `int(11)` | 否 |  | 0 | 是否需要快递服务；0-不需要，1-需要 | internal | business-field | semantic-review-required |
| 19 | `is_card_discount` | `tinyint(1)` | 否 |  |  | 是否参与卡折扣 | internal | business-field | semantic-review-required |
| 20 | `is_pay` | `tinyint(1)` | 否 |  |  | 是否参与支付 | internal | business-field | semantic-review-required |
| 21 | `pno` | `varchar(100)` | 是 |  |  | 货号 | internal | business-field | semantic-review-required |
| 22 | `is_purchase_limit` | `tinyint(1)` | 否 |  |  | 是否限购 | internal | business-field | semantic-review-required |
| 23 | `purchase_limit_type` | `int(11)` | 否 |  |  | 限购方式 0永久 1天  | internal | business-field | semantic-review-required |
| 24 | `purchase_limit_sum` | `int(11)` | 是 |  |  | 限购数量 | internal | business-field | semantic-review-required |
| 25 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 26 | `type` | `int(11)` | 否 |  | 0 | 商品类型；0-默认，1-商城 | internal | business-field | semantic-review-required |
| 27 | `state` | `int(11)` | 否 |  |  | 0下架 1上架 | internal | business-field | semantic-review-required |
| 28 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 29 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 30 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `is_recommend` | `tinyint(1)` | 是 |  |  | 是否推荐位 | internal | business-field | semantic-review-required |
| 34 | `enjoy_vip_discount` | `tinyint(1)` | 否 |  | 1 | 享受会员折扣价 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_class`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：商品分类

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `class_name` | `varchar(50)` | 否 |  |  | 分类名称 | internal | business-field | semantic-review-required |
| 3 | `class_img` | `varchar(255)` | 是 |  |  | 分类图片 | internal | business-field | semantic-review-required |
| 4 | `class_id` | `varchar(20)` | 否 |  |  | 分类ID | internal | relation-key | server-filter-only |
| 5 | `root_id` | `varchar(20)` | 否 |  |  | 父级ID | internal | relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 7 | `sort` | `int(11)` | 否 |  |  | 排序位置，数值越大，位置越靠前 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 1正常 0停用 -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_class_img`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `img` | `varchar(150)` | 是 |  |  | 图片 | internal | business-field | semantic-review-required |
| 4 | `tenant_id` | `int(11)` | 是 |  |  |  | internal | tenant-scope | server-filter-only |
| 5 | `state` | `int(11)` | 是 |  |  | 状态；1-开启，0-关闭 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_class_join`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：商品分类关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `product_id` | `int(11)` | 否 |  | 0 | 商品id | internal | relation-key | server-filter-only |
| 4 | `product_class_id` | `int(11)` | 否 |  | 0 | 商品分类id | internal | relation-key | server-filter-only |
| 5 | `order_by` | `int(11)` | 否 |  |  | 排序 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 0 | 状态；0-停用，1-启用；-1删除 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 8 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_class_sku`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `class_id` | `varchar(20)` | 否 |  |  | 分类id | internal | relation-key | server-filter-only |
| 4 | `sku_id` | `int(11)` | 否 |  |  | SKU id | internal | relation-key | server-filter-only |
| 5 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户Id | internal | tenant-scope | server-filter-only |
| 7 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_img`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：商品图片表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `product_id` | `int(11)` | 否 |  | 0 | 商品id | internal | relation-key | server-filter-only |
| 4 | `img` | `varchar(255)` | 否 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 5 | `is_main` | `int(11)` | 否 |  | 0 | 是否是主图封面图；0-否，1-是 | internal | business-field | semantic-review-required |
| 6 | `type` | `int(11)` | 否 |  | 0 | 图片类型；1-主图，2-详情 | internal | business-field | semantic-review-required |
| 7 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  | 0 | 状态；0-停用，1-启用；-1删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  |  | internal | tenant-scope | server-filter-only |
| 10 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_meun`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：产品菜单表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `product_type` | `int(11)` | 否 |  | 0 | 产品类型 0小程序C 1小程序B 3公众号 4企业微信 | internal | business-field | semantic-review-required |
| 3 | `meun_type` | `int(11)` | 否 |  |  | 菜单类型 0链接 10卡列表 11单卡 20券列表 21单券 22单券包 30商城 31商品  40点单 42餐品 42餐台 50预约 | internal | business-field | semantic-review-required |
| 4 | `meun_name` | `varchar(50)` | 否 |  |  | 菜单名称 | internal | business-field | semantic-review-required |
| 5 | `is_selected` | `tinyint(1)` | 否 |  | 0 | 是否多选子项 | internal | business-field | semantic-review-required |
| 6 | `meun_image` | `varchar(100)` | 是 |  |  | 默认分享图 | internal | business-field | semantic-review-required |
| 7 | `meun_title` | `varchar(20)` | 是 |  |  | 菜单标题 | internal | business-field | semantic-review-required |
| 8 | `meun_info` | `varchar(100)` | 是 |  |  | 菜单简介 | internal | business-field | semantic-review-required |
| 9 | `meun_url` | `varchar(100)` | 是 |  |  | 菜单url | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  | 1 | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 11 | `module_id` | `int(11)` | 否 |  |  | 模块id | internal | relation-key | server-filter-only |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_sku`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：分类sku关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 3 | `outer_id` | `varchar(30)` | 否 |  |  | 商家编码 | internal | relation-key | server-filter-only |
| 4 | `product_sku_attr_id` | `int(11)` | 否 |  | 0 | 商品规格id | internal | relation-key | server-filter-only |
| 5 | `sku_id` | `varchar(100)` | 否 |  |  | 规格ID集合(100:001；200:002) | internal | relation-key | server-filter-only |
| 6 | `sku_name` | `varchar(100)` | 否 |  |  | Sku规格name集合(颜色：灰色；尺码XL) | internal | business-field | semantic-review-required |
| 7 | `price` | `decimal(10,2)` | 否 |  |  | SKU的价格(没有规格的产品此项存产品的价格) | internal | business-field | semantic-review-required |
| 8 | `vip_price` | `decimal(10,2)` | 否 |  |  | vip售价 | internal | business-field | semantic-review-required |
| 9 | `discount_price` | `decimal(10,2)` | 否 |  |  |  折扣价 | internal | business-field | semantic-review-required |
| 10 | `is_default` | `tinyint(1)` | 否 |  |  | 是否是默认的SKU，用来标明多个合并以后SKU的名称取哪个(1是，0否) | internal | business-field | semantic-review-required |
| 11 | `is_combination` | `tinyint(1)` | 否 |  |  | 是否是组合商品(1是，0不是) | internal | business-field | semantic-review-required |
| 12 | `quantity` | `int(11)` | 否 |  |  | 库存数量 | internal | business-field | semantic-review-required |
| 13 | `weight` | `int(11)` | 否 |  |  | 重量(单位g,默认0) | internal | business-field | semantic-review-required |
| 14 | `cost_price` | `decimal(10,2)` | 否 |  |  | 成本价格 | internal | business-field | semantic-review-required |
| 15 | `order_by` | `int(11)` | 否 |  |  |  排序 | internal | business-field | semantic-review-required |
| 16 | `store_id` | `int(11)` | 否 |  |  | 店铺id 0系统 | internal | store-scope | server-filter-only |
| 17 | `state` | `int(11)` | 否 |  |  | 当前状态(1:启用，0:禁用，-1:删除) | internal | business-field | semantic-review-required |
| 18 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 19 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 20 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 21 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_sku_attr`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：商品规格表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `product_id` | `int(11)` | 否 |  | 0 | 商品id | internal | relation-key | server-filter-only |
| 4 | `sku_attr_id` | `int(11)` | 否 |  | 0 | 商品规格id | internal | relation-key | server-filter-only |
| 5 | `name` | `varchar(255)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 6 | `is_single` | `int(11)` | 否 |  | 0 | 单选还是多选；0-单选，1-多选 | internal | business-field | semantic-review-required |
| 7 | `vip_price` | `decimal(10,2)` | 否 |  | 0.00 | 会员价格 | internal | business-field | semantic-review-required |
| 8 | `order_by` | `int(11)` | 否 |  | 0 | 排序 倒序 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  | 0 | 状态；0-停用，1-启用；-1删除 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 11 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `product_sku_attr_detail`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：商品规格属性详情

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `product_id` | `int(11)` | 否 | MUL | 0 | 商品id | internal | relation-key | server-filter-only |
| 4 | `product_sku_ids` | `varchar(500)` | 否 |  |  | id组合 | internal | business-field | semantic-review-required |
| 5 | `product_sku_names` | `varchar(500)` | 是 |  |  | 名称组合 | internal | business-field | semantic-review-required |
| 6 | `is_exchange` | `tinyint(1)` | 否 |  | 0 | 是否是兑换商品 | internal | business-field | semantic-review-required |
| 7 | `exchange_integral` | `int(11)` | 否 |  |  | 兑换所需积分 | internal | business-field | semantic-review-required |
| 8 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 价格 | internal | business-field | semantic-review-required |
| 9 | `vip_price` | `decimal(10,2) unsigned` | 否 |  | 0.00 | 会员价格 | internal | business-field | semantic-review-required |
| 10 | `quantity` | `int(11)` | 否 |  | 0 | 库存 | internal | business-field | semantic-review-required |
| 11 | `pno` | `varchar(100)` | 是 |  |  | 货号 | internal | business-field | semantic-review-required |
| 12 | `is_purchase_limit` | `tinyint(1)` | 否 |  |  | 是否限购 | internal | business-field | semantic-review-required |
| 13 | `purchase_limit_type` | `int(11)` | 否 |  |  | 限购方式 0永久 1天  | internal | business-field | semantic-review-required |
| 14 | `purchase_limit_sum` | `int(11)` | 否 |  |  | 限购数量 | internal | business-field | semantic-review-required |
| 15 | `state` | `int(11)` | 否 |  | 0 | 状态；0-无效，1-有效，-1删除 | internal | business-field | semantic-review-required |
| 16 | `tenant_id` | `int(11)` | 否 |  | 1 |  | internal | tenant-scope | server-filter-only |
| 17 | `update_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 18 | `update_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |
| 19 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 20 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_pid`：非唯一 BTREE（product_id）

### `product_tag`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：商品标签关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `product_id` | `int(11)` | 否 |  | 0 | 商品id | internal | relation-key | server-filter-only |
| 4 | `tag` | `varchar(20)` | 否 |  |  | 标签 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 0 | 状态；0-停用，1-启用；-1删除 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 7 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `promote_users`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：推广人员关系

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id | internal | subject-or-relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `parent_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 6 | `parent_card_id` | `int(11)` | 否 |  |  | 推荐人cardID | internal | relation-key | server-filter-only |
| 7 | `user_name` | `varchar(255)` | 是 |  |  | 用户名称 | sensitive | business-field | masked-or-filter-only |
| 8 | `expiration_date` | `datetime` | 是 |  |  | 分佣截止日期 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |
| 10 | `state` | `int(11)` | 是 |  |  | 状态 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `promoter`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `promoter_id` | `int(11)` | 否 |  |  | 推官员id | internal | relation-key | server-filter-only |
| 4 | `promotion_code` | `varchar(255)` | 是 |  |  | 推广码 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 1 |  | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `promotion_code`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  | 0 | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `code` | `varchar(20)` | 否 |  |  | 推广码 | internal | business-field | semantic-review-required |
| 4 | `agent_id` | `int(11)` | 否 |  |  | 代理id | internal | relation-key | server-filter-only |
| 5 | `channel_id` | `int(11)` | 否 |  | 0 | 渠道id | internal | relation-key | server-filter-only |
| 6 | `remark` | `varchar(20)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  | 1 | 状态 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `provinces`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `class_id` | `varchar(10)` | 否 |  |  | 类id | internal | relation-key | server-filter-only |
| 3 | `name` | `varchar(20)` | 否 |  |  | 省名称 | internal | business-field | semantic-review-required |
| 4 | `root_id` | `varchar(10)` | 否 |  | 0 | 父类id | internal | relation-key | server-filter-only |
| 5 | `p_type` | `int(11)` | 否 |  | 0 | 类型 0省，1市 2区 | internal | business-field | semantic-review-required |
| 6 | `cid` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `rel_user_message`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `mid` | `int(11)` | 否 |  |  | 消息ID | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0已读 1未读 | internal | business-field | semantic-review-required |
| 5 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 6 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `reservation_tag`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：无。
表注释：预约相关标签

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `tag_type` | `int(11)` | 否 |  |  | 标签类型：1个人标签 2擅长3课程 4课程图片 5课程分类 | internal | business-field | semantic-review-required |
| 3 | `tag_title` | `varchar(50)` | 否 |  |  | 标签名 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  | 1 | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 5 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 修改时间 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `return_visit`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 回访记录唯一标识ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `visit_type` | `int(11)` | 否 |  |  | 回访类型 0微信   1电话 | internal | business-field | semantic-review-required |
| 4 | `visit_content` | `varchar(200)` | 是 |  |  | 回访内容 | sensitive-unstructured | business-field | deny |
| 5 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0默认，1正常 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人ID | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `rider_food_order`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `store_rider_id` | `int(11)` | 否 |  |  | 骑手id | internal | relation-key | server-filter-only |
| 4 | `food_order_id` | `int(11)` | 否 |  |  |  | internal | relation-key | server-filter-only |
| 5 | `staff_id` | `int(11)` | 否 |  |  | 员工id | internal | subject-or-relation-key | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态；0-配送中，1-配送成功，2-取消 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `sensitive_word`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：敏感词

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `key_word` | `varchar(20)` | 否 |  |  | 敏感词 | internal | business-field | semantic-review-required |
| 3 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `service_item_card_item`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：价目表购物车子表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `service_item_card_id` | `int(11)` | 是 |  |  | 购物车id | internal | relation-key | server-filter-only |
| 4 | `service_item_id` | `int(11)` | 是 |  |  | 价目表服务的id | internal | relation-key | server-filter-only |
| 5 | `service_item_count` | `int(11)` | 是 |  |  | 价目表服务的个数 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 是 |  |  | 状态 -1：删除，0：无效，1：有效 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `service_item_cart`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：价目表购物车

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺的id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户的id | internal | subject-or-relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 是 |  |  | 状态；1-启用 | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `service_item_category`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：价目表分类

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `name` | `varchar(50)` | 是 |  |  | 名称 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 是 |  |  | 状态；-1删除，0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 5 | `order_by` | `int(11)` | 是 |  |  | 排序 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 是 |  |  |  | internal | tenant-scope | server-filter-only |
| 7 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 是 |  |  | 创建的时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  | 修改的时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `service_item_category_relation`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：价目表分类关联

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `service_item_id` | `int(11)` | 是 |  |  | 服务的id | internal | relation-key | server-filter-only |
| 4 | `service_item_category_id` | `int(11)` | 是 |  |  | 服务分类的id | internal | relation-key | server-filter-only |
| 5 | `state` | `int(11)` | 是 |  |  | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 是 |  |  |  | internal | tenant-scope | server-filter-only |
| 7 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `service_item_order_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：价目表订单子项

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `consumption_service_item_id` | `int(11)` | 是 |  |  | 服务订单的id | internal | relation-key | server-filter-only |
| 4 | `service_item_id` | `int(11)` | 是 |  |  | 价目表服务的id | internal | relation-key | server-filter-only |
| 5 | `item_name` | `varchar(50)` | 是 |  |  | 名称 | internal | business-field | semantic-review-required |
| 6 | `item_count` | `int(11)` | 是 |  |  | 个数 | internal | business-field | semantic-review-required |
| 7 | `item_unit` | `varchar(10)` | 是 |  |  | 单位 | internal | business-field | semantic-review-required |
| 8 | `item_img` | `varchar(255)` | 是 |  |  | 图片 | internal | business-field | semantic-review-required |
| 9 | `item_price` | `decimal(10,2)` | 是 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 是 |  |  | 状态 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `shop_order`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `order_type` | `int(11)` | 否 |  |  | 订单类型 0 邮寄 ,1 配送 2自提 | internal | business-field | semantic-review-required |
| 5 | `pickup_code` | `varchar(20)` | 是 |  |  | 自提提货码 | internal | business-field | semantic-review-required |
| 6 | `pic_path` | `varchar(255)` | 是 |  |  | 商品图片绝对途径 | internal | business-field | semantic-review-required |
| 7 | `title` | `varchar(255)` | 是 |  |  | 订单标题 | internal | business-field | semantic-review-required |
| 8 | `status` | `int(11)` | 是 |  |  | 订单状态：-2,退款。-1 已取消；0 等待买家付款；1 等待卖家发货 2 卖家已发货 3 订单完成 4 订单关闭 | internal | business-field | semantic-review-required |
| 9 | `is_exchange` | `tinyint(1)` | 否 |  | 0 | 是否是兑换商品 | internal | business-field | semantic-review-required |
| 10 | `exchange_integral` | `int(11)` | 否 |  | 0 | 兑换积分 | internal | business-field | semantic-review-required |
| 11 | `product_count` | `int(11)` | 是 |  |  | 商品数量 | internal | business-field | semantic-review-required |
| 12 | `need_payment` | `decimal(10,2)` | 是 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 13 | `payment` | `decimal(10,2)` | 是 |  |  | 实付金额。精确到2位小数;单位:元。如:200.07，表示:200元7分 | internal | business-field | semantic-review-required |
| 14 | `need_post` | `tinyint(1)` | 是 |  |  | 是否需要邮寄 | internal | business-field | semantic-review-required |
| 15 | `post_fee` | `decimal(10,2)` | 是 |  |  | 邮费。精确到2位小数;单位:元。如:200.07，表示:200元7分 | internal | business-field | semantic-review-required |
| 16 | `receiver_name` | `varchar(255)` | 是 |  |  | 收货人的姓名 | internal | business-field | semantic-review-required |
| 17 | `receiver_address` | `varchar(255)` | 是 |  |  | 收货人的详细地址 | sensitive | business-field | masked-or-filter-only |
| 18 | `receiver_zip` | `varchar(255)` | 是 |  |  | 收货人的邮编 | internal | business-field | semantic-review-required |
| 19 | `receiver_mobile` | `varchar(255)` | 是 |  |  | 收货人的手机号码 | sensitive | business-field | masked-or-filter-only |
| 20 | `post_company` | `varchar(255)` | 是 |  |  | 快递公司 | internal | business-field | semantic-review-required |
| 21 | `post_order_no` | `varchar(255)` | 是 |  |  | 快递单号 | internal | business-field | semantic-review-required |
| 22 | `remark` | `varchar(255)` | 是 |  |  | 买家备注 | sensitive-unstructured | business-field | deny |
| 23 | `business_remark` | `varchar(255)` | 是 |  |  | 卖家备注 | sensitive-unstructured | business-field | deny |
| 24 | `buyer_name` | `varchar(255)` | 是 |  |  | 买家名称 | internal | business-field | semantic-review-required |
| 25 | `pay_method` | `int(11)` | 是 |  |  | 支付方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 26 | `take_time` | `varchar(20)` | 是 |  |  | 自提时间 | internal | business-field | semantic-review-required |
| 27 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 28 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 29 | `post_date` | `datetime` | 是 |  |  | 发货时间 | internal | business-field | semantic-review-required |
| 30 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 33 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 34 | `integral_deduct` | `decimal(10,2)` | 否 |  |  | 积分扣除，1.00 | internal | business-field | semantic-review-required |
| 35 | `card_deduct` | `decimal(10,2)` | 否 |  |  | 会员卡扣除，1.00 | internal | business-field | semantic-review-required |
| 36 | `coupon_deduct` | `decimal(10,2)` | 否 |  |  | 优惠券扣除，1.00 | internal | business-field | semantic-review-required |
| 37 | `commission_deduct` | `decimal(10,2)` | 否 |  |  | 佣金扣除 | internal | business-field | semantic-review-required |
| 38 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `shop_order_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `shop_order_id` | `int(11)` | 是 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 5 | `product_id` | `int(11)` | 是 |  |  | 商品ID | internal | relation-key | server-filter-only |
| 6 | `sku_id` | `int(11)` | 否 |  |  | skuid | internal | relation-key | server-filter-only |
| 7 | `pno` | `varchar(50)` | 是 |  |  | 货号 | internal | business-field | semantic-review-required |
| 8 | `product_name` | `varchar(255)` | 是 |  |  | 商品名称 | internal | business-field | semantic-review-required |
| 9 | `product_img` | `varchar(255)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 10 | `is_exchange` | `tinyint(1)` | 否 |  |  | 是否是兑换商品 | internal | business-field | semantic-review-required |
| 11 | `exchange_integral` | `int(11)` | 否 |  |  | 兑换积分 | internal | business-field | semantic-review-required |
| 12 | `product_count` | `int(11)` | 是 |  |  | 数量 | internal | business-field | semantic-review-required |
| 13 | `product_price` | `decimal(10,2)` | 是 |  |  | 商品价格 | internal | business-field | semantic-review-required |
| 14 | `sku_string` | `varchar(500)` | 是 |  |  | SKU描述 | internal | business-field | semantic-review-required |
| 15 | `sku_value` | `varchar(500)` | 是 |  |  | SKU值 | internal | business-field | semantic-review-required |
| 16 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 17 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 18 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 19 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 20 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 21 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeIdAndUid`：非唯一 BTREE（store_id, uid）

### `shopping_cart`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `shopping_cart_product`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `shopping_cart_id` | `int(11)` | 是 |  |  | 购物车ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `product_id` | `int(11)` | 是 |  |  | 商品ID | internal | relation-key | server-filter-only |
| 6 | `sku_id` | `int(11)` | 否 |  |  | skuid | internal | relation-key | server-filter-only |
| 7 | `product_count` | `int(11)` | 是 |  |  | 商品数量 | internal | business-field | semantic-review-required |
| 8 | `sku_string` | `varchar(500)` | 是 |  |  | 商品规格（描述） | internal | business-field | semantic-review-required |
| 9 | `sku_value` | `varchar(500)` | 是 |  |  | 商品规格（值） | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 是 |  |  | 创建日期 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 是 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 14 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `sku_attr`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：sku属性表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID   0系统 | internal | store-scope | server-filter-only |
| 3 | `sku_name` | `varchar(20)` | 否 |  |  | SKU名称 | internal | business-field | semantic-review-required |
| 4 | `order_by` | `int(11)` | 否 |  |  | 排序 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 7 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `sku_attr_child`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：sku属性子表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `sku_id` | `int(11)` | 否 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 4 | `sku_attr` | `varchar(20)` | 否 |  |  | SKU编码 | internal | business-field | semantic-review-required |
| 5 | `sku_name` | `varchar(20)` | 否 |  |  | SKU 父属性名称 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  |  | 排序 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `sms_lable`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：标签表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `lable_name` | `varchar(20)` | 否 |  |  | 标签长度 | internal | business-field | semantic-review-required |
| 3 | `state` | `int(11)` | 否 |  |  | 状态-1删除 1正常 | internal | business-field | semantic-review-required |
| 4 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 5 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `sms_template_label`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：短信标签关联

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `template_id` | `int(11)` | 否 |  |  | 模板ID | internal | relation-key | server-filter-only |
| 3 | `lable_id` | `int(11)` | 否 |  |  | 标签ID | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 1正常 -1删除 | internal | business-field | semantic-review-required |
| 5 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 6 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `sms_template_type`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：营销类型与短信模板关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `sms_type` | `int(11)` | 否 |  |  | 模板场景 0 预约 1群发短信 2放假通知 3优惠券活动 4续费营销 5老顾客激活 6生日营销 7节日祝福 10会员绑卡 | internal | business-field | semantic-review-required |
| 3 | `template_id` | `int(11)` | 否 |  |  | 模板ID | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 | internal | business-field | semantic-review-required |
| 5 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 6 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `sms_validation`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：短信验证表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `mobile` | `varchar(11)` | 否 | MUL |  | 手机号 | sensitive | business-field | masked-or-filter-only |
| 3 | `sms_info` | `varchar(100)` | 否 |  |  | 短信内容 | internal | business-field | semantic-review-required |
| 4 | `sms_code` | `varchar(10)` | 否 |  |  | 验证码 | internal | business-field | semantic-review-required |
| 5 | `sms_type` | `int(11)` | 否 |  |  | 1：登陆，2：解绑手机 ，3：绑定手机 ,4 收款账号错误,5异常提醒，6广告，7，邀请会员，10.商户开通相关 | internal | business-field | semantic-review-required |
| 6 | `val_sum` | `int(11)` | 否 |  | 0 | 验证次数 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  |  | 状态：-1 发送失败,0未发送，1 已发送，2已验证，3已过期 | internal | business-field | semantic-review-required |
| 8 | `remark` | `varchar(20)` | 是 |  |  | 发送失败原因 | sensitive-unstructured | business-field | deny |
| 9 | `send_date` | `datetime` | 是 |  |  | 发送时间 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 | MUL |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_create`：非唯一 BTREE（create_date）
- `mobile`：非唯一 BTREE（mobile, sms_code）
- `mobile_2`：非唯一 BTREE（mobile, sms_type）

### `soft_discount_coupon`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | id 自动增长主键 | internal | relation-key | server-filter-only |
| 2 | `code` | `varchar(50)` | 否 |  |  | 密钥 | internal | business-field | semantic-review-required |
| 3 | `cycle_unit` | `int(11)` | 否 |  |  | 0日 1月 2年 | internal | business-field | semantic-review-required |
| 4 | `cycle_value` | `int(11)` | 否 |  |  | 周期值 | internal | business-field | semantic-review-required |
| 5 | `wangwang_code` | `varchar(50)` | 是 |  |  | 旺旺账号 | internal | business-field | semantic-review-required |
| 6 | `remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 7 | `soft_version` | `int(11)` | 否 |  |  | 软件版本  1试用版本 2会员基础版 3会员标准版 4预约版 5营销版 10高级版 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | 0失效、1可用、2已用 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `soft_order`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键唯一标识 | internal | relation-key | server-filter-only |
| 2 | `pay_order_no` | `varchar(100)` | 是 |  |  | 流水编号  第三方返回的订单流水号 | internal | business-field | semantic-review-required |
| 3 | `soft_price_id` | `int(11)` | 否 |  |  | 产品类目ID | internal | relation-key | server-filter-only |
| 4 | `is_soft_order_child` | `int(11)` | 否 |  | 0 | 是否包含增值项；0-不，1-包含 | internal | business-field | semantic-review-required |
| 5 | `is_added_service_order` | `tinyint(1)` | 否 |  | 0 | 是否包含增值服务订单 | internal | business-field | semantic-review-required |
| 6 | `order_tag` | `int(11)` | 否 |  | 0 | 0,试用，1充值，2赠送，3优惠码，6商城，7点餐，10订购，11续费，12添加 | internal | business-field | semantic-review-required |
| 7 | `soft_discount_coupon_id` | `int(11)` | 是 |  |  | 优惠券ID | internal | relation-key | server-filter-only |
| 8 | `version_type` | `int(11)` | 否 |  | 0 | 版本类型0 版本1增值服务 | internal | business-field | semantic-review-required |
| 9 | `soft_version` | `int(11)` | 否 |  |  | 订购版本 | internal | business-field | semantic-review-required |
| 10 | `before_soft_version` | `int(11)` | 是 |  |  | 上一个版本 | internal | business-field | semantic-review-required |
| 11 | `cycle_title` | `varchar(20)` | 否 |  |  | 周期 0一个月,1三个月,2六个月,3一年,4三年,5五年 | internal | business-field | semantic-review-required |
| 12 | `cycle_unit` | `int(11)` | 否 |  |  | 0日 1月 3年 | internal | business-field | semantic-review-required |
| 13 | `cycle_value` | `int(11)` | 否 |  |  | 周期值 | internal | business-field | semantic-review-required |
| 14 | `original_price` | `decimal(8,2)` | 是 |  |  | 原价 | internal | business-field | semantic-review-required |
| 15 | `activity_price` | `decimal(8,2)` | 是 |  |  | 活动价 | internal | business-field | semantic-review-required |
| 16 | `member_price` | `decimal(8,2)` | 是 |  |  | 会员价 | internal | business-field | semantic-review-required |
| 17 | `discount_price` | `decimal(8,2)` | 是 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 18 | `pay_price` | `decimal(8,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 19 | `service_begin_date` | `datetime` | 否 |  |  | 有效期开始时间 | internal | business-field | semantic-review-required |
| 20 | `service_end_date` | `datetime` | 是 |  |  | 服务到期时间 | internal | business-field | semantic-review-required |
| 21 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 22 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 23 | `channel_users_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 24 | `relation_id` | `int(11)` | 否 |  | 0 | 关联的id；模块的id或者套餐包id或者临时功能表id | internal | relation-key | server-filter-only |
| 25 | `type` | `int(11)` | 否 |  | 0 | 1-模块，2-套餐包 | internal | business-field | semantic-review-required |
| 26 | `sms_count` | `int(11)` | 否 |  | 0 | 短信的数量 | internal | business-field | semantic-review-required |
| 27 | `staff_count` | `int(11)` | 否 |  | 0 | 店员的数量 | internal | business-field | semantic-review-required |
| 28 | `users_count` | `int(11)` | 否 |  | 0 | 会员的数量 | internal | business-field | semantic-review-required |
| 29 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 30 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 31 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `soft_order_buy_module_record`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：软件模块购买记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `soft_order_id` | `int(11)` | 是 |  |  | 订单的id | internal | relation-key | server-filter-only |
| 4 | `function_child_id` | `int(11)` | 是 |  |  | 购买功能的id；可能是模块id也有可能是套餐包id | internal | relation-key | server-filter-only |
| 5 | `function_child_name` | `varchar(50)` | 是 |  |  | 购买功能的名称；模块名称或者套餐包名称 | internal | business-field | semantic-review-required |
| 6 | `function_package_name` | `varchar(50)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `type` | `int(11)` | 是 |  |  | 1-模块，2-套餐包 | internal | business-field | semantic-review-required |
| 8 | `start_date` | `datetime` | 是 |  |  | 开始的时间 | internal | business-field | semantic-review-required |
| 9 | `end_date` | `datetime` | 是 |  |  | 结束的时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 是 |  |  | 状态；1-正常，0-关闭 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `soft_order_child`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键唯一标识 | internal | relation-key | server-filter-only |
| 2 | `soft_order_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 3 | `pay_order_no` | `varchar(100)` | 是 |  |  | 流水编号  第三方返回的订单流水号 | internal | business-field | semantic-review-required |
| 4 | `soft_price_id` | `int(11)` | 否 |  |  | 产品类目ID | internal | relation-key | server-filter-only |
| 5 | `order_tag` | `int(11)` | 否 |  | 0 | 0,试用，1充值，2赠送，3优惠码，6商城 | internal | business-field | semantic-review-required |
| 6 | `soft_discount_coupon_id` | `int(11)` | 是 |  |  | 优惠券ID | internal | relation-key | server-filter-only |
| 7 | `soft_version` | `int(11)` | 否 |  |  | 订购版本 | internal | business-field | semantic-review-required |
| 8 | `before_soft_version` | `int(11)` | 是 |  |  | 上一个版本 | internal | business-field | semantic-review-required |
| 9 | `cycle_title` | `varchar(20)` | 否 |  |  | 周期 0一个月,1三个月,2六个月,3一年,4三年,5五年 | internal | business-field | semantic-review-required |
| 10 | `cycle_unit` | `int(11)` | 否 |  |  | 0日 1月 3年 | internal | business-field | semantic-review-required |
| 11 | `cycle_value` | `int(11)` | 否 |  |  | 周期值 | internal | business-field | semantic-review-required |
| 12 | `original_price` | `decimal(8,2)` | 是 |  |  | 原价 | internal | business-field | semantic-review-required |
| 13 | `activity_price` | `decimal(8,2)` | 是 |  |  | 活动价 | internal | business-field | semantic-review-required |
| 14 | `member_price` | `decimal(8,2)` | 是 |  |  | 会员价 | internal | business-field | semantic-review-required |
| 15 | `discount_price` | `decimal(8,2)` | 是 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 16 | `pay_price` | `decimal(8,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 17 | `service_begin_date` | `datetime` | 否 |  |  | 有效期开始时间 | internal | business-field | semantic-review-required |
| 18 | `service_end_date` | `datetime` | 是 |  |  | 服务到期时间 | internal | business-field | semantic-review-required |
| 19 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 22 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 23 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 24 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 25 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `soft_price`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键唯一标识 | internal | relation-key | server-filter-only |
| 2 | `soft_version` | `int(11)` | 否 |  |  | 软件版本 | internal | business-field | semantic-review-required |
| 3 | `cycle_title` | `varchar(20)` | 是 |  |  | 显示周期 一个月,三个月,六个月,一年,三年,五年 | internal | business-field | semantic-review-required |
| 4 | `cycle_unit` | `int(11)` | 是 |  |  | 对应单位 0日 1月 2年 | internal | business-field | semantic-review-required |
| 5 | `cycle_value` | `int(11)` | 否 |  |  | 周期值 | internal | business-field | semantic-review-required |
| 6 | `original_price` | `decimal(8,2)` | 否 |  |  | 原价 | internal | business-field | semantic-review-required |
| 7 | `activity_price` | `decimal(8,2)` | 是 |  |  | 活动价 | internal | business-field | semantic-review-required |
| 8 | `member_price` | `decimal(8,2)` | 是 |  |  | 会员价 | internal | business-field | semantic-review-required |
| 9 | `discount_price` | `decimal(8,2)` | 否 |  |  | 折扣价 | internal | business-field | semantic-review-required |
| 10 | `soft_info` | `varchar(200)` | 是 |  |  | 周期介绍 | internal | business-field | semantic-review-required |
| 11 | `give_sms_count` | `int(11)` | 否 |  |  | 赠送短信数量 | internal | business-field | semantic-review-required |
| 12 | `is_recommend` | `tinyint(1)` | 否 |  |  | 是否推荐 | internal | business-field | semantic-review-required |
| 13 | `state` | `int(11)` | 否 |  | 0 | 状态-1 删除 0禁用 1正常 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `soft_version`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：软件版本

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 非自增 | internal | relation-key | server-filter-only |
| 2 | `version_name` | `varchar(50)` | 否 |  |  | 版本名称 1试用版本 2会员基础版 3会员标准版 4预约版 5营销版 10高级版 | internal | business-field | semantic-review-required |
| 3 | `version_Tag` | `int(11)` | 否 |  |  | 版本标识 0老版本 1新版本 | internal | business-field | semantic-review-required |
| 4 | `version_info` | `varchar(100)` | 否 |  |  | 版本介绍 | internal | business-field | semantic-review-required |
| 5 | `type` | `int(11)` | 否 |  | 0 | 类型；0-软件，1-增值服务/年，2增值服务/终身 | internal | business-field | semantic-review-required |
| 6 | `info_video` | `varchar(100)` | 否 |  |  | 版本视频 | internal | business-field | semantic-review-required |
| 7 | `version_introduction` | `varchar(1500)` | 否 |  |  | 版本介绍 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | 状态0停用 1正常 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `soft_version_permission`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：软件版本权限

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键唯一标识 | internal | relation-key | server-filter-only |
| 2 | `soft_version` | `int(4)` | 否 |  |  | 软件版本 | internal | business-field | semantic-review-required |
| 3 | `is_member` | `tinyint(1)` | 否 |  |  | 会员权限 | internal | business-field | semantic-review-required |
| 4 | `is_reservation` | `tinyint(1)` | 否 |  |  | 预约权限 | internal | business-field | semantic-review-required |
| 5 | `is_marketing` | `tinyint(1)` | 否 |  |  | 营销权限 | internal | business-field | semantic-review-required |
| 6 | `is_performance` | `tinyint(1)` | 否 |  |  | 绩效权限 | internal | business-field | semantic-review-required |
| 7 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 商城权限 | internal | business-field | semantic-review-required |
| 8 | `is_distribution` | `tinyint(1)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 9 | `is_food` | `tinyint(1)` | 否 |  | 0 | 点餐 | internal | business-field | semantic-review-required |
| 10 | `max_mermber_count` | `int(11)` | 否 |  |  | 最高会员数量    0不限制 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 0停用 1正常 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 16 | `max_clerk_count` | `int(11)` | 否 |  |  | 最高店员数量 0不限制 | internal | business-field | semantic-review-required |
| 17 | `max_tablecards_count` | `int(11)` | 否 |  |  | 赠送最大台牌数量 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_cashout`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 是 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `spare_price` | `decimal(10,2)` | 是 |  |  | 剩余可提现金额 | internal | business-field | semantic-review-required |
| 5 | `cashout_total_price` | `decimal(10,2)` | 是 |  |  | 总提现金额 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `can_cashout` | `tinyint(1)` | 是 |  |  | 是否可以提现 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_cashout_log`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：员工绩效提现记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 是 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 是 |  |  | 状态：0审核中，1通过，2驳回 | internal | business-field | semantic-review-required |
| 5 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 6 | `receiver` | `varchar(255)` | 是 |  |  | 收款人姓名 | internal | business-field | semantic-review-required |
| 7 | `receive_account` | `varchar(255)` | 是 |  |  | 收款账号 | internal | business-field | semantic-review-required |
| 8 | `receive_channel` | `varchar(255)` | 是 |  |  | 收款渠道 | internal | business-field | semantic-review-required |
| 9 | `cashout_price` | `decimal(10,2)` | 是 |  |  | 提现金额 | internal | business-field | semantic-review-required |
| 10 | `spare_price` | `decimal(10,2)` | 是 |  |  | 剩余可提现金额 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `cashout_id` | `int(11)` | 是 |  |  | 提现主表ID | internal | relation-key | server-filter-only |
| 16 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_operate`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 否 |  |  | 员工（技师）ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0停用 1正常 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 6 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  |  | 修改日期 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_operate_time`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：工作时间

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 营业时间自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 否 |  |  | 员工（技师）ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `operate_id` | `bigint(20)` | 否 |  |  | 上班id | internal | relation-key | server-filter-only |
| 5 | `begin_time` | `varchar(20)` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 6 | `end_time` | `varchar(20)` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1正常 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_operate_week`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 否 |  |  | 员工（技师）ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `operate_id` | `bigint(20)` | 否 |  |  | 上班id | internal | relation-key | server-filter-only |
| 5 | `week_info` | `int(11)` | 否 |  |  | 上班日期 星期 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 0停用 1正常 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改日期 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `staff_private_lesson_set`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：私教设置

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `bigint(20)` | 否 |  |  | 员工（技师）ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `is_select_course` | `tinyint(1)` | 否 |  | 0 | 预约是否可选课目 | internal | business-field | semantic-review-required |
| 5 | `course_time` | `int(11)` | 否 |  | 0 | 私教授课时长（分钟） | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `bigint(20)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 0暂停 1正常 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `item_id` | `int(11)` | 否 |  | 0 | 项目ID | internal | relation-key | server-filter-only |
| 5 | `item_name` | `varchar(100)` | 否 |  |  | 项目名称 | internal | business-field | semantic-review-required |
| 6 | `item_price` | `decimal(10,2)` | 否 |  |  | 项目价格 | internal | business-field | semantic-review-required |
| 7 | `remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 8 | `state` | `int(11)` | 否 |  |  | 状态  0停用 1正常 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_vacation`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `begin_date` | `datetime` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 5 | `end_date` | `datetime` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 6 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 2过期 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `staff_vacation_date`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `bigint(20)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `vacation_id` | `bigint(20)` | 否 |  |  | 放假id | internal | relation-key | server-filter-only |
| 5 | `vacation_date` | `date` | 否 |  |  | 请假日期 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_vacation_seting`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：tenant_id。
表注释：店员请假设置


| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `staff_id` | `bigint(20)` | 否 |  |  | 店员id | internal | subject-or-relation-key | server-filter-only |
| 3 | `user_id` | `bigint(20)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `group_lesson_state` | `int(11)` | 否 |  |  | 团课状态 1正常 2停课 3隐藏 | internal | business-field | semantic-review-required |
| 5 | `private_lesson_state` | `int(11)` | 否 |  |  | 私教课状态 1正常 2停课 3隐藏 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `staff_vacation_time`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `bigint(20)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `vacation_id` | `bigint(20)` | 否 |  |  | 放假id | internal | relation-key | server-filter-only |
| 5 | `date_id` | `bigint(20)` | 否 |  |  | dateId | internal | relation-key | server-filter-only |
| 6 | `begin_time` | `varchar(20)` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 7 | `end_time` | `varchar(20)` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_code` | `varchar(20)` | 是 | MUL |  | 店铺编码 | internal | business-field | semantic-review-required |
| 3 | `store_type_id` | `varchar(10)` | 是 |  |  | 店铺类型ID | internal | relation-key | server-filter-only |
| 4 | `store_name` | `varchar(50)` | 是 |  |  | 店铺名称 | internal | business-field | semantic-review-required |
| 5 | `store_logo` | `varchar(100)` | 是 |  |  | 店铺logo | internal | business-field | semantic-review-required |
| 6 | `store_email` | `varchar(30)` | 是 |  |  | 店铺邮箱 | sensitive | business-field | masked-or-filter-only |
| 7 | `bg_img` | `varchar(100)` | 是 |  |  | 店铺背景图 | internal | business-field | semantic-review-required |
| 8 | `nut_gold` | `int(11)` | 否 |  | 0 | 坚果币 | internal | business-field | semantic-review-required |
| 9 | `wx_store_logo` | `varchar(200)` | 是 |  |  | 微信logo地址 | internal | business-field | semantic-review-required |
| 10 | `working_time_start` | `varchar(20)` | 是 |  |  | 工作时间开始 | internal | business-field | semantic-review-required |
| 11 | `working_time_end` | `varchar(20)` | 是 |  |  | 工作时间结束 | internal | business-field | semantic-review-required |
| 12 | `ke_count` | `int(11)` | 否 |  | 0 | 客列；0-灰色，1-红色，2-绿色 | internal | business-field | semantic-review-required |
| 13 | `store_province` | `varchar(20)` | 是 |  |  | 省id | internal | business-field | semantic-review-required |
| 14 | `store_city` | `varchar(20)` | 是 |  |  | 市id | internal | business-field | semantic-review-required |
| 15 | `store_district` | `varchar(20)` | 是 |  |  | 区id | internal | business-field | semantic-review-required |
| 16 | `address` | `varchar(100)` | 是 |  |  | 店铺地址 | sensitive | business-field | masked-or-filter-only |
| 17 | `longitude` | `varchar(15)` | 是 |  |  | 定位经度 | sensitive | business-field | masked-or-filter-only |
| 18 | `latitude` | `varchar(15)` | 是 |  |  | 定位纬度 | sensitive | business-field | masked-or-filter-only |
| 19 | `store_mobile` | `varchar(50)` | 是 |  |  | 预留电话（多个按,分隔） | sensitive | business-field | masked-or-filter-only |
| 20 | `amount` | `decimal(10,2)` | 否 |  | 0.00 | 账户余额 | internal | business-field | semantic-review-required |
| 21 | `withdrawal_amount` | `decimal(10,2)` | 否 |  | 0.00 | 提现金额 | internal | business-field | semantic-review-required |
| 22 | `yop_mer_chant_no` | `varchar(20)` | 是 |  |  | 宜宝商户编号 | internal | business-field | semantic-review-required |
| 23 | `wechat_mer_chant_no` | `varchar(20)` | 否 |  |  | 微信商户编号 | internal | business-field | semantic-review-required |
| 24 | `alipay_mer_chant_no` | `varchar(50)` | 是 |  |  | 支付宝商户编号 | internal | business-field | semantic-review-required |
| 25 | `fubei_mer_chant_no` | `varchar(20)` | 是 |  |  | 付呗商户编号 | internal | business-field | semantic-review-required |
| 26 | `fubei_store_id` | `varchar(10)` | 是 |  |  | 付呗商户店铺ID | internal | relation-key | server-filter-only |
| 27 | `yop_rate` | `decimal(6,2)` | 否 |  | 0.38 | 宜宝费率 | internal | business-field | semantic-review-required |
| 28 | `wechat_rate` | `decimal(6,2)` | 否 |  | 0.38 | 微信费率 1表示1% | internal | business-field | semantic-review-required |
| 29 | `alipay_rate` | `decimal(6,2)` | 是 |  | 0.38 | 支付宝费率 1表示1% | internal | business-field | semantic-review-required |
| 30 | `fubei_rate` | `decimal(6,2)` | 否 |  |  | 付呗费率 | internal | business-field | semantic-review-required |
| 31 | `channel_rate` | `decimal(6,2)` | 否 |  | 0.00 | 渠道的点费 | internal | business-field | semantic-review-required |
| 32 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否开通了商城 | internal | business-field | semantic-review-required |
| 33 | `is_distribution` | `tinyint(1)` | 否 |  | 0 | 是否打开分销 | internal | business-field | semantic-review-required |
| 34 | `is_food` | `tinyint(1)` | 否 |  |  | 是否打开点餐 | internal | business-field | semantic-review-required |
| 35 | `is_reservation` | `tinyint(1)` | 否 |  | 0 | 是否支持预约 | internal | business-field | semantic-review-required |
| 36 | `is_open_mer_chant_no` | `int(11)` | 否 |  | 0 | 是否开启了商户 | internal | business-field | semantic-review-required |
| 37 | `is_credit_pay` | `tinyint(1)` | 否 |  | 1 | 是否可以使用信用卡 | internal | business-field | semantic-review-required |
| 38 | `is_certification` | `tinyint(1)` | 是 |  | 0 | 是否已认证 0否1是 | internal | business-field | semantic-review-required |
| 39 | `is_experience` | `int(11)` | 否 |  | -1 | 收款体验状态 -1未开通 1开启 0体验结束 2关闭，3试用开通 | internal | business-field | semantic-review-required |
| 40 | `pay_preferential_end_date` | `datetime` | 是 |  |  | 免收点费到期时间 | internal | business-field | semantic-review-required |
| 41 | `service_end_date` | `datetime` | 是 |  |  | 服务到期时间 | internal | business-field | semantic-review-required |
| 42 | `soft_version` | `int(11)` | 是 |  | 0 | 软件版本 1试用版、2基础版、3标准版、4预约版、5营销版、10高级版 | internal | business-field | semantic-review-required |
| 43 | `soft_try_out_sum` | `int(11)` | 否 |  | 0 | 试用次数 | internal | business-field | semantic-review-required |
| 44 | `experience_pay_limit` | `int(11)` | 否 |  | 0 | 快捷收款限额 | internal | business-field | semantic-review-required |
| 45 | `is_open_integral` | `tinyint(1)` | 否 |  | 0 | 是否开启积分 | internal | business-field | semantic-review-required |
| 46 | `experience_pay_review_date` | `datetime` | 是 |  |  | 快捷收款审核时间 | internal | business-field | semantic-review-required |
| 47 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否开启了绩效功能 | internal | business-field | semantic-review-required |
| 48 | `is_use_audit` | `tinyint(1)` | 否 |  | 0 | 使用优惠券是否需要审核，0 否 1是 | internal | business-field | semantic-review-required |
| 49 | `alipay_app_auth_code` | `varchar(50)` | 是 |  |  | 支付宝店铺授权码 | internal | business-field | semantic-review-required |
| 50 | `alliance_type` | `int(11)` | 否 |  | 0 | 联盟类型：0默认联盟。1城市联盟（泰州） | internal | business-field | semantic-review-required |
| 51 | `is_complete_guide` | `tinyint(1)` | 否 |  | 0 | 是否完成新手指引 | internal | business-field | semantic-review-required |
| 52 | `is_transfer` | `tinyint(1)` | 否 |  | 0 | 是否允许转让卡余额 | internal | business-field | semantic-review-required |
| 53 | `is_transfer_card` | `tinyint(1)` | 否 |  | 0 | 是否允许转让卡 | internal | business-field | semantic-review-required |
| 54 | `is_chain_store` | `tinyint(1)` | 否 |  | 0 | 是否是连锁店 | internal | business-field | semantic-review-required |
| 55 | `is_chain_main_store` | `tinyint(1)` | 否 |  |  | 是否连锁店主店铺 | internal | business-field | semantic-review-required |
| 56 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 57 | `state` | `int(11)` | 否 |  |  | 状态，1营业，0暂停营业，-1停止运营 | internal | business-field | semantic-review-required |
| 58 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 59 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 60 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 61 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeCode`：非唯一 BTREE（store_code）
- `inx_tenantId`：非唯一 BTREE（tenant_id）

### `store_added_service_order`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `added_services_id` | `int(11)` | 否 |  |  | 增值服务ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `order_tag` | `int(11)` | 否 |  |  | 0 充值 1赠送 | internal | business-field | semantic-review-required |
| 5 | `service_type` | `int(11)` | 否 |  |  | 增值服务类型 0短信 | internal | business-field | semantic-review-required |
| 6 | `title` | `varchar(100)` | 否 |  |  | 标题 | internal | business-field | semantic-review-required |
| 7 | `item_quantity` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 8 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 9 | `end_date` | `datetime` | 是 |  |  | 到期日期 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | -1 失败 0待支付 1成功 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 商户iD | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_added_services`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `service_type` | `int(11)` | 否 |  |  | 服务类型 0短信     | internal | business-field | semantic-review-required |
| 4 | `item_quantity` | `int(11)` | 否 |  |  | 剩余数量 | internal | business-field | semantic-review-required |
| 5 | `used_quantity` | `int(11)` | 否 |  |  | 使用数量 | internal | business-field | semantic-review-required |
| 6 | `end_date` | `datetime` | 是 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 7 | `sign_name` | `varchar(30)` | 是 |  |  | 短信签名 | internal | business-field | semantic-review-required |
| 8 | `sign_state` | `int(11)` | 否 |  |  | 签名状态：-1审核失败 0审核中 1可用 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  | 1 | 1正常 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `store_id`：唯一 BTREE（store_id, service_type）

### `store_added_services01`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `service_type` | `int(11)` | 否 |  |  | 服务类型 0短信     | internal | business-field | semantic-review-required |
| 4 | `item_quantity` | `int(11)` | 否 |  |  | 剩余数量 | internal | business-field | semantic-review-required |
| 5 | `used_quantity` | `int(11)` | 否 |  |  | 使用数量 | internal | business-field | semantic-review-required |
| 6 | `end_date` | `datetime` | 是 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 7 | `sign_name` | `varchar(30)` | 是 |  |  | 短信签名 | internal | business-field | semantic-review-required |
| 8 | `sign_state` | `int(11)` | 否 |  |  | 签名状态：-1审核失败 0审核中 1可用 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  | 1 | 1正常 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `store_id`：唯一 BTREE（store_id, service_type）

### `store_advertisement_seting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 4 | `adv_id` | `int(11)` | 否 |  |  | 广告id | internal | relation-key | server-filter-only |
| 5 | `is_show` | `tinyint(1)` | 否 |  |  | 是否展示 | internal | business-field | semantic-review-required |
| 6 | `show_probability` | `datetime(4)` | 否 |  |  | 概率 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  |  | 状态：0禁用 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_agreement`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `store_agreement` | `text` | 否 |  |  | 会员协议 | internal | business-field | semantic-review-required |
| 4 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 5 | `state` | `int(11)` | 否 |  |  | 1正常 0未开卡 -1 销卡 -2商家删除 -3绑定店铺会员移除散客会员信息 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_alliance`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺联盟

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `alliance_id` | `int(11)` | 否 | MUL |  | 联盟id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `store_identity` | `int(11)` | 否 |  |  | 0创始人，1成员 | internal | business-field | semantic-review-required |
| 5 | `alliance_contribution` | `decimal(10,2)` | 否 |  |  | 联盟贡献 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | -1退出 0禁用 1启用 | internal | business-field | semantic-review-required |
| 7 | `invite_by` | `int(11)` | 否 |  |  | 邀请人 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `store_weiyi`：唯一 BTREE（alliance_id, store_id）

### `store_alliance_card`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：商家联盟卡关联

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `alliance_id` | `int(11)` | 否 |  |  | 联盟id | internal | relation-key | server-filter-only |
| 3 | `alliance_card_id` | `int(11)` | 否 |  |  | 联盟卡ID | internal | relation-key | server-filter-only |
| 4 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 6 | `card_discount` | `decimal(10,2)` | 否 |  | 1.00 | 卡折扣 | internal | business-field | semantic-review-required |
| 7 | `card_instructions` | `varchar(1000)` | 否 |  |  | 卡说明 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 0不可用 1可用 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_card`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `card_name` | `varchar(30)` | 是 |  |  | 卡名称 | internal | business-field | semantic-review-required |
| 4 | `card_type` | `int(11)` | 是 |  | 1 | 类型：0计次，1储值 | internal | business-field | semantic-review-required |
| 5 | `card_img` | `varchar(100)` | 是 |  |  | 背景图 | internal | business-field | semantic-review-required |
| 6 | `card_instructions` | `varchar(1000)` | 是 |  |  | 使用说明 | internal | business-field | semantic-review-required |
| 7 | `card_limit` | `varchar(1000)` | 是 |  |  | 会员权益 | internal | business-field | semantic-review-required |
| 8 | `is_update_card_type` | `int(11)` | 否 |  | 0 | 是否可以修改类型 0是 1否 | internal | business-field | semantic-review-required |
| 9 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 储值卡是否合并 | internal | business-field | semantic-review-required |
| 10 | `is_electronic_card` | `tinyint(1)` | 否 |  | 1 | 是否开通电子卡功能 | internal | business-field | semantic-review-required |
| 11 | `is_pay_by_card` | `tinyint(1)` | 否 |  | 1 | 是否允许顾客自主刷卡 | internal | business-field | semantic-review-required |
| 12 | `is_confirm_pass` | `tinyint(1)` | 否 |  | 0 | 是否在会员消费时输入密码 | internal | business-field | semantic-review-required |
| 13 | `is_confirm_photo` | `tinyint(1)` | 否 |  | 0 | 是否在会员消费时验证照片 | internal | business-field | semantic-review-required |
| 14 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 15 | `state` | `int(11)` | 否 |  |  | 状态 1启用 0停发 -1删除 | internal | business-field | semantic-review-required |
| 16 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 17 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 18 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 19 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_class`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `class_id` | `varchar(10)` | 否 |  |  | 分类id | internal | relation-key | server-filter-only |
| 3 | `class_name` | `varchar(20)` | 否 |  |  | 分类名称 | internal | business-field | semantic-review-required |
| 4 | `root_id` | `varchar(20)` | 否 |  | 0 | 父类名称 | internal | relation-key | server-filter-only |
| 5 | `class_level` | `int(11)` | 否 |  | 2 | 分类级别 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  | 1 | 状态 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_classes`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `class_title` | `varchar(50)` | 否 |  |  | 班级名字 | internal | business-field | semantic-review-required |
| 4 | `class_note` | `text` | 是 |  |  | 班级简介 | sensitive-unstructured | business-field | deny |
| 5 | `class_image` | `varchar(100)` | 是 |  |  | 背景图 | internal | business-field | semantic-review-required |
| 6 | `class_image_id` | `bigint(20)` | 否 |  | 0 | 班级图片id | internal | relation-key | server-filter-only |
| 7 | `class_color` | `varchar(10)` | 是 |  |  | 颜色 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `order_by` | `int(11)` | 否 |  | 0 | 排序 倒序 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_classes_course`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `class_id` | `int(11)` | 否 |  |  | 分组id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `course_id` | `int(11)` | 否 |  |  | 会员id | internal | relation-key | server-filter-only |
| 5 | `begin_date` | `date` | 否 |  |  | 开始日期 | internal | business-field | semantic-review-required |
| 6 | `end_date` | `date` | 否 |  |  | 结束日期 | internal | business-field | semantic-review-required |
| 7 | `week_info` | `varchar(30)` | 否 |  |  | 周几， 以逗号分隔, | internal | business-field | semantic-review-required |
| 8 | `begin_time` | `varchar(10)` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 9 | `end_time` | `varchar(10)` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 10 | `is_stop` | `tinyint(1)` | 否 |  | 0 | 是否停课 | internal | business-field | semantic-review-required |
| 11 | `stop_begin_date` | `datetime` | 是 |  |  | 停课开始时间 | internal | business-field | semantic-review-required |
| 12 | `stop_end_date` | `datetime` | 是 |  |  | 停课结束时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0停课 1启用 | internal | business-field | semantic-review-required |
| 15 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 16 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 17 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 18 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_classes_user`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `class_id` | `int(11)` | 否 |  |  | 分组id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 会员卡id | internal | subject-or-relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0退班 1启用 | internal | business-field | semantic-review-required |
| 8 | `last_date` | `datetime` | 是 |  |  | 最后上课时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_controls`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：商家自定义控件

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `cid` | `int(11)` | 否 |  |  | 控件id | internal | business-field | semantic-review-required |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 4 | `control_name` | `varchar(30)` | 否 |  |  | 控件名称 | internal | business-field | semantic-review-required |
| 5 | `control_instructions` | `varchar(20)` | 否 |  |  | 控件说明 | internal | business-field | semantic-review-required |
| 6 | `control_type` | `varchar(10)` | 否 |  |  | 控件类型 input,radio,select.... | internal | business-field | semantic-review-required |
| 7 | `is_must` | `int(11)` | 否 |  |  | 是否必填 1是 0否 | internal | business-field | semantic-review-required |
| 8 | `is_show` | `tinyint(1)` | 否 |  | 0 | 是否对C端客户显示 | internal | business-field | semantic-review-required |
| 9 | `is_client_data` | `tinyint(1)` | 否 |  | 0 | 是否只由顾客添加 | internal | business-field | semantic-review-required |
| 10 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 12 | `state` | `int(11)` | 否 |  |  | 状态1启用0停用 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_store_id`：唯一 BTREE（store_id, cid）
- `inx_tenant_id`：非唯一 BTREE（tenant_id）

### `store_coupon_center`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `coupon_center_type` | `int(11)` | 否 |  |  | 2续费送,3生日送,4满送，5群发,6营销活动，7节日祝福8放假 9老客户激活，10散客营销， 21 续费营销（新），22 联盟券，23，购卡送券，24 支付宝商家券   | internal | business-field | semantic-review-required |
| 4 | `is_by_user_level` | `tinyint(1)` | 否 |  | 0 | 是否按会员等级 送券 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 0已停用 1正常 | internal | business-field | semantic-review-required |
| 6 | `state_reason` | `int(11)` | 否 |  |  | 0默认 1商家停止 2已达到发行数量上限,3优惠券截止日期已过 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id, coupon_center_type）

### `store_course`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：店铺课程表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `course_type` | `int(11)` | 否 |  | 0 | 授课类型；0-团课，1-私教 2班课 | internal | business-field | semantic-review-required |
| 4 | `course_name` | `varchar(255)` | 否 |  |  | 课程名称 | internal | business-field | semantic-review-required |
| 5 | `course_describe` | `varchar(500)` | 是 |  |  | 课程描述 | internal | business-field | semantic-review-required |
| 6 | `course_image_id` | `bigint(20)` | 否 |  | 0 | 课程图片id | internal | relation-key | server-filter-only |
| 7 | `item_id` | `int(11)` | 否 |  | 0 | 项目id | internal | relation-key | server-filter-only |
| 8 | `course_time` | `int(11)` | 否 |  | 0 | 授课时长（分钟） | internal | business-field | semantic-review-required |
| 9 | `course_people_count` | `int(11)` | 否 |  | 0 | 授课人数 | internal | business-field | semantic-review-required |
| 10 | `min_people` | `int(11)` | 否 |  | 0 | 最小授课人数 | internal | business-field | semantic-review-required |
| 11 | `course_remark` | `varchar(500)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 12 | `course_star` | `int(11)` | 否 |  | 0 | 难度星级1-10 | internal | business-field | semantic-review-required |
| 13 | `course_color` | `varchar(10)` | 是 |  |  | 颜色 | internal | business-field | semantic-review-required |
| 14 | `course_place_id` | `bigint(20)` | 否 |  | 0 | 教室id | internal | relation-key | server-filter-only |
| 15 | `is_recommend` | `tinyint(1)` | 否 |  | 1 | 是否推荐，用作首页展示 | internal | business-field | semantic-review-required |
| 16 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 17 | `order_by` | `int(11)` | 否 |  |  | 排序 倒序 | internal | business-field | semantic-review-required |
| 18 | `state` | `int(11)` | 否 |  | 1 | 状态；0-未开放，1-已开放，-1已删除 | internal | business-field | semantic-review-required |
| 19 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 20 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 21 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 22 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `store_course_card_item`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `relation_id` | `bigint(20)` | 否 |  |  | 关联id | internal | relation-key | server-filter-only |
| 3 | `staff_id` | `bigint(20)` | 否 |  | 0 | 教练id(私教) | internal | subject-or-relation-key | server-filter-only |
| 4 | `course_id` | `bigint(20)` | 否 |  |  | 课程id | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `bigint(20)` | 否 |  |  | 卡id(储值卡) | restricted | relation-key | deny |
| 6 | `item_id` | `bigint(20)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 7 | `item_value` | `int(11)` | 否 |  |  | 项目所扣次数 | internal | business-field | semantic-review-required |
| 8 | `store_id` | `bigint(20)` | 否 | MUL | 0 | 店铺id | internal | store-scope | server-filter-only |
| 9 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `bigint(20)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `bigint(20)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `store_course_card_relation`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `staff_id` | `bigint(20)` | 否 |  | 0 | 教练id(私教) | internal | subject-or-relation-key | server-filter-only |
| 3 | `course_id` | `bigint(20)` | 否 |  |  | 课程id | internal | relation-key | server-filter-only |
| 4 | `prepaid_card_id` | `bigint(20)` | 否 |  |  | 卡id(储值卡) | restricted | relation-key | deny |
| 5 | `card_type` | `int(11)` | 否 |  |  | 类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 6 | `validity_period` | `int(11)` | 否 |  |  | （时限卡）扣减有效期 天 0不扣 | internal | business-field | semantic-review-required |
| 7 | `card_value` | `decimal(10,2)` | 否 |  |  | 扣减卡余额 | internal | business-field | semantic-review-required |
| 8 | `store_id` | `bigint(20)` | 否 | MUL | 0 | 店铺id | internal | store-scope | server-filter-only |
| 9 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `bigint(20)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `bigint(20)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `store_course_name`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `course_id` | `bigint(20)` | 否 |  |  | 课目id | internal | relation-key | server-filter-only |
| 4 | `course_name` | `varchar(50)` | 否 |  |  | 课目标题 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 1启用  | internal | business-field | semantic-review-required |
| 7 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_course_price`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  | 0 | 店铺id | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `bigint(20)` | 否 |  | 0 | 教练id(私教) | internal | subject-or-relation-key | server-filter-only |
| 4 | `course_id` | `bigint(20)` | 否 |  |  | 课程id | internal | relation-key | server-filter-only |
| 5 | `lessons_id` | `bigint(20)` | 否 |  |  | 课id | internal | relation-key | server-filter-only |
| 6 | `course_type` | `int(11)` | 否 |  |  | 课目类型 0团课 1私教 | internal | business-field | semantic-review-required |
| 7 | `is_card_discount` | `tinyint(1)` | 否 |  |  | 是否参与卡折扣 | internal | business-field | semantic-review-required |
| 8 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 9 | `vip_price` | `decimal(10,2)` | 否 |  |  | 会员价 | internal | business-field | semantic-review-required |
| 10 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣价 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 12 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `bigint(20)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `bigint(20)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_course_staff`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：课程授课人员关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL | 0 | 店铺id | internal | store-scope | server-filter-only |
| 3 | `course_id` | `int(11)` | 否 |  | 0 | 课程id | internal | relation-key | server-filter-only |
| 4 | `course_staff_id` | `int(11)` | 否 |  | 0 | 授课人员id | internal | relation-key | server-filter-only |
| 5 | `course_people_count` | `int(11)` | 否 |  | 0 | 最大授课人数 0跟随系统 | internal | business-field | semantic-review-required |
| 6 | `course_time` | `int(11)` | 否 |  | 0 | 授课时长（分钟） | internal | business-field | semantic-review-required |
| 7 | `course_describe` | `varchar(500)` | 是 |  |  | 课程描述 | internal | business-field | semantic-review-required |
| 8 | `order_by` | `int(11)` | 否 |  |  | 排序 倒序 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `store_course_tag_relation`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  | 0 | 店铺id | internal | store-scope | server-filter-only |
| 3 | `course_id` | `bigint(20)` | 否 |  | 0 | 课程id | internal | relation-key | server-filter-only |
| 4 | `tag_id` | `bigint(20)` | 否 |  | 0 | 授课人员id | internal | relation-key | server-filter-only |
| 5 | `tag_type` | `int(11)` | 否 |  |  | 标签类型： 3课程 5课程分类 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_course_time`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：课程授课时间表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `course_id` | `int(11)` | 否 |  | 0 | 课程id | internal | relation-key | server-filter-only |
| 4 | `week_info` | `varchar(30)` | 否 |  |  | 周几， 以逗号分隔, | internal | business-field | semantic-review-required |
| 5 | `begin_time` | `varchar(10)` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 6 | `end_time` | `varchar(10)` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 7 | `time_interval` | `int(11)` | 否 |  | 0 | 预约时间间隔 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  | 1 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_course_time_detailed`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：课程时间明细表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `course_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `store_course_time_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 5 | `time` | `varchar(20)` | 否 |  |  | 时间 | internal | business-field | semantic-review-required |
| 6 | `time_interval` | `int(11)` | 否 |  | 0 | 预约时间间隔 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  | 1 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 11 | `update_time` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_course_time_detailed_week`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：课程时间明细关联周期表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `course_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 4 | `store_course_time_detailed_id` | `int(11)` | 否 |  | 0 |  | internal | relation-key | server-filter-only |
| 5 | `week_info` | `int(11)` | 否 |  | 0 | 周；1-7 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  | 0 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP |  | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_custom_seting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺自定制信息表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | UNI |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `assistant_call` | `varchar(20)` | 否 |  |  | 店员称呼，预约使用 | internal | business-field | semantic-review-required |
| 4 | `place_call` | `varchar(20)` | 否 |  |  | 教室称呼 | internal | business-field | semantic-review-required |
| 5 | `classes_lessons_title` | `varchar(20)` | 否 |  |  | 班课标题 默认空 | internal | business-field | semantic-review-required |
| 6 | `private_lessons_title` | `varchar(20)` | 否 |  |  | 私教标题 默认空 | internal | business-field | semantic-review-required |
| 7 | `background_image` | `varchar(100)` | 否 |  |  | B端首页背景图 | internal | business-field | semantic-review-required |
| 8 | `currency_name` | `varchar(10)` | 否 |  |  | 货币名称 元 | internal | business-field | semantic-review-required |
| 9 | `currency_unit` | `varchar(10)` | 否 |  |  | 货币符号 ￥$ | internal | business-field | semantic-review-required |
| 10 | `time_zone` | `double` | 否 |  | 0 | 时区 | internal | business-field | semantic-review-required |
| 11 | `time_format` | `varchar(30)` | 是 |  |  | 时间格式 | internal | business-field | semantic-review-required |
| 12 | `is_cloud_store` | `tinyint(1)` | 否 |  | 0 | 是否云店模式 | internal | business-field | semantic-review-required |
| 13 | `register_method` | `int(11)` | 否 |  | 2 | 1.先填资料 2.后填资料 3.注册既会员 | internal | business-field | semantic-review-required |
| 14 | `is_user_img_or_nick` | `tinyint(1)` | 否 |  | 1 | 是否需要顾客头像与昵称 | internal | business-field | semantic-review-required |
| 15 | `is_fit_commission` | `tinyint(1)` | 否 |  | 0 | 是否开启散客佣金模式 | internal | business-field | semantic-review-required |
| 16 | `is_build_qr_code` | `tinyint(1)` | 否 |  | 0 | 是否生成二维码 | internal | business-field | semantic-review-required |
| 17 | `is_no_card_vip` | `tinyint(1)` | 否 |  | 1 | 是否开启无卡会员 | internal | business-field | semantic-review-required |
| 18 | `is_refund_protection` | `tinyint(1)` | 否 |  | 0 | 是否开启退卡保护 | internal | business-field | semantic-review-required |
| 19 | `is_birthday_user_count` | `tinyint(1)` | 否 |  | 0 | 是否显示生日会员数量 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 22 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 24 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_store`：唯一 BTREE（store_id）

### `store_customer_mobile`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺顾客表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `customer_name` | `varchar(20)` | 否 |  |  | 顾客姓名 | internal | business-field | semantic-review-required |
| 4 | `customer_mobile` | `varchar(20)` | 否 |  |  | 顾客手机号 | sensitive | business-field | masked-or-filter-only |
| 5 | `name_group` | `varchar(5)` | 否 |  |  | 拼音首字母分组 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 -1删除  1正常 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 8 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_experience_pay`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺快捷收款信息

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `free_quota` | `decimal(10,2)` | 否 |  |  | 免费额度 | internal | business-field | semantic-review-required |
| 4 | `rate` | `decimal(4,2)` | 否 |  |  | 超出额度后费率 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  | 1 | -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_extend`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `poster_qr_code` | `varchar(100)` | 是 |  |  | 店铺海报二维码 | internal | business-field | semantic-review-required |
| 4 | `remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 5 | `flag` | `int(11)` | 是 |  |  | 0 无标记 1标记1，2标记2，3标记3 具体代表啥还没定 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 是 |  |  | 默认值0 排序倒序 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_store_extend_storeid`：非唯一 BTREE（store_id）

### `store_fb_config`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 门店ID | internal | store-scope | server-filter-only |
| 3 | `merchant_id` | `int(11)` | 否 |  |  | 付呗商户号 | internal | relation-key | server-filter-only |
| 4 | `merchant_code` | `varchar(60)` | 否 |  |  | 商户账号，外部系统的唯一商户编号（可以用作登录付呗商户后台） | internal | business-field | semantic-review-required |
| 5 | `merchant_status` | `int(11)` | 是 |  |  | 商户认证状态：0 未认证、1 认证中、2 认证成功、3 认证失败 | internal | business-field | semantic-review-required |
| 6 | `app_id` | `varchar(0)` | 是 |  |  | 商户AppId | internal | relation-key | server-filter-only |
| 7 | `app_secret` | `varchar(255)` | 是 |  |  | 商户AppSecret | restricted | business-field | deny |
| 8 | `wechat_mer_no` | `varchar(30)` | 是 |  |  | 微信商户号 | internal | business-field | semantic-review-required |
| 9 | `wechat_mer_is_certify` | `tinyint(1)` | 否 |  |  | 微信商户号是否认证 | internal | business-field | semantic-review-required |
| 10 | `alipay_mer_no` | `varchar(30)` | 是 |  |  | 支付宝商户号 | internal | business-field | semantic-review-required |
| 11 | `alipay_mer_is_certify` | `tinyint(1)` | 否 |  |  | 支付宝商户号是否认证 | internal | business-field | semantic-review-required |
| 12 | `createtime` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 13 | `updatetime` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `type` | `int(11)` | 是 |  |  | 门店类型：1门店主账号、2门店分账号 | internal | business-field | semantic-review-required |
| 15 | `fb_status` | `int(11)` | 是 |  |  | 付呗审核门店状态1 待审核、2 审核通过、3 审核驳回 | internal | business-field | semantic-review-required |
| 16 | `status` | `int(11)` | 是 |  |  | 系统门店状态：1、正常 2停用 | internal | business-field | semantic-review-required |
| 17 | `fb_store_id` | `int(11)` | 是 |  |  | 对应的付呗门店的ID | internal | relation-key | server-filter-only |
| 18 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_group`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：分组

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `tag_group_id` | `int(11)` | 否 |  | 1 | 标签总id | internal | relation-key | server-filter-only |
| 4 | `group_icon` | `varchar(100)` | 否 |  |  | 分组icon | internal | business-field | semantic-review-required |
| 5 | `group_name` | `varchar(20)` | 否 |  |  | 分组名称 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  |  | 排序 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0未启用 1正常 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）
- `idx_tenantId`：非唯一 BTREE（tenant_id）

### `store_growth_activation`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：YueKe 激活轨道跳过状态

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `store_id` | `bigint(20)` | 否 | PRI |  | 门店主键；每个门店最多一条引导状态 | internal | store-scope | server-filter-only |
| 2 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户主键；用于保持租户数据边界 | internal | tenant-scope | server-filter-only |
| 3 | `private_skipped` | `tinyint(1)` | 否 |  | 0 | 是否由店主跳过私教路径：0 否，1 是 | internal | business-field | semantic-review-required |
| 4 | `group_skipped` | `tinyint(1)` | 否 |  | 0 | 是否由店主跳过团课路径：0 否，1 是 | internal | business-field | semantic-review-required |
| 5 | `class_skipped` | `tinyint(1)` | 否 |  | 0 | 是否由店主跳过班课路径：0 否，1 是 | internal | business-field | semantic-review-required |
| 6 | `update_by` | `bigint(20)` | 否 |  |  | 最后修改引导状态的用户主键 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  |  | 最后修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（store_id）

### `store_growth_event`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：tenant_id, store_id。
表注释：YueKe 商家转化事件

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 事件主键 | internal | relation-key | server-filter-only |
| 2 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户主键；保留 0 兼容历史门店数据 | internal | tenant-scope | server-filter-only |
| 3 | `store_id` | `bigint(20)` | 否 | MUL |  | 事件所属门店主键 | internal | store-scope | server-filter-only |
| 4 | `uid` | `bigint(20)` | 否 |  |  | 触发事件的登录用户主键 | internal | subject-or-relation-key | server-filter-only |
| 5 | `event_code` | `varchar(64)` | 否 | MUL |  | 稳定事件编码，例如 pc_first_login、pricing_view | internal | business-field | semantic-review-required |
| 6 | `source` | `varchar(32)` | 否 |  | yueke_pc | 事件来源；当前固定为 YueKe PC | internal | business-field | semantic-review-required |
| 7 | `properties_json` | `varchar(2000)` | 否 |  |  | 事件扩展属性 JSON；不得存放敏感明文 | internal | business-field | semantic-review-required |
| 8 | `dedupe_key` | `varchar(160)` | 是 | UNI |  | 可选去重键；为空时允许同类事件重复记录 | internal | business-field | semantic-review-required |
| 9 | `occurred_at` | `datetime` | 否 |  |  | 业务事件实际发生时间 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 数据库记录创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_store_growth_event_code_time`：非唯一 BTREE（event_code, occurred_at）
- `idx_store_growth_event_store_time`：非唯一 BTREE（store_id, occurred_at）
- `uk_store_growth_event_dedupe`：唯一 BTREE（dedupe_key）

### `store_index_config`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `module` | `varchar(255)` | 是 |  |  | 模块 | internal | business-field | semantic-review-required |
| 4 | `sort` | `int(11)` | 是 |  |  | 排序 | internal | business-field | semantic-review-required |
| 5 | `data` | `varchar(700)` | 是 |  |  | 默认数据 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 是 |  |  | 状态：0删除 1 启用 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_index_modules`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `Id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `is_activity` | `tinyint(1)` | 否 |  | 0 | 是否显示活动模块 | internal | business-field | semantic-review-required |
| 4 | `is_address` | `tinyint(1)` | 否 |  | 1 | 是否显示地址 | sensitive | business-field | masked-or-filter-only |
| 5 | `is_banner` | `tinyint(1)` | 否 |  | 1 | 是否显示Banner | internal | business-field | semantic-review-required |
| 6 | `is_buy_card_give_coupon` | `tinyint(1)` | 否 |  | 0 | 是否显示购卡送券模块 | internal | business-field | semantic-review-required |
| 7 | `is_coupon_link` | `tinyint(1)` | 否 |  | 0 | 是否显示外券 | internal | business-field | semantic-review-required |
| 8 | `is_advertise` | `tinyint(1)` | 否 |  | 0 | 是否展示广告位 | internal | business-field | semantic-review-required |
| 9 | `is_customer_service` | `tinyint(1)` | 否 |  | 0 | 是否展示客服 | internal | business-field | semantic-review-required |
| 10 | `enterprise_no` | `varchar(50)` | 是 |  |  | 企业号（客服跳转企业微信） | internal | business-field | semantic-review-required |
| 11 | `customer_link` | `varchar(255)` | 是 |  |  | 客服链接（跳转企业微信） | internal | business-field | semantic-review-required |
| 12 | `is_custom_setting` | `tinyint(1)` | 否 |  | 0 | 是否启用客户自定义设置（充值文字，背景颜色，是否展示充值） | internal | business-field | semantic-review-required |
| 13 | `is_distribution` | `tinyint(1)` | 否 |  | 0 | 是否展示分销模块 | internal | business-field | semantic-review-required |
| 14 | `is_introduction` | `tinyint(1)` | 否 |  | 1 | 是否展示介绍图 | internal | business-field | semantic-review-required |
| 15 | `is_food_order_title` | `tinyint(1)` | 否 |  | 0 | 是否使用自定义点餐标题 | internal | business-field | semantic-review-required |
| 16 | `is_shop_title` | `tinyint(1)` | 否 |  |  | 是否自定义商城标题 | internal | business-field | semantic-review-required |
| 17 | `introduction_img` | `varchar(500)` | 是 |  |  | 首页介绍图 | internal | business-field | semantic-review-required |
| 18 | `is_recommend_card` | `tinyint(1)` | 否 |  | 1 | 是否展示推荐购卡 | internal | business-field | semantic-review-required |
| 19 | `is_recommend_food` | `tinyint(1)` | 否 |  | 0 | 是否展示推荐餐品模块 | internal | business-field | semantic-review-required |
| 20 | `is_recommend_product` | `tinyint(1)` | 否 |  | 0 | 是否展示推荐商品模块 | internal | business-field | semantic-review-required |
| 21 | `is_reservation` | `tinyint(1)` | 否 |  | 0 | 是否展示预约模块 | internal | business-field | semantic-review-required |
| 22 | `is_user_center` | `tinyint(1)` | 否 |  | 1 | 是否展示用户中心 | internal | business-field | semantic-review-required |
| 23 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 24 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 25 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 26 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 27 | `state` | `int(11)` | 否 |  | 1 |  | internal | business-field | semantic-review-required |
| 28 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（Id）

### `store_integral_set`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：积分设置

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `money_to_integral_proportion` | `decimal(10,2)` | 否 |  |  | 获取比例 积分 | internal | business-field | semantic-review-required |
| 4 | `integral_to_money_proportion` | `int(11)` | 否 |  |  | 抵扣每N积分比1元 | internal | business-field | semantic-review-required |
| 5 | `expired_set` | `int(11)` | 否 |  |  | 过期设置  0不过期 1按月，2按季度，3按半年，4按年 | internal | business-field | semantic-review-required |
| 6 | `use_rule` | `int(11)` | 否 |  |  | 使用规则 0不能抵扣付款，1可以抵扣付款 | internal | business-field | semantic-review-required |
| 7 | `use_min_integral` | `int(11)` | 否 |  |  | 最少积分使用 | internal | business-field | semantic-review-required |
| 8 | `use_max_proportion` | `decimal(10,2)` | 否 |  |  | 单次使用积分付款的最大比例 | internal | business-field | semantic-review-required |
| 9 | `use_max_money` | `decimal(10,2)` | 否 |  |  | 单次使用积分最大抵扣金额   0不限制 | internal | business-field | semantic-review-required |
| 10 | `integral_info` | `varchar(200)` | 是 |  |  | 积分说明 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 15 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 16 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 17 | `is_use_shop` | `tinyint(1)` | 否 |  |  | 付款是否可用 | internal | business-field | semantic-review-required |
| 18 | `is_use_pay` | `tinyint(1)` | 否 |  |  | 支付是否可用 | internal | business-field | semantic-review-required |
| 19 | `is_use_card` | `tinyint(1)` | 否 |  |  | 刷卡是否可用 | internal | business-field | semantic-review-required |
| 20 | `is_use_food` | `tinyint(1)` | 否 |  |  | 点餐是否可用 | internal | business-field | semantic-review-required |
| 21 | `is_use_reservation` | `tinyint(1)` | 否 |  |  | 预约是否可用 | internal | business-field | semantic-review-required |
| 22 | `is_consumption_get` | `tinyint(1)` | 否 |  | 1 | 是否是消费得积分 | internal | business-field | semantic-review-required |
| 23 | `is_consumption_get_pay` | `tinyint(1)` | 否 |  | 1 | 付款是否得积分 | internal | business-field | semantic-review-required |
| 24 | `is_consumption_get_card` | `tinyint(1)` | 否 |  | 1 | 刷卡是否得积分 | internal | business-field | semantic-review-required |
| 25 | `money_to_integral_money` | `int(11)` | 是 |  |  | 获取比例 元 | internal | business-field | semantic-review-required |
| 26 | `is_lesson_integral` | `tinyint(1)` | 否 |  | 0 | 上课得积分总开关 0关闭 1开启 | internal | business-field | semantic-review-required |
| 27 | `is_group_lesson_integral` | `tinyint(1)` | 否 |  | 0 | 团课上课是否得积分 0否 1是 | internal | business-field | semantic-review-required |
| 28 | `group_lesson_integral` | `int(11)` | 否 |  | 0 | 团课每节完课获得积分 | internal | business-field | semantic-review-required |
| 29 | `is_private_lesson_integral` | `tinyint(1)` | 否 |  | 0 | 私教上课是否得积分 0否 1是 | internal | business-field | semantic-review-required |
| 30 | `private_lesson_integral` | `int(11)` | 否 |  | 0 | 私教每节完课获得积分 | internal | business-field | semantic-review-required |
| 31 | `is_class_lesson_integral` | `tinyint(1)` | 否 |  | 0 | 班课上课是否得积分 0否 1是 | internal | business-field | semantic-review-required |
| 32 | `class_lesson_integral` | `int(11)` | 否 |  | 0 | 班课每节完课获得积分 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_lessons`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：课

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `course_id` | `int(11)` | 否 | MUL |  | 课程ID | internal | relation-key | server-filter-only |
| 4 | `course_type` | `int(11)` | 否 |  |  | 课程类型：0团课，1私教 2班课 | internal | business-field | semantic-review-required |
| 5 | `class_id` | `bigint(20)` | 否 |  | 0 | 班级id | internal | relation-key | server-filter-only |
| 6 | `course_name` | `varchar(255)` | 是 |  |  | 课程名称 | internal | business-field | semantic-review-required |
| 7 | `course_image_id` | `bigint(20)` | 否 |  | 0 | 课程图片id | internal | relation-key | server-filter-only |
| 8 | `course_desc` | `varchar(500)` | 是 |  |  | 课程描述 | internal | business-field | semantic-review-required |
| 9 | `teach_count` | `int(11)` | 否 |  |  | 授课人数 | internal | business-field | semantic-review-required |
| 10 | `min_people` | `int(11)` | 否 |  | 0 | 最小授课人数 | internal | business-field | semantic-review-required |
| 11 | `teach_min` | `int(11)` | 否 |  |  | 授课时长（分钟） | internal | business-field | semantic-review-required |
| 12 | `begin_time` | `datetime` | 是 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 13 | `end_time` | `datetime` | 是 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 14 | `course_star` | `int(11)` | 否 |  | 0 | 难度星级1-10 | internal | business-field | semantic-review-required |
| 15 | `course_color` | `varchar(10)` | 是 |  |  | 颜色 | internal | business-field | semantic-review-required |
| 16 | `course_place_id` | `bigint(20)` | 否 |  | 0 | 教室id | internal | relation-key | server-filter-only |
| 17 | `is_advance_notice` | `tinyint(1)` | 否 |  | 0 | 是否已经发送通知 | internal | business-field | semantic-review-required |
| 18 | `is_auto_cancel` | `tinyint(1)` | 否 |  | 1 | 是否自动触发取消 | internal | business-field | semantic-review-required |
| 19 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 20 | `sign_date` | `datetime` | 是 | MUL |  | 签到时间 | internal | business-field | semantic-review-required |
| 21 | `cancel_date` | `datetime` | 是 |  |  | 取消时间 | internal | business-field | semantic-review-required |
| 22 | `is_make` | `tinyint(1)` | 否 |  | 0 | 是否补课 | internal | business-field | semantic-review-required |
| 23 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 24 | `state` | `int(11)` | 否 |  |  | 状态：0未开课，1完课，2取消 3人数不足 5上课中 10停课 | internal | business-field | semantic-review-required |
| 25 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 26 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 27 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 28 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_courseId`：非唯一 BTREE（course_id）
- `idx_signDate`：非唯一 BTREE（sign_date）
- `idx_storeId`：非唯一 BTREE（store_id）

### `store_lessons_download_set`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  | 0 | 店铺id | internal | store-scope | server-filter-only |
| 3 | `title` | `varchar(50)` | 否 |  |  | 标题 | internal | business-field | semantic-review-required |
| 4 | `sub_title` | `varchar(100)` | 否 |  |  | 副标题 | internal | business-field | semantic-review-required |
| 5 | `sub_title_brand` | `varchar(100)` | 否 |  |  | 品牌副标题 | internal | business-field | semantic-review-required |
| 6 | `head_image` | `varchar(100)` | 是 |  |  | 头图 | internal | business-field | semantic-review-required |
| 7 | `caveat_title` | `varchar(30)` | 是 |  |  | 注意事项标题 | internal | business-field | semantic-review-required |
| 8 | `caveat` | `text` | 是 |  |  | 注意事项 | internal | business-field | semantic-review-required |
| 9 | `lessons_style` | `int(11)` | 否 |  |  | 课程样式 0背景图 1背景色 | internal | business-field | semantic-review-required |
| 10 | `is_show_date` | `tinyint(1)` | 否 |  |  | 是否显示日期 | internal | business-field | semantic-review-required |
| 11 | `is_course_class` | `tinyint(1)` | 否 |  |  | 是否显示分类 | internal | business-field | semantic-review-required |
| 12 | `is_show_staff` | `tinyint(1)` | 否 |  |  | 是否显示教练 | internal | business-field | semantic-review-required |
| 13 | `is_show_course_name` | `tinyint(1)` | 否 |  |  | 是否显示课程名称 | internal | business-field | semantic-review-required |
| 14 | `is_show_staff_name` | `tinyint(1)` | 否 |  |  | 是否显示教练名称 | internal | business-field | semantic-review-required |
| 15 | `is_show_time` | `tinyint(1)` | 否 |  |  | 是否显示时间 | internal | business-field | semantic-review-required |
| 16 | `is_show_tag` | `tinyint(1)` | 否 |  |  | 是否显示标签 | internal | business-field | semantic-review-required |
| 17 | `is_show_star` | `tinyint(1)` | 否 |  |  | 是否显示星级 | internal | business-field | semantic-review-required |
| 18 | `is_show_place_Name` | `tinyint(1)` | 否 |  |  | 是否显示教师名字 | internal | business-field | semantic-review-required |
| 19 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 20 | `state` | `int(11)` | 否 |  |  | 状态1启用 | internal | business-field | semantic-review-required |
| 21 | `create_by` | `bigint(20)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 24 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_lessons_staff`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `lessons_id` | `int(11)` | 否 | MUL |  | 课 ID | internal | relation-key | server-filter-only |
| 3 | `staff_id` | `int(11)` | 否 |  |  | 员工 ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `order_by` | `int(11)` | 否 |  | 0 | 排序 倒序 | internal | business-field | semantic-review-required |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态： -1 无效，0正常 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_lessonsId`：非唯一 BTREE（lessons_id）

### `store_material`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：tenant_id, store_id。
表注释：店铺素材表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户ID | internal | tenant-scope | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `category_id` | `int(11)` | 否 |  | 0 | 分类ID | internal | relation-key | server-filter-only |
| 5 | `material_name` | `varchar(100)` | 否 |  |  | 素材名称 | internal | business-field | semantic-review-required |
| 6 | `material_type` | `tinyint(4)` | 否 |  |  | 素材类型：1图片 2视频 | internal | business-field | semantic-review-required |
| 7 | `file_path` | `varchar(1000)` | 否 |  |  | 素材路径；图片/视频为文件地址，视频号为链接地址 | internal | business-field | semantic-review-required |
| 8 | `file_name` | `varchar(255)` | 否 |  |  | 原始文件名 | internal | business-field | semantic-review-required |
| 9 | `file_ext` | `varchar(20)` | 否 |  |  | 文件扩展名 | internal | business-field | semantic-review-required |
| 10 | `file_size` | `bigint(20)` | 否 |  | 0 | 文件大小，单位Byte | internal | business-field | semantic-review-required |
| 11 | `mime_type` | `varchar(100)` | 否 |  |  | MIME类型 | internal | business-field | semantic-review-required |
| 12 | `video_cover` | `varchar(500)` | 否 |  |  | 视频封面地址 | internal | business-field | semantic-review-required |
| 13 | `video_no` | `varchar(100)` | 否 |  |  | 视频号 | internal | business-field | semantic-review-required |
| 14 | `video_time_length` | `int(11)` | 否 |  | 0 | 视频时长，单位秒 | internal | business-field | semantic-review-required |
| 15 | `width` | `int(11)` | 否 |  | 0 | 宽度 | internal | business-field | semantic-review-required |
| 16 | `height` | `int(11)` | 否 |  | 0 | 高度 | internal | business-field | semantic-review-required |
| 17 | `remark` | `varchar(500)` | 否 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 18 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 19 | `state` | `tinyint(4)` | 否 |  | 1 | 状态：1启用 0禁用 -1删除 | internal | business-field | semantic-review-required |
| 20 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 21 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 22 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_store_category_state`：非唯一 BTREE（store_id, category_id, state）

### `store_material_category`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：tenant_id, store_id。
表注释：店铺素材分类表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户ID | internal | tenant-scope | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `category_name` | `varchar(50)` | 否 |  |  | 分类名称 | internal | business-field | semantic-review-required |
| 5 | `category_type` | `tinyint(4)` | 否 |  | 0 | 分类类型：0通用 1图片 2视频 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `state` | `tinyint(4)` | 否 |  | 1 | 状态：1启用 0禁用 -1删除 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_store_state_order`：非唯一 BTREE（store_id, state, order_by）

### `store_material_course_relation`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：tenant_id, store_id。
表注释：店铺素材课目关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户ID | internal | tenant-scope | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `material_id` | `int(11)` | 否 |  |  | 素材ID，对应 store_material.id | internal | relation-key | server-filter-only |
| 5 | `course_id` | `int(11)` | 否 |  |  | 课目/课程ID，对应 store_course.id | internal | relation-key | server-filter-only |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `state` | `tinyint(4)` | 否 |  | 1 | 状态：1启用 -1删除 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_store_course_state`：非唯一 BTREE（store_id, course_id, state, order_by）

### `store_material_lessons_relation`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：tenant_id, store_id。
表注释：店铺素材课程关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户ID | internal | tenant-scope | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `material_id` | `int(11)` | 否 |  |  | 素材ID，对应 store_material.id | internal | relation-key | server-filter-only |
| 5 | `lessons_id` | `int(11)` | 否 |  |  | 课目/课程ID，对应 store_course.id | internal | relation-key | server-filter-only |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 7 | `state` | `tinyint(4)` | 否 |  | 1 | 状态：1启用 -1删除 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_store_course_state`：非唯一 BTREE（store_id, lessons_id, state, order_by）

### `store_media`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `platform` | `int(11)` | 是 |  |  | 0 阿里云OSS，1 微信，2 支付宝 | internal | business-field | semantic-review-required |
| 3 | `file_name` | `varchar(255)` | 是 |  |  | 文件名 | internal | business-field | semantic-review-required |
| 4 | `file_type` | `int(11)` | 是 |  |  | 0 图片 | internal | business-field | semantic-review-required |
| 5 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `md5` | `varchar(255)` | 是 |  |  | 文件MD5 | internal | business-field | semantic-review-required |
| 7 | `url` | `varchar(255)` | 是 |  |  | 可访问URL | internal | business-field | semantic-review-required |
| 8 | `platform_url` | `varchar(255)` | 是 |  |  | 平台URL | internal | business-field | semantic-review-required |
| 9 | `media_id` | `varchar(255)` | 是 |  |  | 素材ID | internal | relation-key | server-filter-only |
| 10 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `state` | `int(11)` | 是 |  |  | 0 无效 1 正常 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_member_follow_up`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：tenant_id, store_id。
表注释：门店会员试听转化跟进记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 跟进记录主键 | internal | relation-key | server-filter-only |
| 2 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户 ID | internal | tenant-scope | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 门店 ID | internal | store-scope | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 会员卡 ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `user_id` | `int(11)` | 否 |  | 0 | 用户 ID，散客为 0 | internal | subject-or-relation-key | server-filter-only |
| 6 | `operator_staff_id` | `int(11)` | 否 |  |  | 执行跟进的门店员工 ID | internal | relation-key | server-filter-only |
| 7 | `outcome` | `tinyint(4)` | 否 |  |  | 1已联系 2考虑中 3未接通 4明确拒绝 | internal | business-field | semantic-review-required |
| 8 | `state` | `tinyint(4)` | 否 |  | 0 | 0待继续跟进 1本次任务完成 | internal | business-field | semantic-review-required |
| 9 | `next_follow_up_date` | `datetime` | 是 |  |  | 下次跟进时间 | internal | business-field | semantic-review-required |
| 10 | `remark` | `varchar(500)` | 否 |  |  | 跟进备注 | sensitive-unstructured | business-field | deny |
| 11 | `create_by` | `bigint(20)` | 否 |  |  | 操作账号 UID | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_store_id`：非唯一 BTREE（store_id）

### `store_merchants_config`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `request_no` | `varchar(20)` | 是 |  |  | 入网请求号 | sensitive-unstructured | business-field | deny |
| 3 | `store_id` | `int(11)` | 是 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `mer_Level1_No` | `varchar(20)` | 是 |  |  | 商户一级分类 | internal | business-field | semantic-review-required |
| 5 | `mer_Level2_No` | `varchar(20)` | 是 |  |  | 商户二级分类 | internal | business-field | semantic-review-required |
| 6 | `mer_head_bank_code` | `varchar(20)` | 是 |  |  | 小微开户行 | internal | business-field | semantic-review-required |
| 7 | `mer_bank_code` | `varchar(20)` | 是 |  |  | 小微开户支行 | internal | business-field | semantic-review-required |
| 8 | `head_bank_code` | `varchar(20)` | 是 |  |  | 	开户银行编码 | internal | business-field | semantic-review-required |
| 9 | `bank_code` | `varchar(30)` | 是 |  |  | 开户银行支行编码 | internal | business-field | semantic-review-required |
| 10 | `alipay_account` | `varchar(30)` | 是 |  |  | 支付宝账号 | internal | business-field | semantic-review-required |
| 11 | `platform` | `int(11)` | 是 |  | 0 | 平台 0宜宝 1微信 2支付宝  | internal | business-field | semantic-review-required |
| 12 | `img_platform_idcard_fornt` | `varchar(200)` | 是 |  |  | 身份证正面照片(宜宝) | internal | business-field | semantic-review-required |
| 13 | `img_platform_idcard_back` | `varchar(200)` | 是 |  |  | 法人身份证反面(宜宝) | internal | business-field | semantic-review-required |
| 14 | `img_platform_uni_credit_code` | `varchar(200)` | 是 |  |  | 统一社会信用代码证 | internal | business-field | semantic-review-required |
| 15 | `img_platform_corp_code` | `varchar(200)` | 是 |  |  | 营业执照照片(宜宝) | internal | business-field | semantic-review-required |
| 16 | `img_platform_tax_code` | `varchar(200)` | 是 |  |  | 税务登记证(宜宝) | internal | business-field | semantic-review-required |
| 17 | `img_platform_org_code` | `varchar(200)` | 是 |  |  | 组织机构代码证(宜宝) | internal | business-field | semantic-review-required |
| 18 | `img_platform_op_bank_code` | `varchar(200)` | 是 |  |  | 银行开户许可证(宜宝) | internal | business-field | semantic-review-required |
| 19 | `img_platform_bank_card` | `varchar(200)` | 是 |  |  | 结算银行卡(宜宝) | restricted | business-field | deny |
| 20 | `img_platform_hand_idcard` | `varchar(200)` | 是 |  |  | 手持身份证(宜宝) | internal | business-field | semantic-review-required |
| 21 | `img_platform_hand_bank_card` | `varchar(200)` | 是 |  |  | 手持银行卡(宜宝) | restricted | business-field | deny |
| 22 | `img_platform_shop_photo` | `varchar(200)` | 是 |  |  | 门头照 | internal | business-field | semantic-review-required |
| 23 | `img_platform_cashier_scene` | `varchar(200)` | 是 |  |  | 易宝收银台场景照 | internal | business-field | semantic-review-required |
| 24 | `img_platform_transaction_invoice` | `varchar(200)` | 是 |  |  | 易宝 近 3 个月 内交易发票 | internal | business-field | semantic-review-required |
| 25 | `img_platform_hand_corp_code` | `varchar(200)` | 是 |  |  | 易宝手持营业执照的门头照合影 | internal | business-field | semantic-review-required |
| 26 | `mer_chant_no` | `varchar(50)` | 是 |  |  | 商户编号 | internal | business-field | semantic-review-required |
| 27 | `mer_type` | `int(11)` | 是 |  |  | 0小微 1个体 2企业 | internal | business-field | semantic-review-required |
| 28 | `mer_state` | `int(11)` | 是 |  |  | 状态（废弃） 0审核 1通过审核 -1 待签约 -2回退 -3未通过审核 3待签约 | internal | business-field | semantic-review-required |
| 29 | `mer_prepare_open_date` | `datetime` | 是 |  |  | 设置开通收款定时字段 | internal | business-field | semantic-review-required |
| 30 | `mer_open_type` | `int(11)` | 否 |  | 0 | 开通方式:0未设置，1定时开通，2立即开通 | internal | business-field | semantic-review-required |
| 31 | `state` | `int(11)` | 是 |  | -1 | 状态 0审核 1通过审核（已签约） -1 未填写 -2回退 -3未通过审核 2待账户验证（打款） 3待签约 4待授权（支付宝）10 开通支付 | internal | business-field | semantic-review-required |
| 32 | `report_state` | `int(11)` | 是 |  | -1 | 聚合报备状态 0审核 1通过审核 -1 未填写 -2回退 -3未通过审核 | internal | business-field | semantic-review-required |
| 33 | `signing_address` | `varchar(200)` | 是 |  |  | 签约地址 | sensitive | business-field | masked-or-filter-only |
| 34 | `note` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 35 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 36 | `open_date` | `datetime` | 是 |  |  | 开户时间 | internal | business-field | semantic-review-required |
| 37 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 38 | `is_update_bank_card` | `tinyint(1)` | 是 |  | 0 | 是否正在修改银行卡 | restricted | business-field | deny |
| 39 | `update_bank_card_date` | `datetime` | 是 |  |  | 修改银行卡的时间 | restricted | business-field | deny |
| 40 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `store_new_operating`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：新手引导

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `is_set_store_info` | `tinyint(1)` | 否 |  |  | 是否设置店铺信息 | internal | business-field | semantic-review-required |
| 4 | `is_set_card` | `tinyint(1)` | 否 |  | 0 | 是否设置了会员卡 | internal | business-field | semantic-review-required |
| 5 | `is_set_group_lessons` | `tinyint(1)` | 否 |  | 0 | 是否设置了团课 | internal | business-field | semantic-review-required |
| 6 | `is_set_private_lessons` | `tinyint(1)` | 否 |  | 0 | 是否设置了私教 | internal | business-field | semantic-review-required |
| 7 | `is_set_course_card_relation` | `tinyint(1)` | 否 |  | 0 | 是否设置课程扣卡关联 | internal | business-field | semantic-review-required |
| 8 | `is_add_group_lessons` | `tinyint(1)` | 否 |  | 0 | 是否创建团课排课 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_notice_remind_time_set`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `nid` | `bigint(20)` | 否 |  |  | 通知id | internal | business-field | semantic-review-required |
| 3 | `remind_title` | `varchar(20)` | 否 |  |  | 标题 如 2天 2小时 20分钟 | internal | business-field | semantic-review-required |
| 4 | `remind_minute` | `int(11)` | 否 |  |  | 提醒分钟 | internal | business-field | semantic-review-required |
| 5 | `remind_minute_min` | `int(11)` | 否 |  |  | 最小提醒分钟 | internal | business-field | semantic-review-required |
| 6 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_notice_set`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `nid` | `bigint(20)` | 否 |  |  | 通知id | internal | business-field | semantic-review-required |
| 3 | `wechat_is_open` | `tinyint(4)` | 否 |  |  | 是否开启微信消息 | internal | business-field | semantic-review-required |
| 4 | `sms_is_open` | `tinyint(4)` | 否 |  |  | 是否开启短信 | internal | business-field | semantic-review-required |
| 5 | `wechat_temp_id` | `varchar(100)` | 是 |  |  | 微信消息模板id | internal | relation-key | server-filter-only |
| 6 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_operate_time`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 营业时间自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `begin_time` | `varchar(20)` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 4 | `end_time` | `varchar(20)` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1正常 | internal | business-field | semantic-review-required |
| 7 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_operate_week`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `week_info` | `int(11)` | 否 |  |  | 营业日期1-7 | internal | business-field | semantic-review-required |
| 4 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 5 | `state` | `int(11)` | 否 |  |  | 状态 0停用 1启用 | internal | business-field | semantic-review-required |
| 6 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 7 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeid`：非唯一 BTREE（store_id）

### `store_pay_account`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `account_type` | `int(11)` | 否 |  |  | 0银行1微信 2支付宝 | internal | business-field | semantic-review-required |
| 4 | `account_name` | `varchar(10)` | 否 |  |  | 账户姓名 | internal | business-field | semantic-review-required |
| 5 | `account_id` | `varchar(50)` | 否 |  |  | 账户id | internal | relation-key | server-filter-only |
| 6 | `withdrawal_amount` | `decimal(10,2)` | 否 |  | 0.00 | 累计提现金额 | internal | business-field | semantic-review-required |
| 7 | `is_default` | `int(11)` | 否 |  |  | 是否是默认账户 1是 0否 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 0未启用 1启用 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `store_id`：唯一 BTREE（store_id, account_type）

### `store_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 店铺绩效方式ID | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 1正常 0暂停使用 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 6 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `store_id`：唯一 BTREE（store_id, performance_item_id）

### `store_permissions`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `p_name` | `varchar(30)` | 否 |  |  | 权限名称 | internal | business-field | semantic-review-required |
| 3 | `p_controller` | `varchar(30)` | 否 |  |  | 权限控制器 | internal | business-field | semantic-review-required |
| 4 | `p_action` | `varchar(30)` | 否 |  |  | 权限方法 | internal | business-field | semantic-review-required |
| 5 | `p_info` | `varchar(100)` | 是 |  |  | 权限说明 | internal | business-field | semantic-review-required |
| 6 | `p_level` | `int(11)` | 否 |  |  | 权限级别 | internal | business-field | semantic-review-required |
| 7 | `is_default` | `int(2)` | 否 |  |  | 是否默认打开1是 0否 | internal | business-field | semantic-review-required |
| 8 | `p_root_id` | `int(11)` | 否 |  |  | 上级权限Id | internal | relation-key | server-filter-only |
| 9 | `order_by` | `int(11)` | 否 |  |  | 排序 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态0停用 1启用 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_physical_card`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：实物卡

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `pre_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 4 | `card_no` | `varchar(30)` | 否 |  |  | 卡号 | internal | business-field | semantic-review-required |
| 5 | `secret_key` | `varchar(100)` | 否 | MUL |  | 秘钥 | restricted | business-field | deny |
| 6 | `uid` | `int(11)` | 否 |  | 0 | 用户id | internal | subject-or-relation-key | server-filter-only |
| 7 | `card_id` | `int(11)` | 否 |  | 0 | 会员卡id | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_child_id` | `int(11)` | 否 |  | 0 | 子卡id | internal | relation-key | server-filter-only |
| 9 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1可用 2已用 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_key`：非唯一 BTREE（secret_key）

### `store_place`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：场地

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `place_name` | `varchar(30)` | 否 |  |  | 场地名称 | internal | business-field | semantic-review-required |
| 4 | `place_describe` | `varchar(200)` | 是 |  |  | 场地描述 | internal | business-field | semantic-review-required |
| 5 | `reservation_num` | `int(11)` | 否 |  |  | 同时可预约次数 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 0关闭 1开放 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_place_close_info`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `place_id` | `int(11)` | 否 |  |  | 场地id | internal | relation-key | server-filter-only |
| 4 | `close_begin_date` | `date` | 否 |  |  | 关闭开始日期 | internal | business-field | semantic-review-required |
| 5 | `close_end_date` | `date` | 否 |  |  | 结束关闭日期 | internal | business-field | semantic-review-required |
| 6 | `close_weeks` | `varchar(20)` | 否 |  |  | 关闭周期的星期 | internal | business-field | semantic-review-required |
| 7 | `close_times` | `varchar(100)` | 否 |  |  | 关闭的时间段 | internal | business-field | semantic-review-required |
| 8 | `close_remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 9 | `state` | `int(11)` | 否 |  |  | -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_place_close_setting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：场地关闭时间设置

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `close_id` | `int(11)` | 否 |  | 0 | 关闭id | internal | relation-key | server-filter-only |
| 3 | `store_place_id` | `int(11)` | 否 |  |  | 场地ID | internal | relation-key | server-filter-only |
| 4 | `close_time_start` | `datetime` | 否 |  |  | 场地关闭开始时间 | internal | business-field | semantic-review-required |
| 5 | `close_time_end` | `datetime` | 否 |  |  | 场地关闭结束时间 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 0 关闭 1正常 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_place_operate_week`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `place_id` | `int(11)` | 否 |  |  | 场地id | internal | relation-key | server-filter-only |
| 4 | `week_info` | `int(11)` | 否 |  |  | 营业日期1-7 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 0停用 1启用 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_platform_auth_token`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `platform` | `int(11)` | 否 |  |  | 所属平台1 微信，2 QQ，3 支付宝 | internal | business-field | semantic-review-required |
| 4 | `product` | `int(11)` | 否 |  |  | 产品信息 0=C端，1=B端,2预约端，3营销端 4卡券端 | internal | business-field | semantic-review-required |
| 5 | `app_token` | `varchar(50)` | 是 |  |  | 授权令牌 | restricted | business-field | deny |
| 6 | `refresh_token` | `varchar(50)` | 是 |  |  |  刷新令牌 | restricted | business-field | deny |
| 7 | `auth_app_id` | `varchar(20)` | 是 |  |  | 应用id | internal | relation-key | server-filter-only |
| 8 | `expires_in` | `datetime` | 是 |  |  | 有效期 | internal | business-field | semantic-review-required |
| 9 | `re_expires_in` | `datetime` | 是 |  |  | 刷新令牌有效期 | internal | business-field | semantic-review-required |
| 10 | `user_id` | `varchar(20)` | 是 |  |  | 对应平台的用户唯一识别编码 | internal | subject-or-relation-key | server-filter-only |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_prepaid_card`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `card_name` | `varchar(20)` | 是 |  |  | 卡名称 | internal | business-field | semantic-review-required |
| 4 | `card_type` | `int(11)` | 否 |  |  | 类型：0计次，1储值 2时效卡 3权益卡 4安心充卡 6课时卡 | internal | business-field | semantic-review-required |
| 5 | `card_img` | `varchar(50)` | 是 |  |  | 背景图 | internal | business-field | semantic-review-required |
| 6 | `price` | `decimal(10,2)` | 否 |  |  | 售价 | internal | business-field | semantic-review-required |
| 7 | `discount_price` | `decimal(10,2)` | 是 |  |  | 折扣价 | internal | business-field | semantic-review-required |
| 8 | `card_value` | `decimal(10,2)` | 否 |  |  | 卡价值 次/金额 | internal | business-field | semantic-review-required |
| 9 | `card_giving_value` | `decimal(10,2)` | 否 |  |  | 赠送 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  | 1.00 | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `card_note` | `varchar(100)` | 是 |  |  | 卡备注 | sensitive-unstructured | business-field | deny |
| 12 | `card_count` | `int(11)` | 否 |  |  | 剩余数量 | internal | business-field | semantic-review-required |
| 13 | `card_sell_count` | `int(11)` | 否 |  |  | 销售数量 | internal | business-field | semantic-review-required |
| 14 | `max_count` | `int(11)` | 否 |  | 0 | 最大销售数量 0不限制 | internal | business-field | semantic-review-required |
| 15 | `single_max_frequency` | `int(11)` | 否 |  | 0 | 单次最大次数 0不限 | internal | business-field | semantic-review-required |
| 16 | `day_max_frequency` | `int(11)` | 否 |  | 0 | 每日最大核销次数 0不限 (1限制代约.) | internal | business-field | semantic-review-required |
| 17 | `week_max_frequency` | `int(11)` | 否 |  | 0 | 每周最大核销次数 0不限 | internal | business-field | semantic-review-required |
| 18 | `mouth_max_frequency` | `int(11)` | 否 |  | 0 | 每月最大核销次数 0不限 | internal | business-field | semantic-review-required |
| 19 | `day_max_reservation` | `int(11)` | 否 |  | 0 | 每日最大预约次数 0不限 (1限制代约.) | internal | business-field | semantic-review-required |
| 20 | `week_max_reservation` | `int(11)` | 否 |  | 0 | 每周最大预约次数 0不限 | internal | business-field | semantic-review-required |
| 21 | `mouth_max_reservation` | `int(11)` | 否 |  | 0 | 每月最大预约次数 0不限 | internal | business-field | semantic-review-required |
| 22 | `is_limit_time` | `tinyint(1)` | 否 |  | 0 | 是否限制可用时段 | internal | business-field | semantic-review-required |
| 23 | `valid_type` | `int(11)` | 否 |  | 0 | 失效日期类型: 0 相对日期（购卡后N天； 1 绝对日期（指定失效日期） | internal | business-field | semantic-review-required |
| 24 | `invalid_date` | `datetime` | 是 |  |  | 失效日期 | internal | business-field | semantic-review-required |
| 25 | `validity_date` | `int(11)` | 否 |  |  | 有效期（天）0为永久 | internal | business-field | semantic-review-required |
| 26 | `open_card_type` | `int(11)` | 否 |  | 0 | 开卡方式 0购买即开卡，1首次使用开卡 | internal | business-field | semantic-review-required |
| 27 | `stop_card_days` | `int(11)` | 否 |  | 0 | 停卡天数 | internal | business-field | semantic-review-required |
| 28 | `open_card_days_max` | `int(11)` | 否 |  | 0 | 最大延迟开卡天数 | internal | business-field | semantic-review-required |
| 29 | `is_pay_after_receive` | `tinyint(1)` | 否 |  | 0 | 是否支付后领取 | internal | business-field | semantic-review-required |
| 30 | `is_buy_once` | `tinyint(1)` | 否 |  | 0 | 是否只能购买一次 | internal | business-field | semantic-review-required |
| 31 | `is_limit_frequency` | `tinyint(1)` | 否 |  | 0 | 是否限制次数 | internal | business-field | semantic-review-required |
| 32 | `card_instructions` | `varchar(1000)` | 是 |  |  | 会员权益 | internal | business-field | semantic-review-required |
| 33 | `is_prompt_rights` | `tinyint(1)` | 否 |  | 0 | 是否会员权益强提示 | internal | business-field | semantic-review-required |
| 34 | `is_card_child` | `tinyint(1)` | 否 |  | 0 | 是否包含子卡 | internal | business-field | semantic-review-required |
| 35 | `is_auditing` | `tinyint(1)` | 否 |  | 0 | 是否需要发放审核 | internal | business-field | semantic-review-required |
| 36 | `is_use_audit` | `tinyint(1)` | 否 |  | 0 | 是否需要使用审核 | internal | business-field | semantic-review-required |
| 37 | `is_alliance_card` | `tinyint(1)` | 否 |  | 0 | 是否为联盟卡 | internal | business-field | semantic-review-required |
| 38 | `is_custom_price` | `tinyint(1)` | 否 |  | 0 | 是否开启自定义金额 | internal | business-field | semantic-review-required |
| 39 | `custom_price_min` | `decimal(10,2)` | 否 |  |  | 自定义储值最低 0不限 | internal | business-field | semantic-review-required |
| 40 | `custom_price_max` | `decimal(10,2)` | 否 |  |  | 自定义储值最高 0不限 | internal | business-field | semantic-review-required |
| 41 | `custom_price_give_ratio` | `decimal(3,2)` | 否 |  |  | 赠送比例 | internal | business-field | semantic-review-required |
| 42 | `is_transfer_card` | `tinyint(1)` | 否 |  | 0 | 是否开启转让卡 | internal | business-field | semantic-review-required |
| 43 | `is_transfer_card_value` | `tinyint(1)` | 否 |  | 0 | 是否开启转让卡余额 | internal | business-field | semantic-review-required |
| 44 | `transfer_max_count` | `int(11)` | 否 |  | 0 |  转让卡次数 0不限 | internal | business-field | semantic-review-required |
| 45 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 46 | `wx_card_state` | `int(11)` | 是 |  | -1 | 微信卡包卡样状态 -2 审核失败，-1未同步 0审核，1已同步 | internal | business-field | semantic-review-required |
| 47 | `wx_card_id` | `varchar(50)` | 是 |  |  | 微信卡包卡id | internal | relation-key | server-filter-only |
| 48 | `al_card_state` | `int(11)` | 是 |  | -1 | 支付宝卡包卡样状态-2 审核失败，-1未同步 0审核，1已同步 | internal | business-field | semantic-review-required |
| 49 | `al_card_id` | `varchar(50)` | 是 |  |  | 支付宝卡包id | internal | relation-key | server-filter-only |
| 50 | `associated_id` | `int(11)` | 否 |  |  | 用于修改卡后新建卡与基卡的ID相关联 | internal | relation-key | server-filter-only |
| 51 | `is_common` | `tinyint(1)` | 否 |  | 1 | 是否是通用卡（连锁店） | internal | business-field | semantic-review-required |
| 52 | `use_max_count` | `decimal(10,2)` | 否 |  | -1.00 | 最大使用次数 -1不限 | internal | business-field | semantic-review-required |
| 53 | `state` | `int(11)` | 否 |  |  | 1在售 0停售 -1删除  2售完 | internal | business-field | semantic-review-required |
| 54 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 55 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 56 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 57 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 58 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id）
- `store_index`：非唯一 BTREE（store_id）

### `store_prepaid_card_child`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `store_prepaid_card_id` | `int(11)` | 否 |  |  | 店铺卡id | restricted | relation-key | deny |
| 4 | `card_name` | `varchar(50)` | 否 |  |  | 卡名 | internal | business-field | semantic-review-required |
| 5 | `card_img` | `varchar(100)` | 否 |  |  | 图片 | internal | business-field | semantic-review-required |
| 6 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 7 | `give_price` | `decimal(10,2)` | 是 |  |  | 赠送金额 | internal | business-field | semantic-review-required |
| 8 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣价 | internal | business-field | semantic-review-required |
| 9 | `card_sell_count` | `int(11)` | 否 |  |  | 卡售出数量 | internal | business-field | semantic-review-required |
| 10 | `card_count` | `int(11)` | 否 |  | 0 | 剩余数量 | internal | business-field | semantic-review-required |
| 11 | `max_count` | `int(11)` | 否 |  |  | 最大可售出数量 | internal | business-field | semantic-review-required |
| 12 | `valid_type` | `int(11)` | 否 |  | 0 | 失效日期类型: 0 相对日期（购卡后N天)； 1 绝对日期（指定失效日期） | internal | business-field | semantic-review-required |
| 13 | `invalid_date` | `datetime` | 是 |  |  | 失效日期 | internal | business-field | semantic-review-required |
| 14 | `day_max_frequency` | `int(11)` | 否 |  |  | 有效期，天；0-永久 | internal | business-field | semantic-review-required |
| 15 | `is_buy_once` | `tinyint(1)` | 否 |  | 0 | 是否只能购买一次 | internal | business-field | semantic-review-required |
| 16 | `is_alliance_card` | `tinyint(1)` | 否 |  | 0 | 是否为联盟卡 | internal | business-field | semantic-review-required |
| 17 | `state` | `int(11)` | 否 |  |  | 状态；1-在售，0-停售，-1-删除 | internal | business-field | semantic-review-required |
| 18 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 19 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 20 | `update_by` | `int(11)` | 否 |  |  | 更新人 | internal | business-field | semantic-review-required |
| 21 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 22 | `start_date` | `datetime` | 是 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 23 | `end_date` | `datetime` | 是 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 24 | `axc_plan_id` | `varchar(255)` | 是 |  |  | 安心充方案ID | internal | relation-key | server-filter-only |
| 25 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_prepaid_card_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：储值卡关联项目表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `prepaid_card_id` | `int(11)` | 否 | MUL |  | 储值卡id | restricted | relation-key | deny |
| 5 | `card_value` | `decimal(10,2)` | 否 |  |  | 卡价值 次/金额 | internal | business-field | semantic-review-required |
| 6 | `is_gift` | `tinyint(1)` | 否 |  | 0 | 是否是赠送 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  | 1 | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_pcid`：非唯一 BTREE（prepaid_card_id）

### `store_reservation`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：预约

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 会员卡Id | internal | subject-or-relation-key | server-filter-only |
| 5 | `child_card_id` | `int(11)` | 否 |  |  | 子卡id | internal | relation-key | server-filter-only |
| 6 | `store_place_id` | `int(11)` | 是 |  |  | 场地ID | internal | relation-key | server-filter-only |
| 7 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 8 | `user_name` | `varchar(50)` | 是 |  |  | 用户名 | sensitive | business-field | masked-or-filter-only |
| 9 | `user_mobile` | `varchar(20)` | 是 |  |  | 用户手机号 | sensitive | business-field | masked-or-filter-only |
| 10 | `lessons_id` | `int(11)` | 否 | MUL | 0 | 课 ID | internal | relation-key | server-filter-only |
| 11 | `course_type` | `int(11)` | 否 |  | 0 | 课目类型 0团课 1私教 | internal | business-field | semantic-review-required |
| 12 | `staff_id` | `int(11)` | 否 |  |  | 技师（员工）ID | internal | subject-or-relation-key | server-filter-only |
| 13 | `class_id` | `int(11)` | 否 |  |  | 班级id | internal | relation-key | server-filter-only |
| 14 | `reservation_time` | `datetime` | 否 |  |  | 预约时间 | internal | business-field | semantic-review-required |
| 15 | `reservation_time_end` | `datetime` | 是 |  |  | 预约结束时间 | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(200)` | 是 |  |  | 备注 （用户） | sensitive-unstructured | business-field | deny |
| 17 | `business_remark` | `varchar(200)` | 是 |  |  | 备注（商家） | sensitive-unstructured | business-field | deny |
| 18 | `people_count` | `int(11)` | 否 |  | 1 | 人数 | internal | business-field | semantic-review-required |
| 19 | `is_wechat_notice` | `tinyint(1)` | 否 |  | 0 | 是否已经发送通知 | internal | business-field | semantic-review-required |
| 20 | `is_service_item` | `tinyint(1)` | 否 |  | 0 | 是否关联项目 | internal | business-field | semantic-review-required |
| 21 | `is_staff` | `tinyint(1)` | 否 |  | 0 | 是否关联技师 | internal | business-field | semantic-review-required |
| 22 | `is_place` | `tinyint(1)` | 否 |  | 0 | 是否关联场地 | internal | business-field | semantic-review-required |
| 23 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否关联商品 | internal | business-field | semantic-review-required |
| 24 | `is_record_penalty` | `tinyint(1)` | 否 |  | 0 | 是否记录处罚 | internal | business-field | semantic-review-required |
| 25 | `is_penalty` | `tinyint(1)` | 否 |  | 0 | 是否处罚 | internal | business-field | semantic-review-required |
| 26 | `is_set_note` | `tinyint(1)` | 否 |  | 0 | 是否记录笔记 | sensitive-unstructured | business-field | deny |
| 27 | `is_experience` | `tinyint(1)` | 否 |  | 0 | 是否为体验课 | internal | business-field | semantic-review-required |
| 28 | `is_refunds` | `tinyint(1)` | 否 |  | 1 | 是否退款(目的是在付费预约退款失败时记录状态) | internal | business-field | semantic-review-required |
| 29 | `refunds_reason` | `varchar(100)` | 是 |  | 0 | 退款失败原因 | internal | business-field | semantic-review-required |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 -2未到店(旷课)，-1已取消（主动），0未确认（待支付），1以确定，2到店（签到） 10候补 | internal | business-field | semantic-review-required |
| 31 | `sign_date` | `datetime` | 是 |  |  | 签到时间 | internal | business-field | semantic-review-required |
| 32 | `sign_file` | `varchar(100)` | 是 |  |  | 签到文件 | internal | business-field | semantic-review-required |
| 33 | `cancel_type` | `int(11)` | 否 |  | 0 | 取消类型 0主动取消（用于监控惩罚） 1被动取消 | internal | business-field | semantic-review-required |
| 34 | `state_reason` | `varchar(100)` | 是 |  |  | 状态原因 主要针对取消状态 | internal | business-field | semantic-review-required |
| 35 | `is_vacation` | `tinyint(1)` | 否 |  | 0 | 是否请假 | internal | business-field | semantic-review-required |
| 36 | `tenant_id` | `int(11)` | 否 |  | 0 | 商户ID | internal | tenant-scope | server-filter-only |
| 37 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 38 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 39 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 40 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_lessonsId`：非唯一 BTREE（lessons_id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `store_reservation_controls`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  |  | internal | store-scope | server-filter-only |
| 3 | `common_reservation_controls_id` | `int(11)` | 否 |  |  |  | internal | relation-key | server-filter-only |
| 4 | `store_type` | `varchar(10)` | 否 |  |  | 店铺类型（仅对store=0有效） | internal | business-field | semantic-review-required |
| 5 | `control_name` | `varchar(50)` | 否 |  |  | 控件名称 | internal | business-field | semantic-review-required |
| 6 | `control_instructions` | `varchar(100)` | 否 |  |  | 控件说明 | internal | business-field | semantic-review-required |
| 7 | `control_type` | `varchar(20)` | 否 |  |  | 控件类型 input,radio,select.... | internal | business-field | semantic-review-required |
| 8 | `note` | `varchar(100)` | 否 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 9 | `is_must` | `tinyint(1)` | 否 |  |  | 是否必填项 | internal | business-field | semantic-review-required |
| 10 | `is_show` | `tinyint(1)` | 否 |  |  | 是否对C端展示 | internal | business-field | semantic-review-required |
| 11 | `order_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `state` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `store_id`：唯一 BTREE（store_id, common_reservation_controls_id）

### `store_reservation_controls_item`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `store_reservation_controls_id` | `int(11)` | 否 |  |  |  | internal | relation-key | server-filter-only |
| 4 | `item_name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 5 | `item_value` | `varchar(100)` | 否 |  |  | 值 | internal | business-field | semantic-review-required |
| 6 | `is_default` | `tinyint(1)` | 否 |  |  | 是否是默认 | internal | business-field | semantic-review-required |
| 7 | `is_show` | `tinyint(1)` | 否 |  |  | 是否对C端展示 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_reservation_detailed`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `store_reservation_id` | `int(11)` | 否 |  |  | 预约id | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  | 0 | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `user_key` | `varchar(50)` | 否 |  |  | 自定义信息key | internal | business-field | semantic-review-required |
| 6 | `user_value` | `varchar(50)` | 否 |  |  | 自定义信息value | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_reservation_item`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `reservation_id` | `int(11)` | 否 | MUL |  | 预约ID | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目ID | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  |  | 状态1 | internal | business-field | semantic-review-required |
| 5 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 6 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_rid`：非唯一 BTREE（reservation_id）

### `store_reservation_note`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `bigint(20)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `bigint(20)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 5 | `reservation_id` | `bigint(20)` | 否 |  |  | 预约id | internal | relation-key | server-filter-only |
| 6 | `note` | `text` | 否 |  |  | 笔记 | sensitive-unstructured | business-field | deny |
| 7 | `is_have_image` | `tinyint(1)` | 否 |  |  | 是否关联了图片 | internal | business-field | semantic-review-required |
| 8 | `is_show` | `tinyint(1)` | 否 |  | 0 | 是否显示过 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_reservation_note_image`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `reservation_id` | `bigint(20)` | 否 |  |  | 预约id | internal | relation-key | server-filter-only |
| 4 | `note_id` | `bigint(20)` | 否 |  |  | 笔记id | sensitive-unstructured | relation-key | deny |
| 5 | `image_url` | `varchar(100)` | 否 |  |  | 笔记图片 | internal | business-field | semantic-review-required |
| 6 | `order_by` | `int(11)` | 否 |  | 0 | 排序 倒序 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_reservation_seting`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `is_select_staff` | `tinyint(1)` | 否 |  |  | 是否可选技师 | internal | business-field | semantic-review-required |
| 4 | `is_select_item` | `tinyint(1)` | 否 |  |  | 是否可选项目 | internal | business-field | semantic-review-required |
| 5 | `is_vip` | `tinyint(1)` | 否 |  | 0 | 是否仅会员可约 | internal | business-field | semantic-review-required |
| 6 | `card_pay_order` | `int(11)` | 否 |  | 0 | 卡支付顺序，0预约时支付 1签到时支付 | internal | business-field | semantic-review-required |
| 7 | `sign_in_set` | `int(11)` | 否 |  |  | 签到设置 1开课后自动签到 2下课后自动签到 3下课后N分钟自动签到 11老师点名签到 12扫码签到 13签字签到 | internal | business-field | semantic-review-required |
| 8 | `sign_in_minutes` | `int(11)` | 否 |  | 0 | 签到时间分钟 | internal | business-field | semantic-review-required |
| 9 | `group_card_pay_order` | `int(11)` | 否 |  | 0 | 卡支付顺序，0预约时支付 1签到时支付 | internal | business-field | semantic-review-required |
| 10 | `group_sign_in_set` | `int(11)` | 否 |  | 1 | 签到设置 1开课后自动签到 2下课后自动签到 3下课后N分钟自动签到 11老师点名签到 12扫码签到 13签字签到 | internal | business-field | semantic-review-required |
| 11 | `group_sign_in_minutes` | `int(11)` | 否 |  | 0 | 签到时间分钟 | internal | business-field | semantic-review-required |
| 12 | `class_card_pay_order` | `int(11)` | 否 |  | 0 | 卡支付顺序，0预约时支付 1签到时支付 | internal | business-field | semantic-review-required |
| 13 | `class_sign_in_set` | `int(11)` | 否 |  | 11 | 签到设置 1开课后自动签到 2下课后自动签到 3下课后N分钟自动签到 11老师点名签到 12扫码签到 13签字签到 | internal | business-field | semantic-review-required |
| 14 | `class_sign_in_minutes` | `int(11)` | 否 |  | 0 | 签到时间分钟 | internal | business-field | semantic-review-required |
| 15 | `is_select_more_item` | `tinyint(1)` | 否 |  |  | 是否可选多个项目 | internal | business-field | semantic-review-required |
| 16 | `is_open_time` | `tinyint(1)` | 是 |  |  | 是否设置固定时间段 | internal | business-field | semantic-review-required |
| 17 | `is_open_time_conflict` | `tinyint(1)` | 否 |  | 0 | 是否开启冲突时间过滤 | internal | business-field | semantic-review-required |
| 18 | `time_conflict_seting` | `int(11)` | 否 |  |  | 时间冲突设置 0固定间隔，1按项目时长 与选择开启项目联动 | internal | business-field | semantic-review-required |
| 19 | `fixed_time` | `int(11)` | 否 |  | 60 | 固定时间 分钟 | internal | business-field | semantic-review-required |
| 20 | `is_client_wechat_notice` | `tinyint(1)` | 否 |  |  | 预约成功顾客微信通知 | internal | business-field | semantic-review-required |
| 21 | `is_client_sms_notice` | `tinyint(1)` | 否 |  |  | 预约成功顾客短信通知 | internal | business-field | semantic-review-required |
| 22 | `is_advance_staff_wechat_notice` | `tinyint(1)` | 否 |  |  | 提前技师微信通知 | internal | business-field | semantic-review-required |
| 23 | `is_advance_staff_sms_notice` | `tinyint(1)` | 否 |  |  | 提前技师短信通知 | internal | business-field | semantic-review-required |
| 24 | `advance_client_minute` | `int(11)` | 否 |  |  | 顾客提前通知分钟数 | internal | business-field | semantic-review-required |
| 25 | `advance_staff_minute` | `int(11)` | 否 |  |  | 技师提前通知分钟数 | internal | business-field | semantic-review-required |
| 26 | `reservation_num` | `int(11)` | 否 |  |  | 每人每天最多可约场次 | internal | business-field | semantic-review-required |
| 27 | `reservation_minute` | `int(11)` | 否 |  | 0 | 顾客提前多少分钟可约（-1不限制） | internal | business-field | semantic-review-required |
| 28 | `time_interval` | `int(11)` | 否 |  | 0 | 预约时间间隔 | internal | business-field | semantic-review-required |
| 29 | `is_cancel` | `tinyint(1)` | 否 |  | 1 | 是否可以取消预约 | internal | business-field | semantic-review-required |
| 30 | `cancel_minute` | `int(11)` | 否 |  | 0 | 开始前多少分钟可取消（0 不限制 1440 1天） | internal | business-field | semantic-review-required |
| 31 | `cancel_sum` | `int(11)` | 否 |  | 0 | 取消N次 0不限制 | internal | business-field | semantic-review-required |
| 32 | `cancel_cycle` | `int(11)` | 否 |  | 0 | 0天 1周 2月 当N | internal | business-field | semantic-review-required |
| 33 | `cancel_appointment_days` | `int(11)` | 否 |  | 1 |  N天不允许预约 | internal | business-field | semantic-review-required |
| 34 | `service_intervals` | `int(11)` | 否 |  | 0 | 两次服务间隔（分钟 0无间隔） | internal | business-field | semantic-review-required |
| 35 | `miss_appointment_penalty` | `int(11)` | 否 |  |  | 爽约处罚 0未开启 1每月 2每年 | internal | business-field | semantic-review-required |
| 36 | `miss_appointment_sum` | `int(11)` | 否 |  |  | 爽约次数 | internal | business-field | semantic-review-required |
| 37 | `miss_appointment_is_card` | `tinyint(1)` | 否 |  | 0 | 私教是否开启爽约用卡惩罚 | internal | business-field | semantic-review-required |
| 38 | `miss_appointment_penalty_value` | `int(11)` | 否 |  | 0 | 处罚内容（目前支持处罚时限卡有效期。计次卡、储值卡默认处罚最后一次爽约的预约项） | internal | business-field | semantic-review-required |
| 39 | `miss_appointment_black_days` | `int(11)` | 否 |  | 0 | 私教处罚 黑名单天数 0不处罚 | internal | business-field | semantic-review-required |
| 40 | `reservation_people_num` | `int(11)` | 否 |  |  | 私教课可预约人数，0不限制人数 | internal | business-field | semantic-review-required |
| 41 | `is_group_lesson_conflict` | `tinyint(1)` | 否 |  |  | 私教课教练 是否与团课授课时间冲突 | internal | business-field | semantic-review-required |
| 42 | `is_only_staff` | `tinyint(1)` | 否 |  |  | 私教是否只能约指定教练 | internal | business-field | semantic-review-required |
| 43 | `reservation_day` | `int(11)` | 否 |  | -1 | 提前N天可约 (-1不限制,0当天) | internal | business-field | semantic-review-required |
| 44 | `lesson_show_max_day` | `int(11)` | 否 |  | -1 | 私教显示排课范围xx天 -1显示所有 0当天 | internal | business-field | semantic-review-required |
| 45 | `lesson_reservation_time` | `varchar(20)` | 否 |  |  | 私教放课时间 空不限制 | internal | business-field | semantic-review-required |
| 46 | `group_lesson_is_cancel` | `tinyint(1)` | 否 |  | 1 | 团课是否可以取消预约 | internal | business-field | semantic-review-required |
| 47 | `group_lesson_cancel_minute` | `int(11)` | 否 |  | 0 | 团课开始前多少分钟可取消（0 不限制 1440 1天） | internal | business-field | semantic-review-required |
| 48 | `group_lesson_people_auto_cancel` | `int(11)` | 否 |  | 0 | 团课不满足最低人数自动取消分钟 0不限制 | internal | business-field | semantic-review-required |
| 49 | `group_lesson_miss_appointment_penalty` | `int(11)` | 否 |  |  | 团课爽约处罚 0未开启 1每月 2每年 | internal | business-field | semantic-review-required |
| 50 | `group_lesson_miss_appointment_sum` | `int(11)` | 否 |  |  | 团课爽约次数 | internal | business-field | semantic-review-required |
| 51 | `group_lesson_miss_appointment_is_card` | `tinyint(1)` | 否 |  | 0 | 团课是否开启爽约用卡惩罚 | internal | business-field | semantic-review-required |
| 52 | `group_lesson_miss_appointment_penalty_value` | `int(11)` | 否 |  | 0 | 团课处罚内容（目前支持处罚时限卡有效期。计次卡、储值卡默认处罚最后一次爽约的预约项） | internal | business-field | semantic-review-required |
| 53 | `group_lesson_miss_appointment_black_days` | `int(11)` | 否 |  | 0 | 团课处罚 黑名单天数 0不处罚 | internal | business-field | semantic-review-required |
| 54 | `group_lesson_is_reserve` | `tinyint(1)` | 否 |  |  | 团课是否开启候补  | internal | business-field | semantic-review-required |
| 55 | `is_show_avatar` | `tinyint(1)` | 否 |  | 0 | 是否显示头像 | internal | business-field | semantic-review-required |
| 56 | `is_show_people_num` | `tinyint(1)` | 否 |  |  | 是否显示预约人数 | internal | business-field | semantic-review-required |
| 57 | `is_show_unfilled_quota` | `tinyint(1)` | 否 |  |  | 是否显示剩余可约名额 | internal | business-field | semantic-review-required |
| 58 | `is_show_people_list` | `tinyint(1)` | 否 |  |  | 是否显示预约列表 | internal | business-field | semantic-review-required |
| 59 | `group_lesson_reservation_day` | `int(11)` | 否 |  | -1 | 团课提前N天可约 (-1不限制,0当天) | internal | business-field | semantic-review-required |
| 60 | `group_lesson_show_max_day` | `int(11)` | 否 |  | -1 | 显示排课范围xx天 -1显示所有 0当天 | internal | business-field | semantic-review-required |
| 61 | `group_lesson_reservation_time` | `varchar(20)` | 否 |  |  | 团课放课时间 空不限制 | internal | business-field | semantic-review-required |
| 62 | `group_lesson_reservation_minute` | `int(11)` | 否 |  | 0 | 团课顾客提前多少分钟可约（-1不限制） | internal | business-field | semantic-review-required |
| 63 | `is_private_lessons` | `tinyint(1)` | 否 |  | 1 | 是否开启私教 | internal | business-field | semantic-review-required |
| 64 | `is_group_lessons` | `tinyint(1)` | 否 |  | 1 | 是否开启团课 | internal | business-field | semantic-review-required |
| 65 | `private_lessons_title` | `varchar(20)` | 否 |  |  | 私教标题 默认空 | internal | business-field | semantic-review-required |
| 66 | `group_lessons_title` | `varchar(20)` | 否 |  |  | 团课标题，默认空 | internal | business-field | semantic-review-required |
| 67 | `state` | `int(11)` | 否 |  |  | 状态 1正常 | internal | business-field | semantic-review-required |
| 68 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 69 | `update_by` | `int(11)` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 70 | `update_date` | `datetime` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 71 | `create_by` | `int(11)` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 72 | `create_date` | `datetime` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `store_reservation_tag`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：预约相关标签

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `tag_type` | `int(11)` | 否 |  |  | 标签类型：1个人标签 2擅长 3课程 4课程图片 5课程分类 6课程辅助工具 | internal | business-field | semantic-review-required |
| 4 | `tag_title` | `varchar(50)` | 否 |  |  | 标签名 | internal | business-field | semantic-review-required |
| 5 | `tag_sub_title` | `varchar(50)` | 是 |  |  | 标签副标题 | internal | business-field | semantic-review-required |
| 6 | `is_show_lessons_down` | `tinyint(1)` | 否 |  |  | 下载课表是否显示 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `order_by` | `int(11)` | 否 |  | 0 | 排序 倒序 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_reservation_time_seting`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `reservation_time` | `varchar(20)` | 否 |  |  | 预约时间段 | internal | business-field | semantic-review-required |
| 4 | `reservation_time_end` | `varchar(20)` | 是 |  |  | 预约时间段结束 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1正常 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 7 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeid`：非唯一 BTREE（store_id）

### `store_rider`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `staff_id` | `int(11)` | 否 |  |  | 员工id | internal | subject-or-relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 员工用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `rider_type` | `int(11)` | 否 |  |  | 骑手状态；0-空闲，1-配送中 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺项目服务表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键Id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `item_name` | `varchar(20)` | 否 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 4 | `item_unit` | `varchar(10)` | 否 |  | 次 | 单位 | internal | business-field | semantic-review-required |
| 5 | `item_img` | `varchar(100)` | 是 |  |  | 服务的图片 | internal | business-field | semantic-review-required |
| 6 | `item_class_id` | `varchar(20)` | 是 |  |  | 项目分类 | internal | relation-key | server-filter-only |
| 7 | `item_price` | `decimal(10,2)` | 是 |  | 0.00 | 服务价格 | internal | business-field | semantic-review-required |
| 8 | `item_vip_price` | `decimal(10,2)` | 是 |  | 0.00 | vip价格 | internal | business-field | semantic-review-required |
| 9 | `is_reservation` | `tinyint(1)` | 否 |  | 1 | 是否支持预约 | internal | business-field | semantic-review-required |
| 10 | `is_card_discount` | `tinyint(1)` | 否 |  | 0 | 是否参与卡折扣 | internal | business-field | semantic-review-required |
| 11 | `is_pay` | `tinyint(1)` | 否 |  | 0 | 是否参与支付 | internal | business-field | semantic-review-required |
| 12 | `association_card` | `int(11)` | 是 |  |  | 关联储值卡数量 | internal | business-field | semantic-review-required |
| 13 | `item_info` | `varchar(200)` | 是 |  |  | 项目描述 | internal | business-field | semantic-review-required |
| 14 | `reservation_people_sum` | `int(11)` | 是 |  |  | 同一时间段可预约人数 | internal | business-field | semantic-review-required |
| 15 | `item_duration` | `int(11)` | 是 |  |  | 项目时长  分钟 | internal | business-field | semantic-review-required |
| 16 | `is_reservation_show` | `tinyint(1)` | 否 |  | 1 | 是否在预约中显示 | internal | business-field | semantic-review-required |
| 17 | `sell_num` | `int(11)` | 否 |  | 0 | 销量 | internal | business-field | semantic-review-required |
| 18 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 19 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 20 | `state` | `int(11)` | 否 |  |  | 状态 -1删除0禁用 1启用 | internal | business-field | semantic-review-required |
| 21 | `on_off_state` | `int(11)` | 否 |  | 0 | 上下架状态 | internal | business-field | semantic-review-required |
| 22 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 23 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 24 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 25 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 26 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `store_seting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺设置

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `is_controls` | `int(11)` | 否 |  | 0 | 是否设置控件 | internal | business-field | semantic-review-required |
| 4 | `is_limit` | `int(11)` | 否 |  | 0 | 是否设置了权益 | internal | business-field | semantic-review-required |
| 5 | `is_agreement` | `int(11)` | 否 |  | 0 | 是否设置了协议 | internal | business-field | semantic-review-required |
| 6 | `is_info` | `int(11)` | 否 |  | 0 | 是否设置了店铺信息 | internal | business-field | semantic-review-required |
| 7 | `is_sign_agreement` | `tinyint(1)` | 否 |  | 0 | 是否需要签署协议 | internal | business-field | semantic-review-required |
| 8 | `store_agreement` | `text` | 是 |  |  | 会员协议 | internal | business-field | semantic-review-required |
| 9 | `is_stall_mode` | `tinyint(1)` | 否 |  | 0 | 是否档口模式 | internal | business-field | semantic-review-required |
| 10 | `is_confirm_pass` | `tinyint(1)` | 否 |  | 0 | 会员卡消费是否要确认密码 | internal | business-field | semantic-review-required |
| 11 | `is_membership_card_transfer` | `tinyint(1)` | 否 |  | 0 | 是否允许会员卡转让 | internal | business-field | semantic-review-required |
| 12 | `store_introduce` | `text` | 是 |  |  | 店铺介绍 | internal | business-field | semantic-review-required |
| 13 | `manage_wechat` | `varchar(50)` | 是 |  |  | 店长微信 | internal | business-field | semantic-review-required |
| 14 | `manage_wechat_image` | `varchar(100)` | 是 |  |  | 店长微信图片 | internal | business-field | semantic-review-required |
| 15 | `lessons_rank` | `tinyint(1)` | 否 |  | 0 | 是否显示上课排行榜 | internal | business-field | semantic-review-required |
| 16 | `lessons_rank_count` | `int(11)` | 否 |  | 15 | 排行榜数量 | internal | business-field | semantic-review-required |
| 17 | `lessons_show_type` | `int(11)` | 否 |  | 0 | 排课显示类型 0公开 1仅会员 2仅有余额会员 | internal | business-field | semantic-review-required |
| 18 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeid`：非唯一 BTREE（store_id）

### `store_shop_seting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 逐渐ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 门店ID | internal | store-scope | server-filter-only |
| 3 | `shop_title` | `varchar(30)` | 否 |  |  | 商城标题 | internal | business-field | semantic-review-required |
| 4 | `is_enableshop` | `tinyint(1)` | 否 |  |  | 门店是否启用商城1启用 0不启用 | internal | business-field | semantic-review-required |
| 5 | `shop_style` | `int(11)` | 否 |  |  | 商城展现样式0 上下，1左右 | internal | business-field | semantic-review-required |
| 6 | `is_integral_shop` | `tinyint(1)` | 否 |  | 0 | 是否开启积分商城 | internal | business-field | semantic-review-required |
| 7 | `is_integral_deduction` | `tinyint(1)` | 否 |  | 0 | 是否参与积分抵扣 | internal | business-field | semantic-review-required |
| 8 | `is_take` | `tinyint(1)` | 否 |  |  | 是否开启配送服务 | internal | business-field | semantic-review-required |
| 9 | `express_type` | `int(11)` | 否 |  |  | 配送类型，0无需邮寄 1快递，2短途配送 | internal | business-field | semantic-review-required |
| 10 | `is_express` | `tinyint(1)` | 否 |  |  | 是否启用快递 | internal | business-field | semantic-review-required |
| 11 | `express_fee` | `decimal(10,2)` | 是 |  |  | 快递费用 | internal | business-field | semantic-review-required |
| 12 | `send_out_range` | `decimal(10,2)` | 否 |  |  | 配送范围 单位M | internal | business-field | semantic-review-required |
| 13 | `send_out_start_time` | `varchar(10)` | 是 |  |  | 配送开始时间 | internal | business-field | semantic-review-required |
| 14 | `send_out_end_time` | `varchar(10)` | 是 |  |  | 配送结束时间 | internal | business-field | semantic-review-required |
| 15 | `send_out_price` | `decimal(10,2)` | 是 |  |  | 配送费用 | internal | business-field | semantic-review-required |
| 16 | `start_price` | `decimal(10,2)` | 是 |  |  | 起送金额 | internal | business-field | semantic-review-required |
| 17 | `is_can_select_finish_time` | `tinyint(1)` | 否 |  |  | 是否可选送达时间 | internal | business-field | semantic-review-required |
| 18 | `except_finish_minute` | `int(11)` | 否 |  |  | 送达时间 | internal | business-field | semantic-review-required |
| 19 | `is_me_take` | `tinyint(1)` | 否 |  |  | 自提开关 | internal | business-field | semantic-review-required |
| 20 | `take_make_time` | `int(11)` | 否 |  |  | 自提冗余配货时长 单位/分钟 | internal | business-field | semantic-review-required |
| 21 | `discount` | `decimal(10,2)` | 是 |  |  | 门店折扣 | internal | business-field | semantic-review-required |
| 22 | `is_hide_vip_price` | `tinyint(1)` | 否 |  | 0 | 是否隐藏会员价 | internal | business-field | semantic-review-required |
| 23 | `is_open_lnventory_warning` | `tinyint(1)` | 否 |  |  | 是否开启库存预警 | internal | business-field | semantic-review-required |
| 24 | `lnventory_quantity` | `int(11)` | 否 |  |  | 预警库存数量 | internal | business-field | semantic-review-required |
| 25 | `is_lnventory_wechat_notice` | `tinyint(1)` | 否 |  |  | 库存预警微信通知 | internal | business-field | semantic-review-required |
| 26 | `is_lnventory_sms_notice` | `tinyint(1)` | 否 |  |  | 库存预警短信通知 | internal | business-field | semantic-review-required |
| 27 | `is_free_shipping` | `tinyint(1)` | 是 |  |  | 是否包邮 | internal | business-field | semantic-review-required |
| 28 | `tenant_id` | `int(11)` | 是 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 29 | `share_img` | `varchar(80)` | 是 |  |  | 分享图 | internal | business-field | semantic-review-required |
| 30 | `share_title` | `varchar(100)` | 是 |  |  | 分享标题 | internal | business-field | semantic-review-required |
| 31 | `is_hide_sale_sum` | `tinyint(1)` | 否 |  | 0 | 是否隐藏销售数据 | internal | business-field | semantic-review-required |
| 32 | `create_time` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_time` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 34 | `createby` | `int(11)` | 是 |  |  | 创建人uid | internal | business-field | semantic-review-required |
| 35 | `updateby` | `int(11)` | 是 |  |  | 修改人uid | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_sms_notice_set`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺短信通知设置

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | UNI |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `card_by` | `tinyint(1)` | 否 |  | 0 | 购卡通知 | internal | business-field | semantic-review-required |
| 4 | `card_consumption` | `tinyint(1)` | 否 |  | 0 | 卡消费通知 | internal | business-field | semantic-review-required |
| 5 | `card_maturity` | `tinyint(1)` | 否 |  |  | 卡到期提醒 | internal | business-field | semantic-review-required |
| 6 | `coupon_receive` | `tinyint(1)` | 否 |  | 0 | 优惠券领取 | internal | business-field | semantic-review-required |
| 7 | `coupon_maturity` | `tinyint(1)` | 否 |  | 0 | 优惠券到期 | internal | business-field | semantic-review-required |
| 8 | `integral_change` | `tinyint(1)` | 否 |  | 0 | 积分变动 | internal | business-field | semantic-review-required |
| 9 | `integral_maturity` | `tinyint(1)` | 否 |  | 0 | 积分到期 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 11 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `date` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：唯一 BTREE（store_id）

### `store_sms_send_log`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `task_id` | `int(11)` | 否 | MUL |  | 任务ID | internal | relation-key | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 会员卡卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `mobile` | `varchar(20)` | 否 |  |  | 手机号 | sensitive | business-field | masked-or-filter-only |
| 6 | `template_length` | `int(11)` | 否 |  | 0 | 短信长度 | internal | business-field | semantic-review-required |
| 7 | `sms_deduction` | `int(11)` | 否 |  | 0 | 扣费条数 | internal | business-field | semantic-review-required |
| 8 | `send_time` | `datetime` | 否 |  |  | 发送时间 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  |  | 状态 -5删除， -4取消发送 -3审核失败 -2 发送失败 - 1未审核，0未发送 1发送成功 | internal | business-field | semantic-review-required |
| 10 | `state_reason` | `varchar(100)` | 是 |  |  | 失败原因 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `ind_taskId`：非唯一 BTREE（task_id）

### `store_sms_send_task`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `sms_type` | `int(11)` | 否 |  |  |  短信类型（待定） | internal | business-field | semantic-review-required |
| 4 | `template_id` | `int(11)` | 否 |  |  | 短信模板id | internal | relation-key | server-filter-only |
| 5 | `tid` | `varchar(50)` | 是 |  |  | 短信平台模板id | internal | business-field | semantic-review-required |
| 6 | `is_market` | `tinyint(1)` | 否 |  |  | 是否营销 | internal | business-field | semantic-review-required |
| 7 | `sms_info` | `varchar(400)` | 否 |  |  | 短信内容 | internal | business-field | semantic-review-required |
| 8 | `sms_param` | `varchar(200)` | 是 |  |  | 短信参数 | internal | business-field | semantic-review-required |
| 9 | `marketing_id` | `int(11)` | 否 |  |  | 关联活动id | internal | relation-key | server-filter-only |
| 10 | `is_coupon` | `tinyint(1)` | 否 |  |  | 是否关联优惠券 | internal | business-field | semantic-review-required |
| 11 | `is_sent_coupon` | `tinyint(1)` | 否 |  | 0 | 是否已经发送过优惠券了 | internal | business-field | semantic-review-required |
| 12 | `state` | `int(11)` | 否 |  |  |  状态 -4 取消发送 -3审核失败 -2 发送失败 - 1未审核，0未发送 1发送成功 2发送中 | internal | business-field | semantic-review-required |
| 13 | `state_reason` | `varchar(100)` | 是 |  |  | 失败原因 | internal | business-field | semantic-review-required |
| 14 | `is_set_send_time` | `tinyint(1)` | 否 |  |  | 是否设置发送时间 | internal | business-field | semantic-review-required |
| 15 | `set_send_time` | `datetime` | 否 |  |  |  设置发送时间 | internal | business-field | semantic-review-required |
| 16 | `send_time` | `datetime` | 否 |  |  | 实际发送时间 | internal | business-field | semantic-review-required |
| 17 | `template_length` | `int(11)` | 否 |  |  |  长度 | internal | business-field | semantic-review-required |
| 18 | `sms_deduction` | `int(11)` | 否 |  |  | 扣费条数 | internal | business-field | semantic-review-required |
| 19 | `sms_sign` | `varchar(20)` | 否 |  |  | 短信签名 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 21 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 22 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 23 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 24 | `create_date` | `datetime` | 否 | MUL |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_createDate`：非唯一 BTREE（create_date）
- `inx_storeId`：非唯一 BTREE（store_id）

### `store_sms_template`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 | 为0 是系统默认模板 | internal | store-scope | server-filter-only |
| 3 | `root_id` | `int(11)` | 否 |  | 0 | 父级id | internal | relation-key | server-filter-only |
| 4 | `template_type` | `int(4)` | 否 |  |  | 模板类型 0验证码，1通知短信，2推广短信 | internal | business-field | semantic-review-required |
| 5 | `festival` | `int(4)` | 否 |  |  | 节日 | internal | business-field | semantic-review-required |
| 6 | `tid` | `varchar(20)` | 是 |  |  | 短信平台 模板id | internal | business-field | semantic-review-required |
| 7 | `template_name` | `varchar(50)` | 否 |  |  | 模板名称 | internal | business-field | semantic-review-required |
| 8 | `template_content` | `varchar(200)` | 否 |  |  | 模板内容 | sensitive-unstructured | business-field | deny |
| 9 | `template_param` | `varchar(200)` | 是 |  |  | 模板参数 | internal | business-field | semantic-review-required |
| 10 | `template_extension` | `varchar(200)` | 是 |  |  | 模板扩展 | internal | business-field | semantic-review-required |
| 11 | `remark` | `varchar(100)` | 是 |  |  | 记录审核未通过原因 | sensitive-unstructured | business-field | deny |
| 12 | `template_length` | `int(4)` | 否 |  |  | 长度 | internal | business-field | semantic-review-required |
| 13 | `sms_deduction` | `int(4)` | 否 |  |  | 扣费条数 | internal | business-field | semantic-review-required |
| 14 | `order_by` | `int(4)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 15 | `state` | `int(4)` | 否 |  | 0 | 状态 -1未通过，0审核中，1启用 | internal | business-field | semantic-review-required |
| 16 | `state_reason` | `varchar(50)` | 是 |  |  | 失败原因 | internal | business-field | semantic-review-required |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 | 商户ID | internal | tenant-scope | server-filter-only |
| 18 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 19 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 20 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 21 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_sms_template_copy1`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 | 为0 是系统默认模板 | internal | store-scope | server-filter-only |
| 3 | `root_id` | `int(11)` | 否 |  | 0 | 父级id | internal | relation-key | server-filter-only |
| 4 | `template_type` | `int(4)` | 否 |  |  | 模板类型 0验证码，1通知短信，2推广短信 | internal | business-field | semantic-review-required |
| 5 | `festival` | `int(4)` | 否 |  |  | 节日 | internal | business-field | semantic-review-required |
| 6 | `tid` | `varchar(20)` | 是 |  |  | 短信平台 模板id | internal | business-field | semantic-review-required |
| 7 | `template_name` | `varchar(50)` | 否 |  |  | 模板名称 | internal | business-field | semantic-review-required |
| 8 | `template_content` | `varchar(200)` | 否 |  |  | 模板内容 | sensitive-unstructured | business-field | deny |
| 9 | `template_param` | `varchar(200)` | 是 |  |  | 模板参数 | internal | business-field | semantic-review-required |
| 10 | `template_extension` | `varchar(200)` | 是 |  |  | 模板扩展 | internal | business-field | semantic-review-required |
| 11 | `remark` | `varchar(100)` | 是 |  |  | 记录审核未通过原因 | sensitive-unstructured | business-field | deny |
| 12 | `template_length` | `int(4)` | 否 |  |  | 长度 | internal | business-field | semantic-review-required |
| 13 | `sms_deduction` | `int(4)` | 否 |  |  | 扣费条数 | internal | business-field | semantic-review-required |
| 14 | `order_by` | `int(4)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 15 | `state` | `int(4)` | 否 |  | 0 | 状态 -1未通过，0审核中，1启用 | internal | business-field | semantic-review-required |
| 16 | `state_reason` | `varchar(50)` | 是 |  |  | 失败原因 | internal | business-field | semantic-review-required |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 | 商户ID | internal | tenant-scope | server-filter-only |
| 18 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 19 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 20 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 21 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_sms_template_copy2`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 | 为0 是系统默认模板 | internal | store-scope | server-filter-only |
| 3 | `root_id` | `int(11)` | 否 |  | 0 | 父级id | internal | relation-key | server-filter-only |
| 4 | `template_type` | `int(4)` | 否 |  |  | 模板类型 0验证码，1通知短信，2推广短信 | internal | business-field | semantic-review-required |
| 5 | `festival` | `int(4)` | 否 |  |  | 节日 | internal | business-field | semantic-review-required |
| 6 | `tid` | `varchar(20)` | 是 |  |  | 短信平台 模板id | internal | business-field | semantic-review-required |
| 7 | `template_name` | `varchar(50)` | 否 |  |  | 模板名称 | internal | business-field | semantic-review-required |
| 8 | `template_content` | `varchar(200)` | 否 |  |  | 模板内容 | sensitive-unstructured | business-field | deny |
| 9 | `template_param` | `varchar(200)` | 是 |  |  | 模板参数 | internal | business-field | semantic-review-required |
| 10 | `template_extension` | `varchar(200)` | 是 |  |  | 模板扩展 | internal | business-field | semantic-review-required |
| 11 | `remark` | `varchar(100)` | 是 |  |  | 记录审核未通过原因 | sensitive-unstructured | business-field | deny |
| 12 | `template_length` | `int(4)` | 否 |  |  | 长度 | internal | business-field | semantic-review-required |
| 13 | `sms_deduction` | `int(4)` | 否 |  |  | 扣费条数 | internal | business-field | semantic-review-required |
| 14 | `order_by` | `int(4)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 15 | `state` | `int(4)` | 否 |  | 0 | 状态 -1未通过，0审核中，1启用 | internal | business-field | semantic-review-required |
| 16 | `state_reason` | `varchar(50)` | 是 |  |  | 失败原因 | internal | business-field | semantic-review-required |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 | 商户ID | internal | tenant-scope | server-filter-only |
| 18 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 19 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 20 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 21 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_soft_discount`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：软件售卖优惠折扣操作表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增ID 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 门店ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 5 | `discount_tag` | `int(11)` | 是 |  |  | 1、直减 2、折扣 | internal | business-field | semantic-review-required |
| 6 | `discount_value` | `decimal(8,2)` | 是 |  |  | 操作值：如果是直减的话直接是 金额，如果是折扣 这里是百分比 | internal | business-field | semantic-review-required |
| 7 | `version_Tag` | `int(11)` | 是 |  |  | 软件版本标识:1老系统 2新系统 | internal | business-field | semantic-review-required |
| 8 | `version_id` | `int(11)` | 是 |  |  | 软件版本ID | internal | relation-key | server-filter-only |
| 9 | `create_uid` | `int(11)` | 是 |  |  | 操作人ID | internal | business-field | semantic-review-required |
| 10 | `creat_time` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0正常  1已删除 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_soft_module`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺软件模块

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  | 店铺的id | internal | store-scope | server-filter-only |
| 3 | `version_id` | `int(11)` | 否 |  |  | 版本id | internal | relation-key | server-filter-only |
| 4 | `soft_order_id` | `int(11)` | 是 |  |  | 订购表id | internal | relation-key | server-filter-only |
| 5 | `module_id` | `int(11)` | 是 |  |  | 模块的id | internal | relation-key | server-filter-only |
| 6 | `module_name` | `varchar(50)` | 是 |  |  | 模块的名称 | internal | business-field | semantic-review-required |
| 7 | `module_code` | `varchar(50)` | 是 |  |  | 模块的code | internal | business-field | semantic-review-required |
| 8 | `soft_module_id` | `int(11)` | 是 |  | 0 | 官方的模块的id | internal | relation-key | server-filter-only |
| 9 | `is_base` | `tinyint(1)` | 是 |  |  | 是否是基础功能包 | internal | business-field | semantic-review-required |
| 10 | `start_date` | `datetime` | 是 |  |  | 开始的时间 | internal | business-field | semantic-review-required |
| 11 | `end_date` | `datetime` | 是 |  |  | 结束的时间 | internal | business-field | semantic-review-required |
| 12 | `state` | `int(11)` | 是 |  |  | 状态；1-正常，0-关闭 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeid`：非唯一 BTREE（store_id）

### `store_soft_version_permission`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺的版本权限

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `is_member` | `tinyint(1)` | 否 |  |  | 会员权限 | internal | business-field | semantic-review-required |
| 4 | `is_reservation` | `tinyint(1)` | 否 |  |  | 预约权限 | internal | business-field | semantic-review-required |
| 5 | `is_marketing` | `tinyint(1)` | 否 |  |  | 营销权限 | internal | business-field | semantic-review-required |
| 6 | `is_performance` | `tinyint(1)` | 否 |  |  | 绩效权限 | internal | business-field | semantic-review-required |
| 7 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 商城权限 | internal | business-field | semantic-review-required |
| 8 | `is_distribution` | `tinyint(1)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 9 | `is_food` | `tinyint(1)` | 否 |  | 0 | 点餐 | internal | business-field | semantic-review-required |
| 10 | `max_mermber_count` | `int(11)` | 否 |  |  | 最高会员数量 0不限制 | internal | business-field | semantic-review-required |
| 11 | `max_clerk_count` | `int(11)` | 否 |  |  | 最高店员数量 0不限制 | internal | business-field | semantic-review-required |
| 12 | `max_tablecards_count` | `int(11)` | 否 |  |  | 赠送最大台牌数量 | internal | business-field | semantic-review-required |
| 13 | `state` | `int(11)` | 否 |  |  | 状态1  正常 | internal | business-field | semantic-review-required |
| 14 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_tag_group`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `tag_type` | `int(11)` | 否 |  |  | 0多选，1单选 | internal | business-field | semantic-review-required |
| 4 | `tag_group_name` | `varchar(20)` | 否 |  |  | 标签分组名称 | internal | business-field | semantic-review-required |
| 5 | `is_system` | `tinyint(1)` | 否 |  |  | 是否是系统 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0未启用 1正常 | internal | business-field | semantic-review-required |
| 8 | `order_by` | `int(11)` | 否 |  |  | 排序 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_type`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 店铺类别自增ID | internal | relation-key | server-filter-only |
| 2 | `store_type_name` | `varchar(50)` | 否 |  |  | 店铺类别名称 | internal | business-field | semantic-review-required |
| 3 | `store_type_id` | `varchar(10)` | 否 |  |  | 类ID | internal | relation-key | server-filter-only |
| 4 | `store_type_logo` | `varchar(200)` | 否 |  |  | 类logo | internal | business-field | semantic-review-required |
| 5 | `root_id` | `varchar(10)` | 否 |  |  | 父类ID | internal | relation-key | server-filter-only |
| 6 | `type_describe` | `varchar(200)` | 是 |  |  | 店铺行业分类描述 | internal | business-field | semantic-review-required |
| 7 | `is_resvation` | `tinyint(1)` | 否 |  |  | 是否预约 | internal | business-field | semantic-review-required |
| 8 | `is_ai` | `tinyint(1)` | 否 |  |  | 是否ai | internal | business-field | semantic-review-required |
| 9 | `is_leaf` | `tinyint(1)` | 否 |  | 1 | 是否是根类目 | internal | business-field | semantic-review-required |
| 10 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  | 1 | 0 停用  1正常 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_type_tag_relation`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_type_id` | `varchar(20)` | 否 |  |  | 店铺类型ID | internal | relation-key | server-filter-only |
| 3 | `tag_id` | `bigint(20)` | 否 |  | 0 | tagid | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 否 |  | 1 | 状态；0-禁用，1-启用 | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_user`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：店铺 会员信息

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 | MUL |  | 会员卡id | internal | subject-or-relation-key | server-filter-only |
| 3 | `uid` | `int(11)` | 否 | MUL |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 5 | `user_key` | `varchar(30)` | 否 |  |  | 用户信息key | internal | business-field | semantic-review-required |
| 6 | `user_value` | `varchar(300)` | 是 |  |  | 用户信息value | internal | business-field | semantic-review-required |
| 7 | `part_car_number` | `varchar(10)` | 是 |  |  | 车牌号数字部分 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `card_id`：非唯一 BTREE（card_id）
- `store_id`：唯一 BTREE（uid, user_key, card_id）
- `uid`：非唯一 BTREE（uid）

### `store_user_black_list`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id | internal | subject-or-relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 5 | `penalty_level` | `int(11)` | 否 |  |  | 惩罚等级 0禁止进入小程序 1禁止查看排课 2禁止约课 | internal | business-field | semantic-review-required |
| 6 | `penalty_date` | `datetime` | 是 |  |  | 惩罚时间 null永久 | internal | business-field | semantic-review-required |
| 7 | `log_note` | `varchar(100)` | 否 |  |  | 操作备注 | sensitive-unstructured | business-field | deny |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0黑名单失效 1黑名单生效中 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_user_black_list_log`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `black_id` | `bigint(20)` | 否 |  |  | 黑名单id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 会员卡id | internal | subject-or-relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 6 | `log_type` | `int(11)` | 否 |  |  | 日志类型 0加入黑名单 1移出黑名单 2修改黑名单信息 | internal | business-field | semantic-review-required |
| 7 | `operation_type` | `int(11)` | 否 |  |  | 操作类型 0系统操作 1管理员操作  | internal | business-field | semantic-review-required |
| 8 | `log_note` | `varchar(100)` | 否 |  |  | 操作备注 | sensitive-unstructured | business-field | deny |
| 9 | `penalty_level` | `int(11)` | 否 |  |  | 惩罚等级 0禁止进入小程序 1禁止查看排课 2禁止约课 | internal | business-field | semantic-review-required |
| 10 | `penalty_date` | `datetime` | 是 |  |  | 惩罚时间 null永久 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 12 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0黑名单失效 1黑名单生效中 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_user_permissions`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `pid` | `int(11)` | 否 |  |  | 权限id | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 状态 0不可用 1可用 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `store_id`：唯一 BTREE（store_id, uid, pid）

### `store_user_source_way_extend`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `source_way_name` | `varchar(255)` | 否 |  |  | 会员来源渠道名称 | internal | business-field | semantic-review-required |
| 4 | `tenant_id` | `bigint(20)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 5 | `state` | `int(11)` | 否 |  | 1 | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 6 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 7 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_vacation`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `begin_date` | `datetime` | 否 |  |  | 放假开始时间 | internal | business-field | semantic-review-required |
| 4 | `end_date` | `datetime` | 否 |  |  | 放假结束时间 | internal | business-field | semantic-review-required |
| 5 | `remark` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 6 | `vacation_message` | `text` | 是 |  |  | 放假公告信息 | sensitive-unstructured | business-field | deny |
| 7 | `card_extension` | `int(11)` | 否 |  | 0 | 会员卡延期 0不延期 | internal | business-field | semantic-review-required |
| 8 | `card_extension_days` | `int(11)` | 否 |  |  | 延期天数 | internal | business-field | semantic-review-required |
| 9 | `is_show_index` | `tinyint(1)` | 否 |  | 0 | 是否首页弹框展现 | internal | business-field | semantic-review-required |
| 10 | `is_vacation` | `tinyint(1)` | 否 |  |  | 是否开启放假（未开启放假只做公告功能展示） | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态  -1 删除  1正常 2过期3未开始 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 商户ID | internal | tenant-scope | server-filter-only |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 15 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 16 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_vacation_date`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `vacation_id` | `bigint(20)` | 否 |  |  | 放假id | internal | relation-key | server-filter-only |
| 4 | `vacation_date` | `date` | 否 |  |  | 请假日期 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_vacation_seting`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店员id | internal | store-scope | server-filter-only |
| 3 | `group_lesson_state` | `int(11)` | 否 |  |  | 团课状态 1正常 2停课 3隐藏展示公告 | internal | business-field | semantic-review-required |
| 4 | `private_lesson_state` | `int(11)` | 否 |  |  | 私教课状态 1正常 2停课 3隐藏展示公告 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_vacation_time`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `bigint(20)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `vacation_id` | `bigint(20)` | 否 |  |  | 放假id | internal | relation-key | server-filter-only |
| 4 | `begin_time` | `varchar(20)` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 5 | `end_time` | `varchar(20)` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_version`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `version_id` | `int(11)` | 否 |  |  | 版本id | internal | relation-key | server-filter-only |
| 4 | `version_type` | `int(11)` | 否 |  |  | 类型；0-软件，1-增值服务/年，2增值服务/终身 | internal | business-field | semantic-review-required |
| 5 | `service_end_date` | `date` | 是 |  |  | 到期日期 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 1生效 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_version_module`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：无。
表注释：店铺版本模块关联

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `soft_version` | `int(11)` | 是 |  |  | 版本 | internal | business-field | semantic-review-required |
| 3 | `function_id` | `int(11)` | 是 |  |  | 功能的id | internal | relation-key | server-filter-only |
| 4 | `state` | `int(11)` | 是 |  |  | 状态；1-正常，0-关闭 | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `store_workbench`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  |  | internal | store-scope | server-filter-only |
| 3 | `workbench_id` | `int(11)` | 是 |  |  | 工作台id | internal | relation-key | server-filter-only |
| 4 | `name` | `varchar(50)` | 是 |  |  | 名称 | internal | business-field | semantic-review-required |
| 5 | `module` | `varchar(50)` | 是 |  |  | 模块值 | internal | business-field | semantic-review-required |
| 6 | `type` | `int(11)` | 是 |  |  | 类型；0-小程序内部，1-外链，2-外部小程序，3-不跳转 | internal | business-field | semantic-review-required |
| 7 | `path` | `varchar(255)` | 是 |  |  | 跳转的内容 | internal | business-field | semantic-review-required |
| 8 | `data` | `varchar(255)` | 是 |  |  | 内容 | internal | business-field | semantic-review-required |
| 9 | `name_english` | `varchar(50)` | 是 |  |  | 英文的名称 | internal | business-field | semantic-review-required |
| 10 | `border_color` | `varchar(50)` | 是 |  |  | 边框的颜色 | internal | business-field | semantic-review-required |
| 11 | `font_chinese_color` | `varchar(50)` | 是 |  |  | 中文字体色 | internal | business-field | semantic-review-required |
| 12 | `font_english_color` | `varchar(50)` | 是 |  |  | 英文字体色 | internal | business-field | semantic-review-required |
| 13 | `background_color` | `varchar(100)` | 是 |  |  | 背景色 | internal | business-field | semantic-review-required |
| 14 | `right_bottom_img` | `varchar(100)` | 是 |  |  | 右下角的图 | internal | business-field | semantic-review-required |
| 15 | `sort` | `int(11)` | 是 |  |  | 排序 | internal | business-field | semantic-review-required |
| 16 | `state` | `int(11)` | 是 |  |  | 状态；1-开启，0-关闭 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 19 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 20 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 21 | `alipay_marketing_recruit_log` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 22 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `store_yop_config`

类型：BASE TABLE；引擎：InnoDB；领域：store-configuration；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `store_type` | `int(11)` | 否 |  | 1 | 商户类型 0个人 1个体 2企业 | internal | business-field | semantic-review-required |
| 4 | `store_industry` | `varchar(20)` | 是 |  |  | 商家行业 | internal | business-field | semantic-review-required |
| 5 | `store_email` | `varchar(50)` | 是 |  |  | 联系邮箱 | sensitive | business-field | masked-or-filter-only |
| 6 | `store_simple_name` | `varchar(30)` | 是 |  |  | 商户简称 | internal | business-field | semantic-review-required |
| 7 | `store_full_name` | `varchar(50)` | 是 |  |  | 商户全称 | internal | business-field | semantic-review-required |
| 8 | `store_merchant_code` | `varchar(50)` | 是 |  |  | 商户账号 | internal | business-field | semantic-review-required |
| 9 | `store_desc` | `varchar(300)` | 是 |  |  | 店铺描述 | internal | business-field | semantic-review-required |
| 10 | `legal_name` | `varchar(20)` | 是 |  |  | 法人姓名 | internal | business-field | semantic-review-required |
| 11 | `legal_id_card` | `varchar(20)` | 是 |  |  | 法人身份证 | restricted | business-field | deny |
| 12 | `beneficiary_name` | `varchar(20)` | 是 |  |  | 受益人姓名 | internal | business-field | semantic-review-required |
| 13 | `beneficiary_id_card` | `varchar(20)` | 是 |  |  | 受益人身份证 | restricted | business-field | deny |
| 14 | `mer_cert_type` | `varchar(20)` | 是 |  | UNI_CREDIT_CODE | 证件类型 UNI_CREDIT_CODE=统一社会信用代码证；CORP_CODE＝营业执照 | internal | business-field | semantic-review-required |
| 15 | `mer_cert_no` | `varchar(20)` | 是 |  |  | 证件号 所对应的证件类型的证件编号 | internal | business-field | semantic-review-required |
| 16 | `org_code` | `varchar(20)` | 是 |  |  | 组织机构代码证 | internal | business-field | semantic-review-required |
| 17 | `tax_regist_cert` | `varchar(20)` | 是 |  |  | 签约类型为“企业”，且证件类型为“营业执照”，则必填 | internal | business-field | semantic-review-required |
| 18 | `mer_contact_name` | `varchar(20)` | 是 |  |  | 商户联系人姓名 | sensitive | business-field | masked-or-filter-only |
| 19 | `mer_contact_phone` | `varchar(20)` | 是 |  |  | 商户联系人手机号 | sensitive | business-field | masked-or-filter-only |
| 20 | `mer_province` | `varchar(20)` | 是 |  |  | 商户省 | internal | business-field | semantic-review-required |
| 21 | `mer_city` | `varchar(20)` | 是 |  |  | 商户市 | internal | business-field | semantic-review-required |
| 22 | `mer_district` | `varchar(20)` | 是 |  |  | 商户区 | internal | business-field | semantic-review-required |
| 23 | `mer_address` | `varchar(50)` | 是 |  |  | 商户详细地址 | sensitive | business-field | masked-or-filter-only |
| 24 | `account_license` | `varchar(20)` | 是 |  |  | 开户许可证编号 | sensitive | business-field | masked-or-filter-only |
| 25 | `card_no` | `varchar(25)` | 是 |  |  | 结算银行账号或者银行卡号 | internal | business-field | semantic-review-required |
| 26 | `bank_province` | `varchar(20)` | 是 |  |  | 开户省 | internal | business-field | semantic-review-required |
| 27 | `bank_city` | `varchar(20)` | 是 |  |  | 开户市 | internal | business-field | semantic-review-required |
| 28 | `bank_district` | `varchar(20)` | 是 |  |  | 开户区 | internal | business-field | semantic-review-required |
| 29 | `mer_card_no` | `varchar(20)` | 是 |  |  | 小微卡号 | internal | business-field | semantic-review-required |
| 30 | `mer_bank_province` | `varchar(20)` | 是 |  |  | 小微开户省 | internal | business-field | semantic-review-required |
| 31 | `mer_bank_city` | `varchar(20)` | 是 |  |  | 小微开户市 | internal | business-field | semantic-review-required |
| 32 | `mer_bank_district` | `varchar(20)` | 是 |  |  | 小微开户区县 | internal | business-field | semantic-review-required |
| 33 | `mer_idcard_date_start` | `varchar(20)` | 是 |  |  | 法人身份证有效期开始时间 | internal | business-field | semantic-review-required |
| 34 | `mer_idcard_date_end` | `varchar(20)` | 是 |  |  | 法人身份证有效期结束时间 | internal | business-field | semantic-review-required |
| 35 | `beneficiary_idcard_date_start` | `varchar(20)` | 是 |  |  | 受益人身份证有效期开始时间 | internal | business-field | semantic-review-required |
| 36 | `beneficiary_idcard_date_end` | `varchar(20)` | 是 |  |  | 受益人身份证有效期结束时间 | internal | business-field | semantic-review-required |
| 37 | `mer_corp_date_start` | `varchar(20)` | 是 |  |  | 营业执照有效期开始时间 | internal | business-field | semantic-review-required |
| 38 | `mer_corp_date_end` | `varchar(20)` | 是 |  |  | 营业执照有效期结束时间 | internal | business-field | semantic-review-required |
| 39 | `img_idcard_fornt` | `varchar(100)` | 是 |  |  | 身份证正面照片 | internal | business-field | semantic-review-required |
| 40 | `img_idcard_back` | `varchar(100)` | 是 |  |  | 法人身份证反面 | internal | business-field | semantic-review-required |
| 41 | `img_beneficiary_idcard_fornt` | `varchar(100)` | 是 |  |  | 受益人身份证正面 | internal | business-field | semantic-review-required |
| 42 | `img_beneficiary_idcard_back` | `varchar(100)` | 是 |  |  | 受益人身份证反面 | internal | business-field | semantic-review-required |
| 43 | `img_uni_credit_code` | `varchar(100)` | 是 |  |  | 统一社会信用代码证 | internal | business-field | semantic-review-required |
| 44 | `img_corp_code` | `varchar(100)` | 是 |  |  | 营业执照照片 | internal | business-field | semantic-review-required |
| 45 | `img_tax_code` | `varchar(100)` | 是 |  |  | 税务登记证 | internal | business-field | semantic-review-required |
| 46 | `img_org_code` | `varchar(100)` | 是 |  |  | 组织机构代码证 | internal | business-field | semantic-review-required |
| 47 | `img_op_bank_code` | `varchar(100)` | 是 |  |  | 银行开户许可证 | internal | business-field | semantic-review-required |
| 48 | `img_bank_card` | `varchar(100)` | 是 |  |  | 结算银行卡 | restricted | business-field | deny |
| 49 | `img_hand_idcard` | `varchar(100)` | 是 |  |  | 手持身份证 | internal | business-field | semantic-review-required |
| 50 | `img_hand_bank_card` | `varchar(100)` | 是 |  |  | 手持银行卡 | restricted | business-field | deny |
| 51 | `img_shop_photo` | `varchar(100)` | 是 |  |  | 门头照 | internal | business-field | semantic-review-required |
| 52 | `img_cashier_scene` | `varchar(100)` | 是 |  |  | 收银台场景照 | internal | business-field | semantic-review-required |
| 53 | `img_transaction_invoice` | `varchar(100)` | 是 |  |  | 近 3 个月 内交易发票 | internal | business-field | semantic-review-required |
| 54 | `img_panoramic` | `varchar(100)` | 是 |  |  | 店内全景照片 | internal | business-field | semantic-review-required |
| 55 | `img_store_corp_code` | `varchar(100)` | 是 |  |  | 店内包含营业执照照片 | internal | business-field | semantic-review-required |
| 56 | `img_hand_corp_code` | `varchar(100)` | 是 |  |  | 手持营业执照的门头照合影 | internal | business-field | semantic-review-required |
| 57 | `img_confirmation` | `varchar(100)` | 是 |  |  | 确认书 | internal | business-field | semantic-review-required |
| 58 | `is_public_to_private` | `tinyint(1)` | 是 |  | 0 | 是否是公对私 | internal | business-field | semantic-review-required |
| 59 | `mer_chant_no` | `varchar(20)` | 是 |  |  | 宜宝商户编号 | internal | business-field | semantic-review-required |
| 60 | `is_up_grade` | `tinyint(1)` | 否 |  | 0 | false 未升级 1已升级 | internal | business-field | semantic-review-required |
| 61 | `is_owner` | `tinyint(1)` | 否 |  | 0 | 法人是否受益人，如不是需要传受益人身份信息 | internal | business-field | semantic-review-required |
| 62 | `is_admin_show` | `tinyint(1)` | 否 |  | 1 | 0不在后台显示，1在后台显示 | internal | business-field | semantic-review-required |
| 63 | `is_confirm` | `tinyint(1)` | 是 |  | 0 | 是否点击了已确认完成 | internal | business-field | semantic-review-required |
| 64 | `state` | `int(11)` | 否 |  | -1 | 状态 0审核 1通过审核（已签约） -1 未填写 -2回退 -3未通过审核，10 开通支付 | internal | business-field | semantic-review-required |
| 65 | `report_state` | `int(11)` | 否 |  | -1 | 聚合报备状态 0审核 1通过审核 -1 未填写 -2回退 -3未通过审核 | internal | business-field | semantic-review-required |
| 66 | `note` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 67 | `admin_remark` | `varchar(100)` | 是 |  |  | 管理员对商户的备注 | sensitive-unstructured | business-field | deny |
| 68 | `ali_shop_category` | `varchar(50)` | 是 |  |  | 阿里店铺分类 | internal | business-field | semantic-review-required |
| 69 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 70 | `open_date` | `datetime` | 是 |  |  | 开户时间 | internal | business-field | semantic-review-required |
| 71 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 72 | `business_code` | `varchar(128)` | 是 |  |  | 编号 | internal | business-field | semantic-review-required |
| 73 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `sys_message`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：tenant_id, store_id。
表注释：系统消息

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `mess_title` | `varchar(100)` | 是 |  |  | 标题 | internal | business-field | semantic-review-required |
| 3 | `mess_info` | `varchar(300)` | 是 |  |  | 消息内容 | internal | business-field | semantic-review-required |
| 4 | `mess_img` | `varchar(100)` | 是 |  |  | 主图 | internal | business-field | semantic-review-required |
| 5 | `mess_type` | `int(11)` | 否 |  |  | 消息类型 0系统消息，1商户消息 2语音设置 3活动消息 | internal | business-field | semantic-review-required |
| 6 | `mess_range` | `int(11)` | 否 |  |  | 推送范围 0所有，1关联关系 | internal | business-field | semantic-review-required |
| 7 | `activity_id` | `int(11)` | 否 |  | 0 | 活动id | internal | relation-key | server-filter-only |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `store_id` | `int(11)` | 否 |  |  | 商户id | internal | store-scope | server-filter-only |
| 10 | `create_by` | `int(11)` | 是 |  |  | 创建人 0系统 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `send_date` | `datetime` | 是 |  |  | 发送时间 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 15 | `state` | `int(11)` | 是 |  |  | 状态 -1删除 0未发送 1已发送 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `tenant`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `tenant_name` | `varchar(20)` | 是 |  |  | 租户名称 | internal | business-field | semantic-review-required |
| 3 | `founder` | `int(11)` | 否 |  |  | 创始人 | internal | business-field | semantic-review-required |
| 4 | `validity_date` | `datetime` | 是 |  |  | 有效期 | internal | business-field | semantic-review-required |
| 5 | `store_max_count` | `int(11)` | 否 |  | 1 | 最大店铺数量 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 租户状态 1正常，0停用，-1删除 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `tenant_user`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：tenant_id, store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `user_name` | `varchar(20)` | 是 |  |  | 员工姓名 | sensitive | business-field | masked-or-filter-only |
| 5 | `user_img` | `varchar(100)` | 是 |  |  | 员工头像 | internal | business-field | semantic-review-required |
| 6 | `user_tag` | `varchar(20)` | 是 |  |  | 员工标记，用于手机号 | internal | business-field | semantic-review-required |
| 7 | `user_id` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 8 | `user_type` | `int(11)` | 否 |  |  | 用户权限租：0超级管理员，1管理员，2运营人员,3店员 | internal | business-field | semantic-review-required |
| 9 | `is_admin` | `tinyint(1)` | 否 |  | 0 | 是否是管理员 | internal | business-field | semantic-review-required |
| 10 | `is_reservation` | `tinyint(1)` | 否 |  | 0 | 是否是教练 | internal | business-field | semantic-review-required |
| 11 | `is_rider` | `tinyint(1)` | 否 |  | 0 | 是否是骑手 | internal | business-field | semantic-review-required |
| 12 | `job_title` | `varchar(20)` | 否 |  |  | 职称 | internal | business-field | semantic-review-required |
| 13 | `privilege_group_id` | `bigint(20)` | 否 |  |  | 权限组id | internal | relation-key | server-filter-only |
| 14 | `note` | `varchar(50)` | 否 |  |  | 用户备注 | sensitive-unstructured | business-field | deny |
| 15 | `is_voice` | `int(11)` | 否 |  | 0 | 是否收取语音消息 | internal | business-field | semantic-review-required |
| 16 | `is_notice` | `tinyint(1)` | 否 |  | 0 | 是否开启推送通知 | internal | business-field | semantic-review-required |
| 17 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 18 | `last_date` | `datetime` | 否 |  |  | 最后操作时间 | internal | business-field | semantic-review-required |
| 19 | `work_wechat_user_id` | `varchar(50)` | 是 |  |  | 企业微信员工id | internal | relation-key | server-filter-only |
| 20 | `is_recommend` | `tinyint(1)` | 否 |  | 1 | 是否推荐，用作首页展示 | internal | business-field | semantic-review-required |
| 21 | `order_by` | `int(11)` | 否 |  | 0 | 排序 | internal | business-field | semantic-review-required |
| 22 | `state` | `int(11)` | 否 |  |  | 状态：1启用 0离职 -1删除 | internal | business-field | semantic-review-required |
| 23 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 24 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 25 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 26 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）
- `idx_tenantId`：非唯一 BTREE（tenant_id）
- `idx_uid`：非唯一 BTREE（user_id）

### `tenant_user_image`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `staff_id` | `bigint(20)` | 否 |  |  | 店员id | internal | subject-or-relation-key | server-filter-only |
| 3 | `user_id` | `bigint(20)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `staff_img` | `varchar(100)` | 否 |  |  | 图片地址 | internal | business-field | semantic-review-required |
| 5 | `order_by` | `int(11)` | 否 |  |  | 排序倒序 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `tenant_user_info`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：tenant_id。
表注释：店员详情

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `staff_id` | `bigint(20)` | 否 |  |  | 店员id | internal | subject-or-relation-key | server-filter-only |
| 3 | `user_id` | `bigint(20)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `staff_specialise` | `text` | 是 |  |  | 店员擅长 | internal | business-field | semantic-review-required |
| 5 | `staff_experience` | `text` | 是 |  |  | 经历 | internal | business-field | semantic-review-required |
| 6 | `staff_honour` | `text` | 是 |  |  | 荣誉 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `tenant_user_tag_relation`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `staff_id` | `bigint(20)` | 否 |  |  | 店员id | internal | subject-or-relation-key | server-filter-only |
| 3 | `user_id` | `bigint(20)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `tag_type` | `int(11)` | 否 |  |  | 标签类型：1个人标签 2擅长 | internal | business-field | semantic-review-required |
| 5 | `tag_id` | `bigint(20)` | 否 |  |  | 标签id | internal | relation-key | server-filter-only |
| 6 | `order_by` | `int(11)` | 否 |  |  | 排序倒序 | internal | business-field | semantic-review-required |
| 7 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `bigint(20)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `bigint(20)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `three_authorizer_info`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：tenant_id, store_id。
表注释：三方公众号、小程序授权信息

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `appid` | `varchar(255)` | 是 |  |  | 授权方AppId | internal | business-field | semantic-review-required |
| 3 | `app_type` | `int(11)` | 否 |  |  | app类型 0自建 1代开发 2三方应用 | internal | business-field | semantic-review-required |
| 4 | `tenant_id` | `int(11)` | 是 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 5 | `store_id` | `int(11)` | 是 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `account_type` | `int(11)` | 是 |  |  | 账号类型，0：小程序，1：公众号，2企微助手，3企微小程序 | internal | business-field | semantic-review-required |
| 7 | `principal_name` | `varchar(255)` | 是 |  |  | 授权方主体名称 | internal | business-field | semantic-review-required |
| 8 | `refresh_token` | `varchar(255)` | 是 |  |  | 刷新Token | restricted | business-field | deny |
| 9 | `nick_name` | `varchar(255)` | 是 |  |  | 昵称 | internal | business-field | semantic-review-required |
| 10 | `head_img` | `varchar(255)` | 是 |  |  | 头像 | internal | business-field | semantic-review-required |
| 11 | `agent_id` | `varchar(100)` | 是 |  |  | 应用id | internal | relation-key | server-filter-only |
| 12 | `permanent_code` | `varchar(255)` | 是 |  |  | 永久授权码 | internal | business-field | semantic-review-required |
| 13 | `template_id` | `int(11)` | 否 |  | 0 | 模板id | internal | relation-key | server-filter-only |
| 14 | `current_version` | `varchar(255)` | 是 |  | 0.01 | 当前版本 | internal | business-field | semantic-review-required |
| 15 | `state` | `int(11)` | 否 |  | 5 | 状态，0：取消授权 1：已授权 | internal | business-field | semantic-review-required |
| 16 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 17 | `audit_state` | `int(11)` | 否 |  | 5 | 状态   0：待上传代码 1：已授权 2:审核中   3:审核被拒绝  4审核成功  5:已撤销审核 6： 待提交审核   7 已下架 | internal | business-field | semantic-review-required |
| 18 | `update_date` | `datetime` | 是 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 19 | `user_name` | `varchar(255)` | 是 |  |  | 用户名 | sensitive | business-field | masked-or-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `trade`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `seller_id` | `int(11)` | 是 |  | 0 | 卖家id | internal | relation-key | server-filter-only |
| 3 | `buyer_id` | `int(11)` | 否 |  |  | 买家id | internal | relation-key | server-filter-only |
| 4 | `total_price` | `decimal(6,2)` | 否 |  |  | 订单总金额 | internal | business-field | semantic-review-required |
| 5 | `discount_price` | `decimal(6,2)` | 否 |  | 0.00 | 优惠金额 | internal | business-field | semantic-review-required |
| 6 | `post_price` | `decimal(6,2)` | 否 |  | 0.00 | 邮费 | internal | business-field | semantic-review-required |
| 7 | `pay_price` | `decimal(6,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 8 | `receiver_name` | `varchar(50)` | 否 |  |  | 收件人姓名 | internal | business-field | semantic-review-required |
| 9 | `receiver_country` | `varchar(20)` | 是 |  |  | 收货人国籍 | internal | business-field | semantic-review-required |
| 10 | `receiver_state` | `varchar(20)` | 否 |  |  | 收货人的所在省份 | internal | business-field | semantic-review-required |
| 11 | `receiver_city` | `varchar(20)` | 否 |  |  | 收货人的所在城市 | internal | business-field | semantic-review-required |
| 12 | `receiver_district` | `varchar(20)` | 否 |  |  | 收货人的所在地区 | internal | business-field | semantic-review-required |
| 13 | `receiver_address` | `varchar(200)` | 否 |  |  | 收货人的详细地址 | sensitive | business-field | masked-or-filter-only |
| 14 | `receiver_zip` | `varchar(10)` | 是 |  |  | 收货人的邮编 | internal | business-field | semantic-review-required |
| 15 | `receiver_mobile` | `varchar(20)` | 否 |  |  | 收货人的手机号码 | sensitive | business-field | masked-or-filter-only |
| 16 | `receiver_phone` | `varchar(20)` | 是 |  |  | 收货人的电话号码 | sensitive | business-field | masked-or-filter-only |
| 17 | `buyer_message` | `varchar(50)` | 是 |  |  | 买家留言 | sensitive-unstructured | business-field | deny |
| 18 | `seller_memo` | `varchar(50)` | 是 |  |  | 卖家备注 | internal | business-field | semantic-review-required |
| 19 | `seller_flag` | `int(11)` | 是 |  | 0 | 卖家备注旗帜 | internal | business-field | semantic-review-required |
| 20 | `p_num` | `int(11)` | 否 |  | 0 | 商品数量 | internal | business-field | semantic-review-required |
| 21 | `pay_type` | `int(11)` | 否 |  |  | 支付方式0预留 1微信 2支付宝 | internal | business-field | semantic-review-required |
| 22 | `state` | `int(11)` | 是 |  |  | 订单状态：0未付款，1已付款未发货，2已发货，3交易成功,4取消 | internal | business-field | semantic-review-required |
| 23 | `logistics_company` | `varchar(10)` | 是 |  |  | 物流公司 | internal | business-field | semantic-review-required |
| 24 | `logistics_no` | `varchar(20)` | 是 |  |  | 物流单号 | internal | business-field | semantic-review-required |
| 25 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 26 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `transfer_admin_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 转让者 | internal | subject-or-relation-key | server-filter-only |
| 5 | `transfer_uid` | `int(11)` | 否 |  |  | 受让者 | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 否 |  |  | 状态：0取消 1记录 2不记录 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `trial_user_record`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  |  | internal | store-scope | server-filter-only |
| 3 | `login_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 4 | `root_id` | `int(11)` | 是 |  |  |  | internal | relation-key | server-filter-only |
| 5 | `contact_id` | `int(11)` | 是 |  |  |  | sensitive | relation-key | server-filter-only |
| 6 | `contact_people` | `varchar(255)` | 是 |  |  |  | sensitive | business-field | masked-or-filter-only |
| 7 | `contac_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `return_visit_type` | `int(11)` | 是 |  |  | 回访状态；0-待联系，1-已联系，2-无需联系，3-待再联系 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(255)` | 是 |  |  |  | sensitive-unstructured | business-field | deny |
| 10 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `Index_storeid_logindate`：非唯一 BTREE（store_id, login_date）
- `PRIMARY`：唯一 BTREE（id）

### `user_account`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：用户账户余额

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `user_money` | `decimal(6,2)` | 否 |  |  | 当前余额 | internal | business-field | semantic-review-required |
| 4 | `user_integral` | `int(11)` | 否 |  |  | 当前剩余积分 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_card`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 卡id | internal | subject-or-relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_number` | `varchar(30)` | 否 |  |  | 卡号 | sensitive | business-field | masked-or-filter-only |
| 6 | `card_img` | `varchar(100)` | 是 |  |  | 背景图片 | internal | business-field | semantic-review-required |
| 7 | `card_type` | `int(11)` | 是 |  |  | 类型：0计次，1储值 | internal | business-field | semantic-review-required |
| 8 | `card_name` | `varchar(20)` | 是 |  |  | 卡名称 | internal | business-field | semantic-review-required |
| 9 | `validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  | 1.00 | 会员卡折扣 | internal | business-field | semantic-review-required |
| 11 | `card_num` | `int(11)` | 否 |  |  | 剩余次数 | internal | business-field | semantic-review-required |
| 12 | `card_price` | `decimal(10,2)` | 是 |  |  | 剩余金额 | internal | business-field | semantic-review-required |
| 13 | `card_integral` | `int(11)` | 否 |  |  | 积分 | internal | business-field | semantic-review-required |
| 14 | `card_print` | `int(11)` | 否 |  |  | 印章 | internal | business-field | semantic-review-required |
| 15 | `commission` | `decimal(10,2)` | 否 |  | 0.00 | 佣金 | internal | business-field | semantic-review-required |
| 16 | `consumption_num` | `int(11)` | 否 |  |  | 消费次数 | internal | business-field | semantic-review-required |
| 17 | `consumption_price` | `decimal(10,2)` | 否 |  |  | 消费金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_integral` | `int(11)` | 否 |  |  | 消费积分 | internal | business-field | semantic-review-required |
| 19 | `consumption_print` | `int(11)` | 否 |  |  | 消费印章 | internal | business-field | semantic-review-required |
| 20 | `consumption_commission` | `decimal(10,2)` | 否 |  | 0.00 | 已消费佣金 | internal | business-field | semantic-review-required |
| 21 | `card_tag` | `varchar(20)` | 是 | MUL |  | 线下卡绑定标志，默认手机号 | internal | business-field | semantic-review-required |
| 22 | `total_money` | `decimal(10,2)` | 否 |  |  | 总计消费金额 | internal | business-field | semantic-review-required |
| 23 | `total_num` | `int(11)` | 否 |  |  | 总计消费次数 | internal | business-field | semantic-review-required |
| 24 | `remark_name` | `varchar(20)` | 是 |  |  | 商家备注名 | sensitive-unstructured | business-field | deny |
| 25 | `name_group` | `varchar(10)` | 是 |  |  | 会员名首字母（优先级 备注名 真实姓名 用户昵称） | internal | business-field | semantic-review-required |
| 26 | `send_message_date` | `datetime` | 是 |  |  | 发送关联会员卡短信的时间 | sensitive-unstructured | business-field | deny |
| 27 | `is_sent_message` | `tinyint(1)` | 否 |  | 0 | 是否已经发送过关联卡的短信 | sensitive-unstructured | business-field | deny |
| 28 | `store_user_no` | `int(11)` | 否 |  | 0 | 第多少位顾客 | internal | business-field | semantic-review-required |
| 29 | `open_date` | `datetime` | 否 |  |  | 开卡时间 | internal | business-field | semantic-review-required |
| 30 | `last_date` | `datetime` | 是 |  |  | 最后一次消费日期 | internal | business-field | semantic-review-required |
| 31 | `card_pass` | `varchar(255)` | 是 |  |  | 卡密码 | internal | business-field | semantic-review-required |
| 32 | `is_experience` | `tinyint(1)` | 否 |  | 0 | 是否是体验会员 | internal | business-field | semantic-review-required |
| 33 | `staff_id` | `bigint(20)` | 否 |  | 0 | 店员id(销售顾问) | internal | subject-or-relation-key | server-filter-only |
| 34 | `source_type` | `int(11)` | 否 |  | 0 | 来源类型 0无 1特定渠道 1其他会员推荐 | internal | business-field | semantic-review-required |
| 35 | `source_way_id` | `bigint(20)` | 否 |  | 0 | 来源渠道 | internal | relation-key | server-filter-only |
| 36 | `wx_card_state` | `int(11)` | 否 |  | 0 | 微信卡包会员卡状态 0未领卡 1已领卡 | internal | business-field | semantic-review-required |
| 37 | `is_sign_agreement` | `tinyint(1)` | 否 |  | 0 | 是否签署协议 | internal | business-field | semantic-review-required |
| 38 | `tenant_id` | `int(11)` | 是 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 39 | `state` | `int(11)` | 否 |  |  | 1正常 0未开卡 -1 销卡 -2商家删除 -3绑定店铺会员移除散客会员信息 | internal | business-field | semantic-review-required |
| 40 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 41 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 42 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 43 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_cardTag`：非唯一 BTREE（card_tag）
- `idx_tenantId`：非唯一 BTREE（tenant_id）
- `index_storeId`：非唯一 BTREE（store_id）
- `uid_index`：非唯一 BTREE（uid）

### `user_card_agreement`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 卡id | internal | subject-or-relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `agreement_id` | `bigint(20)` | 否 |  |  | 协议id | internal | relation-key | server-filter-only |
| 6 | `sgin_file` | `varchar(100)` | 否 |  |  | 签名文件 | internal | business-field | semantic-review-required |
| 7 | `agreement_file` | `varchar(100)` | 是 |  |  | 协议生成文件 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `bigint(20)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `state` | `int(11)` | 否 |  |  | 1正常 0未开卡 -1 销卡 -2商家删除 -3绑定店铺会员移除散客会员信息 | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_card_child`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `prepaid_card_id` | `int(11)` | 否 |  |  | 卡id(储值卡) | restricted | relation-key | deny |
| 4 | `prepaid_card_child_id` | `int(11)` | 否 |  | 0 | 储值子卡ID | restricted | relation-key | deny |
| 5 | `card_id` | `int(11)` | 否 | MUL |  | 主卡id | internal | subject-or-relation-key | server-filter-only |
| 6 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 7 | `card_number` | `varchar(30)` | 否 | MUL |  | 卡号 | sensitive | business-field | masked-or-filter-only |
| 8 | `card_img` | `varchar(100)` | 是 |  |  | 背景图片 | internal | business-field | semantic-review-required |
| 9 | `card_type` | `int(11)` | 是 |  |  | 类型：0计次，1储值 2 限时卡 3权益卡 4安心充 5课时卡 | internal | business-field | semantic-review-required |
| 10 | `card_name` | `varchar(20)` | 是 |  |  | 卡名称 | internal | business-field | semantic-review-required |
| 11 | `validity_date` | `date` | 是 | MUL |  | 到期时间 | internal | business-field | semantic-review-required |
| 12 | `card_discount` | `decimal(3,2)` | 是 |  |  | 会员卡折扣 | internal | business-field | semantic-review-required |
| 13 | `card_price` | `decimal(10,2)` | 否 |  | 0.00 | 剩余金额(次数) | internal | business-field | semantic-review-required |
| 14 | `card_normal_price` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 15 | `card_give_price` | `decimal(10,2)` | 否 |  | 0.00 | 剩余赠送金额(次数) | internal | business-field | semantic-review-required |
| 16 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 消费金额(次数) | internal | business-field | semantic-review-required |
| 17 | `card_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 总计折扣金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_price` | `decimal(10,2)` | 否 |  | 0.00 | 消费金额(次数) | internal | business-field | semantic-review-required |
| 19 | `card_tag` | `varchar(20)` | 是 |  |  | 线下卡绑定标志，默认手机号 | internal | business-field | semantic-review-required |
| 20 | `total_num` | `int(11)` | 是 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 21 | `single_max_frequency` | `int(11)` | 否 |  | 0 | 单次最大次数 0不限 | internal | business-field | semantic-review-required |
| 22 | `day_max_frequency` | `int(11)` | 否 |  | 0 | 每日最大核销次数 0不限 (1限制代约.) | internal | business-field | semantic-review-required |
| 23 | `week_max_frequency` | `int(11)` | 否 |  | 0 | 每周最大核销次数 0不限 | internal | business-field | semantic-review-required |
| 24 | `mouth_max_frequency` | `int(11)` | 否 |  | 0 | 每月最大核销次数 0不限 | internal | business-field | semantic-review-required |
| 25 | `is_limit_time` | `tinyint(1)` | 否 |  | 0 | 是否限制可用时段 | internal | business-field | semantic-review-required |
| 26 | `stop_frequency` | `int(11)` | 否 |  | 0 | 停卡次数 | internal | business-field | semantic-review-required |
| 27 | `open_card_date` | `datetime` | 是 |  |  | 开卡日期 | internal | business-field | semantic-review-required |
| 28 | `wx_card_state` | `int(11)` | 否 |  | 0 | 微信卡包会员卡状态 0未领卡 1已领卡 | internal | business-field | semantic-review-required |
| 29 | `wx_card_id` | `varchar(50)` | 是 |  |  | 微信卡包ID | internal | relation-key | server-filter-only |
| 30 | `al_card_state` | `int(11)` | 是 |  | 0 | 支付宝卡包会员卡状态 0未领卡 1已领卡 | internal | business-field | semantic-review-required |
| 31 | `al_card_id` | `varchar(50)` | 是 |  |  | 支付宝卡包ID | internal | relation-key | server-filter-only |
| 32 | `is_limit_frequency` | `tinyint(1)` | 否 |  | 0 | 是否显示次数 | internal | business-field | semantic-review-required |
| 33 | `is_use_audit` | `tinyint(1)` | 否 |  |  | 是否使用审核 | internal | business-field | semantic-review-required |
| 34 | `transfer_count` | `int(11)` | 否 |  |  | 转让次数 | internal | business-field | semantic-review-required |
| 35 | `source_id` | `int(11)` | 否 |  |  | 初始id | internal | relation-key | server-filter-only |
| 36 | `is_alliance_card` | `tinyint(1)` | 否 |  | 0 | 是否为联盟卡 | internal | business-field | semantic-review-required |
| 37 | `open_date` | `datetime` | 是 |  |  | 开卡时间 | internal | business-field | semantic-review-required |
| 38 | `last_date` | `datetime` | 是 |  |  | 最后一次消费日期 | internal | business-field | semantic-review-required |
| 39 | `unit_price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 40 | `use_max_count` | `decimal(10,2)` | 否 |  | -1.00 | 最大使用次数 | internal | business-field | semantic-review-required |
| 41 | `state` | `int(11)` | 否 |  |  | -4转让 hebing，-3过期续费删除 ， -2商家删除 -1 销卡 ，0未开卡，1正常 ， 2 已过期， 3停卡,4转卡中 | internal | business-field | semantic-review-required |
| 42 | `tenant_id` | `int(11)` | 是 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 43 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 44 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 45 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 46 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `card_id`：非唯一 BTREE（card_id）
- `idx_cardNumber`：非唯一 BTREE（card_number）
- `idx_storeId`：非唯一 BTREE（store_id）
- `idx_tenantId`：非唯一 BTREE（tenant_id）
- `idx_uid`：非唯一 BTREE（uid）
- `idx_validityDay`：非唯一 BTREE（validity_date）

### `user_card_child_liability`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `card_id` | `int(11)` | 否 |  |  | 主卡id | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_child_id` | `int(11)` | 否 |  |  | 子卡id | internal | relation-key | server-filter-only |
| 6 | `prepaid_card_id` | `int(11)` | 否 |  |  | 卡id(储值卡) | restricted | relation-key | deny |
| 7 | `card_type` | `int(11)` | 是 |  |  | 类型：0计次，1储值 2 限时卡 3权益卡 4安心充 5课时卡 | internal | business-field | semantic-review-required |
| 8 | `validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 9 | `card_price` | `decimal(10,2)` | 否 |  | 0.00 | 剩余金额(次数) | internal | business-field | semantic-review-required |
| 10 | `card_normal_price` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 11 | `card_give_price` | `decimal(10,2)` | 否 |  | 0.00 | 剩余赠送金额(次数) | internal | business-field | semantic-review-required |
| 12 | `card_lability` | `decimal(10,2)` | 否 |  |  | 负债 | internal | business-field | semantic-review-required |
| 13 | `state` | `int(11)` | 否 |  |  | -4转让 hebing，-3过期续费删除 ， -2商家删除 -1 销卡 ，0未开卡，1正常 ， 2 已过期， 3停卡,4转卡中 | internal | business-field | semantic-review-required |
| 14 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 15 | `lability_date` | `date` | 否 |  |  | 负债月份 | internal | business-field | semantic-review-required |
| 16 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_card_commission_trigger_log`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 是 |  |  |  | internal | subject-or-relation-key | server-filter-only |
| 3 | `old_commission` | `decimal(10,2)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 4 | `new_commission` | `decimal(10,2)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 5 | `old_consumption_commission` | `decimal(10,2)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `new_consumption_commission` | `decimal(10,2)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `old_last_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `new_last_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_card_operation_log`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：会员卡操作记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  |  | 会员子卡ID | internal | relation-key | server-filter-only |
| 5 | `operation_info` | `varchar(20)` | 否 |  |  | 说明 30天 2个月 1年 | internal | business-field | semantic-review-required |
| 6 | `begin_date` | `datetime` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 7 | `end_date` | `datetime` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 8 | `actual_end_date` | `datetime` | 否 |  |  | 实际结束时间 | internal | business-field | semantic-review-required |
| 9 | `stop_frequency` | `int(11)` | 否 |  |  | 停卡次数 | internal | business-field | semantic-review-required |
| 10 | `card_befor_expiration_date` | `datetime` | 否 |  |  | 操作前有效期 | internal | business-field | semantic-review-required |
| 11 | `card_after_expiration_date` | `datetime` | 否 |  |  | 操作后有效期 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 13 | `state` | `int(11)` | 否 |  |  | 状态 0 停止，1开启 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 否 |  |  | 解卡操纵人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 17 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_card_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：用户卡关联项目表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 主卡id | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 | MUL |  | 子卡id | internal | relation-key | server-filter-only |
| 5 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 6 | `card_value` | `decimal(10,2)` | 否 |  | 0.00 | 剩余金额(次数) | internal | business-field | semantic-review-required |
| 7 | `card_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 剩余正金（次数） | internal | business-field | semantic-review-required |
| 8 | `card_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 剩余赠送金额(次数) | internal | business-field | semantic-review-required |
| 9 | `consumption_value` | `decimal(10,2)` | 否 |  | 0.00 | 消费金额(次数) | internal | business-field | semantic-review-required |
| 10 | `is_default` | `tinyint(1)` | 否 |  | 0 | 是否默认，默认选中上次核销的项目 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 12 | `state` | `int(11)` | 否 |  |  | 状态-1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cardid`：唯一 BTREE（child_card_id, item_id, state）

### `user_card_service_item_lability`

类型：BASE TABLE；引擎：InnoDB；领域：member-card；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 主卡id | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  |  | 子卡id | internal | relation-key | server-filter-only |
| 5 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 6 | `card_value` | `decimal(10,2)` | 否 |  | 0.00 | 剩余金额(次数) | internal | business-field | semantic-review-required |
| 7 | `card_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 剩余正金（次数） | internal | business-field | semantic-review-required |
| 8 | `card_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 剩余赠送金额(次数) | internal | business-field | semantic-review-required |
| 9 | `service_lability` | `decimal(10,2)` | 否 |  |  | 负债 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 11 | `state` | `int(11)` | 否 |  |  | 状态-1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 12 | `lability_date` | `date` | 否 |  |  | 负债月份 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_coupon`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：store_id, tenant_id。
表注释：用户优惠券关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键Id | internal | relation-key | server-filter-only |
| 2 | `coupon_id` | `int(11)` | 否 | MUL |  | 优惠券Id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  | 0 | 会员卡Id | internal | subject-or-relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户Id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 是 | MUL |  | 店铺Id | internal | store-scope | server-filter-only |
| 6 | `consumption_id` | `bigint(20)` | 否 |  | 0 | 财务ID 使用后更新 | internal | relation-key | server-filter-only |
| 7 | `coupon_type` | `int(11)` | 否 |  |  | 类型 0代金券 1打折券 2服务券 3礼品券 | internal | business-field | semantic-review-required |
| 8 | `coupon_title` | `varchar(20)` | 否 |  |  | 标题 | internal | business-field | semantic-review-required |
| 9 | `coupon_img` | `varchar(70)` | 是 |  |  | 优惠券背景图 | internal | business-field | semantic-review-required |
| 10 | `coupon_icon` | `varchar(70)` | 是 |  |  | 赠品图 | internal | business-field | semantic-review-required |
| 11 | `is_use_vip` | `tinyint(1)` | 否 |  |  | 是否会员可用 | internal | business-field | semantic-review-required |
| 12 | `is_more` | `tinyint(1)` | 否 |  |  | 是否可以同时使用多张 | internal | business-field | semantic-review-required |
| 13 | `is_buy_card` | `tinyint(1)` | 否 |  |  | 是否只用于购买会员卡 | internal | business-field | semantic-review-required |
| 14 | `is_use_audit` | `tinyint(1)` | 否 |  | 0 | 使用优惠券是否需要审核 | internal | business-field | semantic-review-required |
| 15 | `use_min_money` | `decimal(10,2)` | 否 |  | 0.00 | 最低消费限制 | internal | business-field | semantic-review-required |
| 16 | `coupon_value` | `decimal(10,2)` | 否 |  | 0.00 | 优惠卷面值（金额、折扣、现价） | internal | business-field | semantic-review-required |
| 17 | `original_price` | `decimal(10,2)` | 否 |  | 0.00 | 原价 | internal | business-field | semantic-review-required |
| 18 | `coupon_center_id` | `int(11)` | 否 | MUL | 0 | 优惠中心ID | internal | relation-key | server-filter-only |
| 19 | `activity_id` | `int(11)` | 否 |  | 0 | 活动id | internal | relation-key | server-filter-only |
| 20 | `activity_type` | `int(11)` | 否 |  |  | 活动类型 0裂变 1抽奖 | internal | business-field | semantic-review-required |
| 21 | `random_param` | `varchar(40)` | 是 |  |  | 优惠券随机密钥 | internal | business-field | semantic-review-required |
| 22 | `recom_uid` | `int(11)` | 否 |  | 0 | 推荐者用户id | internal | business-field | semantic-review-required |
| 23 | `coupon_source` | `int(11)` | 是 |  |  | 来源 0其他 1活动 2 优惠中心 3店长赠送 4短信营销 | internal | business-field | semantic-review-required |
| 24 | `is_trigger` | `tinyint(1)` | 否 |  | 0 | 使用是否触发条件 | internal | business-field | semantic-review-required |
| 25 | `coupon_count` | `int(11)` | 是 |  |  | 优惠券数量 | internal | business-field | semantic-review-required |
| 26 | `coupon_description` | `varchar(500)` | 是 |  |  | 优惠卷说明 | internal | business-field | semantic-review-required |
| 27 | `begin_date` | `date` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 28 | `end_date` | `date` | 是 | MUL |  | 结束时间 | internal | business-field | semantic-review-required |
| 29 | `state_reason` | `int(11)` | 否 |  |  | 不可用原因 0默认 1没有购买过或续费  -2审核中 | internal | business-field | semantic-review-required |
| 30 | `is_show` | `tinyint(1)` | 否 |  | 0 | 是否已经显示  0未显示 1已显示 | internal | business-field | semantic-review-required |
| 31 | `receive_type` | `int(11)` | 否 |  | 0 | 0 手动领券（已领取）   1 自动送券（已发放） | internal | business-field | semantic-review-required |
| 32 | `use_frequency_type` | `int(11)` | 否 |  |  | 使用频率限制 0每天 1每周 2每月 | internal | business-field | semantic-review-required |
| 33 | `use_frequency_quantity` | `int(11)` | 否 |  |  | 使用频率限制 0每天 1每周 2每月 | internal | business-field | semantic-review-required |
| 34 | `wx_coupon_id` | `varchar(50)` | 是 |  |  | 微信券id | internal | relation-key | server-filter-only |
| 35 | `wx_coupon_code` | `varchar(50)` | 是 | MUL |  | 微信券code | internal | business-field | semantic-review-required |
| 36 | `wx_coupon_state` | `int(11)` | 是 |  | 0 | 微信卡包会员卡状态 0未领卡 1已领卡 | internal | business-field | semantic-review-required |
| 37 | `al_coupon_id` | `varchar(50)` | 是 |  |  | 支付宝id | internal | relation-key | server-filter-only |
| 38 | `al_coupon_code` | `varchar(50)` | 是 |  |  | 支付宝券cide | internal | business-field | semantic-review-required |
| 39 | `al_coupon_state` | `int(11)` | 是 |  | 0 | 支付宝卡包会员卡状态 0未领卡 1已领卡 | internal | business-field | semantic-review-required |
| 40 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0不可用 1正常 2已用 3已过期 | internal | business-field | semantic-review-required |
| 41 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户Id | internal | tenant-scope | server-filter-only |
| 42 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 43 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_couponCenterId`：非唯一 BTREE（coupon_center_id）
- `idx_couponId`：非唯一 BTREE（coupon_id）
- `idx_endDate`：非唯一 BTREE（end_date, state_reason）
- `idx_storeId`：非唯一 BTREE（store_id）
- `idx_tenantId`：非唯一 BTREE（tenant_id）
- `idx_uid`：非唯一 BTREE（uid）
- `inx_wxCode`：非唯一 BTREE（wx_coupon_code）

### `user_coupon_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：coupon-marketing；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `coupon_id` | `int(11)` | 否 |  |  | 优惠券id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `item_name` | `varchar(30)` | 否 |  |  | 项目名 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(11)` | 否 |  |  | 状态 0不可用 1可用 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_group`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：会员分组表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `tag_group_id` | `int(11)` | 否 |  | 1 | 标签分组ID | internal | relation-key | server-filter-only |
| 3 | `group_id` | `int(11)` | 否 |  |  | 分组id | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 | MUL |  | 会员卡id | internal | subject-or-relation-key | server-filter-only |
| 6 | `uid` | `int(11)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 7 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 1启用 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（card_id, store_id）
- `index_sgc`：唯一 BTREE（store_id, group_id, card_id）

### `user_lessons_log`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：store_id, tenant_id。
表注释：用户上课情况

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `reservation_id` | `bigint(20)` | 否 |  |  | 预约id | internal | relation-key | server-filter-only |
| 3 | `lessons_id` | `bigint(20)` | 否 |  |  | 课程id | internal | relation-key | server-filter-only |
| 4 | `card_id` | `bigint(20)` | 否 |  |  | 会员卡id | internal | subject-or-relation-key | server-filter-only |
| 5 | `user_id` | `bigint(20)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_id` | `bigint(20)` | 否 |  | 0 | 财务ID 使用后更新 | internal | relation-key | server-filter-only |
| 7 | `log_type` | `int(11)` | 否 |  |  | 上课日志类型 0预约 1更改预约，2取消预约，3候补 ，10签到 11取消签到 20旷课 21取消旷课 | internal | business-field | semantic-review-required |
| 8 | `is_repeal` | `tinyint(1)` | 否 |  |  | 是否撤销 | internal | business-field | semantic-review-required |
| 9 | `store_id` | `int(11)` | 否 | MUL |  | 店铺id | internal | store-scope | server-filter-only |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 | 租户id | internal | tenant-scope | server-filter-only |
| 11 | `order_by` | `int(11)` | 否 |  |  | 排序 倒序 | internal | business-field | semantic-review-required |
| 12 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 13 | `state` | `int(11)` | 否 |  | 1 | 状态；0-未开放，1-已开放，-1已删除 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  | 0 | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  | CURRENT_TIMESTAMP | 创建时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  | 0 | 修改人 | internal | business-field | semantic-review-required |
| 17 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_storeId`：非唯一 BTREE（store_id）

### `user_login_token`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `uid` | `int(11)` | 否 | PRI |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 2 | `token` | `varchar(50)` | 否 |  |  | token | restricted | business-field | deny |
| 3 | `rc_token` | `varchar(50)` | 是 |  |  | 融云token | restricted | business-field | deny |
| 4 | `client_type` | `int(11)` | 否 |  |  | 客户端类型 0顾客 1商家,2预约，3营销 | internal | business-field | semantic-review-required |
| 5 | `open_id` | `varchar(50)` | 是 |  |  | openId | restricted | relation-key | deny |
| 6 | `open_token` | `varchar(50)` | 是 |  |  | open_token | restricted | business-field | deny |
| 7 | `update_date` | `datetime` | 否 |  |  | 更新时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（uid）

### `user_migration_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `old_uid` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 3 | `new_uid` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 4 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_open_login`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：无。
表注释：开放平台登陆记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 | MUL |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 3 | `platform` | `int(11)` | 否 |  |  | 所属平台1 微信，2 QQ，3 支付宝，4云闪付 | internal | business-field | semantic-review-required |
| 4 | `client_type` | `int(11)` | 否 |  |  | 客户端  0=C端，1=B端 | internal | business-field | semantic-review-required |
| 5 | `open_id` | `varchar(50)` | 是 | MUL |  | 开发者唯一ID | restricted | relation-key | deny |
| 6 | `h5_open_id` | `varchar(50)` | 是 |  |  | 公众号openid | restricted | relation-key | deny |
| 7 | `business_h5_open_id` | `varchar(50)` | 否 |  |  | 商家公众号openid | restricted | relation-key | deny |
| 8 | `business_open_id` | `varchar(50)` | 是 | MUL |  | 商家openid | restricted | relation-key | deny |
| 9 | `business_app_open_id` | `varchar(50)` | 是 |  |  | 商家AppOpenId | restricted | relation-key | deny |
| 10 | `reservation_open_id` | `varchar(50)` | 是 |  |  | 商家预约openid | restricted | relation-key | deny |
| 11 | `marketing_open_id` | `varchar(50)` | 是 |  |  | 商家营销openid | restricted | relation-key | deny |
| 12 | `union_id` | `varchar(50)` | 是 | MUL |  | 平台唯一ID | restricted | relation-key | deny |
| 13 | `u_name` | `varchar(20)` | 是 |  |  | 平台昵称 | internal | business-field | semantic-review-required |
| 14 | `is_register` | `int(11)` | 否 |  |  | 是否是注册账号 | internal | business-field | semantic-review-required |
| 15 | `source_uid` | `int(11)` | 否 |  | 0 | 初始ID | internal | business-field | semantic-review-required |
| 16 | `three_id` | `int(11)` | 否 |  | 0 | 第三方平台ID | internal | relation-key | server-filter-only |
| 17 | `state` | `int(11)` | 否 |  |  | 状态-1解绑，1启用 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_businessOpenId`：非唯一 BTREE（business_open_id）
- `idx_openId`：非唯一 BTREE（open_id）
- `idx_uid`：非唯一 BTREE（uid）
- `idx_unionId`：非唯一 BTREE（union_id）

### `user_point_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `moudle_name` | `varchar(50)` | 否 |  |  | 模块名称 | internal | business-field | semantic-review-required |
| 4 | `name` | `varchar(50)` | 否 |  |  | 名称 | internal | business-field | semantic-review-required |
| 5 | `content` | `varchar(500)` | 否 |  |  | 内容 | sensitive-unstructured | business-field | deny |
| 6 | `type` | `int(11)` | 否 |  | 0 | 类型；-1-异常信息，0-默认，1-新手引导后埋点， | internal | business-field | semantic-review-required |
| 7 | `path` | `varchar(100)` | 否 |  |  | 路径 | internal | business-field | semantic-review-required |
| 8 | `ip_address` | `varchar(50)` | 否 |  |  | ip | sensitive | business-field | masked-or-filter-only |
| 9 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 10 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_recommend`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | id 自动增长主键 | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 受邀请人UID | internal | subject-or-relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 受邀请店铺ID | internal | store-scope | server-filter-only |
| 4 | `ruid` | `int(11)` | 否 |  |  | 邀请人UID | internal | business-field | semantic-review-required |
| 5 | `rcontent` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 6 | `is_rebate` | `tinyint(1)` | 否 |  |  | 是否给客户发了返利 | internal | business-field | semantic-review-required |
| 7 | `rebate_price` | `decimal(10,2)` | 否 |  | 0.00 | 返利金额 | internal | business-field | semantic-review-required |
| 8 | `rebate_date` | `datetime` | 是 |  |  | 返利时间 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  |  | 0无效，1已生效 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_remind`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：用户新消息通知

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `new_friend` | `int(11)` | 否 |  | 0 | 朋友提醒 | internal | business-field | semantic-review-required |
| 4 | `new_message` | `int(11)` | 否 |  | 0 | 消息提醒 | sensitive-unstructured | business-field | deny |
| 5 | `new_version` | `int(11)` | 否 |  | 0 | 更新提醒 | internal | business-field | semantic-review-required |
| 6 | `new_community_notice` | `int(11)` | 否 |  | 0 | 社区通知提醒 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_search_condition`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：搜索条件

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `condition_title` | `varchar(50)` | 是 |  |  | 标题 | internal | business-field | semantic-review-required |
| 4 | `condition_info` | `varchar(2000)` | 是 |  |  | 搜索内容 | internal | business-field | semantic-review-required |
| 5 | `condition_describe` | `varchar(255)` | 是 |  |  | 搜索描述 | internal | business-field | semantic-review-required |
| 6 | `is_share` | `tinyint(1)` | 否 |  |  | 是否所有人可见 | internal | business-field | semantic-review-required |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_seting`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：用户设置

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `course_remind` | `tinyint(4)` | 否 |  |  | 课程提醒 | internal | business-field | semantic-review-required |
| 4 | `remind_time` | `int(11)` | 否 |  |  | 提醒时间 | internal | business-field | semantic-review-required |
| 5 | `mess_last_date` | `datetime` | 否 |  | 2017-01-01 00:00:00 | 消息最后更新时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_staff_relation`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：归属人

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员ID | internal | subject-or-relation-key | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 客户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `staff_id` | `int(11)` | 否 |  |  | 店员id | internal | subject-or-relation-key | server-filter-only |
| 5 | `user_remark` | `varchar(50)` | 否 |  |  | 客户备注 | sensitive-unstructured | business-field | deny |
| 6 | `user_description` | `varchar(100)` | 否 |  |  | 客户描述 | internal | business-field | semantic-review-required |
| 7 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 9 | `add_way` | `int(11)` | 否 |  |  | 添加来源 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_track`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  | 0 |  | internal | store-scope | server-filter-only |
| 3 | `store_name` | `varchar(50)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 4 | `soft_version_name` | `varchar(50)` | 是 |  |  | 版本名称 | internal | business-field | semantic-review-required |
| 5 | `store_class_type_name` | `varchar(50)` | 是 |  |  | 行业名称 | internal | business-field | semantic-review-required |
| 6 | `store_mobile` | `varchar(11)` | 是 |  |  |  | sensitive | business-field | masked-or-filter-only |
| 7 | `vip_count` | `int(11)` | 是 |  |  | 会员数量 | internal | business-field | semantic-review-required |
| 8 | `card_count` | `int(11)` | 是 |  |  | 卡数量 | internal | business-field | semantic-review-required |
| 9 | `login_count` | `int(11)` | 是 |  |  | 登录总次数 | internal | business-field | semantic-review-required |
| 10 | `store_create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 11 | `store_end_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 12 | `end_login_date` | `datetime` | 是 |  |  | 最后登录日期 | internal | business-field | semantic-review-required |
| 13 | `week_login_count` | `int(11)` | 是 |  |  | 周登录次数 | internal | business-field | semantic-review-required |
| 14 | `week_add_user_count` | `int(11)` | 是 |  |  | 周会员增加人数 | internal | business-field | semantic-review-required |
| 15 | `week_hexiao_user_count` | `int(11)` | 是 |  |  | 周会员核减人数 | internal | business-field | semantic-review-required |
| 16 | `end_diff_day` | `int(11)` | 是 |  |  | 距离到期天数 | internal | business-field | semantic-review-required |
| 17 | `state` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_track_black`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  |  | internal | store-scope | server-filter-only |
| 3 | `reason` | `varchar(500)` | 否 |  |  | 原因 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 7 | `admin_id` | `int(11)` | 是 |  |  |  | internal | relation-key | server-filter-only |
| 8 | `admin_name` | `varchar(50)` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_trial_record`

类型：BASE TABLE；引擎：InnoDB；领域：audit-log；隔离字段：store_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 | MUL |  |  | internal | store-scope | server-filter-only |
| 3 | `login_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 4 | `root_id` | `int(11)` | 是 |  |  |  | internal | relation-key | server-filter-only |
| 5 | `contact_id` | `int(11)` | 是 |  |  |  | sensitive | relation-key | server-filter-only |
| 6 | `contact_people` | `varchar(255)` | 是 |  |  |  | sensitive | business-field | masked-or-filter-only |
| 7 | `contac_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 8 | `return_visit_type` | `int(11)` | 是 |  |  | 回访状态；0-待联系，1-已联系，2-无需联系，3-待再联系 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(255)` | 是 |  |  |  | sensitive-unstructured | business-field | deny |
| 10 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `Index_storeid_logindate`：非唯一 BTREE（store_id, login_date）
- `PRIMARY`：唯一 BTREE（id）

### `user_vacation`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 4 | `begin_date` | `datetime` | 否 |  |  | 开始时间 | internal | business-field | semantic-review-required |
| 5 | `end_date` | `datetime` | 否 |  |  | 结束时间 | internal | business-field | semantic-review-required |
| 6 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | -1 删除 1正常 2过期 | internal | business-field | semantic-review-required |
| 8 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `user_week`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `img_path` | `varchar(255)` | 是 |  |  | 图片路径 | internal | business-field | semantic-review-required |
| 4 | `week_start` | `varchar(20)` | 否 |  |  | 周时间 | internal | business-field | semantic-review-required |
| 5 | `last_date` | `datetime` | 是 |  |  | 最后操作时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `users`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：tenant_id, store_id。
表注释：用户表


| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 用户ID | internal | relation-key | server-filter-only |
| 2 | `user_level` | `int(11)` | 否 |  |  | 用户等级 | internal | business-field | semantic-review-required |
| 3 | `user_mobile` | `varchar(20)` | 否 | MUL |  | 用户手机 | sensitive | business-field | masked-or-filter-only |
| 4 | `user_pass` | `varchar(50)` | 否 |  |  | 用户密码 | internal | business-field | semantic-review-required |
| 5 | `user_type` | `int(11)` | 否 |  |  | 用户类型，0普通用户，1教练，2管理员,3审核账号 | internal | business-field | semantic-review-required |
| 6 | `user_identity` | `int(11)` | 否 |  | 0 | 用户身份:0 普通用户，1 公司账号 2 家眷 3 朋友 4 合作伙伴 | internal | business-field | semantic-review-required |
| 7 | `is_vip` | `int(11)` | 否 |  |  | 是否是VIP | internal | business-field | semantic-review-required |
| 8 | `is_robot` | `int(11)` | 否 |  | 0 | 是否是机器人 0不是 1是 | internal | business-field | semantic-review-required |
| 9 | `state` | `int(11)` | 否 |  |  | 用户状态  1正常 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 是 |  | 0 | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `store_id` | `int(11)` | 是 |  | 0 | 店铺ID | internal | store-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_mobile`：非唯一 BTREE（user_mobile）

### `users_info`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：用户详情

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 | UNI |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 3 | `user_name` | `varchar(20)` | 否 |  |  | 用户昵称 | sensitive | business-field | masked-or-filter-only |
| 4 | `user_img` | `varchar(200)` | 否 |  |  | 头像 | internal | business-field | semantic-review-required |
| 5 | `user_sex` | `int(11)` | 否 |  |  | 性别 | internal | business-field | semantic-review-required |
| 6 | `user_povince` | `varchar(10)` | 否 |  |  | 用户省 | internal | business-field | semantic-review-required |
| 7 | `user_city` | `varchar(10)` | 否 |  |  | 用户城市 | internal | business-field | semantic-review-required |
| 8 | `user_district` | `varchar(10)` | 否 |  |  | 用户所在区 | internal | business-field | semantic-review-required |
| 9 | `user_address` | `varchar(20)` | 否 |  |  | 用户详细地址 | sensitive | business-field | masked-or-filter-only |
| 10 | `user_birthday` | `varchar(20)` | 否 |  |  | 生日 | internal | business-field | semantic-review-required |
| 11 | `user_height` | `int(11)` | 否 |  |  | 用户身高（cm） | internal | business-field | semantic-review-required |
| 12 | `user_weight` | `decimal(4,1)` | 否 |  |  | 用户体重（kg） | internal | business-field | semantic-review-required |
| 13 | `user_age` | `int(11)` | 否 |  |  | 年龄 | internal | business-field | semantic-review-required |
| 14 | `user_signature` | `varchar(100)` | 否 |  |  | 用户签名 | internal | business-field | semantic-review-required |
| 15 | `user_mobile_type` | `int(11)` | 否 |  | 0 | 用户手机类型 0:ios,1android | sensitive | business-field | masked-or-filter-only |
| 16 | `bgimg` | `varchar(50)` | 是 |  |  | 个人中心背景图 | internal | business-field | semantic-review-required |
| 17 | `popularize_code` | `varchar(10)` | 是 |  |  | 推广码 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 19 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_uid`：唯一 BTREE（uid）

### `version_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `version_no` | `varchar(10)` | 否 |  |  | 版本编号 | internal | business-field | semantic-review-required |
| 3 | `version_name` | `varchar(50)` | 否 |  |  | 版本名称 | internal | business-field | semantic-review-required |
| 4 | `version_info` | `varchar(500)` | 否 |  |  | 版本说明 | internal | business-field | semantic-review-required |
| 5 | `platform` | `int(11)` | 否 |  |  | 平台：1安卓 2IOS | internal | business-field | semantic-review-required |
| 6 | `environment` | `int(11)` | 否 |  |  | 上线环境：1生产环境 2测试环境 3开发环境 | internal | business-field | semantic-review-required |
| 7 | `is_beat` | `int(11)` | 否 |  |  | 是否是测试版 0 否 1是（测试版只有特定权限可以更新） | internal | business-field | semantic-review-required |
| 8 | `is_must` | `int(11)` | 否 |  |  | 是否必须更新 0否，1是 | internal | business-field | semantic-review-required |
| 9 | `down_url` | `varchar(200)` | 否 |  |  | 下载地址 | internal | business-field | semantic-review-required |
| 10 | `api_url` | `varchar(100)` | 是 |  |  | api请求地址 | internal | business-field | semantic-review-required |
| 11 | `h5_url` | `varchar(100)` | 是 |  |  | h5访问地址 | internal | business-field | semantic-review-required |
| 12 | `state` | `int(11)` | 否 |  |  | -1删除 0未开放 1开放 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 是 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `wechat_attention`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 | MUL |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 3 | `platform` | `int(11)` | 否 |  |  | 0:C端公众号，1:B端公众号 | internal | business-field | semantic-review-required |
| 4 | `open_id` | `varchar(30)` | 否 | MUL |  | 微信公众号OpenId | restricted | relation-key | deny |
| 5 | `union_id` | `varchar(30)` | 否 | MUL |  | 微信平台unionId | restricted | relation-key | deny |
| 6 | `state` | `int(11)` | 否 |  |  | 0取消关注，1已关注 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `three_id` | `int(11)` | 是 | MUL | 0 | 三方ID | internal | relation-key | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_openId`：非唯一 BTREE（open_id）
- `idx_threeId`：非唯一 BTREE（three_id）
- `idx_unionid_uid_platform`：非唯一 BTREE（union_id, uid, platform）
- `inx_uid`：非唯一 BTREE（uid）

### `wechat_message_template`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `type` | `int(11)` | 是 |  |  | 0:小程序 1：公众号 | internal | business-field | semantic-review-required |
| 3 | `appid` | `varchar(255)` | 是 |  |  | appid | internal | business-field | semantic-review-required |
| 4 | `template_id` | `varchar(255)` | 是 |  |  | 模板ID | internal | relation-key | server-filter-only |
| 5 | `tno` | `varchar(255)` | 是 |  |  | 模板编号 | internal | business-field | semantic-review-required |
| 6 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 7 | `tenant_id` | `int(11)` | 是 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 8 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 9 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `wechat_message_template_pub`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `type` | `int(11)` | 否 |  |  | 类型，0：C-小程序，1：C-公众号，2：B-小程序，3：B-公众号 | internal | business-field | semantic-review-required |
| 3 | `title` | `varchar(100)` | 否 |  |  | 模板标题 | internal | business-field | semantic-review-required |
| 4 | `tno` | `varchar(50)` | 否 |  |  | 模板编号，公众号使用 | internal | business-field | semantic-review-required |
| 5 | `tid` | `varchar(300)` | 否 |  |  | tid小程序使用 | internal | business-field | semantic-review-required |
| 6 | `kid_list` | `varchar(500)` | 否 |  |  | 小程序使用 | internal | business-field | semantic-review-required |
| 7 | `temp_type` | `int(11)` | 否 |  |  | 消息类型：对应枚举值 | internal | business-field | semantic-review-required |
| 8 | `sceneDesc` | `varchar(255)` | 是 |  |  | 小程序使用 | internal | business-field | semantic-review-required |
| 9 | `subscribe_type` | `int(11)` | 否 |  |  | 0：一次性订阅 1：长期订阅 | internal | business-field | semantic-review-required |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 更新时间 | internal | business-field | semantic-review-required |
| 12 | `state` | `int(11)` | 否 |  |  | 状态：0 停用，1 启用 | internal | business-field | semantic-review-required |
| 13 | `template_id` | `varchar(255)` | 否 |  |  | 电子会员卡服务中心的模板ID | internal | relation-key | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `wechat_message_template_type`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `type` | `int(11)` | 是 |  |  | 消息类型：对应枚举值 | internal | business-field | semantic-review-required |
| 3 | `template_id` | `int(11)` | 是 |  |  | 公共消息模板ID | internal | relation-key | server-filter-only |
| 4 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 5 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 6 | `state` | `int(11)` | 是 |  |  | 0:禁用 1:启用 | internal | business-field | semantic-review-required |
| 7 | `tno` | `varchar(255)` | 是 |  |  | 模板编号 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `wechat_miniapp_scene`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `scene_name` | `varchar(50)` | 否 |  |  |  | internal | business-field | semantic-review-required |
| 3 | `scene_value` | `varchar(50)` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `wechat_qrcode`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `platform` | `int(11)` | 否 |  |  | 平台 0C 1B | internal | business-field | semantic-review-required |
| 3 | `code_type` | `int(11)` | 否 |  |  | 码用途 0推广 | internal | business-field | semantic-review-required |
| 4 | `code_no` | `int(11)` | 否 |  |  | 编码 | internal | business-field | semantic-review-required |
| 5 | `code_scene` | `varchar(10)` | 否 |  |  | 标识 | internal | business-field | semantic-review-required |
| 6 | `code_ticket` | `varchar(100)` | 否 |  |  | 二维码参数 | internal | business-field | semantic-review-required |
| 7 | `code_remark` | `varchar(50)` | 否 |  |  | 码备注 | sensitive-unstructured | business-field | deny |
| 8 | `agent_id` | `int(11)` | 否 |  |  | 代理id | internal | relation-key | server-filter-only |
| 9 | `user_id` | `int(11)` | 否 |  |  | 关联推广人员ID | internal | subject-or-relation-key | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建日期 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `wechat_reply`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `app_id` | `varchar(50)` | 否 |  |  | 公号APPID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `reply_type` | `int(11)` | 否 |  |  | 回复类型：0 店铺分享，1 储值分享，2领卡.3 商城分享 4点单分享 5 抽奖活动 100 咨询 101 关注自动回复 | internal | business-field | semantic-review-required |
| 5 | `message_type` | `int(11)` | 否 |  |  | 消息类型 0文字 1图 | sensitive-unstructured | business-field | deny |
| 6 | `user_message` | `varchar(20)` | 是 |  |  | 用户发送信息 | sensitive-unstructured | business-field | deny |
| 7 | `message_info` | `varchar(200)` | 否 |  |  | 回复内容 | sensitive-unstructured | business-field | deny |
| 8 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `white_list`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `store_mobile` | `varchar(11)` | 否 |  |  | 手机号 | sensitive | business-field | masked-or-filter-only |
| 3 | `type` | `int(11)` | 否 |  | 0 | 类型；1-试用用户待跟进数据 | internal | business-field | semantic-review-required |
| 4 | `state` | `int(11)` | 否 |  | 1 | 状态；0-无效，1-有效 | internal | business-field | semantic-review-required |
| 5 | `create_by` | `int(11)` | 否 |  | 0 |  | internal | business-field | semantic-review-required |
| 6 | `create_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_bench_class`

类型：BASE TABLE；引擎：InnoDB；领域：reservation-waitlist；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `class_name` | `varchar(10)` | 否 |  |  | 分类名称 | internal | business-field | semantic-review-required |
| 3 | `module_id` | `int(11)` | 否 |  |  | 模块id | internal | relation-key | server-filter-only |
| 4 | `order_by` | `int(10)` | 否 |  |  | 排序 | internal | business-field | semantic-review-required |
| 5 | `state` | `int(4)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_attention`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：tenant_id。
表注释：企微客户信息

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 3 | `union_id` | `varchar(50)` | 是 |  |  | 公众平台ID | restricted | relation-key | deny |
| 4 | `external_userid` | `varchar(50)` | 是 |  |  | 外部联系人ID | internal | business-field | semantic-review-required |
| 5 | `pending_id` | `varchar(50)` | 是 |  |  | 临时ID | internal | relation-key | server-filter-only |
| 6 | `state` | `int(11)` | 是 |  |  | 状态 1以加好友 | internal | business-field | semantic-review-required |
| 7 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 8 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 10 | `three_id` | `int(11)` | 是 |  |  | 第三方APPid | internal | relation-key | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_msg`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `temp_id` | `int(11)` | 否 |  |  | 模板id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `msg_type` | `int(11)` | 否 |  |  | 消息类型 0主动发送 1被动发送 | internal | business-field | semantic-review-required |
| 5 | `msg_info` | `varchar(255)` | 否 |  |  | 消息内容 | internal | business-field | semantic-review-required |
| 6 | `send_time` | `datetime` | 是 |  |  | type=0 群发时间 | internal | business-field | semantic-review-required |
| 7 | `search_condition_id` | `int(11)` | 否 |  |  | 搜索条件id | internal | relation-key | server-filter-only |
| 8 | `condition_info` | `varchar(2000)` | 否 |  |  | 筛选条件 | internal | business-field | semantic-review-required |
| 9 | `condition_describe` | `varchar(255)` | 否 |  |  | 筛选条件描述 | internal | business-field | semantic-review-required |
| 10 | `send_sum` | `int(11)` | 否 |  |  | 发送次数 | internal | business-field | semantic-review-required |
| 11 | `send_people_sum` | `int(11)` | 否 |  |  | 发送人数 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 13 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0未发送 1启用 2发送中 3已发送 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 17 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_msg_attachments`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `msg_id` | `int(11)` | 否 |  |  | 消息id | internal | relation-key | server-filter-only |
| 4 | `msg_type` | `int(11)` | 否 |  |  | 附件消息类型 1文本 2图片 3链接 4小程序 5视频 6文件 | internal | business-field | semantic-review-required |
| 5 | `file_url` | `varchar(100)` | 是 |  |  | 附件资源地址 用来上传获取media_id | internal | business-field | semantic-review-required |
| 6 | `title` | `varchar(50)` | 是 |  |  | 附件标题 3 4 5使用 | internal | business-field | semantic-review-required |
| 7 | `link_picurl` | `varchar(100)` | 是 |  |  | 链接封面图 | internal | business-field | semantic-review-required |
| 8 | `link_desc` | `varchar(100)` | 是 |  |  | 链接描述 | internal | business-field | semantic-review-required |
| 9 | `link_url` | `varchar(255)` | 是 |  |  | 链接地址 | internal | business-field | semantic-review-required |
| 10 | `miniprogram_appid` | `varchar(50)` | 是 |  |  | 小程序appid | internal | business-field | semantic-review-required |
| 11 | `miniprogram_page` | `varchar(100)` | 是 |  |  | 小程序page路径 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 13 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 17 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_msg_send_log`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `msg_id` | `int(11)` | 否 |  |  | 消息ID | internal | relation-key | server-filter-only |
| 3 | `task_id` | `int(11)` | 否 |  |  | 任务ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 5 | `user_id` | `int(11)` | 否 |  |  | 会员id | internal | subject-or-relation-key | server-filter-only |
| 6 | `external_userid` | `varchar(50)` | 否 |  |  | 企微外部联系人ID | internal | business-field | semantic-review-required |
| 7 | `staff_id` | `int(11)` | 否 |  |  | 店员ID | internal | subject-or-relation-key | server-filter-only |
| 8 | `staff_uid` | `int(11)` | 否 |  |  | 店员UID | internal | business-field | semantic-review-required |
| 9 | `follow_user_id` | `varchar(50)` | 否 |  |  | 企业微信联系人ID | internal | relation-key | server-filter-only |
| 10 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 0待发送 1发送中 2已发送 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_msg_staff_log`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `msg_id` | `int(11)` | 否 |  |  | 模板id | internal | relation-key | server-filter-only |
| 3 | `task_id` | `int(11)` | 否 |  |  | 任务ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 5 | `staff_id` | `int(11)` | 否 |  |  | 店员id | internal | subject-or-relation-key | server-filter-only |
| 6 | `follow_user_id` | `varchar(50)` | 否 |  |  | 企微联系人ID | internal | relation-key | server-filter-only |
| 7 | `msg_type` | `int(11)` | 否 |  |  | 消息类型 0主动发送 1被动发送 | internal | business-field | semantic-review-required |
| 8 | `send_people_sum` | `int(11)` | 否 |  |  | 发送人数 | internal | business-field | semantic-review-required |
| 9 | `wechat_msg_id` | `varchar(50)` | 是 |  |  | 企业微信消息ID | internal | relation-key | server-filter-only |
| 10 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0未发送 1启用 2发送中 3已发送 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_msg_task`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键ID | internal | relation-key | server-filter-only |
| 2 | `msg_id` | `int(11)` | 否 |  |  | 模板id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `msg_type` | `int(11)` | 否 |  |  | 消息类型 0主动发送 1被动发送 | internal | business-field | semantic-review-required |
| 5 | `msg_info` | `varchar(255)` | 否 |  |  | 消息内容 | internal | business-field | semantic-review-required |
| 6 | `send_time` | `datetime` | 是 |  |  | type=0 群发时间 | internal | business-field | semantic-review-required |
| 7 | `search_condition_id` | `int(11)` | 否 |  |  | 搜索条件id | internal | relation-key | server-filter-only |
| 8 | `send_sum` | `int(11)` | 否 |  |  | 发送次数 | internal | business-field | semantic-review-required |
| 9 | `send_people_sum` | `int(11)` | 否 |  |  | 发送人数 | internal | business-field | semantic-review-required |
| 10 | `wechat_msg_id` | `varchar(50)` | 是 |  |  | 企业微信消息ID | internal | relation-key | server-filter-only |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 12 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0未发送 1启用 2发送中 3已发送 | internal | business-field | semantic-review-required |
| 13 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 14 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_msg_template`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `temp_name` | `varchar(50)` | 否 |  |  | 模板名称 | internal | business-field | semantic-review-required |
| 4 | `temp_info` | `varchar(255)` | 否 |  |  | 模板内容 | internal | business-field | semantic-review-required |
| 5 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_msg_template_attachments`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `temp_id` | `int(11)` | 否 |  |  | 模板id | internal | relation-key | server-filter-only |
| 4 | `msg_type` | `int(11)` | 否 |  |  | 附件消息类型 1文本 2图片 3链接 4小程序 5视频 6文件 | internal | business-field | semantic-review-required |
| 5 | `file_url` | `varchar(100)` | 是 |  |  | 附件资源地址 用来上传获取media_id | internal | business-field | semantic-review-required |
| 6 | `title` | `varchar(50)` | 是 |  |  | 附件标题 3 4 5使用 | internal | business-field | semantic-review-required |
| 7 | `link_picurl` | `varchar(100)` | 是 |  |  | 链接封面图 | internal | business-field | semantic-review-required |
| 8 | `link_desc` | `varchar(100)` | 是 |  |  | 链接描述 | internal | business-field | semantic-review-required |
| 9 | `link_url` | `varchar(255)` | 是 |  |  | 链接地址 | internal | business-field | semantic-review-required |
| 10 | `miniprogram_appid` | `varchar(50)` | 是 |  |  | 小程序appid | internal | business-field | semantic-review-required |
| 11 | `miniprogram_page` | `varchar(100)` | 是 |  |  | 小程序page路径 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 13 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 17 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_staff_code`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `code` | `varchar(30)` | 否 |  |  | Code | internal | business-field | semantic-review-required |
| 4 | `code_title` | `varchar(50)` | 否 |  |  | 活码标题 | internal | business-field | semantic-review-required |
| 5 | `bg_img` | `varchar(100)` | 是 |  |  | 背景图 | internal | business-field | semantic-review-required |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工id | internal | subject-or-relation-key | server-filter-only |
| 7 | `staff_uid` | `int(11)` | 否 |  |  | 员工Uid | internal | business-field | semantic-review-required |
| 8 | `is_tag` | `tinyint(1)` | 否 |  |  | 是否包含tag | internal | business-field | semantic-review-required |
| 9 | `is_attachment` | `tinyint(1)` | 否 |  |  | 是否包含附件 | internal | business-field | semantic-review-required |
| 10 | `message_info` | `varchar(255)` | 是 |  |  | 欢迎语 | sensitive-unstructured | business-field | deny |
| 11 | `code_img` | `varchar(255)` | 是 |  |  | 顾客端地址 | internal | business-field | semantic-review-required |
| 12 | `code_url` | `varchar(255)` | 是 |  |  | 活码地址 | internal | business-field | semantic-review-required |
| 13 | `code_config_id` | `varchar(50)` | 是 |  |  | 活码id | internal | relation-key | server-filter-only |
| 14 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 15 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 16 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 17 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 18 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 19 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_staff_code_attachments`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `code_id` | `int(11)` | 否 |  |  | 二维码id | internal | relation-key | server-filter-only |
| 4 | `msg_type` | `int(11)` | 否 |  |  | 附件消息类型 1文本 2图片 3链接 4小程序 5视频 6文件 | internal | business-field | semantic-review-required |
| 5 | `file_url` | `varchar(100)` | 是 |  |  | 附件资源地址 用来上传获取media_id | internal | business-field | semantic-review-required |
| 6 | `title` | `varchar(50)` | 是 |  |  | 附件标题 3 4 5使用 | internal | business-field | semantic-review-required |
| 7 | `link_picurl` | `varchar(100)` | 是 |  |  | 链接封面图 | internal | business-field | semantic-review-required |
| 8 | `link_desc` | `varchar(100)` | 是 |  |  | 链接描述 | internal | business-field | semantic-review-required |
| 9 | `link_url` | `varchar(255)` | 是 |  |  | 链接地址 | internal | business-field | semantic-review-required |
| 10 | `miniprogram_appid` | `varchar(50)` | 是 |  |  | 小程序appid | internal | business-field | semantic-review-required |
| 11 | `miniprogram_page` | `varchar(100)` | 是 |  |  | 小程序page路径 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 13 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 0禁用 1启用 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 17 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_staff_code_log`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `external_userid` | `varchar(50)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 3 | `code_id` | `int(11)` | 否 |  |  | 二维码id | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_staff_code_tag`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `code_id` | `int(11)` | 否 |  |  | 二维码id | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 4 | `tag_id` | `int(11)` | 否 |  |  | 标签id | internal | relation-key | server-filter-only |
| 5 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 6 | `state` | `int(11)` | 否 |  |  | 状态 -1删除 1启用 | internal | business-field | semantic-review-required |
| 7 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 10 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `work_wechat_user_relation`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：tenant_id。
表注释：企微好友关系

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 3 | `external_userid` | `varchar(50)` | 否 |  |  | 企微外部联系人ID | internal | business-field | semantic-review-required |
| 4 | `user_remark` | `varchar(20)` | 否 |  |  | 企业微信备注 | sensitive-unstructured | business-field | deny |
| 5 | `user_description` | `varchar(255)` | 是 |  |  | 企业微信描述 | internal | business-field | semantic-review-required |
| 6 | `add_way` | `int(11)` | 否 |  |  | 添加来源 | internal | business-field | semantic-review-required |
| 7 | `user_state` | `varchar(50)` | 是 |  |  | 企业自定义的state参数，用于区分客户具体是通过哪个「联系我」添加，由企业通过创建「联系我」方式指定 | internal | business-field | semantic-review-required |
| 8 | `staff_id` | `int(11)` | 否 |  |  | 店员ID | internal | subject-or-relation-key | server-filter-only |
| 9 | `follow_user_id` | `varchar(50)` | 是 |  |  | 企微员工id | internal | relation-key | server-filter-only |
| 10 | `three_id` | `int(11)` | 否 |  |  | 三方APPid | internal | relation-key | server-filter-only |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `state` | `int(11)` | 否 |  |  | 状态 0禁用 1启用 | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `update_date` | `datetime` | 是 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `workbench`

类型：BASE TABLE；引擎：InnoDB；领域：other；隔离字段：无。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `int(11)` | 否 | PRI |  |  | internal | relation-key | server-filter-only |
| 2 | `name` | `varchar(50)` | 是 |  |  | 名称 | internal | business-field | semantic-review-required |
| 3 | `module` | `varchar(50)` | 是 |  |  | 模块值 | internal | business-field | semantic-review-required |
| 4 | `type` | `int(11)` | 是 |  |  | 类型；0-小程序内部，1-外链，2-外部小程序，3-不跳转 | internal | business-field | semantic-review-required |
| 5 | `path` | `varchar(255)` | 是 |  |  | 跳转的内容 | internal | business-field | semantic-review-required |
| 6 | `module_id` | `int(11)` | 否 |  |  | 模块id | internal | relation-key | server-filter-only |
| 7 | `class_id` | `int(11)` | 否 |  |  | 分类id | internal | relation-key | server-filter-only |
| 8 | `name_english` | `varchar(50)` | 否 |  |  | 英文的名称 | internal | business-field | semantic-review-required |
| 9 | `border_color` | `varchar(50)` | 否 |  |  | 边框的颜色 | internal | business-field | semantic-review-required |
| 10 | `font_chinese_color` | `varchar(50)` | 否 |  |  | 中文字体色 | internal | business-field | semantic-review-required |
| 11 | `font_english_color` | `varchar(50)` | 否 |  |  | 英文字体色 | internal | business-field | semantic-review-required |
| 12 | `background_color` | `varchar(100)` | 否 |  |  | 背景色 | internal | business-field | semantic-review-required |
| 13 | `right_bottom_img` | `varchar(100)` | 否 |  |  | 右下角的图 | internal | business-field | semantic-review-required |
| 14 | `sort` | `int(11)` | 是 |  |  | 排序 | internal | business-field | semantic-review-required |
| 15 | `is_default` | `tinyint(1)` | 否 |  |  | 是否默认 | internal | business-field | semantic-review-required |
| 16 | `state` | `int(11)` | 是 |  |  | 状态；1-开启，0-关闭 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 19 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 20 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### 触发器目录

- `trigger_card_price`：AFTER UPDATE ON `user_card_child`
- `trigger_open_uid`：AFTER UPDATE ON `user_open_login`
- `trigger_user_mobile`：AFTER UPDATE ON `users`

### 存储过程与函数目录

- `UpdateCardDate`：PROCEDURE，返回类型 ``
- `UpdateCardSellCount`：PROCEDURE，返回类型 ``
- `UpdateCardValue`：PROCEDURE，返回类型 ``
- `UpdateUserCardChildSum`：PROCEDURE，返回类型 ``
- `UpdateUserCardSum`：PROCEDURE，返回类型 ``
- `UpdateUserCardTotalSum`：PROCEDURE，返回类型 ``
- `UpdateUserOpenThreeId`：PROCEDURE，返回类型 ``
- `UpdateUserPermissions`：PROCEDURE，返回类型 ``
- `UpdateUserStoreInfo`：PROCEDURE，返回类型 ``
- `UpdateYobConfigState`：PROCEDURE，返回类型 ``

## 数据库 `nutbooking_consumption`

角色：finance-shard；连接别名：TenantData, TenantData9；结构证据：MySQL 实时元数据；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_0`

角色：finance-shard；连接别名：TenantData0；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_1`

角色：finance-shard；连接别名：TenantData1；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_2`

角色：finance-shard；连接别名：TenantData2；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_3`

角色：finance-shard；连接别名：TenantData3；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_4`

角色：finance-shard；连接别名：TenantData4；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_5`

角色：finance-shard；连接别名：TenantData5；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_6`

角色：finance-shard；连接别名：TenantData6；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_7`

角色：finance-shard；连接别名：TenantData7；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

## 数据库 `nutbooking_consumption_8`

角色：finance-shard；连接别名：TenantData8；结构证据：运维确认的同构模板继承；结构来源：`nutbooking_consumption`；结构指纹：`8b5518679630b9d5bb15f861b0156ce04bd6a63ede6972d4077f87165ac69cbf`。

### `consumption_combination`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 否 |  |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 5 | `p_card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | relation-key | server-filter-only |
| 6 | `pay_card_value` | `decimal(10,2)` | 否 |  |  | 卡内支付金额 | internal | business-field | semantic-review-required |
| 7 | `pay_card_money` | `decimal(10,2)` | 否 |  |  | 购卡金额 | internal | business-field | semantic-review-required |
| 8 | `pay_money` | `decimal(10,2)` | 否 |  |  | 需支付金额 | internal | business-field | semantic-review-required |
| 9 | `pay_actual_money` | `decimal(10,2)` | 否 |  |  | 实际支付金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 0未处理 1已处理 | internal | business-field | semantic-review-required |
| 11 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_commission_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：佣金消费记录表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 是 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `uid` | `int(11)` | 是 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 4 | `card_id` | `int(11)` | 是 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `consumption_id` | `bigint(20)` | 是 |  |  | 财务ID | internal | relation-key | server-filter-only |
| 6 | `consumption_value` | `decimal(10,2)` | 是 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 7 | `deduct_price` | `decimal(10,2)` | 是 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `decimal(10,2)` | 是 |  |  | 调整后金额 | internal | business-field | semantic-review-required |
| 9 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8用户提现 | internal | business-field | semantic-review-required |
| 10 | `pay_way` | `int(11)` | 是 |  |  | 方式：0 购买会员 1门店消费 2 商城消费 3公众号 4线下 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 是 |  |  | 0禁用，1正常 | internal | business-field | semantic-review-required |
| 12 | `create_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 13 | `create_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 14 | `update_by` | `int(11)` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 是 |  |  |  | internal | business-field | semantic-review-required |
| 16 | `remark` | `varchar(255)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 17 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_file`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺id | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 4 | `file_path` | `varchar(100)` | 否 |  |  | 文件路径 | internal | business-field | semantic-review-required |
| 5 | `file_type` | `int(11)` | 否 |  |  | 文件类型 0图片 | internal | business-field | semantic-review-required |
| 6 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 -1 删除 1启用 | internal | business-field | semantic-review-required |
| 8 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 9 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 10 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 11 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_integral_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：积分消费明细

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 7 | `consumption_value` | `int(11)` | 否 |  |  | 调整积分 | internal | business-field | semantic-review-required |
| 8 | `after_value` | `int(11)` | 否 |  | 0 | 操作后积分 | internal | business-field | semantic-review-required |
| 9 | `deduct_price` | `decimal(10,2)` | 否 |  |  | 抵扣金额 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_storeId`：非唯一 BTREE（store_id）

### `consumption_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 3 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 4 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 6 | `source_store_id` | `int(11)` | 否 |  | 0 | 源商家id | internal | relation-key | server-filter-only |
| 7 | `staff_id` | `int(11)` | 否 |  | 0 | 员工ID，0商家店长收款 | internal | subject-or-relation-key | server-filter-only |
| 8 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 9 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 10 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 11 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 12 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 13 | `consumption_type` | `int(11)` | 否 |  |  | 消费方式：0 计次，1 金额，2积分，3印章,4兑换券，5佣金 10有效期 天 | internal | business-field | semantic-review-required |
| 14 | `operation_type` | `int(11)` | 否 |  |  | 操作方式：0 用户，1管理员,3 共享用户 | internal | business-field | semantic-review-required |
| 15 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 16 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 17 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 18 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 19 | `merger_value` | `decimal(10,2)` | 否 |  |  | 合并过来的余额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  |  | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_value` | `decimal(10,2)` | 否 |  |  | 操作后值 | internal | business-field | semantic-review-required |
| 22 | `p_card_id` | `int(11)` | 否 |  |  | 储值卡id | internal | relation-key | server-filter-only |
| 23 | `p_card_child_id` | `int(11)` | 是 |  |  | 卡样子ID | internal | relation-key | server-filter-only |
| 24 | `is_first` | `int(11)` | 否 |  |  | 是否第一次记录 | internal | business-field | semantic-review-required |
| 25 | `user_type` | `int(11)` | 否 |  |  | 账户类型 0顾客 1商家 | internal | business-field | semantic-review-required |
| 26 | `store_amount` | `decimal(10,2)` | 否 |  |  | 商家操作后的金额 | internal | business-field | semantic-review-required |
| 27 | `form_id` | `varchar(50)` | 是 |  |  | 小程序formid | internal | relation-key | server-filter-only |
| 28 | `note` | `varchar(100)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 29 | `pay_order_no` | `varchar(255)` | 是 |  |  | 交易流水号 | internal | business-field | semantic-review-required |
| 30 | `is_coupon` | `int(11)` | 否 |  | 0 | 是否使用优惠券 | internal | business-field | semantic-review-required |
| 31 | `pay_rate` | `decimal(4,2)` | 否 |  | 0.00 | 提现费率 | internal | business-field | semantic-review-required |
| 32 | `risk_control_reason` | `int(11)` | 否 |  | 0 | 风控原因0默认 1店主本人超限，2储值卡销售为0时超限，3未完善店铺信息，4付款超限，5购卡超限 | internal | business-field | semantic-review-required |
| 33 | `consumption_sum` | `int(11)` | 否 |  | 0 | 消费次数 | internal | business-field | semantic-review-required |
| 34 | `print_no` | `int(11)` | 否 |  | 0 | 打印机编码 | internal | business-field | semantic-review-required |
| 35 | `is_card_operation` | `tinyint(1)` | 否 |  | 0 | 是否卡调整记录 | internal | business-field | semantic-review-required |
| 36 | `is_integral` | `tinyint(1)` | 否 |  | 0 | 是否使用积分 | internal | business-field | semantic-review-required |
| 37 | `is_service` | `tinyint(1)` | 否 |  | 0 | 是否包含服务 | internal | business-field | semantic-review-required |
| 38 | `is_product` | `tinyint(1)` | 否 |  | 0 | 是否包含商品 | internal | business-field | semantic-review-required |
| 39 | `is_date` | `tinyint(1)` | 否 |  |  | 是否包含有效期 | internal | business-field | semantic-review-required |
| 40 | `is_shop` | `tinyint(1)` | 否 |  | 0 | 是否是商城订单 | internal | business-field | semantic-review-required |
| 41 | `is_food` | `tinyint(1)` | 否 |  | 0 | 是否是点餐订单 | internal | business-field | semantic-review-required |
| 42 | `is_reservation` | `tinyint(1)` | 否 |  |  | 是否关联预约 | internal | business-field | semantic-review-required |
| 43 | `is_performance` | `tinyint(1)` | 否 |  | 0 | 是否是开启了绩效的订单 | internal | business-field | semantic-review-required |
| 44 | `business_remark` | `varchar(100)` | 是 |  |  | 商家备注 | sensitive-unstructured | business-field | deny |
| 45 | `is_show_remark` | `tinyint(1)` | 否 |  | 0 | 是否向顾客展示备注 | sensitive-unstructured | business-field | deny |
| 46 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 47 | `is_commission` | `tinyint(1)` | 否 |  | 0 | 是否包含佣金 | internal | business-field | semantic-review-required |
| 48 | `is_axc` | `tinyint(1)` | 否 |  | 0 | 是否安心充订单 | internal | business-field | semantic-review-required |
| 49 | `is_alliance` | `tinyint(1)` | 否 |  | 0 | 是否为联盟订单 | internal | business-field | semantic-review-required |
| 50 | `is_refunds` | `tinyint(1)` | 否 |  | 0 | 是否退款 | internal | business-field | semantic-review-required |
| 51 | `is_balance_mergers` | `tinyint(1)` | 否 |  | 0 | 是否合并卡余额 | internal | business-field | semantic-review-required |
| 52 | `is_price` | `tinyint(1)` | 否 |  | 0 | 是否有金额详细信息 | internal | business-field | semantic-review-required |
| 53 | `secret_key` | `varchar(100)` | 是 |  |  | 兑换码 | restricted | business-field | deny |
| 54 | `out_trade_no` | `varchar(100)` | 是 |  |  | 外部交易单号，如：微信、支付宝 | internal | business-field | semantic-review-required |
| 55 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 56 | `combination_order` | `int(11)` | 否 |  | 0 | 组合订单 0非组合订单，1主订单 2子订单 | internal | business-field | semantic-review-required |
| 57 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 58 | `source_id` | `bigint(20)` | 是 |  |  | 源数据ID，退款关联 | internal | relation-key | server-filter-only |
| 59 | `device_code` | `varchar(50)` | 是 |  |  | 收款设备编号 | internal | business-field | semantic-review-required |
| 60 | `promote_user_id` | `int(11)` | 是 |  |  | 推荐人ID | internal | relation-key | server-filter-only |
| 61 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 62 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 63 | `refunds_reason` | `varchar(100)` | 是 |  |  | 退款失败原因 | internal | business-field | semantic-review-required |
| 64 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 65 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 66 | `update_by` | `int(11)` | 是 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 67 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 68 | `real_date` | `datetime` | 是 |  | CURRENT_TIMESTAMP | 真实的服务器时间、东八区时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_performance`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `performance_item_id` | `int(11)` | 否 |  |  | 统计方式ID | internal | relation-key | server-filter-only |
| 4 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 5 | `consumption_tag` | `int(11)` | 是 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | internal | business-field | semantic-review-required |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  |  | 绩效总金额 | internal | business-field | semantic-review-required |
| 7 | `performance_item_type` | `int(11)` | 否 |  |  | 绩效统计方式 绩效统计方式类型（快照） 0销售绩效 1工作绩效 | internal | business-field | semantic-review-required |
| 8 | `performance_item_name` | `varchar(20)` | 是 |  |  | 绩效统计方式名称（快照 | internal | business-field | semantic-review-required |
| 9 | `remark` | `varchar(200)` | 是 |  |  | 备注 | sensitive-unstructured | business-field | deny |
| 10 | `flag_color` | `int(11)` | 否 |  |  | 标记颜色 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | -1关闭设置  0 待设置 1 已设置 -2不适用绩效 -3未启用的绩效方式  -4删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）
- `index_sid`：非唯一 BTREE（store_id）

### `consumption_performance_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效关联项目

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_id` | `bigint(20)` | 否 | MUL |  | 绩效订单ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL | 0 | 订单ID | internal | relation-key | server-filter-only |
| 5 | `prepaid_card_id` | `int(11)` | 否 |  | 0 | 充值卡ID | restricted | relation-key | deny |
| 6 | `performance_price` | `decimal(18,2)` | 否 |  | 0.00 | 绩效金额 | internal | business-field | semantic-review-required |
| 7 | `service_item_id` | `int(11)` | 否 |  |  | 服务ID | internal | relation-key | server-filter-only |
| 8 | `service_item_name` | `varchar(20)` | 是 |  |  | 服务名称 | internal | business-field | semantic-review-required |
| 9 | `service_item_unit` | `varchar(20)` | 是 |  | 次 | 服务单位 | internal | business-field | semantic-review-required |
| 10 | `service_item_count` | `int(11)` | 否 |  | 0 | 服务次数 | internal | business-field | semantic-review-required |
| 11 | `state` | `int(11)` | 否 |  |  | 状态 1正常 -1删除 | internal | business-field | semantic-review-required |
| 12 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 13 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 16 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_consumptionid`：非唯一 BTREE（consumption_id）
- `idx_consumptionperformanceid`：非唯一 BTREE（consumption_performance_id）

### `consumption_performance_item_staff`

类型：BASE TABLE；引擎：InnoDB；领域：staff-binding；隔离字段：store_id, tenant_id。
表注释：订单绩效项关联员工

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增ID | internal | relation-key | server-filter-only |
| 2 | `consumption_performance_item_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 3 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单绩效ID | internal | relation-key | server-filter-only |
| 4 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 服务ID | internal | relation-key | server-filter-only |
| 5 | `store_id` | `int(11)` | 否 | MUL |  | 店铺ID | internal | store-scope | server-filter-only |
| 6 | `staff_id` | `int(11)` | 否 |  |  | 员工ID | internal | subject-or-relation-key | server-filter-only |
| 7 | `royalty_price` | `decimal(10,0)` | 否 |  |  | 提成金额 | internal | business-field | semantic-review-required |
| 8 | `state` | `int(11)` | 否 |  |  |  1正常  -1 删除 | internal | business-field | semantic-review-required |
| 9 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 10 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 11 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 12 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 13 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `inx_cid`：非唯一 BTREE（consumption_id）
- `store_id`：非唯一 BTREE（store_id）

### `consumption_performance_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：订单绩效操作日志

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 自增主键 | internal | relation-key | server-filter-only |
| 2 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 3 | `consumption_id` | `bigint(20)` | 否 |  |  | 订单ID | internal | relation-key | server-filter-only |
| 4 | `consumption_performance_id` | `bigint(20)` | 否 |  |  | 订单关联绩效ID | internal | relation-key | server-filter-only |
| 5 | `method` | `varchar(50)` | 否 |  |  | 执行的方法名称 | internal | business-field | semantic-review-required |
| 6 | `operation_content` | `text` | 否 |  |  | 操作后的对象 JSON串 | sensitive-unstructured | business-field | deny |
| 7 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 8 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 9 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 10 | `tenant_id` | `int(11)` | 否 |  | 0 |  | internal | tenant-scope | server-filter-only |

索引：
- `PRIMARY`：唯一 BTREE（id）

### `consumption_price_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：消费财务记录

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `card_id` | `int(11)` | 否 |  |  | 会员卡id 无卡为0 | internal | subject-or-relation-key | server-filter-only |
| 4 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 5 | `uid` | `int(11)` | 否 | MUL |  | 用户id | internal | subject-or-relation-key | server-filter-only |
| 6 | `store_id` | `int(11)` | 否 | MUL |  | 商家id | internal | store-scope | server-filter-only |
| 7 | `card_operation_id` | `int(11)` | 否 |  | 0 | 卡调整记录ID | internal | relation-key | server-filter-only |
| 8 | `card_type` | `int(11)` | 否 |  | 0 | 快照类型：0计次，1储值 2 限时卡 3权益卡 | internal | business-field | semantic-review-required |
| 9 | `pay_type` | `int(11)` | 否 |  |  | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 4优惠券支付 | internal | business-field | semantic-review-required |
| 10 | `card_discount` | `decimal(3,2)` | 否 |  |  | 会员折扣 | internal | business-field | semantic-review-required |
| 11 | `pay_model` | `int(11)` | 否 |  | 0 | 付款模式 0实付 1应付(不对金额做任何校验) | internal | business-field | semantic-review-required |
| 12 | `consumption_way` | `int(11)` | 否 |  | 0 | 付款通道：0 临时（领克先行），1 商户 | internal | business-field | semantic-review-required |
| 13 | `consumption_tag` | `int(11)` | 否 |  |  | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现   11 调整有效期 12转让 13受让 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 30退款 31退卡 | internal | business-field | semantic-review-required |
| 14 | `total_price` | `decimal(10,2)` | 否 |  |  | 应付金额 | internal | business-field | semantic-review-required |
| 15 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 16 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 17 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 18 | `card_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 折扣金额 | internal | business-field | semantic-review-required |
| 19 | `merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 未使用消费金额 | internal | business-field | semantic-review-required |
| 20 | `other_value` | `decimal(10,2)` | 否 |  | 0.00 | 如果是充值 则记录次数或者其他值 | internal | business-field | semantic-review-required |
| 21 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后正金 | internal | business-field | semantic-review-required |
| 22 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后赠金 | internal | business-field | semantic-review-required |
| 23 | `after_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后以优惠金额 | internal | business-field | semantic-review-required |
| 24 | `after_merger_discount_price` | `decimal(10,2)` | 否 |  | 0.00 | 操作后未优惠金额 | internal | business-field | semantic-review-required |
| 25 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 26 | `is_bookkeeping` | `tinyint(1)` | 否 |  | 1 | 是否记账 | internal | business-field | semantic-review-required |
| 27 | `pay_way` | `int(11)` | 否 |  |  | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | internal | business-field | semantic-review-required |
| 28 | `pay_channel` | `int(11)` | 否 |  | 0 | 支付渠道 0坚果卡包 1直连 2付呗间联 | internal | business-field | semantic-review-required |
| 29 | `tenant_id` | `int(11)` | 否 | MUL |  | 租户id | internal | tenant-scope | server-filter-only |
| 30 | `state` | `int(11)` | 否 |  |  | 状态 1成功 0待入账 -1删除 | internal | business-field | semantic-review-required |
| 31 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 32 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 33 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 34 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `idx_tenantId`：非唯一 BTREE（tenant_id, card_id）
- `idx_uid_cardid_storeid`：非唯一 BTREE（uid, card_id, store_id）
- `index_storeId`：非唯一 BTREE（store_id）

### `consumption_product`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：财务记录商品关联表

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `pid` | `int(11)` | 否 |  |  | 商品ID | internal | business-field | semantic-review-required |
| 4 | `p_title` | `varchar(100)` | 否 |  |  | 商品标题 | internal | business-field | semantic-review-required |
| 5 | `p_img` | `varchar(200)` | 是 |  |  | 商品图片 | internal | business-field | semantic-review-required |
| 6 | `sku_id` | `int(11)` | 是 |  |  | SKU ID | internal | relation-key | server-filter-only |
| 7 | `sku_name` | `varchar(20)` | 是 |  |  | SKU 名称 | internal | business-field | semantic-review-required |
| 8 | `num` | `int(11)` | 否 |  |  | 数量 | internal | business-field | semantic-review-required |
| 9 | `price` | `decimal(10,2)` | 否 |  |  | 价格 | internal | business-field | semantic-review-required |
| 10 | `total_price` | `decimal(10,2)` | 否 |  |  | 总价 | internal | business-field | semantic-review-required |
| 11 | `discount_price` | `decimal(10,2)` | 否 |  |  | 折扣金额 | internal | business-field | semantic-review-required |
| 12 | `pay_price` | `decimal(10,2)` | 否 |  |  | 实付金额 | internal | business-field | semantic-review-required |
| 13 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 14 | `state` | `int(11)` | 否 |  |  | 状态 | internal | business-field | semantic-review-required |
| 15 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 16 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 17 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 18 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_service_item`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | 主键id | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 | MUL |  | 财务id | internal | relation-key | server-filter-only |
| 3 | `item_id` | `int(11)` | 否 |  |  | 项目id | internal | relation-key | server-filter-only |
| 4 | `consumption_value` | `decimal(10,2)` | 否 |  |  | 消费值 | internal | business-field | semantic-review-required |
| 5 | `price` | `decimal(10,2)` | 否 |  | 0.00 | 单价 | internal | business-field | semantic-review-required |
| 6 | `pay_price` | `decimal(10,2)` | 否 |  | 0.00 | 实付金额 | internal | business-field | semantic-review-required |
| 7 | `total_price` | `decimal(10,2)` | 否 |  | 0.00 | 应付金额 | internal | business-field | semantic-review-required |
| 8 | `normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金 | internal | business-field | semantic-review-required |
| 9 | `give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金 | internal | business-field | semantic-review-required |
| 10 | `after_value` | `decimal(10,2)` | 否 |  | 0.00 | 操作后值 | internal | business-field | semantic-review-required |
| 11 | `after_normal_value` | `decimal(10,2)` | 否 |  | 0.00 | 正金余额 | internal | business-field | semantic-review-required |
| 12 | `after_give_value` | `decimal(10,2)` | 否 |  | 0.00 | 赠金余额 | internal | business-field | semantic-review-required |
| 13 | `discount` | `decimal(10,2)` | 是 |  |  | 折扣 | internal | business-field | semantic-review-required |
| 14 | `pay_date` | `datetime` | 是 |  |  | 支付时间 | internal | business-field | semantic-review-required |
| 15 | `pay_by` | `int(11)` | 是 |  |  | 支付人 | internal | business-field | semantic-review-required |
| 16 | `integral_deduct` | `decimal(10,2)` | 是 |  |  | 积分扣除 | internal | business-field | semantic-review-required |
| 17 | `card_deduct` | `decimal(10,2)` | 是 |  |  | 会员卡扣除 | internal | business-field | semantic-review-required |
| 18 | `coupon_deduct` | `decimal(10,2)` | 是 |  |  | 优惠券扣除 | internal | business-field | semantic-review-required |
| 19 | `pay_method` | `int(11)` | 是 |  |  | 付款方式：0 会员卡支付、1微信支付、2支付宝支付 | internal | business-field | semantic-review-required |
| 20 | `tenant_id` | `int(11)` | 否 |  |  | 租户id | internal | tenant-scope | server-filter-only |
| 21 | `state` | `int(11)` | 是 |  |  | 状态：0待付款 1已付款  | internal | business-field | semantic-review-required |
| 22 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |
| 23 | `update_date` | `datetime` | 否 |  |  |  | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
- `index_cid`：非唯一 BTREE（consumption_id）

### `consumption_validity_date_log`

类型：BASE TABLE；引擎：InnoDB；领域：payment-finance；隔离字段：store_id, tenant_id。
表注释：无

| 序号 | 字段 | 类型 | 可空 | 键 | 默认值 | 注释 | 敏感级别 | 范围角色 | 查询策略 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `id` | `bigint(20)` | 否 | PRI |  | ID | internal | relation-key | server-filter-only |
| 2 | `consumption_id` | `bigint(20)` | 否 |  |  | 消费ID | internal | relation-key | server-filter-only |
| 3 | `store_id` | `int(11)` | 否 |  |  | 店铺ID | internal | store-scope | server-filter-only |
| 4 | `uid` | `int(11)` | 否 |  |  | 用户ID | internal | subject-or-relation-key | server-filter-only |
| 5 | `card_id` | `int(11)` | 否 |  |  | 会员卡ID | internal | subject-or-relation-key | server-filter-only |
| 6 | `child_card_id` | `int(11)` | 否 |  | 0 | 子会员卡ID | internal | relation-key | server-filter-only |
| 7 | `consumption_tag` | `int(11)` | 否 |  |  |  0支出 ，1增加,2 核减，3返还，4赠送，5付款,6初始化，8过期 | internal | business-field | semantic-review-required |
| 8 | `consumption_value` | `int(11)` | 否 |  |  | 调整天数 | internal | business-field | semantic-review-required |
| 9 | `after_validity_date` | `date` | 是 |  |  | 到期时间 | internal | business-field | semantic-review-required |
| 10 | `state` | `int(11)` | 否 |  |  | 状态1正常 | internal | business-field | semantic-review-required |
| 11 | `tenant_id` | `int(11)` | 否 |  |  | 租户ID | internal | tenant-scope | server-filter-only |
| 12 | `update_by` | `int(11)` | 否 |  |  | 修改人 | internal | business-field | semantic-review-required |
| 13 | `update_date` | `datetime` | 否 |  |  | 修改时间 | internal | business-field | semantic-review-required |
| 14 | `create_by` | `int(11)` | 否 |  |  | 创建人 | internal | business-field | semantic-review-required |
| 15 | `create_date` | `datetime` | 否 |  |  | 创建时间 | internal | business-field | semantic-review-required |

索引：
- `PRIMARY`：唯一 BTREE（id）
