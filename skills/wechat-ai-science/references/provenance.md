# 来源、许可与取舍

本技能是根据用户写作需求独立组织的 AI 科普垂类规则，WeWrite 提供确定性本地任务工具。源代码、入口、写作规则及默认档案以根目录 MIT LICENSE 开源。默认档案只包含通用规则，不包含用户文章、运行记录、改稿历史或凭证。

## WeWrite：运行依赖

来源：https://github.com/imraywang/wewrite 。固定版本 4.2.1，提交 `de69e06c2596a0f3e2b0eb3d6229f201d7559584`，MIT；上游许可原文见根目录 `licenses/WeWrite-MIT.txt`。通过 requirements.txt 安装，不随本仓库分发上游源码、环境或通用 skill。自有适配为 scripts/wewrite_local.py、scripts/wewrite_checks.py；没有修改上游代码。工具只用于本地任务、来源、主张、审稿与用户实际改稿学习；不是事实核查模型，也不是操作系统安全沙箱。

## AIWriteX：只借鉴通用设计

来源：https://github.com/iniwap/AIWriteX ，静态检查提交 `1abed0cb47a0a8923a3e26470c139389ebc01998`。只借鉴资料、成稿、编辑分步与平台受众约束的通用设计。未复制代码、提示词、配置或表达，不作为依赖。上游 LICENSE 为 Apache-2.0，NOTICE 另有声明；本仓库 MIT 不覆盖任何上游材料。未来如引入内容须重新审核。

## TrendRadar：排除接入

来源：https://github.com/sansan0/TrendRadar ，检查提交 `ae6e980f8f51ad32924d96e4508a6163efcb2005`，GPL-3.0。未复制代码、不依赖、不安装、不接入热点监控。

## 表达参考

用户对科技报道、口语讲解和纸感封面的偏好被转述为通用规则；不复制参考作者原句、身份、人格或封面作品。用户样本中的事件与数据必须另行核查。正文插图仅作文字占位，封面先提供方案再确认生成。
