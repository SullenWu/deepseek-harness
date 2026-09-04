#!/usr/bin/env python3
"""从 LingKe.CApi / LingKe.CRMApi 源码生成 AI 只读工具筛选目录。

该脚本只做静态分析，不启动 API、不连接数据库，也不会把配置、密钥或真实业务数据写入目录。
机械信息（路由、DTO、特性、代码校验、Provider 调用）由脚本提取；无法由源码确定的业务语义
必须在目录中明确标记为“待人工复核”，不能伪装成已确认事实。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable


HTTP_ATTRIBUTE_RE = re.compile(r"\[\s*Http(Get|Post|Put|Delete|Patch|Head|Options)\b", re.I)
NAMESPACE_RE = re.compile(r"\bnamespace\s+(?P<name>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*(?:;|\{)")
USING_RE = re.compile(r"^\s*using\s+(?P<name>[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*;", re.M)
CLASS_RE = re.compile(
    r"\b(?:public|internal)\s+(?:sealed\s+|abstract\s+|partial\s+)*class\s+"
    r"(?P<name>[A-Za-z_]\w*)(?:\s*<[^>{}]+>)?(?:\s*:\s*(?P<bases>[^\{\r\n]+))?\s*\{"
)
PROPERTY_RE = re.compile(
    r"(?P<attrs>(?:\s*\[[^\]]+\]\s*)*)"
    r"\bpublic\s+(?P<type>[A-Za-z_][\w\.\?<>,\[\]\s:]*)\s+"
    r"(?P<name>[A-Za-z_]\w*)\s*\{\s*get\s*;\s*(?:(?:set|init)\s*;\s*)?\}"
    r"(?:\s*=\s*(?P<default>[^;\r\n]+))?\s*;?",
    re.S,
)
METHOD_RE = re.compile(
    r"(?P<attrs>(?:\s*\[[^\]]+\]\s*)+)"
    r"\bpublic\s+(?:async\s+)?(?P<return>[A-Za-z_][\w\.\?<>,\[\]\s:]*)\s+"
    r"(?P<name>[A-Za-z_]\w*)\s*\(",
    re.S,
)
IF_RE = re.compile(r"\bif\s*\(")
CALL_RE = re.compile(
    r"\b(?P<owner>[A-Za-z_]\w*(?:Provider|Service|Helper|Manager|Dao|Client|Repository))"
    r"(?:\.Instance)?\.(?P<method>[A-Za-z_]\w*)\s*\("
)

READ_NAME_RE = re.compile(
    r"(Get|Query|Search|Find|List|Check|Exists|Exist|Has|Is|Count|Statistic|Report|"
    r"Detail|Info|Preview|Validate|Verify|Resolve|Load|Calculate)",
    re.I,
)
WRITE_NAME_RE = re.compile(
    r"^(Add|Insert|Create|Update|Set|Delete|Remove|Save|Edit|Modify|Pay|Refund|Consume|"
    r"Cancel|Confirm|Submit|Apply|Upload|Send|Bind|Unbind|Change|Start|Stop|Open|Close|"
    r"Receive|SignUp|Recharge|Renew|Transfer|Audit|Publish|Issue|Grant|Sync)",
    re.I,
)
MUTATION_CALL_RE = re.compile(
    r"^(Add|Insert|Create|Update|Set|Delete|Remove|Save|Edit|Modify|Pay|Refund|Consume|"
    r"Cancel|Confirm|Submit|Apply|Upload|Send|Bind|Unbind|Change|Start|Stop|Open|Close|"
    r"Receive|SignUp|Recharge|Renew|Transfer|Audit|Publish|Issue|Grant|Sync|Append|Write)",
    re.I,
)
DENY_CONTROLLER_RE = re.compile(r"(Test|UnitTest|TemplateTest|AdminWebAuth)", re.I)
DENY_ACTION_RE = re.compile(r"(Callback|CallBack|Login|Logout|Webhook|Notify|Notification)", re.I)
IDENTIFIER_NAME_RE = re.compile(r"(^Id$|Id$|^Uid$|UserId$|StoreId$|CardId$|OrderId$|LessonsId$)", re.I)
BUSINESS_REFERENCE_NAME_RE = re.compile(r"(OrderNo|OrderNumber|TradeNo|SerialNo|RecordNo|BillNo)$", re.I)
PAGING_NAME_RE = re.compile(r"(PageIndex|PageSize|Limit|Offset)", re.I)
DATE_NAME_RE = re.compile(r"(Date|Time|Begin|End|Start)", re.I)
STATE_NAME_RE = re.compile(r"(State|Status|Type|Tag|Sort|OrderBy)", re.I)

# 个别旧接口把手机号复用在通用搜索字段中，单靠字段名无法识别其真实敏感语义。
# 这里声明的是“已审核 API 参数来源”，不是客户问题、关键词或接口路由；模型仍通过通用能力检索动态选接口。
TRUSTED_REQUEST_SOURCE_POLICY_OVERRIDES = {
    ("crmapi.card.business_get_user_cards", "KeyWord"): "conversation-sensitive-context",
}

READ_VERB_TOKENS = {
    "get", "query", "search", "serarch", "find", "list", "check", "exists", "exist",
    "has", "is", "count", "statistic", "report", "detail", "info", "preview", "validate",
    "verify", "resolve", "load", "calculate",
}
WRITE_VERB_TOKENS = {
    "add", "insert", "create", "update", "set", "delete", "remove", "save", "edit",
    "modify", "pay", "refund", "consume", "cancel", "confirm", "submit", "apply", "upload",
    "send", "bind", "unbind", "change", "start", "stop", "open", "close", "receive", "signup",
    "recharge", "renew", "transfer", "audit", "publish", "issue", "grant", "sync", "register",
    "export", "import", "modify", "approve", "reject", "dispatch", "notify",
}

SCALAR_TYPES = {
    "bool", "byte", "sbyte", "short", "ushort", "int", "uint", "long", "ulong",
    "float", "double", "decimal", "char", "string", "object", "dynamic", "DateTime",
    "DateTimeOffset", "TimeSpan", "Guid", "Uri", "IFormFile", "CancellationToken",
}
GENERIC_COLLECTIONS = {
    "List", "IList", "IReadOnlyList", "IEnumerable", "ICollection", "HashSet", "Array",
}

DOMAIN_BY_CONTROLLER = {
    "User": "会员与身份",
    "Card": "会员卡与课卡",
    "StoreCard": "卡产品与售卡",
    "Reservation": "预约",
    "ReservationSet": "预约配置",
    "Lessons": "课次与排课",
    "Course": "课程",
    "StoreCourse": "门店课程",
    "Consumption": "消费与核销",
    "Order": "订单",
    "ShopOrder": "商城订单",
    "Food": "餐饮订单",
    "Coupon": "优惠券",
    "CouponCenter": "领券中心",
    "Integral": "积分",
    "StoreIntegral": "积分配置",
    "Store": "门店",
    "StoreSet": "门店设置",
    "Staff": "员工与教练",
    "Employee": "员工",
    "OperatingReports": "经营报表",
    "WorkBench": "工作台",
    "Soft": "软件订购与版本",
    "MobileManagement": "移动端绑定",
    "WorkWeChat": "企业微信",
    "Product": "商品",
    "StoreProduct": "门店商品",
    "ShoppingMall": "商城",
    "Message": "消息",
    "Complaint": "投诉与客服",
    "CustomerService": "客服",
}

# 机器目录中的能力选择语义。这里描述接口自身的稳定用途、返回范围和与相邻接口的边界，
# 不保存客户问法、关键词路由或固定回答。未列出的接口仍由 Controller 摘要和响应 DTO 确定性生成。
MANIFEST_USAGE_OVERRIDES: dict[str, dict[str, object]] = {
    # 商家端：同一读取接口通过 DataType 明确区分时间、数量和预约人数，不能把缺省 0 当成空结果。
    "crmapi.lessons.get_course_scheduling": {
        "capability": "按日期范围获取门店排课安排、排课数量或预约人数（日历聚合）",
        "purpose": (
            "按门店时区和日期范围读取排课日历；DataType=1 返回具体排课时间，DataType=2 返回排课数量，"
            "DataType=3 返回预约人数，Conditions=0 按日、Conditions=1 按月聚合。"
        ),
        "whenToUse": (
            "需要核对门店在某日或某月的排课安排、排课数量或预约人数时使用；可按课程类型筛选，"
            "CourseId 和 StaffId 仅在已取得对应上游引用时限定。"
        ),
        "doNotUse": (
            "不用于查询指定会员个人的上课日历，也不用于员工请假或增长统计。DataType 必须按目标明确选择，"
            "响应为空不能在缺少完整性证据时直接解释为数量 0。"
        ),
        "usageEvidence": [
            "LessonsController.GetCourseScheduling 的 DataType 分支",
            "GetCourseSchedulingRequestModel 参数契约",
            "GetCourseSchedulingResponseModel 日历聚合响应",
        ],
    },
    # 商家端：会员详情是会员域的聚合读取入口，不能被普通列表、单卡余额或流水接口替代。
    "crmapi.user.business_get_user_info": {
        "capability": "获取会员完整详情及名下全部会员卡、余额与有效期（会员详情聚合）",
        "purpose": (
            "商家端会员详情聚合读取：一次返回目标会员在当前门店的基础资料、备注和自定义资料、"
            "分组/标签、来源渠道、销售顾问、黑名单与协议状态、积分/佣金和消费汇总，并在 Cards 中"
            "返回该会员主账户名下全部子会员卡及每张卡的类型、状态、余额或次数、有效期、折扣、"
            "服务项目和使用限制。"
        ),
        "whenToUse": (
            "已从会员列表、搜索结果或其他受控上游取得 UserId 或 CardId，需要打开或刷新会员详情，"
            "或需要同时核对会员资料、分组、全部持卡、各卡余额/次数和有效期时首选。UserId 与 CardId "
            "至少一项必须有效；预约选卡或核对指定用卡时点时才传 UsedDatetime。"
        ),
        "doNotUse": (
            "不要为同一会员的综合详情先拆调会员卡列表或余额接口；消费流水、预约/上课记录、优惠券"
            "明细仍应调用各自分页或详情接口。本接口只读当前快照，不证明历史时点，也不执行资料或资产修改。"
        ),
        "usageEvidence": [
            "PC 全局会员详情抽屉调用链",
            "UserController.BusinessGetUserInfo",
            "BusinessGetUserInfoResponseModel",
        ],
    },
    "crmapi.user.get_users_list_v2": {
        "capability": "分页筛选会员列表与列表摘要",
        "purpose": "按服务端 SearchCondition 分页读取当前门店会员列表和列表展示所需摘要，用于定位会员对象。",
        "whenToUse": "会员管理列表加载、翻页或按服务端支持的条件筛选时使用；取得目标会员引用后，再用会员详情聚合接口读取完整资料和全部持卡。",
        "doNotUse": "列表摘要不能替代会员详情、具体持有卡状态/余额或历史流水。",
        "usageEvidence": ["PC 会员列表调用链", "UserController.GetUsersListV2", "列表响应 DTO"],
    },
    "crmapi.store.get_search_user": {
        "capability": "按手机号尾号或会员线索定位当前门店会员",
        "purpose": "在当前门店范围内搜索会员候选，返回建立后续会员、卡和预约查询所需的受控对象引用。",
        "whenToUse": "只有会员尚未定位、且会话已安全提供搜索线索时作为查询入口；定位成功后转会员详情聚合接口。",
        "doNotUse": "不能跨门店搜索、不能把搜索候选当成完整会员详情，也不能向模型或客户暴露内部主键。",
        "usageEvidence": ["会员搜索调用链", "StoreController.GetSearchUser", "搜索响应 DTO"],
    },
    "crmapi.card.business_get_users": {
        "capability": "按卡状态读取会员首页分组列表",
        "purpose": "按服务端 CardState 与关键字口径读取会员首页的分组会员集合及余额、卡数、最近消费等摘要。",
        "whenToUse": "商家端会员首页查看正常、临期、过期等卡状态分组，或按该专用口径定位会员时使用。",
        "doNotUse": "不能替代通用分页筛选列表，也不能替代单个会员完整详情。",
        "usageEvidence": ["商家会员首页调用链", "CardController.BusinessGetUsers", "分组列表 DTO"],
    },
    "crmapi.card.business_get_user_cards": {
        "capability": "分页筛选多名会员的持卡摘要",
        "purpose": "按筛选条件分页返回多名会员及其卡类型、有效期、积分、印章等持卡摘要。",
        "whenToUse": "需要跨会员筛选或浏览持卡列表时使用；定位单个会员后优先用会员详情聚合接口获取其全部子卡和完整余额。",
        "doNotUse": "不要用它回答已定位会员的完整资料或全部卡内服务余额，也不要把列表摘要当单卡详情。",
        "usageEvidence": ["会员卡筛选页调用链", "CardController.BusinessGetUserCards", "分页响应 DTO"],
    },
    "crmapi.card.business_get_user_card_balance": {
        "capability": "读取单张会员卡的可调整余额构成",
        "purpose": "返回调整余额页面所需的目标卡信息、剩余金额/次数、正金、赠金、优惠金额和已消费值。",
        "whenToUse": "已取得目标 CardId/ChildCardId，且需要核对调账前后单卡余额构成时使用。",
        "doNotUse": "不是会员综合详情或多卡列表接口，也不执行余额调整。",
        "usageEvidence": ["余额调整页面调用链", "CardController.BusinessGetUserCardBalance", "余额响应 DTO"],
    },
    "crmapi.consumption.business_get_user_consumption_list": {
        "capability": "分页读取指定会员的消费、充值与卡资产变动流水",
        "purpose": "按会员、主卡或子卡及筛选条件分页返回消费、充值、核减、返还、赠送、过期、停复卡等流水和操作后值。",
        "whenToUse": "会员已定位后，会员详情页切换到消费记录或需要按时间、类型核对资产变化过程时使用。",
        "doNotUse": "不用于读取会员基础资料或全部持卡快照；单笔原因和商品/服务明细需再查消费详情。",
        "usageEvidence": ["PC 会员详情消费面板调用链", "ConsumptionController.BusinessGetUserConsumptionList", "分页流水 DTO"],
    },
    "crmapi.consumption.business_get_consumption_info": {
        "capability": "读取单笔消费或充值单据详情",
        "purpose": "返回单笔消费的会员、门店、支付方式、资产变化、操作人员以及服务/商品等明细。",
        "whenToUse": "已从流水列表取得 ConsumptionId，需要解释某一笔交易的组成、支付方式或操作结果时使用。",
        "doNotUse": "不能替代流水列表或当前余额快照，也不执行退款、返还或调账。",
        "usageEvidence": ["会员详情单据抽屉调用链", "ConsumptionController.BusinessGetConsumptionInfo", "消费详情 DTO"],
    },
    "crmapi.lessons.get_user_lessons_reservation_list": {
        "capability": "分页读取指定会员的预约与上课记录",
        "purpose": "按会员卡、日期和状态分页返回预约课程、教练、签到与预约状态等记录。",
        "whenToUse": "会员详情页查看课程记录，或核对目标会员是否预约、取消、候补、签到、完课或旷课时使用。",
        "doNotUse": "不用于查询全店课表或修改预约状态；单条预约的完整信息应使用预约/个人预约详情。",
        "usageEvidence": ["PC 会员详情课程面板调用链", "LessonsController.GetUserLessonsReservationList", "预约记录 DTO"],
    },
    "crmapi.lessons.get_user_lessons_scheduling": {
        "capability": "读取指定会员的上课日历分布",
        "purpose": "按日期范围汇总目标会员有课程或上课记录的日历数据。",
        "whenToUse": "会员详情课程面板需要先展示月份日历、再按选中日期加载记录时使用。",
        "doNotUse": "不返回单条预约完整详情，也不用于全店排课。",
        "usageEvidence": ["PC 会员上课日历调用链", "LessonsController.GetUserLessonsScheduling", "日历响应 DTO"],
    },
    "crmapi.store.business_get_store_user_statistical": {
        "capability": "读取会员首页的门店会员统计",
        "purpose": "返回会员首页所需的会员总量、新会员、活跃/沉睡会员和体验人员等服务端统计口径。",
        "whenToUse": "加载会员经营概览或核对当前门店会员分层数量时使用。",
        "doNotUse": "统计结果不能定位具体会员，也不能代替会员列表或详情。",
        "usageEvidence": ["PC 会员概览调用链", "StoreController.BusinessGetStoreUserStatistical", "统计响应 DTO"],
    },

    # 顾客端：按真实页面加载链区分首页聚合、会员账户聚合、单卡、记录和交易详情。
    "capi.card.get_user_card": {
        "capability": "获取当前门店会员账户及名下全部会员卡、余额与有效期",
        "purpose": (
            "顾客端当前门店的会员与持卡聚合入口：返回主会员账户、积分/印章/佣金、门店能力和协议状态，"
            "并在 Cards 中返回名下全部子会员卡的类型、状态、余额或次数、有效期、折扣、服务项目、"
            "核销频次及转赠/用卡限制。"
        ),
        "whenToUse": (
            "进入首页、我的、会员中心、充值/续卡或预约选卡前，需要刷新当前门店会员身份和全部持卡快照时首选；"
            "预约场景传 UsedDatetime，以返回指定用卡时间是否可用。"
        ),
        "doNotUse": "不要用跨门店卡列表或单张子卡详情替代当前门店会员账户聚合；消费历史、预约历史和优惠券另查对应记录接口。",
        "usageEvidence": ["顾客端首页/我的/checkUser 调用链", "CardController.GetUserCard", "会员账户及子卡 DTO"],
    },
    "capi.card.get_user_cards": {
        "capability": "获取顾客跨门店的会员账户与全部持卡列表",
        "purpose": "返回顾客关联的多个门店会员账户及每个账户下的子卡、余额/次数、有效期、状态和门店能力摘要。",
        "whenToUse": "没有确定当前门店、需要展示全部门店卡包或启动回退选择默认门店时使用。",
        "doNotUse": "已确定当前门店时应优先使用 GetUserCard；查看某张子卡完整详情时使用 GetUserChildCard。",
        "usageEvidence": ["顾客端启动回退/卡包调用链", "CardController.GetUserCards", "跨门店卡列表 DTO"],
    },
    "capi.card.get_user_child_card": {
        "capability": "获取顾客名下单张子会员卡完整详情",
        "purpose": "按 ChildCardId 返回单张持有卡的卡名、卡号、类型、状态、余额/次数、有效期、折扣、二维码及服务项目余额。",
        "whenToUse": "已从当前门店会员账户或跨门店卡列表取得子卡引用，需要打开卡详情、卡码、续卡或消费记录入口时使用。",
        "doNotUse": "不能用于发现顾客名下全部卡，也不能替代当前门店会员身份与积分等账户级信息。",
        "usageEvidence": ["顾客端卡管理/卡详情调用链", "CardController.GetUserChildCard", "子卡详情 DTO"],
    },
    "capi.card.get_store_prepaid_cards": {
        "capability": "获取当前门店可购买或续费的卡产品列表",
        "purpose": "返回门店在售充值/会员卡产品及价格、赠送、有效期、折扣、库存和购买限制等商品化规则。",
        "whenToUse": "进入购卡、充值或续卡选择卡产品时使用。",
        "doNotUse": "这是卡产品目录，不表示当前顾客已经持有这些卡；持有卡应查询 GetUserCard。",
        "usageEvidence": ["顾客端充值/购卡调用链", "CardController.GetStorePrepaidCards", "卡产品列表 DTO"],
    },
    "capi.card.get_store_prepaid_card_by_id": {
        "capability": "获取单个在售卡产品及购买规则",
        "purpose": "按卡产品引用返回价格、赠送、有效期、折扣、协议、适用服务与购买限制等详情。",
        "whenToUse": "从购卡列表进入某个卡产品详情或提交购买前复核规则时使用。",
        "doNotUse": "不返回顾客已持有卡的实际余额、状态或有效期。",
        "usageEvidence": ["顾客端购卡详情调用链", "CardController.GetStorePrepaidCardById", "卡产品详情 DTO"],
    },
    "capi.store.get_store_index_data": {
        "capability": "获取顾客端首页模块、菜单数据与当前会员标记",
        "purpose": "按当前门店和顾客上下文聚合首页 Modules、Menus 及 IsVip，决定动态首页模块的数据和导航入口。",
        "whenToUse": "顾客端进入/刷新首页、切换门店或登录状态变化后重建首页模块时使用；IsLoadData 决定是否同时加载模块数据。",
        "doNotUse": "不能单独决定最终页面样式和跳转协议；模板结构需配合 GetTemplate，门店规则需配合门店信息/显示设置。",
        "usageEvidence": ["顾客端首页加载顺序", "StoreController.GetStoreIndexData", "首页模块 DTO"],
    },
    "capi.template.get_template": {
        "capability": "获取顾客端动态页面模板、控件与跳转协议",
        "purpose": "返回页面模板样式、模块层级、Inputs/DataSource、显隐、排序以及 JumpType/JumpUrl 等动态渲染和跳转配置。",
        "whenToUse": "首页已取得门店和模块数据，需要按门店配置渲染最终页面结构或解释某入口为何显示/跳转时使用。",
        "doNotUse": "模板只能证明配置结构，不能替代模块业务数据，也不能保证 JumpUrl 对应能力当前可用。",
        "usageEvidence": ["顾客端动态首页渲染链", "TemplateController.GetTemplate", "模板树 DTO"],
    },
    "capi.store.get_store_info": {
        "capability": "获取当前门店营业、地址、联系方式与支付能力信息",
        "purpose": "返回门店名称、Logo、地址、经纬度、电话、营业/放假时间、营业状态和收款能力等当前门店基础信息。",
        "whenToUse": "进入门店、首页、地图导航、联系门店或支付前需要门店基础状态时使用。",
        "doNotUse": "不返回首页动态模块、模板结构或顾客持卡信息。",
        "usageEvidence": ["顾客端启动/首页门店加载链", "StoreController.GetStoreInfo", "门店信息 DTO"],
    },
    "capi.store.get_store_list": {
        "capability": "获取顾客可访问的门店列表与切店信息",
        "purpose": "返回顾客关联或可进入的门店列表、门店状态、地址、联系方式和权限摘要。",
        "whenToUse": "启动时没有唯一门店、顾客拥有多个门店关系或需要展示切换门店入口时使用。",
        "doNotUse": "不能替代当前选中门店的完整信息、首页模块或模板。",
        "usageEvidence": ["顾客端启动/首页切店调用链", "StoreController.GetStoreList", "门店列表 DTO"],
    },
    "capi.store.get_store_display_info": {
        "capability": "获取顾客端门店展示与约课可见性设置",
        "purpose": "返回门店介绍、联系展示、环境照片、排行开关、团课/私教开关和 LessonsShowType 等展示规则。",
        "whenToUse": "首页或我的加载后，需要决定课程、排行、门店介绍等模块是否展示以及非会员能否看课时使用。",
        "doNotUse": "显隐设置不是实时课表、预约资格或会员余额；最终预约仍以对应接口校验为准。",
        "usageEvidence": ["顾客端首页/我的显隐调用链", "StoreController.GetStoreDisplayInfo", "显示设置 DTO"],
    },
    "capi.store.get_store_vacation": {
        "capability": "获取门店公告、放假区间及会员卡顺延规则",
        "purpose": "返回当前和后续放假/公告、起止时间、弹窗状态，以及适用卡类型和顺延天数。",
        "whenToUse": "进入或刷新首页、约课日历前需要展示公告或解释放假期间课程/卡有效期影响时使用。",
        "doNotUse": "不能仅凭公告推断某一课次已取消或某张卡已完成延期；需再查课次或持卡当前状态。",
        "usageEvidence": ["顾客端首页公告加载链", "StoreController.GetStoreVacation", "放假响应 DTO"],
    },
    "capi.user.get_store_controls": {
        "capability": "获取顾客注册/完善资料所需的动态字段规则与当前值",
        "purpose": "返回手机号、门店自定义资料控件、必填/显隐、校验公式、选项及当前用户值。",
        "whenToUse": "顾客注册、授权后资料完整性检查或进入资料完善页面时使用。",
        "doNotUse": "不用于展示已确定会员的持卡、余额或会员详情；字段保存需调用写接口。",
        "usageEvidence": ["顾客端 checkUser/注册调用链", "UserController.GetStoreControls", "动态控件 DTO"],
    },
    "capi.user.get_store_user_info": {
        "capability": "加载顾客当前门店会员资料及可编辑动态字段",
        "purpose": "返回会员昵称、头像、手机号，以及门店自定义字段的当前值、必填/显隐、校验和选项。",
        "whenToUse": "已建立当前门店会员关系，进入会员资料查看或编辑页面，需要回填现有资料时使用。",
        "doNotUse": "不返回会员名下全部卡、余额或有效期；持卡信息使用 GetUserCard。",
        "usageEvidence": ["顾客端会员资料页调用链", "UserController.GetStoreUserInfo", "资料响应 DTO"],
    },
    "capi.user.user_vip_info": {
        "capability": "获取顾客在当前门店的会员关系状态",
        "purpose": "返回顾客昵称、头像、备注、最后操作信息及非会员、会员、待授权、已删除等关系状态。",
        "whenToUse": "只需要确认当前门店会员关系或授权状态，而不需要加载全部持卡明细时使用。",
        "doNotUse": "不能据此判断某张卡的余额、有效期或可用性。",
        "usageEvidence": ["顾客端会员身份判断", "UserController.UserVipInfo", "会员状态 DTO"],
    },
    "capi.reservation.get_group_course_week_list_v2": {
        "capability": "获取顾客端团课/班课周课表及个人预约状态",
        "purpose": "按周、课程类型和筛选条件返回课次时间、教练/容量、价格、可约/候补状态及当前顾客预约状态。",
        "whenToUse": "约课主页面以周视图加载团课或班课、切周/分类/教练筛选时使用。",
        "doNotUse": "课表可见和 IsCanReservation 不是最终提交成功证明；预约提交前仍需服务端预检与正式校验。",
        "usageEvidence": ["顾客端约课周视图调用链", "ReservationController.GetGroupCourseWeekListV2", "课表响应 DTO"],
    },
    "capi.reservation.get_group_course_list_v2": {
        "capability": "获取顾客端团课/班课日期列表",
        "purpose": "按日期范围返回课次、容量、价格、可约/候补状态和当前顾客预约状态。",
        "whenToUse": "约课主页面使用列表模式、按日期或分类刷新课程时使用。",
        "doNotUse": "不替代课次详情或预约提交校验。",
        "usageEvidence": ["顾客端约课列表调用链", "ReservationController.GetGroupCourseListV2", "课程列表 DTO"],
    },
    "capi.reservation.get_group_course_list_v3": {
        "capability": "分页获取顾客端团课详情列表",
        "purpose": "分页返回团课课次、课程信息、时间、容量、价格和个人预约状态。",
        "whenToUse": "课程详情或需要服务端分页的团课列表场景使用。",
        "doNotUse": "不用于周课表整体展示，也不执行预约。",
        "usageEvidence": ["顾客端团课详情列表调用链", "ReservationController.GetGroupCourseListV3", "分页课程 DTO"],
    },
    "capi.reservation.get_lessons_reservation_calender_v2": {
        "capability": "获取团课/私教日历的可预约日期与不可约原因",
        "purpose": "按日期范围、课程、教练和课程类型返回每天是否可约及休息、放假、请假、无课或尚未开放等原因。",
        "whenToUse": "约课页面先加载月份日期状态，或切换课程/教练后刷新可约日历时使用。",
        "doNotUse": "日期可约不代表具体时间段仍有名额；私教还需查询教练和时间段。",
        "usageEvidence": ["顾客端私教/课程日历调用链", "ReservationController.GetLessonsReservationCalenderV2", "日历 DTO"],
    },
    "capi.reservation.get_private_staff": {
        "capability": "获取顾客端可预约私教及其可选课程",
        "purpose": "返回当前门店可约教练、教练资料、是否必须选课程及其关联私教课程。",
        "whenToUse": "私教预约选择教练，或门店规则要求先按教练选择课程时使用。",
        "doNotUse": "教练存在不代表指定日期时间可约；需继续查询日历和时间段。",
        "usageEvidence": ["顾客端私教预约调用链", "ReservationController.GetPrivateStaff", "私教列表 DTO"],
    },
    "capi.reservation.get_private_lessons_reservation_time_seting": {
        "capability": "获取指定私教、课程和日期的可预约时间段",
        "purpose": "返回每个起止时间段、是否可约、是否占用及剩余可预约人数。",
        "whenToUse": "已选择私教/课程和预约日期，需要展示最终可选时间段时使用。",
        "doNotUse": "时间段结果是查询时快照，不等于已锁定名额；提交预约仍需重新校验。",
        "usageEvidence": ["顾客端私教时间选择调用链", "ReservationController.GetPrivateLessonsReservationTimeSeting", "时间段 DTO"],
    },
    "capi.reservation.get_store_reservation_seting": {
        "capability": "获取顾客端预约、支付顺序、取消处罚与展示规则",
        "purpose": "返回预约支付/签到设置、可约天数、取消次数处罚、私教归属、人数和头像/名额显示等门店规则。",
        "whenToUse": "进入约课或发起预约前，需要决定页面显隐、取消限制、支付阶段和人数规则时使用。",
        "doNotUse": "配置不能替代目标课次、会员卡、余额、黑名单和冲突等实时资格校验。",
        "usageEvidence": ["顾客端约课初始化调用链", "ReservationController.GetStoreReservationSeting", "预约设置 DTO"],
    },
    "capi.reservation.get_reservation_by_id": {
        "capability": "获取顾客单条预约详情及可取消状态",
        "purpose": "按预约引用返回预约日期/时间、人数、留言、自定义字段、当前状态和是否允许取消。",
        "whenToUse": "从预约记录、深链或课程页面打开某一条预约详情时使用。",
        "doNotUse": "不用于列出全部预约，也不执行取消、签到或支付。",
        "usageEvidence": ["顾客端预约详情调用链", "ReservationController.GetReservationById", "预约详情 DTO"],
    },
    "capi.lessons.get_user_lessons_reservation_list": {
        "capability": "分页获取顾客预约、候补、签到与上课记录",
        "purpose": "按会员卡、日期和状态分页返回顾客的课程、教练、预约时间、签到和预约生命周期状态。",
        "whenToUse": "我的预约、上课记录或按状态查看待上课/已完成/已取消记录时使用。",
        "doNotUse": "单条预约完整内容需查询预约/个人预约详情；本接口不改变预约状态。",
        "usageEvidence": ["顾客端预约记录调用链", "LessonsController.GetUserLessonsReservationList", "预约记录 DTO"],
    },
    "capi.lessons.get_lessons_statistics": {
        "capability": "获取顾客上课累计、本月分类、排行、待上课和旷课统计",
        "purpose": "按月份返回累计上课、本月团课/私教、月排行、待上课和累计旷课数量。",
        "whenToUse": "顾客端“我的”头部或课程统计页加载汇总指标时使用。",
        "doNotUse": "统计不能证明某一条预约或课程状态；明细需查询预约记录。",
        "usageEvidence": ["顾客端我的/课程统计调用链", "LessonsController.GetLessonsStatistics", "统计响应 DTO"],
    },
    "capi.consumption.get_user_consumption_list": {
        "capability": "分页获取顾客消费、充值及会员卡资产变动记录",
        "purpose": "按会员主卡分页返回消费、充值、核减、返还、赠送、积分、优惠券、有效期和停复卡等记录及操作后值。",
        "whenToUse": "顾客进入消费记录/充值记录，或需要核对余额、次数、积分为何变化时使用。",
        "doNotUse": "不能替代当前持卡余额快照；单笔商品、服务、支付和退款详情需查询消费详情。",
        "usageEvidence": ["顾客端消费/充值记录调用链", "ConsumptionController.GetUserConsumptionList", "分页流水 DTO"],
    },
    "capi.consumption.get_user_consumption_info": {
        "capability": "获取顾客单笔消费、充值或支付单据详情",
        "purpose": "返回单笔记录的门店、支付方式、卡类型、资产变化、操作人员及关联服务/商品等明细。",
        "whenToUse": "已从消费记录、订单或深链取得单据引用，需要查看某一笔交易组成和结果时使用。",
        "doNotUse": "不用于列出全部记录或读取当前卡余额，也不执行退款。",
        "usageEvidence": ["顾客端消费详情调用链", "ConsumptionController.GetUserConsumptionInfo", "消费详情 DTO"],
    },
    "capi.coupon.get_user_coupon_list": {
        "capability": "获取顾客优惠券列表及当前场景使用条件",
        "purpose": "按门店、状态和使用场景返回顾客优惠券、券类型、面值/折扣、有效期、门槛和适用范围。",
        "whenToUse": "进入券包，或预约、商城、点餐、购卡结算前选择可用优惠券时使用。",
        "doNotUse": "列表中的可见券不等于最终可用；多券组合和实付金额需调用可用性校验接口。",
        "usageEvidence": ["顾客端券包/结算调用链", "CouponController.GetUserCouponList", "优惠券列表 DTO"],
    },
    "capi.coupon.get_user_coupon": {
        "capability": "获取顾客单张优惠券的完整规则与当前状态",
        "purpose": "按券引用返回券类型、面值/折扣、有效期、最低消费、适用服务、频次、审核要求、当前状态和不可用原因。",
        "whenToUse": "从券包、领券活动或结算页打开单张券详情，或需要解释该券为什么不可用时使用。",
        "doNotUse": "不用于列出全部优惠券，也不执行领券或核销。",
        "usageEvidence": ["顾客端优惠券详情调用链", "CouponController.GetUserCoupon", "优惠券详情 DTO"],
    },
    "capi.coupon.get_user_coupon_count": {
        "capability": "获取顾客当前可用优惠券数量",
        "purpose": "返回当前门店上下文中的可用优惠券数量，用于角标或入口提示。",
        "whenToUse": "首页、我的或券包入口只需刷新可用券角标时使用。",
        "doNotUse": "数量不能说明具体券、适用场景或不可用原因；详情需查询券列表或单券。",
        "usageEvidence": ["顾客端优惠券角标调用链", "CouponController.GetUserCouponCount", "优惠券数量 DTO"],
    },
    "capi.coupon.check_user_coupon_used": {
        "capability": "校验所选优惠券组合并计算优惠后实付金额",
        "purpose": "根据当前消费金额和已选优惠券返回是否可用、不可用原因、组合限制及优惠后金额。",
        "whenToUse": "结算页已经选择优惠券，需要在提交订单或支付前进行最终券规则预校验时使用。",
        "doNotUse": "校验成功不等于优惠券已核销或订单已支付。",
        "usageEvidence": ["顾客端结算用券调用链", "CouponController.CheckUserCouponUsed", "用券校验 DTO"],
    },
    "capi.shopping_mall.get_products_list_by_store_id": {
        "capability": "按分类获取顾客端商城商品列表、价格与库存摘要",
        "purpose": "返回门店分类下商品、图片、普通价/会员价、库存、销量、标签、上下架和规格摘要。",
        "whenToUse": "商城首页或切换商品分类时使用。",
        "doNotUse": "列表价格和库存是查询快照；下单前需读取商品详情并由服务端重算。",
        "usageEvidence": ["顾客端商城列表调用链", "ShoppingMallController.GetProductsListByStoreId", "商品列表 DTO"],
    },
    "capi.shopping_mall.get_business_products_message_by_product_id": {
        "capability": "获取顾客端单个商城商品、规格、价格与配送要求详情",
        "purpose": "返回商品图片、描述、价格/会员价、库存、兑换积分、规格属性和是否需要配送。",
        "whenToUse": "从商城列表、搜索或深链打开商品详情，选择规格或加入购物车前使用。",
        "doNotUse": "查询结果不锁库存、不创建订单，也不能替代结算时服务端价格校验。",
        "usageEvidence": ["顾客端商品详情调用链", "ShoppingMallController.GetBusinessProductsMessageByProductId", "商品详情 DTO"],
    },
    "capi.shopping_cart.get_shopping_cart": {
        "capability": "获取顾客商城购物车、有效商品与结算金额",
        "purpose": "返回购物车商品、规格、数量、价格、库存、失效原因、配送要求、会员折扣和合计。",
        "whenToUse": "进入购物车、商品数量变化后刷新或提交商城结算前使用。",
        "doNotUse": "购物车合计不是最终订单金额，也不表示库存已锁定。",
        "usageEvidence": ["顾客端商城购物车调用链", "ShoppingCartController.GetShoppingCart", "购物车 DTO"],
    },
    "capi.shop_order.get_all_shop_orders": {
        "capability": "分页获取顾客商城订单列表与履约状态",
        "purpose": "返回顾客商城订单的金额、支付/订单状态、配送或自提方式、商品摘要和下单时间。",
        "whenToUse": "顾客查看全部或按状态筛选商城订单时使用。",
        "doNotUse": "列表摘要不能替代单笔订单详情或支付回调最终状态。",
        "usageEvidence": ["顾客端商城订单列表调用链", "ShopOrderController.GetAllShopOrders", "订单列表 DTO"],
    },
    "capi.shop_order.get_shop_order_detail": {
        "capability": "获取顾客单笔商城订单、收货与履约详情",
        "purpose": "返回订单金额、支付/退款/履约状态、商品、配送/自提、收货和物流等详情。",
        "whenToUse": "从订单列表或支付结果页打开单笔商城订单时使用。",
        "doNotUse": "不执行取消、退款、发货或确认收货；支付面板成功也不能替代服务端订单状态。",
        "usageEvidence": ["顾客端商城订单详情调用链", "ShopOrderController.GetShopOrderDetail", "订单详情 DTO"],
    },
    "capi.food.get_food_list_to_c": {
        "capability": "获取顾客端点餐分类、菜品、会员价与库存列表",
        "purpose": "按分类返回菜品名称、图片、价格/会员价、库存、销量、上下架、多规格和购物车数量。",
        "whenToUse": "顾客进入点餐首页或切换菜品分类时使用。",
        "doNotUse": "列表摘要不能替代菜品规格详情，也不锁定库存。",
        "usageEvidence": ["顾客端点餐首页调用链", "FoodController.GetFoodListToC", "菜品列表 DTO"],
    },
    "capi.food.get_food_inforation_to_c": {
        "capability": "获取顾客端单个菜品、规格、库存与会员价详情",
        "purpose": "返回菜品图片、说明、普通价/会员价、库存、分类/标签以及单选或多选规格及规格价格。",
        "whenToUse": "从点餐列表或分享深链打开菜品详情、选择规格或加入购物车前使用。",
        "doNotUse": "查询结果不创建购物车或订单，提交时仍需服务端重算价格和库存。",
        "usageEvidence": ["顾客端菜品详情调用链", "FoodController.GetFoodInforationToC", "菜品详情 DTO"],
    },
    "capi.food.get_food_cart": {
        "capability": "获取顾客当前桌台/门店点餐购物车与结算摘要",
        "purpose": "返回购物车菜品、规格、数量、会员折扣、合计以及多人点餐参与者等当前快照。",
        "whenToUse": "进入点餐购物车、桌台或菜品数量变化后刷新，以及提交点餐订单前使用。",
        "doNotUse": "购物车合计不是最终支付结果，也不表示菜品库存已锁定。",
        "usageEvidence": ["顾客端点餐购物车调用链", "FoodController.GetFoodCart", "点餐购物车 DTO"],
    },
    "capi.food.get_food_order_list": {
        "capability": "分页获取顾客点餐订单与出餐/配送状态",
        "purpose": "按当前、历史或全部口径返回点餐订单金额、菜品、桌台、堂食/外卖/自取、出餐配送和退款状态。",
        "whenToUse": "顾客查看点餐订单列表或按订单状态筛选时使用。",
        "doNotUse": "列表摘要不能替代单笔订单详情，也不能据支付前端回调推断最终入账。",
        "usageEvidence": ["顾客端点餐订单列表调用链", "FoodController.GetFoodOrderList", "点餐订单列表 DTO"],
    },
    "capi.food.get_food_order_detail": {
        "capability": "获取顾客单笔点餐订单、支付、出餐配送与退款详情",
        "purpose": "返回单笔点餐订单的菜品、金额、支付方式、优惠拆分、桌台/取餐、配送、退款和当前状态。",
        "whenToUse": "从点餐订单列表、待支付或支付结果页打开具体订单时使用。",
        "doNotUse": "不执行支付、退款、出餐或配送状态修改。",
        "usageEvidence": ["顾客端点餐订单详情调用链", "FoodController.GetFoodOrderDetail", "点餐订单详情 DTO"],
    },
    "capi.store_item.get_service_list": {
        "capability": "获取顾客端可购买服务项目、会员价与上下架列表",
        "purpose": "按分类返回服务名称、图片、原价/会员价、销量、卡折扣资格和当前上下架状态。",
        "whenToUse": "顾客进入服务项目商城或切换服务分类时使用。",
        "doNotUse": "列表不表示顾客已购买服务，也不创建服务订单。",
        "usageEvidence": ["顾客端服务项目商城调用链", "StoreItemController.GetServiceList", "服务列表 DTO"],
    },
    "capi.store_item.get_service_cart": {
        "capability": "获取顾客服务项目购物车与会员折扣合计",
        "purpose": "返回服务项目、数量、原价/会员价、卡折扣资格、会员折扣和购物车总价。",
        "whenToUse": "进入服务购物车或提交服务结算前刷新时使用。",
        "doNotUse": "购物车金额不是最终支付结果，也不代表订单已创建。",
        "usageEvidence": ["顾客端服务购物车调用链", "StoreItemController.GetServiceCart", "服务购物车 DTO"],
    },
    "capi.store_item.get_service_order_info": {
        "capability": "获取顾客单笔服务项目订单与优惠拆分详情",
        "purpose": "返回服务订单的项目、数量、总金额、实付、支付方式以及积分、会员卡和优惠券抵扣。",
        "whenToUse": "服务结算完成或从订单入口打开单笔服务订单时使用。",
        "doNotUse": "不执行支付、退款或服务核销。",
        "usageEvidence": ["顾客端服务订单详情调用链", "StoreItemController.GetServiceOrderInfo", "服务订单 DTO"],
    },
    "capi.reservation.get_reservation_list": {
        "capability": "分页获取顾客通用预约记录",
        "purpose": "按日期范围分页返回预约时间、技师、服务项目、场地、留言和当前预约状态。",
        "whenToUse": "顾客查看非课程型或旧预约体系的预约记录列表时使用。",
        "doNotUse": "课程型预约记录优先使用会员课程预约列表；单条详情使用 GetReservationById。",
        "usageEvidence": ["顾客端通用预约记录调用链", "ReservationController.GetReservationList", "预约列表 DTO"],
    },
    "capi.order.order_get_list": {
        "capability": "分页获取顾客旧版商品订单列表",
        "purpose": "返回旧订单体系的商品、金额、收件信息、支付方式和未付款/已付款/已发货/完成/取消状态。",
        "whenToUse": "只有前端进入仍使用 OrderController 的历史兼容订单页面时使用。",
        "doNotUse": "当前商城订单优先使用 ShopOrder 接口；不能把两套订单状态或主键混用。",
        "usageEvidence": ["顾客端历史订单调用链", "OrderController.OrderGetList", "旧订单列表 DTO"],
    },
    "capi.order.order_get": {
        "capability": "获取顾客旧版单笔商品订单详情",
        "purpose": "返回旧订单体系的商品、金额、收货地址、支付、物流和订单状态。",
        "whenToUse": "已确认来源为旧版 OrderController 列表或历史深链，并取得对应 Tid 时使用。",
        "doNotUse": "不能用旧订单详情读取 ShopOrder 或点餐订单，也不执行订单状态修改。",
        "usageEvidence": ["顾客端历史订单详情调用链", "OrderController.OrderGet", "旧订单详情 DTO"],
    },
    "capi.integral.get_integral_summary": {
        "capability": "获取顾客当前积分余额与汇总",
        "purpose": "返回当前会员积分账户的余额和汇总口径。",
        "whenToUse": "进入积分页或只需确认当前积分余额时使用。",
        "doNotUse": "不解释每次积分增减；变化过程需查询积分明细。",
        "usageEvidence": ["顾客端积分页调用链", "IntegralController.GetIntegralSummary", "积分汇总 DTO"],
    },
    "capi.integral.get_integral_detail": {
        "capability": "分页获取顾客积分增减明细",
        "purpose": "返回积分获取、消费、过期等逐笔记录及时间和变动值。",
        "whenToUse": "顾客需要核对积分为何增加、扣减或过期时使用。",
        "doNotUse": "不替代当前积分余额汇总，也不执行积分调整。",
        "usageEvidence": ["顾客端积分明细调用链", "IntegralController.GetIntegralDetail", "积分明细 DTO"],
    },
}


@dataclass
class PropertyDef:
    """请求或响应 DTO 的单个公开属性。"""

    name: str
    type_name: str
    summary: str
    required_attribute: bool
    range_minimum: float | int | None
    range_maximum: float | int | None
    default: str
    source_file: str
    line: int


@dataclass
class TypeDef:
    """源码中一个可用于请求/响应契约的类型。"""

    name: str
    bases: list[str]
    properties: list[PropertyDef]
    summary: str
    source_file: str
    line: int
    namespace: str
    using_namespaces: list[str]


@dataclass
class ParameterDef:
    """Controller Action 的形参。"""

    name: str
    type_name: str
    binding: str
    default: str


@dataclass
class ActionDef:
    """一个实际带 Http 特性的 Controller Action。"""

    project_key: str
    perspective: str
    controller: str
    controller_base: str
    action: str
    http_method: str
    route: str
    return_type: str
    parameters: list[ParameterDef]
    summary: str
    attributes: str
    body: str
    source_file: str
    line: int
    using_namespaces: list[str] = field(default_factory=list)
    validations: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    grade: str = "D"
    grade_reason: str = ""
    id_suffix: str = ""

    @property
    def tool_id(self) -> str:
        """生成与路由解耦、适合后续工具注册的稳定编号。"""

        base = f"{self.project_key}.{to_snake(self.controller)}.{to_snake(self.action)}"
        return f"{base}.{self.id_suffix}" if self.id_suffix else base

    @property
    def authenticated(self) -> bool:
        return "NoAuth" not in self.controller_base


def to_snake(value: str) -> str:
    """把 PascalCase/camelCase 名称转换为稳定的小写工具标识。"""

    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()


def identifier_tokens(value: str) -> list[str]:
    """按属性最后一段拆分 CamelCase，避免 Keyword、PrivateLessons 等子串误判为密钥或电话。"""

    leaf = re.split(r"[.\[\]]+", value)[-1]
    return [item.lower() for item in re.findall(r"[A-Z]+(?=[A-Z][a-z]|\b)|[A-Z]?[a-z]+|\d+", leaf)]


def is_sensitive_name(value: str) -> bool:
    """识别个人信息字段；只按完整语义词判断，不做危险的任意子串匹配。"""

    compact = "".join(identifier_tokens(value))
    exact_or_suffix = (
        "mobile", "phone", "tel", "address", "receiver", "receivername", "receivermobile",
        "idcard", "identity", "realname", "username", "nickname", "openid", "unionid",
        "externaluserid", "email", "cardnumber", "controlvalue", "remark", "remarkname",
        "userimg", "avatar",
    )
    return compact in exact_or_suffix or any(compact.endswith(item) for item in exact_or_suffix)


def is_secret_name(value: str) -> bool:
    """识别真正的凭据字段；KeyWord、SignAgreement 等普通业务词不能误判。"""

    compact = "".join(identifier_tokens(value))
    exact_or_suffix = (
        "password", "pwd", "token", "secret", "secretkey", "apikey", "accesskey", "privatekey",
        "encryptkey", "randomparam", "signature", "cipher", "credential", "sign",
    )
    return compact in exact_or_suffix or any(compact.endswith(item) for item in exact_or_suffix[:-1])


def clean_type(value: str) -> str:
    """压缩 C# 类型中的无意义空白，但保留泛型结构。"""

    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s*([<>,\[\]\?])\s*", r"\1", value)
    return value


