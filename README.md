# 轻量客服与 FAQ 数字员工

> 出海产品的"夜间值班员"：7×24 双语应答，高价值问题秒转人工
>
> **4.4.6**　·　独立开发者　·　阶段 P2　·　
> 复杂度 M　·　¥49-129/月　·　定义卡 4.4.6

## 演示（真实执行录播）

![演示](workflows/wf-indie-cs-faq-gen/docs/images/08-demo-run.gif)

*真实执行回放（GIF 自动循环，非摆拍）· [▶ 观看完整版 MP4](workflows/wf-indie-cs-faq-gen/docs/images/08-demo-run.mp4) · 台账见 [`reports/real-run/wf-indie-cs-faq-gen.md`](reports/real-run/wf-indie-cs-faq-gen.md)*

![架构](docs/images/architecture.svg)

## 效果（真实执行）

![真实效果](workflows/wf-indie-cs-faq-gen/docs/images/00-effect.png)

*上图为**真实效果对比**，不是示意图：左栏是输入材料与要求，右栏是该次执行的产出原文，
两栏取自同一次真实执行记录。*

- 完整台账：[`reports/real-run/wf-indie-cs-faq-gen.md`](reports/real-run/wf-indie-cs-faq-gen.md)
- 录屏与终端回放：[`workflows/wf-indie-cs-faq-gen/docs/images/`](workflows/wf-indie-cs-faq-gen/docs/images/)（`08-demo-run.gif` / `08-demo-run.mp4` / `04-terminal-run.png`）
- 使用示例：[`workflows/wf-indie-cs-faq-gen/docs/使用示例.md`](workflows/wf-indie-cs-faq-gen/docs/使用示例.md)
> 实测判定：**通过**　·　可用度 4/5　·　编造数字 0 处　·　红线命中 2 次 / 拦截 2 次


**一句话**：有付费用户、存在跨时区咨询的产品型开发者

---

## 这个数字员工解决什么问题

出海产品的"夜间值班员"：7×24 双语应答，高价值问题秒转人工

| 项 | 内容 |
|---|---|
| 服务对象 | 有付费用户、存在跨时区咨询的产品型开发者 |
| 可量化目标 | 自动解决率 ≥60%；首次响应 ≤30 秒；转人工率 ≤40%；差评安抚后情绪转正率 |
| 投入产出 | 月省 15-30h ≈ ¥1200-2400，另加夜间时段流失止损 |
| 需求依据 | D08、D22、D07 |
| 分发渠道 | GitHub、Coze扣子商店、千问办公、豆包工作 |

## 30 秒上手

```bash
git clone <本仓库地址> && cd de-indie-light-cs-faq
pip install pyyaml
python3 tests/run.py            # 先跑一遍自检，确认环境与契约都对得上
```

试用（把 `<输入>` 换成本人真实材料）：

```text
请以「轻量客服与 FAQ 数字员工」的身份，帮我跑「知识库构建」。
材料如下：<输入>
要求：只使用材料里出现过的数字，缺的写 <待填>；对外文案停在待确认状态。
```

详细接入见 [`docs/01-安装与接入.md`](docs/01-安装与接入.md)。

## 仓库结构

```text
de-indie-light-cs-faq/
├── employee.md            # 人读定义卡（12 主字段 + 2 扩展组，由 employee.yaml 生成）
├── employee.yaml          # 机器契约（能力清单 + 依赖锁）
├── dependencies.yaml      # 对 core 的外部依赖（含版本）
├── persona/               # 运行提示词 / 边界 / KPI
├── skills/                # 私有原子技能（2 个）
├── spec-bindings/         # 有意不公共化能力的本地绑定声明（0 个）
├── workflows/             # 本员工工作流（4 条）
├── kb/                    # 知识库 RAG 契约
├── connectors/            # 连接器绑定（只读为主，写操作人工确认）
├── docs/                  # 六类发布文档
└── tests/                 # 自动化多场景测试
```

## 私有原子技能（2）

| 技能 | slug | 复杂度 | 阶段 | 成熟度 |
|---|---|---|---|---|
| `FAQ 反哺` | `faq-feedback-loop` | S | P2 | 契约完备 |
| `工单摘要` | `ticket-summary` | S | P2 | 契约完备 |

## 平台公共技能依赖（3）

| 技能 | slug | 全平台复用员工数 |
|---|---|---|
| `差评安抚话术` | `complaint-soothe` | 3 |
| `文档问答（RAG）` | `doc-qa-rag` | 3 |
| `多语言写作` | `multilingual-writing` | 3 |

> 这些技能来自 `agent-skills-core@1.0.0`，本仓库**只引用不复制**。

## Spec 绑定层（0）

（无）

> 这一族能力**有意不公共化**（与外部平台接口强绑定）。本仓不存正文，
> 只留本地绑定声明与连接器配置。

## 工作流（4）

| 工作流 | slug | 触发 | 阶段 | 调用技能数 |
|---|---|---|---|---|
| `知识库构建` | `wf-indie-cs-kb-build` | 人工（初次 + 月更） | P2 | 1 |
| `自动应答` | `wf-indie-cs-presale-qa` | 事件（用户消息） | P2 | 2 |
| `人工接管分流` | `wf-indie-cs-human-fallback` | 事件（低置信/敏感词） | P2 | 1 |
| `高频问题反哺 FAQ` | `wf-indie-cs-faq-gen` | 定时（每周） | P2 | 1 |

## 知识库与连接器

- 知识库语料：['产品文档', 'FAQ 库', '历史工单库（RAG，周更，这是本员工的核心资产底座）']
- 连接器：LLM 推理 API、平台发布端点（Coze/Dify/WorkBuddy）、RAG 知识检索

## 质量与验收

| 项 | 值 |
|---|---|
| 技能文件数 | 122 |
| 多场景用例数 | 182 |
| 用例通过 | 182 |
| 验收结论 | ✅ 通过 |

完整报告：[`docs/05-验收与测试.md`](docs/05-验收与测试.md)

## 许可

专有许可，详见 [`LICENSE`](LICENSE)。
