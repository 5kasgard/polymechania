# Review of routing.md by Llama 3.3 70B (Workers AI, free), 2026-10-29

Kept as received.

Here's a review of the document in under 250 words as a numbered list:

1. **Missing routing dimension**: The document does not consider the dimension of "worker utilization" or "worker workload", which could impact the decision of which worker to assign a job to. For example, a worker that is already heavily utilized may not be the best choice for a new job, even if it is the strongest or cheapest option (Section 2, "What decides the route").
2. **Testing rule that still lets bias in**: Rule 8 in Section 3, "Unbiased testing", states that the bias of the test's author should be stated, but it does not provide a clear mechanism for mitigating this bias. This could potentially allow bias towards the author's preferred vendor or model (Section 3, "Unbiased testing", rule 8).
3. **Vague or contradictory rule**: The document states that "the decision stays the planner's" (Section 2, "The decision"), but it also provides a set of rules for routing work to workers. It is unclear how these rules are used in conjunction with the planner's decision, or how conflicts between the rules and the planner's decision are resolved (Section 2, "The decision" vs. Section 2, "What decides the route").
