# 分析岗求职工作流

适用方向：Business/Data/BI、Growth/Marketing/Advertising、Product/Revenue/Monetization、GTM/Strategy & Operations。

## 一次日常找岗

1. 先读取 `.local/private/profile.json`、本地真实投递记录和已有排除决定。只读取查重所需字段。
2. 运行 `python3 custom/search_plan.py --profile .local/private/profile.json`。这是检索计划，不是实际搜索；不运行旧 healthcare planner 作为分析岗默认入口。
3. 执行有希望的检索，并结合 LinkedIn、Jobright 和公司官网。开放式日常请求先深入 5–8 个高潜岗位，默认以找到 3 个已核验且未重复的候选为停止条件；用户指定更大范围时按指定范围执行。
4. 回官网核对真实地点、完整 JD、实际年限、签证条款和申请入口。0–2 年优先，明确 3 年降权单独判断，4 年及以上排除；Senior 不只凭标题判断。美国 Remote 不等于全球 Remote。
5. 湾区、纽约、美国 Remote、Atlanta、DFW 优先；Charlotte 补充，其他城市按匹配、薪资、签证和搬迁条件判断。不能用“仅湾区或 Remote”过滤。
6. 签证明确拒绝现在或将来支持则排除；历史 H-1B 记录、当前资格和本岗位支持意愿分别记录。未知不写成拒绝，也不写成已确认支持。
7. 保存来源、岗位ID、发布日期（未知留空）、首次发现时间、最后核验时间和缺口。未读到或访问被拦不是岗位关闭。
8. 推荐清单写入待投池；只有实际提交或可核验的确认才记录申请事件。内推请求、OA邀请、OA完成、面试安排是不同事件。
9. 更新后运行 `python3 custom/workspace.py build`。此步骤不读 Gmail、不搜网页、不申请、不发私信。

## 可复制任务 Prompt

> 按 custom/WORKFLOW.md 和当前私有 profile 找美国分析岗。先查重，以近期 ATS、LinkedIn、Jobright 和官网补漏，核验原始 JD、地点、年限、签证及申请入口。交付最多三个高质量候选，保留无法核验项，不降低标准凑数。所有日期和事件必须有证据。找岗不授权投递、私信、上传简历或定时任务。

## 定时任务

本项目不安装任何调度，也不自动执行搜索。将上面 Prompt 配置到你选择的调度工具前，应明确执行频率、来源、查重路径及通知条件。没有新且值得行动的发现时保持安静，不把生成计划称为完成搜索。

## 继承组件的边界

上游 `工具/healthcare岗位抓取/` 保留原路径供面板兼容，里面的科研/医疗打分、博士/博后规则不适用于此定制版，不应直接用于分析岗筛选。`skills/` 和原 `prompts/` 保留为上游参考，默认使用本文件和 custom/search_plan.py；未安装到用户全局 skills。
