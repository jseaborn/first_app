# LinkedIn Post 4: The design problem (revised from McKinsey source)

McKinsey looked at 50+ agentic AI builds and the finding that sticks with me is this: organizations keep focusing on the agent instead of the workflow. They build impressive demos that don't improve the actual work. Some companies have had to rehire people where agents failed.

The report says the teams getting value are the ones redesigning entire workflows, not just dropping an agent into an existing process. And their framework for doing that is interesting. They argue most tasks in a workflow don't need agents at all. Rule-based and repetitive work gets automated. Extractive tasks get basic gen AI. Classification and forecasting get predictive analytics. You only reach for an agent when you've got multi-step decisions with high variability. Everything else in the workflow gets the simplest technology that handles it.

That's a design problem. But it doesn't look like any design problem I was trained for.

I've been doing product design for over twenty years. The job, as I learned it, is about making tools usable. You design screens, flows, interactions. The user is in control. Your job is reducing friction between what someone wants to do and the tool that helps them do it.

Agentic AI flips that. The agent does the work. The human evaluates it. And evaluating someone else's work is a completely different cognitive task than doing it yourself. Anyone who's managed people knows this. You're reading output you didn't produce, trying to decide if it's good enough, often in a domain where "good enough" is hard to define.

So the design question isn't "can the user accomplish their goal?" anymore. It's "can the user tell whether the agent accomplished it correctly?" Most of the design patterns we've spent decades refining don't help with that second question.

McKinsey's report has a detail that I keep coming back to. One insurer in the study built their agent review interface so that AI summaries appeared alongside the source documents with auto-scrolling and bounding boxes highlighting what the AI referenced. User acceptance hit 95%. The AI itself didn't change. They just made verification fast enough that people would actually do it.

That intervention came from watching people struggle, not from a product spec. Nobody wireframed it. It's closer to the kind of problem-solving you see in operations design or process engineering than in a typical product design sprint.

McKinsey also talks about treating agent onboarding like employee onboarding. Give agents job descriptions. Run evals. Provide continuous feedback. The language is telling. We've moved from designing tools to designing working relationships. The agent isn't an interface element. It's a collaborator that's sometimes wrong and can't tell you when.

The instinct most product designers have, the one I have, is to make things smooth. Remove friction. Get out of the user's way. In agentic workflows, some of that friction is what makes the system work. Take it out and you get the failure modes the report keeps documenting: humans rubber-stamping bad output because checking it is too hard, or re-doing everything from scratch because they don't trust any of it.

The skill set this actually needs is closer to organizational design than product design. You're deciding how much autonomy the agent gets. Where humans have to engage deeply. How to signal confidence and uncertainty. What happens at the edges when the system breaks down. Those are management questions dressed up as interface questions. And I think most of us in design are going to have to learn a different set of muscles to get them right.

Source: [One year of agentic AI: Six lessons from the people doing the work](https://www.mckinsey.com/capabilities/quantumblack/our-insights/one-year-of-agentic-ai-six-lessons-from-the-people-doing-the-work) (McKinsey / QuantumBlack)
