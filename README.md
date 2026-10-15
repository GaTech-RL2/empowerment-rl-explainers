# Empowerment · Visual RL

[Watch the six films and explore the labs](https://gatech-rl2.github.io/empowerment-rl-explainers/)

Six original **7-minute narrated videos** centered on empowerment papers by Benjamin Eysenbach and collaborators: **42 minutes, 36 chapters, 108 derivation steps**. Each film includes animated diagrams, equations, captions, a full transcript, source notes, and an interactive mathematical experiment.

| Film | Primary paper | What the lesson develops |
| --- | --- | --- |
| [1 · DIAYN](https://gatech-rl2.github.io/empowerment-rl-explainers/diayn.html) | [Diversity Is All You Need](https://arxiv.org/abs/1802.06070), Eysenbach et al., ICLR 2019 | Skills as messages, mutual information, variational decoding, intrinsic reward |
| [2 · Geometry](https://gatech-rl2.github.io/empowerment-rl-explainers/geometry.html) | [The Geometry of Empowerment](https://arxiv.org/abs/2610.07796), Ji et al., October 2026 preprint | Discounted occupancy, the probability simplex, information radius, channel capacity |
| [3 · Scaling](https://gatech-rl2.github.io/empowerment-rl-explainers/scaling.html) | [Scaling Empowered Agents](https://arxiv.org/abs/2610.13002), Ji et al., October 2026 preprint | Inner skills, outer preparation, decoder and value approximations, measurement bottlenecks |
| [4 · Representations](https://gatech-rl2.github.io/empowerment-rl-explainers/representation.html) | [Learning to Perceive the World Through Control](https://arxiv.org/abs/2605.30656), Bastankhah et al., ICML 2026 | Forward and backward equivalence, independent nuisance cancellation, minimality assumptions |
| [5 · Human assistance](https://gatech-rl2.github.io/empowerment-rl-explainers/assistance.html) | [Learning to Assist Humans without Inferring Rewards](https://arxiv.org/abs/2411.02623), Myers et al., NeurIPS 2024 | Human influence, two contrastive predictors, density-ratio cancellation, takeover |
| [6 · Language agents](https://gatech-rl2.github.io/empowerment-rl-explainers/language.html) | [Training LLM Agents to Empower Humans](https://arxiv.org/abs/2510.13709), Ellis et al., ICML 2026 | Entropy versus surprisal, likelihood proxies, stopping thresholds, selective fine-tuning |

The teaching sequence combines intuition, derivation, worked examples, and geometric visuals, inspired by the requested Jia-Bin Huang and 3Blue1Brown presentation references. The scripts, diagrams, and animations are original. Narration is the neutral synthetic macOS Samantha voice. This independent collection is not produced or endorsed by those creators or the paper authors.

## Follow-up literature

[What can an agent learn with the skills it has?](https://gatech-rl2.github.io/empowerment-rl-explainers/literature.html) is a searchable, annotated guide to 19 primary papers on dynamics identification, information-seeking exploration, skill composition and acquisition, curriculum selection, and transfer limits. It includes eight Eysenbach-coauthored papers, a suggested reading order, a proposed research structure, a rope-manipulation experiment sketch, and downloadable BibTeX/JSON. The literature guide is a written companion; it is separate from the six video topics. Rebuild it with `python3 src/literature.py`.

## Watch and experiment

Open `index.html` locally, or use the hosted collection. Keep the `assets`, `media`, `previews`, `captions`, `transcripts`, and `code` directories with the HTML. The complete player, lab code, and lesson data are embedded; playback and experiments require no API key or network access. Burned captions work even where a browser restricts local-file caption tracks.

For a local server with video seeking support:

```sh
python3 serve.py --port 8772
```

Open `http://127.0.0.1:8772`. Films are H.264/AAC, 1600 × 900, 20 fps. Each MP4 includes six chapter markers and a selectable subtitle stream; captions are also visible in the film. Each lesson has a direct HTML entry point, MP4 download, VTT/SRT captions, and plain-text transcript.

## Mathematical labs

The labs are exact finite-channel teaching experiments, not reproductions of the papers’ trained agents or benchmarks. Information quantities use **natural logarithms and nats**. The browser code and standard-library Python implementation compute:

- Mutual information, skill posteriors, and a variational decoder bound.
- Finite-channel capacity with Blahut–Arimoto and an explicit upper/lower gap.
- A two-context example separating potential, learned skills, decoding, and estimator bias.
- Independent nuisance cancellation and the distinction between state entropy and control.
- Human action priors, path clearance, takeover, and a hypothetical task outcome.
- Cumulative surprisal, a strict stopping threshold, and the corresponding sequence-probability floor.

The full Python source is visible inside every lab and downloadable as `code/empowerment_lab.py`.

```sh
python3 code/empowerment_lab.py
python3 -m unittest discover -s code -p 'test_*.py'
```

The scripts preserve important limits: mutual information is a weighted average KL for a fixed prior; channel capacity optimizes that prior; population variational bounds do not certify arbitrary neural predictions; representation results require their stated optimality and minimality conditions; the LLM method uses a proxy and target selection rather than exact empowerment policy-gradient RL.

## Rebuild

Use Python 3.12+, FFmpeg, and ffprobe. Narration regeneration uses **macOS `say` with Samantha**, without a remote API. Other platforms can reuse the delivered MP4s or supply aligned audio/timings. Audio chunks are cached by text, voice, and speaking rate. Caption boundaries come from the measured durations of those chunks.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python src/prepare_audio.py
.venv/bin/python src/prepare_math.py
.venv/bin/python src/render_all.py
.venv/bin/python src/render.py --previews
.venv/bin/python src/build_site.py
```

`src/content.py` contains the complete original lesson scripts. `content.json` adds aligned narration, chapter, and derivation timestamps. `src/scenes.py` draws the animated diagrams. `src/labs.js` computes the interactive examples. No third-party browser scripts, analytics, or CDN assets are needed.

## Verification and sources

`src/verify_media.py` checks duration, streams, chapter counts, ordered beat/caption timing, audio levels, and full video/audio decoding. With the local server running, `qa/verify_site.py` checks all six players, chapter navigation, slider boundaries, desktop/mobile layout, offline labs, and Python/JavaScript numerical agreement. Browser checks use an installed Google Chrome through Playwright; change its executable path for another platform.

Primary paper URLs, consultation dates, and PDF checksums are recorded in `sources/manifest.json`. PDFs were read for research and are linked rather than redistributed. The transcripts and notes identify original examples and distinguish them from paper claims. The October 2026 work is labeled as preprints rather than peer-reviewed results.

Related collections: [Reset-free RL](https://gatech-rl2.github.io/reset-free-rl-explainers/) · [TAMP](https://gatech-rl2.github.io/tamp-explainers/).