def mask_comments(text: str) -> str:
    """用空格遮盖注释并保持字符位置，避免把注释中的旧接口识别为有效 Action。"""

    chars = list(text)
    index = 0
    state = "code"
    while index < len(chars):
        current = chars[index]
        following = chars[index + 1] if index + 1 < len(chars) else ""
        if state == "code":
            if current == '"':
                state = "string"
            elif current == "'":
                state = "char"
            elif current == "/" and following == "/":
                chars[index] = chars[index + 1] = " "
                index += 1
                state = "line_comment"
            elif current == "/" and following == "*":
                chars[index] = chars[index + 1] = " "
                index += 1
                state = "block_comment"
        elif state == "string":
            if current == "\\":
                index += 1
            elif current == '"':
                state = "code"
        elif state == "char":
            if current == "\\":
                index += 1
            elif current == "'":
                state = "code"
        elif state == "line_comment":
            if current == "\n":
                state = "code"
            else:
                chars[index] = " "
        elif state == "block_comment":
            if current == "*" and following == "/":
                chars[index] = chars[index + 1] = " "
                index += 1
                state = "code"
            elif current != "\n":
                chars[index] = " "
        index += 1
    return "".join(chars)


def find_matching(text: str, start: int, opening: str, closing: str) -> int:
    """在已遮盖注释的源码中查找与起始符号配对的结束位置。"""

    if start < 0 or start >= len(text) or text[start] != opening:
        return -1
    depth = 0
    state = "code"
    index = start
    while index < len(text):
        current = text[index]
        if state == "code":
            if current == '"':
                state = "string"
            elif current == "'":
                state = "char"
            elif current == opening:
                depth += 1
            elif current == closing:
                depth -= 1
                if depth == 0:
                    return index
        elif state == "string":
            if current == "\\":
                index += 1
            elif current == '"':
                state = "code"
        elif state == "char":
            if current == "\\":
                index += 1
            elif current == "'":
                state = "code"
        index += 1
    return -1


