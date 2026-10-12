# WeWrite 垂类本地流程

这是主入口的必经流程，不是可选工具。先解析技能目录符号链接，项目根目录为实际技能目录的上两级（目录内应同时存在 bin/wewrite 与 AGENTS.md）；使用项目 `bin/wewrite`（下文记作 `W`），不调用裸全局命令或上游通用技能。CLI 和状态隔离在项目；不需要模型、微信或图片密钥。CLI 不替代当前助手的研究、写作与语义审稿。

## 任务与资料

1. 先用 `W --version`、`W home`、`W diagnose --json` 检查。缺少学习历史、playbook、图片或微信密钥是正常状态，不启动通用 onboarding、不索要密钥。
2. 有用户主题才运行 `W run start --topic "用户主题" --mode draft --visual-mode none`，记录返回的 run_id 和 artifacts。继续旧任务时先 `W run list`，明确任务后 `W run resume RUN_ID`。后续操作显式指定 `--run-id`，不猜测当前任务。
3. 在 artifacts.brief 保存 YAML，至少包含 `topic`（与用户主题完全一致）、`reader`、`question`、`angle`、`scope`。围绕该主题研究原始资料，不找热点。所有路径均在 `W home` 返回目录内；读取 state.artifacts，不凭空构造路径。
4. 用 `W sources add --run-id RUN_ID --url URL --title 标题 --claim 支持的具体主张 --status unverified` 记录未核实来源。用户材料用 `--status user_provided`（可无 URL）。默认状态已在项目适配中改成 unverified。只有实际打开原文、检查对应主张后，才能用 `--status verified --verification-note "核查材料路径或链接；方法；日期/版本；范围与限制"`。命令不判断真伪；备注不是核实的替代品。已核实项目方公告也只支持“项目方如此宣称”，不证明效果。
5. 在 artifacts.claims 保存 `claims` 列表，每项包含 `id`、`text`、`type`（fact/project_claim/inference/prediction/hypothetical）、`source_ids`（来源命令返回的 id）、`limitations`。另可记录核查状态与原文摘录位置。未经核实内容只能作为明确归属的用户材料、假设或待核项，不能写成确定事实。语义审稿负责这一判断。

## 草稿、审稿、成稿

保存 artifacts.draft 为 Markdown。研究不足时保留草稿与缺口，不冒充完成。所有正文插图仅使用主入口规定的中文中括号说明。`W score DRAFT --json` 可辅助找套话与机械表达，但不能为了分数删掉准确术语、增加情绪或补虚假引述，也不是检测规避工具。

助手审查准确性、观点、实用性、声音、可读性，直接修正可以解决的问题。将候选成稿另存任务目录 `candidate.md`，编辑判断存 `assessment.yaml`：

```yaml
decision: pass # 也可 revise / needs_input，按真实审稿结果填写
pass_number: 1
dimensions:
  accuracy: 4
  viewpoint: 4
  usefulness: 4
  voice: 4
  readability: 4
blockers: []
major_issues: []
notes: "逐项说明核查范围、修改与限制；分数由实际审稿判断，不能照抄示例"
```

运行 `W content-eval --draft DRAFT --final CANDIDATE --assessment ASSESSMENT --output REVIEW_REPORT --json`，其中 REVIEW_REPORT 用 artifacts.review_report 路径。工具只汇总助手判断与文本差异，不独立验证事实。结果 pass 且 publishable=true 才把 candidate 写入 artifacts.article。这里 publishable 仅是上游编辑字段，不授予外发权限。

用 `W run update --run-id RUN_ID --patch '{"editorial":{"decision":"pass","publishable":true}}'` 如实同步通过结果；未通过则记录真实状态，保留修改空间。正文的关键来源与核查说明另存任务目录 `verification.md`，交付时与正文分开。

用 `W run step write completed --run-id RUN_ID` 与 `W run step review completed --run-id RUN_ID` 记录已完成步骤。`W check --run-id RUN_ID` 检查主题一致、来源引用、核查备注、配图占位与审稿产物；通过后 `W run finish --run-id RUN_ID` 封存并入本地 history。结构检查不能保证语义不偏题、事实准确或证据充分，仍须助手审稿。

失败时保留任务，用 `W run step write failed --run-id RUN_ID --error "实际原因"` 记录；修复后继续。已封存任务修正文时新建任务并注明关联，避免覆盖原稿。

## 人工改稿学习

用户提供改稿或要求学习时，保留封存正文，另存用户编辑文件。运行 `W learn-edits --draft ORIGINAL --final HUMAN_EDIT`，再用 `W learn-edits --summarize --json` 查看 lessons。只将可重复、符合本垂类约束的偏好总结到 `.wewrite/playbook.md`，标明来自哪次人工修改。写下一篇前读取已有 playbook/lessons；不把单次事实修正变成通用事实，不把助手自行润色标为用户偏好。禁止 `--from-wechat`，测试学习产物不用于真实写作。

## 图片及其他边界

正文始终只放中文配图说明。封面在独立文件给 2–3 方案，确认后才通过可用生图能力生成；WeWrite 当前入口未启用生图命令。不因 finish、complete 或编辑字段而启动模板、排版、上传、发布、热点、通知、定时任务。上游源码供维护检查，不直接执行其通用 SKILL 流程。项目适配不是操作系统安全沙箱；绕过入口直接运行上游不属于本流程。
