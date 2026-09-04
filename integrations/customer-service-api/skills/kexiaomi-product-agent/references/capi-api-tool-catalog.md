# 课小秘 顾客视角 API 工具筛选目录

> 内部 AI 工具目录。只用于选择和约束 API 调用，不得把路由、内部类型、鉴权字段、Provider 名称或内部主键直接回复给客户。

## 目录元数据

- 源项目：`LingKe.CApi`（`Public/LingKe/Link.CApi`）
- 目标框架：`.NET 8 / ASP.NET Core Controller API`
- 视角：`顾客视角`
- 源码提交：`07b36b96d`
- 生成日期：`2026-09-03`
- Controller 数：`38`
- 实际 Http Action 数：`214`
- 工具等级：`A=0`、`B=110`、`C=11`、`D=93`
- Controller 源码指纹：`sha256:e9802bff7a1437a2f128588564b273f128dd2d06e28bf19bcc1da5c8a2c380e5`
- 机器目录：`capi-api-tool-manifest.json`（所有工具默认关闭）

## 使用边界

- 本目录从当前 Controller、DTO、继承字段、代码内 `if` 校验和一层 Provider/Service 调用静态生成；静态结果不是生产可用性证明。
- A/B/C 级才会提供详细契约。D 级仍保留完整 Action 索引和排除原因，但不得注册为客服查询工具。
- `Uid`、`StoreId`、`AppId` 和内部业务 ID 不能由模型猜测；必须由已验证会话注入，或来自同一会话上游 API 的服务端引用。
- `[Required]` 只代表模型特性声明。值类型默认值和 Controller 条件会改变真实必填性，因此每个字段同时列出代码校验证据。
- 空集合只表示本次条件没有匹配结果，不能自行推断对象不存在、已经删除或某个业务原因成立。
- 当前查询只能证明调用时事实。历史问题必须使用明确的日志、记录或历史接口，不能用当前状态冒充过去状态。
- 直接响应可能含个人信息、内部 ID 或凭据字段；调用执行器必须按目录标记做最小化投影，不能把完整响应无条件交给模型。
- C 端与商家端即使 Action 同名，也代表不同视角；需要解释差异时应分别取证，不能互相替代。
- 文档中的使用时机只是能力理解示例，不是运行时问题路由；机器目录不包含问题关键词、固定场景到接口映射或固定回答。

## Agent 选取与调用流程

1. 商家反馈顾客端问题时，先要求商家提供顾客手机号，并确认问题所属门店。手机号只交给受控身份解析流程，不直接拼入任意查询参数。
2. 服务端在已确认门店范围内把手机号解析为目标会员引用；存在同号多会员、跨门店歧义或未找到时停止调用并返回可核实提示。
3. 由执行器注入目标会员 `Uid`、门店 `StoreId`、应用 `AppId` 等上下文，再选择本目录中的 C 端候选查询工具。模型不得生成或改写这些身份值。
4. 只把本次问题需要的脱敏字段交给模型；若需解释商家与顾客看到的数据差异，再调用商家端对应工具交叉核对。

### 给工具筛选器的检索建议

- 不要把整份目录一次性放入模型上下文。先按问题域、工具编号、用途和使用时机召回少量候选，再读取对应的详细契约。
- 第一轮优先 A/B 级；只有候选不足且有人工审批时才考虑 C 级。D 级只用于审计覆盖，不参与召回。
- 同一问题需要多步查询时，上一步返回的内部 ID 只能作为执行器保存的服务端引用传给下一步，不能暴露给模型自由改写。
- 典型顺序是“定位主体 → 查询列表/概览 → 用上游引用查询详情 → 必要时做 C/B 对照”，避免无边界批量拉取。

## 公共响应包装

| 包装 | 字段 | 含义 |
| --- | --- | --- |
| `DataResult<T>` | `State`、`StatusCode`、`Message`、`MsgType`、`Data` | 单对象结果；只有 `State=true` 才能把 `Data` 当成功事实 |
| `DataList<T>` | 上述状态字段及 `PageIndex`、`PageSize`、`PageCount`、`TotalCount`、`Data` | 分页列表；空列表不能解释为空的业务原因 |
| `PageData<T>` | `PageIndex`、`PageSize`、`PageCount`、`TotalCount`、`IsNext`、`Data` | 常作为 `DataResult<T>.Data` 的分页载荷 |

## 工具等级

| 等级 | 含义 | 运行要求 |
| --- | --- | --- |
| A | 静态路径未发现参数或明显副作用 | 仍需 AI 专用部署的只读验收 |
| B | 候选只读接口，但需要身份注入、上游对象引用或响应脱敏 | 满足约束后才可注册 |
| C | 查询路径存在疑似副作用、凭据参数或语义不充分 | 人工复核通过前不开放 |
| D | 写接口、登录、回调、测试或无法证明只读 | 永久排除或另行审批 |

## 全部 Action 索引

| 工具编号 | 业务域 | 方法与路由 | 摘要/用途 | 鉴权 | 等级 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| `capi.activity.activity_get_info` | Activity 模块 | `POST /api/Activity/ActivityGetInfo` | 获取活动详情 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：UserCouponProvider.UserCouponAdd, ActivityLogProvider.ActivityLogAdd |
| `capi.activity.activity_qr_code_share` | Activity 模块 | `POST /api/Activity/ActivityQrCodeShare` | 生成活动二维码 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.activity.activity_share` | Activity 模块 | `POST /api/Activity/ActivityShare` | 分享活动 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.activity.get_business_new_activity` | Activity 模块 | `POST /api/Activity/GetBusinessNewActivity` | 获取店铺最新活动详情 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.ali_pay.auth_token_app` | AliPay 模块 | `POST /api/AliPay/AuthTokenApp` | 支付宝授权 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.ali_pay.login_user` | AliPay 模块 | `POST /api/AliPay/LoginUser` | 支付宝登录 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.ali_pay.pay` | AliPay 模块 | `POST /api/AliPay/Pay` | 获取Js签名 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.ali_pay.result_notify` | AliPay 模块 | `POST /api/AliPay/ResultNotify` | 获取异步支付通知 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.ali_pay.user_authorization` | AliPay 模块 | `POST /api/AliPay/UserAuthorization` | 支付宝授权修改用户数据 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.ali_pay.user_mobile_decryption` | AliPay 模块 | `POST /api/AliPay/UserMobileDecryption` | 支付宝解密手机号 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.article.article_get` | Article 模块 | `POST /api/Article/ArticleGet` | 获取文章详情 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.article.article_get_list` | Article 模块 | `POST /api/Article/ArticleGetList` | 获取文章列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.base.get_areas` | Base 模块 | `POST /api/Base/GetAreas` | 获取省市数据 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.base.get_province_data` | Base 模块 | `POST /api/Base/GetProvinceData` | 获取省市数据 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.base.get_week_data` | Base 模块 | `POST /api/Base/GetWeekData` | 获取星期数据 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.commission.apply_cash_out` | Commission 模块 | `POST /api/Commission/ApplyCashOut` | 用户申请佣金提现 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.commission.get_commission_cashout_logs` | Commission 模块 | `POST /api/Commission/GetCommissionCashoutLogs` | 获取用户佣金提现记录 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.commission.get_user_cash_info` | Commission 模块 | `POST /api/Commission/GetUserCashInfo` | 获取用户佣金提现信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.commission.get_user_commission_log_list` | Commission 模块 | `POST /api/Commission/GetUserCommissionLogList` | 获取用户佣金消费明细 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.common.check_new_version` | Common 模块 | `POST /api/Common/CheckNewVersion` | 检查版本更新 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.common.check_state` | Common 模块 | `POST /api/Common/CheckState` | 校验用户状态(Y) | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.common.get_oss_conf` | Common 模块 | `POST /api/Common/GetOssConf` | 获取OSS配置信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.common.send_sms` | Common 模块 | `POST /api/Common/SendSms` | 发送手机验证码 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.common.upload_file` | Common 模块 | `POST /api/Common/UploadFile` | 上传文件 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.common.upload_file_for_xcx` | Common 模块 | `POST /api/Common/UploadFileForXcx` | 上传文件for小程序 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.common.upload_files` | Common 模块 | `POST /api/Common/UploadFiles` | OSS上传文件后回调借口 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.content.add_banner_log` | Content 模块 | `POST /api/Content/AddBannerLog` | 记录Banner日志 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.content.filter_word` | Content 模块 | `POST /api/Content/FilterWord` | 过滤敏感词 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.content.get_index_banner` | Content 模块 | `POST /api/Content/GetIndexBanner` | 获取首页Banner | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.device.device_init` | Device 模块 | `POST /api/pos/deviceInit/1.0` | 设备初始化 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.device.get_pos_params` | Device 模块 | `POST /api/Device/GetPosParams` | 获取设备支付参数 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.device.pos_order_detail` | Device 模块 | `POST /api/pos/orderDetail/1.0` | 订单查询 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.device.pos_pay` | Device 模块 | `POST /api/pos/pay/1.0` | 订单支付 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.fu_bei.unified_pay_call_back` | FuBei 模块 | `POST /api/FuBei/UnifiedPayCallBack` | 支付回调方法 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.log.push_share_log` | Log 模块 | `POST /api/Log/PushShareLog` | 写入分享日志 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.lottery.get_lottery_by_id` | Lottery 模块 | `POST /api/Lottery/GetLotteryById` | 获取活动详情 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：LotteryUserProvider.LotteryUserAddLotteryCount, PromoteUsersProvider.BindPromoteUser, ActivityLogProvider.ActivityLogAdd |
| `capi.lottery.user_lottery` | Lottery 模块 | `POST /api/Lottery/UserLottery` | 抽奖 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.poster.get_poster_list` | Poster 模块 | `POST /api/Poster/GetPosterList` | 获取海报列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.promote.bind_promote_user` | Promote 模块 | `POST /api/Promote/BindPromoteUser` | 绑定推广人 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.promote.get_promote_user_count` | Promote 模块 | `POST /api/Promote/GetPromoteUserCount` | 获取推荐人数 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.promote.get_promote_user_list` | Promote 模块 | `POST /api/Promote/GetPromoteUserList` | 获取推荐人列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.search.get_serarch_hot` | Search 模块 | `POST /api/Search/GetSerarchHot` | 获取搜索热词 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.shopping_cart.add_product` | ShoppingCart 模块 | `POST /api/ShoppingCart/AddProduct` | 添加商品至购物车 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.shopping_cart.edit_product` | ShoppingCart 模块 | `POST /api/ShoppingCart/EditProduct` | 修改购物车商品数量 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.shopping_cart.get_shopping_cart` | ShoppingCart 模块 | `POST /api/ShoppingCart/GetShoppingCart` | 获取用户购物车 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.shopping_cart.remove_product` | ShoppingCart 模块 | `POST /api/ShoppingCart/RemoveProduct` | 从购物车删除商品 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.template.get_template` | Template 模块 | `POST /api/Template/GetTemplate` | 获取页面模板 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.test.test_pay_success` | Test 模块 | `POST /api/Test/TestPaySuccess` | 支付成功回调测试 | 需要登录 | D | 测试、模板测试或后台认证 Controller，不进入客服工具。 |
| `capi.union_pay.get_js_pay_param` | UnionPay 模块 | `POST /api/UnionPay/GetJsPayParam` | 获取Js签名 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.union_pay.login_user` | UnionPay 模块 | `POST /api/UnionPay/LoginUser` | 云闪付登录 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.wei_xin.admin_login` | WeiXin 模块 | `POST /api/WeiXin/AdminLogin` | 管理员微信登录 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.wei_xin.check_user_is_attention_official_account` | WeiXin 模块 | `POST /api/WeiXin/CheckUserIsAttentionOfficialAccount` | 判断当前用户是否关注公众号 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：WechatAttentionProvider.GetOpenIdListByUid |
| `capi.wei_xin.get_js_pay_param` | WeiXin 模块 | `POST /api/WeiXin/GetJsPayParam` | 获取Js签名 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.wei_xin.get_js_signature` | WeiXin 模块 | `POST /api/WeiXin/GetJsSignature` | 获取Js签名 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.wei_xin.login_user` | WeiXin 模块 | `POST /api/WeiXin/LoginUser` | 微信接口跳转 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.wei_xin.result_notify` | WeiXin 模块 | `POST /api/WeiXin/ResultNotify` | 获取异步支付通知 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.wei_xin.user_authorization` | WeiXin 模块 | `POST /api/WeiXin/UserAuthorization` | 微信授权修改用户数据 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.wei_xin.user_mobile_decryption` | WeiXin 模块 | `POST /api/WeiXin/UserMobileDecryption` | 微信解密手机号 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.wei_xin.we_chat_call_back` | WeiXin 模块 | `POST /api/WeiXin/WeChatCallBack` | 公众号异步消息处理 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.yop_pay.pay_notify_url` | YopPay 模块 | `POST /api/YopPay/PayNotifyUrl` | 获取宜宝支付结果异步通知 | 需要登录 | D | 登录、回调或通知入口，不是只读业务查询。 |
| `capi.coupon.check_user_coupon_used` | 优惠券 | `POST /api/Coupon/CheckUserCouponUsed` | 判断优惠券是否可用 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.coupon.coupoen_center_get_by_id` | 优惠券 | `POST /api/Coupon/CoupoenCenterGetById` | 通过优惠中心ID 获取优惠中心优惠券内容 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.coupon.coupon_h5_qr_code_share` | 优惠券 | `POST /api/Coupon/CouponH5QrCodeShare` | 生成H5营销活动 小程序码 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.coupon.coupon_qr_code_share` | 优惠券 | `POST /api/Coupon/CouponQrCodeShare` | 生成定向券二维码 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.coupon.exists_coupon_is_show` | 优惠券 | `POST /api/Coupon/ExistsCouponIsShow` | 检测用户是否有新的优惠券 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.coupon.full_money_coupon_get_list` | 优惠券 | `POST /api/Coupon/FullMoneyCouponGetList` | 满赠优惠券列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.coupon.get_alliance_coupon_list` | 优惠券 | `POST /api/Coupon/GetAllianceCouponList` | 获取联盟可领优惠券列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.coupon.get_marketing_center_coupons` | 优惠券 | `POST /api/Coupon/GetMarketingCenterCoupons` | 营销中心领取券页面获取优惠券列表 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：MarketingLogProvider.MarketingLogAdd |
| `capi.coupon.get_user_coupon` | 优惠券 | `POST /api/Coupon/GetUserCoupon` | 获取单个优惠券 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.coupon.get_user_coupon_count` | 优惠券 | `POST /api/Coupon/GetUserCouponCount` | 获取用户可用优惠券数量 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.coupon.get_user_coupon_list` | 优惠券 | `POST /api/Coupon/GetUserCouponList` | 获取优惠券列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.coupon.marketing_share_qr_code` | 优惠券 | `POST /api/Coupon/MarketingShareQrCode` | 生成营销活动领券二维码 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.coupon.receive_coupon` | 优惠券 | `POST /api/Coupon/ReceiveCoupon` | 领取优惠券 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.coupon.receive_marketing_center_coupons` | 优惠券 | `POST /api/Coupon/ReceiveMarketingCenterCoupons` | 营销中心领取券 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.coupon.user_coupon_used` | 优惠券 | `POST /api/Coupon/UserCouponUsed` | 使用优惠券 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.coupon.user_receive_coupon` | 优惠券 | `POST /api/Coupon/UserReceiveCoupon` | 用户领取优惠券 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.change_card_pass` | 会员与身份 | `POST /api/User/ChangeCardPass` | 修改会员卡密码 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.check_reset_card_pass_sms_code` | 会员与身份 | `POST /api/User/CheckResetCardPassSmsCode` | 校验重置会员密码的验证码 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.user.check_user_card_pass` | 会员与身份 | `POST /api/User/CheckUserCardPass` | 验证会员卡密码 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.user.check_user_mobile` | 会员与身份 | `POST /api/User/CheckUserMobile` | 检测手机号能否使用 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.user.get_content` | 会员与身份 | `POST /api/User/GetContent` | 分销说明 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.user.get_store_controls` | 会员与身份 | `POST /api/User/GetStoreControls` | 注册用户获取店铺用户自定义控件（会员编辑资料页） | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.user.get_store_user_info` | 会员与身份 | `POST /api/User/GetStoreUserInfo` | 加载用户信息（会员编辑资料页） | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.user.get_user_sign_agreement_info` | 会员与身份 | `POST /api/User/GetUserSignAgreementInfo` | 签署合同 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.user.has_set_card_pass` | 会员与身份 | `POST /api/User/HasSetCardPass` | 是否设置了会员卡密码 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.set_card_pass` | 会员与身份 | `POST /api/User/SetCardPass` | 设置会员卡密码 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.set_store_user_info` | 会员与身份 | `POST /api/User/SetStoreUserInfo` | 修改用户信息（会员编辑资料页） | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.set_user_mobile` | 会员与身份 | `POST /api/User/SetUserMobile` | 修改手机号码（会员编辑资料页） | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.set_user_nick` | 会员与身份 | `POST /api/User/SetUserNick` | 修改用户昵称 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.store_user_add` | 会员与身份 | `POST /api/User/StoreUserAdd` | 注册店铺会员 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.update_user_image` | 会员与身份 | `POST /api/User/UpdateUserImage` | 更新头像 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.user_bind_store_user_card` | 会员与身份 | `POST /api/User/UserBindStoreUserCard` | 用户绑定店铺会员 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.user_sign_agreement` | 会员与身份 | `POST /api/User/UserSignAgreement` | 签署合同 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.user.user_vip_info` | 会员与身份 | `POST /api/User/UserVipInfo` | 获取用户会员信息 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：UserCardProvider.BusinessBindUserCard |
| `capi.card.activation_user_card` | 会员卡与课卡 | `POST /api/Card/ActivationUserCard` | 重新会员卡 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.card.active_alipay_card` | 会员卡与课卡 | `POST /api/Card/ActiveAlipayCard` | 激活支付宝会员卡 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.card.cancel_user_card` | 会员卡与课卡 | `POST /api/Card/CancelUserCard` | 注销会员卡 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.card.check_for_card_tag_and_user_mobile` | 会员卡与课卡 | `POST /api/Card/CheckForCardTagAndUserMobile` | 检测会员卡预留手机号与当前会员绑定手机号是否一致 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.check_new_user_card` | 会员卡与课卡 | `POST /api/Card/CheckNewUserCard` | 检查是否有新会员卡（第三方开卡所用） | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：StoreCardProvider.GetAddCardSignature |
| `capi.card.get_card_interests` | 会员卡与课卡 | `POST /api/Card/GetCardInterests` | 获取会员卡权益 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_card_transfer_info_by_id` | 会员卡与课卡 | `POST /api/Card/GetCardTransferInfoById` | 根据转让秘钥获取单个充值卡 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.card.get_prepaid_card_qr_code` | 会员卡与课卡 | `POST /api/Card/GetPrepaidCardQrCode` | 获取购买储值卡的二维码 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_store_card_agreement` | 会员卡与课卡 | `POST /api/Card/GetStoreCardAgreement` | 获取会员协议 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_store_free_card` | 会员卡与课卡 | `POST /api/Card/GetStoreFreeCard` | 获取商家权益卡 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_store_prepaid_card_by_id` | 会员卡与课卡 | `POST /api/Card/GetStorePrepaidCardById` | 获取商家单个充值卡 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_store_prepaid_card_by_key` | 会员卡与课卡 | `POST /api/Card/GetStorePrepaidCardByKey` | 根据兑换秘钥获取商家单个充值卡 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_store_prepaid_card_by_random_param` | 会员卡与课卡 | `POST /api/Card/GetStorePrepaidCardByRandomParam` | 根据转让秘钥获取单个充值卡 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：CardPasswordProvider.CardPasswordUpdateState |
| `capi.card.get_store_prepaid_cards` | 会员卡与课卡 | `POST /api/Card/GetStorePrepaidCards` | 获取商家所有充值卡 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_user_cancel_cards` | 会员卡与课卡 | `POST /api/Card/GetUserCancelCards` | 获取用户注销会员卡列表 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.card.get_user_card` | 会员卡与课卡 | `POST /api/Card/GetUserCard` | 获取用户单个会员卡 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_user_card_by_prepaid_card_id` | 会员卡与课卡 | `POST /api/Card/GetUserCardByPrepaidCardId` | 通过储值卡Id查询用户会员卡 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_user_card_child_qr_code` | 会员卡与课卡 | `POST /api/Card/GetUserCardChildQrCode` | 获取单个会员子卡的二维码 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_user_cards` | 会员卡与课卡 | `POST /api/Card/GetUserCards` | 获取用户会员卡列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.get_user_child_card` | 会员卡与课卡 | `POST /api/Card/GetUserChildCard` | 获取会员的单张会员卡 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.card.transfer_card_balance_get_random_param` | 会员卡与课卡 | `POST /api/Card/TransferCardBalanceGetRandomParam` | 生成转让卡余额随机密钥 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.card.transferee_card` | 会员卡与课卡 | `POST /api/Card/TransfereeCard` | 受让卡余额 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.shopping_mall.get_business_products_message_by_product_id` | 商城 | `POST /api/ShoppingMall/GetBusinessProductsMessageByProductId` | 根据商品ID获取商品信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.shopping_mall.get_products_class_by_store_id` | 商城 | `POST /api/ShoppingMall/GetProductsClassByStoreId` | 根据门店ID获取B端商品分类集合 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.shopping_mall.get_products_list_by_key_word` | 商城 | `POST /api/ShoppingMall/GetProductsListByKeyWord` | 搜索商品 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.shopping_mall.get_products_list_by_store_id` | 商城 | `POST /api/ShoppingMall/GetProductsListByStoreId` | 根据分类展示商品列表接口 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.customer_service.consult` | 客服 | `POST /api/CustomerService/Consult` | 商务咨询 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.complaint.add_complaint` | 投诉与客服 | `POST /api/Complaint/AddComplaint` | 提交投诉\举报 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.complaint.get_complaint_info` | 投诉与客服 | `POST /api/Complaint/GetComplaintInfo` | 查看投诉详情 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.complaint.get_complaint_list` | 投诉与客服 | `POST /api/Complaint/GetComplaintList` | 查看投诉列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.message.get_list` | 消息 | `POST /api/Message/GetList` | 获取消息列表(Y) | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.message.get_message` | 消息 | `POST /api/Message/GetMessage` | 获取单个消息(Y) | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：RelUserMessageProvider.UpdateState |
| `capi.message.get_new_message_count` | 消息 | `POST /api/Message/GetNewMessageCount` | 获取未读消息数量 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.message.ignore_all` | 消息 | `POST /api/Message/IgnoreAll` | 忽略全部消息(Y) | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.consumption.consumption_add_pay_order` | 消费与核销 | `POST /api/Consumption/ConsumptionAddPayOrder` | 新增付款订单 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.consumption.consumption_by_card` | 消费与核销 | `POST /api/Consumption/ConsumptionByCard` | 用户会员卡消费 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.consumption.get_pay_after_marketing` | 消费与核销 | `POST /api/Consumption/GetPayAfterMarketing` | 获取支付后营销活动 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.consumption.get_user_consumption_info` | 消费与核销 | `POST /api/Consumption/GetUserConsumptionInfo` | 获取单个消费明细信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.consumption.get_user_consumption_list` | 消费与核销 | `POST /api/Consumption/GetUserConsumptionList` | 获取消费明细列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.consumption.get_user_recharge_list` | 消费与核销 | `POST /api/Consumption/GetUserRechargeList` | 获取充值记录列表 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.consumption.receive_physical_card` | 消费与核销 | `POST /api/Consumption/ReceivePhysicalCard` | 领取实体卡 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.integral.get_integral_detail` | 积分 | `POST /api/Integral/GetIntegralDetail` | 获取用户积分明细 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.integral.get_integral_summary` | 积分 | `POST /api/Integral/GetIntegralSummary` | 获取用户积分汇总 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.order.add_order` | 订单 | `POST /api/Order/AddOrder` | 添加订单 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.order.order_get` | 订单 | `POST /api/Order/OrderGet` | 获取单一订单详情 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.order.order_get_list` | 订单 | `POST /api/Order/OrderGetList` | 获取订单列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.shop_order.cancel_shop_order` | 订单 | `POST /api/ShopOrder/CancelShopOrder` | 取消订单 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.shop_order.create_shop_order` | 订单 | `POST /api/ShopOrder/CreateShopOrder` | 创建订单 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.shop_order.get_all_shop_orders` | 订单 | `POST /api/ShopOrder/GetAllShopOrders` | 获取所有订单 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.shop_order.get_shop_order_detail` | 订单 | `POST /api/ShopOrder/GetShopOrderDetail` | 获取订单详情 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.add_lessons_reservation` | 课次与排课 | `POST /api/Lessons/AddLessonsReservation` | 新增课程预约 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.lessons.add_lessons_reservation_check` | 课次与排课 | `POST /api/Lessons/AddLessonsReservationCheck` | 新增课程预约检查 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.lessons.get_course` | 课次与排课 | `POST /api/Lessons/GetCourse` | 获取单个课目 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.get_course_list` | 课次与排课 | `POST /api/Lessons/GetCourseList` | 获取课目列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.get_lessons` | 课次与排课 | `POST /api/Lessons/GetLessons` | 获取单个课程信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.get_lessons_rank` | 课次与排课 | `POST /api/Lessons/GetLessonsRank` | 获取上课排名 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.get_lessons_statistics` | 课次与排课 | `POST /api/Lessons/GetLessonsStatistics` | 获取上课统计 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.get_people_reservation_info` | 课次与排课 | `POST /api/Lessons/GetPeopleReservationInfo` | 获取个人预约信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.get_user_lessons_note` | 课次与排课 | `POST /api/Lessons/GetUserLessonsNote` | 获取会员上课笔记详细信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.get_user_lessons_note_list` | 课次与排课 | `POST /api/Lessons/GetUserLessonsNoteList` | 获取会员上课笔记列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.get_user_lessons_reservation_list` | 课次与排课 | `POST /api/Lessons/GetUserLessonsReservationList` | 获取会员已约列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.lessons.update_lessons_reservation_state` | 课次与排课 | `POST /api/Lessons/UpdateLessonsReservationState` | 修改课程状态 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.store_course.get_store_course_type` | 课程 | `POST /api/StoreCourse/GetStoreCourseType` | 获取当前店铺团课、私教课信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store.get_integral_description` | 门店 | `POST /api/Store/GetIntegralDescription` | 获取积分说明 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store.get_integral_set` | 门店 | `POST /api/Store/GetIntegralSet` | 获取积分设置 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.store.get_store_display_info` | 门店 | `POST /api/Store/GetStoreDisplayInfo` | 获取商户显示信息信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store.get_store_index_data` | 门店 | `POST /api/Store/GetStoreIndexData` | 获取首页展示功能模块及数据 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store.get_store_info` | 门店 | `POST /api/Store/GetStoreInfo` | 获取商户信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store.get_store_list` | 门店 | `POST /api/Store/GetStoreList` | 获取商户列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store.get_store_vacation` | 门店 | `POST /api/Store/GetStoreVacation` | 获取店铺放假时间 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store_item.add_service_cart` | 门店 | `POST /api/StoreItem/AddServiceCart` | 添加到购物车 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.store_item.edit_service_cart_count` | 门店 | `POST /api/StoreItem/EditServiceCartCount` | 修改服务的数量 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.store_item.get_service_cart` | 门店 | `POST /api/StoreItem/GetServiceCart` | 获取服务购物车 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store_item.get_service_list` | 门店 | `POST /api/StoreItem/GetServiceList` | 获取服务列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store_item.get_service_order_info` | 门店 | `POST /api/StoreItem/GetServiceOrderInfo` | 获取订单的详情 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.store_item.remove_all_service_cart_item` | 门店 | `POST /api/StoreItem/RemoveAllServiceCartItem` | 清空购物车 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.store_item.remove_service_cart_item` | 门店 | `POST /api/StoreItem/RemoveServiceCartItem` | 移除购物车子项 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.store_place.get_reservation_place` | 门店 | `POST /api/StorePlace/GetReservationPlace` | 获取预约场地 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：StorePlaceCloseSettingProvider.GetStorePlaceCloseSettingByStoreId |
| `capi.reservation.add_reservation` | 预约 | `POST /api/Reservation/AddReservation` | 新增预约 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.reservation.cancel_reservation` | 预约 | `POST /api/Reservation/CancelReservation` | 取消预约 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.reservation.get_course_card_bind_info` | 预约 | `POST /api/Reservation/GetCourseCardBindInfo` | 获取课卡绑定信息 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.reservation.get_course_list` | 预约 | `POST /api/Reservation/GetCourseList` | 获取课程列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_group_course_class_tag` | 预约 | `POST /api/Reservation/GetGroupCourseClassTag` | 获取团课分类信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_group_course_list_v2` | 预约 | `POST /api/Reservation/GetGroupCourseListV2` | 获取团课列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_group_course_list_v3` | 预约 | `POST /api/Reservation/GetGroupCourseListV3` | 获取团课列表分页 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_group_course_people_list` | 预约 | `POST /api/Reservation/GetGroupCoursePeopleList` | 获取课程预约人员列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_group_course_week_list_v2` | 预约 | `POST /api/Reservation/GetGroupCourseWeekListV2` | 获取团课周课列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_lessons_reservation_calender_v2` | 预约 | `POST /api/Reservation/GetLessonsReservationCalenderV2` | 获取课程日历可预约时间V2 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_miss_appointment_penalty_explain` | 预约 | `POST /api/Reservation/GetMissAppointmentPenaltyExplain` | 获取旷课爽约惩罚说明 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_private_lessons_reservation_time_seting` | 预约 | `POST /api/Reservation/GetPrivateLessonsReservationTimeSeting` | 获取私教预约时间段 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：StaffPrivateLessonSetProvider.GetStaffPrivateLessonSet |
| `capi.reservation.get_private_staff` | 预约 | `POST /api/Reservation/GetPrivateStaff` | 获取私教教练 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_reservation_by_id` | 预约 | `POST /api/Reservation/GetReservationById` | 获取已约列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_reservation_calender` | 预约 | `POST /api/Reservation/GetReservationCalender` | 获取日历不可预约时间 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_reservation_controls_list` | 预约 | `POST /api/Reservation/GetReservationControlsList` | 获取自定义控件列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_reservation_list` | 预约 | `POST /api/Reservation/GetReservationList` | 获取已约列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_reservation_time_seting` | 预约 | `POST /api/Reservation/GetReservationTimeSeting` | 获取预约时间段 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_staff_info` | 预约 | `POST /api/Reservation/GetStaffInfo` | 获取教练详情 | 需要登录 | C | 查询路径包含疑似写入或外部副作用调用，必须人工复核：StaffPrivateLessonSetProvider.GetStaffPrivateLessonSet |
| `capi.reservation.get_staff_service_item_list` | 预约 | `POST /api/Reservation/GetStaffServiceItemList` | 获取商户信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_store_reservation_seting` | 预约 | `POST /api/Reservation/GetStoreReservationSeting` | 获取商家预约设置 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.get_work_staff_list` | 预约 | `POST /api/Reservation/GetWorkStaffList` | 工作技师列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.reservation.update_reservation` | 预约 | `POST /api/Reservation/UpdateReservation` | 修改预约 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.add_user_address` | 餐饮订单 | `POST /api/Food/AddUserAddress` | 新增用户地址信息 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.cancel_order` | 餐饮订单 | `POST /api/Food/CancelOrder` | 取消订单 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.create_food_order` | 餐饮订单 | `POST /api/Food/CreateFoodOrder` | 创建订单 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.create_food_order_again` | 餐饮订单 | `POST /api/Food/CreateFoodOrderAgain` | 再来一单 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.delete_user_address` | 餐饮订单 | `POST /api/Food/DeleteUserAddress` | 删除用户地址 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.food_cart_add` | 餐饮订单 | `POST /api/Food/FoodCartAdd` | 添加菜品到购物车 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.food_cart_clear` | 餐饮订单 | `POST /api/Food/FoodCartClear` | 清空购物车 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.food_cart_remove` | 餐饮订单 | `POST /api/Food/FoodCartRemove` | 移除购物车子项 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.food_cart_update` | 餐饮订单 | `POST /api/Food/FoodCartUpdate` | 修改购物车商品数量 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.get_client_list` | 餐饮订单 | `POST /api/Food/GetClientList` | 获取购物车的客户列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.food.get_food_cart` | 餐饮订单 | `POST /api/Food/GetFoodCart` | 获取点餐购物车 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.food.get_food_inforation_to_c` | 餐饮订单 | `POST /api/Food/GetFoodInforationToC` | 获取食品详情 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.food.get_food_list_to_c` | 餐饮订单 | `POST /api/Food/GetFoodListToC` | 获取食品列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.food.get_food_order_detail` | 餐饮订单 | `POST /api/Food/GetFoodOrderDetail` | 获取订单详情 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.food.get_food_order_list` | 餐饮订单 | `POST /api/Food/GetFoodOrderList` | 获取订单列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.food.get_food_table_info` | 餐饮订单 | `POST /api/Food/GetFoodTableInfo` | 获取桌台信息 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.food.get_user_address` | 餐饮订单 | `POST /api/Food/GetUserAddress` | 获取用户地址列表 | 需要登录 | B | 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| `capi.food.pay_food_order` | 餐饮订单 | `POST /api/Food/PayFoodOrder` | 订单支付 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |
| `capi.food.print_food_order` | 餐饮订单 | `POST /api/Food/PrintFoodOrder` | 打印订单 | 需要登录 | D | Action 名称和摘要不足以证明只读，默认禁止。 |

## 可筛选工具详细契约