def brace_depth(text: str, position: int) -> int:
    """计算片段指定位置前的花括号深度，用于排除嵌套类和方法体内匹配。"""

    depth = 0
    for char in text[:position]:
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
    return depth


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, max(position, 0)) + 1


def xml_summary_before(raw: str, position: int) -> str:
    """读取声明前连续的 XML 文档注释；允许中间存在特性行。"""

    prefix = raw[:position]
    lines = prefix.splitlines()
    collected: list[str] = []
    index = len(lines) - 1
    while index >= 0:
        stripped = lines[index].strip()
        if not stripped:
            if collected:
                break
            index -= 1
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            index -= 1
            continue
        if stripped.startswith("///"):
            collected.append(stripped[3:].strip())
            index -= 1
            continue
        break
    collected.reverse()
    xml = " ".join(collected)
    match = re.search(r"<summary>\s*(.*?)\s*</summary>", xml, re.S | re.I)
    if match:
        xml = match.group(1)
    xml = re.sub(r"<[^>]+>", " ", xml)
    return re.sub(r"\s+", " ", xml).strip()


def split_top_level(value: str, delimiter: str = ",") -> list[str]:
    """按顶层分隔符拆分泛型或参数列表。"""

    result: list[str] = []
    depth_angle = depth_round = depth_square = 0
    start = 0
    for index, char in enumerate(value):
        if char == "<":
            depth_angle += 1
        elif char == ">":
            depth_angle = max(0, depth_angle - 1)
        elif char == "(":
            depth_round += 1
        elif char == ")":
            depth_round = max(0, depth_round - 1)
        elif char == "[":
            depth_square += 1
        elif char == "]":
            depth_square = max(0, depth_square - 1)
        elif char == delimiter and depth_angle == depth_round == depth_square == 0:
            result.append(value[start:index].strip())
            start = index + 1
    result.append(value[start:].strip())
    return [item for item in result if item]


