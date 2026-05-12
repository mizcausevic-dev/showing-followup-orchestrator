# Why We Built This

**showing-followup-orchestrator** grew out of repeated work around real estate operations, where the hardest problems were rarely about raw data collection. The real challenge was turning scattered evidence into something humans could govern quickly.

The recurring pressure in this space showed up around lead-routing delays, discoverability gaps, and weak follow-up discipline across the buyer journey. In practice, that meant teams could collect logs, metrics, workflow state, documents, or events and still not have a good answer to the hardest questions: what is drifting, what matters first, who owns the next move, and what evidence supports that move? Once a system reaches that point, the problem is no longer only technical. It becomes operational.

That is why **showing-followup-orchestrator** was built the way it was. The repo is a deliberate attempt to model a real operating layer for brokerages, real-estate teams, and growth operators. It is not just trying to present data attractively or prove that a stack can be wired together. It is trying to show what happens when evidence, prioritization, and next-best action are treated as first-class product concerns.

The surrounding tooling was not useless. CRM tools, listing plugins, and marketing platforms each handled a slice of the work. But they still left out a coherent operating layer that linked discovery, routing, follow-up, and brokerage accountability. That gap kept turning ordinary review work into detective work.

That shaped the design philosophy:

- **operator-first** so the riskiest or most time-sensitive signal is surfaced early
- **decision-legible** so the logic behind a recommendation can be understood by humans under pressure
- **review-friendly** so the repo supports discussion, governance, and iteration instead of hiding the reasoning
- **CI-native** so checks and narratives can live close to the build and change process

This repo also avoids trying to be a vague platform for everything. Its value comes from being opinionated about a real problem: Real estate follow-up engine for post-showing sequencing, buyer-intent scoring, and agent reminder workflows.

What comes next is practical. The roadmap is about closed-loop conversion analytics, deeper brokerage reporting, and stronger schema publishing workflows. The point of the repo is to turn that messy middle layer into something teams can actually work with.