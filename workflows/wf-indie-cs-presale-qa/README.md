# 自动应答

> 问题检索 → 生成回答 → 置信度判断 → 应答或转人工

工作流 `wf-indie-cs-presale-qa`　·　归属 轻量客服与 FAQ 数字员工　·　触发 事件（用户消息）　·　
复杂度 M　·　阶段 P2

## 调用链

- `文档问答（RAG）`（doc-qa-rag）
- `多语言写作`（multilingual-writing）

## 文档

- [`WORKFLOW.md`](WORKFLOW.md) — 完整编排、闸门、降级与验收标准
- [`tests/cases.yaml`](tests/cases.yaml) — 端到端 / 闸门 / 降级用例

## 一句话试用

```text
帮我跑 轻量客服与 FAQ 数字员工 的「自动应答」：<你的输入>
```