def parse_generic(value: str) -> tuple[str, list[str]]:
    """返回泛型根类型和顶层泛型参数。"""

    value = clean_type(value).rstrip("?")
    if value.endswith("[]"):
        return "Array", [value[:-2]]
    start = value.find("<")
    if start < 0 or not value.endswith(">"):
        return value.split(".")[-1], []
    root = value[:start].split(".")[-1]
    return root, split_top_level(value[start + 1:-1])


def unwrap_return_type(value: str) -> tuple[str, str]:
    """拆出常见 Task/ActionResult/DataResult 包装及实际 Data 类型。"""

    wrappers: list[str] = []
    current = clean_type(value)
    while True:
        root, args = parse_generic(current)
        if root in {"Task", "ValueTask", "ActionResult", "ObjectResult"} and args:
            wrappers.append(root)
            current = args[0]
            continue
        if root in {"DataResult", "DataList", "PosDataResult"} and args:
            wrappers.append(root)
            return "/".join(wrappers), args[0]
        return "/".join(wrappers), current


def escape_cell(value: str, limit: int = 360) -> str:
    """把源码摘要安全压缩为 Markdown 表格单元格。"""

    value = re.sub(r"\s+", " ", value or "").strip().replace("|", "\\|")
    value = value.replace("`", "'")
    if len(value) > limit:
        return value[: limit - 1] + "…"
    return value or "—"


def normalize_condition(value: str) -> str:
    """压缩代码校验条件，并避免向目录写入过长实现。"""

    return escape_cell(value, 260)


def normalize_machine_condition(value: str) -> str:
    """压缩机器目录中的代码条件，不加入 Markdown 转义字符。"""

    normalized = re.sub(r"\s+", " ", value or "").strip()
    return normalized[:259] + "…" if len(normalized) > 260 else normalized


class ModelCatalog:
    """从当前项目实际引用的 Libraries/LingKeModel 构建 DTO 索引。"""

    def __init__(self, repo_root: Path, source_roots: list[Path]) -> None:
        self.repo_root = repo_root
        self.source_roots = list(source_roots)
        self.types: dict[str, list[TypeDef]] = {}
        for root in source_roots:
            for path in sorted(root.rglob("*.cs")):
                self._read_file(path)

    def _read_file(self, path: Path) -> None:
        raw = path.read_text(encoding="utf-8-sig", errors="replace")
        clean = mask_comments(raw)
        namespace_match = NAMESPACE_RE.search(clean)
        namespace = namespace_match.group("name") if namespace_match else ""
        using_namespaces = [match.group("name") for match in USING_RE.finditer(clean)]
        for class_match in CLASS_RE.finditer(clean):
            open_brace = clean.find("{", class_match.start())
            close_brace = find_matching(clean, open_brace, "{", "}")
            if close_brace < 0:
                continue
            body = clean[open_brace + 1:close_brace]
            raw_body = raw[open_brace + 1:close_brace]
            properties: list[PropertyDef] = []
            for prop_match in PROPERTY_RE.finditer(body):
                if brace_depth(body, prop_match.start()) != 0:
                    continue
                absolute = open_brace + 1 + prop_match.start()
                attrs = prop_match.group("attrs") or ""
                range_match = re.search(
                    r"\bRange\s*\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)",
                    attrs,
                )
                def parse_range_value(value: str) -> float | int:
                    parsed = float(value)
                    return int(parsed) if parsed.is_integer() else parsed
                properties.append(
                    PropertyDef(
                        name=prop_match.group("name"),
                        type_name=clean_type(prop_match.group("type")),
                        summary=xml_summary_before(raw, absolute),
                        required_attribute="Required" in attrs,
                        range_minimum=parse_range_value(range_match.group(1)) if range_match else None,
                        range_maximum=parse_range_value(range_match.group(2)) if range_match else None,
                        default=clean_type(prop_match.group("default") or ""),
                        source_file=str(path.relative_to(self.repo_root)),
                        line=line_number(raw, absolute),
                    )
                )
            bases = []
            if class_match.group("bases"):
                bases = [clean_type(item).split("<", 1)[0].split(".")[-1]
                         for item in split_top_level(class_match.group("bases"))]
            item = TypeDef(
                name=class_match.group("name"),
                bases=bases,
                properties=properties,
                summary=xml_summary_before(raw, class_match.start()),
                source_file=str(path.relative_to(self.repo_root)),
                line=line_number(raw, class_match.start()),
                namespace=namespace,
                using_namespaces=using_namespaces,
            )
            self.types.setdefault(item.name, []).append(item)

    def resolve(self, type_name: str, preferred_namespaces: Iterable[str] = ()) -> TypeDef | None:
        """解析 DTO；同名类型优先匹配 Controller/DTO 文件实际 using 的命名空间。"""

        root, args = parse_generic(type_name)
        if root in GENERIC_COLLECTIONS and args:
            return self.resolve(args[0], preferred_namespaces)
        name = root if args else clean_type(type_name).rstrip("?").split(".")[-1]
        candidates = self.types.get(name, [])
        if not candidates:
            return None
        explicit_type = clean_type(type_name).rstrip("?")
        explicit_namespace = explicit_type.rsplit(".", 1)[0] if "." in explicit_type and "<" not in explicit_type else ""
        preferred = list(dict.fromkeys(filter(None, [explicit_namespace, *preferred_namespaces])))
        candidates = sorted(candidates, key=lambda item: (
            preferred.index(item.namespace) if item.namespace in preferred else len(preferred),
            0 if item.source_file.startswith("Libraries/LingKeModel/") else 1,
            item.source_file,
        ))
        return candidates[0]

    def all_properties(
        self,
        type_name: str,
        preferred_namespaces: Iterable[str] = (),
        seen: set[str] | None = None,
    ) -> list[PropertyDef]:
        """递归合并继承链属性，保证 Uid/StoreId 等共享字段不会遗漏。"""

        seen = seen or set()
        item = self.resolve(type_name, preferred_namespaces)
        identity = f"{item.namespace}.{item.name}" if item is not None else ""
        if item is None or identity in seen:
            return []
        seen.add(identity)
        nested_preferences = list(dict.fromkeys(filter(None, [
            item.namespace,
            *item.using_namespaces,
            *preferred_namespaces,
        ])))
        result: list[PropertyDef] = []
        for base in item.bases:
            result.extend(self.all_properties(base, nested_preferences, seen))
        names = {prop.name for prop in result}
        for prop in item.properties:
            if prop.name not in names:
                result.append(prop)
                names.add(prop.name)
        return result

    def flatten(
        self,
        type_name: str,
        max_depth: int = 3,
        preferred_namespaces: Iterable[str] = (),
    ) -> list[tuple[str, PropertyDef]]:
        """展开响应 DTO；集合用 [] 标识，深度受限以避免循环模型无限展开。"""

        rows: list[tuple[str, PropertyDef]] = []

        initial_preferences = tuple(preferred_namespaces)

        def visit(
            current_type: str,
            prefix: str,
            depth: int,
            seen: tuple[str, ...],
            preferences: tuple[str, ...],
        ) -> None:
            root, args = parse_generic(current_type)
            if root in GENERIC_COLLECTIONS and args:
                visit(args[0], prefix + "[]", depth, seen, preferences)
                return
            if root == "PageData" and args:
                # PageData<T> 的泛型属性无法仅靠简单类名替换 T，这里按公共源码契约显式展开。
                wrapper_source = "Libraries/LingKeModel/DataListResult.cs"
                for name, prop_type, summary in (
                    ("PageSize", "int", "每页数量"),
                    ("PageIndex", "int", "当前页"),
                    ("PageCount", "int", "总页数"),
                    ("TotalCount", "int", "数据总数量"),
                    ("IsNext", "bool", "是否有下页"),
                ):
                    rows.append((
                        f"{prefix}.{name}" if prefix else name,
                        PropertyDef(name, prop_type, summary, False, None, None, "", wrapper_source, 62),
                    ))
                data_path = f"{prefix}.Data[]" if prefix else "Data[]"
                rows.append((
                    data_path,
                    PropertyDef("Data", f"List<{args[0]}>", "数据集合", False, None, None, "", wrapper_source, 62),
                ))
                visit(args[0], data_path, depth + 1, seen, preferences)
                return
            item = self.resolve(current_type, preferences)
            identity = f"{item.namespace}.{item.name}" if item is not None else ""
            if item is None or depth > max_depth or identity in seen:
                return
            next_seen = seen + (identity,)
            next_preferences = tuple(dict.fromkeys(filter(None, [
                item.namespace,
                *item.using_namespaces,
                *preferences,
            ])))
            for prop in self.all_properties(item.name, next_preferences):
                path = f"{prefix}.{prop.name}" if prefix else prop.name
                rows.append((path, prop))
                prop_root, prop_args = parse_generic(prop.type_name)
                nested = prop_args[0] if prop_root in GENERIC_COLLECTIONS and prop_args else prop.type_name
                nested_item = self.resolve(nested, next_preferences)
                if nested_item is not None and depth < max_depth:
                    nested_prefix = path + ("[]" if prop_root in GENERIC_COLLECTIONS else "")
                    visit(nested, nested_prefix, depth + 1, next_seen, next_preferences)

        visit(type_name, "", 0, tuple(), initial_preferences)
        return rows


def parse_parameters(value: str) -> list[ParameterDef]:
    """解析 Action 形参并保留 FromBody/FromQuery/FromForm 等绑定来源。"""

    result: list[ParameterDef] = []
    for item in split_top_level(value):
        binding_matches = re.findall(r"\[\s*(FromBody|FromQuery|FromRoute|FromForm|FromHeader)[^\]]*\]", item)
        binding = binding_matches[-1] if binding_matches else "ApiController推断"
        item = re.sub(r"\[[^\]]+\]", " ", item)
        default = ""
        parts = split_top_level(item, "=")
        if len(parts) > 1:
            item, default = parts[0], "=".join(parts[1:]).strip()
        tokens = item.strip().split()
        if len(tokens) < 2:
            continue
        name = tokens[-1]
        type_name = clean_type(" ".join(tokens[:-1]).replace("ref ", "").replace("out ", ""))
        result.append(ParameterDef(name=name, type_name=type_name, binding=binding, default=default))
    return result


def extract_if_conditions(clean_body: str) -> list[str]:
    """提取 Action 内的 if 条件，作为参数必要性和条件关系的直接代码证据。"""

    result: list[str] = []
    for match in IF_RE.finditer(clean_body):
        open_paren = clean_body.find("(", match.start())
        close_paren = find_matching(clean_body, open_paren, "(", ")")
        if close_paren < 0:
            continue
        condition = re.sub(r"\s+", " ", clean_body[open_paren + 1:close_paren]).strip()
        if condition and condition not in result:
            result.append(condition)
    return result


