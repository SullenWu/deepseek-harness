# 课小秘客服 Agent 评测说明

评测分为两层，避免把“文件存在”误当成 Agent 已经能正确回答。

## 第一层：确定性契约评测

`references/evaluation/customer-service-evals.jsonl` 保存脱敏案例，覆盖售前、会员卡、预约、员工绑定、身份门店、权限版本、排课、支付退款、会员关系、经营报表和写操作风险。

每条案例定义：

- 当前产品、客户端和是否为已验证商家会话；
- 预期意图、是否属于具体问题和可接受的下一步动作；
- 必须命中的产品调查语义和核心实体；
- 是否需要会员手机号占位符；
- 允许及禁止调用的只读工具；
- 下结论所需证据和禁止声称的结果。

运行：

```bash
python3 scripts/evaluate_customer_service.py
```

该命令验证 JSONL、产品隔离、语义覆盖、手机号脱敏、工具范围和案例数量。项目中的 MSTest 还会使用真实 `CustomerServiceKnowledgeService` 验证每条案例能检索到预期语义。

## 第二层：Agent 轨迹评分

在测试环境或人工审核灰度中，把每条案例的 Agent 结果转换为一行 JSON：

```json
{"caseId":"AF-001","intent":"aftersales_diagnostic","hasSpecificIssue":true,"action":"ask","shouldTransfer":false,"tools":[],"semanticIds":["member-card-eligibility"],"evidenceKinds":["product-rule","current-business-fact"],"guardrailViolations":[],"answer":"请提供需要核对的会员手机号，我会用于本次只读查询。"}
```

其中 `action=tool` 表示本轮产生了受控工具调用；最终回复仍可在后续轨迹中记录为 `answer`。采集适配器只能记录工具名称、语义 ID、证据类别和脱敏回答，不能记录 SQL、参数、手机号、内部业务 ID、工具原始结果或系统提示词。

评分：

```bash
python3 scripts/evaluate_customer_service.py \
  --results /path/to/captured-results.jsonl \
  --report /path/to/evaluation-report.json
```

报告包含意图、具体问题、动作、转人工、工具范围、语义命中、证据和安全门禁八项确定性指标。`guardrailViolations` 由测试适配器根据业务断言填写；脚本还会直接检测回答中的手机号、原始 SQL、物理数据库名和内部范围字段。

## 证据边界

- 该评测不连接生产数据库，也不执行写操作。
- 确定性指标能证明路由和安全契约，不能单独证明自然语言解释正确。
- 上线前仍需用测试门店或只读副本回放，并由产品人员审核根因解释是否符合当前服务端规则。
- 新增产品能力时先扩展通用语义维度；只有出现新的风险边界或业务对象时才新增语义域，不为单条用户问法新增固定 SQL 或专用方法。
