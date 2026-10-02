# CS230 — Deep Learning, Autumn 2025

Independent local textbook following nine Stanford CS230 recordings. Open [index.html](index.html) for the searchable reading edition. The recordings supply the topic sequence; mathematical developments, finite numerical examples and worked exercises are independently authored additions.

| Book chapter | Recording lecture | Reading page |
|---|---|---|
| 1 | 1 | [Learning curves and capacity](lecture-01-introduction-to-deep-learning.html) |
| 2 | 2 | [Supervised, self-supervised and weak supervision](lecture-02-supervised-self-supervised-and-weakly-supervised-learning.html) |
| 3 | 3 | [The full project cycle](lecture-03-full-cycle-of-a-deep-learning-project.html) |
| 4 | 4 | [Adversarial robustness and generative models](lecture-04-adversarial-robustness-and-generative-models.html) |
| 5 | 5 | [Reinforcement and preference learning](lecture-05-deep-reinforcement-learning.html) |
| 6 | 6 | [AI project strategy](lecture-06-ai-project-strategy.html) |
| 7 | 8 | [Agents, prompts and retrieval](lecture-07-agents-prompts-and-rag.html) |
| 8 | 9 | [Career advice and finite decision models](lecture-08-career-advice-in-ai.html) |
| 9 | 10 | [Inspecting a model](lecture-09-whats-going-on-inside-my-model.html) |

There is no recording Lecture 7 in the approved playlist. The [source manifest](source-manifest.json) preserves exact recording identities and numbering. [The source map](source-map.html) separates recording material, research extensions and original teaching constructions. [Primary references](references.html) identify supported claims and explicit source-access limits.

The reader includes offline MathJax, desktop/mobile layouts, a chapter table of contents, theme and text controls, expandable solutions, printing with solutions, code copying and index search. The [numerical laboratory](numerical-lab.html) explores detector base rates and dependent attempts; its [Python checks](numerical_lab.py) use the standard library. Each chapter contains its own separate runnable mathematical fixture and full solutions. These fixtures check finite models rather than reproduce neural benchmarks.

## Local use

Open `index.html` directly, or serve this directory locally:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8000/` yourself. No model API, training service or GPU is required. Chapter programs that import NumPy need NumPy installed; the course lab uses only Python's standard library.

```powershell
python numerical_lab.py
```

## Evidence and limitations

Raw recordings, slides, machine transcripts and acquired research copies remain outside this reader directory. Transcript hashes establish source identity, not transcription accuracy. Timestamp links are navigation anchors, and unavailable visual demonstrations are not represented as independently verified video behavior. Speaker judgments, company claims, empirical studies and formal results remain distinct in the chapters.

This is a local reading edition. Complete source and accessibility certification requires the remaining explicitly recorded source-access checks and a human screen-reader review. Matching artifact hashes and passing numerical/reader checks establish their recorded scopes, rather than the absence of every scientific or accessibility defect. Current validation outcomes are recorded in `validation-summary.json`; no publication or live-site claim is made.
