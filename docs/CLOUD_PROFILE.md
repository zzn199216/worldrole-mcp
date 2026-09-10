# 云端职业摘要 / Cloud career summaries

网页版、不会长期记忆的 Agent、换设备后的新对话，都可以复用同一份求职方向、偏好和关键经历。WorldRole 保存精简摘要，Agent 负责从你允许使用的信息中整理；你不用为了注册重新填一份简历。

## 按你使用的客户端连接

- **支持远程 MCP 和网页登录授权：**连接 `https://mcp.worldrole.work/mcp`，选择 OAuth，在 WorldRole 页面注册或登录，允许职业摘要访问。客户端需要申请 `boardwork:read profile:manage`。这是最适合兼容网页客户端的方式，不必把密钥复制到聊天里。
- **支持 MCP，但只接受个人密钥：**在[账号页](https://mcp.worldrole.work/account)生成密钥，放入客户端的私有凭证设置。请 Agent 指导配置，不要把密钥当作普通聊天内容发送。
- **没有 MCP 或外部工具能力：**使用 https://mcp.worldrole.work/onboarding 复制含已有档案的提示词（也可生成只读临时链接），再粘贴 AI 整理的 JSON，预览确认后保存。也可下载摘要交给新 Agent。注册本身不授予普通网页 AI 自动读写能力。

不同网页产品的接入入口、套餐和管理策略可能不同。服务器提供标准 OAuth/PKCE 与个人密钥连接；是否能在某个具体网页中完成授权，仍需在该客户端实际验证。

连接后，可以告诉 Agent：

> 先读取我的 WorldRole 职业摘要，再结合这次对话帮我找工作。已有信息直接复用，重要变化在我允许的范围内更新，剩余必要问题一次问齐。

第一次介绍账号记忆即可，不要每次搜索都要求注册或确认。只读连接、缺少授权或保存失败时，要说明当前没有保存成功；不要悄悄转成游客后声称已经同步。已有只读 OAuth 授权不会自动获得摘要权限，需要重新授权。对不支持 MCP 的网页，整理结果须由用户预览确认保存；输出 JSON 不代表已经同步。

## 保存范围与控制

摘要最多 8 KB，包含职业方向、技能与经历概要、地点及工作许可、薪资偏好、可工作时间、明确限制和下一步等重要信息。不同 Agent 使用同一账号时共享这份摘要，并非每个对话独立一份。

不保存完整对话、简历附件、邮箱内容或本地申请记录。它能提供可回看的信息依据，不能保证 Agent 不会误解。你可以让 Agent 查看、修改、清空或停止记忆；清空后换客户端也不会自动恢复旧内容。只有重要信息变化时才保存，冲突时先读取最新版本，合并仍然有效的修改。

## English

Web clients, agents without persistent memory and new devices can reuse the same concise career summary. The agent organizes permitted facts; registration does not require completing another resume form.

- **Remote MCP with OAuth:** connect `https://mcp.worldrole.work/mcp`, sign in on WorldRole and approve career-summary access. Request `boardwork:read profile:manage`. No API key needs to enter the conversation.
- **MCP with API-key settings:** create a key on the [account page](https://mcp.worldrole.work/account) and store it in private client credentials, not chat text.
- **No MCP/external tools:** use https://mcp.worldrole.work/onboarding to copy instructions with the existing summary, paste the AI’s JSON back, and preview/confirm saving. A temporary read-only link or downloaded summary is also available. Registration alone grants no automatic read/write access to a web chat.

Client features, plans and administrative policies vary. The server supports OAuth/PKCE and personal keys; end-to-end support must be verified in the particular web client. Existing read-only OAuth grants require fresh consent for profile access and are never silently upgraded.

Ask: “Read my WorldRole career summary first, reuse what is known, save important changes within my permission, and collect essential remaining questions together.” Explain cloud memory once, not on every search. Report missing authorization or failed saves honestly.

The summary holds up to 8 KB of career goals, skills, experience, preferences, constraints and next steps. The same account shares one summary across clients; conversations do not each receive separate profiles. Full chats, attachments, emails and local application records are not synchronized. Users can ask their agent to inspect, update, clear or pause memory. Deletion/pause survives reconnection. Save meaningful changes only and reload/merge on version conflicts. A stored summary provides a reference, not a guarantee against model mistakes.

## 新 Agent 的交接 / Handoff

按 [交接指南](../skills/worldrole/references/profile-sync.md)，由接收端先复用云端资料，针对实际缺口生成给熟悉用户的网页 AI 的提问。用户粘回回答后，接收端整理并提交；不比较两端分数。默认一轮，有有效新增和重要缺口才继续。服务器只校验保存，不用模型重新解释职业档案。

The receiving client asks targeted questions through the user, reconciles the answers and compiles changed fields. Stop on sufficient task evidence or no useful additions, not equal model scores. The server validates and stores; see the linked guide for version checks and submission modes.
