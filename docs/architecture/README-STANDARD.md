# Infinity Repository README Standard

Use this structure when normalizing any Infinity subsystem README.

## 1. Title + one-sentence role

State what the repository is for in plain language.

## 2. Status

Use explicit labels:

- Concept
- Model
- Prototype
- Implemented
- Verified
- Needs verification

A repository can contain more than one status at once. Mark sections individually when needed.

## 3. System role

Explain where the repository sits in Infinity and what other repositories it depends on or serves.

## 4. Problem statement

Describe the problem the project is trying to solve without overstating whether the solution already works.

## 5. Core architecture

Use a simple block diagram before detailed prose.

```text
Input
  |
  v
Processing / physical mechanism
  |
  v
Control / verification
  |
  v
Output
```

## 6. Repository layout

Document real files and directories only. If a proposed layout does not yet exist, label it `Proposed repository layout`.

## 7. Theory and known science

Separate:

### Established background
Facts supported by standard references or measured behavior.

### Infinity hypothesis
The project's proposed extension, interpretation or mechanism.

### Open questions
What has not yet been demonstrated.

## 8. Implementation

Document code that actually exists, entry points, runtime requirements, supported platforms and known limitations.

Do not describe simulated UI behavior as physical hardware behavior.

## 9. Security / safety

For software:
- threat model
- permissions
- local/remote trust boundaries
- secrets/key handling
- dependency risks

For physical or scientific projects:
- hazards
- safe test boundaries
- what should remain simulation-only until qualified facilities are available

## 10. Validation

Every major claim should map to one of:

```text
claim -> measurement -> test -> expected result -> actual result -> confidence
```

Keep proposed tests separate from completed results.

## 11. Sources

Prefer primary sources: papers, standards, official documentation, measured datasets and manufacturer specifications.

Avoid placeholder citations such as `[arXiv]`, `[YouTube]` or `[wikipedia]` without an exact source.

## 12. Roadmap

Use concrete deliverables rather than vague expansion prompts.

Example:

- [ ] separate hypothesis from established background
- [ ] add runnable simulation
- [ ] add test dataset
- [ ] document interfaces
- [ ] publish validation results

## Companion-file pattern

For research-heavy repositories:

```text
README.md
KNOWN-PHYSICS.md
HYPOTHESIS.md
MODEL.md
EXPERIMENTS.md
RESULTS.md
SOURCES.md
SAFETY.md
```

For software-heavy repositories:

```text
README.md
ARCHITECTURE.md
API.md
SECURITY.md
TESTING.md
ROADMAP.md
```

For hardware-heavy repositories:

```text
README.md
DESIGN.md
MATERIALS.md
SCHEMATICS.md
CONTROL.md
SIMULATION.md
SAFETY.md
TEST-PLAN.md
RESULTS.md
```

## Preservation rule

Never delete a useful original Gemini theory simply because it is speculative. Move it into the appropriate theory/hypothesis document, clean its formatting, preserve attribution/history where relevant, and make the README accurately state its current evidence level.

## Language rule

Avoid absolute claims such as `unhackable`, `impossible to weaponize`, `zero attack surface`, `perfect equilibrium`, or `self-sustaining` unless they have been demonstrated under a defined threat/test model. Replace them with precise engineering claims that can be tested.

## Goal

The Infinity documentation layer should make it possible to read the entire system in two directions:

```text
Infinity master map -> subsystem -> component -> test/result
```

and

```text
individual experiment -> component -> subsystem -> Infinity master map
```

That turns the repository collection into a navigable technical knowledge system instead of a pile of disconnected READMEs.