def extract_errors(body: str) -> list[str]:
    """提取显式状态码和固定消息；不包含日志正文、异常栈或请求数据。"""

    result: list[str] = []
    status_matches = list(re.finditer(r"(?:StatusCode|MsgType)\s*=\s*([^;\r\n]+)", body))
    message_matches = list(re.finditer(r"Message\s*=\s*\"([^\"]{1,160})\"", body))
    for match in status_matches[:12]:
        normalized_status = re.sub(r"\s+", " ", match.group(0)).strip()
        result.append(f"状态赋值：{normalized_status}")
    for match in message_matches[:12]:
        result.append(f"固定提示：{match.group(1).strip()}")
    return list(dict.fromkeys(result))


def parse_controller(path: Path, repo_root: Path, project_key: str, perspective: str) -> list[ActionDef]:
    """解析一个 Controller 文件中的有效 Http Action。"""

    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    clean = mask_comments(raw)
    using_namespaces = [match.group("name") for match in USING_RE.finditer(clean)]
    class_match = CLASS_RE.search(clean)
    if class_match is None:
        return []
    controller_name = re.sub(r"Controller$", "", class_match.group("name"))
    controller_base = clean_type(class_match.group("bases") or "ControllerBase").split(",", 1)[0]
    class_open = clean.find("{", class_match.start())
    class_close = find_matching(clean, class_open, "{", "}")
    if class_close < 0:
        return []
    class_clean = clean[class_open + 1:class_close]
    offset = class_open + 1
    actions: list[ActionDef] = []
    for http_match in HTTP_ATTRIBUTE_RE.finditer(class_clean):
        if brace_depth(class_clean, http_match.start()) != 0:
            continue
        candidate_start = class_clean.rfind("\n", 0, http_match.start()) + 1
        method_match = METHOD_RE.match(class_clean, candidate_start)
        if method_match is None or "Http" not in method_match.group("attrs"):
            continue
        params_open = class_clean.find("(", method_match.end() - 1)
        params_close = find_matching(class_clean, params_open, "(", ")")
        if params_close < 0:
            continue
        body_open = class_clean.find("{", params_close)
        expression_arrow = class_clean.find("=>", params_close, body_open if body_open >= 0 else len(class_clean))
        if expression_arrow >= 0:
            semicolon = class_clean.find(";", expression_arrow)
            if semicolon < 0:
                continue
            body_close = semicolon
            body = class_clean[expression_arrow:semicolon + 1]
        else:
            if body_open < 0:
                continue
            body_close = find_matching(class_clean, body_open, "{", "}")
            if body_close < 0:
                continue
            body = class_clean[body_open + 1:body_close]
        attrs = method_match.group("attrs")
        http_attr = re.search(r"Http(Get|Post|Put|Delete|Patch|Head|Options)", attrs, re.I)
        route_match = re.search(r"\[\s*Route\s*\(\s*\"([^\"]+)\"", attrs, re.I)
        http_route_match = re.search(
            r"\[\s*Http(?:Get|Post|Put|Delete|Patch|Head|Options)\s*\(\s*\"([^\"]+)\"",
            attrs,
            re.I,
        )
        action_name = method_match.group("name")
        route = route_match.group(1) if route_match else (
            http_route_match.group(1) if http_route_match else f"api/{controller_name}/{action_name}"
        )
        absolute_start = offset + candidate_start
        raw_body = raw[offset + (expression_arrow if expression_arrow >= 0 else body_open) + 1:offset + body_close]
        calls = [f"{match.group('owner')}.{match.group('method')}"
                 for match in CALL_RE.finditer(body)]
        action = ActionDef(
            project_key=project_key,
            perspective=perspective,
            controller=controller_name,
            controller_base=controller_base,
            action=action_name,
            http_method=(http_attr.group(1).upper() if http_attr else "UNKNOWN"),
            route=route.lstrip("/"),
            return_type=clean_type(method_match.group("return")),
            parameters=parse_parameters(class_clean[params_open + 1:params_close]),
            summary=xml_summary_before(raw, absolute_start),
            attributes=re.sub(r"\s+", " ", attrs).strip(),
            body=body,
            source_file=str(path.relative_to(repo_root)),
            line=line_number(raw, absolute_start),
            using_namespaces=using_namespaces,
            validations=extract_if_conditions(body),
            calls=list(dict.fromkeys(calls)),
            errors=extract_errors(raw_body),
        )
        classify_action(action)
        actions.append(action)
    return actions


def semantic_verb_kind(value: str) -> str:
    """按名称中的语义动词判断读写；任何写动词优先，避免 GetInfoModify 被误判为查询。"""

    write_prefixes = ("append", "write", "refund", "update", "delete", "remove", "insert", "create")
    tokens = to_snake(value).split("_")
    for token in tokens:
        if token in WRITE_VERB_TOKENS or token.startswith(write_prefixes):
            return "write"
    for token in tokens:
        if token in READ_VERB_TOKENS:
            return "read"
    return ""


def classify_action(action: ActionDef) -> None:
    """依据名称与调用链给出保守工具等级；安全判断宁可降级，不把写接口误开放。"""

    # 旧项目常用 ActivityGetInfo / MediaUpload 这类“业务域 + 动词”命名，按首个语义动词判断读写。
    # 这样既能识别 ActivityGetInfo 为查询，也不会把 MediaUpload、BusinessSetXxx 漏成只读。
    verb_kind = semantic_verb_kind(re.sub(r"^Business", "", action.action, flags=re.I))
    read_like = verb_kind == "read"
    mutation_calls = [call for call in action.calls if semantic_verb_kind(call.split(".")[-1]) == "write"]
    if DENY_CONTROLLER_RE.search(action.controller):
        action.grade = "D"
        action.grade_reason = "测试、模板测试或后台认证 Controller，不进入客服工具。"
        return
    if DENY_ACTION_RE.search(action.action):
        action.grade = "D"
        action.grade_reason = "登录、回调或通知入口，不是只读业务查询。"
        return
    if not read_like:
        action.grade = "D"
        action.grade_reason = "Action 名称和摘要不足以证明只读，默认禁止。"
        return
    if mutation_calls:
        action.grade = "C"
        action.grade_reason = "查询路径包含疑似写入或外部副作用调用，必须人工复核：" + ", ".join(mutation_calls[:5])
        return
    secret_params = []
    for parameter in action.parameters:
        if is_secret_name(parameter.name):
            secret_params.append(parameter.name)
    if secret_params:
        action.grade = "C"
        action.grade_reason = "请求包含签名、令牌或随机凭据类参数，不能直接交由模型：" + ", ".join(secret_params)
        return
    if action.authenticated or action.parameters:
        action.grade = "B"
        action.grade_reason = "代码路径看起来只读，但身份字段和业务标识必须由受控上下文注入或从上游结果取得。"
        return
    action.grade = "A"
    action.grade_reason = "无请求参数且静态调用链未发现明显写入，仍需部署前只读验收。"


def property_visibility(name: str, type_name: str = "", description: str = "") -> tuple[str, str]:
    """标记字段敏感等级和是否适合原样进入模型上下文。"""

    compact = "".join(identifier_tokens(name))
    is_boolean_sign = compact == "sign" and clean_type(type_name).rstrip("?").lower() == "bool"
    description_sensitive = (
        clean_type(type_name).rstrip("?").lower() == "string"
        and any(token in compact for token in ("keyword", "search", "value", "content"))
        and bool(re.search(r"手机号|手机|电话|姓名|身份证|地址", description or ""))
    )
    if is_secret_name(name) and not is_boolean_sign:
        return "密钥/凭据", "禁止原样进入模型"
    if is_sensitive_name(name) or description_sensitive:
        return "个人信息", "仅在当前授权场景按最小范围提供"
    leaf = re.split(r"[.\[\]]+", name)[-1]
    if IDENTIFIER_NAME_RE.search(leaf) or BUSINESS_REFERENCE_NAME_RE.search(leaf):
        return "内部标识", "不向客户展示；模型调用时优先使用服务端引用"
    return "普通业务字段", "可按问题需要提供"


def parameter_source(name: str, perspective: str, description: str = "", type_name: str = "") -> str:
    """确定模型参数应从何处取得，防止模型猜测身份和内部主键。"""

    if name.lower() == "uid":
        return "服务端注入：目标会员 UID" if perspective == "顾客视角" else "服务端注入：当前操作人 UID"
    if name.lower() == "storeid":
        return "服务端注入：已确认门店"
    if name.lower() == "appid":
        return "服务端注入：当前产品/小程序配置"
    sensitivity, _ = property_visibility(name, type_name, description)
    if sensitivity == "个人信息":
        return "当前会话提供并临时使用；不得持久化到模型历史"
    if is_secret_name(name):
        return "不得由模型提供"
    if IDENTIFIER_NAME_RE.search(name):
        return "必须来自同一会话上游 API 结果或服务端对象引用"
    if PAGING_NAME_RE.search(name):
        return "AI 可在服务端上限内选择"
    if DATE_NAME_RE.search(name):
        return "AI 可按客户问题选择，必须使用门店时区和合法范围"
    if STATE_NAME_RE.search(name):
        return "AI 只能使用文档确认的枚举值"
    return "AI 可按业务问题提供；仍需服务端 Schema 校验"


def requiredness_for(prop: PropertyDef, parameter_name: str, action: ActionDef) -> tuple[str, str]:
    """从特性与 Controller 条件共同判断必填性，并保留证据而非只给布尔值。"""

    references = []
    conditional_references = []
    for condition in action.validations:
        if re.search(rf"\b{re.escape(parameter_name)}\s*\.\s*{re.escape(prop.name)}\b", condition):
            target = rf"{re.escape(parameter_name)}\s*\.\s*{re.escape(prop.name)}"
            invalid_patterns = (
                rf"(?<!\!)string\.IsNullOr(?:Empty|WhiteSpace)\s*\(\s*{target}\s*\)",
                rf"{target}\s*==\s*(?:0|null|default|string\.Empty|\"\")",
                rf"{target}\s*<\s*1\b",
                rf"{target}\s*<=\s*0\b",
                rf"!\s*{target}\.HasValue\b",
                rf"!\s*StringOperate\.IsDate\s*\(\s*{target}\s*\)",
            )
            if any(re.search(pattern, condition) for pattern in invalid_patterns):
                references.append(condition)
                # “A 无效 || B 无效”代表各字段分别必填；只有字段所在的同一 OR 分支含 && 时才是组合/条件约束。
                target_branch = next(
                    (branch for branch in re.split(r"\|\|", condition) if re.search(target, branch)),
                    "",
                )
                if "&&" in target_branch:
                    conditional_references.append(condition)
    if prop.name.lower() in {"uid", "storeid", "appid"} and (references or prop.required_attribute):
        label = "服务端必注入"
    elif prop.name.lower() in {"uid", "storeid", "appid"}:
        label = "服务端上下文注入（源码未确认必填）"
    elif references:
        label = "参与组合校验" if conditional_references else "代码校验必填"
    elif prop.required_attribute:
        label = "模型特性声明必填"
    elif prop.default:
        label = "可选/有默认值"
    else:
        label = "源码未确认必填"
    evidence_parts = []
    if prop.required_attribute:
        evidence_parts.append("[Required]")
    if prop.default:
        evidence_parts.append("默认值=" + prop.default)
    evidence_parts.extend("if(" + normalize_condition(item) + ")" for item in references[:3])
    return label, "；".join(evidence_parts) or "未发现显式必填证据"


def effective_property_description(prop: PropertyDef) -> str:
    """保留源码注释，同时把明显的字段名/注释冲突标为待复核，避免机器目录传播错误语义。"""

    description = prop.summary or "源码属性注释缺失"
    name_summary_conflict = (
        is_sensitive_name(prop.name)
        and re.search(r"(?:课程|卡片|门店|员工|项目)\s*[Ii][Dd]", description)
    ) or (
        "keyword" in "".join(identifier_tokens(prop.name))
        and re.search(r"(?:分类|课程|卡片|门店|员工|项目)\s*[Ii][Dd]", description)
    )
    if name_summary_conflict:
        return f"源码注释疑似与字段名冲突，待人工复核（原注释：{description}）"
    return description


def infer_domain(controller: str) -> str:
    for key, value in DOMAIN_BY_CONTROLLER.items():
        if controller.lower() == key.lower() or key.lower() in controller.lower():
            return value
    return controller + " 模块"


def infer_freshness(action: ActionDef) -> str:
    value = action.action + " " + action.summary
    if re.search(r"(Log|History|Record|日志|历史|记录)", value, re.I):
        return "历史/记录型数据；具体保留范围以接口代码为准"
    if re.search(r"(Statistic|Report|Count|统计|报表)", value, re.I):
        return "聚合结果；时间范围和门店时区必须由请求参数确认"
    if re.search(r"(Cache|Redis)", action.body, re.I):
        return "可能包含缓存结果；不能等同数据库即时状态"
    return "当前调用时状态；不能据此还原过去某一时刻"


def infer_usage(action: ActionDef) -> tuple[str, str]:
    """优先使用源码 XML 摘要；缺失时只做明确标记的名称推断。"""

    summary = action.summary or f"【源码推断】{action.action} 的 XML 摘要缺失，按 Action 名仅能判断为候选查询。"
    name = action.action.lower()
    perspective = action.perspective
    scenario = f"在{perspective}中核对“{summary}”对应的当前返回结果。"
    if "usercards" in name or "usercardlist" in name:
        scenario = (
            "顾客反馈在顾客端看不到会员卡/课卡，或余额、有效期、卡状态与预期不一致时，读取目标会员实际可见卡列表。"
            if perspective == "顾客视角"
            else "商家核对会员卡列表、筛选结果、余额、有效期和卡状态时使用；复现单个顾客页面还需对照 C 端接口。"
        )
    elif "usercard" in name or "cardbalance" in name or "childcard" in name:
        scenario = (
            "已从上游卡列表取得服务端卡引用后，核对顾客端单张卡的余额、状态、有效期、服务项目或使用限制。"
            if perspective == "顾客视角"
            else "已定位会员和卡后，核对商家端单张卡详情、余额、操作记录或可管理状态。"
        )
    elif "reservation" in name or "lessons" in name or "course" in name:
        scenario = (
            "顾客反馈课程不可见、某日不可约、候补/预约状态或可用卡资格异常时，用于还原顾客端当前课程与预约视图。"
            if perspective == "顾客视角"
            else "商家核对排课、预约名单、预约状态、教练/场地或预约配置时使用；顾客可见性需再对照 C 端结果。"
        )
    elif "consumption" in name or "recharge" in name:
        scenario = (
            "顾客反馈消费、充值、余额变化或交易明细问题时，读取顾客端当前可见记录和单据详情。"
            if perspective == "顾客视角"
            else "商家核对会员消费、充值、核减、返还、退款前置事实或操作后余额时使用。"
        )
    elif "order" in name:
        scenario = (
            "顾客反馈订单列表、订单详情、支付后状态或商品信息不一致时，读取顾客端当前订单视图。"
            if perspective == "顾客视角"
            else "商家核对商城/餐饮订单列表、详情、支付和履约状态时使用。"
        )
    elif "coupon" in name:
        scenario = (
            "顾客反馈优惠券不可见、不可用、已用或过期状态异常时，核对顾客端券列表和使用条件。"
            if perspective == "顾客视角"
            else "商家核对优惠券配置、发放、领取、使用条件和统计时使用。"
        )
    elif "userinfo" in name or "userslist" in name or "searchuser" in name or "usermobile" in name:
        scenario = (
            "商家提供手机号后，用于确认目标会员在顾客端当前资料或会员身份；只允许当前门店范围。"
            if perspective == "顾客视角"
            else "商家按手机号或筛选条件定位会员、确认会员档案与门店关系，为后续卡/预约/消费查询建立上游对象引用。"
        )
    elif "store" in name or "soft" in name or "version" in name:
        scenario = (
            "核对顾客端当前门店展示、功能开关或版本相关可见结果。"
            if perspective == "顾客视角"
            else "核对门店配置、软件版本、服务期或模块开关；需要解释顾客端差异时再调用 C 端对应接口。"
        )
    elif "staff" in name or "employee" in name:
        scenario = "商家核对员工、教练、权限或门店关系；不得把其他员工的个人信息无条件交给模型。"
    if action.summary:
        return action.summary, scenario
    return (
        summary,
        scenario + " 由于 XML 摘要缺失，只有请求/响应字段也能证明目标事实时才可调用。",
    )


