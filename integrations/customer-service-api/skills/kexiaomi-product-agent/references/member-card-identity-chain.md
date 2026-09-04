# 会员身份与持卡链路

本参考只定义跨问题复用的实体语义和查询不变量，不定义具体故障流程、固定 SQL 或客服答案。

## 实体语义

- `users` 是平台账号身份。手机号只能通过服务端提供的 `member-mobile` 值来源匹配 `users.user_mobile`。
- `user_card` 是账号在当前门店的会员身份。它可以用于确认会员关系和身份状态，但其汇总字段不能证明某张具体持有卡的状态、类型、有效期或余额。
- `user_card_child` 是会员实际持有的具体卡。具体卡事实必须读取该表，并通过 `user_card.id = user_card_child.card_id` 关联会员身份。

## 身份解析

已领卡会员使用账号链路：以 `users.user_mobile = member-mobile` 定位平台账号，通过运行目录授权的 `users.id = user_card.uid` 关联当前门店会员身份，再通过 `user_card.id = user_card_child.card_id` 读取具体持有卡。允许在一个结构化查询计划中完成这些关联；不得选择、回传或让模型填写 UID 和内部主键。

通过 API-MCP 查询会员详情或其他以当前门店会员身份为范围的私有信息时，必须先由上游身份定位能力取得 `CardId` 短期引用，并在后续查询中携带该引用。`UserId` 只表示平台账号，不能单独确定当前门店的 `user_card` 身份；即使接口兼容只传 `UserId`，Agent 也不得走该歧义分支。该约束按实体身份和工具契约生效，不依赖客户问法或预设客服场景。

本轮没有 `CardId` 时，Agent 不得向客户索取该内部标识。应先使用当前开放的会员定位能力，以客户已经提供且该能力契约明确支持的会员信息换取短期引用；如果必要定位信息尚未提供，只追问一项最小信息。`crmapi.store.get_search_user` 接口本身接受会员完整手机号或至少四位手机号尾号，不接受姓名；当前 DuckAI 安全上下文只采集并注入完整手机号，因此搜索结果的 `CustomerPrompt` 会要求会员完整手机号。不能把姓名填入 `Value`。客户补充后继续原查询目标，不得因缺少 `CardId` 就让客户自行进入后台查询或直接转人工。

`crmapi.store.get_search_user` 的 `Data[].State` 是搜索结果层根据会员身份及其具体持卡情况派生的展示状态；其中 `0` 表示存在正常可用卡。`crmapi.user.business_get_user_info` 的 `Data.State` 是所传 `CardId` 对应的 `user_card` 会员身份状态；`Data.Cards` 是该身份下的未删除具体持卡集合，空数组表示该身份下没有卡。两条路径的 `State` 不属于同一枚举，不能互相套用或直接比较。

未领卡会员使用离线身份链路：以 `user_card.card_tag = member-mobile` 定位当前门店会员身份，并同时使用 `user_card.uid = unclaimed-member`。`unclaimed-member` 是服务端固定为数值 `0` 的受控值来源，模型不得提交 UID 字面值。随后通过 `user_card.id = user_card_child.card_id` 读取具体持有卡。

## 调查边界

- 不直接使用 `user_card_child.card_tag` 定位会员或持有卡。
- 不把 `user_card` 返回的卡名、卡类型、余额或状态描述成会员持有的某张具体卡；具体卡结论只引用 `user_card_child` 证据。
- 一条链路返回空结果只证明该链路和当前条件没有匹配。若尚未确认是否已领卡，应根据已有上下文选择另一条身份链路，不得直接断言会员或卡不存在。
- 只组合当前问题需要的安全业务字段；手机号、UID、会员身份主键和具体卡主键不得出现在工具结果或客户回复中。
