# First-use understanding scores

Use two independent integer scores, 0 through 10 inclusive. They are approximate agent self-assessments of currently available evidence, not validated measurements, percentages, job-match probabilities or judgments of the user's ability. Use the bands below consistently and give one concrete reason for each score. Do not total or average them.

## 1. Career-capability understanding / 职业能力了解程度

| Score | Available evidence |
|---|---|
| 0 | No usable evidence about skills or experience. A desired job alone does not establish capability. |
| 1–2 | An occupation, a skill mention or a broad experience claim, with little detail. |
| 3–4 | Main skills and some work/project history, with few concrete examples. |
| 5–6 | Concrete examples explain what the user did; individual contribution, depth or results still have important gaps. |
| 7–8 | Relevant examples make the user's own contribution, problem-solving approach, results and suitable work reasonably clear. |
| 9–10 | Several detailed, consistent examples support a clear understanding of depth, transferable capabilities and limits for the current career direction. Material unknowns and their implications for the current direction are explicitly understood; not every unknown needs resolving. This is still not independent verification of every claim. |

Choose within a band according to how complete and consistent the relevant evidence is. Separate explicit user statements, accessible documentary support and tentative inference. Job titles, long conversations or repeated claims alone do not justify high scores. Career preferences belong in the recap but are not evidence of professional competence. Do not demand years of experience, salary or formal credentials that are irrelevant to the user's goal.

Career understanding and independent verification are separate. Detailed user-reported contributions and outcomes may justify strong understanding without external proof; retain their provenance and evidence limits. Do not deduct career-understanding points solely for missing third-party audits, payslips, public GitHub or a resume file. Deduct for missing relevant detail, ambiguous personal contribution or unresolved contradictions instead. Knowing an important boundary is informative, not automatically a deficiency. Never restore a predecessor's score or use decimal precision to imply measurement; assess what the current summary actually conveys. Read profile-compiler.md when compression has reduced contributions to keywords.

## 2. Application-material knowledge / 求职资料掌握程度

Consider the materials relevant to the user's current search: resumes, application letters, portfolios and supporting material actually required for the next step. Do not penalize someone for not having unnecessary documents. Distinguish three things in the explanation: **known to exist**, **contents/version understood**, and **currently accessible for use**.

| Score | Available evidence |
|---|---|
| 0 | No usable record of relevant application materials. It does not mean the user has none. |
| 1–2 | Knows that one or more documents exist, without useful content or version knowledge. |
| 3–4 | Has partial contents or a summary, but substantial content, version or access details remain unknown. |
| 5–6 | Understands the core material well enough to draft or tailor content, but original files or current versions remain unavailable/unverified. |
| 7–8 | Understands most relevant materials and versions, with usable files available; some important access or completeness uncertainty remains. |
| 9–10 | Understands the relevant material set and current versions, can access the needed files, and knows which to use for the current task. Sending still requires applicable authorization and a final attachment check. |

A cloud summary naming a resume is not the resume itself. Without access to the necessary originals, do not use the 7–10 bands merely because you remember their contents. When moving to a new device/agent, reassess actual file availability. An accessible file alone is insufficient if it has not been read. If the task uses only a portfolio URL or text, assess those relevant materials rather than requiring a PDF artificially.

## Timing, missing access and cloud saving

Show the scores on first use after setup or in a new agent context. If already shown in the current conversation, do not repeat them on a routine restart, reload or new search. Update when asked or when important new evidence changes the assessment. There is no target score the user must reach.

Restore permitted cloud memory before scoring. If retrieval fails, explain that the assessment is provisional and based only on visible information. Zero reflects no usable evidence available to this agent, not a claim that no cloud records exist. Never fill gaps from unavailable chats, deleted memory or private files the user has not authorized.

For saving and transfer timing follow [profile-sync.md](profile-sync.md). Scores are transient and never saved. During an active handoff, accumulate evidence until its stopping condition rather than saving on every assessment.

## Compact examples — illustrative, never assumed facts

No available information:

> 职业能力了解：**0/10**。当前还没有可用的经历记录。  
> 求职资料掌握：**0/10**。当前还没有可用的求职材料信息。  
> 可以先说想找什么工作，我们边找边了解，不需要先填完整档案。

Useful career knowledge but only a document summary:

> 职业能力了解：**7/10**。已了解主要项目、独立贡献和擅长的问题类型。  
> 求职资料掌握：**5/10**。了解英文简历的主要内容，但当前原文件及版本还未核实。  
> 现在可以先筛选岗位、起草求职信；投递时再核实必要附件。

Already authorized memory, after a verified successful save:

> 已把重要经历和偏好更新到你的 WorldRole 职业摘要，换 Agent 时可以继续读取。原始附件仍需在投递时确认可用。

Match the user's language and keep the opening brief. Do not append a full questionnaire, mandatory recap confirmation or repeated registration prompt. Complete independent work first and ask all remaining essential blockers together.
