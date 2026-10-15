"""Curated primary-source literature map; summaries and synthesis are original."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
PAPERS=[]
def add(id,title,authors,year,venue,url,topics,evidence,mechanism,limit,use,ben=False,priority=0):
    PAPERS.append(dict(id=id,title=title,authors=authors,year=year,venue=venue,url=url,topics=topics,evidence=evidence,mechanism=mechanism,limit=limit,use=use,eysenbach=ben,priority=priority,consulted='2026-10-15'))

add('slap','SLAP: Shortcut Learning for Abstract Planning','Y. Isabel Liu; Bowen Li; Benjamin Eysenbach; Tom Silver',2026,'ICLR 2026','https://arxiv.org/abs/2511.01107',['skills','curriculum'],'Method + simulated robot experiments',
'Builds an abstract planning graph from existing TAMP options, then learns new low-level policies that shortcut paths through that graph.',
'The main formulation assumes known deterministic dynamics, full observability, an abstraction, and base options sufficient for the task distribution. It does not establish which arbitrary new skills are learnable in an unknown world.',
'The closest match to starting with programmed skills and deciding which additional skills could make plans better. Read Sections 3–4 and the limitations before transferring it to a new setting.',True,1)
add('symbols','From Skills to Symbols: Learning Symbolic Representations for Abstract High-Level Planning','George Konidaris; Leslie Pack Kaelbling; Tomas Lozano-Perez',2018,'JAIR 61','https://cs.brown.edu/people/gdk/pubs/orig_sym_jair.pdf',['skills','dynamics'],'Representation theory + robot experiments',
'Starts with high-level actions and derives the sets or distributions needed to evaluate their compositions. Initiation conditions and effects ground an abstract planning model.',
'Planning sufficiency is relative to the supplied action repertoire and model assumptions. It is not full identification of every physical parameter.',
'Use this to specify what an agent must learn about its existing skills before predicting which compositions can succeed.',False,2)
add('dads','Dynamics-Aware Unsupervised Discovery of Skills','Archit Sharma; Shixiang Gu; Sergey Levine; Vikash Kumar; Karol Hausman',2020,'ICLR 2020','https://arxiv.org/abs/1907.01657',['skills','dynamics'],'Method + continuous-control experiments',
'Learns diverse, predictable skills together with a skill-conditioned dynamics model, then plans in skill space for downstream goals.',
'Predictability concerns transitions induced by the learned skills. Accurate predictions on this distribution do not identify all primitive-action dynamics or guarantee novel-task success.',
'Use as the bridge between a skill library and a predictive model. Ask whether an added skill opens outcomes that existing skill compositions cannot reliably produce.',False,3)
add('plan2explore','Planning to Explore via Self-Supervised World Models','Ramanan Sekar; Oleh Rybkin; Kostas Daniilidis; Pieter Abbeel; Danijar Hafner; Deepak Pathak',2020,'ICML 2020','https://proceedings.mlr.press/v119/sekar20a.html',['information','dynamics'],'Method + visual-control experiments',
'Learns a world model and plans exploratory behavior using ensemble disagreement about future predictions; later adapts to downstream rewards.',
'Disagreement is a practical uncertainty proxy. It can be miscalibrated and depends on model class, training data, and whether useful experiments are reachable.',
'Use for deciding where to collect informative dynamics data, including multi-step preparation before an informative interaction.',False,4)
add('tople','Task-Optimal Exploration in Linear Dynamical Systems','Andrew J. Wagenmaker; Max Simchowitz; Kevin Jamieson',2021,'ICML 2021','https://proceedings.mlr.press/v139/wagenmaker21a.html',['dynamics','information'],'Finite-time theory + experiments',
'Characterizes task-dependent exploration difficulty and designs experiments that collect the information required for the target decision problem.',
'The guarantees concern a specified class of linear dynamical systems and decision problems. They do not transfer unchanged to arbitrary nonlinear, partially observed robots.',
'The strongest conceptual starting point for asking how much dynamics accuracy is enough for a particular skill, rather than trying to reconstruct the whole world.',False,5)
add('alpgmm','Teacher algorithms for curriculum learning of Deep RL in continuously parameterized environments','Rémy Portelas; Cédric Colas; Katja Hofmann; Pierre-Yves Oudeyer',2020,'CoRL 2019 · proceedings 2020','https://proceedings.mlr.press/v100/portelas20a.html',['curriculum'],'Method + curriculum experiments',
'ALP-GMM samples parameterized environments according to absolute learning progress, adapting practice to the current learner and revisiting regressions.',
'Requires a task/environment parameterization and measurable competence. Progress can be noisy; a learning-progress signal alone does not certify transfer to the final task.',
'Use for choosing which skill variants to practice next when easy, useful, and unlearnable regions are initially unknown.',False,6)
add('activeid','Active Learning for Identification of Linear Dynamical Systems','Andrew Wagenmaker; Kevin Jamieson',2020,'COLT 2020','https://proceedings.mlr.press/v125/wagenmaker20a.html',['dynamics','information'],'Identification rates + lower bounds',
'Adaptively chooses control inputs for parameter estimation and establishes finite-time estimation bounds with asymptotically matching rates up to constants.',
'Assumes a linear-system setting and control of the excitation inputs. A frozen skill library restricts this experiment set, so the paper’s input-design guarantee is not automatic.',
'Use to formalize persistent excitation, estimation error, and the difference between purposeful experiments and merely injecting random action noise.')
add('rewardfree','Reward-Free Exploration for Reinforcement Learning','Chi Jin; Akshay Krishnamurthy; Max Simchowitz; Tiancheng Yu',2020,'ICML 2020','https://proceedings.mlr.press/v119/jin20d.html',['dynamics','transfer'],'Sample-complexity theory',
'Explores a finite-horizon tabular MDP before rewards are specified, then supports near-optimal planning for subsequently supplied reward functions.',
'The guarantee depends on state/action/horizon size, accuracy, and the stated access model. Rarely reachable states and unrepresented actions remain important; a fixed skill library changes the action model.',
'Use as a rigorous version of learning dynamics once for many later tasks. Separate this requirement from learning just enough for one chosen task.')
add('vime','VIME: Variational Information Maximizing Exploration','Rein Houthooft; Xi Chen; Yan Duan; John Schulman; Filip De Turck; Pieter Abbeel',2016,'NeurIPS 2016','https://arxiv.org/abs/1605.09674',['information','dynamics'],'Approximate Bayesian method + experiments',
'Rewards information gain about uncertain dynamics parameters, approximating Bayesian posterior updates with a variational neural dynamics model.',
'The usable bonus is approximate and model-dependent. Prediction error by itself is not information gain; irreducible randomness need not teach anything.',
'Use to distinguish curiosity about unknown mechanics from empowerment, which measures how much actions can influence outcomes.')
add('dsg','Skill Discovery for Exploration and Planning using Deep Skill Graphs','Akhil Bagaria; Jason K. Senthil; George Konidaris',2021,'ICML 2021','https://proceedings.mlr.press/v139/bagaria21a.html',['skills','curriculum'],'Method + continuous-control experiments',
'Alternates discovering skills and planning with a graph whose nodes are subgoals and edges are skill policies, expanding the explored state space.',
'An acquired graph covers the discovered region; it does not enumerate all physically possible skills or prove complete exploration in a general continuous environment.',
'Use for the iterative loop: deploy known skills to reach a frontier, learn a connecting skill, add it to the library, and explore farther.')
add('imgep','Intrinsically Motivated Goal Exploration Processes with Automatic Curriculum Learning','Sébastien Forestier; Rémy Portelas; Yoan Mollard; Pierre-Yves Oudeyer',2022,'JMLR 23(152)','https://www.jmlr.org/papers/v23/21-0808.html',['curriculum','skills'],'Framework + robot experiments',
'Formalizes agents that generate and select goals, reuse outcomes across goals, and organize practice through intrinsic signals. Modular goals can create stepping stones toward more complex behavior.',
'Results depend on how goals, policy search, and competence are represented. Self-generated goals do not make every target reachable or learnable.',
'Use for a broader curriculum architecture when the agent must choose both what to practice and how to exploit incidental outcomes.')
add('sgcrl','A Single Goal is All You Need: Skills and Exploration Emerge from Contrastive RL without Rewards, Demonstrations, or Subgoals','Grace Liu; Michael Tang; Benjamin Eysenbach',2025,'ICLR 2025','https://arxiv.org/abs/2408.05804',['curriculum','skills'],'Empirical mechanism discovery',
'Conditions exploration on one target observation while learning contrastive goal-conditioned values. Intermediate behaviors emerge before the final goal is first achieved.',
'The reported emergence is empirical, not a guarantee that arbitrary prerequisite skills or impossible goals will be discovered. The agent still receives a target observation.',
'An especially relevant Eysenbach baseline: test whether explicit subtask curricula outperform the implicit exploration already produced by single-goal contrastive RL.',True)
add('demystifying','Demystifying the Mechanisms Behind Emergent Exploration in Goal-conditioned RL','Mahsa Bastankhah; Grace Liu; Dilip Arumugam; Thomas L. Griffiths; Benjamin Eysenbach',2026,'ICLR 2026','https://arxiv.org/abs/2510.14129',['curriculum','transfer'],'Objective analysis + controlled experiments',
'Analyzes how contrastive representations induce implicit rewards that favor exploration before goal discovery and exploitation afterward; low-rank representation structure is central to the investigated mechanism.',
'The explanation is about this algorithm and its analyzed settings. It is not a universal theorem that every goal-conditioned learner constructs a useful curriculum.',
'Read immediately after SGCRL to ask which representation updates make a new task look learnable, and when an explicit teacher adds value.',True)
add('temporal','Temporal Representations for Exploration: Learning Complex Exploratory Behavior without Extrinsic Rewards','Faisal Mohamed; Catherine Ji; Benjamin Eysenbach; Glen Berseth',2026,'ICLR 2026','https://arxiv.org/abs/2603.02008',['information','skills'],'Method + exploration experiments',
'Uses temporal contrastive representations to guide exploration toward states with unpredictable future outcomes, seeking complex behavior without extrinsic rewards.',
'Temporal unpredictability is an exploration signal, not a calibrated estimate of all unknown physical parameters. Coverage and downstream utility require separate evaluation.',
'A recent Eysenbach connection between learning temporal structure and producing useful exploration, complementing explicit world-model disagreement.',True)
add('identifiable','Skill Learning via Policy Diversity Yields Identifiable Representations for Reinforcement Learning','Patrik Reizinger; Bálint Mucsányi; Siyuan Guo; Benjamin Eysenbach; Bernhard Schölkopf; Wieland Brendel',2026,'ICLR 2026','https://arxiv.org/abs/2507.14748',['dynamics','transfer'],'Conditional identifiability theory + experiments',
'Connects diverse skill-conditioned policies and contrastive successor features to recovery of underlying features up to a linear transformation.',
'The theorem imposes specific data-generating distributions, sufficient skill variability, an injective observation map, critic structure, and ideal optimization. Identifying features is not identifying the entire transition law.',
'Use when asking whether the existing skill set is varied enough to reveal latent factors. Read the assumptions before treating representation recovery as a general world-model guarantee.',True)
add('controlmax','Unifying Goal-Conditioned RL and Unsupervised Skill Learning via Control-Maximization','Alireza Modirshanechi; Benjamin Eysenbach; Peter Dayan; Eric Schulz',2026,'May 2026 preprint','https://arxiv.org/abs/2605.06145',['transfer','skills'],'Theoretical correspondence · preprint',
'Separates three goal-reaching formulations and relates matching mutual-information skill objectives to formulation-specific downstream goal sensitivity.',
'The formulations can prefer different policies. A correspondence or bound for one goal criterion is not a universal success guarantee for every downstream task.',
'Use to choose a skill-learning objective after deciding whether the desired task means reaching, occupying, or otherwise controlling a goal-related outcome.',True)
add('sorb','Search on the Replay Buffer: Bridging Planning and Reinforcement Learning','Benjamin Eysenbach; Ruslan Salakhutdinov; Sergey Levine',2019,'NeurIPS 2019','https://arxiv.org/abs/1906.05253',['skills','transfer'],'Planning method + experiments',
'Uses a learned goal-conditioned value function to connect states in a replay-buffer graph and plan through intermediate waypoints.',
'Stitching depends on reliable local reachability estimates and useful replay coverage. Planning alone does not create a physically missing primitive capability.',
'Use to test whether a supposedly new task is already solvable by composing available local behaviors, before spending trials on new skill learning.',True)
add('contrastive','Contrastive Learning as Goal-Conditioned Reinforcement Learning','Benjamin Eysenbach; Tianjun Zhang; Ruslan Salakhutdinov; Sergey Levine',2022,'NeurIPS 2022','https://arxiv.org/abs/2206.07568',['skills','transfer'],'Value/representation connection + experiments',
'Applies contrastive learning to action-labeled trajectories to obtain representations related to goal-conditioned values, then uses the critic to improve goal-reaching behavior.',
'A critic’s probabilistic interpretation depends on its sampling distribution and ideal fitting assumptions. It does not by itself certify exploration coverage or uncertainty.',
'The technical foundation for the SGCRL line. Useful when a goal-reaching model can replace a more expensive full observation-prediction model.',True)
add('successor','Successor Features for Transfer in Reinforcement Learning','André Barreto; Will Dabney; Rémi Munos; Jonathan J. Hunt; Tom Schaul; Hado van Hasselt; David Silver',2017,'NeurIPS 2017','https://arxiv.org/abs/1606.05312',['transfer','skills'],'Transfer bounds + experiments',
'Decouples expected future features from reward weights and uses generalized policy improvement to reuse a set of policies across tasks.',
'The principal transfer setting keeps dynamics fixed and assumes an appropriate reward-feature representation. It is not a theorem for arbitrary changing mechanics or an unlimited task family.',
'Use to distinguish reusing existing skills under a new objective from acquiring new dynamics knowledge or a new motor ability.')

if __name__=='__main__':
    (ROOT/'literature/papers.json').write_text(json.dumps(PAPERS,ensure_ascii=False,indent=2)+'\n')
    bib=''
    for p in PAPERS:
        bib+=('@misc{'+p['id']+',\n  title = {'+p['title']+'},\n  author = {'+' and '.join(p['authors'].split('; '))+'},\n  year = {'+str(p['year'])+'},\n  note = {'+p['venue']+'},\n  url = {'+p['url']+'}\n}\n\n')
    (ROOT/'literature/references.bib').write_text(bib.rstrip()+'\n')
    template=(ROOT/'src/literature.template.html').read_text()
    cards=''
    labels={'dynamics':'Learnable dynamics','information':'Information-seeking','skills':'Build and compose skills','curriculum':'Choose practice','transfer':'Transfer and limits'}
    for p in PAPERS:
        tags=' '.join(p['topics'])+(' eysenbach' if p['eysenbach'] else '')
        cards+=f'<article id="{p["id"]}" class="paper" data-tags="{tags}"><p class="eyebrow">{html.escape(p["venue"])}'+(' · EYSENBACH COAUTHOR' if p['eysenbach'] else '')+f'</p><h3><a href="{p["url"]}" target="_blank" rel="noopener">{html.escape(p["title"])} ↗</a></h3><p class="authors">{html.escape(p["authors"])}</p><p class="evidence">{html.escape(p["evidence"])}</p><p>{html.escape(p["mechanism"])}</p><p><strong>Why read it:</strong> {html.escape(p["use"])}</p><p class="limit"><strong>Scope:</strong> {html.escape(p["limit"])}</p></article>\n'
    template=template.replace('<!-- CARDS -->',cards).replace('/* INLINE_CSS */',(ROOT/'src/style.css').read_text())
    (ROOT/'literature.html').write_text(template)
    print('Built literature map with',len(PAPERS),'primary papers;',sum(p['eysenbach'] for p in PAPERS),'Eysenbach coauthored.')
