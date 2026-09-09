# Applications and mail / 申请与邮件

## 中文

本地 companion 0.2.0 提供申请草稿、附件校验、发送记录、到期跟进队列，以及可选的 SMTP 发信和 IMAP 回复检查。远程 WorldRole 的八个工具没有因此增加邮件功能。

推荐顺序：**复用用户已经连接的邮箱工具 → 需要时配置本地 SMTP/IMAP**。找工作和准备草稿不需要邮箱账户，也不需要购买另一项服务。邮箱供应商可能限制 SMTP/IMAP 或收费；优先复用已有连接，勿承诺所有邮箱均免费。

1. 从已允许的对话、职业摘要和用户提供的材料开始。Agent 自己查职位要求、公司页面与投递方式，只把真正无法解决的必要信息一次列给用户。
2. Agent 写好求职信，检查实际可用的简历附件，用 `prepare_application` 保存。返回的 `digest` 绑定收件人、正文、主题和附件内容。草稿修改时传入旧的 `expected_digest`；不会覆盖已经发出的记录。
3. 在用户已经授权的范围内发信：已有邮箱工具可直接执行，之后用 `record_application_event(kind="host_sent")` 保存实际回执；可提供真实 RFC `Message-ID`，便于本地 IMAP 匹配。也可用 `send_application` 发送该 digest 对应的完整草稿。若用户尚未授权，先把收件对象、内容和材料准备好，再一次取得所需授权。配置邮箱不等于授权投递。
4. `get_applications` 返回待处理事项与默认七天后的跟进队列。检查最新邮箱后，仍无回复才用 `prepare_application_followup` 准备一次跟进；它保留邮件引用头，仍需要覆盖跟进的用户授权才能发送。默认最多一次，不无限催促。
5. 已有邮箱工具读取正文并记录结果；可选 `sync_application_replies` 只读取最近 50 封 INBOX 邮件的部分头部，以 `In-Reply-To/References` 精确匹配。本地发现非自动回复即暂停跟进。Agent 再用邮箱工具阅读完整线程，核实发件人和要求。
6. 自动确认收件无需打扰。已有资料能回答的常规补件请求，Agent 在既有授权内处理。面试安排、谈薪、录用决定、要求本人身份验证或承诺等进入 `handoff`：只交给用户简洁的背景、对方要求、期限和建议回复。普通拒信可以汇总；明确重要结果和临近期限及时提醒。

`host_sent` 等手动事件标为 `agent_reported`，不能替代真实回执。SMTP 的 `sent` 仅表示服务器接受，不能保证送达、阅读或申请完成；仍可能退信。超时后 `unknown` 不允许直接重发，必须先查邮件服务记录。进程意外退出留下的 `sending` 也需人工核查，不能自行改成成功或重试。不要把“找不到 Sent 文件夹中的记录”当作未发送证明；本地 SMTP 不自动保存 Sent 副本。

### 本地设置

调用 `get_application_capabilities` 查看能力与数据目录，不会输出凭证。默认目录：Windows `%LOCALAPPDATA%/WorldRole`；macOS/Linux `~/.local/share/WorldRole`。可用私有环境变量 `WORLDROLE_DATA_DIR` 指定独立绝对目录。申请、正文、收件地址、授权摘要和回执保存在本机 SQLite；附件放在此目录的 `attachments/`，总计最多 10 MiB、最多五个。Agent 只能复制用户已经提供或授权选用的文件。

通过 MCP 客户端的私有进程环境设置以下变量；不要把真实值写进 README、版本库或对话：

| 功能 | 环境变量 |
|---|---|
| SMTP over TLS，端口 465 | `WORLDROLE_SMTP_HOST`, `WORLDROLE_SMTP_USER`, `WORLDROLE_SMTP_PASSWORD`, `WORLDROLE_SMTP_FROM` |
| IMAP over TLS，端口 993 | `WORLDROLE_IMAP_HOST`, `WORLDROLE_IMAP_USER`, `WORLDROLE_IMAP_PASSWORD` |

这是可选的账户/应用密码模式，不包含 OAuth 登录流程或 STARTTLS；已经连接的 OAuth 邮箱通常更省心。本地文件没有应用层加密，应使用本人系统账户和磁盘保护，勿选共享/同步目录。停止 MCP 后，删除该私有目录可清除本地记录和缓存；它不会删除已发出的邮件或云端职业摘要。