### `capi.activity.activity_get_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Activity 模块 |
| 用途 | 获取活动详情 |
| 使用时机 | 在顾客视角中核对“获取活动详情”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Activity/ActivityGetInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：UserCouponProvider.UserCouponAdd, ActivityLogProvider.ActivityLogAdd |
| 返回 | `Task<DataResult<ActivityGetInfoResponseModel>>`；包装 `Task/DataResult`；Data `ActivityGetInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ActivityController.cs:27` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.ActivityId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ActivityId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.ActivityId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 活动id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ShareSum` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 分享次数；普通业务字段；可按问题需要提供 |
| `RecomUid` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 推荐者Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | store_id 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Address` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Title` | `string` | 活动标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.ActivityType` | `int` | 0 新用户活动 | 普通业务字段 | 可按问题需要提供 |
| `Data.BgImg` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsOneReward` | `bool` | 是否开启新客奖励 | 普通业务字段 | 可按问题需要提供 |
| `Data.OneIsMobile` | `bool` | 领取是否索要手机号码 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.OneReceiveLimit` | `int` | 新客奖励领取限制 0无限制 1新客 2会员 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsTwoReward` | `bool` | 是否开启转发人奖励 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShareLimit` | `int` | share_limit 转发限制，0允许转发，1不允许转发 | 普通业务字段 | 可按问题需要提供 |
| `Data.TwoReceiveLimit` | `int` | two_receive_limit 转发人奖励限制 0 只要转发就可以得到 1有人领取才可以得到 2使用卷后才可以得到 | 普通业务字段 | 可按问题需要提供 |
| `Data.TwoReceiveCount` | `int` | two_receive_count 转发人奖励数量 0 仅限一份 1满足限制条件 无限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.TwoIsMobile` | `bool` | 转发是否索要手机号码 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ActivityRules` | `string` | activity_rules 活动规则 | 普通业务字段 | 可按问题需要提供 |
| `Data.BeginDate` | `string` | begin_date 活动开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.EndDate` | `string` | end_date 活动结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsRewardUnite` | `bool` | 是否奖励统一 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 1正常 2未开始 3结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.EndReason` | `int` | 结束原因 0默认 1到期 2优惠券发放完毕 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserIsReceiveOne` | `bool` | 用户是否可以领取第一份奖励 | 普通业务字段 | 可按问题需要提供 |
| `Data.NoReceiveOneReason` | `int` | 不能领取原因因 0默认 1已领取 2不是新会员 3不是老会员 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons` | `List<ActivityCouponViewModel>` | 优惠卷 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].AcType` | `int` | 类型 0活动主动领券，1分享后领券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建活动，修改活动 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiveDataLogs` | `List<ActivityReceiveDataLogViewModel>` | 优惠券领取记录 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiveDataLogs[].UserId` | `int` | 用户id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReceiveDataLogs[].UserImg` | `string` | 会员头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiveDataLogs[].UserName` | `string` | 会员昵称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiveDataLogs[].IsNewUser` | `bool` | 是否是新客 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiveDataLogs[].LogType` | `int` | 0 查看 1领券 2分享 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiveDataLogs[].CreateDate` | `string` | 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiveCouponSum` | `long` | 获得推荐奖励优惠券数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.ActivityId < 1`；`resultMsg.State`；`model.Uid == model.RecomUid`；`card?.Id > 0 && (card.State == 1 \|\| card.State == -1)`；`activityModel.State == -1`；`activityModel.Coupons?.Count > 0`；`resultMsg.Data.IsOneReward`；`resultMsg.Data.OneReceiveLimit == 1`；`cardId > 0`；`resultMsg.Data.OneReceiveLimit == 2`；`cardId == 0`；`item.Id > 0`
- 一层业务调用：`ActivityProvider.ActivityGetById`、`UserCardProvider.GetUserCardByUid`、`UserCouponProvider.GetUserCouponListByCouponId`、`UserCouponProvider.GetUserCouponSelfGetCount`、`UserCouponProvider.UserCouponAdd`、`ActivityLogProvider.ActivityLogAdd`
- 疑似副作用：`UserCouponProvider.UserCouponAdd`、`ActivityLogProvider.ActivityLogAdd`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.activity.get_business_new_activity`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Activity 模块 |
| 用途 | 获取店铺最新活动详情 |
| 使用时机 | 在顾客视角中核对“获取店铺最新活动详情”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Activity/GetBusinessNewActivity` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetBusinessNewActivityResponseModel>>`；包装 `Task/DataResult`；Data `GetBusinessNewActivityResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ActivityController.cs:187` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList` | `List<NewActivityModel>` | 活动列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].ActivityId` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewActivityList[].Title` | `string` | 活动标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].IsOneReward` | `bool` | 是否有优惠券 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon` | `ActivityCouponViewModel` | 优惠卷 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewActivityList[].Coupon.CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewActivityList[].Coupon.Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewActivityList[].Coupon.StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewActivityList[].Coupon.StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.NewActivityList[].Coupon.CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewActivityList[].Coupon.Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewActivityList[].Coupon.Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.AcType` | `int` | 类型 0活动主动领券，1分享后领券 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewActivityList[].Coupon.CouponCount` | `int` | 已领取数量 ***** 在创建活动，修改活动 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1`；`resultMsg.State`；`activityModel?.Id > 0`；`activityModel.IsOneReward`
- 一层业务调用：`ActivityProvider.GetNewActivityByStoreId`、`StoreProvider.GetStoreByIdAsync`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.article.article_get`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Article 模块 |
| 用途 | 获取文章详情 |
| 使用时机 | 在顾客视角中核对“获取文章详情”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Article/ArticleGet` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<ArticleGetInfoResponseModel>>`；包装 `Task/DataResult`；Data `ArticleGetInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ArticleController.cs:65` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ArticleId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.ArticleId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 文章id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `int` | 主键唯一标识 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Title` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsTop` | `bool` | 是否置顶 | 普通业务字段 | 可按问题需要提供 |
| `Data.Keyword` | `string` | 关键词 | 普通业务字段 | 可按问题需要提供 |
| `Data.ArticleDescribe` | `string` | 描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Author` | `string` | 作者 | 普通业务字段 | 可按问题需要提供 |
| `Data.Abstract` | `string` | 摘要 | 普通业务字段 | 可按问题需要提供 |
| `Data.Content` | `string` | 内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateDate` | `string` | 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.ArticleImg` | `string` | 文章图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreTypeName` | `string` | 行业名称 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.ArticleId < 1`；`resultMsg.State`；`articleModel == null`
- 一层业务调用：`ArticleProvider.GetArticleInfo`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 101`；`固定提示：参数不正确`；`固定提示：当前文章不存在或已被下架`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.article.article_get_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Article 模块 |
| 用途 | 获取文章列表 |
| 使用时机 | 在顾客视角中核对“获取文章列表”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Article/ArticleGetList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<PageData<GetArticleListResponseModel>>`；包装 `DataResult`；Data `PageData<GetArticleListResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ArticleController.cs:23` |
| C/B 对照 | crmapi.article.article_get_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `PageIndex` | `int` | 代码校验必填 | 绑定=ApiController推断；默认值=1；if(model.PageIndex == 0) | AI 可在服务端上限内选择 | 页码；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 代码校验必填 | 绑定=ApiController推断；默认值=8；if(model.PageSize == 0) | AI 可在服务端上限内选择 | 每页显示行数；普通业务字段；可按问题需要提供 |
| `ArticleTypeId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 文章类型ID 0表示查询所有；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<GetArticleListResponseModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Id` | `int` | id 主键唯一标识 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ArticleTypeId` | `int` | 文章类型Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ArticleTypeName` | `string` | 文章类型Id | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Title` | `string` | title 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsTop` | `bool` | is_top 是否置顶 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Keyword` | `string` | keyword 关键词 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ArticleDescribe` | `string` | describe 描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Author` | `string` | author 作者 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Abstract` | `string` | abstract 摘要 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Content` | `string` | content 内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].OrderBy` | `int` | order_by 排序字段 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].UpdateDate` | `string` | update_date 修改时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CreateDate` | `string` | create_date 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ArticleImg` | `string` | 文章图片 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.PageSize == 0`；`model.PageIndex == 0`；`resultMsg.State`
- 一层业务调用：`ArticleProvider.GetArticleList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 302`；`状态赋值：StatusCode = 303`；`固定提示：请求数据数量不正确`；`固定提示：页码不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.base.get_areas`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Base 模块 |
| 用途 | 获取省市数据 |
| 使用时机 | 在顾客视角中核对“获取省市数据”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Base/GetAreas` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetAreasResponseViewModel>>`；包装 `Task/DataResult`；Data `GetAreasResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/BaseController.cs:43` |
| C/B 对照 | crmapi.base.get_areas |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `RootId` | `string` | 可选/有默认值 | 绑定=ApiController推断；默认值="0" | 必须来自同一会话上游 API 结果或服务端对象引用 | 父类id 取省传0；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.AreasData` | `List<AreasData>` | 地区实体 | 普通业务字段 | 可按问题需要提供 |
| `Data.AreasData[].Name` | `string` | 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.AreasData[].ClassId` | `string` | ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |

#### 代码行为与证据

- Controller 条件：未发现显式 `if` 参数校验；这不代表所有参数都可省略。
- 一层业务调用：`ProvincesProvider.ProvincesGetByRootId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.base.get_province_data`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Base 模块 |
| 用途 | 获取省市数据 |
| 使用时机 | 在顾客视角中核对“获取省市数据”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Base/GetProvinceData` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<List<ProvinceModel>>`；包装 `DataResult`；Data `List<ProvinceModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/BaseController.cs:26` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| — | — | 无 Action 业务参数 | — | — | — |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].Name` | `string` | 省名称 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Citys` | `List<City>` | 用户所在区 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Citys[].Name` | `string` | 市名称 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：未发现显式 `if` 参数校验；这不代表所有参数都可省略。
- 一层业务调用：`BaseProvider.GetProvinceList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.base.get_week_data`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Base 模块 |
| 用途 | 获取星期数据 |
| 使用时机 | 在顾客视角中核对“获取星期数据”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Base/GetWeekData` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<List<GetWeekDataResponseViewModel>>`；包装 `DataResult`；Data `List<GetWeekDataResponseViewModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/BaseController.cs:73` |
| C/B 对照 | crmapi.base.get_week_data |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].WeekInfo` | `string` | 星期内容 | 普通业务字段 | 可按问题需要提供 |
| `Data[].WeekStart` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data[].WeekEnd` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0`；`resultMsg.State`
- 一层业务调用：`UsersInfoProvider.UsersInfoGetByUid`、`DateTimeHelper.GetGroupWeekByDateRange`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.commission.get_commission_cashout_logs`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Commission 模块 |
| 用途 | 获取用户佣金提现记录 |
| 使用时机 | 在顾客视角中核对“获取用户佣金提现记录”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Commission/GetCommissionCashoutLogs` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataList<CommissionCashoutLogResponseModel>>`；包装 `Task/DataList`；Data `CommissionCashoutLogResponseModel` |
| 数据时效 | 历史/记录型数据；具体保留范围以接口代码为准 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CommissionController.cs:43` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageIndex` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].Id` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].StoreId` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Uid` | `int` | 用户ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].State` | `int` | 状态 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Remark` | `string` | 备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data[].Receiver` | `string` | 收款人 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data[].ReceiveAccount` | `string` | 收款账号 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ReceiveChannel` | `string` | 收款渠道 | 普通业务字段 | 可按问题需要提供 |
| `Data[].CashoutPrice` | `decimal` | 申请提现金额 | 普通业务字段 | 可按问题需要提供 |
| `Data[].SparePrice` | `decimal` | 剩余可提现金额 | 普通业务字段 | 可按问题需要提供 |
| `Data[].CreateDate` | `DateTime` | 申请日期 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ApplyUser` | `string` | 申请人 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：未发现显式 `if` 参数校验；这不代表所有参数都可省略。
- 一层业务调用：`CommissionCashoutLogProvider.GetCommissionCashoutLogs`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.commission.get_user_cash_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Commission 模块 |
| 用途 | 获取用户佣金提现信息 |
| 使用时机 | 在顾客视角中核对“获取用户佣金提现信息”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Commission/GetUserCashInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserCommissionInfoResponseModel>>`；包装 `Task/DataResult`；Data `GetUserCommissionInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CommissionController.cs:91` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PromoteUserId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 推广人ID、C端可不填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Uid` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | 商家ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Commission` | `decimal` | 可提现佣金 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionCommission` | `decimal` | 已提现佣金 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`
- 一层业务调用：`CommissionCashoutLogProvider.GetCashInfo`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.commission.get_user_commission_log_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Commission 模块 |
| 用途 | 获取用户佣金消费明细 |
| 使用时机 | 在顾客视角中核对“获取用户佣金消费明细”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Commission/GetUserCommissionLogList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataList<GetUserCommissionLogListRespnseModel>>`；包装 `Task/DataList`；Data `GetUserCommissionLogListRespnseModel` |
| 数据时效 | 历史/记录型数据；具体保留范围以接口代码为准 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CommissionController.cs:21` |
| C/B 对照 | crmapi.commission.get_user_commission_log_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(request.StoreId <= 0 \\|\\| request.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(request.StoreId <= 0 \\|\\| request.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CardId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Type` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 类型：0全部 ，1收入，2支出；普通业务字段；可按问题需要提供 |
| `PromoteUserId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 推广人ID、C端可不填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageIndex` | `int` | 可选/有默认值 | 绑定=ApiController推断；默认值=1 | AI 可在服务端上限内选择 | 页码；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 可选/有默认值 | 绑定=ApiController推断；默认值=20 | AI 可在服务端上限内选择 | 分页大小；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].ConsumptionId` | `string` | 财务ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Source` | `int` | 消费类型 | 普通业务字段 | 可按问题需要提供 |
| `Data[].StrSource` | `string` | 消费类型 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ConsumptionTag` | `int` | 消费类型 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ConsumptionValue` | `decimal` | 消费值 | 普通业务字段 | 可按问题需要提供 |
| `Data[].PayWay` | `int` | 支付方式 | 普通业务字段 | 可按问题需要提供 |
| `Data[].AfterValue` | `decimal` | 支付后剩余佣金 | 普通业务字段 | 可按问题需要提供 |
| `Data[].CreateDate` | `DateTime` | 时间 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`request.StoreId <= 0 \|\| request.Uid <= 0`
- 一层业务调用：`ConsumptionCommissionLogProvider.GetUserCommissionLogList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数有误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.common.check_new_version`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Common 模块 |
| 用途 | 检查版本更新 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Common/CheckNewVersion` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<CheckNewVersionResponseModel>>`；包装 `Task/DataResult`；Data `CheckNewVersionResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CommonController.cs:699` |
| C/B 对照 | crmapi.common.check_new_version |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.Uid == 0 \\|\\| string.IsNullOrEmpty(requestModel.LocalVersion) \\|\\| requestModel.SystemType == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `LocalVersion` | `String` | 代码校验必填 | 绑定=ApiController推断；if(requestModel.Uid == 0 \\|\\| string.IsNullOrEmpty(requestModel.LocalVersion) \\|\\| requestModel.SystemType == 0) | AI 可按业务问题提供；仍需服务端 Schema 校验 | 设备本地版本号；普通业务字段；可按问题需要提供 |
| `SystemType` | `int` | 代码校验必填 | 绑定=ApiController推断；if(requestModel.Uid == 0 \\|\\| string.IsNullOrEmpty(requestModel.LocalVersion) \\|\\| requestModel.SystemType == 0) | AI 只能使用文档确认的枚举值 | 系统类型：1 Android，2 IOS；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.VersionNo` | `string` | 版本编号 | 普通业务字段 | 可按问题需要提供 |
| `Data.VersionName` | `string` | version_name 版本名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.VersionInfo` | `string` | 版本说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.DownUrl` | `string` | 下载地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsMust` | `int` | is_must 是否强制更新 0 否 1是 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNewVersion` | `bool` | 是否有新版本 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`requestModel.Uid == 0 \|\| string.IsNullOrEmpty(requestModel.LocalVersion) \|\| requestModel.SystemType == 0`；`resultMsg.State`；`vm != null && vm.Id > 0`；`v1 < v2 && vm.IsBeat == 0`
- 一层业务调用：`VersionLogProvider.GetVersionLogByPlatform`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.common.check_state`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Common 模块 |
| 用途 | 校验用户状态(Y) |
| 使用时机 | 在顾客视角中核对“校验用户状态(Y)”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Common/CheckState` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<CheckStateResponseModel>>`；包装 `Task/DataResult`；Data `CheckStateResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CommonController.cs:645` |
| C/B 对照 | crmapi.common.check_state |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `LocalVersion` | `String` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(requestModel.LocalVersion)) | AI 可按业务问题提供；仍需服务端 Schema 校验 | 设备本地版本号；普通业务字段；可按问题需要提供 |
| `SystemType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 系统类型：1 Android，2 IOS；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.NewMessageCount` | `int` | 新的系统消息数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNewSettingMessage` | `bool` | 是否有新的系统设置消息 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`requestModel.Uid == 0`；`resultMsg.State`；`urm != null && urm.Id > 0`；`string.IsNullOrEmpty(requestModel.LocalVersion)`；`vm.Id > 0 && v1 < v2 && vm.IsBeat == 0`
- 一层业务调用：`UserRemindProvider.UserRemindGetByUid`、`VersionLogProvider.GetVersionLogByPlatform`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.common.get_oss_conf`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Common 模块 |
| 用途 | 获取OSS配置信息 |
| 使用时机 | 在顾客视角中核对“获取OSS配置信息”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Common/GetOssConf` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetOssConfResponseViewModel>>`；包装 `Task/DataResult`；Data `GetOssConfResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CommonController.cs:764` |
| C/B 对照 | crmapi.common.get_oss_conf |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `UseType` | `int` | 模型特性声明必填 | 绑定=ApiController推断；[Required] | AI 只能使用文档确认的枚举值 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `FileType` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.FileType == 0) | AI 只能使用文档确认的枚举值 | 文件类型 1图片 2视频 3文档；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.UploadFileDirectory` | `string` | 文件上传目录 | 普通业务字段 | 可按问题需要提供 |
| `Data.OssConf` | `StsTockenV2Model` | OSS配置 | 普通业务字段 | 可按问题需要提供 |
| `Data.OssConf.UploadUrl` | `String` | 上传地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.OssConf.SignatureVersion` | `String` | 指定签名的版本和算法 | 普通业务字段 | 可按问题需要提供 |
| `Data.OssConf.Credential` | `String` | 指明派生密钥的参数集 | 密钥/凭据 | 禁止原样进入模型 |
| `Data.OssConf.RequestDate` | `String` | 请求时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.OssConf.Signature` | `String` | 签名信息 | 密钥/凭据 | 禁止原样进入模型 |
| `Data.OssConf.SecurityToken` | `String` | 安全令牌 | 密钥/凭据 | 禁止原样进入模型 |
| `Data.OssConf.Policy` | `String` | policy 表单域 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0`；`resultMsg.State`；`model.FileType == 0`；`model.FileType == 1`
- 一层业务调用：`STSHelper.GetStsTokenV2`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.content.get_index_banner`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Content 模块 |
| 用途 | 获取首页Banner |
| 使用时机 | 在顾客视角中核对“获取首页Banner”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Content/GetIndexBanner` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<IndexBananerResponseModel>>`；包装 `Task/DataResult`；Data `IndexBananerResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ContentController.cs:23` |
| C/B 对照 | crmapi.content.get_index_banner |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Location` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 位置 0首页头部 1首页下部 2启动页；普通业务字段；可按问题需要提供 |
| `Count` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 数量(可不填)；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Banners` | `List<IndexBannerInfoResponseModel>` | 图片集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Banners[].Id` | `int` | ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Banners[].ImgSrc` | `string` | 图片地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Banners[].Link` | `string` | 链接地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Banners[].ActionType` | `int` | 动作类型 0-Html 1-Acitivity | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：未发现显式 `if` 参数校验；这不代表所有参数都可省略。
- 一层业务调用：`IndexBannerProvider.GetIndexBanner`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.device.get_pos_params`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Device 模块 |
| 用途 | 获取设备支付参数 |
| 使用时机 | 在顾客视角中核对“获取设备支付参数”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Device/GetPosParams` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `GetPosParamsResponseModel`；包装 `无已识别包装`；Data `GetPosParamsResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/DeviceController.cs:30` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Sign` | `string` | 代码校验必填 | 绑定=ApiController推断；[Required]；if(string.IsNullOrEmpty(model.DeviceId) \\|\\| string.IsNullOrEmpty(model.Provider) \\|\\| string.IsNullOrEmpty(model.Sign)) | 不得由模型提供 | 源码属性注释缺失；密钥/凭据；禁止原样进入模型 |
| `DeviceId` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.DeviceId) \\|\\| string.IsNullOrEmpty(model.Provider) \\|\\| string.IsNullOrEmpty(model.Sign)) | 必须来自同一会话上游 API 结果或服务端对象引用 | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Provider` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.DeviceId) \\|\\| string.IsNullOrEmpty(model.Provider) \\|\\| string.IsNullOrEmpty(model.Sign)) | AI 可按业务问题提供；仍需服务端 Schema 校验 | 厂商标识；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.Code` | `int` | 信息类型 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data` | `PosParamsDataModel` | 信息类型 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data.AppId` | `string` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data.SecretKey` | `string` | secretKey，用于设备后续接口加签 | 密钥/凭据 | 禁止原样进入模型 |
| `Data.Data.Url` | `string` | 请求地址，作为设备后续接口的请求地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data.Sign` | `string` | 厂商标识 | 密钥/凭据 | 禁止原样进入模型 |

#### 代码行为与证据

- Controller 条件：`string.IsNullOrEmpty(model.DeviceId) \|\| string.IsNullOrEmpty(model.Provider) \|\| string.IsNullOrEmpty(model.Sign)`
- 一层业务调用：`SecurityHelper.Md5Encrypt`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.device.pos_order_detail`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Device 模块 |
| 用途 | 订单查询 |
| 使用时机 | 顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/pos/orderDetail/1.0` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<PosDataResult<PosOrderDetailResponseModel>>`；包装 `Task/PosDataResult`；Data `PosOrderDetailResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/DeviceController.cs:364` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `model` | `PosDataRequest<PosOrderDetailRequestModel>` | Action 形参 | ApiController推断 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.CxOrderNum` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayAmount` | `string` | 支付金额，单位（元）2位小数 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayStatus` | `int` | 支付状态（0待支付，5支付中，10支付完成，15支付失败），订单返回支付中时，需轮询调用支付订单查询接口，查询订单最终状态 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayType` | `int` | 1支付宝，2微信，3云闪付 | 普通业务字段 | 可按问题需要提供 |
| `Data.MerchantReceiveAmount` | `string` | 实收金额，单位（元）2位小数 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayableAmount` | `string` | 实付金额，单位（元）2位小数 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreatedAt` | `string` | 交易时间 2022-04-15 17:07:48 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`string.IsNullOrEmpty(model.Sign) \|\| string.IsNullOrEmpty(model.Data.CxOrderNum)`；`cm?.Id>0`；`cm?.State == 1`
- 一层业务调用：`StoreProvider.GetStoreByCode`、`ConsumptionLogProvider.GetConsumptionLogById`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lottery.get_lottery_by_id`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Lottery 模块 |
| 用途 | 获取活动详情 |
| 使用时机 | 在顾客视角中核对“获取活动详情”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lottery/GetLotteryById` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：LotteryUserProvider.LotteryUserAddLotteryCount, PromoteUsersProvider.BindPromoteUser, ActivityLogProvider.ActivityLogAdd |
| 返回 | `Task<DataResult<GetLotteryByIdResponseModel>>`；包装 `Task/DataResult`；Data `GetLotteryByIdResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LotteryController.cs:28` |
| C/B 对照 | crmapi.lottery.business_get_lottery_by_id |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.LotteryId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `LotteryId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid < 1 \\|\\| model.LotteryId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 抽奖ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ShareSum` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 分享次数；普通业务字段；可按问题需要提供 |
| `RecomUid` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 推荐者Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreLogo` | `string` | 店铺Logo | 普通业务字段 | 可按问题需要提供 |
| `Data.BgImg` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Title` | `string` | 抽奖活动名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.LotteryType` | `int` | 抽奖类型 0进店，1积分，2消费后，3满额 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShareReward` | `int` | 转发奖励次数(进店) | 普通业务字段 | 可按问题需要提供 |
| `Data.LotteryRules` | `string` | 活动规则 | 普通业务字段 | 可按问题需要提供 |
| `Data.BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserLotteryCount` | `int` | 用户可抽奖次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 1正常 2未开始 3结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShareQrCode` | `string` | 领卡二维码 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items` | `List<LotteryItemViewModel>` | 奖项 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Items[].LotteryId` | `int` | 抽奖id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Items[].ItemIndex` | `int` | 抽奖项位置1-8 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].IsReward` | `bool` | is_reward 是否包含奖励 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].WinProbability` | `decimal` | 中奖几率（0.3=30%） | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].RewardTitle` | `string` | 奖品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].RewardLevel` | `int` | 奖品级别 0特等奖，1-3等奖 4普通奖 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].RewardType` | `int` | 奖励类型0优惠券，1积分，2红包奖励，3实物奖励 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].RewardValue` | `decimal` | 奖励值（积分，红包） | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].RewardCount` | `int` | 奖励数量-1不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].RewardWinCount` | `int` | 中奖数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons` | `List<CouponCenterCouponViewModel>` | 优惠券列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Items[].Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Items[].Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Items[].Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Items[].Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Items[].Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Items[].Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Items[].Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建，修改 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].CouponSum` | `int` | 活动优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Items[].Coupons[].ItemId` | `int` | 活动项目ID（预留） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.LotteryId < 1`；`resultMsg.State`；`model.Uid == model.RecomUid`；`resultMsg.Data.Items?.Count > 0`；`lotteryModel.State == -2`；`lotteryModel.State == 1`；`lotteryModel?.Id > 0 && model.RecomUid > 0`；`lotteryModel.ShareReward > 0`；`!(logs?.Count>0)`
- 一层业务调用：`LotteryProvider.LotteryGetById`、`UserCardProvider.GetUserCardByUid`、`LotteryUserProvider.GetLotteryUserByLotteryId`、`ActivityLogProvider.GetActivityLogListByWhere`、`LotteryUserProvider.LotteryUserAddLotteryCount`、`PromoteUsersProvider.BindPromoteUser`、`ActivityLogProvider.ActivityLogAdd`、`WeiXinProvider.GetStoreMpQrCode`
- 疑似副作用：`LotteryUserProvider.LotteryUserAddLotteryCount`、`PromoteUsersProvider.BindPromoteUser`、`ActivityLogProvider.ActivityLogAdd`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.poster.get_poster_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Poster 模块 |
| 用途 | 获取海报列表 |
| 使用时机 | 在顾客视角中核对“获取海报列表”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Poster/GetPosterList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<PageData<GetPosterListResponseModel>>>`；包装 `Task/DataResult`；Data `PageData<GetPosterListResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/PosterController.cs:21` |
| C/B 对照 | crmapi.poster.get_poster_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PostType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 海报类型 0朋友圈，10转卡；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 请求页数；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<GetPosterListResponseModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Id` | `int` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].PosterTitle` | `string` | 海报标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].PosterImg` | `string` | poster_img 海报路径 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsFree` | `bool` | 是否免费 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsVip` | `bool` | 是否vip | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsHot` | `bool` | 是否热门 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Tags` | `List<string>` | 标签 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`
- 一层业务调用：`PosterProvider.GePosterList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.promote.get_promote_user_count`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Promote 模块 |
| 用途 | 获取推荐人数 |
| 使用时机 | 在顾客视角中核对“获取推荐人数”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Promote/GetPromoteUserCount` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetPromoteUserCountResponseModel>>`；包装 `Task/DataResult`；Data `GetPromoteUserCountResponseModel` |
| 数据时效 | 聚合结果；时间范围和门店时区必须由请求参数确认 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/PromoteController.cs:19` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(request.StoreId <= 0 \\|\\| request.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(request.StoreId <= 0 \\|\\| request.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PeopleCount` | `int` | 总人数 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`request.StoreId <= 0 \|\| request.Uid <= 0`
- 一层业务调用：`PromoteUsersProvider.GetPromoteUserCount`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数有误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.promote.get_promote_user_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Promote 模块 |
| 用途 | 获取推荐人列表 |
| 使用时机 | 在顾客视角中核对“获取推荐人列表”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Promote/GetPromoteUserList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataList<GetPromoteUserListResponseModel>>`；包装 `Task/DataList`；Data `GetPromoteUserListResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/PromoteController.cs:43` |
| C/B 对照 | crmapi.promote.business_get_promote_user_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(request.StoreId <= 0 \\|\\| request.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(request.StoreId <= 0 \\|\\| request.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageIndex` | `int` | 可选/有默认值 | 绑定=ApiController推断；默认值=1 | AI 可在服务端上限内选择 | 页码；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 可选/有默认值 | 绑定=ApiController推断；默认值=20 | AI 可在服务端上限内选择 | 分页大小；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].UserName` | `string` | 用户名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data[].CreateDate` | `string` | 时间 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Uid` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |

#### 代码行为与证据

- Controller 条件：`request.StoreId <= 0 \|\| request.Uid <= 0`
- 一层业务调用：`PromoteUsersProvider.GetPromoteUserList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数有误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.search.get_serarch_hot`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Search 模块 |
| 用途 | 获取搜索热词 |
| 使用时机 | 在顾客视角中核对“获取搜索热词”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Search/GetSerarchHot` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<List<String>>`；包装 `DataResult`；Data `List<String>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/SearchController.cs:16` |
| C/B 对照 | crmapi.search.get_serarch_hot |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[]` | `String` | 标量集合；具体业务含义以 Action 摘要为准 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：未发现显式 `if` 参数校验；这不代表所有参数都可省略。
- 一层业务调用：`SearchProvider.GetSerachHotWord`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.shopping_cart.get_shopping_cart`

| 项目 | 内容 |
| --- | --- |
| 业务域 | ShoppingCart 模块 |
| 用途 | 获取用户购物车 |
| 使用时机 | 在顾客视角中核对“获取用户购物车”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/ShoppingCart/GetShoppingCart` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetShoppingCartResponseModel>>`；包装 `Task/DataResult`；Data `GetShoppingCartResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ShoppingCartController.cs:22` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Id` | `int` | 购物车ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ProductCount` | `int` | 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalPrice` | `decimal` | 总价 | 普通业务字段 | 可按问题需要提供 |
| `Data.VipDiscount` | `decimal` | 会员折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products` | `List<ShoppingCartProductViewModel>` | 商品列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].Id` | `int` | 购物车商品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].ProductId` | `int` | 商品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].ProductCount` | `int` | 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductName` | `string` | 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductSkuStr` | `string` | 商品SKU描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductSkuValue` | `string` | 商品SKU编号 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].Price` | `decimal` | 商品价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductImg` | `string` | 商品图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].Quantity` | `int` | 商品库存 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].State` | `int` | 状态：-1 无效，0 正常 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].StateInfo` | `string` | 失效原因 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].IsExpress` | `bool` | 是否需要快递 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].EnjoyVipDiscount` | `bool` | 享受会员折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].IsPurchaseLimit` | `bool` | 是否限购 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].PurchaseLimitType` | `int` | 限购方式 0永久 1天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].PurchaseLimitSum` | `int` | 限购数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`
- 一层业务调用：`ShoppingCartProvider.GetShoppingCart`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 200 }`；`状态赋值：StatusCode = 301`；`固定提示：请求参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.template.get_template`

| 项目 | 内容 |
| --- | --- |
| 业务域 | Template 模块 |
| 用途 | 获取页面模板 |
| 使用时机 | 在顾客视角中核对“获取页面模板”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Template/GetTemplate` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<BusinessGetTemplateResponseModel>>`；包装 `Task/DataResult`；Data `BusinessGetTemplateResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/TemplateController.cs:52` |
| C/B 对照 | crmapi.template.business_get_template |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(string.IsNullOrEmpty(model.StoreCode) \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 店铺CODE；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreCode` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.StoreCode) \\|\\| model.Uid < 1) | AI 可按业务问题提供；仍需服务端 Schema 校验 | 店铺CODE；普通业务字段；可按问题需要提供 |
| `TemplateType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 模板类型 0主页；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `long` | 模板Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TemplateId` | `long` | 原始模板ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TemplateType` | `int` | template_type 模板类型 0主页 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateTitle` | `string` | template_title 模板标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateInfo` | `string` | template_info 模板介绍 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateImg` | `string` | template_img 预览图 | 普通业务字段 | 可按问题需要提供 |
| `Data.BackgroundColor` | `string` | background_color 背景色 | 普通业务字段 | 可按问题需要提供 |
| `Data.BackgroundImg` | `string` | background_img 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateFont` | `string` | template_font 通用字体 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateFontSize` | `int` | template_font_size 字号 | 普通业务字段 | 可按问题需要提供 |
| `Data.LetterSpacing` | `int` | letter_spacing 字间距 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsCustomerService` | `bool` | is_customer_service 是否显示客服 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsShare` | `bool` | is_share 是否显示分享按钮 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas` | `List<StoreTemplateControlViewModel>` | 模板数据 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Id` | `long` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TemplateDatas[].ControlId` | `long` | control_id 控件id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TemplateDatas[].StyleId` | `long` | style_id 样式id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TemplateDatas[].DataType` | `int` | control_type 控件类型 0默认 1商家数据 2用户数据 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].ControlType` | `int` | control_type 控件类型 0其他 1功能项 2自定义功能 3控件 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].ControlName` | `string` | 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].ControlTitle` | `string` | control_title 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].IsEdit` | `bool` | is_edit 是否可以修改 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].IsShow` | `bool` | is_show 是否显示 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].ShowRow` | `int` | show_row 每行显示数据数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].State` | `int` | state 状态 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs` | `List<StoreTemplateInputViewModel>` | 标签集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].Id` | `long` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TemplateDatas[].Inputs[].StyleId` | `long` | 样式id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TemplateDatas[].Inputs[].DataType` | `int` | data_type 数据类型 0不需赋值 1需要 2数据源 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].DataStyle` | `int` | 数据为数据源时显示情况 0不处理，1有数据显示 2无数据显示 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].InputType` | `string` | input_type 标签类型 img / swiper / scroll / div / span / input / text | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].DataName` | `string` | 数据项名称 StoreName | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].DataPro` | `string` | 数据项名称 StorePro | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].DataValue` | `string` | 默认数据 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].InputX` | `int` | input_x 坐标点X | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].InputY` | `int` | input_y 坐标点Y | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].InputWidth` | `int` | input_width 控件宽度 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].InputHeight` | `int` | input_height 控件高度 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].IsEdit` | `bool` | is_edit 是否可编辑 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].JumpTitle` | `string` | 跳转标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].JumpType` | `int` | jump_type 跳转类型 0无跳转 1网页 2本小程序 3其他小程序 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].JumpAppId` | `string` | jump_app_id 三方小程序appid,跳转类型为3的时候填写 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TemplateDatas[].Inputs[].JumpUrl` | `string` | jump_url 跳转最终地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].ChildInputs` | `List<StoreTemplateInputViewModel>` | 子项标签集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].DataSource` | `string` | 数据源 | 普通业务字段 | 可按问题需要提供 |
| `Data.TemplateDatas[].Inputs[].State` | `int` | state 状态 -1删除 0禁用 1启用 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`string.IsNullOrEmpty(model.StoreCode) \|\| model.Uid < 1`；`resultMsg.State`
- 一层业务调用：`StoreProvider.GetStoreByCode`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数格式错误!`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.wei_xin.check_user_is_attention_official_account`

| 项目 | 内容 |
| --- | --- |
| 业务域 | WeiXin 模块 |
| 用途 | 判断当前用户是否关注公众号 |
| 使用时机 | 在顾客视角中核对“判断当前用户是否关注公众号”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/WeiXin/CheckUserIsAttentionOfficialAccount` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：WechatAttentionProvider.GetOpenIdListByUid |
| 返回 | `Task<DataResult<CheckUserIsAttentionOfficialAccountResponseModel>>`；包装 `Task/DataResult`；Data `CheckUserIsAttentionOfficialAccountResponseModel` |
| 数据时效 | 聚合结果；时间范围和门店时区必须由请求参数确认 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/WeiXinController.cs:948` |
| C/B 对照 | crmapi.wei_xin.check_user_is_attention_official_account |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsAttentionOfficialAccount` | `bool` | 是否关注公众号 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`requestModel.Uid < 1`；`resultMsg.State`；`wam!=null && !string.IsNullOrEmpty(wam.OpenId)`
- 一层业务调用：`WechatAttentionProvider.GetOpenIdListByUid`
- 疑似副作用：`WechatAttentionProvider.GetOpenIdListByUid`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 306`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.wei_xin.get_js_signature`

| 项目 | 内容 |
| --- | --- |
| 业务域 | WeiXin 模块 |
| 用途 | 获取Js签名 |
| 使用时机 | 在顾客视角中核对“获取Js签名”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/WeiXin/GetJsSignature` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetJsSignatureResponseModel>>`；包装 `Task/DataResult`；Data `GetJsSignatureResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/WeiXinController.cs:42` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `model` | `GetJsSignatureRequestModel` | Action 形参 | ApiController推断 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.AppId` | `string` | AppId | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.AgentId` | `string` | 应用ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Signature` | `string` | 签名 | 密钥/凭据 | 禁止原样进入模型 |

#### 代码行为与证据

