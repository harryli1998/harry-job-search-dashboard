# Career Compass · 分析岗求职面板

面向 Business、Data、Growth、Marketing、Product、Revenue 和 GTM 分析岗位的本地求职工作区。基于 [HenryVarro666/job-search-dashboard](https://github.com/HenryVarro666/job-search-dashboard) 定制，保留原作者 MIT 许可及版权。

## 这个版本改了什么

- 主导航聚焦今天、近期发现、待投岗位和投递进度；不展示博士实习入口。
- 演示职位改为分析岗，页面明确标注全部演示记录虚构。
- 新增读取配置的 ATS 检索计划，使用 America/Los_Angeles 日期，覆盖六类 ATS 域名、四组分析职位及轮换城市。
- 加入分析岗工作流与年限、城市、签证证据和查重约束。
- 公共配置不包含真实授权身份或投递历史；个性化配置、地址、联系方式和真实记录只保存在忽略目录 `.local/private/`。
- 空白私人工作区与公开演示独立生成。不会从私人工作区生成公开 demo。

## 立即预览

下载仓库后直接打开 [demo/index.html](demo/index.html)，无需服务器、密钥或依赖。GitHub 文件页展示源代码，需下载 HTML 后用浏览器打开。演示报告日期固定为 2026-10-27，不能当作实时岗位或 Harry 的真实申请结果。

Python 3.10+：

```sh
python3 custom/workspace.py demo   # 重建虚构演示，不读取私人文件
python3 custom/workspace.py init   # 一次性建立空白私人工作区；已有目录不覆盖
python3 custom/workspace.py build  # 生成本地私人面板
python3 custom/search_plan.py --profile .local/private/profile.json
```

私人面板位置：`.local/private/工具/求职进度面板/dashboard.html`。
先在 `.local/private/profile.json` 填写或确认自己的搜索配置。工作身份、年限与到岗信息需用真实且最新的事实填写，不能从示例推断。个人版导入真实记录应先核对来源和事件类型，不扫描邮箱、不把未知日期补成今天。

## 日常使用

详见 [定制工作流与可复制 Prompt](custom/WORKFLOW.md)。默认近期计划有 24 个带地点的检索及 6 个不限日期的美国补漏检索，地点轮换并非全组合穷尽覆盖。生成计划不会搜索网络或验证岗位；需要有搜索工具的执行者逐条保存证据。没有自动登录、投递、私信或定时任务。

上游面板支持筛选、全局查找、详情抽屉、申请事件时间线、OA 状态、统计、去向图、配色和移动端布局。维护实际数据仍使用本地 JSON，不提供在线编辑数据库。

## 验证

```sh
npm ci --ignore-scripts
python3 scripts/check.py                  # 上游完整回归套件
python3 -m unittest discover -s custom -p 'test_*.py'
node custom/test_dom.cjs  # 先生成 demo，并 init/build 私人空白工作区
```

完整保留上游通用引擎。旧科研、医疗、博士和博后规则属于上游参考，不是此版本默认找岗政策。来源说明见 [UPSTREAM.md](UPSTREAM.md)，原文说明见 [docs/UPSTREAM_README.md](docs/UPSTREAM_README.md)。

## 隐私和许可

生成的个人 HTML 内嵌数据，必须与原始记录一样保密。只公开本仓库内的虚构 demo，不上传 `.local/`、私人配置、申请材料或账户记录。MIT；Copyright 2026 Chao Cao，详见 [LICENSE](LICENSE)。本定制版不宣称上游代码为独立原创。