**没有后台服务。** MCP 工具只在被调用时工作。持续检查需要用户授权且确实运行的宿主调度器；未配置时应明确说“下次运行时检查”，不能承诺离线提醒。可配置的宿主任务应定期检查邮箱、读取队列，在授权范围处理必要跟进；无变化和自动回执保持安静，只有有意义的结果、期限或需要用户行动时提醒。正文读取、复杂回复、表单提交与 CAPTCHA 仍依赖宿主现有工具或本人操作。

## English

The local 0.2.0 companion adds private drafts, attachment integrity checks, receipts, due follow-ups, optional SMTP sending and IMAP reply-header checks. The hosted WorldRole service still exposes its original eight tools.

Prefer an already connected mailbox. Search and drafting need no mail account. Optional SMTP/IMAP uses the user's provider; provider availability, limits and fees vary.

1. Reuse permitted conversation, profile facts and supplied documents. Inspect the real job and application channel. Ask for all remaining essential gaps together.
2. `prepare_application` saves completed text and selected existing attachments. Its digest binds the recipient, subject, body and attachment hashes. Revise an unsent draft with its previous `expected_digest`.
3. Send only within actual user delegation. With host mailbox tools, save the real receipt using `record_application_event(kind="host_sent")`; supply the RFC `Message-ID` if available. Alternatively, `send_application` sends the exact prepared digest through private SMTP settings. Configured credentials are not permission. If delegation is missing, prepare the concrete recipients/materials first and ask once for the necessary scope.
4. `get_applications` returns attention and due queues, including older records. The default follow-up is due after seven days. Check the mailbox first; `prepare_application_followup` prepares one threaded follow-up only while still awaiting a reply. Sending requires applicable delegation. No endless chasing.
5. Use host mailbox tools for full conversation review. Optional `sync_application_replies` reads selected headers from the latest 50 INBOX messages, matches exact reply references, and pauses follow-ups on nonautomatic replies. It does not read message bodies or verify recruiter identity. Host-sent messages need their actual RFC Message-ID for local matching.
6. Keep automatic acknowledgments quiet. Resolve routine document requests from available material within delegation. Hand off interviews, negotiation, offers, identity checks and personal commitments with concise context, deadline and a suggested reply. Consolidate ordinary rejections; surface meaningful outcomes and approaching deadlines.

Manual events are `agent_reported`, not independent verification. SMTP `sent` means server acceptance, not delivery, reading or completed application. Reconcile `unknown` outcomes with actual provider evidence before retrying. A process crash can leave `sending` and requires operator investigation; never assume success or resend. SMTP does not save a Sent-folder copy, so absence there is not proof of non-delivery.

`get_application_capabilities` returns configuration booleans and the data directory, never credentials. Defaults: `%LOCALAPPDATA%/WorldRole` on Windows, `~/.local/share/WorldRole` elsewhere. Use private `WORLDROLE_DATA_DIR` for another absolute directory. SQLite stores application text, recipient addresses, authorization summaries and receipts locally. Put user-selected files in its `attachments/` folder, at most five files totaling 10 MiB. Files are not encrypted by this application; use a private OS account/protected disk and avoid shared/synced directories. After stopping the MCP, deleting the private directory clears local records/cache, not sent emails or cloud profiles.

Private process variables: `WORLDROLE_SMTP_HOST`, `WORLDROLE_SMTP_USER`, `WORLDROLE_SMTP_PASSWORD`, `WORLDROLE_SMTP_FROM` for SMTP TLS port 465; `WORLDROLE_IMAP_HOST`, `WORLDROLE_IMAP_USER`, `WORLDROLE_IMAP_PASSWORD` for IMAP TLS port 993. Never commit actual values or paste them into chat. This optional account/app-password mode does not implement OAuth or STARTTLS; existing OAuth mailbox connections are usually easier.

**No background executor is included.** Tools run only when called. Ongoing monitoring requires an authorized, running host scheduler. Otherwise say that checking resumes on the next run. A configured host task should inspect replies and queues, perform in-scope follow-up, and stay quiet unless a meaningful outcome, deadline or user action arises. Full-body reading, complex replies, application forms and CAPTCHA require host tools or the user.
