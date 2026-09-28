# Module 09: Agentic coding

Agents and chatbots have opened large perspectives in scientific applications, from
coding assistance to hypothesis generation. In this module, we just want to discuss
how agents are currently used and how they should be employed to generate image
analysis pipelines in a scientific context.

## What are people worried about?

There are many worries thata are often discussed when it comes to agentic AI in science,
beyond job security and the worth of skills that took a while to acquire.

- Loss of skills
- Loss of creativity
- Increased cognitive load
- Over-engineered solutions
- Methodological flaws
- Lack of understanding

Agents can create thousands of lines in the space of minutes, by design the code will
run and coding errors will be fixed by the agents. But does the final pipeline make sense?
Is it methodologically sound?

Reviewing hundreds of lines of code is hard, and it is easy to give in and just let the
agents snowball into whatever solution seems to output what we want.

Example: user comes to the facility with 3000+ lines of code of a pipeline and they want
us to fix some aspects of it prior to publication. We will most likely not review the
code, as it is already too late to untangle whatever the pipeline is. We would start from
scratch building the pipeline up.

## How to use agents

There is no perfect recipe, it will heavily depend on the task and the current state of
whatever model you are using.

- Do some background research on what is possible or logical to do to achieve your goal
- Know what you want to do, not what results you expect
- Make a technical plan with the agent, ask it to keep it simple and non-verbose, updated
into a .md file on disk
- Include verifiable intermediate steps and save intermediate states
- Make the pipeline modular, where each modules can be independently tested and verified
- Always review the updated plan
- Use git to version control the code base and non-binary results