- Controller 条件：`string.IsNullOrEmpty(model.Url)`；`resultMsg.State`
- 一层业务调用：`WeChatHelper.GetJsSignature`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.check_user_coupon_used`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 判断优惠券是否可用 |
| 使用时机 | 顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/CheckUserCouponUsed` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<CouponUsedViewModel>>`；包装 `Task/DataResult`；Data `CouponUsedViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:476` |
| C/B 对照 | crmapi.coupon.business_check_user_coupon_used |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.CouponIds.Count < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.CouponIds.Count < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CouponIds` | `List<int>` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 优惠券Ids；普通业务字段；可按问题需要提供 |
| `UsedType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 使用场景 1现金支付 2购买会员卡 3 会员卡核销 4现场使用（服务或实物兑换）；普通业务字段；可按问题需要提供 |
| `CardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.CardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 核销会员卡的卡Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `TotalPrice` | `decimal` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 实付金额；普通业务字段；可按问题需要提供 |
| `PayModel` | `int` | 参与组合校验 | 绑定=ApiController推断；if(model.UsedType == 3 && model.PayModel == 0) | AI 可按业务问题提供；仍需服务端 Schema 校验 | 付款模式 0实付 1应付(不对金额做任何校验)；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.IsUsed` | `bool` | 是否可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayPrice` | `decimal` | 优惠后金额（实付） | 普通业务字段 | 可按问题需要提供 |
| `Data.ErrorCode` | `int` | 1 优惠券不可多选, 2选择的优惠券中存在不可用不可用 查看CouponErrorInfo | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponErrorInfo` | `List<CouponUsedErrorInfoViewModel>` | 优惠券中的错误信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponErrorInfo[].Id` | `int` | 优惠券id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponErrorInfo[].IsUsed` | `bool` | 是否可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponErrorInfo[].StateReasonContent` | `string` | 不可用原因说明 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| model.CouponIds.Count < 1`；`model.UsedType == 3 && model.PayModel == 0`；`model.CardId < 1`；`uccm?.Id == null && uccm.State < 1`；`uccm.State == 2`；`uccm.CardType == 0`；`resultMsg.State`
- 一层业务调用：`UserCardChildProvider.GetUserCardChildById`、`UserCouponProvider.CheckUsed`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`状态赋值：StatusCode = 303`；`状态赋值：StatusCode = 304`；`状态赋值：StatusCode = 305`；`固定提示：参数格式错误！`；`固定提示：使用场景不正确！`；`固定提示：无效的会员卡！`；`固定提示：会员卡已过期！`；`固定提示：会员卡类型不正确！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.coupoen_center_get_by_id`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 通过优惠中心ID 获取优惠中心优惠券内容 |
| 使用时机 | 在顾客视角中核对“通过优惠中心ID 获取优惠中心优惠券内容”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/CoupoenCenterGetById` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<CoupoenCenterGetByIdResponseModel>>`；包装 `Task/DataResult`；Data `CoupoenCenterGetByIdResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:635` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.CouponCenterId < 1 && model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CouponCenterId` | `int` | 参与组合校验 | 绑定=ApiController推断；if(model.CouponCenterId < 1 && model.Uid < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 优惠中心ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `RandomParam` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.RandomParam)) | 不得由模型提供 | 优惠券随机密钥；密钥/凭据；禁止原样进入模型 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter` | `CouponCenterViewModel` | 优惠中心 详细内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.TemplateId` | `int` | 短信模板ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.CouponCenterType` | `int` | 券类型 1开卡送,2续费送,3生日送,4满送，5群发,6营销活动，7节日祝福8放假 9老客户激活，10散客营销， 21 续费营销（新），22 联盟券，23，购卡送券，24 支付宝商家券 ，25 券包 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.StoreId` | `int` | 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.IsByUserLevel` | `bool` | 是否按会员等级 1是0否 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.PreCardId` | `int` | 按会员等级时必填 储值卡ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.IsOnlyOne` | `int` | 满赠券时必填 1单次 0累十 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.ConsumptionType` | `int` | 满赠券时必填 消费方式1仅付款2卡内消费 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.MeetAmountMin` | `decimal` | 满赠券时必填 金额到达区间开始 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.MeetAmountMax` | `decimal` | 预留字段 金额到达区间结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.SendGroupDate` | `string` | 群发券必填 发放时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.SendGroup` | `int` | 群发券必填发放群体 0全部会员 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.SendGroupTimes` | `int` | 群发券必填 群发次数 1只发一次2按月次数 3按年发送 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.LessMoney` | `decimal` | 续费送券 当余额低于多少时送券 (元) | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.LessTimes` | `int` | 续费送券 当余额低于多少时送券（次） | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.ShareRegularCount` | `int` | 定向券时必填 微信分享限制几人领取 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.AllianceDay` | `int` | 联盟券，多少天未在本店消费 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.SendStartDate` | `DateTime?` | 支付宝商家券发券时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.SendEndDate` | `DateTime?` | 支付宝商家券发券时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.CouponSum` | `int` | 活动优惠券张数 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.State` | `int` | 状态 -1删除 0停止使用 1正常 群发券 0默认 1,未开始 2已发送 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.MaxSendCount` | `int` | 最大发送数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.CouponCenterName` | `string` | 活动名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.SendCount` | `int` | 发送数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons` | `List<CouponCenterCouponViewModel>` | 优惠券列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.CouponCenter.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponCenter.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建，修改 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].CouponSum` | `int` | 活动优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCenter.Coupons[].ItemId` | `int` | 活动项目ID（预留） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CouponsState` | `List<CoupoenCenterStateInfoGetById>` | 优惠券可领取状态 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponsState[].State` | `int` | 优惠券是否可领取状态 0 已领取 1正常 2发放完毕 3优惠券使用时间已经结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponsState[].StateReason` | `string` | 不可以领取原因 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponsState[].CouponId` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |

#### 代码行为与证据

- Controller 条件：`model.CouponCenterId < 1 && model.Uid < 1`；`string.IsNullOrEmpty(model.RandomParam)`；`resultMsg.State`；`coupons?.Count > 0`；`UserCouponProvider.Instance.GetUserCouponCountByUserCouponIdPassword(model.Uid, item.Id, model.RandomParam) > 0`；`item.State == 2`；`(Convert.ToDateTime(item.EndDate) - Convert.ToDateTime(DateTime.Now.AddDays(1).ToShortDateString())).Milliseconds < 0 && item.RangeType == 1`；`CouponPasswordProvider.Instance.GetCouponPasswordByRandomParam(model.RandomParam).RemainingCoupons == 0`
- 一层业务调用：`CouponCenterProvider.CouponCenterGetModelById`、`UserCouponProvider.GetUserCouponCountByUserCouponIdPassword`、`CouponPasswordProvider.GetCouponPasswordByRandomParam`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`固定提示：参数错误`；`固定提示：随机参数不能为空`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.exists_coupon_is_show`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 检测用户是否有新的优惠券 |
| 使用时机 | 顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/ExistsCouponIsShow` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<ExistsCouponIsShowResponseModel>>`；包装 `Task/DataResult`；Data `ExistsCouponIsShowResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:819` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons` | `List<UserCouponViewModel>` | 优惠券列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].ActivityId` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].ActivityType` | `int` | 活动类型 0裂变 1抽奖 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponCenterId` | `int` | 优惠中心ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponCount` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSum` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyCount` | `int` | 限制频率已使用张数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StateReasonContent` | `string` | 不可用原因说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSourceContent` | `string` | 来源说明 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1`；`resultMsg.State`
- 一层业务调用：`UserCouponProvider.ExistsCouponIsShow`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.full_money_coupon_get_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 满赠优惠券列表 |
| 使用时机 | 顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/FullMoneyCouponGetList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<FullMoneyCouponGetListResponseModel>>`；包装 `Task/DataResult`；Data `FullMoneyCouponGetListResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:731` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 && model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 && model.Uid < 1) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons` | `List<CouponViewModel>` | 优惠券列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.FullMoneyContents` | `List<FullMoneyCouponGetListInfoModel>` | 满送描述内容 列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.FullMoneyContents[].Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.FullMoneyContents[].Content` | `string` | 满送描述内容 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 && model.Uid < 1`；`resultMsg.State`；`(await StoreCouponCenterProvider.Instance .StoreCouponCenterState(model.StoreId, (int)CouponCenterTypeEnum.FullMoney))?.State == 1`；`item.ConsumptionType == 1`；`item.IsOnlyOne == 0`；`couponItem.CouponType == 0`；`couponItem.CouponType == 1`；`couponItem.CouponType == 2`；`couponItem.CouponType == 3`
- 一层业务调用：`CouponCenterProvider.CouponCenterGetByStoreCouponCenterType`、`CouponProvider.CouponGetListByCouponCenterId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.get_alliance_coupon_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 获取联盟可领优惠券列表 |
| 使用时机 | 顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/GetAllianceCouponList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetAllianceCouponResponseModel>>`；包装 `Task/DataResult`；Data `GetAllianceCouponResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:1354` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons` | `List<CouponViewModel>` | 优惠券列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1`；`resultMsg.State`
- 一层业务调用：`CouponCenterProvider.GetAllianceCoupons`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.get_marketing_center_coupons`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 营销中心领取券页面获取优惠券列表 |
| 使用时机 | 顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/GetMarketingCenterCoupons` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：MarketingLogProvider.MarketingLogAdd |
| 返回 | `Task<DataResult<GetMarketingCenterCouponsResponseModel>>`；包装 `Task/DataResult`；Data `GetMarketingCenterCouponsResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:1150` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `MarketingId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.MarketingId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 营销中心ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `RandomParam` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 不得由模型提供 | 随机参数；密钥/凭据；禁止原样进入模型 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.CouponCenterName` | `string` | 活动名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponsState` | `List<CoupoenCenterStateInfoGetById>` | 优惠券可领取状态 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponsState[].State` | `int` | 优惠券是否可领取状态 0 已领取 1正常 2发放完毕 3优惠券使用时间已经结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponsState[].StateReason` | `string` | 不可以领取原因 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponsState[].CouponId` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons` | `List<MarketingCenterCouponViewModel>` | 优惠券列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建，修改 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSum` | `int` | 活动优惠券数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.MarketingId < 1`；`resultMsg.State`；`marketing?.StoreId == model.StoreId`；`coupons?.Count > 0 && model.Uid > 0`；`UserCouponProvider.Instance.GetUserCouponCountByUserCouponIdPassword(model.Uid, item.Id, model.RandomParam) >= (couponPass?.ReceiveCount > 0 ? couponPass?.ReceiveCount : 0) && !marketing.CouponCenterType.Equals(25)`；`item.State == 2 && !marketing.CouponCenterType.Equals(25)`；`marketing.State == 2 && marketing.CouponCenterType.Equals(25)`；`(Convert.ToDateTime(item.EndDate + (" 23:59:59")) - Convert.ToDateTime(DateTime.Now.ToShortDateString())).TotalSeconds < 0 && item.RangeType == 1`；`UserCouponProvider.Instance.ExistsUserCouponByCouponCenterId(model.StoreId,model.MarketingId,model.Uid)>0 && marketing.CouponCenterType.Equals(25)`；`CouponPasswordProvider.Instance.GetCouponPasswordByRandomParam(model.RandomParam)?.RemainingCoupons == 0`；`resultMsg.Data.Coupons.Count > 0`；`model.Uid > 0`
- 一层业务调用：`CouponCenterProvider.CouponCenterGetModelById`、`CouponPasswordProvider.GetCouponPasswordByRandomParam`、`UserCouponProvider.GetUserCouponCountByUserCouponIdPassword`、`UserCouponProvider.ExistsUserCouponByCouponCenterId`、`CouponProvider.CouponGetListByCouponCenterId`、`MarketingLogProvider.MarketingLogAdd`、`UserCardProvider.GetIsVipByUid`
- 疑似副作用：`MarketingLogProvider.MarketingLogAdd`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 303`；`固定提示：参数错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.get_user_coupon`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 获取单个优惠券 |
| 使用时机 | 顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/GetUserCoupon` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserCouponResponseModel>>`；包装 `Task/DataResult`；Data `GetUserCouponResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:413` |
| C/B 对照 | crmapi.coupon.get_user_coupon |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CouponId` | `int` | 参与组合校验 | 绑定=ApiController推断；if(model.CouponId < 1 && model.PCouponId < 1 && string.IsNullOrEmpty(model.CouponCode)) | 必须来自同一会话上游 API 结果或服务端对象引用 | 优惠券Id（三选一）；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CouponCode` | `string` | 参与组合校验 | 绑定=ApiController推断；if(model.CouponId < 1 && model.PCouponId < 1 && string.IsNullOrEmpty(model.CouponCode)) | AI 可按业务问题提供；仍需服务端 Schema 校验 | 优惠券Code（三选一）；普通业务字段；可按问题需要提供 |
| `PCouponId` | `int` | 参与组合校验 | 绑定=ApiController推断；if(model.CouponId < 1 && model.PCouponId < 1 && string.IsNullOrEmpty(model.CouponCode)) | 必须来自同一会话上游 API 结果或服务端对象引用 | 原始优惠券Id（三选一）；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon` | `UserCouponViewModel` | 优惠券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupon.CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupon.Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupon.StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupon.StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupon.CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupon.Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupon.Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.ActivityId` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupon.ActivityType` | `int` | 活动类型 0裂变 1抽奖 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponCenterId` | `int` | 优惠中心ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupon.CouponCount` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponSum` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.UseFrequencyCount` | `int` | 限制频率已使用张数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.StateReasonContent` | `string` | 不可用原因说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupon.CouponSourceContent` | `string` | 来源说明 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0`；`model.CouponId < 1 && model.PCouponId < 1 && string.IsNullOrEmpty(model.CouponCode)`；`resultMsg.State`
- 一层业务调用：`UserCouponProvider.UserCouponGetById`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.get_user_coupon_count`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 获取用户可用优惠券数量 |
| 使用时机 | 顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/GetUserCouponCount` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserCouponCountResponseModel>>`；包装 `Task/DataResult`；Data `GetUserCouponCountResponseModel` |
| 数据时效 | 聚合结果；时间范围和门店时区必须由请求参数确认 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:449` |
| C/B 对照 | crmapi.coupon.get_user_coupon_count |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponCount` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1`；`resultMsg.State`
- 一层业务调用：`UserCouponProvider.GetUserCouponCountByUserId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.coupon.get_user_coupon_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 优惠券 |
| 用途 | 获取优惠券列表 |
| 使用时机 | 顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Coupon/GetUserCouponList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserCouponListResponseModel>>`；包装 `Task/DataResult`；Data `GetUserCouponListResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CouponController.cs:377` |
| C/B 对照 | crmapi.coupon.get_user_coupon_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `UsedType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 使用场景 1现金支付 2购买会员卡 3 会员卡核销 4现场使用（服务或实物兑换）；普通业务字段；可按问题需要提供 |
| `TotalPrice` | `decimal` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 实付金额；普通业务字段；可按问题需要提供 |
| `QueryState` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 查询状态 0不限制 1未生效或可用 2已用或过期 3 已用 4 已过期；普通业务字段；可按问题需要提供 |
| `PayModel` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 付款模式 0实付 1应付(不对金额做任何校验)；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons` | `List<UserCouponViewModel>` | 优惠券列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].ActivityId` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].ActivityType` | `int` | 活动类型 0裂变 1抽奖 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponCenterId` | `int` | 优惠中心ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponCount` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSum` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyCount` | `int` | 限制频率已使用张数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StateReasonContent` | `string` | 不可用原因说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSourceContent` | `string` | 来源说明 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0`；`resultMsg.State`
- 一层业务调用：`UserCouponProvider.GetUserCouponByUserId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.user.check_reset_card_pass_sms_code`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员与身份 |
| 用途 | 校验重置会员密码的验证码 |
| 使用时机 | 在顾客视角中核对“校验重置会员密码的验证码”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/User/CheckResetCardPassSmsCode` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<CheckResetCardPassSmsCodeResponseModel>>`；包装 `Task/DataResult`；Data `CheckResetCardPassSmsCodeResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/UserController.cs:903` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Mobile` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.Mobile) \\|\\| string.IsNullOrEmpty(model.VerificationCode)) | 当前会话提供并临时使用；不得持久化到模型历史 | 手机号；个人信息；仅在当前授权场景按最小范围提供 |
| `VerificationCode` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.Mobile) \\|\\| string.IsNullOrEmpty(model.VerificationCode)) | AI 可按业务问题提供；仍需服务端 Schema 校验 | 验证码；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.CheckResult` | `bool` | 检查结果 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`string.IsNullOrEmpty(model.Mobile) \|\| string.IsNullOrEmpty(model.VerificationCode)`；`success`
- 一层业务调用：`SmsValidationProvider.SmsCheck`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 200,`；`状态赋值：StatusCode = 301`；`固定提示：手机号或验证码不能为空`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.user.check_user_card_pass`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员与身份 |
| 用途 | 验证会员卡密码 |
| 使用时机 | 已从上游卡列表取得服务端卡引用后，核对顾客端单张卡的余额、状态、有效期、服务项目或使用限制。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/User/CheckUserCardPass` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<CheckUserCardPassResponseModel>>`；包装 `Task/DataResult`；Data `CheckUserCardPassResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/UserController.cs:938` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| string.IsNullOrEmpty(model.CardPass)) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CardPass` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| string.IsNullOrEmpty(model.CardPass)) | AI 可按业务问题提供；仍需服务端 Schema 校验 | 会员卡密码；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.CheckResult` | `bool` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| string.IsNullOrEmpty(model.CardPass)`；`i > 0`
- 一层业务调用：`UserCardProvider.CheckUserCardPass`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 200,`；`状态赋值：StatusCode = 301`；`固定提示：手机号或验证码不能为空`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.user.check_user_mobile`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员与身份 |
| 用途 | 检测手机号能否使用 |
| 使用时机 | 商家提供手机号后，用于确认目标会员在顾客端当前资料或会员身份；只允许当前门店范围。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/User/CheckUserMobile` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<CheckUserMobileResponseModel>>`；包装 `Task/DataResult`；Data `CheckUserMobileResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/UserController.cs:552` |
| C/B 对照 | crmapi.user.check_user_mobile |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.OperationType == 1 && model.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `OperationType` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.OperationType == 0) | AI 只能使用文档确认的枚举值 | 应用场景：0注册 1修改；普通业务字段；可按问题需要提供 |
| `UserMobile` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 当前会话提供并临时使用；不得持久化到模型历史 | 手机号；个人信息；仅在当前授权场景按最小范围提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsUse` | `bool` | 是否可以试用该手机号 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.OperationType == 1 && model.Uid == 0`；`resultMsg.State`；`ucModel?.Id > 0`；`model.OperationType == 1`；`model.OperationType == 0`；`ucModel.Uid != 0`
- 一层业务调用：`UserCardProvider.BusinessCheckMobile`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.user.get_content`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员与身份 |
| 用途 | 分销说明 |
| 使用时机 | 在顾客视角中核对“分销说明”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/User/GetContent` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetContentResponseModel>>`；包装 `Task/DataResult`；Data `GetContentResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/UserController.cs:975` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ExtendContent` | `string` | 说明 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`resultMsg.State`；`sm?.Count > 0`；`m.IsCommissionConsume \|\| m.IsCommissionCash`；`m.IsCommissionConsume`；`m.IsCommissionCash`
- 一层业务调用：`DistributionSettingProvider.GetDistributionSetting`、`DistributionSettingChildProvider.GetDistributionSettingChildList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.user.get_store_controls`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员与身份 |
| 用途 | 注册用户获取店铺用户自定义控件（会员编辑资料页） |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/User/GetStoreControls` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreControlsResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreControlsResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/UserController.cs:193` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Scenes` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 0注册 修改前，1获取信息；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.UserMobile` | `string` | 手机号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Controls` | `List<StoreUserForControlViewModel>` | 用户信息集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlName` | `string` | 控件名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlInstructions` | `string` | 控件说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlType` | `string` | control_type 控件类型 input,radio,select.... | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlValue` | `string` | 控件值 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Controls[].IsMust` | `int` | 是否必填 1是 0否 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].IsShow` | `bool` | 是否必填对C端展示 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlsValidations` | `List<CustomControlsValidationViewModel>` | 控件验证规则 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlsValidations[].ValidationFormula` | `string` | 验证公式 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlsValidations[].ValidationInstructions` | `string` | 不通过提示信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].Items` | `List<CustomControlsItemViewModel>` | 选项列表 控件类型 为 radio select 不为空 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].Items[].Id` | `int` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Controls[].Items[].Cid` | `int` | cid 控件id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Controls[].Items[].ItemValue` | `string` | item_value 值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].Items[].ItemName` | `string` | item_name 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].Items[].IsDefault` | `int` | is_default 是否是默认 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1`；`resultMsg.State`
- 一层业务调用：`StoreControlsProvider.GetStoreControls`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.user.get_store_user_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员与身份 |
| 用途 | 加载用户信息（会员编辑资料页） |
| 使用时机 | 商家提供手机号后，用于确认目标会员在顾客端当前资料或会员身份；只允许当前门店范围。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/User/GetStoreUserInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreUserInfoResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreUserInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/UserController.cs:448` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CardId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.UserMobile` | `string` | 会员电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserName` | `string` | 会员昵称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserImg` | `string` | 会员头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserInfos` | `List<StoreUserForControlViewModel>` | 用户信息集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].ControlName` | `string` | 控件名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].ControlInstructions` | `string` | 控件说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].ControlType` | `string` | control_type 控件类型 input,radio,select.... | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].ControlValue` | `string` | 控件值 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserInfos[].IsMust` | `int` | 是否必填 1是 0否 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].IsShow` | `bool` | 是否必填对C端展示 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].ControlsValidations` | `List<CustomControlsValidationViewModel>` | 控件验证规则 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].ControlsValidations[].ValidationFormula` | `string` | 验证公式 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].ControlsValidations[].ValidationInstructions` | `string` | 不通过提示信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].Items` | `List<CustomControlsItemViewModel>` | 选项列表 控件类型 为 radio select 不为空 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].Items[].Id` | `int` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserInfos[].Items[].Cid` | `int` | cid 控件id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserInfos[].Items[].ItemValue` | `string` | item_value 值 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].Items[].ItemName` | `string` | item_name 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserInfos[].Items[].IsDefault` | `int` | is_default 是否是默认 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0`；`resultMsg.State`
- 一层业务调用：`StoreUserProvider.GetStoreUser`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.user.get_user_sign_agreement_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员与身份 |
| 用途 | 签署合同 |
| 使用时机 | 在顾客视角中核对“签署合同”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/User/GetUserSignAgreementInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserSignAgreementInfoResponseModel>>`；包装 `Task/DataResult`；Data `GetUserSignAgreementInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/UserController.cs:1077` |
| C/B 对照 | crmapi.user.get_user_sign_agreement_info |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.CardId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.CardId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.CardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreAgreement` | `string` | 会员协议 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsSignAgreement` | `bool` | 是否签署 | 普通业务字段 | 可按问题需要提供 |
| `Data.SignImage` | `string` | 签字图片地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.SignDate` | `string` | 签字时间 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| model.CardId < 1`；`uam?.CardId > 0`；`sam?.Id>0`
- 一层业务调用：`UserCardAgreementProvider.GetUserCardAgreementFirstOrDefaultByCondition`、`StoreAgreementProvider.GetStoreAgreementFirstOrDefaultByCondition`、`StoreAgreementProvider.GetNewStoreAgreement`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.user.user_vip_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员与身份 |
| 用途 | 获取用户会员信息 |
| 使用时机 | 在顾客视角中核对“获取用户会员信息”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/User/UserVipInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：UserCardProvider.BusinessBindUserCard |
| 返回 | `Task<DataResult<UserVipInfoResponseModel>>`；包装 `Task/DataResult`；Data `UserVipInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/UserController.cs:29` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardId` | `int` | 会员卡Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserName` | `string` | 用户昵称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserImg` | `string` | 用户头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.OperationDate` | `string` | 最后操作时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.OperationUser` | `string` | 最后操作人 | 普通业务字段 | 可按问题需要提供 |
| `Data.Note` | `string` | 备注信息 电话 多个电话用,分割 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 -2商家删除 -1用户自己删除 0非会员 1是会员 2商家添加会员 10需要授权信息 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1`；`resultMsg.State`；`userModel == null \|\| userModel.Id == 0 \|\| string.IsNullOrEmpty(userModel.UserMobile)`；`ucm?.Id > 0 && ucm.State != 0`；`ucm.State < 0`；`ucm.State == -2`；`ucardModel?.Id > 0`；`ucardModel.Uid == 0`；`UserCardProvider.Instance.BusinessBindUserCard(ucardModel.Id, model.StoreId, model.Uid, isDelUserInfo) > 0`；`uc?.UserId > 0`；`!string.IsNullOrEmpty(sim.StoreMobile)`；`resultMsg.Data.State == 0`
- 一层业务调用：`UsersProvider.GetUserMobileByUid`、`UsersInfoProvider.UsersInfoGetByUid`、`UserCardProvider.BusinessGetUserCardByUid`、`UserCardProvider.BusinessExistUserCardByMobile`、`StoreUserProvider.CheckUserInfo`、`UserCardProvider.BusinessBindUserCard`、`TenantUserProvider.GetTenantUserByStoreId`、`StoreProvider.GetStoreByIdAsync`
- 疑似副作用：`UserCardProvider.BusinessBindUserCard`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.check_for_card_tag_and_user_mobile`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 检测会员卡预留手机号与当前会员绑定手机号是否一致 |
| 使用时机 | 商家提供手机号后，用于确认目标会员在顾客端当前资料或会员身份；只允许当前门店范围。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/CheckForCardTagAndUserMobile` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<CheckForCardTagAndUserMobileResponseModel>>`；包装 `Task/DataResult`；Data `CheckForCardTagAndUserMobileResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:1103` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.ChildCardId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ChildCardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid < 1 \\|\\| model.ChildCardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员子卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `UserMobile` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.UserMobile) \\|\\| !StringOperate.IsNumber(model.UserMobile)) | 当前会话提供并临时使用；不得持久化到模型历史 | 当前会员的手机号；个人信息；仅在当前授权场景按最小范围提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsSame` | `bool` | 预留手机号 与要绑定的手机号是否一致 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.ChildCardId < 1`；`string.IsNullOrEmpty(model.UserMobile) \|\| !StringOperate.IsNumber(model.UserMobile)`；`resultMsg.State`
- 一层业务调用：`UserCardProvider.CheckForCardTagAndUserMobile`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`固定提示：参数不正确`；`固定提示：校验手机号不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.check_new_user_card`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 检查是否有新会员卡（第三方开卡所用） |
| 使用时机 | 已从上游卡列表取得服务端卡引用后，核对顾客端单张卡的余额、状态、有效期、服务项目或使用限制。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/CheckNewUserCard` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：StoreCardProvider.GetAddCardSignature |
| 返回 | `Task<DataResult<CheckNewUserCardResponseModel>>`；包装 `Task/DataResult`；Data `CheckNewUserCardResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:496` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 当前店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CheckType` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.CheckType == 0 \\|\\| model.CheckType == 1)；if(model.CheckType == 0 \\|\\| model.CheckType == 2) | AI 只能使用文档确认的枚举值 | 0全部 1会员卡 2优惠券；普通业务字段；可按问题需要提供 |
| `IsCheck` | `bool` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 检查传ture 领卡可false；普通业务字段；可按问题需要提供 |
| `Platform` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 平台 1微信 3支付宝；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.OpenId` | `string` | 领卡者OpenId | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Timestamp` | `long` | 当前时间戳 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCards` | `List<NewCardModel>` | 卡集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCards[].Id` | `int` | 卡/券 系统内ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewCards[].CardId` | `string` | 会员卡Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewCards[].CardType` | `int` | 类型 1会员卡 2优惠券 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCards[].Code` | `string` | 会员卡Code | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCards[].TemplateParams` | `string` | 支付宝券动态参数 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCards[].FixedBeginTimestamp` | `string` | 领取时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCards[].NonceStr` | `string` | 随机字符串 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCards[].Signature` | `string` | 签名 | 密钥/凭据 | 禁止原样进入模型 |
| `Data.NewCards[].SendCouponMerchant` | `string` | 发券商户号 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCards[].AliPayActiveCardUrl` | `string` | 支付宝领卡接口 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCoupons` | `List<NewCardModel>` | 券集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCoupons[].Id` | `int` | 卡/券 系统内ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewCoupons[].CardId` | `string` | 会员卡Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.NewCoupons[].CardType` | `int` | 类型 1会员卡 2优惠券 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCoupons[].Code` | `string` | 会员卡Code | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCoupons[].TemplateParams` | `string` | 支付宝券动态参数 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCoupons[].FixedBeginTimestamp` | `string` | 领取时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCoupons[].NonceStr` | `string` | 随机字符串 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCoupons[].Signature` | `string` | 签名 | 密钥/凭据 | 禁止原样进入模型 |
| `Data.NewCoupons[].SendCouponMerchant` | `string` | 发券商户号 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewCoupons[].AliPayActiveCardUrl` | `string` | 支付宝领卡接口 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards` | `List<StorePrepaidCardViewModel>` | 用户会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].PrepaidCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].CardImg` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardType` | `int` | 类型：0计次，1储值 2时限 3权益 4安心充 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardValue` | `decimal` | 卡价值 次/金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardGivingValue` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardCount` | `int` | 库存剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardSellCount` | `long` | card_sell_count 销售数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].ValidityDate` | `int` | 有效期 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsBuyOnce` | `bool` | 是否只能购买一次 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].State` | `int` | 状态 1在售 0停售 -1删除 2售罄 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].OpenCardType` | `int` | 开卡方式 0购买即开卡，1首次使用开卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].StopCardDays` | `int` | 停卡天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].OpenCardDaysMax` | `int` | 最大延迟开卡天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsPayAfterReceive` | `bool` | 是否支付后领取 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardInstructions` | `string` | 会员权益 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsPromptRights` | `bool` | 是否强制提示会员权益 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsAllianceCard` | `bool` | 是否为联盟卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Services` | `List<StorePrepaidCardServiceItemViewModel>` | 服务项目列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Services[].PrepaidCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Services[].ItemUnit` | `string` | 项目单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Services[].CardValue` | `decimal` | 服务项 卡价值 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Services[].IsGift` | `bool` | 是否是赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons` | `List<CouponCenterCouponViewModel>` | 购卡送的券 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserCards[].Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建，修改 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].CouponSum` | `int` | 活动优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Coupons[].ItemId` | `int` | 活动项目ID（预留） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].IsAudit` | `bool` | 卡是否需要审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].ServiceItems` | `List<string>` | 审核卡消费项目明细 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CheckItemId` | `int` | 代办事项明细ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].CardTimeList` | `List<StorePrepaidCardViewCardTimeModel>` | 会员卡有效期集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].Id` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].CardTimeList[].ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天)； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].ValidityDate` | `int` | 有效期单位天 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].MaxCount` | `int` | 最大可售出数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].CardCount` | `int` | 剩余卡数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].IsBuyOnce` | `bool` | 是否只能购买一次 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].GivePrice` | `decimal` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].StartDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].EndDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardTimeList[].CreateDate` | `DateTime` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsCardChild` | `bool` | 是否包含子卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].RemainderDay` | `int` | 剩余天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsCustomPrice` | `bool` | 是否开启自定义金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CustomPriceMin` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CustomPriceMax` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CustomPriceGiveRatio` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].BindCourseSum` | `long` | 绑定课目数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons` | `List<UserCouponViewModel>` | 优惠券列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].ActivityId` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].ActivityType` | `int` | 活动类型 0裂变 1抽奖 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponCenterId` | `int` | 优惠中心ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponCount` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSum` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyCount` | `int` | 限制频率已使用张数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StateReasonContent` | `string` | 不可用原因说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSourceContent` | `string` | 来源说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Signature` | `string` | 签名 | 密钥/凭据 | 禁止原样进入模型 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1`；`model.Platform == 3`；`model.CheckType == 0 \|\| model.CheckType == 1`；`ucModels?.Count > 0`；`pCard != null`；`auth != null`；`!model.IsCheck`；`model.CheckType == 0 \|\| model.CheckType == 2`；`model.Platform == 1`
- 一层业务调用：`UserCardProvider.CheckNewUserCard`、`UsersProvider.GetUserLoginInfo`、`StorePrepaidCardProvider.GetStorePrepaidCardByIds`、`StorePrepaidCardProvider.GetStorePrepaidCard`、`AlipayAuthInfoProvider.GetAlipayAuthInfoByStoreId`、`AlipayThirdPlatformProvider.CardActiveUrl`、`StoreCardProvider.GetAddCardSignature`、`UserCouponProvider.CheckNewUserCoupon`、`UserCouponProvider.GetUserCouponByIds`、`AlipayThirdPlatformProvider.GetTemplateParams`、`DateTimeHelper.TimeStampToDateTime`
- 疑似副作用：`StoreCardProvider.GetAddCardSignature`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_card_interests`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取会员卡权益 |
| 使用时机 | 在顾客视角中核对“获取会员卡权益”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetCardInterests` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetCardInterestsResponseViewModel>>`；包装 `Task/DataResult`；Data `GetCardInterestsResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:156` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.CardId == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.CardId == 0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ChildCardId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员子卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardInstructions` | `string` | 使用说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardLimit` | `string` | 使用须知 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.CardId == 0`；`resultMsg.State`；`scModel?.Id > 0`
- 一层业务调用：`StoreCardProvider.GetCardInterests`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_prepaid_card_qr_code`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取购买储值卡的二维码 |
| 使用时机 | 在顾客视角中核对“获取购买储值卡的二维码”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetPrepaidCardQrCode` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetPrepaidCardQrCodeResponseModel>>`；包装 `Task/DataResult`；Data `GetPrepaidCardQrCodeResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:1067` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1 \\|\\| model.PrepaidCardId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PrepaidCardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid < 1 \\|\\| model.StoreId < 1 \\|\\| model.PrepaidCardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 储值卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid < 1 \\|\\| model.StoreId < 1 \\|\\| model.PrepaidCardId < 1) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCardQrCode` | `string` | 购买储值卡二维码路径 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1 \|\| model.PrepaidCardId < 1`；`resultMsg.State`
- 一层业务调用：`StoreCardProvider.GetPrepaidCardQrCode`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_store_card_agreement`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取会员协议 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetStoreCardAgreement` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreCardAgreementResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreCardAgreementResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:199` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId == 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreAgreement` | `string` | 会员协议 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId == 0`；`resultMsg.State`；`scModel?.Id > 0`
- 一层业务调用：`StoreSetingProvider.StoreSetingGetAgreement`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_store_free_card`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取商家权益卡 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetStoreFreeCard` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreFreeCardResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreFreeCardResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:1146` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商户ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard` | `StorePrepaidCardViewModel` | 权益卡 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.PrepaidCard.PrepaidCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.CardImg` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardType` | `int` | 类型：0计次，1储值 2时限 3权益 4安心充 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardValue` | `decimal` | 卡价值 次/金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardGivingValue` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardCount` | `int` | 库存剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardSellCount` | `long` | card_sell_count 销售数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.ValidityDate` | `int` | 有效期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.IsBuyOnce` | `bool` | 是否只能购买一次 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.State` | `int` | 状态 1在售 0停售 -1删除 2售罄 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.OpenCardType` | `int` | 开卡方式 0购买即开卡，1首次使用开卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.StopCardDays` | `int` | 停卡天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.OpenCardDaysMax` | `int` | 最大延迟开卡天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.IsPayAfterReceive` | `bool` | 是否支付后领取 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardInstructions` | `string` | 会员权益 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.IsPromptRights` | `bool` | 是否强制提示会员权益 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.IsAllianceCard` | `bool` | 是否为联盟卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Services` | `List<StorePrepaidCardServiceItemViewModel>` | 服务项目列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Services[].PrepaidCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Services[].ItemUnit` | `string` | 项目单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Services[].CardValue` | `decimal` | 服务项 卡价值 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Services[].IsGift` | `bool` | 是否是赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons` | `List<CouponCenterCouponViewModel>` | 购卡送的券 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.PrepaidCard.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建，修改 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].CouponSum` | `int` | 活动优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.Coupons[].ItemId` | `int` | 活动项目ID（预留） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.IsAudit` | `bool` | 卡是否需要审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.ServiceItems` | `List<string>` | 审核卡消费项目明细 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CheckItemId` | `int` | 代办事项明细ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.CardTimeList` | `List<StorePrepaidCardViewCardTimeModel>` | 会员卡有效期集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].Id` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCard.CardTimeList[].ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天)； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].ValidityDate` | `int` | 有效期单位天 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].MaxCount` | `int` | 最大可售出数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].CardCount` | `int` | 剩余卡数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].IsBuyOnce` | `bool` | 是否只能购买一次 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].GivePrice` | `decimal` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].StartDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].EndDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CardTimeList[].CreateDate` | `DateTime` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.IsCardChild` | `bool` | 是否包含子卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.RemainderDay` | `int` | 剩余天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.IsCustomPrice` | `bool` | 是否开启自定义金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CustomPriceMin` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CustomPriceMax` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.CustomPriceGiveRatio` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCard.BindCourseSum` | `long` | 绑定课目数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1`；`resultMsg.State`
- 一层业务调用：`UserCardProvider.GetStoreFreeCard`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_store_prepaid_card_by_id`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取商家单个充值卡 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetStorePrepaidCardById` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStorePrepaidCardByIdResponseModel>>`；包装 `Task/DataResult`；Data `GetStorePrepaidCardByIdResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:713` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId == 0 \\|\\| (model.PrepaidCardId == 0 && string.IsNullOrEmpty(model.RandomParam))) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PrepaidCardId` | `int` | 参与组合校验 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId == 0 \\|\\| (model.PrepaidCardId == 0 && string.IsNullOrEmpty(model.RandomParam))) | 必须来自同一会话上游 API 结果或服务端对象引用 | 储值卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `RandomParam` | `string` | 参与组合校验 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId == 0 \\|\\| (model.PrepaidCardId == 0 && string.IsNullOrEmpty(model.RandomParam))) | 不得由模型提供 | 秘钥；密钥/凭据；禁止原样进入模型 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId == 0 \\|\\| (model.PrepaidCardId == 0 && string.IsNullOrEmpty(model.RandomParam))) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardImg` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardType` | `int` | 类型：0计次，1储值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardValue` | `decimal` | 卡价值 次/金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardGivingValue` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardCount` | `int` | 库存剩余数量 0不限量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.ValidityDate` | `int` | 有效期 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 1在售 0停售 -1删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.StateInfo` | `string` | 状态 1在售 0停售 -1删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsCustomPrice` | `bool` | 是否开启自定义金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomPriceMin` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomPriceMax` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomPriceGiveRatio` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsAllianceCard` | `bool` | 是否为联盟卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services` | `List<StorePrepaidCardServiceItemViewModel>` | 服务项目列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].PrepaidCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ItemUnit` | `string` | 项目单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].CardValue` | `decimal` | 服务项 卡价值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].IsGift` | `bool` | 是否是赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons` | `List<CouponCenterCouponViewModel>` | 购卡送的券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建，修改 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSum` | `int` | 活动优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].ItemId` | `int` | 活动项目ID（预留） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardTimeList` | `List<StorePrepaidCardViewCardTimeModel>` | 会员卡有效期集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].Id` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardTimeList[].ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天)； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].ValidityDate` | `int` | 有效期单位天 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].MaxCount` | `int` | 最大可售出数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].CardCount` | `int` | 剩余卡数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].IsBuyOnce` | `bool` | 是否只能购买一次 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].GivePrice` | `decimal` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].StartDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].EndDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTimeList[].CreateDate` | `DateTime` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId == 0 \|\| (model.PrepaidCardId == 0 && string.IsNullOrEmpty(model.RandomParam))`；`!string.IsNullOrEmpty(model.RandomParam)`；`cardPass?.Id > 0`；`resultMsg.State`；`scModel?.Id > 0`；`scModel.IsCardChild`；`scModel.State == 0`；`!string.IsNullOrEmpty(model.RandomParam) && cardPass?.Id > 0`；`cardPass.RemainingCoupons == 0`；`scModel.IsBuyOnce`；`childCards.Any(cc => cc.PrepaidCardId == scModel.Id)`；`(await StoreCouponCenterProvider.Instance.StoreCouponCenterState(model.StoreId, 23))?.State == 1`
- 一层业务调用：`CouponPasswordProvider.GetCouponPasswordByRandomParam`、`StorePrepaidCardProvider.GetStorePrepaidCard`、`StorePrepaidCardChildProvider.GetStorePrepaidCardChildList`、`StorePrepaidCardServiceItemProvider.GetStorePerpaidCardServices`、`UserCardChildProvider.GetUserCardChildViewByUid`、`StoreCouponCenterProvider.StoreCouponCenterState`、`CouponCenterProvider.CouponCenterGetByStoreCouponCenterTypeByPerCardId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 307`；`状态赋值：StatusCode = 308`；`状态赋值：StatusCode = 302`；`固定提示：参数不正确`；`固定提示：该二维码领取人数已达到上限！`；`固定提示：秘钥无效！`；`固定提示：不存在该储值卡`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_store_prepaid_card_by_key`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 根据兑换秘钥获取商家单个充值卡 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetStorePrepaidCardByKey` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStorePrepaidCardByKeyResponseModel>>`；包装 `Task/DataResult`；Data `GetStorePrepaidCardByKeyResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:899` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| string.IsNullOrEmpty(model.SecretKey)) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `SecretKey` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| string.IsNullOrEmpty(model.SecretKey)) | 不得由模型提供 | 秘钥；密钥/凭据；禁止原样进入模型 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreId` | `int` | 会员卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardId` | `int` | 会员卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardChildId` | `int` | 子卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PreCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.State` | `int` | 状态1可用 2已用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card` | `GetStorePrepaidCardByIdResponseModel` | 储值卡详情 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardImg` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardType` | `int` | 类型：0计次，1储值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardValue` | `decimal` | 卡价值 次/金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardGivingValue` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardCount` | `int` | 库存剩余数量 0不限量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.ValidityDate` | `int` | 有效期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.State` | `int` | 状态 1在售 0停售 -1删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.StateInfo` | `string` | 状态 1在售 0停售 -1删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.IsCustomPrice` | `bool` | 是否开启自定义金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CustomPriceMin` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CustomPriceMax` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CustomPriceGiveRatio` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.IsAllianceCard` | `bool` | 是否为联盟卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Services` | `List<StorePrepaidCardServiceItemViewModel>` | 服务项目列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Services[].PrepaidCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Services[].ItemUnit` | `string` | 项目单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Services[].CardValue` | `decimal` | 服务项 卡价值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Services[].IsGift` | `bool` | 是否是赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons` | `List<CouponCenterCouponViewModel>` | 购卡送的券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Card.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建，修改 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].CouponSum` | `int` | 活动优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.Coupons[].ItemId` | `int` | 活动项目ID（预留） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.CardTimeList` | `List<StorePrepaidCardViewCardTimeModel>` | 会员卡有效期集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].Id` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Card.CardTimeList[].ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天)； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].ValidityDate` | `int` | 有效期单位天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].MaxCount` | `int` | 最大可售出数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].CardCount` | `int` | 剩余卡数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].IsBuyOnce` | `bool` | 是否只能购买一次 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].GivePrice` | `decimal` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].StartDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].EndDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.Card.CardTimeList[].CreateDate` | `DateTime` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| string.IsNullOrEmpty(model.SecretKey)`；`resultMsg.State`；`!(spm?.Id > 0)`；`spm.State == 2 && spm.Uid != model.Uid`；`spm.State == 1`；`scModel?.Id > 0`；`(await StoreCouponCenterProvider.Instance.StoreCouponCenterState(spm.StoreId, 23))?.State == 1`；`couponRenewals?.Id > 0 && couponRenewals.Coupons?.Count > 0`
- 一层业务调用：`StorePhysicalCardProvider.GetStorePhysicalCardByKey`、`StorePrepaidCardProvider.GetStorePrepaidCard`、`StorePrepaidCardServiceItemProvider.GetStorePerpaidCardServices`、`StoreCouponCenterProvider.StoreCouponCenterState`、`CouponCenterProvider.CouponCenterGetByStoreCouponCenterTypeByPerCardId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 303`；`状态赋值：StatusCode = 304`；`状态赋值：StatusCode = 302`；`固定提示：参数不正确`；`固定提示：兑换码无效`；`固定提示：该卡已被兑换`；`固定提示：不存在该储值卡`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_store_prepaid_card_by_random_param`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 根据转让秘钥获取单个充值卡 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetStorePrepaidCardByRandomParam` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：CardPasswordProvider.CardPasswordUpdateState |
| 返回 | `Task<DataResult<GetStorePrepaidCardByRandomParamResponseModel>>`；包装 `Task/DataResult`；Data `GetStorePrepaidCardByRandomParamResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:1433` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| string.IsNullOrEmpty(model.RandomParam)) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `RandomParam` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| string.IsNullOrEmpty(model.RandomParam)) | 不得由模型提供 | 秘钥；密钥/凭据；禁止原样进入模型 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `int` | 原卡ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardImg` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardType` | `int` | 类型：0计次，1储值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardValue` | `decimal` | 卡价值 次/金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardGivingValue` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardCount` | `int` | 库存剩余数量 0不限量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ValidityDate` | `string` | 有效期 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 1在售 0停售 -1删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.BackgroundImage` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserName` | `string` | 转让人 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.IsGetCard` | `bool` | 是否可以领取卡片 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsThemselves` | `bool` | 是否是自己领取 | 普通业务字段 | 可按问题需要提供 |
| `Data.FailedMessage` | `string` | 失败提示 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| string.IsNullOrEmpty(model.RandomParam)`；`resultMsg.State`；`transferInfo?.Id > 0`；`transferInfo.State == -2`；`transferInfo.State == 1`；`transferInfo.CreateDate.AddHours(24) > DateTime.Now`；`card?.Id > 0`；`transferInfo.CardValue > 10 && resultMsg.Data.IsGetCard`；`transferInfo.CardValue > card.CardPrice`；`card?.ValidityDate != null && card?.ValidityDate < DateTime.Now.AddDays(-1)`；`!(card.State == 1 \|\| card.State == 4 \|\| card.State == 0)`；`scModel?.Id > 0`
- 一层业务调用：`CardPasswordProvider.GetCardPasswordByRandomParam`、`CardPasswordProvider.CardPasswordUpdateState`、`UserCardChildProvider.GetUserCardChildByIdAll`、`StorePrepaidCardProvider.GetStorePrepaidCardAll`、`UsersInfoProvider.UsersInfoGetByUid`
- 疑似副作用：`CardPasswordProvider.CardPasswordUpdateState`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 305`；`状态赋值：StatusCode = 304`；`状态赋值：StatusCode = 308`；`状态赋值：StatusCode = 302`；`固定提示：参数不正确`；`固定提示：该卡已被领取过`；`固定提示：该卡已失效！`；`固定提示：查询不到对应的秘钥`；`固定提示：原卡余额不足！`；`固定提示：原卡已过期！`；`固定提示：该卡已不存在！`；`固定提示：不存在该卡`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_store_prepaid_cards`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取商家所有充值卡 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetStorePrepaidCards` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStorePrepaidCardsResponseViewModel>>`；包装 `Task/DataResult`；Data `GetStorePrepaidCardsResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:242` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId == 0) | 服务端注入：已确认门店 | 商户id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards` | `List<StorePrepaidCardViewModel>` | 充值卡列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].PrepaidCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].CardImg` | `string` | 背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardType` | `int` | 类型：0计次，1储值 2时限 3权益 4安心充 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardValue` | `decimal` | 卡价值 次/金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardGivingValue` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardCount` | `int` | 库存剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardSellCount` | `long` | card_sell_count 销售数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].ValidityDate` | `int` | 有效期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].IsBuyOnce` | `bool` | 是否只能购买一次 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].State` | `int` | 状态 1在售 0停售 -1删除 2售罄 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].OpenCardType` | `int` | 开卡方式 0购买即开卡，1首次使用开卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].StopCardDays` | `int` | 停卡天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].OpenCardDaysMax` | `int` | 最大延迟开卡天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].IsPayAfterReceive` | `bool` | 是否支付后领取 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardInstructions` | `string` | 会员权益 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].IsPromptRights` | `bool` | 是否强制提示会员权益 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].IsAllianceCard` | `bool` | 是否为联盟卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Services` | `List<StorePrepaidCardServiceItemViewModel>` | 服务项目列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Services[].PrepaidCardId` | `int` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Services[].ItemUnit` | `string` | 项目单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Services[].CardValue` | `decimal` | 服务项 卡价值 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Services[].IsGift` | `bool` | 是否是赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons` | `List<CouponCenterCouponViewModel>` | 购卡送的券 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.PrepaidCards[].Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponCount` | `int` | 已领取数量 ***** 在创建，修改 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].CouponSum` | `int` | 活动优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].Coupons[].ItemId` | `int` | 活动项目ID（预留） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].IsAudit` | `bool` | 卡是否需要审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].ServiceItems` | `List<string>` | 审核卡消费项目明细 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CheckItemId` | `int` | 代办事项明细ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].CardTimeList` | `List<StorePrepaidCardViewCardTimeModel>` | 会员卡有效期集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].Id` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCards[].CardTimeList[].ValidType` | `int` | 失效日期类型: 0 相对日期（购卡后N天)； 1 绝对日期（指定失效日期） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].InvalidDate` | `string` | 失效日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].ValidityDate` | `int` | 有效期单位天 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].Price` | `decimal` | 售价 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].MaxCount` | `int` | 最大可售出数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].CardCount` | `int` | 剩余卡数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].IsBuyOnce` | `bool` | 是否只能购买一次 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].GivePrice` | `decimal` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].StartDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].EndDate` | `string` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CardTimeList[].CreateDate` | `DateTime` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].IsCardChild` | `bool` | 是否包含子卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].RemainderDay` | `int` | 剩余天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].IsCustomPrice` | `bool` | 是否开启自定义金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CustomPriceMin` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CustomPriceMax` | `decimal` | 自定义储值最低 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].CustomPriceGiveRatio` | `decimal` | 赠送 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrepaidCards[].BindCourseSum` | `long` | 绑定课目数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId == 0`；`resultMsg.State`；`models != null && models.Count > 0`；`(await StoreCouponCenterProvider.Instance.StoreCouponCenterState(model.StoreId, 23))?.State == 1`；`item.State == 1`；`ucm?.Id > 0`；`item.CardType == 3 && Constant.AppType == 0`；`item.IsBuyOnce`；`item.CardType == 3`；`item.IsCardChild`；`!isOk`；`(items.CardCount <= items.MaxCount && items.CardCount != 0) \|\| items.MaxCount == 0`
- 一层业务调用：`StorePrepaidCardProvider.GetStorePrepaidCardByStoreId`、`UserCardProvider.GetUserCardByUid`、`StoreCouponCenterProvider.StoreCouponCenterState`、`UserCardChildProvider.ExistsFreeChildCard`、`UserCardChildProvider.GetUserCardChildViewByUid`、`StorePrepaidCardChildProvider.GetStorePrepaidCardChildList`、`UserCardChildProvider.GetUserCardChildByPrepaidCardId`、`StorePrepaidCardServiceItemProvider.GetStorePerpaidCardServices`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_user_card`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取用户单个会员卡 |
| 使用时机 | 已从上游卡列表取得服务端卡引用后，核对顾客端单张卡的余额、状态、有效期、服务项目或使用限制。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetUserCard` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserCardResponseViewModel>>`；包装 `Task/DataResult`；Data `GetUserCardResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:34` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId == 0) | 服务端注入：已确认门店 | 店铺id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `UsedDatetime` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 用卡时间。预约传预约时间 其他不用传；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardId` | `int` | 卡片id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardName` | `string` | 卡片名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.CardNumber` | `string` | 卡号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.CardImg` | `string` | 背景图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardType` | `int` | 类型：0计次，1储值 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardIntegral` | `int` | 积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardPrint` | `int` | 印章 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionIntegral` | `int` | 消费积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionPrint` | `int` | 消费印章 | 普通业务字段 | 可按问题需要提供 |
| `Data.ValidityDate` | `string` | 到期时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.LastDate` | `string` | 最近一次消费时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreIsReservation` | `bool` | 是否支持预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | state 1正常 0停用 -1 销卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsOpenIntegral` | `bool` | 是否开启积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsEnableshop` | `bool` | 是否开启商城 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardExpiredIntegral` | `long` | 将过期积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardExpiredIntegralDate` | `string` | 积分过期时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards` | `List<UserCardChildViewModel>` | 子会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Id` | `int` | 子卡Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Cards[].PrepaidCardId` | `int` | 卡id(储值卡) | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Cards[].CardNumber` | `string` | 卡号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Cards[].CardImg` | `string` | 背景图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].CardType` | `int` | 类型：0计次，1储值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].ValidityDate` | `string` | 到期时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].CardPrice` | `decimal` | 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].CardNormalPrice` | `decimal` | card_normal_price 正金 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].CardGivePrice` | `decimal` | card_give_price 赠金 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].CardDiscountPrice` | `decimal` | card_discount_price 已优惠金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].CardMergerDiscountPrice` | `decimal` | card_merger_discount_price 合并后未使用优惠金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].ConsumptionPrice` | `decimal` | 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].State` | `int` | 1正常 0未开卡 -1 销卡 -2商家删除 2 已过期，-3过期续费删除 3停卡 4转让中 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].LastDate` | `string` | 最后一次消费日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].OpenDate` | `string` | 开卡时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].OpenCardDate` | `string` | 自动开卡时间， 如果为“”空，需要手动解卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].StopCardDays` | `int` | 默认停卡天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].MemberCardQrCode` | `string` | 会员卡的二维码 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].SingleMaxFrequency` | `int` | 单次最大次数 0不限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].DayMaxFrequency` | `int` | 每日最大核销次数0 不限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].WeekMaxFrequency` | `int` | week_max_frequency 每周最大核销次数 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].MouthMaxFrequency` | `int` | mouth_max_frequency 每月最大核销次数 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].IsLimitFrequency` | `bool` | 是否限制次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].ConsumptionTimes` | `int` | 已经销卡次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].WeekConsumptionTimes` | `int` | 已经销卡次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].MouthConsumptionTimes` | `int` | 已经销卡次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].IsAllianceCard` | `bool` | 是否为联盟卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services` | `List<UserCardServiceItemViewModel>` | 服务项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Cards[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services[].ItemUnit` | `string` | 项目单位（服务单位） | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services[].CardValue` | `decimal` | 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services[].CardNormalValue` | `decimal` | 正金(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services[].CardGiveValue` | `decimal` | 赠送金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services[].ConsumptionValue` | `decimal` | 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services[].ItemPrice` | `decimal` | 项目单价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].Services[].IsDefault` | `bool` | 是否默认，默认选中上次核销的项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].IsTransferCard` | `bool` | 是否开启转让卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].IsTransferCardValue` | `bool` | 是否开启转让卡余额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].IsUsedDateTime` | `bool` | 是否在使用时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].BindCourseSum` | `long` | 绑定课目数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].UseMaxCount` | `decimal` | 最大使用次数 -1不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Cards[].UseCount` | `decimal` | 已用次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsConfirmPass` | `bool` | 消费验证密码 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsFreeVersion` | `bool` | 是否是免费版 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsFood` | `bool` | 是否开通了点单 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodMode` | `int` | 点单模式 0一人一单 1多人一单 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsFoodDelay` | `bool` | 是否开启延迟取餐 | 普通业务字段 | 可按问题需要提供 |
| `Data.Commission` | `decimal` | 佣金 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionCommission` | `decimal` | 提现佣金 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsTransferCard` | `bool` | 是否开启转让卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsTransferCardValue` | `bool` | 是否开启转让卡余额 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsMustSignAgreement` | `bool` | 是否需要签署协议 true表示用户需要签署协议（还未签署） | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId == 0`；`sm.State < 0`；`resultMsg.State`；`!(ucvm?.CardId > 0)`；`sm.Alliance?.Id > 0 && sm.Alliance.IsOpenAllianceCard && model.StoreId != sm.Alliance.StoreId`
- 一层业务调用：`StoreProvider.GetStoreByIdAsync`、`UserCardProvider.GetUserCardByStoreId`、`UserCardProvider.GetUserCardByAlliance`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 310`；`固定提示：参数不正确`；`固定提示：店铺被封禁！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_user_card_by_prepaid_card_id`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 通过储值卡Id查询用户会员卡 |
| 使用时机 | 已从上游卡列表取得服务端卡引用后，核对顾客端单张卡的余额、状态、有效期、服务项目或使用限制。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetUserCardByPrepaidCardId` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserCardByPrepaidCardIdResponseModel>>`；包装 `Task/DataResult`；Data `GetUserCardByPrepaidCardIdResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:651` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.PrepaidCardId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.PrepaidCardId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PrepaidCardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.PrepaidCardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 储值卡Id ///；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `int` | 子卡Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardPrice` | `decimal` | card_price 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionPrice` | `decimal` | consumption_price 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services` | `List<UserCardServiceItemViewModel>` | 储值卡服务列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ItemUnit` | `string` | 项目单位（服务单位） | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].CardValue` | `decimal` | 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].CardNormalValue` | `decimal` | 正金(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].CardGiveValue` | `decimal` | 赠送金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ConsumptionValue` | `decimal` | 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ItemPrice` | `decimal` | 项目单价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].IsDefault` | `bool` | 是否默认，默认选中上次核销的项目 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| model.PrepaidCardId < 1`；`ucModel?.CardType == 1`；`sm.IsBalanceMergers`；`uccms?.Count() > 0`；`ucModel?.CardPrice > 0 \|\| ucModel?.State == 1`
- 一层业务调用：`UserCardChildProvider.GetUserCardChildByPCardId`、`StoreProvider.GetStoreByIdAsync`、`UserCardChildProvider.GetUserCardChildsByUid`、`UserCardServiceItemProvider.GetUserCardServiceItemList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_user_card_child_qr_code`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取单个会员子卡的二维码 |
| 使用时机 | 已从上游卡列表取得服务端卡引用后，核对顾客端单张卡的余额、状态、有效期、服务项目或使用限制。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetUserCardChildQrCode` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserCardChildQrCodeResponseModel>>`；包装 `Task/DataResult`；Data `GetUserCardChildQrCodeResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:1033` |
| C/B 对照 | crmapi.card.business_get_user_card_child_qr_code |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.ChildCardId < 1) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ChildCardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.ChildCardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员子卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.QrCode` | `string` | 会员子卡二维码 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.ChildCardId < 1`；`resultMsg.State`
- 一层业务调用：`UserCardChildProvider.GetUserCardChildQrCode`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_user_cards`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取用户会员卡列表 |
| 使用时机 | 顾客反馈在顾客端看不到会员卡/课卡，或余额、有效期、卡状态与预期不一致时，读取目标会员实际可见卡列表。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetUserCards` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserCardsResponseViewModel>>`；包装 `Task/DataResult`；Data `GetUserCardsResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:88` |
| C/B 对照 | crmapi.card.business_get_user_cards |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `UsedDatetime` | `DateTime?` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 用卡时间。预约传预约时间 其他不用传；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards` | `List<UserCardsApiViewModel>` | 用户会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardId` | `int` | 卡片id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].StoreId` | `int` | 店铺id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardNumber` | `string` | card_number 卡号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserCards[].CardImg` | `string` | card_img 背景图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardName` | `string` | 卡片名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].ValidityDate` | `string` | 到期时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardIntegral` | `int` | 积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardPrint` | `int` | 印章 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].ConsumptionIntegral` | `int` | 消费积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].ConsumptionPrint` | `int` | 消费印章 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].StoreIsReservation` | `bool` | 是否支持预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].State` | `int` | state 1正常 0停用 -1 销卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsOpenIntegral` | `bool` | 是否开启积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsEnableshop` | `bool` | 是否开启商城 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardExpiredIntegral` | `long` | 将过期积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].CardExpiredIntegralDate` | `string` | 积分过期时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards` | `List<UserCardChildViewModel>` | 子会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Id` | `int` | 子卡Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Cards[].PrepaidCardId` | `int` | 卡id(储值卡) | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Cards[].CardNumber` | `string` | 卡号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserCards[].Cards[].CardImg` | `string` | 背景图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].CardType` | `int` | 类型：0计次，1储值 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].ValidityDate` | `string` | 到期时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].CardPrice` | `decimal` | 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].CardNormalPrice` | `decimal` | card_normal_price 正金 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].CardGivePrice` | `decimal` | card_give_price 赠金 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].CardDiscountPrice` | `decimal` | card_discount_price 已优惠金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].CardMergerDiscountPrice` | `decimal` | card_merger_discount_price 合并后未使用优惠金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].ConsumptionPrice` | `decimal` | 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].State` | `int` | 1正常 0未开卡 -1 销卡 -2商家删除 2 已过期，-3过期续费删除 3停卡 4转让中 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].LastDate` | `string` | 最后一次消费日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].OpenDate` | `string` | 开卡时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].OpenCardDate` | `string` | 自动开卡时间， 如果为“”空，需要手动解卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].StopCardDays` | `int` | 默认停卡天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].MemberCardQrCode` | `string` | 会员卡的二维码 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].SingleMaxFrequency` | `int` | 单次最大次数 0不限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].DayMaxFrequency` | `int` | 每日最大核销次数0 不限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].WeekMaxFrequency` | `int` | week_max_frequency 每周最大核销次数 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].MouthMaxFrequency` | `int` | mouth_max_frequency 每月最大核销次数 0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].IsLimitFrequency` | `bool` | 是否限制次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].ConsumptionTimes` | `int` | 已经销卡次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].WeekConsumptionTimes` | `int` | 已经销卡次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].MouthConsumptionTimes` | `int` | 已经销卡次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].IsAllianceCard` | `bool` | 是否为联盟卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services` | `List<UserCardServiceItemViewModel>` | 服务项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCards[].Cards[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services[].ItemUnit` | `string` | 项目单位（服务单位） | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services[].CardValue` | `decimal` | 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services[].CardNormalValue` | `decimal` | 正金(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services[].CardGiveValue` | `decimal` | 赠送金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services[].ConsumptionValue` | `decimal` | 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services[].ItemPrice` | `decimal` | 项目单价 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].Services[].IsDefault` | `bool` | 是否默认，默认选中上次核销的项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].IsTransferCard` | `bool` | 是否开启转让卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].IsTransferCardValue` | `bool` | 是否开启转让卡余额 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].IsUsedDateTime` | `bool` | 是否在使用时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].BindCourseSum` | `long` | 绑定课目数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].UseMaxCount` | `decimal` | 最大使用次数 -1不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Cards[].UseCount` | `decimal` | 已用次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsConfirmPass` | `bool` | 是否需要确认密码 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsFreeVersion` | `bool` | 店铺是否是免费版 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsFood` | `bool` | 是否开通了点单 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].FoodMode` | `int` | 点单模式 0一人一单 1多人一单 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].IsFoodDelay` | `bool` | 是否开启延迟取餐 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].Commission` | `decimal` | 佣金 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserCards[].ConsumptionCommission` | `decimal` | 提现佣金 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0`；`resultMsg.State`
- 一层业务调用：`UserCardProvider.GetUserCardListByUid`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.card.get_user_child_card`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 会员卡与课卡 |
| 用途 | 获取会员的单张会员卡 |
| 使用时机 | 已从上游卡列表取得服务端卡引用后，核对顾客端单张卡的余额、状态、有效期、服务项目或使用限制。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Card/GetUserChildCard` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserChildCardResponseModel>>`；包装 `Task/DataResult`；Data `GetUserChildCardResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/CardController.cs:1005` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.ChildCardId < 1) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ChildCardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.ChildCardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 子卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.CardTag` | `string` | 预留信息 默认手机号 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `int` | 子卡Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PrepaidCardId` | `int` | 卡id(储值卡) | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardNumber` | `string` | 卡号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.CardImg` | `string` | 背景图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardType` | `int` | 类型：0计次，1储值 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ValidityDate` | `string` | 到期时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardDiscount` | `decimal` | 会员卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardPrice` | `decimal` | 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionPrice` | `decimal` | 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 1正常 0未开卡 -1 销卡 -2商家删除 2 已过期，-3过期续费删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.LastDate` | `string` | 最后一次消费日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.MemberCardQrCode` | `string` | 会员卡的二维码 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services` | `List<UserCardServiceItemViewModel>` | 服务项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ItemUnit` | `string` | 项目单位（服务单位） | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].CardValue` | `decimal` | 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].CardNormalValue` | `decimal` | 正金(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].CardGiveValue` | `decimal` | 赠送金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ConsumptionValue` | `decimal` | 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].ItemPrice` | `decimal` | 项目单价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Services[].IsDefault` | `bool` | 是否默认，默认选中上次核销的项目 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.ChildCardId < 1`；`resultMsg.State`
- 一层业务调用：`UserCardChildProvider.GetUserChildCard`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.shopping_mall.get_business_products_message_by_product_id`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 商城 |
| 用途 | 根据商品ID获取商品信息 |
| 使用时机 | 在顾客视角中核对“根据商品ID获取商品信息”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/ShoppingMall/GetBusinessProductsMessageByProductId` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<ProductsMessageResponseViewModel>>`；包装 `Task/DataResult`；Data `ProductsMessageResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ShoppingMallController.cs:100` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.ProductId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ProductId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid < 1 \\|\\| model.ProductId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 商品ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `int` | 商品id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ImgList` | `List<string>` | 商品图片集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductName` | `string` | 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductInfo` | `string` | 商品描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsExchange` | `bool` | 是否兑换商品 | 普通业务字段 | 可按问题需要提供 |
| `Data.ExchangeIntegral` | `int` | 兑换积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Quantity` | `int` | 库存 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsExpress` | `int` | 是否需要快递服务；0-不需要，1-需要 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductClassList` | `List<string>` | 商品分类集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductTagList` | `List<string>` | 商品标签集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList` | `List<ProductsMessageSkuListModel>` | 规格列表集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].Id` | `int` | 规格id（新增即传入0） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SkuList[].SkuName` | `ProductsMessageSkuNameModel` | 规格名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuName.Id` | `int` | 规格id（新增即传入0） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SkuList[].SkuName.SkuName` | `string` | 规格名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuName.SkuAttrList` | `List<ProductsMessageSkuAttrListModel>` | 规格属性集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuName.SkuAttrList[].Id` | `int` | 规格属性的id（新增即传入0） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SkuList[].SkuName.SkuAttrList[].SkuAttrName` | `string` | 规格属性名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuAttrList` | `List<ProductsMessageSkuAttrListModel>` | 规格属性集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuAttrList[].Id` | `int` | 规格属性的id（新增即传入0） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SkuList[].SkuAttrList[].SkuAttrName` | `string` | 规格属性名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 0下架 1上架 | 普通业务字段 | 可按问题需要提供 |
| `Data.Detail` | `string` | 商品详情 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList` | `List<ProductMessageSkuAttrDetailListModel>` | 商品规格属性详情集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].Id` | `int` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SkuAttrDetailList[].ProductSkuIds` | `string` | id组合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].IsExchange` | `bool` | 是否兑换商品 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].ExchangeIntegral` | `int` | 兑换积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].VipPrice` | `decimal` | 会员价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].Quantity` | `int` | 库存 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].IsPurchaseLimit` | `bool` | 是否限购 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].PurchaseLimitType` | `int` | 限购方式 0永久 1天 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].PurchaseLimitSum` | `int` | 限购数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuAttrDetailList[].PurchaseLimitBySum` | `int` | 已购数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsVip` | `bool` | 是否是vip | 普通业务字段 | 可按问题需要提供 |
| `Data.EnjoyVipDiscount` | `bool` | 享受会员折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Pno` | `string` | 货号 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsHaveSku` | `bool` | 是否包含多SKU | 普通业务字段 | 可按问题需要提供 |
| `Data.IsPurchaseLimit` | `bool` | 是否限购 | 普通业务字段 | 可按问题需要提供 |
| `Data.PurchaseLimitType` | `int` | 限购方式 0永久 1天 | 普通业务字段 | 可按问题需要提供 |
| `Data.PurchaseLimitSum` | `int` | 限购数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PurchaseLimitBySum` | `int` | 已购数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.ProductId < 1`；`resultMsg.State`；`m == null`
- 一层业务调用：`ProductProvider.GetBusinessProductsMessageByProductId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`；`固定提示：当前商品不存在`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.shopping_mall.get_products_class_by_store_id`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 商城 |
| 用途 | 根据门店ID获取B端商品分类集合 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/ShoppingMall/GetProductsClassByStoreId` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<ProductsClassResponseViewModel>>`；包装 `Task/DataResult`；Data `ProductsClassResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ShoppingMallController.cs:23` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsClassItems` | `List<ProductsClassModel>` | 门店商品分类集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsClassItems[].Id` | `int` | id ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ProductsClassItems[].ClassName` | `string` | class_name 分类名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsClassItems[].ClassImg` | `string` | 分类图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsClassItems[].RootId` | `string` | root_id 父级ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ProductsClassItems[].StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ProductsClassItems[].IsSystem` | `bool` | 是否是系统分类 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsClassItems[].State` | `int` | state 状态 1正常 0停用 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1`
- 一层业务调用：`ProductClassProvider.GetClassListByStoreId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.shopping_mall.get_products_list_by_key_word`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 商城 |
| 用途 | 搜索商品 |
| 使用时机 | 在顾客视角中核对“搜索商品”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/ShoppingMall/GetProductsListByKeyWord` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<ProductsListClientResponseViewModel>>`；包装 `Task/DataResult`；Data `ProductsListClientResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ShoppingMallController.cs:74` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `KeyWord` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 源码注释疑似与字段名冲突，待人工复核（原注释：商品分类ID,0为全部商品）；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.VipDiscount` | `decimal` | 会员折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList` | `List<ProductClientViewModel>` | 门店分类商品集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].Id` | `int` | 商品id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ProductsList[].ImgStr` | `string` | 商品图片集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].ProductName` | `string` | 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].IsExchange` | `bool` | 是否兑换商品 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].ExchangeIntegral` | `int` | 兑换积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].State` | `int` | 0下架 1上架 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].ProductTagList` | `List<string>` | 商品标签集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].SellNum` | `int` | 销量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].SkuCount` | `int` | 规格数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].SkuList` | `List<ProductsSkuNameViewModel>` | 规格列表集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].SkuList[].Id` | `int` | 规格id（新增即传入0） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ProductsList[].SkuList[].ProductSkuValue` | `string` | 商品SKU值 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].EnjoyVipDiscount` | `bool` | 享受会员折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].IsHaveSku` | `bool` | 是否包含多SKU | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].IsPurchaseLimit` | `bool` | 是否限购 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].PurchaseLimitType` | `int` | 限购方式 0永久 1天 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].PurchaseLimitSum` | `int` | 限购数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].PurchaseLimitBySum` | `int` | 已购数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1`
- 一层业务调用：`ProductProvider.GetProductsByKeyWord`、`UserCardProvider.GetVipMinDiscount`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.shopping_mall.get_products_list_by_store_id`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 商城 |
| 用途 | 根据分类展示商品列表接口 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/ShoppingMall/GetProductsListByStoreId` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<ProductsListClientResponseViewModel>>`；包装 `Task/DataResult`；Data `ProductsListClientResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ShoppingMallController.cs:49` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ClassId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 商品分类ID,0为全部商品；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `KeyWord` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 源码注释疑似与字段名冲突，待人工复核（原注释：商品分类ID,0为全部商品）；普通业务字段；可按问题需要提供 |
| `ProductType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 商品类型 0全部商品 1只买商品 2兑换商品；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.VipDiscount` | `decimal` | 会员折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList` | `List<ProductClientViewModel>` | 门店分类商品集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].Id` | `int` | 商品id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ProductsList[].ImgStr` | `string` | 商品图片集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].ProductName` | `string` | 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].IsExchange` | `bool` | 是否兑换商品 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].ExchangeIntegral` | `int` | 兑换积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].State` | `int` | 0下架 1上架 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].ProductTagList` | `List<string>` | 商品标签集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].SellNum` | `int` | 销量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].SkuCount` | `int` | 规格数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].SkuList` | `List<ProductsSkuNameViewModel>` | 规格列表集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].SkuList[].Id` | `int` | 规格id（新增即传入0） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ProductsList[].SkuList[].ProductSkuValue` | `string` | 商品SKU值 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].EnjoyVipDiscount` | `bool` | 享受会员折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].IsHaveSku` | `bool` | 是否包含多SKU | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].IsPurchaseLimit` | `bool` | 是否限购 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].PurchaseLimitType` | `int` | 限购方式 0永久 1天 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].PurchaseLimitSum` | `int` | 限购数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductsList[].PurchaseLimitBySum` | `int` | 已购数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1`
- 一层业务调用：`ProductProvider.GetProductsList`、`UserCardProvider.GetVipMinDiscount`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.complaint.get_complaint_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 投诉与客服 |
| 用途 | 查看投诉详情 |
| 使用时机 | 在顾客视角中核对“查看投诉详情”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Complaint/GetComplaintInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetComplaintInfoResponseModel>>`；包装 `Task/DataResult`；Data `GetComplaintInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ComplaintController.cs:119` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.Uid == 0 \\|\\| requestModel.StoreId == 0 \\|\\| requestModel.Id == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.Uid == 0 \\|\\| requestModel.StoreId == 0 \\|\\| requestModel.Id == 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Id` | `long` | 代码校验必填 | 绑定=ApiController推断；[Required]；if(requestModel.Uid == 0 \\|\\| requestModel.StoreId == 0 \\|\\| requestModel.Id == 0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.UserMobile` | `string` | 投诉人联系电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ComplaintType` | `int` | 类型 0投诉，1举报、2建议 | 普通业务字段 | 可按问题需要提供 |
| `Data.ComplaintReason` | `string` | 投诉原因 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | state 状态 -1删除 0未处理 2处理中 1处理完成 | 普通业务字段 | 可按问题需要提供 |
| `Data.ComplaintInfos` | `List<ComplaintInfoViewModel>` | 投诉详情 | 普通业务字段 | 可按问题需要提供 |
| `Data.ComplaintInfos[].Id` | `long` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ComplaintInfos[].CreateType` | `int` | 发起类型 0顾客 1商家 3平台回复 | 普通业务字段 | 可按问题需要提供 |
| `Data.ComplaintInfos[].IsMain` | `bool` | 是否首次发起 | 普通业务字段 | 可按问题需要提供 |
| `Data.ComplaintInfos[].ComplaintContent` | `string` | 投诉或回复内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.ComplaintInfos[].ComplaintImgs` | `List<string>` | 举证图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreId` | `int` | 店铺id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`requestModel.Uid == 0 \|\| requestModel.StoreId == 0 \|\| requestModel.Id == 0`；`resultMsg.State`；`data?.Id > 0`；`cim.IsImg`；`ciims?.Count > 0`
- 一层业务调用：`ComplaintProvider.GetComplaintById`、`ComplaintInfoProvider.GetComplaintInfoByComplaintId`、`StoreProvider.GetStoreByIdAsync`、`ComplaintImgProvider.GetComplaintImgByComplaintInfoId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.complaint.get_complaint_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 投诉与客服 |
| 用途 | 查看投诉列表 |
| 使用时机 | 在顾客视角中核对“查看投诉列表”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Complaint/GetComplaintList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetComplaintListResponseModel>>`；包装 `Task/DataResult`；Data `GetComplaintListResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ComplaintController.cs:82` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.Uid == 0 \\|\\| requestModel.StoreId == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.Uid == 0 \\|\\| requestModel.StoreId == 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Complaints` | `List<GetComplaintListViewModel>` | 投诉列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Complaints[].Id` | `long` | 举报ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Complaints[].StoreId` | `int` | 门店ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Complaints[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Complaints[].UserMobile` | `string` | 店铺名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Complaints[].ComplaintType` | `int` | 类型 0投诉，1举报、2建议 | 普通业务字段 | 可按问题需要提供 |
| `Data.Complaints[].ComplaintReason` | `string` | 投诉原因 | 普通业务字段 | 可按问题需要提供 |
| `Data.Complaints[].ComplaintContent` | `string` | complaint_content 投诉内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.Complaints[].CreateDate` | `string` | 投诉时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Complaints[].State` | `int` | state 状态 0未处理 2处理中 1处理完成 | 普通业务字段 | 可按问题需要提供 |
| `Data.Complaints[].ComplaintImgs` | `List<string>` | 举证图片 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`requestModel.Uid == 0 \|\| requestModel.StoreId == 0`；`resultMsg.State`
- 一层业务调用：`ComplaintProvider.UserGetComplaintList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.message.get_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 消息 |
| 用途 | 获取消息列表(Y) |
| 使用时机 | 在顾客视角中核对“获取消息列表(Y)”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Message/GetList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<PageData<MessageGetListResponseViewModel>>`；包装 `DataResult`；Data `PageData<MessageGetListResponseViewModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/MessageController.cs:55` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid==0 \\|\\| model.StoreId <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageSize` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageSize == 0) | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageIndex == 0) | AI 可在服务端上限内选择 | 请求页数；普通业务字段；可按问题需要提供 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid==0 \\|\\| model.StoreId <= 0) | 服务端注入：已确认门店 | 商户Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<MessageGetListResponseViewModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Id` | `int` | 主键ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ActivityId` | `int` | 活动Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].MessTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].MessInfo` | `string` | 消息内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].MessType` | `int` | 消息类型 0.系统消息 1.金额变动语音消息，2 语音设置 3 活动消息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].State` | `int` | 状态 0已读 1未读 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CreateDate` | `string` | 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity` | `NewActivityModel` | 活动消息的信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.ActivityId` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Activity.Title` | `string` | 活动标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.IsOneReward` | `bool` | 是否有优惠券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon` | `ActivityCouponViewModel` | 优惠卷 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Activity.Coupon.CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Activity.Coupon.Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Activity.Coupon.StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Activity.Coupon.StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].Activity.Coupon.CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Activity.Coupon.Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.AcType` | `int` | 类型 0活动主动领券，1分享后领券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Activity.Coupon.CouponCount` | `int` | 已领取数量 ***** 在创建活动，修改活动 接口中 该字段表示 优惠券总发行量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid==0 \|\| model.StoreId <= 0`；`model.PageSize == 0`；`model.PageIndex == 0`；`resultMsg.State`；`model.PageIndex==1`
- 一层业务调用：`SysMessageProvider.GetSysMessageViewModelList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`状态赋值：StatusCode = 303`；`固定提示：参数不正确`；`固定提示：请求数据数量不正确`；`固定提示：页码不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.message.get_message`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 消息 |
| 用途 | 获取单个消息(Y) |
| 使用时机 | 在顾客视角中核对“获取单个消息(Y)”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Message/GetMessage` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：RelUserMessageProvider.UpdateState |
| 返回 | `Task<DataResult<GetMessageResponseViewModel>>`；包装 `Task/DataResult`；Data `GetMessageResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/MessageController.cs:102` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.MessageId==0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `MessageId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.MessageId==0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 消息ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.MessTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.MessInfo` | `string` | 消息内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.MessType` | `int` | 消息类型 0系统消息，1商户消息 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 0已读 1未读 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateDate` | `string` | 创建时间 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.MessageId==0`；`resultMsg.State`
- 一层业务调用：`SysMessageProvider.GetSysMessageById`、`RelUserMessageProvider.UpdateState`
- 疑似副作用：`RelUserMessageProvider.UpdateState`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.message.get_new_message_count`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 消息 |
| 用途 | 获取未读消息数量 |
| 使用时机 | 在顾客视角中核对“获取未读消息数量”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Message/GetNewMessageCount` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetNewMessageCountResponseViewModel>>`；包装 `Task/DataResult`；Data `GetNewMessageCountResponseViewModel` |
| 数据时效 | 聚合结果；时间范围和门店时区必须由请求参数确认 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/MessageController.cs:24` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.Uid <= 0 \\|\\| requestModel.StoreId<=0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(requestModel.Uid <= 0 \\|\\| requestModel.StoreId<=0) | 服务端注入：已确认门店 | 商户id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.NewMessageCount` | `int` | 新的系统消息数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`requestModel.Uid <= 0 \|\| requestModel.StoreId<=0`；`resultMsg.State`
- 一层业务调用：`SysMessageProvider.GetNewSysMessageCount`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.consumption.get_user_consumption_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 消费与核销 |
| 用途 | 获取单个消费明细信息 |
| 使用时机 | 顾客反馈消费、充值、余额变化或交易明细问题时，读取顾客端当前可见记录和单据详情。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Consumption/GetUserConsumptionInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<BusinessGetConsumptionInfoResponseModel>>`；包装 `Task/DataResult`；Data `BusinessGetConsumptionInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ConsumptionController.cs:228` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId == 0 \\|\\| model.ConsumptionId < 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId == 0 \\|\\| model.ConsumptionId < 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ConsumptionId` | `long` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 主键id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.ConsumptionId` | `string` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreName` | `string` | 门店名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserId` | `int` | 用户id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardId` | `int` | 会员卡Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardType` | `int` | 类型：0计次，1储值 2 限时卡 3权益卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserImg` | `string` | 会员头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserMobile` | `string` | 用户手机号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserName` | `string` | 会员昵称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserStoreName` | `string` | 会员商户昵称 | 普通业务字段 | 可按问题需要提供 |
| `Data.RemarkName` | `string` | 备注名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.PayType` | `string` | 支付名字 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayTypeInt` | `int` | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardDiscount` | `string` | 支付方式 0 线上 1 现金 2POST 3个人码微信 4个人码支付宝 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionType` | `int` | 消费方式：0 计次，1 金额，2积分，3印章 | 普通业务字段 | 可按问题需要提供 |
| `Data.OperationType` | `int` | 操作方式：0 用户，1管理员 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreUserName` | `string` | 操作店员姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ConsumptionTag` | `int` | 0支出 ，1充值,2 核减，3返还，4赠送，5付款 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionTagValue` | `string` | 交易类型 刷卡 返还…… | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionValue` | `string` | 消费值（统计数据：充值金额） | 普通业务字段 | 可按问题需要提供 |
| `Data.OtherValue` | `decimal` | 备用字段，例如次卡充值时充值的次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.AfterValue` | `string` | 操作后值（统计数据 消费次数） | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateDate` | `string` | 创建时间（统计数据 年） | 普通业务字段 | 可按问题需要提供 |
| `Data.CardName` | `string` | 卡号名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardNumber` | `string` | 卡号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.TotalPrice` | `string` | 应付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsCoupon` | `int` | 是否使用优惠卷 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsIntegral` | `bool` | 是否使用积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsProduct` | `bool` | 是否包含商品 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsService` | `bool` | 是否包含服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.BusinessRemark` | `string` | 商家备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.IsShowRemark` | `bool` | 是否向顾客展示备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.RemarkFiles` | `List<FileViewModel>` | 文件列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.RemarkFiles[].Id` | `string` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.RemarkFiles[].FilePath` | `string` | file_path 文件路径 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrintNo` | `int` | 打印机编号 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons` | `List<UserCouponViewModel>` | 优惠券信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Id` | `int` | 优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponId` | `int` | 原始优惠券Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Uid` | `int` | 用户Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StoreAddress` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Coupons[].CouponType` | `int` | 类型 0代金券 1打折券 2服务券 3礼品券 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponImg` | `string` | 优惠券背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponIcon` | `string` | 赠品图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseAudit` | `bool` | 优惠券使用是否需要使用审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSource` | `int` | 创建来源 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponBgImg` | `string` | 优惠券卡包背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsUseVip` | `bool` | 是否会员可用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsMore` | `bool` | 是否可以同时使用多张 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsBuyCard` | `bool` | 是否只用于购买会员卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseMinMoney` | `decimal` | 最低消费限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponValue` | `decimal` | 优惠卷面值（金额、折扣、现价） | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].OriginalPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].WxCouponCode` | `string` | 优惠卷Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponDescription` | `string` | 优惠卷说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StartRangeDate` | `int` | 领取后第N天生效 0立即生效 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDate` | `string` | 有效周期 格式 ps:01-02-03 表示1年2个月3天 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeDateRead` | `string` | 有效周期 的展示描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].RangeType` | `int` | 有效期类型 0固定周期，1起始结束日期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyType` | `int` | 使用频率限制 0每天 1每周 2每月 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyQuantity` | `int` | 使用频率数量0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsAuditing` | `bool` | 发放和使用优惠券是否需要审核 true 需要审核 false 无需审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].State` | `int` | 状态 -1删除 0暂停发放 1正常发放 2发放完毕 (用户)状态 -1不可用 0未生效 1正常 2已用 3已过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponRemaining` | `int` | 优惠券剩余数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].MarketingId` | `int` | 营销ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services` | `List<CouponServiceItemViewModel>` | 优惠券服务 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].IsExpired` | `bool` | 是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].ActivityId` | `int` | 活动id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].ActivityType` | `int` | 活动类型 0裂变 1抽奖 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponCenterId` | `int` | 优惠中心ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Coupons[].CouponCount` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSum` | `int` | 优惠券数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].UseFrequencyCount` | `int` | 限制频率已使用张数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].StateReasonContent` | `string` | 不可用原因说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Coupons[].CouponSourceContent` | `string` | 来源说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Service` | `List<ConsumptionServiceItemViewModel>` | 服务信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Service[].ItemId` | `int` | 项目id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Service[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Service[].ConsumptionValue` | `decimal` | consumption_value 消费值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Service[].AfterValue` | `decimal` | after_value 操作后值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Service[].PayPrice` | `decimal` | 实付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Service[].ItemUnit` | `string` | 服务单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products` | `List<ConsumptionProductViewModel>` | 商品 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductId` | `int` | 商品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].ProductTitle` | `string` | 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].SkuName` | `string` | Sku名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductImg` | `string` | 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductSum` | `int` | 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductUnit` | `int` | 商品单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].PayPrice` | `string` | 实付总金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.AfterIntegral` | `string` | 剩余积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsShop` | `bool` | 是否商城 | 普通业务字段 | 可按问题需要提供 |
| `Data.PostFee` | `string` | 快递费 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderId` | `int` | 点餐订单ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.IsCommission` | `string` | 是否使用佣金 | 普通业务字段 | 可按问题需要提供 |
| `Data.AfterCommission` | `string` | 剩余佣金 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsBookkeeping` | `bool` | 是否记账 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsVip` | `bool` | 是否是会员 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsAxc` | `bool` | 是否安心充 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsShowRefundButton` | `bool` | 是否显示退款按钮 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsRefunds` | `bool` | 是否已退款 | 普通业务字段 | 可按问题需要提供 |
| `Data.SourceId` | `string` | 退款原订单ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.RefundPrice` | `string` | 退款金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.RefundsReason` | `string` | 退款失败原因 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsShowDelete` | `bool` | 是否可以删除 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId == 0 \|\| model.ConsumptionId < 0`；`resultMsg.State`；`resultMsg.Data.IsAxc`
- 一层业务调用：`ConsumptionLogProvider.BusinessGetConsumptionLogById`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.consumption.get_user_consumption_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 消费与核销 |
| 用途 | 获取消费明细列表 |
| 使用时机 | 顾客反馈消费、充值、余额变化或交易明细问题时，读取顾客端当前可见记录和单据详情。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Consumption/GetUserConsumptionList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<PageData<GetUserConsumptionListResponseViewModel>>>`；包装 `Task/DataResult`；Data `PageData<GetUserConsumptionListResponseViewModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ConsumptionController.cs:186` |
| C/B 对照 | crmapi.consumption.business_get_user_consumption_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CardId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员卡ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId == 0) | 服务端注入：已确认门店 | 商户id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageSize` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageSize == 0) | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageIndex == 0) | AI 可在服务端上限内选择 | 请求页数；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<GetUserConsumptionListResponseViewModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Id` | `string` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].PayType` | `int` | 支付方式：0 会员卡，1 微信支付，2支付宝，3 现金 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CardType` | `int` | 类型：0计次，1储值 2时限卡 3权益卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ConsumptionType` | `int` | 消费方式：0 计次，1 金额，2积分，3印章 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].OperationType` | `int` | 操作方式：0 用户，1管理员 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ConsumptionImg` | `string` | 图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].StoreUserName` | `string` | 操作店员姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].ConsumptionTag` | `int` | consumption_tag 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6初始化,7商家录入,8过期(积分),9优惠券,10商户提现 11 调整有效期 20 限时卡停卡 21限时卡开卡 22 限时卡复卡 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ConsumptionTagValue` | `string` | 0支出 ，1充值,2 核减，3返还，4赠送，5付款,6商家初始化,10商户提现 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ConsumptionValue` | `string` | 消费值（统计数据：充值金额） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].OtherValue` | `decimal` | 备用字段，例如次卡充值时充值的次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].AfterValue` | `string` | 操作后值（统计数据 消费次数） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CreateYear` | `string` | 创建时间（统计数据 年） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CreateDate` | `string` | 创建时间（统计数据 年） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].DataType` | `int` | 数据类型0列表 1统计数据 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsCoupon` | `int` | 是否使用优惠卷 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsIntegral` | `bool` | 是否使用积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].BusinessRemark` | `string` | 商家备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].ServiceItems` | `List<ConsumptionServiceItemViewModel>` | 服务项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].ItemId` | `int` | 项目id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ServiceItems[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].ConsumptionValue` | `decimal` | consumption_value 消费值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].AfterValue` | `decimal` | after_value 操作后值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].PayPrice` | `decimal` | 实付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].ItemUnit` | `string` | 服务单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Products` | `List<ConsumptionProductViewModel>` | 商品 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Products[].ProductId` | `int` | 商品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Products[].ProductTitle` | `string` | 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Products[].SkuName` | `string` | Sku名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Products[].ProductImg` | `string` | 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Products[].ProductSum` | `int` | 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Products[].ProductUnit` | `int` | 商品单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Products[].PayPrice` | `string` | 实付总金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsHaveInfo` | `bool` | 是否有小票 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsBookkeeping` | `bool` | 是否记账 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsAxc` | `bool` | 是否安心充订单 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsRefunds` | `bool` | 是否已退款 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId == 0`；`model.PageSize == 0`；`model.PageIndex == 0`；`resultMsg.State`
- 一层业务调用：`ConsumptionLogProvider.GetConsumptionLogList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`状态赋值：StatusCode = 303`；`固定提示：参数不正确`；`固定提示：请求数据数量不正确`；`固定提示：页码不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.integral.get_integral_detail`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 积分 |
| 用途 | 获取用户积分明细 |
| 使用时机 | 在顾客视角中核对“获取用户积分明细”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Integral/GetIntegralDetail` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataList<IntegralViewModel>>`；包装 `Task/DataList`；Data `IntegralViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/IntegralController.cs:20` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.StoreId <= 0 \\|\\| requestModel.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.StoreId <= 0 \\|\\| requestModel.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageIndex` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `BeginDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `CardId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].Id` | `long` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].ConsumptionValue` | `int` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data[].AfterValue` | `int` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ConsumptionId` | `long` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].ConsumptionTag` | `int` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data[].CreateDate` | `DateTime` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`requestModel.StoreId <= 0 \|\| requestModel.Uid <= 0`
- 一层业务调用：`ConsumptionIntegralLogProvider.GetIntegralDetail`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数有误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.integral.get_integral_summary`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 积分 |
| 用途 | 获取用户积分汇总 |
| 使用时机 | 在顾客视角中核对“获取用户积分汇总”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Integral/GetIntegralSummary` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetIntegralSummaryResponseModel>>`；包装 `Task/DataResult`；Data `GetIntegralSummaryResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/IntegralController.cs:40` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.StoreId <= 0 \\|\\| requestModel.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(requestModel.StoreId <= 0 \\|\\| requestModel.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageIndex` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `BeginDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `CardId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Integral` | `int` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionIntegral` | `int` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`requestModel.StoreId <= 0 \|\| requestModel.Uid <= 0`
- 一层业务调用：`ConsumptionIntegralLogProvider.GetIntegralSummary`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数有误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.order.order_get`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 订单 |
| 用途 | 获取单一订单详情 |
| 使用时机 | 顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Order/OrderGet` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<OrderGetResponseViewModel>>`；包装 `Task/DataResult`；Data `OrderGetResponseViewModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/OrderController.cs:128` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Tid == 0 \\|\\| model.Uid==0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Tid` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Tid == 0 \\|\\| model.Uid==0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 订单id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Tid` | `long` | 主键ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TotalPrice` | `decimal` | total_price 订单总金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.DiscountPrice` | `decimal` | discount_price 优惠金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.PostPrice` | `decimal` | post_price 邮费 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayPrice` | `decimal` | pay_price 实际支付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiverName` | `string` | receiver_name 收件人姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiverState` | `string` | receiver_state 收货人的所在省份 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiverCity` | `string` | receiver_city 收货人的所在城市 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiverDistrict` | `string` | receiver_district 收货人的所在地区 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiverAddress` | `string` | receiver_address 收货人的详细地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiverMobile` | `string` | receiver_mobile 收货人的手机号码 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.PNum` | `int` | p_num 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayType` | `int` | 支付方式 1微信 2支付宝 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | state 订单状态：0未付款，1已付款未发货，2已发货，3交易成功,4取消 | 普通业务字段 | 可按问题需要提供 |
| `Data.LogisticsCompany` | `string` | logistics_company 物流公司 | 普通业务字段 | 可按问题需要提供 |
| `Data.LogisticsNo` | `string` | logistics_no 物流单号 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateDate` | `string` | create_date 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Orders` | `List<OrdersViewModel>` | 子订单合集 | 普通业务字段 | 可按问题需要提供 |
| `Data.Orders[].Oid` | `long` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Orders[].Pid` | `int` | pid 商品id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Orders[].PTitle` | `string` | p_title 商品id | 普通业务字段 | 可按问题需要提供 |
| `Data.Orders[].PPic` | `string` | p_pic 商品图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Orders[].SkuId` | `int` | sku_id skuid | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Orders[].SkuTitle` | `string` | sku_title sku名字 | 普通业务字段 | 可按问题需要提供 |
| `Data.Orders[].Price` | `decimal` | price 单价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Orders[].TotalPrice` | `decimal` | total_price 应付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Orders[].PayPrice` | `decimal` | price_price 实付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Orders[].Num` | `int` | num 购买数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Tid == 0 \|\| model.Uid==0`；`resultMsg.State`
- 一层业务调用：`TradeProvider.GetTradeInfoByTid`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.order.order_get_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 订单 |
| 用途 | 获取订单列表 |
| 使用时机 | 顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Order/OrderGetList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<PageData<OrderGetListResponseViewModel>>`；包装 `DataResult`；Data `PageData<OrderGetListResponseViewModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/OrderController.cs:84` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Tid` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 订单id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReceiverName` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 当前会话提供并临时使用；不得持久化到模型历史 | 收件人姓名；个人信息；仅在当前授权场景按最小范围提供 |
| `ReceiverMobile` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 当前会话提供并临时使用；不得持久化到模型历史 | 收货人的手机号码；个人信息；仅在当前授权场景按最小范围提供 |
| `PageSize` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageSize == 0) | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageIndex == 0) | AI 可在服务端上限内选择 | 请求页数；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<OrderGetListResponseViewModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Tid` | `long` | 主键ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ReceiverName` | `string` | 收件人姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].ReceiverState` | `string` | 收货人的所在省份 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReceiverMobile` | `string` | 收货人的手机号码 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].TotalPrice` | `decimal` | total_price 订单总金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].PNum` | `int` | p_num 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].PayPrice` | `decimal` | pay_price 实际支付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].PayType` | `int` | 支付方式 1微信 2支付宝 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].State` | `int` | 状态 0未付款 1已付款 2已发货 3成功 4取消 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CreateDate` | `string` | 下单时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Orders` | `List<OrdersViewModel>` | 子订单合集 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Orders[].Oid` | `long` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Orders[].Pid` | `int` | pid 商品id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Orders[].PTitle` | `string` | p_title 商品id | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Orders[].PPic` | `string` | p_pic 商品图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Orders[].SkuId` | `int` | sku_id skuid | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Orders[].SkuTitle` | `string` | sku_title sku名字 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Orders[].Price` | `decimal` | price 单价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Orders[].TotalPrice` | `decimal` | total_price 应付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Orders[].PayPrice` | `decimal` | price_price 实付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Orders[].Num` | `int` | num 购买数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0`；`model.PageSize == 0`；`model.PageIndex == 0`；`resultMsg.State`
- 一层业务调用：`TradeProvider.GetTradeList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`状态赋值：StatusCode = 303`；`固定提示：参数不正确`；`固定提示：请求数据数量不正确`；`固定提示：页码不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.shop_order.get_all_shop_orders`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 订单 |
| 用途 | 获取所有订单 |
| 使用时机 | 顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/ShopOrder/GetAllShopOrders` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataList<GetAllShopOrdersResponseModel>`；包装 `DataList`；Data `GetAllShopOrdersResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ShopOrderController.cs:21` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageIndex` | `int` | 可选/有默认值 | 绑定=ApiController推断；默认值=1 | AI 可在服务端上限内选择 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 可选/有默认值 | 绑定=ApiController推断；默认值=20 | AI 可在服务端上限内选择 | 源码属性注释缺失；普通业务字段；可按问题需要提供 |
| `Keywords` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 当前会话提供并临时使用；不得持久化到模型历史 | 关键词，可为空 订单号、姓名、手机号等；个人信息；仅在当前授权场景按最小范围提供 |
| `Status` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 订单状态：-1 全部，0 等待买家付款；1 等待卖家发货 2 卖家已发货 3 订单完成 4 订单关闭；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].Id` | `int` | id 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Uid` | `int` | uid 用户ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].ConsumptionId` | `long` | 订单编号 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].IsExchange` | `bool` | 是否兑换 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ExchangeIntegral` | `int` | 兑换积分 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Payment` | `decimal` | 实付款 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Status` | `int` | 订单状态 | 普通业务字段 | 可按问题需要提供 |
| `Data[].TakeTime` | `string` | 自提时间（例：10:00） | 普通业务字段 | 可按问题需要提供 |
| `Data[].OrderType` | `int` | 0邮寄 1配送 2自提 | 普通业务字段 | 可按问题需要提供 |
| `Data[].PickupCode` | `string` | 自提提货码 | 普通业务字段 | 可按问题需要提供 |
| `Data[].CreateDate` | `DateTime` | 下单时间 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ProductCount` | `int` | 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products` | `List<ShopOrderProductModel>` | 商品列表 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].Id` | `int` | id 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Products[].StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Products[].Uid` | `int` | uid 用户ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Products[].ShopOrderId` | `int` | shop_order_id 订单ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Products[].ProductId` | `int` | product_id 商品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Products[].SkuId` | `int` | sku_id 商品SkuID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Products[].Pno` | `string` | 货号 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].ProductName` | `string` | product_name 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].ProductImg` | `string` | product_img 商品图片 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].ProductCount` | `int` | product_num 数量 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].IsExchange` | `bool` | 是否兑换商品 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].ExchangeIntegral` | `int` | 兑换积分 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].ProductPrice` | `decimal` | product_price 商品价格 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].SkuString` | `string` | sku_string SKU描述 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].SkuValue` | `string` | sku_value SKU值 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].State` | `int` | 状态 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].CreateDate` | `DateTime` | create_date | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].CreateBy` | `int` | create_by | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].UpdateDate` | `DateTime` | update_date | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].UpdateBy` | `int` | update_by | 普通业务字段 | 可按问题需要提供 |
| `Data[].Products[].TenantId` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`
- 一层业务调用：`ShopOrderProvider.GetAllShopOrders`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 200`；`状态赋值：StatusCode = 301`；`固定提示：请求参数有误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.shop_order.get_shop_order_detail`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 订单 |
| 用途 | 获取订单详情 |
| 使用时机 | 顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/ShopOrder/GetShopOrderDetail` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetShopOrderDetailResponseModel>>`；包装 `Task/DataResult`；Data `GetShopOrderDetailResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ShopOrderController.cs:50` |
| C/B 对照 | crmapi.shop_order.get_shop_order_detail |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0 \\|\\| model.ShopOrderId <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| model.Uid <= 0 \\|\\| model.ShopOrderId <= 0) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ShopOrderId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| model.Uid <= 0 \\|\\| model.ShopOrderId <= 0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 商城订单ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Id` | `int` | id 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Uid` | `int` | uid 用户ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.BuyerHeadImg` | `string` | 买家头像 | 普通业务字段 | 可按问题需要提供 |
| `Data.PicPath` | `string` | pic_path 商品图片绝对途径 | 普通业务字段 | 可按问题需要提供 |
| `Data.Title` | `string` | title 订单标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Status` | `int` | status 订单状态：-2退款，0 等待买家付款；1 等待卖家发货 2 卖家已发货 3 订单完成 4 订单关闭 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsExchange` | `bool` | 是否兑换 | 普通业务字段 | 可按问题需要提供 |
| `Data.ExchangeIntegral` | `int` | 兑换积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.ProductCount` | `int` | product_number 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.NeedPayment` | `decimal` | need_payment 应付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Payment` | `decimal` | payment 实付金额。精确到2位小数;单位:元。如:200.07，表示:200元7分 | 普通业务字段 | 可按问题需要提供 |
| `Data.NeedPost` | `bool` | need_post 是否需要邮寄 | 普通业务字段 | 可按问题需要提供 |
| `Data.PostFee` | `decimal` | post_fee 邮费。精确到2位小数;单位:元。如:200.07，表示:200元7分 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiverName` | `string` | receiver_name 收货人的姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiverAddress` | `string` | receiver_address 收货人的详细地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiverZip` | `string` | receiver_zip 收货人的邮编 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReceiverMobile` | `string` | receiver_mobile 收货人的手机号码 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.PostCompany` | `string` | post_company 快递公司 | 普通业务字段 | 可按问题需要提供 |
| `Data.PostOrderNo` | `string` | post_order_no 快递单号 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Remark` | `string` | remark 买家备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.BusinessRemark` | `string` | business_remark 卖家备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.BuyerName` | `string` | buyer_name 买家名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayMethod` | `int` | pay_method 支付方式：0 会员卡支付、1微信支付、2支付宝支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateDate` | `DateTime` | create_date 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayDate` | `DateTime` | pay_date 支付时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.PostDate` | `DateTime` | post_date 发货时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UpdateDate` | `DateTime` | update_date 更新时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateBy` | `int` | create_by 创建人 | 普通业务字段 | 可按问题需要提供 |
| `Data.UpdateBy` | `int` | update_by 更新人 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionId` | `string` | consumption_id 财务ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.IntegralDeduct` | `decimal` | 积分减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CommissionDeduct` | `decimal` | 佣金减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardDeduct` | `decimal` | 权益卡、储值卡减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponDeduct` | `decimal` | 优惠券减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products` | `List<ShopOrderProductModel>` | 商品列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].Id` | `int` | id 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].Uid` | `int` | uid 用户ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].ShopOrderId` | `int` | shop_order_id 订单ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].ProductId` | `int` | product_id 商品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].SkuId` | `int` | sku_id 商品SkuID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Products[].Pno` | `string` | 货号 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductName` | `string` | product_name 商品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductImg` | `string` | product_img 商品图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductCount` | `int` | product_num 数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].IsExchange` | `bool` | 是否兑换商品 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ExchangeIntegral` | `int` | 兑换积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].ProductPrice` | `decimal` | product_price 商品价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].SkuString` | `string` | sku_string SKU描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].SkuValue` | `string` | sku_value SKU值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].State` | `int` | 状态 | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].CreateDate` | `DateTime` | create_date | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].CreateBy` | `int` | create_by | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].UpdateDate` | `DateTime` | update_date | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].UpdateBy` | `int` | update_by | 普通业务字段 | 可按问题需要提供 |
| `Data.Products[].TenantId` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardId` | `int` | 会员卡ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.IsShowRefundButton` | `bool` | 是否显示退款按钮 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsRefunds` | `bool` | 是否已退款 | 普通业务字段 | 可按问题需要提供 |
| `Data.SourceId` | `string` | 退款原订单ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.RefundPrice` | `decimal` | 退款金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreUserName` | `string` | 操作店员姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.TakeTime` | `string` | 自提时间（例：10:00） | 普通业务字段 | 可按问题需要提供 |
| `Data.OrderType` | `int` | 0邮寄 1配送 2自提 | 普通业务字段 | 可按问题需要提供 |
| `Data.PickupCode` | `string` | 自提提货码 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0 \|\| model.ShopOrderId <= 0`
- 一层业务调用：`ShopOrderProvider.GetShopOrderDetail`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数有误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_course`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取单个课目 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetCourse` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetCourseResponseModel>>`；包装 `Task/DataResult`；Data `GetCourseResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:1011` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| (model.CourseId < 1 && model.LessonsId < 1)) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| (model.CourseId < 1 && model.LessonsId < 1)) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseId` | `int` | 参与组合校验 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| (model.CourseId < 1 && model.LessonsId < 1)) | 必须来自同一会话上游 API 结果或服务端对象引用 | 课目id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `LessonsId` | `int` | 参与组合校验 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| (model.CourseId < 1 && model.LessonsId < 1)) | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseType` | `int` | 授课类型；0-团课，1-私教 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseImageId` | `long` | 课程图片id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CourseImage` | `string` | 课程图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.ImageStyle` | `int` | 图片样式 0明亮 1暗黑 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseTime` | `int` | 授课时长（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs` | `List<CourseStaffViewModel>` | 教练信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].Id` | `long` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].UserName` | `string` | 教练名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Staffs[].UserImage` | `string` | 教练图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePeopleCount` | `int` | 最大授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.MinPeople` | `int` | 最小授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseStar` | `int` | 难度星级1-10 | 普通业务字段 | 可按问题需要提供 |
| `Data.Tags` | `List<StoreReservationTagViewModel>` | 标签 | 普通业务字段 | 可按问题需要提供 |
| `Data.Tags[].Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Tags[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.ClassTag` | `StoreReservationTagViewModel` | 分类 | 普通业务字段 | 可按问题需要提供 |
| `Data.ClassTag.Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ClassTag.TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseTools` | `List<StoreReservationTagViewModel>` | 课程工具 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseTools[].Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CourseTools[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseColor` | `string` | 颜色 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePlace` | `CoursePlaceViewModel` | 教室 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePlace.Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CoursePlace.PlaceName` | `string` | 场地名 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseDescribe` | `string` | 课程描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardCount` | `int` | 支持卡的数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.SchedulingCount` | `long` | 排课数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePrice` | `StoreCoursePriceViewModel` | 单次付费信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePrice.IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePrice.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePrice.VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePrice.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePrice.State` | `int` | 状态；0-禁用，1-启用 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsRecommend` | `bool` | 是否推荐，用作首页展示 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials` | `List<StoreMaterialViewModel>` | 关联素材 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].Id` | `int` | 素材ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Materials[].StoreId` | `int` | 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Materials[].CategoryId` | `int` | 素材分类ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Materials[].CategoryName` | `string` | 素材分类名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].MaterialName` | `string` | 素材名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].MaterialType` | `int` | 素材类型：1图片，2视频，3视频号链接 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FilePath` | `string` | 素材路径；图片/视频为文件地址，视频号为链接地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FileUrl` | `string` | 素材完整访问地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FileName` | `string` | 文件名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FileExt` | `string` | 文件扩展名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FileSize` | `long` | 文件大小，单位字节 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].MimeType` | `string` | 文件MIME类型 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].VideoCover` | `string` | 视频封面路径 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].VideoCoverUrl` | `string` | 视频封面完整访问地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].VideoNo` | `string` | 视频号标识 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].VideoTimeLength` | `int` | 视频时长，单位秒 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].Width` | `int` | 素材宽度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].Height` | `int` | 素材高度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].Remark` | `string` | 备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Materials[].OrderBy` | `int` | 排序值，值越大越靠前 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].State` | `int` | 状态：1启用，0停用，-1删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态；0-未开放，1-已开放，-1已删除 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| (model.CourseId < 1 && model.LessonsId < 1)`；`resultMsg.State`；`courseId < 1 && model.LessonsId > 0`；`course?.Id > 0`；`model.LessonsId > 0`；`courseStaffs?.Count > 0`；`staffModel?.Id > 0`
- 一层业务调用：`StoreLessonsProvider.GetStoreLessonsFirstOrDefaultByCondition`、`StoreCourseProvider.GetStoreCourses`、`StoreLessonsProvider.GetSchedulingCount`、`StoreMaterialProvider.GetLessonsMaterials`、`StoreMaterialProvider.GetCourseMaterials`、`StoreLessonsStaffProvider.GetStoreLessonsStaffElementsByCondition`、`TenantUserProvider.GetTenantUserByStoreId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_course_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取课目列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetCourseList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetCourseListV2ResponseModel>>`；包装 `Task/DataResult`；Data `GetCourseListV2ResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:963` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 授课类型；0-团课，1-私教；普通业务字段；可按问题需要提供 |
| `State` | `int?` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 课目状态 不传显示所有 0停用的 1有效的；普通业务字段；可按问题需要提供 |
| `TagIds` | `List<long>` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 标签；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses` | `List<StoreCourseViewModel>` | 管理员列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].CourseType` | `int` | 授课类型；0-团课，1-私教 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseDescribe` | `string` | 课程描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseImageId` | `long` | 课程图片id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].CourseMainImage` | `string` | 课程图片(长图) | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseSmallImage` | `string` | 课程图片（方图） | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].ImageStyle` | `int` | 图片样式 0明亮 1暗黑 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Tags` | `List<StoreReservationTagViewModel>` | 标签 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Tags[].Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].Tags[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].ClassTag` | `StoreReservationTagViewModel` | 分类 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].ClassTag.Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].ClassTag.TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseTools` | `List<StoreReservationTagViewModel>` | 课程工具 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseTools[].Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].CourseTools[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseTime` | `int` | 授课时长（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePeopleCount` | `int` | 最大授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].MinPeople` | `int` | 最小授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseStar` | `int` | 难度星级1-10 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CourseColor` | `string` | 颜色 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].IsRecommend` | `bool` | 是否推荐，用作首页展示 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePlace` | `CoursePlaceViewModel` | 教室 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePlace.Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].CoursePlace.PlaceName` | `string` | 场地名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CardCount` | `int` | 支持卡的数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].SchedulingCount` | `long` | 排课数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].State` | `int` | 状态；0-未开放，1-已开放，-1已删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Staffs` | `List<CourseStaffViewModel>` | 教练信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Staffs[].Id` | `long` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].Staffs[].UserName` | `string` | 教练名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Courses[].Staffs[].UserImage` | `string` | 教练图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos` | `List<CourseCardBindInfoViewModelModel>` | 课卡绑定信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].PrepaidCardId` | `long` | 储值卡id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].BindCardInfos[].CardType` | `int` | 类型：0计次，1储值 2时限 3权益 4安心充 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].CardName` | `string` | 卡名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].ValidityPeriod` | `int` | （时限卡）扣减有效期 天 0不扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].CardValue` | `decimal` | 扣减卡余额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].Services` | `List<CourseCardBindItemViewModel>` | 服务项目列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].Services[].ItemId` | `long` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].BindCardInfos[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].Services[].ItemUnit` | `string` | 项目单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].Services[].ItemValue` | `int` | 服务项 卡价值 0 不支持 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].BindCardInfos[].State` | `int` | 关联状态；0-禁用，1-启用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePrice` | `StoreCoursePriceViewModel` | 单次付费信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePrice.IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePrice.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePrice.VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePrice.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].CoursePrice.State` | `int` | 状态；0-禁用，1-启用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos` | `List<StoreMaterialViewModel>` | 关联视频素材 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].Id` | `int` | 素材ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].Videos[].StoreId` | `int` | 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].Videos[].CategoryId` | `int` | 素材分类ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Courses[].Videos[].CategoryName` | `string` | 素材分类名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].MaterialName` | `string` | 素材名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].MaterialType` | `int` | 素材类型：1图片，2视频，3视频号链接 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].FilePath` | `string` | 素材路径；图片/视频为文件地址，视频号为链接地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].FileUrl` | `string` | 素材完整访问地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].FileName` | `string` | 文件名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].FileExt` | `string` | 文件扩展名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].FileSize` | `long` | 文件大小，单位字节 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].MimeType` | `string` | 文件MIME类型 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].VideoCover` | `string` | 视频封面路径 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].VideoCoverUrl` | `string` | 视频封面完整访问地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].VideoNo` | `string` | 视频号标识 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].VideoTimeLength` | `int` | 视频时长，单位秒 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].Width` | `int` | 素材宽度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].Height` | `int` | 素材高度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].Remark` | `string` | 备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Courses[].Videos[].OrderBy` | `int` | 排序值，值越大越靠前 | 普通业务字段 | 可按问题需要提供 |
| `Data.Courses[].Videos[].State` | `int` | 状态：1启用，0停用，-1删除 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1`；`resultMsg.State`；`courseData?.Count > 0`；`course?.Id > 0`
- 一层业务调用：`StoreCourseProvider.GetStoreCourses`、`StoreLessonsProvider.GetSchedulingCount`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_lessons`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取单个课程信息 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetLessons` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetLessonsResponseModel>>`；包装 `Task/DataResult`；Data `GetLessonsResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:1310` |
| C/B 对照 | crmapi.lessons.get_lessons |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.LessonsId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.LessonsId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `LessonsId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.LessonsId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseId` | `long` | 课目id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CourseType` | `int` | 授课类型；0-团课，1-私教 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseImage` | `string` | 课程图片id | 普通业务字段 | 可按问题需要提供 |
| `Data.ImageStyle` | `int` | 图片样式 0明亮 1暗黑 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseName` | `string` | 课目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.BeginDate` | `string` | 开始时间 yyyy-MM-dd hh:mm | 普通业务字段 | 可按问题需要提供 |
| `Data.EndDate` | `string` | 结束时间 yyyy-MM-dd hh:mm | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseTime` | `int` | 授课时长（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs` | `List<CourseStaffViewModel>` | 教练信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].Id` | `long` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].UserName` | `string` | 教练名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Staffs[].UserImage` | `string` | 教练图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.TeachCount` | `int` | 最大授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.MinPeople` | `int` | 最小授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseColor` | `string` | 颜色 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseStar` | `int` | 难度星级1-10 | 普通业务字段 | 可按问题需要提供 |
| `Data.SignDate` | `string` | 签到时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CancelDate` | `string` | 取消时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePlace` | `CoursePlaceViewModel` | 教室 | 普通业务字段 | 可按问题需要提供 |
| `Data.CoursePlace.Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CoursePlace.PlaceName` | `string` | 场地名 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsAutoCancel` | `bool` | 是否自动停课 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态：0未开课，1已开课，2取消 3人数不足 5完课 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials` | `List<StoreMaterialViewModel>` | 关联素材 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].Id` | `int` | 素材ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Materials[].StoreId` | `int` | 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Materials[].CategoryId` | `int` | 素材分类ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Materials[].CategoryName` | `string` | 素材分类名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].MaterialName` | `string` | 素材名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].MaterialType` | `int` | 素材类型：1图片，2视频，3视频号链接 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FilePath` | `string` | 素材路径；图片/视频为文件地址，视频号为链接地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FileUrl` | `string` | 素材完整访问地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FileName` | `string` | 文件名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FileExt` | `string` | 文件扩展名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].FileSize` | `long` | 文件大小，单位字节 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].MimeType` | `string` | 文件MIME类型 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].VideoCover` | `string` | 视频封面路径 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].VideoCoverUrl` | `string` | 视频封面完整访问地址 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].VideoNo` | `string` | 视频号标识 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].VideoTimeLength` | `int` | 视频时长，单位秒 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].Width` | `int` | 素材宽度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].Height` | `int` | 素材高度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].Remark` | `string` | 备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Materials[].OrderBy` | `int` | 排序值，值越大越靠前 | 普通业务字段 | 可按问题需要提供 |
| `Data.Materials[].State` | `int` | 状态：1启用，0停用，-1删除 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| model.LessonsId < 1`；`resultMsg.State`；`lms?.Id > 0`；`lms.CourseType == 0 \|\| lms.CourseType == 2`；`cm?.Id > 0`；`lms.CoursePlaceId > 0`；`pm?.Id > 0`；`courseStaffs?.Count > 0`；`staffModel?.Id > 0`；`lms.SignDate != null`；`lms.CancelDate != null`；`lms.CourseImageId > 0`
- 一层业务调用：`StoreLessonsProvider.GetStoreLessonsFirstOrDefaultByCondition`、`StoreMaterialProvider.GetLessonsMaterials`、`StoreCourseProvider.GetStoreCourses`、`StorePlaceProvider.GetStorePlaceById`、`StoreLessonsStaffProvider.GetStoreLessonsStaffElementsByCondition`、`TenantUserProvider.GetTenantUserByStoreId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_lessons_rank`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取上课排名 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetLessonsRank` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetLessonsRankResponseModel>>`；包装 `Task/DataResult`；Data `GetLessonsRankResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:77` |
| C/B 对照 | crmapi.lessons.business_get_lessons_rank |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1 \\|\\| string.IsNullOrEmpty(model.ReservationDate)) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1 \\|\\| string.IsNullOrEmpty(model.ReservationDate)) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid < 1 \\|\\| model.StoreId < 1 \\|\\| string.IsNullOrEmpty(model.ReservationDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 查询月份；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.RankData` | `List<LessonsRankViewModel>` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.RankData[].Rank` | `long` | 排名 | 普通业务字段 | 可按问题需要提供 |
| `Data.RankData[].CardId` | `int` | 会员id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.RankData[].Uid` | `int` | 用户id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.RankData[].UserName` | `string` | 用户名字 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.RankData[].UserImg` | `string` | 用户头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.RankData[].LessonsCount` | `long` | 上课次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.RankData[].IsInBlackList` | `bool` | 是否在黑名单中（仅生效中） | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1 \|\| string.IsNullOrEmpty(model.ReservationDate)`；`resultMsg.State`；`rankData != null`
- 一层业务调用：`StoreReservationProvider.GetLessonsRank`、`PrivacyMaskHelper.MaskUserName`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_lessons_statistics`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取上课统计 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetLessonsStatistics` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetLessonsStatisticsResponseModel>>`；包装 `Task/DataResult`；Data `GetLessonsStatisticsResponseModel` |
| 数据时效 | 聚合结果；时间范围和门店时区必须由请求参数确认 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:35` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 查询月份；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsCount` | `long` | 累计上课 | 普通业务字段 | 可按问题需要提供 |
| `Data.MonthLessonsRank` | `long` | 本月上课排名 | 普通业务字段 | 可按问题需要提供 |
| `Data.MonthGroupLessonsCount` | `long` | 本月团课 | 普通业务字段 | 可按问题需要提供 |
| `Data.MonthPrivateLessonsCount` | `long` | 本月私教 | 普通业务字段 | 可按问题需要提供 |
| `Data.WaitLessonsCount` | `long` | 待上课 | 普通业务字段 | 可按问题需要提供 |
| `Data.MissAppointmentLessonsCount` | `long` | 累计旷课 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1`；`resultMsg.State`；`!string.IsNullOrEmpty(model.ReservationDate)`
- 一层业务调用：`StoreReservationProvider.GetLessonsStatistics`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_people_reservation_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取个人预约信息 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetPeopleReservationInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetPeopleReservationInfoResponseModel>>`；包装 `Task/DataResult`；Data `GetPeopleReservationInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:1082` |
| C/B 对照 | crmapi.lessons.get_people_reservation_info |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.ReservationId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.ReservationId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationId` | `long` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.ReservationId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 预约Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CardId` | `long` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `UserId` | `long` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 顾客id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationId` | `long` | 当前预约Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserId` | `int` | 顾客Id，用于详情内继续执行签到和笔记操作 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardId` | `int` | 会员主卡Id，用于详情内读取可用课卡和保存上课笔记 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsId` | `int` | 当前课次Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CourseId` | `int` | 当前课程项目Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StaffId` | `int` | 私教员工Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.IsExperience` | `bool` | 是否体验预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsPay` | `bool` | 是否已经产生预约消费 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserName` | `string` | 顾客名称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserImg` | `string` | 顾客头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.LessonsName` | `string` | 课程名字 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseImage` | `string` | 课次创建时选择的课程背景图 | 普通业务字段 | 可按问题需要提供 |
| `Data.ImageStyle` | `int` | 课程背景图显示风格 | 普通业务字段 | 可按问题需要提供 |
| `Data.StaffName` | `string` | 私教教练名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.StaffImg` | `string` | 私教教练头像 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseType` | `int` | 课程类型 0团课 1私教 2班课 | 普通业务字段 | 可按问题需要提供 |
| `Data.BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Remark` | `string` | 备注 （用户） | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.BusinessRemark` | `string` | 备注（商家） | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.PeopleCount` | `int` | 人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 -2未到店(旷课)，-1已取消，0未确认，1以确定，2到店（签到） 3上课中 5上课中 10候补 | 普通业务字段 | 可按问题需要提供 |
| `Data.OperationLogs` | `List<PeopleReservationInfoResponseModel>` | 操作日志 | 普通业务字段 | 可按问题需要提供 |
| `Data.OperationLogs[].Id` | `long` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.OperationLogs[].ConsumptionId` | `string` | 财务ID 使用后更新 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.OperationLogs[].LogType` | `int` | 上课日志类型 0预约 1修改预约 2取消预约，10签到 11取消签到 20旷课 21取消旷课 | 普通业务字段 | 可按问题需要提供 |
| `Data.OperationLogs[].SignFile` | `string` | 签到文件 | 普通业务字段 | 可按问题需要提供 |
| `Data.OperationLogs[].IsRepeal` | `bool` | 是否撤销 | 普通业务字段 | 可按问题需要提供 |
| `Data.OperationLogs[].OperationType` | `int` | 操作方式：0 用户，1管理员,3 共享用户 10系统 | 普通业务字段 | 可按问题需要提供 |
| `Data.OperationLogs[].OperationUserName` | `string` | 操作者名称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.OperationLogs[].OperationUserImg` | `string` | 操作者头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.OperationLogs[].OperationDate` | `string` | 操作者时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Note` | `string` | 笔记内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.NoteId` | `long` | 上课笔记Id；为0表示当前预约尚未添加笔记 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Files` | `List<FileViewModel>` | 文件列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Files[].Id` | `string` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Files[].FilePath` | `string` | file_path 文件路径 | 普通业务字段 | 可按问题需要提供 |
| `Data.LastUpdateDate` | `string` | 最后操作时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsCancel` | `bool` | 是否可以取消预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.LastCancelDate` | `string` | 最晚取消时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos` | `List<GetReservationInfosModel>` | 预约信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].ControlName` | `string` | 控件名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].ControlValue` | `string` | 控件值 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReservationInfos[].IsShow` | `bool` | 是否对C端显示 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].IsMust` | `int` | 是否必填项 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].ControlType` | `string` | 控件类型 input,radio,select.... | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].ControlInstructions` | `string` | 控件说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].Items` | `List<GetReservationItemControlsListViewModel>` | 选项列表 控件类型 为 radio select 不为空 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].Items[].Id` | `int` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationInfos[].Items[].CommonReservationControlsId` | `int` | cid 控件id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationInfos[].Items[].ItemValue` | `string` | item_value 值 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].Items[].ItemName` | `string` | item_name 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].Items[].IsDefault` | `int` | is_default 是否是默认 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| model.ReservationId < 1`；`resultMsg.State`；`rm?.Id > 0`；`snm?.Id > 0`；`snm.IsHaveImage`；`images.Count > 0`；`rm.State == 0 \|\| rm.State == 1`；`lessonsInfo.CourseType == 0`；`reservationSeting.GroupLessonIsCancel`；`reservationSeting.IsCancel`；`rm.State == 10`；`rm.CardId > 0`
- 一层业务调用：`StoreReservationProvider.GetStoreReservationById`、`StoreReservationNoteProvider.GetStoreReservationNoteFirstOrDefaultByCondition`、`StoreLessonsProvider.GetStoreLessonsFirstOrDefaultByCondition`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreProvider.GetStoreDateTime`、`UserCardProvider.BusinessGetUserCardBasisInfo`、`UsersInfoProvider.UsersInfoGetByUid`、`UserLessonsLogProvider.GetUserLessonsLogElementsByCondition`、`TenantUserProvider.GetTenantUserByStoreId`、`StoreReservationDetailedProvider.GetReservationInfoList`、`StoreReservationControlsProvider.GetReservationControlsList`、`CommonReservationControlsItemProvider.GetCommonReservationControlsItemList`、`StoreReservationControlsProvider.GetStoreReservationControlsByInstructtions`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_user_lessons_note`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取会员上课笔记详细信息 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetUserLessonsNote` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetUserLessonsNoteResponseModel>>`；包装 `Task/DataResult`；Data `GetUserLessonsNoteResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:195` |
| C/B 对照 | crmapi.lessons.get_user_lessons_note |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.CardId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.CardId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Id` | `long` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 笔记id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.CardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员卡id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsId` | `long` | 课程id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CreateDate` | `string` | 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateUser` | `string` | 创建人 | 普通业务字段 | 可按问题需要提供 |
| `Data.BeginDate` | `string` | 课程开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseName` | `string` | 课程名字 | 普通业务字段 | 可按问题需要提供 |
| `Data.Note` | `string` | 笔记内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.Files` | `List<FileViewModel>` | 文件列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Files[].Id` | `string` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Files[].FilePath` | `string` | file_path 文件路径 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1 \|\| model.CardId < 1`；`resultMsg.State`；`snm?.Id > 0`；`snm.IsHaveImage`；`images?.Count > 0`；`snm.ReservationId > 0`；`rm?.Id > 0 && rm.LessonsId > 0`
- 一层业务调用：`StoreReservationNoteProvider.GetStoreReservationNoteFirstOrDefaultByCondition`、`StoreReservationProvider.GetStoreReservationById`、`TenantUserProvider.GetTenantUserByStoreId`、`StoreLessonsProvider.GetStoreLessonsElementById`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_user_lessons_note_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取会员上课笔记列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetUserLessonsNoteList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<PageData<GetUserLessonsNoteListResponseModel>>>`；包装 `Task/DataResult`；Data `PageData<GetUserLessonsNoteListResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:160` |
| C/B 对照 | crmapi.lessons.get_user_lessons_note_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.CardId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.CardId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageSize` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 请求页数；普通业务字段；可按问题需要提供 |
| `CardId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.CardId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员卡id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<GetUserLessonsNoteListResponseModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Id` | `long` | 笔记id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].CourseName` | `string` | 课程名字 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].StaffName` | `string` | 店员名字 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsHaveImage` | `bool` | 是否包含图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Note` | `string` | 笔记内容 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CreateTime` | `string` | 创建时间 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1 \|\| model.CardId < 1`；`resultMsg.State`
- 一层业务调用：`StoreReservationNoteProvider.GetStoreReservationNotes`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.lessons.get_user_lessons_reservation_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课次与排课 |
| 用途 | 获取会员已约列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Lessons/GetUserLessonsReservationList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<PageData<GetUserLessonsReservationListResponseModel>>>`；包装 `Task/DataResult`；Data `PageData<GetUserLessonsReservationListResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/LessonsController.cs:125` |
| C/B 对照 | crmapi.lessons.get_user_lessons_reservation_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageSize` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 请求页数；普通业务字段；可按问题需要提供 |
| `BeginDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 开始时间 yyyy-MM-dd；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 开始时间 yyyy-MM-dd；普通业务字段；可按问题需要提供 |
| `CardId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 会员卡id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ChildCardId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 子卡id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseType` | `int?` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 课程类型 0团课 1私教 2班课；普通业务字段；可按问题需要提供 |
| `OrderBy` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 排序方式0 上课时间正序 1上课时间倒序；普通业务字段；可按问题需要提供 |
| `State` | `int?` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 状态 -2未到店(旷课)，-1已取消，0未确认，1以确定，2到店（签到） 3上课中 5上课中 10候补；普通业务字段；可按问题需要提供 |
| `IsRefunds` | `bool?` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 是否已退款；普通业务字段；可按问题需要提供 |
| `IsSign` | `bool?` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 是否签到；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<GetUserLessonsReservationListResponseModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReservationId` | `int` | 预约Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ReservationTime` | `string` | 预约时间段（时间部分 10:30） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].StaffName` | `string` | 技师名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].StaffImg` | `string` | 技师头像 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Remark` | `string` | 客户留言 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].BusinessRemark` | `string` | 商家备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].State` | `int` | -2未到店(旷课)，-1已取消，0未确认，1以确定，2到店（签到） 3上课中 5上课中 10候补 状态 -2未到店(旷课)，-1已取消，0未确认，1以确定，2到店（签到） 3上课中 5完课 10候补 20完课未签到 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].SignDate` | `string` | 签到时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseId` | `int` | 课目id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].LessonsId` | `int` | 课ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].CourseName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseColor` | `string` | 课程颜色 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseDesc` | `string` | 课程描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseStar` | `int` | 难度星级1-10 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].TeachCount` | `int` | 授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseType` | `int` | 课程类型：0私教，1团课 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].TeachMin` | `int` | 授课时长（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ConsumptionId` | `string` | 财务ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ConsumptionValue` | `string` | 消费值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].AfterValue` | `string` | 消费后余额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsRefunds` | `bool` | 是否已退款 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ConsumptionState` | `int` | 财务状态 0未支付 1已支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsSetNote` | `bool` | 是否设置了笔记 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsCancel` | `bool` | 是否可以取消预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems` | `List<ConsumptionServiceItemViewModel>` | 服务项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].ItemId` | `int` | 项目id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ServiceItems[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].ConsumptionValue` | `decimal` | consumption_value 消费值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].AfterValue` | `decimal` | after_value 操作后值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].PayPrice` | `decimal` | 实付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ServiceItems[].ItemUnit` | `string` | 服务单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Tags` | `List<StoreReservationTagViewModel>` | 标签 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Tags[].Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Tags[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ClassTag` | `StoreReservationTagViewModel` | 分类 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ClassTag.Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ClassTag.TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePlace` | `CoursePlaceViewModel` | 教室 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePlace.Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].CoursePlace.PlaceName` | `string` | 场地名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Staffs` | `List<CourseStaffViewModel>` | 教练信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Staffs[].Id` | `long` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Staffs[].UserName` | `string` | 教练名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].Staffs[].UserImage` | `string` | 教练图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsExperience` | `bool` | 是否体验用户 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CreateDate` | `string` | 预约创建时间 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`
- 一层业务调用：`StoreReservationProvider.GetUserLessonsReservationList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store_course.get_store_course_type`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 课程 |
| 用途 | 获取当前店铺团课、私教课信息 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/StoreCourse/GetStoreCourseType` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreCourseTypeResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreCourseTypeResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreCourseController.cs:20` |
| C/B 对照 | crmapi.store_course.get_store_course_type |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsTuan` | `bool` | 是否有团课 true-有，false-无 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsSi` | `bool` | 是否有私教课 true-有，false-无 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：未发现显式 `if` 参数校验；这不代表所有参数都可省略。
- 一层业务调用：`StoreCourseProvider.GetStoreCourseType`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store.get_integral_description`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取积分说明 |
| 使用时机 | 在顾客视角中核对“获取积分说明”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Store/GetIntegralDescription` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetIntegralDescriptionResponseModel>>`；包装 `Task/DataResult`；Data `GetIntegralDescriptionResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreController.cs:348` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 店铺ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.IntegralInfo` | `string` | 积分说明 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1`；`resultMsg.State`
- 一层业务调用：`StoreIntegralSetProvider.StoreIntegralGetByStoreId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store.get_store_display_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取商户显示信息信息 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Store/GetStoreDisplayInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreDisplayInfoResponseViewModel>>`；包装 `Task/DataResult`；Data `GetStoreDisplayInfoResponseViewModel` |
| 数据时效 | 可能包含缓存结果；不能等同数据库即时状态 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreController.cs:198` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1) | 服务端注入：已确认门店 | 商户id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreIntroduce` | `string` | 店铺介绍 | 普通业务字段 | 可按问题需要提供 |
| `Data.ManageWechat` | `string` | 店长微信 | 普通业务字段 | 可按问题需要提供 |
| `Data.ManageWechatImage` | `string` | 店长微信图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Images` | `List<string>` | 环境照片 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsRank` | `bool` | 是否显示上课排行榜 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsPrivateLessons` | `bool` | 是否开启私教 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsGroupLessons` | `bool` | 是否开启团课 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsShowType` | `int` | 排课显示类型 0公开 1仅会员 2仅有余额会员 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1`；`resultMsg.State`；`sm != null && sm.Id > 0`；`sm.State < 0`
- 一层业务调用：`StoreProvider.GetStoreByIdAsync`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreSetingProvider.GetStoreSetingByStoreId`、`CloudStoreIndexBannerProvider.GetCloudStoreIndexByStoreId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 310`；`固定提示：参数不正确`；`固定提示：店铺被封禁！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store.get_store_index_data`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取首页展示功能模块及数据 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Store/GetStoreIndexData` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreIndexDataResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreIndexDataResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreController.cs:435` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `IsLoadData` | `bool` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 是否加载数据；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Modules` | `IList<StoreIndexDataItem>` | 模块列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Modules[].Module` | `string` | 模块 | 普通业务字段 | 可按问题需要提供 |
| `Data.Modules[].Data` | `object` | 数据 | 普通业务字段 | 可按问题需要提供 |
| `Data.Modules[].Sort` | `int` | 排序 | 普通业务字段 | 可按问题需要提供 |
| `Data.Menus` | `IList<string>` | 菜单 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsVip` | `bool` | 是否是会员 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：未发现显式 `if` 参数校验；这不代表所有参数都可省略。
- 一层业务调用：`StoreProvider.GetStoreIndexData`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store.get_store_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取商户信息 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Store/GetStoreInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreInfoResponseViewModel>>`；包装 `Task/DataResult`；Data `GetStoreInfoResponseViewModel` |
| 数据时效 | 可能包含缓存结果；不能等同数据库即时状态 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreController.cs:28` |
| C/B 对照 | crmapi.store.business_get_store_info |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1) | 服务端注入：已确认门店 | 商户id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreTypeId` | `string` | 店铺类型ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreCode` | `string` | 店铺Code | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreProvince` | `string` | 商户省 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreCity` | `string` | 商户市 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreDistrict` | `string` | 商户区 | 普通业务字段 | 可按问题需要提供 |
| `Data.Address` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Longitude` | `string` | 定位经度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Latitude` | `string` | 定位纬度 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreMobile` | `string` | 预留电话（多个按,分隔） | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.State` | `int` | state 状态，1营业，0暂停营业，-1停止运营 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayState` | `int` | 收款状态 1开启 0未开通 2关闭 | 普通业务字段 | 可按问题需要提供 |
| `Data.WorkingWeeks` | `List<int>` | 工作时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.WorkingTimes` | `List<string>` | 工作时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations` | `List<StoreVacationViewModel>` | 放假时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].Id` | `int` | ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Vacations[].BeginDate` | `string` | 放假时间开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].EndDate` | `string` | 放假时间结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsOpenIntegral` | `bool` | 是否开启积分 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade` | `CustomMadeInfoViewModel` | 定制化信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.ShopAssistantCall` | `string` | 技师（店员）称呼 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.PlaceCall` | `string` | place_call 场地称呼，预约使用 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.PrivateLessonsTitle` | `string` | private_lessons_title 私教课标题，预约使用 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.ClassesLessonsTitle` | `string` | 班课标题，预约使用 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.BackgroundImage` | `string` | 背景图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.IsShowCarSearch` | `bool` | 是否显示汽车搜索 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.IsPerformance` | `bool` | 是否开启了绩效功能 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.AreaSimple` | `string` | 省份简称 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.AllianceType` | `int` | 联盟类型：0默认联盟。1城市联盟（泰州） | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.CurrencyName` | `string` | 货币名称 元 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.CurrencyUnit` | `string` | 货币符号 ￥$ | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.IsOfficialPay` | `bool` | 是否是官方支付渠道 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.SoftVersionTag` | `int` | 软件版本标记 0老版本 1新版本 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.IsUseAudit` | `bool` | 优惠券是否需要审核 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.AppId` | `string` | APPID 店铺小程序的APPID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CustomMade.QrCodeRule` | `string` | 三方小程序二维码规则 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.IsStallMode` | `bool` | 是否档口模式 | 普通业务字段 | 可按问题需要提供 |
| `Data.CustomMade.AntShopId` | `string` | 蚂蚁门店ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CustomMade.AliPayPid` | `string` | 支付宝PID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.IsIntegralShop` | `bool` | 是否开启积分商城 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsExpress` | `bool` | 是否需要快递 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsIntegralDeduction` | `bool` | 是否参与积分抵扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.ExpressFee` | `decimal` | 快递费用 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsPayByCard` | `bool` | 是否允许顾客自主核销 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsConfirmPass` | `bool` | 会员消费是否需要输入密码 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsConfirmPhoto` | `bool` | 是否在会员消费时验证照片 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsStallMode` | `bool` | 是否是档口模式 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsFreeVersion` | `bool` | 是否免费版本 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsFood` | `bool` | 是否开通了点单 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodMode` | `int` | 点单模式 0一人一单 1多人一单 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsFoodDelay` | `bool` | 是否开启延迟取餐 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsDistribution` | `bool` | 是否打开分销 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsExtend` | `bool` | 是否开通了推广 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsCommission` | `bool` | 佣金开关 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsCommissionConsume` | `bool` | 佣金消费开关 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsExpired` | `bool` | 服务是否过期 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsCommissionCash` | `bool` | 佣金提现开关 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsMultipleTable` | `bool` | 是否是多码 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsEatHere` | `bool` | 是否是堂食 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsTakeOut` | `bool` | 是否是外卖 | 普通业务字段 | 可按问题需要提供 |
| `Data.SendOutRange` | `decimal` | 配送范围 | 普通业务字段 | 可按问题需要提供 |
| `Data.SendOutStartTime` | `string` | 配送开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.SendOutEndTime` | `string` | 配送结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.SendOutPrice` | `decimal` | 配送费用 | 普通业务字段 | 可按问题需要提供 |
| `Data.StartPrice` | `decimal` | 起送金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsTransfer` | `bool` | 是否允许转让卡余额 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsFreeShipping` | `bool` | 是否包邮 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsHideVipPrice` | `bool` | 是否隐藏会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.RegisterMethod` | `int` | 1.先填资料 2.后填资料 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsUserImgOrNick` | `bool` | 是否需要获取用户头像昵称 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsPromotionCodeVisable` | `bool` | 推广码是否可见 0 不可见 ； 1 可见 ; | 普通业务字段 | 可按问题需要提供 |
| `Data.IsPromotBoxVisable` | `bool` | 分佣弹框是否提示 1提示 ； 0 不提示 ； | 普通业务字段 | 可按问题需要提供 |
| `Data.IsMeTake` | `bool` | 是否自提 | 普通业务字段 | 可按问题需要提供 |
| `Data.CanSelectFinishTime` | `bool` | 可选送达时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.ExceptFinishMinute` | `int` | 期望送达时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsShowPay` | `bool` | is_show_pay 是否展示支付按钮 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsRefundProtection` | `bool` | 是否开启退卡保护 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsSignAgreement` | `bool` | 是否需要签署协议 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting` | `ReservationSetingViewModel` | 预约设置 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.Id` | `int` | 主键ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationSeting.IsSelectStaff` | `bool` | 是否可选技师 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsSelectItem` | `bool` | 是否可选项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsVip` | `bool` | 是否可选项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.CardPayOrder` | `int` | 卡支付顺序，0预约时支付 1签到时支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.SignInSet` | `int` | sign_in_set 签到设置 1开课后自动签到 2下课后自动签到 3下课后N分钟自动签到 11老师点名签到 12扫码签到 13签字签到 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.SignInMinutes` | `int` | sign_in_minutes 签到时间分钟 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupCardPayOrder` | `int` | 卡支付顺序，0预约时支付 1签到时支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupSignInSet` | `int` | 签到设置 1开课后自动签到 2下课后自动签到 3下课后N分钟自动签到 11老师点名签到 12扫码签到 13签字签到 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupSignInMinutes` | `int` | sign_in_minutes 签到时间分钟 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ClassCardPayOrder` | `int` | 卡支付顺序，0预约时支付 1签到时支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ClassSignInSet` | `int` | 签到设置 1开课后自动签到 2下课后自动签到 3下课后N分钟自动签到 11老师点名签到 12扫码签到 13签字签到 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ClassSignInMinutes` | `int` | sign_in_minutes 签到时间分钟 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsSelectMoreItem` | `bool` | 是否可选多个项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsOpenTimeConflict` | `bool` | 是否开启冲突时间过滤 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.TimeConflictSeting` | `int` | 时间冲突设置 0固定间隔，1按项目时长 与选择开启项目联动 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.FixedTime` | `int` | 固定时间间隔 分钟数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsClientWechatNotice` | `bool` | 预约成功顾客微信通知 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsClientSmsNotice` | `bool` | 预约成功顾客短信通知 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsAdvanceStaffWechatNotice` | `bool` | 提前技师微信通知 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsAdvanceStaffSmsNotice` | `bool` | 提前技师短信通知 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.AdvanceStaffMinute` | `int` | 技师提前通知分钟数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationNum` | `int` | 每位顾客当天累计的可预约场次 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsCancel` | `bool` | 是否可以取消预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.CancelMinute` | `int` | 开始前多少分钟可取消0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationMinute` | `int` | 顾客提前多少分钟可约0不限 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.TimeInterval` | `int` | 预约时间间隔 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ServiceIntervals` | `int` | service_intervals 两次服务间隔（分钟 0无间隔） | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.MissAppointmentPenalty` | `int` | miss_appointment_ penalty 爽约处罚 0未开启 1每月 2每年 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.MissAppointmentSum` | `int` | miss_appointment_sum 爽约次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.MissAppointmentPenaltyValue` | `int` | miss_appointment_ penalty_value 处罚内容（目前支持处罚时限卡有效期。计次卡、储值卡默认处罚最后一次爽约的预约项） | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.MissAppointmentBlackDays` | `int` | miss_appointment_black_days 私教爽约处罚黑名单天数（0不处罚） | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.MissAppointmentIsCard` | `bool` | miss_appointment_is_card 私教是否开启爽约用卡惩罚 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationPeopleNum` | `int` | reservation_people_num 私教课可预约人数，0不限制人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsGroupLessonConflict` | `bool` | is_group_lesson_conflict 私教课教练 是否与团课授课时间冲突 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsOnlyStaff` | `bool` | is_only_staff 私教是否只能约指定教练 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationDay` | `int` | reservation_day 提前N天可约 (-1不限制,0当天) | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.LessonShowMaxDay` | `int` | lesson_show_max_day 私教显示排课范围xx天 0显示所有 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.LessonReservationTime` | `string` | 私教放课时间 空不限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonIsCancel` | `bool` | group_lesson_is_cancel 团课是否可以取消预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonCancelMinute` | `int` | group_lesson_cancel_minute 团课开始前多少分钟可取消（0 不限制 1440 1天） | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonPeopleAutoCancel` | `int` | group_lesson_people_auto_cancel 团课不满足最低人数自动取消分钟 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonMissAppointmentPenalty` | `int` | group_lesson_miss_appointment_ penalty 团课爽约处罚 0未开启 1每月 2每年 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonMissAppointmentSum` | `int` | group_lesson_miss_appointment_sum 团课爽约次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonMissAppointmentPenaltyValue` | `int` | group_lesson_miss_appointment_ penalty_value 团课处罚内容（目前支持处罚时限卡有效期。计次卡、储值卡默认处罚最后一次爽约的预约项） | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonMissAppointmentBlackDays` | `int` | group_lesson_miss_appointment_black_days 团课爽约处罚黑名单天数（0不处罚） | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonMissAppointmentIsCard` | `bool` | group_lesson_miss_appointment_is_card 团课是否开启爽约用卡惩罚 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonIsReserve` | `bool` | group_lesson_is_reserve 团课是否可以候补 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsShowAvatar` | `bool` | is_show_avatar 是否显示头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReservationSeting.IsShowPeopleNum` | `bool` | is_show_people_num 是否显示预约人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsShowPeopleList` | `bool` | is_show_people_list 是否显示预约列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsShowUnfilledQuota` | `bool` | is_show_unfilled_quota 是否显示剩余可约名额 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonReservationDay` | `int` | group_lesson_reservation_day 团课提前N天可约 (-1不限制,0当天) | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonShowMaxDay` | `int` | group_lesson_show_max_day 显示排课范围xx天 0显示所有 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonReservationTime` | `string` | 团课放课时间 空不限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.CancelCycle` | `int` | 0天 1周 2月 当N | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.CancelSum` | `int` | 取消N次 0不限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.CancelAppointmentDays` | `int` | N天不允许预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsPrivateLessons` | `bool` | 是否开启私教 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.IsGroupLessons` | `bool` | 是否开启团课 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.PrivateLessonsTitle` | `string` | 私教标题 默认空 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonsTitle` | `string` | 团课标题，默认空 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.GroupLessonReservationMinute` | `int` | 团课顾客提前多少分钟可约（-1不限制） | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationTimes` | `List<StoreReservationTimeSetingViewModel>` | 预约时间段集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationTimes[].Id` | `int` | 时间端Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationSeting.ReservationTimes[].ReservationTime` | `string` | 预约时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationTimes[].ReservationTimeEnd` | `string` | 预约时间段 结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationTimes[].IsReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationTimes[].IsOccupy` | `bool` | 时间被占用 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationSeting.ReservationTimes[].SurplusCount` | `int` | 剩余可预约人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting` | `StoreFoodSetingViewModel` | 点单设置 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.Id` | `int` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodSeting.StoreId` | `int` | store_id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodSeting.FoodTitle` | `string` | food_title 点餐标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsOpen` | `bool` | is_open 点单开关；0-关，1-开 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.FoodMode` | `int` | 点餐模式，0 一人一餐 ，1多人一餐 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsMeTake` | `bool` | is_me_take 自取开关；0-关，1-开 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.TakeMakeTime` | `int` | take_make_time 自提配货冗余时长 分钟 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsAutomaticMeal` | `bool` | is_automatic_meal 出餐设置；0-关，1-开 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsTable` | `bool` | is_table 餐台设置；1-多餐台 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsEatHere` | `bool` | is_eat_here 是否是堂食 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsTakeOut` | `bool` | is_take_out 是否是外卖 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.SendOutRange` | `decimal` | send_out_range 配送范围 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.SendOutStartTime` | `string` | send_out_start_time 配送开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.SendOutEndTime` | `string` | send_out_end_time 配送结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.SendOutPrice` | `decimal` | send_out_price 配送费用 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.StartPrice` | `decimal` | start_price 起送金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsSubscribe` | `bool` | 扫码点餐是否需要订阅公众号 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.ExceptFinishMinute` | `int` | 期望送达时间（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.CanSelectFinishTime` | `bool` | 可选送达时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsSetScene` | `bool` | 是否设置过点餐场景 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsFoodDelay` | `bool` | 是否开启延迟取餐 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.IsMultipleTable` | `bool` | 是否是多码 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodSeting.ShareImg` | `string` | 分享图 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting` | `StoreShopSetingViewModel` | 商城设置 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.Id` | `int` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ShopSeting.ShopTitle` | `string` | 商城名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsEnableshop` | `bool` | is_enableshop 门店是否启用商城1启用 0不启用 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsIntegralShop` | `bool` | 是否开启积分商城 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsIntegralDeduction` | `bool` | 是否参与积分抵扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsTake` | `bool` | 是否是开启配送 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.ExpressType` | `int` | 配送类型，0无需邮寄 1快递，2短途配送 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsExpress` | `bool` | 是否启用快递 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.ExpressFee` | `decimal` | express_fee 快递费用 ExpressType=1 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.Discount` | `decimal` | discount 门店折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsFreeShipping` | `bool` | 是否包邮 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsHideVipPrice` | `bool` | 是否隐藏会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.ShopStyle` | `int` | 商城展现样式0 上下，1左右 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsMeTake` | `bool` | is_me_take 自取开关；0-关，1-开 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.TakeMakeTime` | `int` | take_make_time 自提配货冗余时长 分钟 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.SendOutRange` | `decimal` | send_out_range 配送范围 ExpressType=2 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.SendOutStartTime` | `string` | send_out_start_time 配送开始时间 ExpressType=2 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.SendOutEndTime` | `string` | send_out_end_time 配送结束时间 ExpressType=2 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.SendOutPrice` | `decimal` | send_out_price 配送费用 ExpressType=2 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.StartPrice` | `decimal` | start_price 起送金额 ExpressType=2 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsCanSelectFinishTime` | `bool` | 可选送达时间 ExpressType=2 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.ExceptFinishMinute` | `int` | 期望送达时间（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsOpenLnventoryWarning` | `bool` | 是否开启库存预警 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.LnventoryQuantity` | `int` | 预警库存数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsLnventoryWechatNotice` | `bool` | 是否开启库存预警微信提醒 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsLnventorySmsNotice` | `bool` | 是否开启库存预警短信提醒 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.ShareImg` | `string` | 分享图 | 普通业务字段 | 可按问题需要提供 |
| `Data.ShopSeting.IsHideSaleSum` | `bool` | 是否隐藏销售数据 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting` | `StoreDistributionSetingViewModel` | 分销设置 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.Id` | `int` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.DistributionSeting.IsExtend` | `bool` | is_extend 是否开通了推广 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsPromotionCodeVisable` | `bool` | 推广码是否可见 false 不可见 ture 可见 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsPromotBoxVisable` | `bool` | 分佣弹框是否提示 true 提示 false 不提示 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.CommissionValidDate` | `int` | 分佣有效天数 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.PromotionType` | `int` | 推广类型 1 全员推广 ； 2指定推广； | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.CommissionType` | `int` | 分佣类型 0单次分佣 ； 1 永久分佣 ； 2限时分佣 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.ExtendContent` | `string` | extend_content 推广说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsBuyCommission` | `bool` | is_buy_commission 购卡分佣开关 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsConsumeCommission` | `bool` | is_consume_commission 消费分佣开关 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.CommissionStartMoney` | `decimal` | commission_start_money 分佣起始金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsCommission` | `bool` | 佣金开关(佣金查看) | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsCommissionConsume` | `bool` | 佣金消费开关 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsCommissionCash` | `bool` | is_commission_cash 佣金提现开关 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsForeverCommission` | `bool` | 永久分佣开关（分佣类型 0单次分佣 ； 1 永久分佣 ； 2限时分佣 ； ） | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.CommissionMinCashMoney` | `decimal` | 佣金提现最低金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.CommissionCashCount` | `int` | commission_cash_count 佣金每天提现次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.DistributionSeting.IsCommissionLook` | `bool` | 佣金是否可以查看 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1`；`resultMsg.State`；`sm != null && sm.Id > 0`；`sm.State < 0`；`sm.IsShop`；`sm.IsFood`；`sm.IsDistribution`；`sm.IsReservation`；`resultMsg.Data.WorkingWeeks != null && resultMsg.Data.WorkingWeeks.Contains(7)`
- 一层业务调用：`StoreProvider.GetStoreByIdAsync`、`PromoterProvider.GetUserIsPromoter`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreOperateTimeProvider.GetStoreOperateTime`、`StoreVacationProvider.GetStoreVacation`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 310`；`固定提示：参数不正确`；`固定提示：店铺被封禁！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store.get_store_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取商户列表 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Store/GetStoreList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreListResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreListResponseModel` |
| 数据时效 | 可能包含缓存结果；不能等同数据库即时状态 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreController.cs:267` |
| C/B 对照 | crmapi.store.business_get_store_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1) | 服务端注入：已确认门店 | 商户id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores` | `List<StoreInfoViewModel>` | 店铺列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].StoreId` | `int` | 店铺Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Stores[].StoreCode` | `string` | 店铺Code | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].StoreName` | `string` | 店铺名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].StoreLogo` | `string` | 店铺logo | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].StoreTypeId` | `string` | 店铺类型ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Stores[].StoreProvince` | `string` | 商户省 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].StoreCity` | `string` | 商户市 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].StoreDistrict` | `string` | 商户区 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].Address` | `string` | 店铺地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Stores[].Longitude` | `string` | 定位经度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].Latitude` | `string` | 定位纬度 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].StoreMobile` | `string` | 预留电话（多个按,分隔） | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Stores[].State` | `int` | state 状态，1营业，0暂停营业，-1停止运营 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].WorkingWeeks` | `List<int>` | 工作时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].UserType` | `int` | 用户权限 | 普通业务字段 | 可按问题需要提供 |
| `Data.Stores[].WorkingTimes` | `List<string>` | 工作时间 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1`；`resultMsg.State`；`storeModels?.Count > 0`；`sm != null && sm.Id > 0`；`stm.WorkingWeeks != null && stm.WorkingWeeks.Contains(7)`
- 一层业务调用：`StoreProvider.GetStoreListByTenant`、`StoreProvider.GetStoreByIdAsync`、`StoreOperateTimeProvider.GetStoreOperateTime`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store.get_store_vacation`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取店铺放假时间 |
| 使用时机 | 核对顾客端当前门店展示、功能开关或版本相关可见结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Store/GetStoreVacation` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreVacationResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreVacationResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreController.cs:466` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `IsMore` | `bool` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 是否更多；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsMore` | `bool` | 是否有更多 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations` | `List<StoreVacationResponseInfoModel>` | 放假列表信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].Id` | `int` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Vacations[].Remark` | `string` | 备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Vacations[].VacationMessage` | `string` | 放假公告信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].CardExtension` | `int` | 会员卡延期模式：0 不延期；1 仅期限类卡（CardType=2/3）； 2 所有符合有效期和状态条件的持卡记录。 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].CardExtensionDays` | `int` | 会员卡延期天数；独立配置，不自动等于放假起止日期的跨度。 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].BeginDate` | `string` | 开始时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].EndDate` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].IsShowIndex` | `bool` | 是否首页弹框展现 | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].IsVacation` | `bool` | 是否开启放假（未开启放假只做公告功能展示） | 普通业务字段 | 可按问题需要提供 |
| `Data.Vacations[].VacationState` | `int` | 1未开始 2已过期 3放假中 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`；`svms?.Count > 0`；`item.State == 1 && item.BeginDate < DateTime.Now`
- 一层业务调用：`StoreVacationProvider.GetStoreVacationByStoreId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store_item.get_service_cart`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取服务购物车 |
| 使用时机 | 在顾客视角中核对“获取服务购物车”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/StoreItem/GetServiceCart` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetServiceCartResponseModel>>`；包装 `Task/DataResult`；Data `GetServiceCartResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreItemController.cs:50` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Id` | `int` | 购物车ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ServiceCount` | `int` | 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalPrice` | `decimal` | 总价 | 普通业务字段 | 可按问题需要提供 |
| `Data.VipDiscount` | `decimal` | 会员折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList` | `List<ServiceCartViewModel>` | 服务列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].Id` | `int` | 购物车子项的id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ServiceList[].ItemId` | `int` | 服务的id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ServiceList[].ItemName` | `string` | 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].ItemImg` | `string` | 图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].ItemPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].ItemVipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].ItemCount` | `int` | 数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`；`resultMsg.State`
- 一层业务调用：`ServiceItemCartProvider.GetServiceCart`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store_item.get_service_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取服务列表 |
| 使用时机 | 在顾客视角中核对“获取服务列表”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/StoreItem/GetServiceList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<List<GetServiceListToCResponseModel>>>`；包装 `Task/DataResult`；Data `List<GetServiceListToCResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreItemController.cs:20` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId <= 0) | 服务端注入：已确认门店 | 店铺id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ClassId` | `int` | 分类id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].ClassName` | `string` | 分类名称 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Count` | `int` | 个数 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList` | `List<ServiceListViewModel>` | 服务列表 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].Id` | `int` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].ServiceList[].ItemName` | `string` | 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].ItemImg` | `string` | 图片 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].SellNum` | `int` | 销量 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].ItemPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].ItemVipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].State` | `int` | 状态；0-下架，1-上架 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].OnOffState` | `int` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ServiceList[].VipDisCount` | `decimal` | 源码属性注释缺失 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0`；`resultMsg.State`
- 一层业务调用：`StoreServiceItemProvider.GetServiceListToC`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store_item.get_service_order_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取订单的详情 |
| 使用时机 | 顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/StoreItem/GetServiceOrderInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetServiceOrderInfoResponseModel>>`；包装 `Task/DataResult`；Data `GetServiceOrderInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StoreItemController.cs:253` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ServiceOrderId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 服务订单的id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreName` | `string` | 店铺名 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalPrice` | `decimal` | 总金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayPrice` | `decimal` | 支付的金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayMethod` | `int` | 支付方式：0 会员卡支付、1微信支付、2支付宝支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.IntegralDeduct` | `decimal` | 积分减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardDeduct` | `decimal` | 权益卡、储值卡减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponDeduct` | `decimal` | 优惠券减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList` | `List<ServiceOrderInfoViewModel>` | 子项 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].ItemId` | `int` | 服务的id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ServiceList[].ItemName` | `string` | 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].ItemImg` | `string` | 图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].ItemPrice` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceList[].ItemCount` | `int` | 数量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`；`resultMsg.State`
- 一层业务调用：`ServiceItemCartProvider.GetServiceOrderInfo`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.store_place.get_reservation_place`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 门店 |
| 用途 | 获取预约场地 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/StorePlace/GetReservationPlace` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：StorePlaceCloseSettingProvider.GetStorePlaceCloseSettingByStoreId |
| 返回 | `Task<DataResult<GetReservationPlaceResponseModel>>`；包装 `Task/DataResult`；Data `GetReservationPlaceResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/StorePlaceController.cs:24` |
| C/B 对照 | crmapi.store_place.get_reservation_place |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.ReservationDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约时间（格式"2012-01-21"）；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationNum` | `int` | 每位顾客当天累计的可预约场次 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserReservationNum` | `int` | 用户已约次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes` | `List<StoreReservationTimeSetingViewModel>` | 预约时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].Id` | `int` | 时间端Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationTimes[].ReservationTime` | `string` | 预约时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].ReservationTimeEnd` | `string` | 预约时间段 结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].IsReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].IsOccupy` | `bool` | 时间被占用 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].SurplusCount` | `int` | 剩余可预约人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Places` | `List<StorePlaceReservationModel>` | 预约场地 | 普通业务字段 | 可按问题需要提供 |
| `Data.Places[].Id` | `int` | id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Places[].PlaceName` | `string` | 场地名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Places[].PlaceDescribe` | `string` | 场地描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Places[].ReservationNum` | `int` | 同时可预约次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Places[].ReservationTimes` | `List<PlaceTimeModel>` | 时间段(只返回关闭) | 普通业务字段 | 可按问题需要提供 |
| `Data.Places[].ReservationTimes[].Id` | `int` | 时间段Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Places[].ReservationTimes[].UserReservationNum` | `int` | 已约人次 | 普通业务字段 | 可按问题需要提供 |
| `Data.Places[].ReservationTimes[].IsReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`string.IsNullOrEmpty(model.ReservationDate)`；`model.StoreId == 15846`；`ucs.Any(x=>x.PrepaidCardId==20390 \|\| x.PrepaidCardId==20389)`；`pm?.Id>0`；`!(placeModels?.Count > 0)`；`resultMsg.State`；`resultMsg.Data.ReservationTimes?.Count > 0`；`reservationSeting.ReservationNum > 0`；`placeCloseModels?.Count > 0`；`placeModel.ReservationTimes.All(x => x.Id != placeCloseTime.Id)`；`placeReservationModels?.Count > 0`
- 一层业务调用：`StorePlaceProvider.GetStorePlaceByStoreId`、`UserCardChildProvider.GetChildCardByUid`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreReservationTimeSetingProvider.GetReservationTimeSeting`、`StoreReservationProvider.GetStoreReservationPlaceByUid`、`StorePlaceCloseSettingProvider.GetStorePlaceCloseSettingByStoreId`、`StoreReservationProvider.GetStoreReservationPlace`
- 疑似副作用：`StorePlaceCloseSettingProvider.GetStorePlaceCloseSettingByStoreId`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`状态赋值：StatusCode = 303`；`状态赋值：StatusCode = 310`；`状态赋值：StatusCode = 305`；`固定提示：参数不正确`；`固定提示：预约时间不正确`；`固定提示：没有可预约场地`；`固定提示：当日没有可预约的时间`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_course_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取课程列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetCourseList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<List<GetCourseListResponseModel>>`；包装 `DataResult`；Data `List<GetCourseListResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1053` |
| C/B 对照 | crmapi.reservation.get_course_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21”)；普通业务字段；可按问题需要提供 |
| `StaffId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 员工ID，非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].CourseId` | `int` | 课程ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].CourseName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data[].CourseType` | `int` | 授课类型；0-团课，1-私教 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Remark` | `string` | 备注，例如：（13/20）、（满） | 个人信息 | 仅在当前授权场景按最小范围提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`；`!success`；`result.State`
- 一层业务调用：`StoreReservationProvider.GetCanReservationCourseList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 401`；`状态赋值：StatusCode = 200`；`固定提示：参数错误`；`固定提示：日期格式错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_group_course_class_tag`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取团课分类信息 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetGroupCourseClassTag` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetGroupCourseClassTagResponseModel>>`；包装 `Task/DataResult`；Data `GetGroupCourseClassTagResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1220` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Tags` | `List<ReservationTagResponseModel>` | 获取团课分类 | 普通业务字段 | 可按问题需要提供 |
| `Data.Tags[].Id` | `long` | 标签id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Tags[].TagTitle` | `string` | 标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Tags[].TagSubTitle` | `string` | 子标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Tags[].IsCanDelete` | `bool` | 是否可以删除 | 普通业务字段 | 可按问题需要提供 |
| `Data.Tags[].State` | `int` | 状态 0禁用 1启用 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`；`tags?.Count > 0`
- 一层业务调用：`StoreReservationTagProvider.GetTagsByStoreId`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_group_course_list_v2`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取团课列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetGroupCourseListV2` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetGroupCourseListV2ResponseModel>>`；包装 `Task/DataResult`；Data `GetGroupCourseListV2ResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1390` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate) \\|\\| !StringOperate.IsDate(model.EndDate)) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate) \\|\\| !StringOperate.IsDate(model.EndDate)) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 00:00”)；普通业务字段；可按问题需要提供 |
| `BeginDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate) \\|\\| !StringOperate.IsDate(model.EndDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 00:00”)；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate) \\|\\| !StringOperate.IsDate(model.EndDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 23:59”)；普通业务字段；可按问题需要提供 |
| `StaffId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 员工ID，非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 课目Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ClassTagId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 分类id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 课目类型 0团课 2班课；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Uid` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | 商家ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData` | `List<CourseListV2ResponseModel>` | 课程列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].CourseId` | `int` | 课程ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].CourseType` | `int` | 授课类型；0-团课，1-私教 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseImage` | `string` | 课程图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ImageStyle` | `int` | 图片样式 0明亮 1暗黑 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseDescribe` | `string` | 课程描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseStar` | `int` | 难度星级1-10 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseColor` | `string` | 颜色 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].BeginTime` | `string` | 开课时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].EndTime` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].TeachMin` | `int` | 授课时长（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePeopleCount` | `int` | 最大授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].MinPeople` | `int` | 最小授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].IsReserve` | `bool` | 是否可以候补 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ReservationCount` | `int` | 已预约的人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].State` | `int` | 课程状态；状态：0未开课，1完课，2取消 3（取消）人数不足 10停课 11约满 12未到可约时间 13 已过可约时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].Staffs` | `List<CourseStaffViewModel>` | 教练信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].Staffs[].Id` | `long` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].Staffs[].UserName` | `string` | 教练名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.LessonsData[].Staffs[].UserImage` | `string` | 教练图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ClassTag` | `StoreReservationTagViewModel` | 分类 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ClassTag.Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].ClassTag.TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].LessonsPeoples` | `List<LessonsPeopleViewModel>` | 预约人员信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].LessonsPeoples[].UserName` | `string` | 预约者名称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.LessonsData[].LessonsPeoples[].UserImg` | `string` | 预约者头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.LessonsData[].CoursePlace` | `CoursePlaceViewModel` | 教室 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePlace.Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].CoursePlace.PlaceName` | `string` | 场地名 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseTools` | `List<StoreReservationTagViewModel>` | 课程工具 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseTools[].Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].CourseTools[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].FirstReservationTime` | `string` | 最早可约时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].IsCanReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].IsReservation` | `bool` | 是否已约 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ReservationId` | `long` | 预约id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].CoursePrice` | `StoreCoursePriceViewModel` | 单次付费信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.State` | `int` | 状态；0-禁用，1-启用 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].IsVacation` | `bool` | 是否请假 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ReservationState` | `int` | 预约状态 -2未到店(旷课)，-1已取消，0未确认，1以确定，2到店（签到） 3上课中 5完课 10候补 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| !StringOperate.IsDate(model.BeginDate) \|\| !StringOperate.IsDate(model.EndDate)`；`blackModel?.Id > 0`；`resultMsg.State`；`lms?.Count > 0`
- 一层业务调用：`StoreUserBlackListProvider.GetValidBlackList`、`StoreProvider.GetStoreDateTime`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreLessonsProvider.GetStoreLessonsTime`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_group_course_list_v3`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取团课列表分页 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetGroupCourseListV3` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<PageData<CourseListV2ResponseModel>>>`；包装 `Task/DataResult`；Data `PageData<CourseListV2ResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1446` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate)) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate)) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 00:00”)；普通业务字段；可按问题需要提供 |
| `BeginDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 00:00”)；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 23:59”)；普通业务字段；可按问题需要提供 |
| `StaffId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 员工ID，非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 课目Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ClassTagId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 分类id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 课目类型 0团课 2班课；普通业务字段；可按问题需要提供 |
| `PageSize` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageSize <= 0) | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageIndex <= 0) | AI 可在服务端上限内选择 | 请求页数；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<CourseListV2ResponseModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].CourseId` | `int` | 课程ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].CourseType` | `int` | 授课类型；0-团课，1-私教 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseImage` | `string` | 课程图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ImageStyle` | `int` | 图片样式 0明亮 1暗黑 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseDescribe` | `string` | 课程描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseStar` | `int` | 难度星级1-10 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseColor` | `string` | 颜色 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].BeginTime` | `string` | 开课时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].EndTime` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].TeachMin` | `int` | 授课时长（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePeopleCount` | `int` | 最大授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].MinPeople` | `int` | 最小授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsReserve` | `bool` | 是否可以候补 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReservationCount` | `int` | 已预约的人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].State` | `int` | 课程状态；状态：0未开课，1完课，2取消 3（取消）人数不足 10停课 11约满 12未到可约时间 13 已过可约时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Staffs` | `List<CourseStaffViewModel>` | 教练信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Staffs[].Id` | `long` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Staffs[].UserName` | `string` | 教练名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].Staffs[].UserImage` | `string` | 教练图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ClassTag` | `StoreReservationTagViewModel` | 分类 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ClassTag.Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ClassTag.TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].LessonsPeoples` | `List<LessonsPeopleViewModel>` | 预约人员信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].LessonsPeoples[].UserName` | `string` | 预约者名称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].LessonsPeoples[].UserImg` | `string` | 预约者头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].CoursePlace` | `CoursePlaceViewModel` | 教室 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePlace.Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].CoursePlace.PlaceName` | `string` | 场地名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseTools` | `List<StoreReservationTagViewModel>` | 课程工具 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CourseTools[].Id` | `long` | Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].CourseTools[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FirstReservationTime` | `string` | 最早可约时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsCanReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsReservation` | `bool` | 是否已约 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReservationId` | `long` | 预约id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].CoursePrice` | `StoreCoursePriceViewModel` | 单次付费信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePrice.IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePrice.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePrice.VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePrice.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CoursePrice.State` | `int` | 状态；0-禁用，1-启用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].IsVacation` | `bool` | 是否请假 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReservationState` | `int` | 预约状态 -2未到店(旷课)，-1已取消，0未确认，1以确定，2到店（签到） 3上课中 5完课 10候补 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| !StringOperate.IsDate(model.BeginDate)`；`model.PageSize <= 0`；`model.PageIndex <= 0`；`resultMsg.State`；`blackModel?.Id > 0`
- 一层业务调用：`StoreUserBlackListProvider.GetValidBlackList`、`StoreProvider.GetStoreDateTime`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreLessonsProvider.GetStoreLessonsTime`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 302`；`状态赋值：StatusCode = 303`；`固定提示：参数格式错误！`；`固定提示：请求数据数量不正确`；`固定提示：页码不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_group_course_people_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取课程预约人员列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetGroupCoursePeopleList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetGroupCoursePeopleListResponseModel>>`；包装 `Task/DataResult`；Data `GetGroupCoursePeopleListResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:2029` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.LessonsId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.LessonsId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `LessonsId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.LessonsId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Uid` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | 商家ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsPeoples` | `List<LessonsPeopleViewModel>` | 预约人员信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsPeoples[].UserName` | `string` | 预约者名称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.LessonsPeoples[].UserImg` | `string` | 预约者头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| model.LessonsId < 1`；`blackModel?.Id > 0`；`resultMsg.State`；`rms?.Count > 0`；`rm.CardId > 0`；`rm.Uid > 0`
- 一层业务调用：`StoreUserBlackListProvider.GetValidBlackList`、`StoreReservationProvider.GetStoreReservationElementsByCondition`、`UserCardProvider.BusinessGetUserCardBasisInfo`、`UsersInfoProvider.UsersInfoGetByUid`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_group_course_week_list_v2`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取团课周课列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetGroupCourseWeekListV2` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetGroupCourseWeekListV2ResponseModel>>`；包装 `Task/DataResult`；Data `GetGroupCourseWeekListV2ResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1782` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate) \\|\\| !StringOperate.IsDate(model.EndDate)) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate) \\|\\| !StringOperate.IsDate(model.EndDate)) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 00:00”)；普通业务字段；可按问题需要提供 |
| `BeginDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate) \\|\\| !StringOperate.IsDate(model.EndDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 00:00”)；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| !StringOperate.IsDate(model.BeginDate) \\|\\| !StringOperate.IsDate(model.EndDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21 23:59”)；普通业务字段；可按问题需要提供 |
| `StaffId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 员工ID，非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 课目Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ClassTagId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 分类id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 课目类型 0团课 2班课；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Uid` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | 商家ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData` | `List<CourseWeekListV2ResponseModel>` | 课程列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].CourseId` | `int` | 课程ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].CourseName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseStar` | `int` | 难度星级1-10 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CourseColor` | `string` | 颜色 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].BeginTime` | `string` | 开课时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].EndTime` | `string` | 结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].TeachMin` | `int` | 授课时长（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePeopleCount` | `int` | 最大授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].MinPeople` | `int` | 最小授课人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].IsReserve` | `bool` | 是否可以候补 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ReservationCount` | `int` | 已预约的人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].State` | `int` | 课程状态；状态：0未开课，1完课，2取消 3（取消）人数不足 10停课 11约满 12未到可约时间 13提前不可约 100放假停课 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].FirstReservationTime` | `string` | 最早可约时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].IsCanReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].IsReservation` | `bool` | 是否已约 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ReservationId` | `long` | 预约id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessonsData[].CoursePrice` | `StoreCoursePriceViewModel` | 单次付费信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].CoursePrice.State` | `int` | 状态；0-禁用，1-启用 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].IsVacation` | `bool` | 是否请假 | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonsData[].ReservationState` | `int` | 预约状态 -2未到店(旷课)，-1已取消，0未确认，1以确定，2到店（签到） 3上课中 5完课 10候补 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| !StringOperate.IsDate(model.BeginDate) \|\| !StringOperate.IsDate(model.EndDate)`；`blackModel?.Id > 0`；`resultMsg.State`；`srsm.GroupLessonShowMaxDay > -1`；`DateTime.Parse(model.EndDate).Date > storeTime.AddDays(srsm.GroupLessonShowMaxDay)`；`lms?.Count > 0`；`srsm.GroupLessonReservationDay > -1`；`storeVacations?.Count > 0 && storeVacations.Any(x => x.BeginDate < lessonsItem.EndTime && x.EndDate > lessonsItem.BeginTime)`；`storeVacationSet.GroupLessonState != 1 && lessonsItem.CourseType == 0`；`storeVacationSet.PrivateLessonState != 1 && lessonsItem.CourseType == 1`；`newData.State != 100`；`(lessonsItem.BeginTime.Date > canReservationTime.Date) \|\| (lessonsItem.BeginTime.Date == canReservationTime.Date && !string.IsNullOrEmpty(srsm.GroupLessonReservationTime) && storeTime.AddDays(srsm.GroupLessonReservationDay) < DateTime.Parse( canReservationT…`
- 一层业务调用：`StoreUserBlackListProvider.GetValidBlackList`、`StoreProvider.GetStoreDateTime`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreLessonsProvider.GetStoreLessonsTime`、`TenantUserProvider.GetTenantUserByStoreId`、`StoreVacationSetingProvider.GetStoreVacationSetingByStoreId`、`StoreVacationProvider.GetStoreVacationElementsByCondition`、`StoreReservationProvider.GetStoreReservationElementsByCondition`、`StoreLessonsStaffProvider.GetStoreLessonsStaffElementsByCondition`、`StaffVacationSetingProvider.GetStaffVacationSetingElementByStaffId`、`StaffVacationProvider.GetStaffVacationByVacationDate`、`UserVacationProvider.GetUserVacationElementsByCondition`、`StoreCoursePriceProvider.GetStoreCoursePriceFirstOrDefaultByCondition`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`固定提示：参数格式错误！`；`固定提示：商家暂未开放该日期的课程！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_lessons_reservation_calender_v2`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取课程日历可预约时间V2 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetLessonsReservationCalenderV2` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetReservationCalenderV2ResponseModel>>`；包装 `Task/DataResult`；Data `GetReservationCalenderV2ResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1271` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `BeginDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 开始时间；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 结束时间；普通业务字段；可按问题需要提供 |
| `ClassTagId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 分类id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseType` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 课程类型 0团课 1私教；普通业务字段；可按问题需要提供 |
| `CourseId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程ID 非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StaffId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 员工ID，非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.VacationDates` | `List<VacationDateViewModel>` | 店铺可预约日期(格式 MM-dd) | 普通业务字段 | 可按问题需要提供 |
| `Data.VacationDates[].Date` | `string` | 日期 yyyy-MM-dd | 普通业务字段 | 可按问题需要提供 |
| `Data.VacationDates[].IsReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.VacationDates[].DateState` | `int` | 日期状态 1休息 2放假 3员工休息 4请假 5无课程 12 未到预约四件 | 普通业务字段 | 可按问题需要提供 |
| `Data.VacationDates[].DateMessage` | `string` | 放假信息 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`
- 一层业务调用：`StoreReservationProvider.GetReservationCalenderV2`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_miss_appointment_penalty_explain`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取旷课爽约惩罚说明 |
| 使用时机 | 在顾客视角中核对“获取旷课爽约惩罚说明”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetMissAppointmentPenaltyExplain` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetMissAppointmentPenaltyExplainResponseModel>>`；包装 `Task/DataResult`；Data `GetMissAppointmentPenaltyExplainResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1163` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule` | `MissAppointmentPenaltyRuleResponseModel` | 私教惩罚说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule.RuleName` | `string` | 规则名称（私教/团课） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule.IsEnabled` | `bool` | 是否启用惩罚 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule.PenaltyCycle` | `int` | 爽约处罚周期 0未开启 1每月 2每年 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule.PenaltySum` | `int` | 爽约处罚次数阈值 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule.PenaltyValue` | `int` | 处罚内容值（系统配置原值） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule.IsCardPenalty` | `bool` | 是否启用用卡惩罚 | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule.BlackDays` | `int` | 黑名单天数（0不处罚） | 普通业务字段 | 可按问题需要提供 |
| `Data.PrivateLessonsRule.Detail` | `string` | 详细说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule` | `MissAppointmentPenaltyRuleResponseModel` | 团课惩罚说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule.RuleName` | `string` | 规则名称（私教/团课） | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule.IsEnabled` | `bool` | 是否启用惩罚 | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule.PenaltyCycle` | `int` | 爽约处罚周期 0未开启 1每月 2每年 | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule.PenaltySum` | `int` | 爽约处罚次数阈值 | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule.PenaltyValue` | `int` | 处罚内容值（系统配置原值） | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule.IsCardPenalty` | `bool` | 是否启用用卡惩罚 | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule.BlackDays` | `int` | 黑名单天数（0不处罚） | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupLessonsRule.Detail` | `string` | 详细说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Summary` | `string` | 汇总说明 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1`；`set?.Id <= 0`
- 一层业务调用：`StoreReservationSetingProvider.GetReservationSeting`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`固定提示：参数格式错误！`；`固定提示：未找到门店预约设置`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_private_lessons_reservation_time_seting`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取私教预约时间段 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetPrivateLessonsReservationTimeSeting` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：StaffPrivateLessonSetProvider.GetStaffPrivateLessonSet |
| 返回 | `Task<DataResult<GetPrivateLessonsReservationTimeSetingResponseModel>>`；包装 `Task/DataResult`；Data `GetPrivateLessonsReservationTimeSetingResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:2107` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `CourseId` | `int` | 参与组合校验 | 绑定=ApiController推断；if(setModel.IsSelectCourse && model.CourseId <= 0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程ID 非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StaffId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 技师Id 团课非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `LessonsId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程id(修改课程预约时间传入)；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约时间（格式"2012-01-21"）；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes` | `List<StoreReservationTimeSetingViewModel>` | 预约时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].Id` | `int` | 时间端Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationTimes[].ReservationTime` | `string` | 预约时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].ReservationTimeEnd` | `string` | 预约时间段 结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].IsReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].IsOccupy` | `bool` | 时间被占用 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].SurplusCount` | `int` | 剩余可预约人数 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`；`setModel.IsSelectCourse && model.CourseId <= 0`；`srsm.LessonShowMaxDay > -1 && DateTime.Parse(model.ReservationDate).Date > storeTime.Date.AddDays(srsm.LessonShowMaxDay)`；`srsm.ReservationDay > -1`；`(rd.Date> canReservationTime.Date) \|\| (rd.Date == canReservationTime.Date && !string.IsNullOrEmpty(srsm.LessonReservationTime) && storeTime.AddDays(srsm.ReservationDay)< DateTime.Parse(canReservationTime.ToString($"yyyy-MM-dd {srsm.LessonReservationTime}")))`
- 一层业务调用：`StoreProvider.GetStoreDateTime`、`StaffPrivateLessonSetProvider.GetStaffPrivateLessonSet`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreReservationTimeSetingProvider.GetReservationTimeSetingV2`
- 疑似副作用：`StaffPrivateLessonSetProvider.GetStaffPrivateLessonSet`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`状态赋值：StatusCode = 303`；`固定提示：参数不正确`；`固定提示：课程ID不能为空`；`固定提示：商家暂未开放该日期的课程！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_private_staff`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取私教教练 |
| 使用时机 | 商家核对员工、教练、权限或门店关系；不得把其他员工的个人信息无条件交给模型。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetPrivateStaff` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetPrivateStaffResponseModel>>`；包装 `Task/DataResult`；Data `GetPrivateStaffResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1311` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0 \\|\\| !StringOperate.IsDate(model.ReservationDate)) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0 \\|\\| !StringOperate.IsDate(model.ReservationDate)) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(model.StoreId <= 0 \\|\\| model.Uid <= 0 \\|\\| !StringOperate.IsDate(model.ReservationDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21”)；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Uid` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | 商家ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs` | `List<PrivateStaffViewModel>` | 课程列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].Id` | `long` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].UserName` | `string` | 教练名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Staffs[].UserImage` | `string` | 教练图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].IsReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].IsHide` | `bool` | 是否隐藏 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].ReservationState` | `int` | 状态 1休息 2放假 3员工休息 4请假 5无课程 12未到可约时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].FirstReservationTime` | `string` | 最早可约时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].IsSelectCourse` | `bool` | 预约是否可选课目 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffTags` | `List<ReservationTagViewModel>` | 教练标签 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffTags[].Id` | `long` | 标签id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].StaffTags[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].SpecialiseTags` | `List<ReservationTagViewModel>` | 擅长标签 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].SpecialiseTags[].Id` | `long` | 标签id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].SpecialiseTags[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffExperience` | `string` | 店员经历 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].Reservations` | `List<PrivateUserReservationViewModel>` | 已约时段 如有 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].Reservations[].ReservationId` | `long` | 预约id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].Reservations[].ReservationTime` | `string` | 预约时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].Reservations[].ReservationState` | `int` | 预约状态 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses` | `List<StaffCourseViewModel>` | 关联私教课目 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].Id` | `int` | 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].StaffCourses[].CourseId` | `int` | 课目id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].StaffCourses[].CourseName` | `string` | 课程名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CourseImage` | `string` | 课程图片id | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CourseTime` | `int` | 授课时长（分钟） | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CourseDescribe` | `string` | 课程描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CardCount` | `int` | 支持卡的数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CoursePrice` | `StoreCoursePriceViewModel` | 单次付费信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CoursePrice.IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CoursePrice.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CoursePrice.VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CoursePrice.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].CoursePrice.State` | `int` | 状态；0-禁用，1-启用 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffCourses[].State` | `int` | 状态；0-未开放，1-已开放 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].CoursePrice` | `StoreCoursePriceViewModel` | 单次付费信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].CoursePrice.IsCardDiscount` | `bool` | 是否参与卡折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].CoursePrice.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].CoursePrice.VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].CoursePrice.DiscountPrice` | `decimal` | 折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].CoursePrice.State` | `int` | 状态；0-禁用，1-启用 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0 \|\| !StringOperate.IsDate(model.ReservationDate)`；`blackModel?.Id > 0`；`result.State`；`srsm.LessonShowMaxDay > -1 && DateTime.Parse(model.ReservationDate).Date > storeTime.Date.AddDays(srsm.LessonShowMaxDay)`；`staffs?.Count > 0`；`srsm.ReservationDay > -1`；`(rd.Date> canReservationTime.Date) \|\| (rd.Date == canReservationTime.Date && !string.IsNullOrEmpty(srsm.LessonReservationTime) && storeTime.AddDays(srsm.ReservationDay)< DateTime.Parse(canReservationTime.ToString($"yyyy-MM-dd {srsm.LessonReservationTime}")))`
- 一层业务调用：`StoreUserBlackListProvider.GetValidBlackList`、`StoreProvider.GetStoreDateTime`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreReservationProvider.GetWorkStaffListV2`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 401`；`状态赋值：StatusCode = 302`；`固定提示：参数错误`；`固定提示：商家暂未开放该日期的课程！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_reservation_by_id`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取已约列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetReservationById` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetReservationByIdResponseModel>>`；包装 `Task/DataResult`；Data `GetReservationByIdResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:73` |
| C/B 对照 | crmapi.reservation.business_get_reservation_by_id |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.ReservationId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.ReservationId < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1 \\|\\| model.ReservationId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 预约Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationId` | `int` | 预约Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationDate` | `string` | 预约时间（日期部分 09-23） | 普通业务字段 | 可按问题需要提供 |
| `Data.StaffId` | `int` | 技师Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationTime` | `string` | 预约时间（时间部分 10:00） | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimeEnd` | `string` | 预约结束时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.ItemIds` | `List<int>` | 项目Id(非必填) | 普通业务字段 | 可按问题需要提供 |
| `Data.PlaceId` | `int` | 场地Id(非必填) | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Remark` | `string` | 客户留言 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.IsCancel` | `bool` | 是否可以取消预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 -2未到店，-1已取消，0未确认，1以确定，2已到店 | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseType` | `int` | 课程类型（如果是课程得话，则有返回) | 普通业务字段 | 可按问题需要提供 |
| `Data.CourseId` | `int` | 课程ID（如果是课程得话，则有返回） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.LessionId` | `int` | 课ID（如果是课程得话，则有返回） | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PeopleCount` | `int` | 人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos` | `List<GetReservationInfosModel>` | 预约信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].ControlName` | `string` | 控件名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].ControlValue` | `string` | 控件值 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReservationInfos[].IsShow` | `bool` | 是否对C端显示 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].IsMust` | `int` | 是否必填项 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].ControlType` | `string` | 控件类型 input,radio,select.... | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].ControlInstructions` | `string` | 控件说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].Items` | `List<GetReservationItemControlsListViewModel>` | 选项列表 控件类型 为 radio select 不为空 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].Items[].Id` | `int` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationInfos[].Items[].CommonReservationControlsId` | `int` | cid 控件id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationInfos[].Items[].ItemValue` | `string` | item_value 值 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].Items[].ItemName` | `string` | item_name 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationInfos[].Items[].IsDefault` | `int` | is_default 是否是默认 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1 \|\| model.ReservationId < 1`；`resultMsg.State`；`reservationInfo?.Id > 0`；`controlsModel.IsShow`；`reservationInfo.LessonsId > 0`；`reservationSeting.IsCancel && reservationSeting.CancelMinute > 0`；`ts.TotalMinutes <= reservationSeting.CancelMinute`
- 一层业务调用：`StoreReservationProvider.GetStoreReservationById`、`StoreReservationDetailedProvider.GetReservationInfoList`、`CommonReservationControlsItemProvider.GetCommonReservationControlsItemList`、`StoreReservationControlsProvider.GetStoreReservationControlsByInstructtions`、`StoreLessonsProvider.GetStoreLessonsByID`、`StoreReservationSetingProvider.GetReservationSeting`、`StoreProvider.GetStoreDateTime`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`固定提示：参数不正确`；`固定提示：预约记录不存在`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_reservation_calender`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取日历不可预约时间 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetReservationCalender` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetReservationCalenderResponseModel>>`；包装 `Task/DataResult`；Data `GetReservationCalenderResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:208` |
| C/B 对照 | crmapi.reservation.get_reservation_calender |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `BeginDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 开始时间；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 结束时间；普通业务字段；可按问题需要提供 |
| `CourseId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程ID 非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.VacationDates` | `List<string>` | 店铺不可预约日期(格式 MM-dd) | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`
- 一层业务调用：`StoreReservationProvider.GetReservationCalender`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_reservation_controls_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取自定义控件列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetReservationControlsList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetReservationControlsListResponseModel>>`；包装 `Task/DataResult`；Data `GetReservationControlsListResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:2329` |
| C/B 对照 | crmapi.reservation.get_reservation_controls_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls` | `List<GetReservationControlsListViewModel>` | 集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlName` | `string` | 控件名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlType` | `string` | 控件类型 input,radio,select.... | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].ControlInstructions` | `string` | 控件说明 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].IsMust` | `int` | 是否必填 1是 0否 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].IsShow` | `bool` | 是否对C端显示 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].Items` | `List<GetReservationItemControlsListViewModel>` | 选项列表 控件类型 为 radio select 不为空 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].Items[].Id` | `int` | id 主键id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Controls[].Items[].CommonReservationControlsId` | `int` | cid 控件id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Controls[].Items[].ItemValue` | `string` | item_value 值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].Items[].ItemName` | `string` | item_name 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Controls[].Items[].IsDefault` | `int` | is_default 是否是默认 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1`；`resultMsg.State`
- 一层业务调用：`StoreReservationControlsProvider.GetReservationControlsList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_reservation_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取已约列表 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetReservationList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<PageData<GetReservationListResponseModel>>>`；包装 `Task/DataResult`；Data `PageData<GetReservationListResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:37` |
| C/B 对照 | crmapi.reservation.business_get_reservation_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageSize` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可在服务端上限内选择 | 请求页数；普通业务字段；可按问题需要提供 |
| `StartDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 起始时间；普通业务字段；可按问题需要提供 |
| `EndDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 结束时间；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<GetReservationListResponseModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReservationId` | `int` | 预约id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ReservationDate` | `string` | 预约时间（日期部分 09-23） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReservationWeek` | `string` | 预约时间（星期部分 周一） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReservationTime` | `string` | 预约时间（时间部分 10:30） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ReservationTimeEnd` | `string` | 预约时间（时间部分 10:30） | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].StaffName` | `string` | 技师名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].StaffImg` | `string` | 技师头像 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].ItemsNames` | `List<string>` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].PlaceName` | `string` | 场地名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Remark` | `string` | 客户留言 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].State` | `int` | 状态 -2未到店，-1已取消，0未确认，1以确定，2已到店 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`
- 一层业务调用：`StoreReservationProvider.GetStoreReservationList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_reservation_time_seting`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取预约时间段 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetReservationTimeSeting` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetReservationTimeSetingResponseModel>>`；包装 `Task/DataResult`；Data `GetReservationTimeSetingResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:407` |
| C/B 对照 | crmapi.reservation.get_reservation_time_seting |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StaffId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 技师Id 团课非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约时间（格式"2012-01-21"）；普通业务字段；可按问题需要提供 |
| `ItemIds` | `List<int>` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按业务问题提供；仍需服务端 Schema 校验 | 项目Id(非必填)；普通业务字段；可按问题需要提供 |
| `CourseId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.CourseId <= 0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes` | `List<StoreReservationTimeSetingViewModel>` | 预约时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].Id` | `int` | 时间端Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ReservationTimes[].ReservationTime` | `string` | 预约时间段 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].ReservationTimeEnd` | `string` | 预约时间段 结束 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].IsReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].IsOccupy` | `bool` | 时间被占用 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationTimes[].SurplusCount` | `int` | 剩余可预约人数 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`resultMsg.State`；`store.StoreTypeId == "007" \|\| store.StoreTypeId == "010"`；`model.CourseId <= 0`
- 一层业务调用：`StoreProvider.GetStoreByIdAsync`、`StoreReservationTimeSetingProvider.GetReservationTimeSeting`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`固定提示：参数不正确`；`固定提示：课程ID不能为空`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_staff_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取教练详情 |
| 使用时机 | 商家核对员工、教练、权限或门店关系；不得把其他员工的个人信息无条件交给模型。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetStaffInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `C` — 查询路径包含疑似写入或外部副作用调用，必须人工复核：StaffPrivateLessonSetProvider.GetStaffPrivateLessonSet |
| 返回 | `Task<DataResult<GetStaffInfoViewModelResponseModel>>`；包装 `Task/DataResult`；Data `GetStaffInfoViewModelResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:2360` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.StaffId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.StaffId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StaffId` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Uid == 0 \\|\\| model.StoreId < 1 \\|\\| model.StaffId < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 员工的ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.StaffId` | `long` | 管理员id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserId` | `long` | 用户id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserName` | `string` | 用户名称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserImg` | `string` | 用户头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserMobile` | `string` | 用户手机 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserSex` | `int` | 用户性别 | 普通业务字段 | 可按问题需要提供 |
| `Data.StaffTags` | `List<ReservationTagViewModel>` | 教练标签 | 普通业务字段 | 可按问题需要提供 |
| `Data.StaffTags[].Id` | `long` | 标签id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StaffTags[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.SpecialiseTags` | `List<ReservationTagViewModel>` | 擅长标签 | 普通业务字段 | 可按问题需要提供 |
| `Data.SpecialiseTags[].Id` | `long` | 标签id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SpecialiseTags[].TagTitle` | `string` | 标签标题 | 普通业务字段 | 可按问题需要提供 |
| `Data.StaffExperience` | `string` | 店员经历 | 普通业务字段 | 可按问题需要提供 |
| `Data.ImgList` | `List<string>` | 图片集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 开放预约状态 1开放 0未开放 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid == 0 \|\| model.StoreId < 1 \|\| model.StaffId < 1`；`resultMsg.State`；`adminInfo?.Id > 0`；`staffInfo != null`；`user?.Id > 0`；`staffTags?.Count > 0`；`baseTags?.Count() > 0`；`experienceTags?.Count() > 0`；`staffImages?.Count > 0`
- 一层业务调用：`TenantUserProvider.GetTenantUserByStoreId`、`UsersInfoProvider.UsersInfoGetByUid`、`StaffPrivateLessonSetProvider.GetStaffPrivateLessonSet`、`TenantUserInfoProvider.GetTenantUserInfo`、`TenantUserTagRelationProvider.GetTenantUserTagRelationElementsByCondition`、`TenantUserImageProvider.GetTenantUserImageElementsByCondition`、`StoreReservationTagProvider.GetTagsByStoreId`
- 疑似副作用：`StaffPrivateLessonSetProvider.GetStaffPrivateLessonSet`。人工复核前禁止开放。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_staff_service_item_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取商户信息 |
| 使用时机 | 商家核对员工、教练、权限或门店关系；不得把其他员工的个人信息无条件交给模型。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetStaffServiceItemList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStaffServiceItemListResponseModel>>`；包装 `Task/DataResult`；Data `GetStaffServiceItemListResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:309` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StaffId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 技师Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationTime` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约时间 (格式 "2012-12-21 13:30")；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsSelectMoreItem` | `bool` | 是否可以多选 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems` | `List<StaffServiceItemViewModel>` | 预约项目 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems[].ItemId` | `int` | 服务ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.ServiceItems[].ItemImg` | `string` | 项目图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems[].ItemUnit` | `string` | 项目单位 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems[].ItemDuration` | `int` | 项目时长 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems[].ItemInfo` | `string` | 项目描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems[].ReservationPeopleSum` | `int` | 可预约总人数，0不显示 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems[].AlreadyReservationPeopleSum` | `long` | 已经预约人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.ServiceItems[].IsReservation` | `bool` | 是否可以预约 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`model.StaffId > 0 && TenantUserProvider.Instance.GetTenantUserByStoreId(model.StoreId) .All(x => x.Id != model.StaffId)`；`resultMsg.State`；`reservationSet.IsSelectItem`；`model.StaffId > 0`；`retModlTemp?.ItemId > 0`；`item.ReservationPeopleSum > 0`
- 一层业务调用：`TenantUserProvider.GetTenantUserByStoreId`、`StoreReservationSetingProvider.GetReservationSeting`、`StaffServiceItemProvider.BusinessGetStaffReservationServiceItems`、`StoreServiceItemProvider.BusinessGetReservationServiceItems`、`StaffServiceItemProvider.BusinessGetStaffReservationServiceItemPeopleSum`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`固定提示：参数不正确`；`固定提示：店员不存在`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_store_reservation_seting`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 获取商家预约设置 |
| 使用时机 | 顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetStoreReservationSeting` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetStoreReservationSetingResponseModel>>`；包装 `Task/DataResult`；Data `GetStoreReservationSetingResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:1102` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.Uid < 1 \\|\\| model.StoreId < 1) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardPayOrder` | `int` | 卡支付顺序，0预约时支付 1签到时支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.SignInSet` | `int` | 签到设置 1开课后自动签到 2下课后自动签到 3下课后N分钟自动签到 11老师点名签到 12扫码签到 13签字签到 | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupCardPayOrder` | `int` | 卡支付顺序，0预约时支付 1签到时支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.GroupSignInSet` | `int` | 签到设置 1开课后自动签到 2下课后自动签到 3下课后N分钟自动签到 11老师点名签到 12扫码签到 13签字签到 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsOnlyStaff` | `bool` | 私教是否只能约指定教练 | 普通业务字段 | 可按问题需要提供 |
| `Data.UserStaffId` | `long` | 登录人的销售顾问 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserCancelSum` | `long` | 用户在周期内已取消次数 | 普通业务字段 | 可按问题需要提供 |
| `Data.CancelCycle` | `int` | 0天 1周 2月 当N | 普通业务字段 | 可按问题需要提供 |
| `Data.CancelSum` | `int` | 取消N次 0不限制 | 普通业务字段 | 可按问题需要提供 |
| `Data.CancelAppointmentDays` | `int` | N天不允许预约 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsShowAvatar` | `bool` | 是否显示头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.IsShowPeopleNum` | `bool` | 是否显示预约人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsShowUnfilledQuota` | `bool` | 是否显示剩余可约名额 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationDay` | `int` | 提前N天可约 (-1不限制,0当天) | 普通业务字段 | 可按问题需要提供 |
| `Data.LessonShowMaxDay` | `int` | 私教显示排课范围xx天 0显示所有 | 普通业务字段 | 可按问题需要提供 |
| `Data.ReservationPeopleNum` | `int` | 私教课可预约人数，0不限制人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsShowPeopleList` | `bool` | is_show_people_list 是否显示预约列表 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Uid < 1 \|\| model.StoreId < 1`；`resultMsg.State`；`ucModel?.Id > 0`；`resultMsg.Data.CancelSum > 0`
- 一层业务调用：`StoreReservationSetingProvider.GetReservationSeting`、`UserCardProvider.BusinessGetUserCardInfo`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：参数格式错误！`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.reservation.get_work_staff_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 预约 |
| 用途 | 工作技师列表 |
| 使用时机 | 商家核对员工、教练、权限或门店关系；不得把其他员工的个人信息无条件交给模型。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Reservation/GetWorkStaffList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetWorkStaffListResponseModel>>`；包装 `Task/DataResult`；Data `GetWorkStaffListResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/ReservationController.cs:249` |
| C/B 对照 | crmapi.reservation.get_work_staff_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；if(model.StoreId < 1 \\|\\| model.Uid < 1) | 服务端注入：已确认门店 | 店铺Id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationTime` | `string` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约时间段；普通业务字段；可按问题需要提供 |
| `CourseId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 课程ID，非必填；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ReservationDate` | `string` | 代码校验必填 | 绑定=ApiController推断；if(string.IsNullOrEmpty(model.ReservationDate)) | AI 可按客户问题选择，必须使用门店时区和合法范围 | 预约日期(格式 "2012-12-21”)；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs` | `List<StoreStaffViewModel>` | 技师列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffId` | `int` | 技师Id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Staffs[].StaffImg` | `string` | 技师头像 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].StaffName` | `string` | 技师姓名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].JobTitle` | `string` | 职称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].IsVacation` | `bool` | 是否休假 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].IsReservation` | `bool` | 是否可约 | 普通业务字段 | 可按问题需要提供 |
| `Data.Staffs[].Tips` | `string` | 提示语 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId < 1 \|\| model.Uid < 1`；`string.IsNullOrEmpty(model.ReservationDate)`；`resultMsg.State`；`reservationSet.IsSelectStaff \|\| store.StoreTypeId == "007" \|\| store.StoreTypeId == "010"`；`model.CourseId > 0`
- 一层业务调用：`StoreReservationSetingProvider.GetReservationSeting`、`StoreProvider.GetStoreByIdAsync`、`StoreReservationProvider.GetLessonsStaffList`、`StoreReservationProvider.GetWorkStaffList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：MsgType = 0`；`状态赋值：StatusCode = 301`；`状态赋值：StatusCode = 302`；`固定提示：参数不正确`；`固定提示：请选择预约时间`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.food.get_client_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 餐饮订单 |
| 用途 | 获取购物车的客户列表 |
| 使用时机 | 在顾客视角中核对“获取购物车的客户列表”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Food/GetClientList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<List<GetClientListResponseModel>>`；包装 `DataResult`；Data `List<GetClientListResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/FoodPartialController.cs:27` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `FoodCartId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 购物车ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].UserName` | `string` | 用户名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data[].HeadImg` | `string` | 头像 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`
- 一层业务调用：`FoodTableProvider.GetClientList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.food.get_food_cart`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 餐饮订单 |
| 用途 | 获取点餐购物车 |
| 使用时机 | 在顾客视角中核对“获取点餐购物车”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Food/GetFoodCart` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetFoodCartResponseModel>>`；包装 `Task/DataResult`；Data `GetFoodCartResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/FoodPartialController.cs:239` |
| C/B 对照 | crmapi.food.get_food_cart |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `TableId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 桌号；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Id` | `int` | 购物车ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodCount` | `int` | 商品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalPrice` | `decimal` | 总价 | 普通业务字段 | 可按问题需要提供 |
| `Data.VipDiscount` | `decimal` | 会员折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems` | `List<FoodCartItemViewModel>` | 商品列表 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Id` | `int` | id 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodCartItems[].StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodCartItems[].FoodCartId` | `int` | food_cart_id 购物车ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodCartItems[].FoodId` | `int` | food_name 菜品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodCartItems[].FoodName` | `string` | 菜品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].FoodPrice` | `decimal` | 菜品价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].FoodImg` | `string` | 菜品图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].FoodCount` | `int` | food_num 菜品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].SkuValue` | `string` | sku_value 规格 值 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].SkuString` | `string` | sku_string 规格 文本 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].State` | `int` | state 状态 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].CreateDate` | `DateTime` | create_date | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].UpdateDate` | `DateTime` | update_date | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].CreateBy` | `int` | create_by | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].UpdateBy` | `int` | update_by | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].EnjoyVipDiscount` | `bool` | 享受会员折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users` | `List<UserInfoViewModel>` | 点餐用户 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Uid` | `int` | 用户ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodCartItems[].Users[].CardId` | `int` | 会员卡ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodCartItems[].Users[].Mobile` | `string` | 手机号 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.FoodCartItems[].Users[].UserImg` | `string` | 用户头像 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.FoodCartItems[].Users[].UserName` | `string` | 用户昵称 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.FoodCartItems[].Users[].IsVip` | `bool` | 是否是VIP | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services` | `List<UserCardServiceItemViewModel>` | 项目信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services[].ItemId` | `int` | 项目ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodCartItems[].Users[].Services[].ItemName` | `string` | 项目名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services[].ItemUnit` | `string` | 项目单位（服务单位） | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services[].CardValue` | `decimal` | 剩余金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services[].CardNormalValue` | `decimal` | 正金(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services[].CardGiveValue` | `decimal` | 赠送金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services[].ConsumptionValue` | `decimal` | 消费金额(次数) | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services[].ItemPrice` | `decimal` | 项目单价 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCartItems[].Users[].Services[].IsDefault` | `bool` | 是否默认，默认选中上次核销的项目 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`
- 一层业务调用：`FoodCartProvider.GetFoodCart`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.food.get_food_inforation_to_c`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 餐饮订单 |
| 用途 | 获取食品详情 |
| 使用时机 | 在顾客视角中核对“获取食品详情”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Food/GetFoodInforationToC` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetFoodInforationToCResponseModel>>`；包装 `Task/DataResult`；Data `GetFoodInforationToCResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/FoodController.cs:23` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `Id` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.Id < 1) | 必须来自同一会话上游 API 结果或服务端对象引用 | 食品id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 店铺id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data.Id` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.IsVip` | `bool` | 是否是vip；false-不是，true-是 | 普通业务字段 | 可按问题需要提供 |
| `Data.ImgList` | `List<string>` | 食品图片集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Name` | `string` | 食品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Describe` | `string` | 食品描述 | 普通业务字段 | 可按问题需要提供 |
| `Data.Price` | `decimal` | 价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.VipPrice` | `decimal?` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.Quantity` | `int` | 库存 | 普通业务字段 | 可按问题需要提供 |
| `Data.CategoryList` | `List<int>` | 食品分类集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.TagList` | `List<int>` | 食品标签集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.RightTagList` | `List<string>` | 食品角标集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList` | `List<EditFoodSkuListModel>` | 规格列表集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuId` | `int` | 规格id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SkuList[].SkuName` | `string` | 规格名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].IsSingle` | `bool` | 是否单选；0-单选，1-多选 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuItemList` | `List<EditFoodSkuItemListModel>` | 规格属性集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuItemList[].SkuItemId` | `int` | 规格子项id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SkuList[].SkuItemList[].SkuItemName` | `string` | 规格属性名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuItemList[].SkuItemPrice` | `decimal` | 规格属性价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.SkuList[].SkuItemList[].SkuItemVipPrice` | `decimal` | 规格属性会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data.SellNum` | `int` | 销量 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.Id < 1`；`resultMsg.State`
- 一层业务调用：`FoodProvider.GetFoodInforationToC`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请填写id`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.food.get_food_list_to_c`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 餐饮订单 |
| 用途 | 获取食品列表 |
| 使用时机 | 在顾客视角中核对“获取食品列表”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Food/GetFoodListToC` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<List<GetFoodListToCResponseModel>>>`；包装 `Task/DataResult`；Data `List<GetFoodListToCResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/FoodController.cs:53` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `AppId` | `string` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：当前产品/小程序配置 | 小程序APPID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端上下文注入（源码未确认必填） | 绑定=ApiController推断；未发现显式必填证据 | 服务端注入：已确认门店 | 店铺id；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].Message` | `string` | 返回信息 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ClassId` | `int` | 分类id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].ClassName` | `string` | 分类名称 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Count` | `int` | 个数 | 普通业务字段 | 可按问题需要提供 |
| `Data[].ShopCount` | `int` | 当前分类中购物车个数 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList` | `List<FoodListViewModel>` | 食品列表 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].Id` | `int` | 食品id | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].FoodList[].Name` | `string` | 名称 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].Img` | `string` | 图片 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].RightTagName` | `List<string>` | 角标签 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].Quantity` | `string` | 库存 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].SellNum` | `string` | 销量 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].Price` | `decimal` | 原价 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].VipPrice` | `decimal` | 会员价 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].VipDisCount` | `decimal` | 会员最低折扣 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].State` | `int` | 状态；0-下架，1-上架 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].EnjoyVipDiscount` | `bool` | 是否享受会员卡折扣价 | 普通业务字段 | 可按问题需要提供 |
| `Data[].FoodList[].IsWithSku` | `bool` | 是否多规格 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`resultMsg.State`
- 一层业务调用：`FoodProvider.GetFoodListToC`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.food.get_food_order_detail`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 餐饮订单 |
| 用途 | 获取订单详情 |
| 使用时机 | 顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Food/GetFoodOrderDetail` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetFoodOrderDetailResponseModel>>`；包装 `Task/DataResult`；Data `GetFoodOrderDetailResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/FoodPartialController.cs:393` |
| C/B 对照 | crmapi.food.get_food_order_detail |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `ConsumptionId` | `long` | 参与组合校验 | 绑定=ApiController推断；if(model.FoodOrderId <= 0 && model.ConsumptionId <= 0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 财务ID（非必填）；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `FoodOrderId` | `int` | 参与组合校验 | 绑定=ApiController推断；if(model.FoodOrderId <= 0 && model.ConsumptionId <= 0) | 必须来自同一会话上游 API 结果或服务端对象引用 | 订单ID（非必填）；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Id` | `int` | id 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.OrderType` | `int` | 订单类型 0 堂食 1外卖 2自取 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | status 订单状态：0 未付款 ，1 已付款 | 普通业务字段 | 可按问题需要提供 |
| `Data.No` | `string` | 流水号 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodCount` | `int` | product_number 菜品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.NeedPayment` | `decimal` | need_payment 应付金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.Payment` | `decimal` | payment 实付金额。精确到2位小数;单位:元。如:200.07，表示:200元7分 | 普通业务字段 | 可按问题需要提供 |
| `Data.Remark` | `string` | remark 买家备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.BusinessRemark` | `string` | business_remark 卖家备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.BuyerName` | `string` | buyer_name 买家名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.BuyerHeadImg` | `string` | 买家头像 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayMethod` | `int` | pay_method 支付方式：0 会员卡支付、1微信支付、2支付宝支付 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateDate` | `DateTime` | create_date 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.PayDate` | `DateTime` | pay_date 支付时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.UpdateDate` | `DateTime` | update_date 更新时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.CreateBy` | `int` | create_by 创建人 | 普通业务字段 | 可按问题需要提供 |
| `Data.UpdateBy` | `int` | update_by 更新人 | 普通业务字段 | 可按问题需要提供 |
| `Data.ConsumptionId` | `string` | consumption_id 财务ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.IntegralDeduct` | `decimal` | 积分减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CommissionDeduct` | `decimal` | 佣金减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CardDeduct` | `decimal` | 权益卡、储值卡减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.CouponDeduct` | `decimal` | 优惠券减免金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems` | `List<FoodOrderItemModel>` | 订单子项 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].Id` | `int` | id 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodOrderItems[].StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodOrderItems[].FoodOrderId` | `int` | food_order_id 订单ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodOrderItems[].FoodId` | `int` | 菜品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.FoodOrderItems[].FoodName` | `string` | food_name 菜品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].FoodCount` | `int` | food_num 菜品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].FoodPrice` | `decimal` | food_price 菜品价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].SkuValue` | `string` | sku_value 规格值 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].SkuString` | `string` | sku_string 规格文本 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].FoodImg` | `string` | food_img 图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].State` | `int` | state | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].CreateBy` | `int` | create_by | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].CreateDate` | `DateTime` | create_date | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].UpdateBy` | `int` | update_by | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].UpdateDate` | `DateTime` | update_date | 普通业务字段 | 可按问题需要提供 |
| `Data.FoodOrderItems[].TenantId` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.PreferentialType` | `int` | 优惠类型 | 普通业务字段 | 可按问题需要提供 |
| `Data.TableNo` | `int` | 桌号 | 普通业务字段 | 可按问题需要提供 |
| `Data.TableName` | `string` | 桌名 | 普通业务字段 | 可按问题需要提供 |
| `Data.PeopleCount` | `int` | 人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.FinalPrice` | `decimal` | 商议金额（商家最终优惠） | 普通业务字段 | 可按问题需要提供 |
| `Data.DisCount` | `decimal` | 折扣（商家最终优惠） | 普通业务字段 | 可按问题需要提供 |
| `Data.TakeTime` | `string` | 取餐时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.TableId` | `int` | 桌台ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.CardId` | `int` | 会员卡ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.RiderName` | `string` | 配送员名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.RiderMobile` | `string` | 配送员电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.RiderAddress` | `string` | 配送员地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiverName` | `string` | 收货人姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiverMobile` | `string` | 收货人电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.ReceiverAddress` | `string` | 收货人地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Distance` | `int` | 配送距离 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreRiderId` | `int` | 配送员ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.UserAddressId` | `int` | 收货地址ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.SendOutPrice` | `decimal` | 配送费 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreMobile` | `string` | 店铺电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.UserMobile` | `string` | 会员电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.IsShowRefundButton` | `bool` | 是否显示退款按钮 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsRefunds` | `bool` | 是否已退款 | 普通业务字段 | 可按问题需要提供 |
| `Data.SourceId` | `string` | 退款原订单ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.RefundPrice` | `decimal` | 退款金额 | 普通业务字段 | 可按问题需要提供 |
| `Data.StoreUserName` | `string` | 操作店员姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |

