# Design references / 参考与取舍

Reviewed on 2026-09-10. These are design references, not imported implementations or claims of interoperability tests.

| Reference | Adopted idea / 借鉴点 |
|---|---|
| [HireBridge/jobops](https://github.com/HireBridge/jobops) | Reuse career materials and maintain an application/follow-up workflow. 复用职业材料，区分准备与实际投递。 |
| [vijay-prabhu/jobsearch-mcp](https://github.com/vijay-prabhu/jobsearch-mcp) | Track correspondence and who is waiting for whom. 跟踪回复与下一步责任；本项目用引用头匹配线程，不按公司名合并邮件。 |
| [jgalea/mailbox-mcp](https://github.com/jgalea/mailbox-mcp) | Prefer reusable mailbox capabilities for thread reading, drafts and replies. 优先复用已有邮箱工具，避免重复配置。 |
| [Jobicy API](https://jobicy.com/jobs-rss-feed) | Public feed, attribution and hourly refresh policy. 免费聚合补充，并尊重来源及刷新频率。 |
| [Arbeitnow API](https://www.arbeitnow.com/blog/job-board-api) | Additional European jobs with explicit coverage limits. 欧洲岗位补充，不把一页结果宣传为完整检索。 |

Original implementation: no upstream code copied. No upstream data license is replaced by this repository's MIT license. We deliberately expose partial failures, bounded coverage, unknown send outcomes and absent background execution. 这些边界让 Agent 能完成真实工作，而不会把草稿说成投递成功、把自动回执说成面试邀请。
