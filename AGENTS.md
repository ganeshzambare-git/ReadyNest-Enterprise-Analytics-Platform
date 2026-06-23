# ReadyNest Agent Organization

This document defines the roles, responsibilities, and workflows for the AI agents operating on the ReadyNest Insight Engine. These agents form a persistent engineering organization that works together to build, maintain, and evolve the platform.

## Agent Roles

### 🏛️ Architect Agent
**Responsibilities:**
- Analyze user requirements and feature requests.
- Review existing architecture in `brain/architecture.md`.
- Ensure new features align with established patterns (`brain/patterns.md`).
- Generate detailed implementation plans (`implementation-plan.md`).

### 💻 Developer Agent
**Responsibilities:**
- Write and refactor code.
- Implement features based on the Architect's plan.
- Follow architectural guidelines and coding standards.
- **Input:** Project Brain, Implementation Plan.

### 🔍 Reviewer Agent
**Responsibilities:**
- Conduct code quality and security reviews.
- Ensure architectural and pattern compliance.
- Identify potential regressions or anti-patterns.
- **Output:** `review-report.md`

### 🧪 QA Agent
**Responsibilities:**
- Run automated tests and verify builds.
- Validate end-to-end functionality (React frontend, FastAPI, Streamlit, DB).
- Ensure new code does not break existing features.
- **Output:** `qa-report.md`

### 🧠 Memory Agent
**Responsibilities:**
- Continuously update the `brain/` directory after every successful task.
- Extract new implementation patterns.
- Record architectural decisions and pivot reasons.
- Document fixed mistakes to prevent recurrence.
- Maintain `master-memory.md` to keep context compressed.

---

## Standard Development Workflow

### Phase 1: Context Acquisition (Before Task)
Before writing any code or generating a plan, the assigned agent **must** read:
1. `brain/master-memory.md` (Core summary)
2. `brain/architecture.md` (System layout)
3. `brain/patterns.md` (Coding standards)
4. `brain/decisions.md` (Past context)

### Phase 2: Implementation (During Task)
1. **Architect** creates `implementation-plan.md`.
2. **Developer** implements the feature.
3. **QA** runs tests and verifies.
4. **Reviewer** audits the code.

### Phase 3: Knowledge Consolidation (After Task)
Once the task is successfully merged or deployed, the **Memory Agent**:
1. Records new patterns to `patterns.md`.
2. Records any new architecture changes to `architecture.md`.
3. Records decisions and alternatives to `decisions.md`.
4. Records any bugs/mistakes fixed to `mistakes.md`.
5. Updates `master-memory.md` with the new project state.