#### 代码行为与证据

- Controller 条件：`model.FoodOrderId <= 0 && model.ConsumptionId <= 0`
- 一层业务调用：`FoodOrderProvider.GetFoodOrderDetail`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数有误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.food.get_food_order_list`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 餐饮订单 |
| 用途 | 获取订单列表 |
| 使用时机 | 顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Food/GetFoodOrderList` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<PageData<GetFoodOrderListResponseModel>>>`；包装 `Task/DataResult`；Data `PageData<GetFoodOrderListResponseModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/FoodPartialController.cs:423` |
| C/B 对照 | crmapi.food.get_food_order_list |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required] | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `OrderState` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | AI 只能使用文档确认的枚举值 | 订单状态 0 当前 1历史,2全部,3待出餐 4 待配送；普通业务字段；可按问题需要提供 |
| `RiderId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 骑手ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `PageSize` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageIndex == 0 \\|\\| model.PageSize == 0) | AI 可在服务端上限内选择 | 每页的数据；普通业务字段；可按问题需要提供 |
| `PageIndex` | `int` | 代码校验必填 | 绑定=ApiController推断；if(model.PageIndex == 0 \\|\\| model.PageSize == 0) | AI 可在服务端上限内选择 | 页码索引；普通业务字段；可按问题需要提供 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.PageSize` | `int` | 每页数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageIndex` | `int` | 当前页 | 普通业务字段 | 可按问题需要提供 |
| `Data.PageCount` | `int` | 总页数 | 普通业务字段 | 可按问题需要提供 |
| `Data.TotalCount` | `int` | 数据总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.IsNext` | `bool` | 是否有下页 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[]` | `List<GetFoodOrderListResponseModel>` | 数据集合 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Id` | `int` | 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].ConsumptionId` | `long` | 财务ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].StoreId` | `int` | 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].State` | `int` | 订单状态：-2 退款 0 未付款 ，1 已付款，2已出餐，3已配送，4已完成 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].No` | `string` | 流水号 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].Payment` | `decimal` | 实付金额。精确到2位小数;单位:元。如:200.07，表示:200元7分 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].CreateDate` | `DateTime` | 创建时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].TableNo` | `long` | 桌号 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].TableName` | `string` | 桌名 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].PeopleCount` | `int` | 人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].TakeTime` | `string` | 取餐时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems` | `List<FoodOrderItemModel>` | 订单子项 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].Id` | `int` | id 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].FoodOrderItems[].StoreId` | `int` | store_id 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].FoodOrderItems[].FoodOrderId` | `int` | food_order_id 订单ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].FoodOrderItems[].FoodId` | `int` | 菜品ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].FoodOrderItems[].FoodName` | `string` | food_name 菜品名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].FoodCount` | `int` | food_num 菜品数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].FoodPrice` | `decimal` | food_price 菜品价格 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].SkuValue` | `string` | sku_value 规格值 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].SkuString` | `string` | sku_string 规格文本 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].FoodImg` | `string` | food_img 图片 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].State` | `int` | state | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].CreateBy` | `int` | create_by | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].CreateDate` | `DateTime` | create_date | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].UpdateBy` | `int` | update_by | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].UpdateDate` | `DateTime` | update_date | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodOrderItems[].TenantId` | `int` | 源码属性注释缺失 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].FoodTypeCount` | `int` | 食品种类数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].FoodCount` | `int` | 食品总数量 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].RiderName` | `string` | 配送员名称 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].RiderMobile` | `string` | 配送员电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].RiderAddress` | `string` | 配送员地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].ReceiverName` | `string` | 收货人姓名 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].ReceiverMobile` | `string` | 收货人电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].ReceiverAddress` | `string` | 收货人地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].Distance` | `int` | 配送距离 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].StoreRiderId` | `int` | 配送员ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].UserAddressId` | `int` | 收货地址ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.Data[].Remark` | `string` | 备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].BusinessRemark` | `string` | 商家备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.Data[].SendOutPrice` | `decimal` | 配送费 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].OrderType` | `int` | 0堂食 1外卖 2自取 | 普通业务字段 | 可按问题需要提供 |
| `Data.Data[].StoreMobile` | `string` | 商家电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |

#### 代码行为与证据

- Controller 条件：`model.PageIndex == 0 \|\| model.PageSize == 0`；`resultMsg.State`
- 一层业务调用：`FoodOrderProvider.GetFoodOrderList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请传递参数`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.food.get_food_table_info`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 餐饮订单 |
| 用途 | 获取桌台信息 |
| 使用时机 | 在顾客视角中核对“获取桌台信息”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Food/GetFoodTableInfo` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `Task<DataResult<GetFoodTableInfoResponseModel>>`；包装 `Task/DataResult`；Data `GetFoodTableInfoResponseModel` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/FoodPartialController.cs:56` |
| C/B 对照 | crmapi.food.get_food_table_info |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(model.StoreId <= 0 \\|\\| model.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `TableId` | `int` | 源码未确认必填 | 绑定=ApiController推断；未发现显式必填证据 | 必须来自同一会话上游 API 结果或服务端对象引用 | 桌台ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data.Id` | `int` | 桌台ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.StoreId` | `int` | 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data.TableName` | `string` | 桌名 | 普通业务字段 | 可按问题需要提供 |
| `Data.TableNo` | `int` | 桌号 | 普通业务字段 | 可按问题需要提供 |
| `Data.PeopleNum` | `int` | 人数 | 普通业务字段 | 可按问题需要提供 |
| `Data.State` | `int` | 状态 | 普通业务字段 | 可按问题需要提供 |
| `Data.LastUseTime` | `DateTime` | 最后使用时间 | 普通业务字段 | 可按问题需要提供 |
| `Data.Remark` | `string` | 备注 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data.TableQrcode` | `string` | 桌号二维码 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`model.StoreId <= 0 \|\| model.Uid <= 0`
- 一层业务调用：`FoodTableProvider.GetFoodTableInfo`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

### `capi.food.get_user_address`

| 项目 | 内容 |
| --- | --- |
| 业务域 | 餐饮订单 |
| 用途 | 获取用户地址列表 |
| 使用时机 | 在顾客视角中核对“获取用户地址列表”对应的当前返回结果。 |
| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |
| 请求 | `POST /api/Food/GetUserAddress` |
| 鉴权 | 继承登录鉴权基类 |
| 工具等级 | `B` — 代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。 |
| 返回 | `DataResult<List<FoodUserAddressViewModel>>`；包装 `DataResult`；Data `List<FoodUserAddressViewModel>` |
| 数据时效 | 当前调用时状态；不能据此还原过去某一时刻 |
| 源码 | `Public/LingKe/Link.CApi/Controllers/WebApi/FoodPartialController.cs:584` |
| C/B 对照 | 未发现同 Controller/同语义名称的另一视角接口 |

#### 请求参数

| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |
| --- | --- | --- | --- | --- | --- |
| `Uid` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(request.StoreId <= 0 \\|\\| request.Uid <= 0) | 服务端注入：目标会员 UID | 源码属性注释缺失；内部标识；不向客户展示；模型调用时优先使用服务端引用 |
| `StoreId` | `int` | 服务端必注入 | 绑定=ApiController推断；[Required]；if(request.StoreId <= 0 \\|\\| request.Uid <= 0) | 服务端注入：已确认门店 | 商家ID；内部标识；不向客户展示；模型调用时优先使用服务端引用 |

#### 响应参数

除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。

| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |
| --- | --- | --- | --- | --- |
| `Data[].Id` | `int` | 主键 | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].StoreId` | `int` | 店铺ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].Uid` | `int` | 用户ID | 内部标识 | 不向客户展示；模型调用时优先使用服务端引用 |
| `Data[].IsDefault` | `bool` | 是否默认地址 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Province` | `string` | 省 | 普通业务字段 | 可按问题需要提供 |
| `Data[].City` | `string` | 市 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Area` | `string` | 区域 | 普通业务字段 | 可按问题需要提供 |
| `Data[].Address` | `string` | 地址 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data[].Mobile` | `string` | 电话 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data[].Receiver` | `string` | 联系人 | 个人信息 | 仅在当前授权场景按最小范围提供 |
| `Data[].Sex` | `int` | 性别 0 男 1 女 2保密 | 普通业务字段 | 可按问题需要提供 |
| `Data[].HouseNumber` | `string` | 门牌号 | 普通业务字段 | 可按问题需要提供 |

#### 代码行为与证据

- Controller 条件：`request.StoreId <= 0 \|\| request.Uid <= 0`
- 一层业务调用：`FoodUserAddressProvider.GetUserAddressList`
- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。
- 显式失败信号：`状态赋值：StatusCode = 301`；`固定提示：请求参数错误`
- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。

## 排除项复核规则

- D 级接口已保留在“全部 Action 索引”中以证明审计范围，但不提供模型调用契约。
- C 级接口只有在确认查询过程不写业务数据、不发消息、不产生支付/核销/退款等外部状态后才能升级。
- 后续新增 Action 必须重新运行生成脚本；如果源码指纹变化而目录未更新，应阻止工具目录发布。
- XML 摘要缺失、DTO 无法解析或 Controller/Provider 结论冲突时，以“待人工复核”处理，不能由 Agent 自行解释。
