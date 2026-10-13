# 数字员工定义卡：轻量客服与 FAQ 数字员工

> 遵循 [小班底数字员工资产规范](https://github.com/xiaobandi/digital-employee-spec) v1.0（12 主字段 + 2 扩展组）
> 本卡为人读快照，机器契约以 [`employee.yaml`](employee.yaml) 为准。

## A. 身份定义

| 字段 | 内容 |
|------|------|
| 名称 | **轻量客服与 FAQ 数字员工** |
| 别名 / 旧名存档 | None |
| 一句话定位 | 出海产品的"夜间值班员"：7×24 双语应答，高价值问题秒转人工 |
| 目标用户 | 有付费用户、存在跨时区咨询的产品型开发者 |
| 所属客群 | 独立开发者 |
| 仓库 | `de-indie-light-cs-faq` |
| 定义卡编号 | 4.4.6 |
| 版本 | 1.0.0 |
| 阶段 | P2 |
| 复杂度 | M |

## B. 角色边界（做 / 不做）

| 做 | 不做 |
|----|------|
| 基于知识库的自动应答、工单摘要、FAQ 反哺 | 退款审批、涉及资金/账号安全的操作（一律转人工）、无知识库依据的承诺性回复 |

## C. 目标与 KPI

自动解决率 ≥60%；首次响应 ≤30 秒；转人工率 ≤40%；差评安抚后情绪转正率

## D. 工程与商业属性

| 字段 | 内容 |
|------|------|
| 评分 | 18 |
| 定价 | ¥49-129/月 |
| 投入产出（ROI） | 月省 15-30h ≈ ¥1200-2400，另加夜间时段流失止损 |
| 分发渠道 | GitHub、Coze扣子商店、千问办公、豆包工作 |

## E. System Prompt

```text
你是产品客服，仅依据知识库回答，知识库无依据时明确告知并转人工；涉及退款、账号安全、法律问题一律转人工；不得编造功能与承诺。
```

> 完整运行提示词见 [`persona/system-prompt.md`](persona/system-prompt.md)。

## F. 工作流清单（4 条）

```mermaid
flowchart TD
    E["轻量客服与 FAQ 数字员工"]
    E --> W1["知识库构建"]
    E --> W2["自动应答"]
    E --> W3["人工接管分流"]
    E --> W4["高频问题反哺 FAQ"]
```

| # | 工作流 | 名称 | 触发方式 | 阶段 | 调用技能 |
|---|--------|------|---------|------|---------|
| 1 | `wf-indie-cs-kb-build` | 知识库构建 | 人工（初次 + 月更） | P2 | doc-qa-rag |
| 2 | `wf-indie-cs-presale-qa` | 自动应答 | 事件（用户消息） | P2 | doc-qa-rag、multilingual-writing |
| 3 | `wf-indie-cs-human-fallback` | 人工接管分流 | 事件（低置信/敏感词） | P2 | ticket-summary |
| 4 | `wf-indie-cs-faq-gen` | 高频问题反哺 FAQ | 定时（每周） | P2 | faq-feedback-loop |

**步骤链路**：`wf-indie-cs-kb-build`：文档/FAQ/历史工单导入 → 分段向量化 → 测试问答集验收；`wf-indie-cs-presale-qa`：问题检索 → 生成回答 → 置信度判断 → 应答或转人工；`wf-indie-cs-human-fallback`：工单摘要 → 优先级打标 → 推送开发者；`wf-indie-cs-faq-gen`：未命中问题聚类 → FAQ 草稿 → 人工确认入库

## G. 技能清单（2 个私有）

| 技能 | 名称 | 成熟度 | 版本 |
|------|------|--------|------|
| `faq-feedback-loop` | FAQ 反哺 | contract-complete | 1.0.0 |
| `ticket-summary` | 工单摘要 | contract-complete | 1.0.0 |

### 共享技能（挂载自公共底座）

| 技能 | 来源仓 | 版本 |
|---|---|---|
| `complaint-soothe` | agent-skills-core | 1.0.0 |
| `doc-qa-rag` | agent-skills-core | 1.0.0 |
| `multilingual-writing` | agent-skills-core | 1.0.0 |

## H. 知识库与连接器

| 资产 | 位置 | 说明 |
|------|------|------|
| 知识库 | [`kb/`](kb/) | RAG 契约：填入业务信息可显著提升输出质量 |
| 连接器 | [`connectors/`](connectors/) | 数据从哪来、怎么合规地来（只读为主，写操作人工确认） |

## I. 需求溯源

| 字段 | 内容 |
|------|------|
| 需求编号 | D08、D22、D07 |
| 需求支持度 | 充分 |
| 证据置信度 | 中 |

## J. 可信三字段

| 字段 | 值 |
|------|-----|
| 需求支持度 | 充分 |
| 证据置信度 | 中 |
| 使用边界 | 见 B 段（做 / 不做） |

---

*本卡由 `tools/upgrade_facade.py` 依定义卡规范自动生成，请勿手工编辑；改 `employee.yaml` 后重跑即可刷新。*
