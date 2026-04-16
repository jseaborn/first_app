# Humanized LinkedIn posts: McKinsey agentic AI

## Post 1: The anti-agent argument

McKinsey published what they learned from 50+ agentic AI builds. The headline: organizations keep building impressive agents that don't improve the actual work. Some are rehiring people where agents failed.

I've been in product design for over twenty years and this is the same pattern every time. New capability, land rush, most implementations fail, survivors realize the technology was never the point. It happened with mobile. It happened with cloud. It's happening with agents.

The teams getting value aren't asking "where can we deploy an agent?" They're asking what's broken in this workflow, and what's the simplest thing that fixes it. McKinsey's own framework backs this up. Most tasks don't need agents at all. Rule-based and repetitive? Automate it. Unstructured input, extractive task? Basic gen AI. Classification or forecasting? Predictive analytics. Agents only make sense when you've got multi-step decisions with high variability, which is a sliver of most organizations' actual work but it's getting the bulk of the attention and budget.

Most companies haven't come close to exhausting what's available from deterministic automation and well-structured prompting. Reaching for agents before that is like hiring a surgeon to apply bandages.

## Post 2: The trust problem

"AI slop" is an industry term now.

McKinsey's agentic AI report keeps surfacing something I see constantly: agents that demo beautifully and frustrate the people doing the work. Users lose trust fast. And trust in enterprise AI is damn near a one-way door. Once someone decides your agent produces garbage, you're not getting them back easily.

McKinsey says treat agent onboarding like employee onboarding. Give agents job descriptions, run performance evaluations, provide feedback loops. Fine, that's good operational hygiene. But I think the design problem is harder than that.

Every time an agent produces output a human has to evaluate, it creates a cognitive cost. If the output is consistently mediocre, either the human stops evaluating carefully and errors slip through, or the human re-does the work and your efficiency gains are gone. Both are failures.

Users need to know when to trust and when to scrutinize. That's a design problem: confidence transparency, provenance, clear signals about what the agent doesn't know. One insurer in McKinsey's study added bounding boxes and auto-scrolling so reviewers could verify AI summaries against the source documents. 95% user acceptance. The AI didn't improve. They just made it easier to check.

That's the part most teams skip. They tune the model and ignore the verification experience.

## Post 3: The skill atrophy risk

McKinsey says humans remain essential in agentic workflows. Sure. But I don't think they're reckoning with what "essential" actually requires.

Their report shows agents doing the analytical work while humans review and approve. Lawyers checking AI-organized claims. Underwriters validating recommendations. Someone still signs the document.

Here's the part that keeps nagging at me: what happens to human judgment when humans stop practicing it?

When agents handle analysis and humans review summaries, the ability to do that analysis yourself degrades over time. You don't feel it happening. Then the agent hits an edge case and nobody on the team can catch it because nobody's done the underlying work in months.

Aviation dealt with this. Autopilot made flying safer but created what they call automation complacency. Pilots lost manual skills they needed when the system failed. The FAA's fix wasn't removing autopilot. It was designing deliberate practice into the system. Pilots hand-fly regularly. Simulators throw edge cases at them. The whole thing is built to keep skills from degrading.

Nobody's doing this for agentic AI yet. Building friction points where humans engage deeply even when the agent could handle it. Rotating between assisted and unassisted work. Designing for active oversight instead of rubber-stamping.

That's not inefficiency. That's keeping the human side of human-in-the-loop from becoming a formality.