def manifest_usage(
    action: ActionDef,
    response_fields: list[dict[str, object]],
) -> dict[str, object]:
    """生成机器目录的用途、选择时机和相邻能力边界；不绑定具体客户问法。"""

    usage, when_to_use = infer_usage(action)
    fact_terms = list(dict.fromkeys(
        str(item["description"]) for item in response_fields
        if item["exposurePolicy"] not in {"blocked", "reference-only"}
        and str(item["description"]) not in {
            "返回信息", "每页数量", "当前页", "总页数", "数据总数量", "是否有下页", "数据集合",
        }
    ))[:8]
    purpose = usage.rstrip("。")
    if fact_terms:
        purpose += "；主要读取：" + "、".join(fact_terms) + "。"
    else:
        purpose += "。"

    override = MANIFEST_USAGE_OVERRIDES.get(action.tool_id, {})
    return {
        "capability": str(override.get("capability", action.summary or usage)),
        "purpose": str(override.get("purpose", purpose)),
        "whenToUse": str(override.get("whenToUse", when_to_use)),
        "doNotUse": str(override.get(
            "doNotUse",
            "不用于写入、修改、支付、退款或核销；不用于响应字段无法证明的结论，历史问题不能只靠当前结果。",
        )),
        "usageEvidence": list(override.get(
            "usageEvidence",
            ["Controller XML 摘要", "请求/响应 DTO", "Controller 校验与直接调用"],
        )),
    }


def validation_rows(action: ActionDef, parameter_name: str, prop_name: str) -> list[str]:
    pattern = re.compile(rf"\b{re.escape(parameter_name)}\s*\.\s*{re.escape(prop_name)}\b")
    return [item for item in action.validations if pattern.search(item)]


def counterpart_map(actions: list[ActionDef]) -> dict[tuple[str, str], list[ActionDef]]:
    """按 Controller 和去除 Business 前缀后的 Action 建立 C/B 视角对照索引。"""

    result: dict[tuple[str, str], list[ActionDef]] = {}
    for action in actions:
        normalized = re.sub(r"^Business", "", action.action, flags=re.I)
        key = (action.controller.lower(), normalized.lower())
        result.setdefault(key, []).append(action)
    return result


def render_request_rows(action: ActionDef, catalog: ModelCatalog) -> list[str]:
    rows: list[str] = []
    for parameter in action.parameters:
        flattened = catalog.flatten(
            parameter.type_name,
            max_depth=2,
            preferred_namespaces=action.using_namespaces,
        )
        if not flattened:
            sensitivity, visibility = property_visibility(parameter.name)
            required = "有默认值" if parameter.default else "Action 形参"
            rows.append(
                f"| `{parameter.name}` | `{parameter.type_name}` | {required} | "
                f"{escape_cell(parameter.binding)} | {escape_cell(parameter_source(parameter.name, action.perspective))} | "
                f"{escape_cell(sensitivity + '；' + visibility)} |"
            )
            continue
        for path, prop in flattened:
            is_direct = "." not in path and "[]" not in path
            if is_direct:
                required, evidence = requiredness_for(prop, parameter.name, action)
            elif prop.required_attribute:
                required, evidence = "嵌套模型特性声明必填", "[Required]；Controller 未直接校验该嵌套路径"
            elif prop.default:
                required, evidence = "可选/有默认值", "默认值=" + prop.default
            else:
                required, evidence = "源码未确认必填", "未发现嵌套字段显式必填证据"
            evidence = f"绑定={parameter.binding}；{evidence}"
            description = effective_property_description(prop)
            sensitivity, visibility = property_visibility(path, prop.type_name, description)
            rows.append(
                f"| `{path}` | `{prop.type_name}` | {required} | {escape_cell(evidence)} | "
                f"{escape_cell(parameter_source(path, action.perspective, description, prop.type_name))} | "
                f"{escape_cell(description + '；' + sensitivity + '；' + visibility)} |"
            )
    return rows


def render_response_rows(action: ActionDef, catalog: ModelCatalog) -> list[str]:
    wrapper, payload_type = unwrap_return_type(action.return_type)
    payload_root, payload_args = parse_generic(payload_type)
    if "DataList" in wrapper:
        base_path = "Data[]"
        flattened = catalog.flatten(payload_type, preferred_namespaces=action.using_namespaces)
    elif payload_root in GENERIC_COLLECTIONS and payload_args:
        base_path = "Data[]"
        flattened = catalog.flatten(payload_args[0], preferred_namespaces=action.using_namespaces)
    else:
        base_path = "Data"
        flattened = catalog.flatten(payload_type, preferred_namespaces=action.using_namespaces)
    if not flattened:
        if payload_root in GENERIC_COLLECTIONS and payload_args:
            item_type = payload_args[0]
            sensitivity, visibility = property_visibility("Data[]", item_type)
            return [
                f"| `Data[]` | `{item_type}` | 标量集合；具体业务含义以 Action 摘要为准 | "
                f"{escape_cell(sensitivity)} | {escape_cell(visibility)} |"
            ]
        if clean_type(payload_type).rstrip("?") in SCALAR_TYPES:
            sensitivity, visibility = property_visibility("Data", payload_type)
            meaning = "运行时对象，字段结构无法由方法签名静态确定" if payload_type == "object" else "标量返回值；具体业务含义以 Action 摘要为准"
            return [
                f"| `Data` | `{payload_type}` | {meaning} | "
                f"{escape_cell(sensitivity)} | {escape_cell(visibility)} |"
            ]
        sensitivity, visibility = property_visibility(payload_type, payload_type)
        return [
            f"| `Data` | `{payload_type}` | 返回类型未能从当前 DTO 源码递归展开 | "
            f"{escape_cell(sensitivity)} | {escape_cell(visibility)} |"
        ]
    rows: list[str] = []
    for path, prop in flattened[:240]:
        full_path = f"{base_path}.{path}" if path else base_path
        description = effective_property_description(prop)
        sensitivity, visibility = property_visibility(full_path, prop.type_name, description)
        rows.append(
            f"| `{full_path}` | `{prop.type_name}` | {escape_cell(description)} | "
            f"{escape_cell(sensitivity)} | {escape_cell(visibility)} |"
        )
    if len(flattened) > 240:
        rows.append(
            f"| `{base_path}.…` | — | 嵌套字段共 {len(flattened)} 个，为控制单接口目录规模仅展示前 240 个；"
            "调用前仍应以当前编译 DTO 为准 | — | — |"
        )
    return rows


def manifest_source_policy(name: str, perspective: str, description: str = "", type_name: str = "") -> str:
    """把请求字段归入执行器可验证的来源，不允许模型自由填写身份、敏感值和内部主键。"""

    leaf = re.split(r"[.\[\]]+", name)[-1].lower()
    if leaf == "uid":
        return "customer-context" if perspective == "顾客视角" else "operator-context"
    if leaf == "storeid":
        return "store-context"
    if leaf == "appid":
        return "application-context"
    if is_secret_name(name):
        return "forbidden"
    sensitivity, _ = property_visibility(name, type_name, description)
    if sensitivity == "个人信息":
        return "conversation-sensitive-context"
    if IDENTIFIER_NAME_RE.search(leaf) or BUSINESS_REFERENCE_NAME_RE.search(leaf):
        return "upstream-reference"
    return "model-argument"


def manifest_request_source_policy(
    action: ActionDef,
    path: str,
    description: str = "",
    type_name: str = "",
) -> str:
    """优先使用人工审核的字段来源覆写，其余字段继续走统一静态分类规则。"""

    return TRUSTED_REQUEST_SOURCE_POLICY_OVERRIDES.get(
        (action.tool_id, path),
        manifest_source_policy(path, action.perspective, description, type_name),
    )


def json_schema_for_csharp_type(type_name: str) -> dict[str, object]:
    """生成保守 JSON Schema 片段；复杂 DTO 的明细仍由 requestFields 描述。"""

    normalized = clean_type(type_name).rstrip("?")
    root, args = parse_generic(normalized)
    if root in GENERIC_COLLECTIONS and args:
        return {"type": "array", "items": json_schema_for_csharp_type(args[0]), "maxItems": 20}
    lowered = normalized.lower()
    if lowered in {"bool", "boolean"}:
        return {"type": "boolean"}
    if lowered in {"byte", "sbyte", "short", "ushort", "int", "uint", "long", "ulong"}:
        return {"type": "integer"}
    if lowered in {"float", "double", "decimal"}:
        return {"type": "number"}
    if lowered in {"datetime", "datetimeoffset"}:
        return {"type": "string", "format": "date-time"}
    if lowered in {"guid"}:
        return {"type": "string", "format": "uuid"}
    if lowered in {"string", "char", "uri", "timespan"}:
        return {"type": "string", "maxLength": 600}
    if lowered in {"object", "dynamic"}:
        return {"type": "object"}
    return {"type": "object", "x-csharp-type": normalized}


def apply_execution_safety_constraints(path: str, schema: dict[str, object]) -> dict[str, object]:
    """为通用分页参数增加执行上限，避免模型触发无边界数据库查询；不包含业务场景路由。"""

    result = dict(schema)
    leaf = re.split(r"[.\[\]]+", path)[-1].lower()
    if result.get("type") == "integer" and leaf in {"pagesize", "limit"}:
        result["minimum"] = 1
        result["maximum"] = 100
    elif result.get("type") == "integer" and leaf in {"pageindex", "page"}:
        result["minimum"] = 1
        result["maximum"] = 10000
    elif result.get("type") == "integer" and leaf == "offset":
        result["minimum"] = 0
        result["maximum"] = 1000000
    return result


def apply_declared_range(
    schema: dict[str, object],
    minimum: float | int | None,
    maximum: float | int | None,
) -> dict[str, object]:
    """把 DTO 的 DataAnnotations Range 无损带入模型参数 Schema，不推测未声明的业务枚举。"""

    result = dict(schema)
    if minimum is not None:
        result["minimum"] = minimum
    if maximum is not None:
        result["maximum"] = maximum
    return result


def manifest_request_fields(action: ActionDef, catalog: ModelCatalog) -> list[dict[str, object]]:
    """输出完整请求字段策略；Agent Schema 只会再选取其中明确允许模型填写的简单字段。"""

    fields: list[dict[str, object]] = []
    for parameter in action.parameters:
        flattened = catalog.flatten(
            parameter.type_name,
            max_depth=2,
            preferred_namespaces=action.using_namespaces,
        )
        if not flattened:
            policy = manifest_request_source_policy(action, parameter.name, "", parameter.type_name)
            sensitivity, visibility = property_visibility(parameter.name, parameter.type_name)
            fields.append({
                "path": parameter.name,
                "type": parameter.type_name,
                "binding": parameter.binding,
                "requiredness": "action-parameter" if not parameter.default else "optional-default",
                "requirednessEvidence": f"default={parameter.default}" if parameter.default else "Action 形参",
                "sourcePolicy": policy,
                "modelWritable": policy == "model-argument",
                "description": "Action 形参；源码属性注释不可用",
                "sensitivity": sensitivity,
                "visibility": visibility,
                "schema": apply_execution_safety_constraints(
                    parameter.name, json_schema_for_csharp_type(parameter.type_name)
                ),
            })
            continue
        for path, prop in flattened:
            is_direct = "." not in path and "[]" not in path
            if is_direct:
                requiredness, evidence = requiredness_for(prop, parameter.name, action)
            elif prop.required_attribute:
                requiredness, evidence = "嵌套模型特性声明必填", "[Required]；Controller 未直接校验该嵌套路径"
            elif prop.default:
                requiredness, evidence = "可选/有默认值", "默认值=" + prop.default
            else:
                requiredness, evidence = "源码未确认必填", "未发现嵌套字段显式必填证据"
            description = effective_property_description(prop)
            policy = manifest_request_source_policy(action, path, description, prop.type_name)
            sensitivity, visibility = property_visibility(path, prop.type_name, description)
            fields.append({
                "path": path,
                "containerParameter": parameter.name,
                "type": prop.type_name,
                "binding": parameter.binding,
                "requiredness": requiredness,
                "requirednessEvidence": evidence.replace("\\|", "|"),
                "sourcePolicy": policy,
                "modelWritable": policy == "model-argument" and is_direct,
                "description": description,
                "sensitivity": sensitivity,
                "visibility": visibility,
                "schema": apply_execution_safety_constraints(
                    path, apply_declared_range(
                        json_schema_for_csharp_type(prop.type_name),
                        prop.range_minimum,
                        prop.range_maximum,
                    )
                ),
                "source": f"{prop.source_file}:{prop.line}",
            })
    return fields


def manifest_agent_argument_schema(fields: list[dict[str, object]]) -> dict[str, object]:
    """只向模型开放顶层简单业务参数；身份、手机号、凭据和内部引用由执行器另外绑定。"""

    properties: dict[str, object] = {}
    required: list[str] = []
    for field in fields:
        if not field["modelWritable"]:
            continue
        schema = field["schema"]
        if not isinstance(schema, dict) or schema.get("type") not in {"string", "integer", "number", "boolean"}:
            continue
        path = str(field["path"])
        properties[path] = {
            **schema,
            "description": field["description"],
        }
        if field["requiredness"] in {"代码校验必填", "模型特性声明必填", "action-parameter"}:
            required.append(path)
    result: dict[str, object] = {
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
    }
    if required:
        result["required"] = sorted(required)
    return result


def manifest_response_fields(action: ActionDef, catalog: ModelCatalog) -> list[dict[str, object]]:
    """输出响应投影策略，内部标识只可转为短期引用，凭据字段永远阻断。"""

    _, payload_type = unwrap_return_type(action.return_type)
    payload_root, payload_args = parse_generic(payload_type)
    if payload_root in GENERIC_COLLECTIONS and payload_args:
        base_path = "Data[]"
        flattened = catalog.flatten(payload_args[0], preferred_namespaces=action.using_namespaces)
    else:
        base_path = "Data"
        flattened = catalog.flatten(payload_type, preferred_namespaces=action.using_namespaces)
    if not flattened:
        scalar_type = payload_args[0] if payload_root in GENERIC_COLLECTIONS and payload_args else payload_type
        scalar_path = "Data[]" if payload_root in GENERIC_COLLECTIONS and payload_args else "Data"
        sensitivity, visibility = property_visibility(scalar_path, scalar_type)
        return [{
            "path": scalar_path,
            "type": scalar_type,
            "description": "运行时对象，字段结构无法由方法签名静态确定" if scalar_type == "object" else "标量返回值",
            "sensitivity": sensitivity,
            "exposurePolicy": "blocked" if sensitivity == "密钥/凭据" else "minimum" if sensitivity == "个人信息" else "allowed",
            "visibility": visibility,
        }]
    fields: list[dict[str, object]] = []
    for path, prop in flattened:
        full_path = f"{base_path}.{path}" if path else base_path
        description = effective_property_description(prop)
        sensitivity, visibility = property_visibility(full_path, prop.type_name, description)
        if sensitivity == "密钥/凭据":
            exposure = "blocked"
        elif sensitivity == "个人信息":
            exposure = "minimum"
        elif sensitivity == "内部标识":
            exposure = "reference-only"
        else:
            exposure = "allowed"
        fields.append({
            "path": full_path,
            "type": prop.type_name,
            "description": description,
            "sensitivity": sensitivity,
            "exposurePolicy": exposure,
            "visibility": visibility,
            "source": f"{prop.source_file}:{prop.line}",
        })
    return fields


