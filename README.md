# 公众号 AI 科普写作 skill

面向已了解 AI、希望深入学习的读者。用户给定主题或标题后，完成原始资料核查、中文科普正文、独立来源说明与封面方案。使用 WeWrite 作为本地任务与编辑记录底座；写作与语义核查由运行 skill 的助手执行。

## 安装与使用

需要 macOS/Linux（Windows 使用 WSL）、Git、Python 3.11+，以及能够联网读取资料的 Codex 环境。安装依赖需要访问 GitHub 与 Python 包索引。推荐 Python 3.12；已在 Python 3.12 验证。

```sh
git clone https://github.com/DarkHummingbird/wechat-ai-writer-skill.git
cd wechat-ai-writer-skill
python3 scripts/setup.py
bin/wewrite --version
bin/wewrite diagnose --json
```

若 `python3` 版本较旧，用已安装的 `python3.12` 等执行 setup。安装脚本在仓库内创建 `.venv` 与 `.wewrite`，将通用默认规则复制到本地状态，并建立项目 skill 发现链接。重复运行不会覆盖已有风格、配置或同名 skill。不会安装全局 skill，不需要公众号或图片密钥，不需要配置模型服务。依赖安装使用正常 pip 配置与固定版本；没有禁用 TLS 验证。

在 Codex 中打开本仓库作为工作目录，重新加载项目技能，然后提出：

> 使用 $wechat-ai-science，围绕“你指定的主题”写一篇公众号文章，核查关键说法，给出配图占位、独立来源说明和封面方案。

不要只把 SKILL.md 复制到全局目录：本 skill 需要仓库里的 bin、scripts 和本地状态。完整流程见 [本地任务流程](skills/wechat-ai-science/references/wewrite-workflow.md)。

## 范围

- 只写用户指定主题；联网用于该主题研究，不主动找热点。
- 区分事实、项目宣称、亲测、推断和预测；不虚构采访、引语、体验或测试。
- 正文只放具体中文配图占位；封面先给两至三个方案，用户确认后才生成。
- 保存 brief、sources、claims、draft、assessment、article、verification 与历史记录；来源 verified 必须附实际核查说明。
- 仅在用户提供真实改稿或要求学习时进行本地改稿学习。
- 不启用热点监控、模板排版、上传发布、通知或定时任务。

入口限制是项目工作流约束，不是操作系统沙箱。结构检查和 content-eval 记录不能替代助手事实核查；publishable 字段只表示编辑通过，不构成外发授权。

## 文件与隐私

`skills/` 是写作规则，`scripts/` 是安装与本地适配，`bin/wewrite` 是统一入口，`defaults/` 是不含私人内容的初始规则。`.wewrite/` 是运行时资料、文章、用户改稿及配置；`.venv/` 是安装环境，两者均被忽略。发布仓库不包含下载的上游仓库、历史文章、测试输出、凭证或本机绝对路径。

## 依赖与许可

本项目 MIT，见 [LICENSE](LICENSE)。WeWrite 固定为 4.2.1 / `de69e06c2596a0f3e2b0eb3d6229f201d7559584`，独立安装，不分发其源码；MIT 归属原文见 [licenses/WeWrite-MIT.txt](licenses/WeWrite-MIT.txt)。其他 Python 依赖及间接依赖固定在 requirements.txt，各自保留上游许可。

AIWriteX 仅作为通用设计参考，TrendRadar 已排除；两者均不作为依赖，不包含其代码或提示词。详见 [来源与取舍](skills/wechat-ai-science/references/provenance.md)。
