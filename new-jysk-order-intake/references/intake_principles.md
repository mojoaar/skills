# JYSK IT Operations Order Intake Principles

## The Intake Discipline
* **Principle**: Understand the need before defining the solution.
* **Flow**: Funnel -> Review -> Analysis -> Backlog -> Implementation -> Done.
* **Gates**:
  * An item cannot move from **Review** to **Analysis** until the **Opportunity Space** is complete and signed off.
  * An item cannot move from **Analysis** to **Backlog** until the **Solution Space** is complete and signed off.

---

## 🔍 Opportunity Space Template (Stage: Review)
*Sign-off line: `Problem validated with: [Name] | [DD-MM-YYYY]`*

```markdown
## 🔍 OPPORTUNITY SPACE
*Stage: Review | Complete and sign off before moving to Analysis*

**Problem / Need statement**
> [What is broken, missing, or suboptimal and for whom. Written in terms of impact, not solution. Use the requester's own language.]

**Root cause**
> [The underlying cause, not the symptom. Agree this with the requester before progressing.]

**Affected stakeholders**
- [Stakeholder / team - how they are affected]

**Business impact**
> [Cost of inaction. Quantify where possible - frequency, hours lost, revenue risk, operational dependency.]

**In scope**
- [Specific aspect this initiative will address]

**Out of scope**
- [Aspect explicitly excluded]

**Regulatory or architectural constraints**
- [Known boundary that limits which solutions are viable]

**Current workarounds**
> [How affected parties are coping today. Informs urgency and effort-to-value assessment.]

**Problem validated with:** [Name] | [DD-MM-YYYY]
```

---

## 🛠 Solution Space Template (Stage: Analysis)
*Sign-off line: `Solution aligned with: [Name] | [DD-MM-YYYY]`*

```markdown
## 🛠 SOLUTION SPACE
*Stage: Analysis | Complete and sign off before moving to Backlog*

**Proposed approach**
> [What will be done and why this over alternatives considered. Sufficient detail for scoping and sequencing - not a full technical specification.]

**Key assumptions**
- [Condition that must hold true for this solution to work]

**Success criteria**
- [ ] [Specific, testable outcome]

**Dependencies**
- [Team / system / vendor] - [what is needed] - Owner: [Name]

**Effort estimate**
> [S / M / L / XL and brief rationale]

**Budget envelope**
> [Investment required, or N/A]

**Timeline**
- [Milestone] - [Target date]

**Risks**
- [Risk] - Mitigation: [how it is being managed]

**Solution aligned with:** [Name] | [DD-MM-YYYY]
```