def controller_source_fingerprint(repo_root: Path, actions: list[ActionDef]) -> str:
    """计算本视角 Controller 输入指纹，用于发布时阻止目录与源码漂移。"""

    fingerprint = hashlib.sha256()
    for path in sorted({repo_root / item.source_file for item in actions}):
        fingerprint.update(str(path.relative_to(repo_root)).encode("utf-8"))
        fingerprint.update(path.read_bytes())
    return fingerprint.hexdigest()


def catalog_source_fingerprint(repo_root: Path, source_roots: Iterable[Path]) -> str:
    """覆盖目录生成实际读取的 Controller、DTO 和生成器源码，避免只改 DTO 时清单静默过期。"""

    fingerprint = hashlib.sha256()
    source_files: set[Path] = {Path(__file__).resolve()}
    for root in source_roots:
        if root.is_file():
            source_files.add(root.resolve())
        elif root.is_dir():
            # bin/obj 中的 AssemblyInfo 等文件会随每次编译变化，不属于目录生成器读取的业务源码。
            # 将它们计入会造成“刚生成清单，编译后立即过期”的伪漂移。
            source_files.update(
                path.resolve()
                for path in root.rglob("*.cs")
                if not {"bin", "obj"}.intersection(path.relative_to(root).parts)
            )
    for path in sorted(source_files, key=lambda item: str(item)):
        try:
            relative = path.relative_to(repo_root)
        except ValueError:
            relative = path
        fingerprint.update(str(relative).encode("utf-8"))
        fingerprint.update(path.read_bytes())
    return fingerprint.hexdigest()


def build_manifest(
    repo_root: Path,
    project_key: str,
    project_name: str,
    perspective: str,
    actions: list[ActionDef],
    other_actions: list[ActionDef],
    catalog: ModelCatalog,
    commit: str,
) -> dict[str, object]:
    """生成动态能力目录；不写用户问题、场景触发词或固定问题到接口映射。"""

    other_index = counterpart_map(other_actions)
    tools: list[dict[str, object]] = []
    for action in sorted(
        (item for item in actions if item.grade in {"A", "B", "C"}),
        key=lambda item: item.tool_id,
    ):
        request_fields = manifest_request_fields(action, catalog)
        response_fields = manifest_response_fields(action, catalog)
        usage = manifest_usage(action, response_fields)
        wrapper, payload_type = unwrap_return_type(action.return_type)
        normalized = re.sub(r"^Business", "", action.action, flags=re.I)
        counterparts = [
            item.tool_id
            for item in other_index.get((action.controller.lower(), normalized.lower()), [])
            if item.grade in {"A", "B", "C"}
        ]
        response_terms = list(dict.fromkeys(
            str(item["description"]) for item in response_fields
            if item["exposurePolicy"] not in {"blocked", "reference-only"}
        ))[:16]
        tools.append({
            "toolId": action.tool_id,
            "perspective": perspective,
            "domain": infer_domain(action.controller),
            "capability": usage["capability"],
            "purpose": usage["purpose"],
            "whenToUse": usage["whenToUse"],
            "doNotUse": usage["doNotUse"],
            "usageEvidence": usage["usageEvidence"],
            "selectorText": "；".join(filter(None, [
                infer_domain(action.controller),
                str(usage["capability"]),
                str(usage["purpose"]),
                str(usage["whenToUse"]),
                "、".join(response_terms),
            ])),
            "grade": action.grade,
            "gradeReason": action.grade_reason,
            "registration": {
                "status": "candidate" if action.grade in {"A", "B"} else "manual-review",
                "defaultEnabled": False,
                "requiresRuntimeAllowlist": True,
                "requiresReadOnlyAcceptance": True,
            },
            "transport": {
                "httpMethod": action.http_method,
                "path": "/" + action.route,
                "authentication": "existing-api-signature" if action.authenticated else "source-allows-anonymous",
                "binding": list(dict.fromkeys(item.binding for item in action.parameters)),
            },
            "requestType": [item.type_name for item in action.parameters],
            "requestFields": request_fields,
            "agentArgumentSchema": manifest_agent_argument_schema(request_fields),
            "requiredRuntimeInputs": [
                {"path": item["path"], "sourcePolicy": item["sourcePolicy"], "requiredness": item["requiredness"]}
                for item in request_fields
                if item["sourcePolicy"] != "model-argument"
                and ("必" in str(item["requiredness"]) or item["requiredness"] in {"参与组合校验", "action-parameter"})
            ],
            "response": {
                "declaredType": action.return_type,
                "wrapper": wrapper or "unknown",
                "payloadType": payload_type,
                "successCondition": "State == true for DataResult/DataList wrappers; otherwise use the declared HTTP contract",
                "fields": response_fields,
            },
            "evidence": {
                "source": f"{action.source_file}:{action.line}",
                "controllerValidations": [normalize_machine_condition(item) for item in action.validations],
                "directCalls": action.calls,
                "explicitFailureSignals": action.errors,
                "freshness": infer_freshness(action),
            },
            "counterparts": counterparts,
        })
    return {
        "schemaVersion": "1.1",
        "catalogKind": "existing-api-agent-capabilities",
        "selectionMode": "agent-semantic-retrieval",
        "fixedQuestionRouting": False,
        "project": project_name,
        "perspective": perspective,
        "sourceCommit": commit,
        "generatedDate": date.today().isoformat(),
        "controllerFingerprint": "sha256:" + controller_source_fingerprint(repo_root, actions),
        "catalogSourceFingerprint": "sha256:" + catalog_source_fingerprint(repo_root, catalog.source_roots),
        "auditedActionCount": len(actions),
        "manifestToolCount": len(tools),
        "gradeCounts": {grade: sum(1 for item in actions if item.grade == grade) for grade in "ABCD"},
        "runtimePolicy": {
            "allToolsDisabledByDefault": True,
            "gradeDExcluded": True,
            "gradeCRequiresManualReview": True,
            "modelCannotSupplyIdentitySensitiveOrInternalReferenceValues": True,
            "toolMustBeReturnedByRecentCapabilitySearch": True,
        },
        "tools": tools,
    }


def validate_manifest(actions: list[ActionDef], manifest: dict[str, object], project_key: str) -> None:
    """验证机器目录没有固定场景路由、D 级工具或默认开放能力。"""

    tools = manifest.get("tools")
    if not isinstance(tools, list):
        raise ValueError(f"{project_key} manifest tools must be an array")
    expected = sum(1 for item in actions if item.grade in {"A", "B", "C"})
    if len(tools) != expected:
        raise ValueError(f"{project_key} manifest count mismatch: expected {expected}, actual {len(tools)}")
    tool_ids = [str(item.get("toolId", "")) for item in tools]
    if len(tool_ids) != len(set(tool_ids)):
        raise ValueError(f"{project_key} manifest contains duplicate tool ids")
    forbidden_keys = {"scenario", "trigger", "questionMapping", "fixedAnswer", "keywordRoute"}
    serialized = json.dumps(manifest, ensure_ascii=False)
    for key in forbidden_keys:
        if f'"{key}"' in serialized:
            raise ValueError(f"{project_key} manifest contains forbidden fixed-routing key: {key}")
    for tool in tools:
        if tool.get("grade") == "D":
            raise ValueError(f"{project_key} manifest exposes grade D tool: {tool.get('toolId')}")
        for key in ("capability", "purpose", "whenToUse", "doNotUse"):
            if not isinstance(tool.get(key), str) or not str(tool.get(key)).strip():
                raise ValueError(f"{project_key} manifest is missing {key}: {tool.get('toolId')}")
        usage_evidence = tool.get("usageEvidence")
        if not isinstance(usage_evidence, list) or not usage_evidence:
            raise ValueError(f"{project_key} manifest is missing usageEvidence: {tool.get('toolId')}")
        registration = tool.get("registration", {})
        if not isinstance(registration, dict) or registration.get("defaultEnabled") is not False:
            raise ValueError(f"{project_key} manifest enables a tool by default: {tool.get('toolId')}")
        for field in tool.get("requestFields", []):
            if field.get("modelWritable") and field.get("sourcePolicy") != "model-argument":
                raise ValueError(f"{project_key} manifest allows protected field: {tool.get('toolId')}/{field.get('path')}")

    if project_key == "crmapi":
        member_detail = next(
            (item for item in tools if item.get("toolId") == "crmapi.user.business_get_user_info"),
            None,
        )
        required_terms = ("全部会员卡", "分组", "资料", "余额", "有效期")
        searchable_text = " ".join(str(member_detail.get(key, "")) for key in (
            "capability", "purpose", "whenToUse", "selectorText"
        )) if isinstance(member_detail, dict) else ""
        missing_terms = [term for term in required_terms if term not in searchable_text]
        if missing_terms:
            raise ValueError(
                "crmapi member detail usage is incomplete: " + ", ".join(missing_terms)
            )


