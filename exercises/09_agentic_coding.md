# Module 09: Agentic coding

1h

Agents and chatbots have opened large perspectives in scientific applications, from
coding assistance to hypothesis generation. In this module, we just want to discuss
how agents are currently used and how they should be employed to generate image
analysis pipelines in a scientific context.

## How do you use LLMs?

- Do you code on your own or do you systematically get help from coding agents?
- Do you have the agents modify your code or do you copy paste suggestions?
- How often do you fully understand the code that the agent produced?
- What's the different between copy pasting results from an agent and from stackoverflow?
- Do you use agents for coding only or also to drive your analysis/hypotheses/experiments?

## How do we use coding agents?

- Planning, specs, implementation
- Rubber-ducking problems
- Quickly generate known boiler plate code
- Rapid prototyping of an idea
- Simple questions: remind me how to call this function from this library

BUT code is always checked, changed, corrected, and updated by us.

## How to use agents responsibly?

There is no perfect recipe, it will heavily depend on the task and the current state of whichever model you are using.

- Do some background research on what is possible or logical to do to achieve your goal
- Make a technical plan with the agent, ask it to keep it simple and non-verbose, updated into a .md file on disk
- Include verifiable intermediate steps (e.g. known results) and save intermediate states
- Make the pipeline modular, where each module can be independently tested and verified
- Always review the updated plan
- Use git to version control the code base and results (e.g. csv files)
- Don't publish what you don't understand

## Discussion

- Accountability
- Scientific integrity
- Understanding of the method
- Re-usability
- Bloated code bases






## How do we use coding agents?

Example: user comes to the facility with 3000+ lines of code of a pipeline and they want
us to fix some aspects of it prior to publication. We will most likely not review the
code, as it is already too late to untangle whatever the pipeline is. We would start from
scratch building the pipeline up.

## How to use agents responsibly







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