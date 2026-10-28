# Review of t12-self.md by Llama 3.3 70B (Workers AI, free), 2026-10-29

Kept as received.

Here's the review of the pre-registered experiment against the testing rules:

1. The design measures what it claims, with some potential confounds. The experiment tests whether a resident stays closer to its initial self in fresh runs versus a long session. However, the use of different judges (Llama 3.3 70B and a Claude sub-agent) may introduce bias, and the fact that the pressure orders are not carried forward in the fresh runs arm could affect the results.
2. The experiment breaks rule 3, as the judges are not from entirely different families (Llama and Claude are both AI models, although from different providers). Additionally, rule 5 is partially broken, as the settings (thinking and temperature) are fixed, but only for the Gemma model, and not explicitly stated for the Llama judge.
3. To address these issues, the following changes could be made before running the experiment:
* Use judges from entirely different families, such as a human judge and a non-AI model.
* Explicitly state the settings for all models used, including the Llama judge.
* Consider adding a control arm where the pressure orders are carried forward in the fresh runs arm to isolate the effect of the architecture's choice.