def render_document(
    repo_root: Path,
    project_key: str,
    project_name: str,
    perspective: str,
    project_root: Path,
    actions: list[ActionDef],
    other_actions: list[ActionDef],
    catalog: ModelCatalog,
    commit: str,
) -> str:
    """把 Action 索引和 A/B/C 级候选详细契约渲染为一份 Markdown。"""

    grades = {grade: sum(1 for item in actions if item.grade == grade) for grade in "ABCD"}
    controller_count = len({item.controller for item in actions})
    fingerprint = controller_source_fingerprint(repo_root, actions)
    other_index = counterpart_map(other_actions)

    lines = [
        f"# 课小秘 {perspective} API 工具筛选目录",
        "",
        "> 内部 AI 工具目录。只用于选择和约束 API 调用，不得把路由、内部类型、鉴权字段、Provider 名称或内部主键直接回复给客户。",
        "",
        "## 目录元数据",
        "",
        f"- 源项目：`{project_name}`（`{project_root.relative_to(repo_root)}`）",
        f"- 目标框架：`.NET 8 / ASP.NET Core Controller API`",
        f"- 视角：`{perspective}`",
        f"- 源码提交：`{commit}`",
        f"- 生成日期：`{date.today().isoformat()}`",
        f"- Controller 数：`{controller_count}`",
        f"- 实际 Http Action 数：`{len(actions)}`",
        f"- 工具等级：`A={grades['A']}`、`B={grades['B']}`、`C={grades['C']}`、`D={grades['D']}`",
        f"- Controller 源码指纹：`sha256:{fingerprint}`",
        f"- 机器目录：`{project_key}-api-tool-manifest.json`（所有工具默认关闭）",
        "",
        "## 使用边界",
        "",
        "- 本目录从当前 Controller、DTO、继承字段、代码内 `if` 校验和一层 Provider/Service 调用静态生成；静态结果不是生产可用性证明。",
        "- A/B/C 级才会提供详细契约。D 级仍保留完整 Action 索引和排除原因，但不得注册为客服查询工具。",
        "- `Uid`、`StoreId`、`AppId` 和内部业务 ID 不能由模型猜测；必须由已验证会话注入，或来自同一会话上游 API 的服务端引用。",
        "- `[Required]` 只代表模型特性声明。值类型默认值和 Controller 条件会改变真实必填性，因此每个字段同时列出代码校验证据。",
        "- 空集合只表示本次条件没有匹配结果，不能自行推断对象不存在、已经删除或某个业务原因成立。",
        "- 当前查询只能证明调用时事实。历史问题必须使用明确的日志、记录或历史接口，不能用当前状态冒充过去状态。",
        "- 直接响应可能含个人信息、内部 ID 或凭据字段；调用执行器必须按目录标记做最小化投影，不能把完整响应无条件交给模型。",
        "- C 端与商家端即使 Action 同名，也代表不同视角；需要解释差异时应分别取证，不能互相替代。",
        "- 文档中的使用时机只是能力理解示例，不是运行时问题路由；机器目录不包含问题关键词、固定场景到接口映射或固定回答。",
        "",
        "## Agent 选取与调用流程",
        "",
    ]
    if perspective == "顾客视角":
        lines.extend([
            "1. 商家反馈顾客端问题时，先要求商家提供顾客手机号，并确认问题所属门店。手机号只交给受控身份解析流程，不直接拼入任意查询参数。",
            "2. 服务端在已确认门店范围内把手机号解析为目标会员引用；存在同号多会员、跨门店歧义或未找到时停止调用并返回可核实提示。",
            "3. 由执行器注入目标会员 `Uid`、门店 `StoreId`、应用 `AppId` 等上下文，再选择本目录中的 C 端候选查询工具。模型不得生成或改写这些身份值。",
            "4. 只把本次问题需要的脱敏字段交给模型；若需解释商家与顾客看到的数据差异，再调用商家端对应工具交叉核对。",
            "",
        ])
    else:
        lines.extend([
            "1. 从已验证的商家会话注入当前操作人 `Uid`、`StoreId`、`AppId` 和权限上下文，模型不得使用请求正文覆盖身份。",
            "2. 按问题域检索本目录，只选择 A/B 级候选；C 级需要人工复核，D 级不得调用。",
            "3. 商家反馈顾客端展示问题时，转入 C 端流程：取得顾客手机号、限定门店、解析目标会员引用，再以顾客视角查询。",
            "4. 对 C/B 两端结果按字段和数据时点比较，只陈述响应能证明的差异，不把当前状态解释成历史原因。",
            "",
        ])
    lines.extend([
        "### 给工具筛选器的检索建议",
        "",
        "- 不要把整份目录一次性放入模型上下文。先按问题域、工具编号、用途和使用时机召回少量候选，再读取对应的详细契约。",
        "- 第一轮优先 A/B 级；只有候选不足且有人工审批时才考虑 C 级。D 级只用于审计覆盖，不参与召回。",
        "- 同一问题需要多步查询时，上一步返回的内部 ID 只能作为执行器保存的服务端引用传给下一步，不能暴露给模型自由改写。",
        "- 典型顺序是“定位主体 → 查询列表/概览 → 用上游引用查询详情 → 必要时做 C/B 对照”，避免无边界批量拉取。",
        "",
        "## 公共响应包装",
        "",
        "| 包装 | 字段 | 含义 |",
        "| --- | --- | --- |",
        "| `DataResult<T>` | `State`、`StatusCode`、`Message`、`MsgType`、`Data` | 单对象结果；只有 `State=true` 才能把 `Data` 当成功事实 |",
        "| `DataList<T>` | 上述状态字段及 `PageIndex`、`PageSize`、`PageCount`、`TotalCount`、`Data` | 分页列表；空列表不能解释为空的业务原因 |",
        "| `PageData<T>` | `PageIndex`、`PageSize`、`PageCount`、`TotalCount`、`IsNext`、`Data` | 常作为 `DataResult<T>.Data` 的分页载荷 |",
        "",
        "## 工具等级",
        "",
        "| 等级 | 含义 | 运行要求 |",
        "| --- | --- | --- |",
        "| A | 静态路径未发现参数或明显副作用 | 仍需 AI 专用部署的只读验收 |",
        "| B | 候选只读接口，但需要身份注入、上游对象引用或响应脱敏 | 满足约束后才可注册 |",
        "| C | 查询路径存在疑似副作用、凭据参数或语义不充分 | 人工复核通过前不开放 |",
        "| D | 写接口、登录、回调、测试或无法证明只读 | 永久排除或另行审批 |",
        "",
        "## 全部 Action 索引",
        "",
        "| 工具编号 | 业务域 | 方法与路由 | 摘要/用途 | 鉴权 | 等级 | 结论 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for action in sorted(actions, key=lambda item: (infer_domain(item.controller), item.controller, item.action)):
        usage, _ = infer_usage(action)
        lines.append(
            f"| `{action.tool_id}` | {escape_cell(infer_domain(action.controller), 80)} | "
            f"`{action.http_method} /{action.route}` | {escape_cell(usage, 180)} | "
            f"{'需要登录' if action.authenticated else '源码标记免登录'} | {action.grade} | "
            f"{escape_cell(action.grade_reason, 220)} |"
        )

    lines.extend(["", "## 可筛选工具详细契约", ""])
    for action in sorted(
        (item for item in actions if item.grade in {"A", "B", "C"}),
        key=lambda item: (infer_domain(item.controller), item.controller, item.action),
    ):
        usage, when_to_use = infer_usage(action)
        normalized = re.sub(r"^Business", "", action.action, flags=re.I)
        counterparts = [item for item in other_index.get((action.controller.lower(), normalized.lower()), [])
                        if item.grade in {"A", "B", "C"}]
        wrapper, payload_type = unwrap_return_type(action.return_type)
        mutation_calls = [call for call in action.calls if semantic_verb_kind(call.split(".")[-1]) == "write"]
        lines.extend([
            f"### `{action.tool_id}`",
            "",
            "| 项目 | 内容 |",
            "| --- | --- |",
            f"| 业务域 | {escape_cell(infer_domain(action.controller))} |",
            f"| 用途 | {escape_cell(usage)} |",
            f"| 使用时机 | {escape_cell(when_to_use)} |",
            f"| 不应使用 | 写入、修改、支付、退款、核销或无法由响应字段证明的结论；历史问题不能只靠当前结果 |",
            f"| 请求 | `{action.http_method} /{action.route}` |",
            f"| 鉴权 | {'继承登录鉴权基类' if action.authenticated else '源码继承免鉴权基类；AI 部署仍需服务级访问控制'} |",
            f"| 工具等级 | `{action.grade}` — {escape_cell(action.grade_reason)} |",
            f"| 返回 | `{action.return_type}`；包装 `{wrapper or '无已识别包装'}`；Data `{payload_type}` |",
            f"| 数据时效 | {escape_cell(infer_freshness(action))} |",
            f"| 源码 | `{action.source_file}:{action.line}` |",
            f"| C/B 对照 | {escape_cell(', '.join(item.tool_id for item in counterparts[:6]) or '未发现同 Controller/同语义名称的另一视角接口')} |",
            "",
            "#### 请求参数",
            "",
            "| 参数 | 类型 | 必要性 | 代码依据/绑定 | 参数来源 | 业务含义与可见性 |",
            "| --- | --- | --- | --- | --- | --- |",
        ])
        request_rows = render_request_rows(action, catalog)
        lines.extend(request_rows or ["| — | — | 无 Action 业务参数 | — | — | — |"])
        lines.extend([
            "",
            "#### 响应参数",
            "",
            "除下表 `Data` 字段外，始终先检查公共包装的 `State/StatusCode/Message`。",
            "",
            "| 字段路径 | 类型 | 含义 | 敏感等级 | 模型可见性 |",
            "| --- | --- | --- | --- | --- |",
        ])
        lines.extend(render_response_rows(action, catalog))
        lines.extend(["", "#### 代码行为与证据", ""])
        if action.validations:
            lines.append("- Controller 条件：" + "；".join(f"`{normalize_condition(item)}`" for item in action.validations[:12]))
        else:
            lines.append("- Controller 条件：未发现显式 `if` 参数校验；这不代表所有参数都可省略。")
        if action.calls:
            lines.append("- 一层业务调用：" + "、".join(f"`{escape_cell(item, 120)}`" for item in action.calls[:18]))
        else:
            lines.append("- 一层业务调用：静态扫描未识别到标准 Provider/Service 调用。")
        if mutation_calls:
            lines.append("- 疑似副作用：" + "、".join(f"`{item}`" for item in mutation_calls[:10]) + "。人工复核前禁止开放。")
        else:
            lines.append("- 疑似副作用：当前 Action 静态扫描未发现标准写入命名调用；仍需专用部署的只读账号和真实请求验收。")
        if action.errors:
            lines.append("- 显式失败信号：" + "；".join(f"`{escape_cell(item, 180)}`" for item in action.errors[:16]))
        else:
            lines.append("- 显式失败信号：Action 内未提取到固定状态码/提示，需以公共包装和 Provider 返回为准。")
        lines.extend([
            "- Agent 结论边界：只能引用本次成功响应实际返回的字段；不得根据接口名称、空结果或错误提示补造业务原因。",
            "",
        ])

    lines.extend([
        "## 排除项复核规则",
        "",
        "- D 级接口已保留在“全部 Action 索引”中以证明审计范围，但不提供模型调用契约。",
        "- C 级接口只有在确认查询过程不写业务数据、不发消息、不产生支付/核销/退款等外部状态后才能升级。",
        "- 后续新增 Action 必须重新运行生成脚本；如果源码指纹变化而目录未更新，应阻止工具目录发布。",
        "- XML 摘要缺失、DTO 无法解析或 Controller/Provider 结论冲突时，以“待人工复核”处理，不能由 Agent 自行解释。",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def git_commit(repo_root: Path) -> str:
    """记录目录对应的源码提交，失败时给出明确占位而非静默省略。"""

    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=repo_root, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def validate_document(actions: list[ActionDef], document: str, project_key: str) -> None:
    """阻止重复工具编号、索引缺项或等级明细越界进入生成结果。"""

    tool_ids = [item.tool_id for item in actions]
    duplicate_ids = sorted({item for item in tool_ids if tool_ids.count(item) > 1})
    if duplicate_ids:
        raise ValueError(f"{project_key} contains duplicate tool ids: {', '.join(duplicate_ids[:20])}")
    for action in actions:
        index_marker = f"| `{action.tool_id}` |"
        detail_marker = f"### `{action.tool_id}`"
        if document.count(index_marker) != 1:
            raise ValueError(f"{project_key} action index is missing or duplicated: {action.tool_id}")
        expected_detail = action.grade in {"A", "B", "C"}
        if (detail_marker in document) != expected_detail:
            raise ValueError(f"{project_key} action detail violates grade boundary: {action.tool_id}")
    if "## Agent 选取与调用流程" not in document or "## 排除项复核规则" not in document:
        raise ValueError(f"{project_key} document is missing required safety guidance")


def build_actions(repo_root: Path, project_root: Path, project_key: str, perspective: str) -> list[ActionDef]:
    """只枚举 Controllers/WebApi，排除 MVC 页面 Controller。"""

    controller_root = project_root / "Controllers" / "WebApi"
    actions: list[ActionDef] = []
    for path in sorted(controller_root.rglob("*.cs")):
        actions.extend(parse_controller(path, repo_root, project_key, perspective))
    unique: dict[tuple[str, str, str], ActionDef] = {}
    for action in actions:
        key = (action.http_method, action.route.lower(), action.action)
        unique.setdefault(key, action)
    result = list(unique.values())
    # C# 允许同名 Action 分别承载 GET/POST 回调；只在发生冲突时追加方法后缀，保持其余工具编号简洁稳定。
    by_base_id: dict[str, list[ActionDef]] = {}
    for action in result:
        by_base_id.setdefault(action.tool_id, []).append(action)
    for duplicates in by_base_id.values():
        if len(duplicates) > 1:
            for action in duplicates:
                action.id_suffix = action.http_method.lower()
    return result


def validate_action_type_resolution(
    actions: Iterable[ActionDef],
    catalog: ModelCatalog,
    project_key: str,
) -> None:
    """同名根 DTO 必须能由 Controller using 唯一定位，禁止静默选到另一命名空间的契约。"""

    unresolved: list[str] = []
    for action in actions:
        root_types = [parameter.type_name for parameter in action.parameters]
        root_types.append(unwrap_return_type(action.return_type)[1])
        for type_name in root_types:
            root, args = parse_generic(type_name)
            candidates_to_check = args if root in GENERIC_COLLECTIONS else [type_name]
            for candidate_type in candidates_to_check:
                simple_name = clean_type(candidate_type).rstrip("?").split(".")[-1]
                candidates = catalog.types.get(simple_name, [])
                if len(candidates) <= 1:
                    continue
                explicit = clean_type(candidate_type).rstrip("?")
                explicit_namespace = explicit.rsplit(".", 1)[0] if "." in explicit else ""
                matching_namespaces = {
                    item.namespace for item in candidates
                    if item.namespace == explicit_namespace or item.namespace in action.using_namespaces
                }
                if len(matching_namespaces) != 1:
                    unresolved.append(
                        f"{action.tool_id}/{simple_name}=>" +
                        ",".join(sorted(item.namespace for item in candidates))
                    )
    if unresolved:
        raise ValueError(
            f"{project_key} contains ambiguous root DTO resolutions: " + "; ".join(unresolved[:20])
        )


def normalize_document_for_check(document: str) -> str:
    """忽略每次提交或跨日必然变化的元数据，只比较真正影响能力契约的内容。"""

    document = re.sub(r"^- 源码提交：`[^`]+`$", "- 源码提交：`<ignored>`", document, flags=re.M)
    return re.sub(r"^- 生成日期：`[^`]+`$", "- 生成日期：`<ignored>`", document, flags=re.M)


def normalize_manifest_for_check(manifest: dict[str, object]) -> dict[str, object]:
    """复制并移除非契约元数据，避免提交清单本身后立刻造成 sourceCommit 漂移。"""

    normalized = json.loads(json.dumps(manifest, ensure_ascii=False))
    normalized.pop("sourceCommit", None)
    normalized.pop("generatedDate", None)
    return normalized


def check_generated_outputs(
    outputs: list[tuple[Path, str, str]],
    manifests: list[tuple[Path, dict[str, object], str]],
) -> list[str]:
    """返回所有过期或缺失的生成物标签；调用方据此以非零状态阻断 CI。"""

    mismatches: list[str] = []
    for path, generated, label in outputs:
        if not path.is_file():
            mismatches.append(f"{label}:missing:{path}")
            continue
        existing = path.read_text(encoding="utf-8-sig", errors="replace")
        if normalize_document_for_check(existing) != normalize_document_for_check(generated):
            mismatches.append(f"{label}:stale:{path}")
    for path, generated, label in manifests:
        if not path.is_file():
            mismatches.append(f"{label}:missing:{path}")
            continue
        try:
            existing = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            mismatches.append(f"{label}:invalid-json:{path}")
            continue
        if normalize_manifest_for_check(existing) != normalize_manifest_for_check(generated):
            mismatches.append(f"{label}:stale:{path}")
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[6])
    parser.add_argument("--capi-output", type=Path)
    parser.add_argument("--crmapi-output", type=Path)
    parser.add_argument("--capi-manifest-output", type=Path)
    parser.add_argument("--crmapi-manifest-output", type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="只校验现有目录是否与当前源码一致，不改写文件；提交号和生成日期不参与比较。",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    reference_root = repo_root / "Public/LingKe/Lingke.DuckAI/Skills/kexiaomi-product-agent/references"
    capi_output = args.capi_output or reference_root / "capi-api-tool-catalog.md"
    crmapi_output = args.crmapi_output or reference_root / "crmapi-api-tool-catalog.md"
    capi_manifest_output = args.capi_manifest_output or reference_root / "capi-api-tool-manifest.json"
    crmapi_manifest_output = args.crmapi_manifest_output or reference_root / "crmapi-api-tool-manifest.json"
    capi_root = repo_root / "Public/LingKe/Link.CApi"
    crmapi_root = repo_root / "Public/LingKe/Link.CRMApi"
    model_root = repo_root / "Libraries/LingKeModel"
    for required in (capi_root, crmapi_root, model_root):
        if not required.is_dir():
            parser.error(f"required source directory does not exist: {required}")

    # DTO 以两个 API 当前 csproj 的模型项目及其实际使用的微信/公共模型源码为主，同时收录 Controller 内部模型。
    catalog = ModelCatalog(
        repo_root,
        [
            model_root,
            repo_root / "Libraries/LingKe.Common",
            repo_root / "Libraries/WeChat.OpenSdk",
            repo_root / "Libraries/WeChatWork.OpenSdk.Core",
            capi_root / "Controllers/WebApi",
            crmapi_root / "Controllers/WebApi",
        ],
    )
    capi_actions = build_actions(repo_root, capi_root, "capi", "顾客视角")
    crmapi_actions = build_actions(repo_root, crmapi_root, "crmapi", "商家视角")
    validate_action_type_resolution(capi_actions, catalog, "capi")
    validate_action_type_resolution(crmapi_actions, catalog, "crmapi")
    commit = git_commit(repo_root)

    capi_document = render_document(
        repo_root, "capi", "LingKe.CApi", "顾客视角", capi_root,
        capi_actions, crmapi_actions, catalog, commit,
    )
    crmapi_document = render_document(
        repo_root, "crmapi", "LingKe.CRMApi", "商家视角", crmapi_root,
        crmapi_actions, capi_actions, catalog, commit,
    )
    capi_manifest = build_manifest(
        repo_root, "capi", "LingKe.CApi", "顾客视角",
        capi_actions, crmapi_actions, catalog, commit,
    )
    crmapi_manifest = build_manifest(
        repo_root, "crmapi", "LingKe.CRMApi", "商家视角",
        crmapi_actions, capi_actions, catalog, commit,
    )
    validate_document(capi_actions, capi_document, "capi")
    validate_document(crmapi_actions, crmapi_document, "crmapi")
    validate_manifest(capi_actions, capi_manifest, "capi")
    validate_manifest(crmapi_actions, crmapi_manifest, "crmapi")
    if args.check:
        mismatches = check_generated_outputs(
            [
                (capi_output, capi_document, "capi-document"),
                (crmapi_output, crmapi_document, "crmapi-document"),
            ],
            [
                (capi_manifest_output, capi_manifest, "capi-manifest"),
                (crmapi_manifest_output, crmapi_manifest, "crmapi-manifest"),
            ],
        )
        if mismatches:
            print(json.dumps({"status": "stale", "mismatches": mismatches}, ensure_ascii=False, sort_keys=True))
            return 1
        print(json.dumps({"status": "ok"}, ensure_ascii=False, sort_keys=True))
        return 0
    capi_output.parent.mkdir(parents=True, exist_ok=True)
    crmapi_output.parent.mkdir(parents=True, exist_ok=True)
    capi_manifest_output.parent.mkdir(parents=True, exist_ok=True)
    crmapi_manifest_output.parent.mkdir(parents=True, exist_ok=True)
    capi_output.write_text(capi_document, encoding="utf-8")
    crmapi_output.write_text(crmapi_document, encoding="utf-8")
    capi_manifest_output.write_text(
        json.dumps(capi_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    crmapi_manifest_output.write_text(
        json.dumps(crmapi_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    result = {
        "capi": {
            "actions": len(capi_actions),
            "grades": {grade: sum(1 for item in capi_actions if item.grade == grade) for grade in "ABCD"},
            "output": str(capi_output),
            "manifest": str(capi_manifest_output),
            "manifestTools": capi_manifest["manifestToolCount"],
        },
        "crmapi": {
            "actions": len(crmapi_actions),
            "grades": {grade: sum(1 for item in crmapi_actions if item.grade == grade) for grade in "ABCD"},
            "output": str(crmapi_output),
            "manifest": str(crmapi_manifest_output),
            "manifestTools": crmapi_manifest["manifestToolCount"],
        },
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
