"""Original six-lesson scripts. Paper claims are distinguished from worked examples."""
from schema import ROOT, chapter, episode

LINKS = {
 'diayn':('Diversity Is All You Need: Learning Skills without a Reward Function','https://arxiv.org/abs/1802.06070'),
 'geometry':('The Geometry of Empowerment','https://arxiv.org/abs/2610.07796'),
 'scaling':('Scaling Empowered Agents','https://arxiv.org/abs/2610.13002'),
 'representation':('Learning to Perceive the World Through Control: Empowerment-Based Representation Learning','https://arxiv.org/abs/2605.30656'),
 'assistance':('Learning to Assist Humans without Inferring Rewards','https://arxiv.org/abs/2411.02623'),
 'language':('Training LLM Agents to Empower Humans','https://arxiv.org/abs/2510.13709'),
}
def C(title, visual, steps, narration, source):
    return chapter(title,visual,steps,narration,source)
def E(id,n,short,title,authors,year,color,summary,chapters):
    paper,url=LINKS[id]
    return episode(id,n,short,title,paper,authors,year,url,color,summary,
                   [dict(title=LINKS[k][0],url=LINKS[k][1]) for k in dict.fromkeys([id,'diayn','geometry'])],chapters)

EPISODES = [E('diayn',1,'DIAYN','Learning skills before choosing a task',
 'Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, Sergey Levine','ICLR 2019 · preprint 2018','#67d9ef',
 'Start with information, derive the discriminator reward, and separate diverse skills from empowered states.',[
 C('Control is a communication channel','channel',[
 ('Choose an input',r'Z\sim p(z),\quad S^+\sim p(s^+\mid z,s_0)','A skill is the message; its outcome is the received signal.'),
 ('Subtract uncontrollable randomness',r'I(Z;S^+\mid s_0)=H(S^+\mid s_0)-H(S^+\mid Z,s_0)','Unpredictable outcomes are not necessarily controllable outcomes.'),
 ('Optimize the channel input',r'\mathcal{E}(s_0)=\max_{p(z)}I(Z;S^+\mid s_0)','This capacity is for the specified skill channel and horizon.')],
 """Imagine a robot with two buttons. One reliably moves a puck left, and the other reliably moves it right. After seeing the puck, an observer can infer which button was pressed. The robot has transmitted one bit through the physical world. That is the basic intuition behind empowerment.

Now disconnect the buttons and let a fan randomly blow the puck left or right. The outcome still has one bit of entropy. Yet it tells us nothing about the chosen button. Subtracting the uncertainty that remains after the input is known removes this uncontrollable randomness. What remains is mutual information.

A learned skill can replace a single button: choose a latent variable, run a policy, and observe a future state. Maximizing information over the input distribution gives the capacity of that particular channel. The available skills, the observation, and the time horizon all matter. We will use this communication picture to understand DIAYN.""",
 'Original two-button channel example; empowerment definitions in Geometry §3. DIAYN is a related state-marginal skill objective, not this exact fixed-horizon channel.'),
 C('Make a skill recognizable from its states','skills',[
 ('Sample a persistent identity',r'z\sim p(z),\qquad a_t\sim\pi_\theta(a_t\mid s_t,z)','Keep the chosen skill fixed during its rollout.'),
 ('Separate state distributions',r'I(Z;S)=H(Z)-H(Z\mid S)','The discriminator sees states, not the action sequence.'),
 ('Keep behavior flexible',r'\mathcal{J}=I(Z;S)+\alpha H(A\mid S,Z)','Distinct state occupancies plus conditional action entropy.')],
 """In DIAYN, we first draw a skill label from a fixed prior. The same policy network receives both the current state and this label. Hold the label fixed while collecting a trajectory. Different labels should produce state distributions that an observer can distinguish, without being told a downstream task reward.

Our diagram has three colored skills exploring different parts of a room. If every color visits exactly the same distribution, the state reveals no information about the label. If the distributions become distinct, the label becomes easier to decode. This is a statement about distributions, not just three hand-picked trajectory endpoints.

DIAYN also rewards entropy in the action distribution conditioned on the state and skill. That encourages flexible behavior within each distinguishable skill. The canonical information objective combines state-skill mutual information with this action entropy term. High action entropy alone would just produce randomness; the state discriminator supplies the pressure toward identifiable effects.""",
 'DIAYN §§3–4: skill-conditioned policy, state discriminator, and conditional action entropy. The room is an original schematic.'),
 C('Turn mutual information into a reward','bound',[
 ('Start from the posterior',r'I(Z;S)=\mathbb{E}[\log p(z\mid s)-\log p(z)]','The true posterior is generally unavailable.'),
 ('Insert a learned decoder',r'I(Z;S)=\mathbb{E}\log\frac{q_\phi(z\mid s)}{p(z)}+\mathbb{E}_s D_{KL}(p\Vert q)','The omitted KL term is nonnegative.'),
 ('Use a variational lower bound',r'r_z(s)=\log q_\phi(z\mid s)-\log p(z)','Reward states that provide evidence for the sampled skill.')],
 """Here is the mathematical bridge from information theory to reinforcement learning. Write mutual information as the expected log posterior probability of the skill, minus its log prior probability. The prior is chosen by us. The posterior would require knowing the complete distributions generated by the policies.

Replace that posterior with a trainable classifier. Add and subtract its log probability inside the expectation. The leftover term is an expected Kullback Leibler divergence from the true posterior to the classifier. Because this divergence cannot be negative, the classifier expression is a lower bound on the information we wanted.

This gives a concrete intrinsic reward: log classifier probability minus log prior. A state earns reward when it is stronger evidence for the sampled skill than the prior alone. The bound becomes tight with a correct classifier. Otherwise, improving the classifier and improving the policy address different sources of error in the same objective.""",
 'DIAYN variational discriminator reward; the KL decomposition is a standard information-theory identity, derived here with original notation.'),
 C('A numerical reward you can check','reward',[
 ('Four equally likely skills',r'p(z)=1/4,\qquad H(Z)=\log 4','All logarithms in these lessons use natural units: nats.'),
 ('A confident correct prediction',r'q(z\mid s)=0.8\;\Rightarrow\;r=\log(3.2)\approx1.163','The state provides positive evidence for its skill.'),
 ('Compare against chance',r'q(z\mid s)=0.25\;\Rightarrow\;r=0','A wrong confident prediction can produce negative reward.')],
 """Let us compute the reward instead of treating the formula as decoration. Suppose there are four equally probable skills. Before observing a state, the probability of the chosen skill is one quarter. If the discriminator assigns probability point eight to the correct label afterward, the reward is log three point two, about one point one six nats.

If the classifier stays at chance, the ratio is one and the reward is zero. If it gives the true skill probability point zero five, the ratio becomes point two and the reward is negative. The policy is rewarded for evidence about its actual label, not simply for producing any confident classifier prediction.

The lab generalizes this example into a noisy categorical channel. Change how much the skill distributions overlap and compare actual mutual information with the variational bound. A miscalibrated decoder can lower the bound even when the underlying skills remain distinct. This is a controlled calculation, not a replication of a locomotion benchmark.""",
 'Original four-skill arithmetic and exact finite-channel teaching model; reward form from DIAYN.'),
 C('Two optimizers, one feedback loop','training',[
 ('Collect labeled experience',r'\mathcal{D}\leftarrow\mathcal{D}\cup\{(s,a,s^\prime,z)\}','The skill label is self-generated supervision.'),
 ('Train the discriminator',r'\max_\phi\;\mathbb{E}_{\mathcal{D}}\log q_\phi(z\mid s)','Classification changes the intrinsic reward landscape.'),
 ('Improve the skill policy',r'\max_\theta\;\mathbb{E}\sum_t\gamma^t[r_z(s_t)+\alpha H(\pi_\theta)]','An entropy-regularized RL optimizer improves behavior.')],
 """The learning loop now has two coupled parts. Sample a label, execute the label-conditioned policy, and store states with their labels. Those labels are free supervision: they came from the experimenter, rather than an external reward function. A discriminator learns to predict them from the observed states.

Next, use the discriminator reward inside an entropy-regularized reinforcement learning update. Better policies can produce more separable states, which give the discriminator a clearer classification problem. A more accurate discriminator gives the policy a more faithful signal. Neither update makes the other automatically correct, especially with limited data or function approximation.

A practical implementation must keep the skill identity attached to each replay transition. It must also separate the task reward used for later evaluation from the intrinsic reward used during pretraining. Otherwise an apparently unsupervised result can quietly depend on downstream supervision. Our included code computes the information objective exactly, rather than pretending to reproduce the entire training system.""",
 'DIAYN training structure and entropy-regularized learning; replay explanation and finite-channel code are educational illustrations.'),
 C('Diverse skills are only the beginning','options',[
 ('State what was learned',r'\pi(a\mid s,z)\quad\mathrm{and}\quad q(z\mid s)','A behavioral repertoire and a decoder.'),
 ('Separate skill use from preparation',r'I_\pi(Z;S^+\mid s_0)\leq\mathcal{E}(s_0)','A particular skill set supplies evidence about capacity.'),
 ('Ask where skills remain available',r'\max_\mu\;\mathbb{E}_\mu\sum_t\gamma^t\mathcal{E}(S_t)','The next lessons add an outer state-seeking objective.')],
 """The useful product is a repertoire: a skill-conditioned policy together with a decoder. A later task can select skills, compose them, or fine-tune their parameters. But distinguishable behavior is not a promise that every useful task is covered. The features supplied to the discriminator influence which differences are worth learning.

There is another subtle distinction. Executing a skill may consume an opportunity. A robot can demonstrate that it knows several ways to leave a platform, while ending up somewhere with few remaining choices. Measuring information transmitted by a chosen skill set and seeking states with many available skills are different optimization problems.

Keep three questions separate as the series continues. What behaviors are distinguishable? From which starting states can they actually be executed? And who benefits from those choices? DIAYN provides our starting language for the first question. The geometry and scaling papers address the second; the assistance papers change the agent whose control we care about.""",
 'DIAYN transfer motivation; effective-versus-potential distinction from Geometry §3. The platform example is original.')]),

E('geometry',2,'Geometry','Where are the states with the most options?',
 'Catherine Ji, Vivek Myers, Sergey Levine, Benjamin Eysenbach','October 2026 preprint','#bea8ff',
 'See occupancy distributions as points, mutual information as a KL radius, and why empowerment does not guarantee every reward.',[
 C('Spend a choice or preserve choices','options',[
 ('Actualized control',r'\mathcal{E}_{\mathrm{eff}}(\pi,s)=I_\pi(Z;S^+\mid s)','A fixed skill family realizes a particular amount of information.'),
 ('Available control',r'\mathcal{E}_{\mathrm{pot}}(s)=\sup_{\pi,p(z)}I_\pi(Z;S^+\mid s)','Capacity optimizes the available skill channel.'),
 ('Navigate toward capacity',r'\mu^*=\arg\max_\mu\mathbb{E}_\mu\sum_t\gamma^t\mathcal{E}_{\mathrm{pot}}(S_t)','The outer policy seeks states from which choices are possible.')],
 """Consider a junction with three one-way exits. Choosing different skills can reliably take you down different exits, so the junction supports several distinguishable futures. But after taking an exit, you may lose access to the others. Exercising a choice and preserving the opportunity to choose are different behaviors.

Effective empowerment describes the information realized by a specified set of skills and its sampling distribution. Potential empowerment optimizes that information over the available behaviors. A further policy can seek states with high potential empowerment. Notice the two levels: one optimization measures a state's options, while another moves through the world to obtain them.

The Geometry of Empowerment studies this distinction through reachable future-state distributions. The paper's policies are closed-loop skills and its future state is sampled at a discounted random time. Our junction example initially uses a finite endpoint channel to make the information calculation transparent. We will state when we switch between these two settings.""",
 'Geometry §3 definitions. The one-way junction is an original finite-channel illustration.'),
 C('Replace trajectories with distributions','simplex',[
 ('A normalized discounted future',r'd_z(s^+\mid s_0)=(1-\gamma)\sum_{t=0}^{\infty}\gamma^t p(s_{t+1}=s^+\mid s_0,z)','Sample a future time geometrically, beginning at the next step.'),
 ('Every distribution is a point',r'd_z\in\Delta^{n-1},\qquad\sum_{i=1}^n d_z(i)=1','Three outcomes form a triangle, not ordinary physical space.'),
 ('Mix the skills',r'\bar d=\sum_z p(z)d_z','A random skill selection produces a mixture occupancy.')],
 """A trajectory is long and detailed. For this analysis, compress it into a probability distribution over future states. Discounted occupancy assigns weight one minus gamma to the next state, then multiplies subsequent weights by gamma. The weights sum to one, so the result is a genuine distribution rather than an unnormalized visit count.

With three possible outcomes, draw each distribution as a point inside a triangle. A corner means certainty about one outcome. An interior point means a mixture. This triangle is a probability simplex. Distances inside it will describe differences in outcome probabilities, not the physical distances that a robot travels.

Each skill gives one point. Randomly choose among the skills and their distributions average into another point. Varying the mixture weights traces their convex hull. This is why geometric language becomes useful: an apparently complicated policy problem can sometimes be examined through a set of reachable distributions and the center induced by a skill mixture.""",
 'Geometry §3 discounted occupancy and §4 information geometry. Triangle construction is an original three-outcome example.'),
 C('Mutual information is an average KL radius','radius',[
 ('Measure a skill against the mixture',r'D_{KL}(d_z\Vert\bar d)=\sum_i d_z(i)\log\frac{d_z(i)}{\bar d(i)}','KL compares probabilities; it is asymmetric and not Euclidean distance.'),
 ('Average over skill choices',r'I(Z;S^+)=\sum_z p(z)D_{KL}(d_z\Vert\bar d)','For a fixed prior, this is an average—not the maximum radius.'),
 ('Optimize a finite channel',r'C=\min_q\max_z D_{KL}(d_z\Vert q)','The information-radius dual holds for a finite fixed channel.')],
 """Why does this picture involve information rather than an arbitrary geometric distance? For each skill, compare its outcome distribution with the mixture over skills. The Kullback Leibler divergence measures how much that skill-specific distribution differs from the mixture. Average these divergences using the skill prior, and the expression is exactly mutual information.

That average is important. For an arbitrary prior, mutual information is not equal to the largest divergence. If we optimize the prior for a fixed finite channel, a dual description becomes available: find a reference distribution that minimizes the largest divergence from the channel's rows. This is an information radius.

At a capacity-achieving solution, active input symbols touch the relevant outer boundary; unused symbols cannot improve the optimum. Our lab solves the finite-channel optimization numerically and checks its upper and lower bounds. The picture supplies intuition for the paper's broader occupancy geometry, while avoiding the mistaken claim that every triangle's Euclidean area equals empowerment.""",
 'Geometry §4.1; standard finite-channel information-radius dual, derived with original probability-simplex diagrams.'),
 C('Count distinguishable outcomes, not labels','capacity',[
 ('Perfectly distinguishable futures',r'C=\log m\quad\text{for }m\text{ distinct deterministic outputs}','Duplicate inputs do not add new channel outputs.'),
 ('Noisy binary control',r'C=\log 2-h(\epsilon)','For a binary symmetric channel; h is binary entropy in nats.'),
 ('Independent outcomes erase control',r'p(s^+\mid z)=p(s^+)\;\Rightarrow\;I=0','A broad random future may carry no information about the input.')],
 """Here are three sanity checks. First, if every input deterministically selects one of three distinct outputs, capacity is log three. Add ten new input labels that duplicate existing outputs and capacity does not increase. Labels are cheap; distinguishable consequences are what carry information.

Second, suppose two buttons are confused with probability epsilon. The binary symmetric channel has capacity log two minus binary entropy. At zero noise, control is reliable. At one-half noise, the output is independent of the input and capacity vanishes. A perfectly predictable inversion would still transmit information, so randomness and inversion must not be confused.

Third, imagine a machine that samples uniformly from a thousand outcomes regardless of the chosen button. Its future-state entropy is large, yet its empowerment through those buttons is zero. These examples explain why counting visited states or measuring visual diversity alone is insufficient. The causal dependence on the selected behavior is essential to this channel calculation.""",
 'Original exact categorical examples. The deterministic reachability interpretation is discussed in Geometry appendix B.1.'),
 C('Information geometry is not reward geometry','geometry_limit',[
 ('A task introduces another geometry',r'V_r(d)=\langle d,r\rangle','A reward weights state occupancies in a task-specific direction.'),
 ('Tiny distinguishable changes can matter little',r'I(Z;S^+)\gg0\;\not\Rightarrow\;V_r\gg0','Many reliable distinctions can lie in an irrelevant coordinate.'),
 ('Keep the theorem assumptions',r'\text{tabular, specified reward prior}\neq\text{all tasks}','Continuous states and anisotropic rewards require care.')],
 """Now give each state a reward. The value of an occupancy is its dot product with the reward vector. That introduces a task-specific direction in the simplex. Information geometry asks whether outcomes are distinguishable; reward geometry asks whether those distinctions improve the particular quantity we care about.

In our toy example, a control can reliably set many tiny values of an indicator light, while another control opens a useful door. The light may offer many distinguishable outcomes and little task value. Increasing measurement precision can amplify this mismatch. Information is sensitive to distinguishability, even when every change is irrelevant to the selected task.

The paper proves a positive adaptation connection under a specified tabular reward distribution, and also gives limitations for continuous states and uneven reward priors. Treat these as conditional mathematical statements. They do not imply that any high-empowerment policy will solve any future task, or that all controllable variables are equally useful to represent.""",
 'Geometry §4.3 and appendices F–H: adaptation result and limitations. Indicator-light counterexample is an original teaching illustration.'),
 C('From a geometric object to an algorithm','two_policy',[
 ('Specify the channel',r'(s_0,\;Z,\;S^+,\;\gamma)','State, skills, measured outcomes, and horizon define the quantity.'),
 ('Estimate rather than assume capacity',r'\widehat I\leq I_\pi\leq\mathcal{E}_{\mathrm{pot}}','The first inequality requires a valid population lower bound.'),
 ('Use the estimate as a reward',r'r_{\mathrm{outer}}(s)=\widehat{\mathcal{E}}(s)','A second learner seeks states with many executable skills.')],
 """To turn this theory into an experiment, write down the channel first. Specify the starting state, the skill family, the future-state observation, and the horizon. Changing any one of these changes what counts as control. Two empowerment curves are not directly comparable if they measure different channels.

Next, separate an estimator from the ideal capacity. A learned decoder may provide a lower bound on the information realized by a limited skill set. That information is itself no larger than the best capacity available in the full policy class. Approximation error, incomplete skills, and optimization error create distinct gaps.

Finally, imagine rewarding another policy for reaching states where this estimate is high. We have arrived at the outer optimization promised at the beginning. The geometry identifies what to measure and warns about reward mismatch. The next paper develops a practical two-policy recipe that uses skill learning to estimate empowerment while learning where to go.""",
 'Synthesis of Geometry §3–4 and Scaling §4. Bounds refer to exact population objectives, not arbitrary fitted neural estimates.')]),
E('scaling',3,'Scaling','Skills estimate empowerment; another policy seeks it',
 'Catherine Ji, Vivek Myers, Joshua Lin, Alexandra Wingate, Sergey Levine, Benjamin Eysenbach','October 2026 preprint','#83e0b2',
 'Derive the two-policy SEE recipe, understand its estimator gaps, and see why useful control depends on what is measured.',[
 C('A workshop and a box of skills','two_policy',[
 ('Probe the current state',r'z\sim p(z),\quad a\sim\pi_{\mathrm{eff}}(a\mid s,z;s_0)','Skills test which controllable futures are available here.'),
 ('Estimate available control',r'\widehat{\mathcal{E}}(s_0)\approx\mathbb{E}_z V_{\mathrm{eff}}(s_0;s_0,z)','Average the skill values from this same starting context.'),
 ('Seek better starting states',r'a\sim\pi_{\mathrm{pot}}(a\mid s)','The outer policy makes future skills easier to execute.')],
 """Imagine arriving at an empty workshop. You know how to cut, assemble, and repair things, but none of those skills works well without tools and materials. One behavior gathers resources and prepares the workspace. Other behaviors use those resources to produce different outcomes. Both are useful, but they optimize different immediate objectives.

Skills Estimate Empowerment, abbreviated SEE, turns this distinction into a two-policy recipe. A skill policy probes the distinguishable futures available from a starting context. A separate potential-empowerment policy learns to visit states where the skill-based estimate is high. The same state may therefore be an endpoint for preparation and a starting point for skill execution.

Our workshop is a teaching example, not a reported environment. It highlights the key architectural separation: the skill latent describes what to do, while the outer policy improves where skills can begin. Simply switching among diverse skills does not automatically implement that outer preparation objective.""",
 'Scaling §4 two-policy SEE recipe. Workshop illustration is original; no benchmark reproduction is claimed.'),
 C('Decode the skill from a future outcome','decoder',[
 ('Choose the context explicitly',r'q_\phi(z\mid s_0,s^+)','Do not confuse the fixed skill start with the current state.'),
 ('Compare posterior with prior',r'r_z(s^+;s_0)=\log\frac{q_\phi(z\mid s_0,s^+)}{p(z)}','A normalized decoder gives the variational reward.'),
 ('Normalize a contrastive score',r'\log\frac{q_\phi(z\mid s_0,s^+)}{p(z)}=f_\phi-\log\mathbb{E}_{\tilde z}e^{f_\phi}','A raw logit is not automatically an information estimate.')],
 """The ideal decoder receives both the starting context and a future outcome, then predicts which skill was selected. A far-away outcome can mean different things depending on where the skill began. Conditioning on that starting context is therefore part of the mathematical channel, not an incidental implementation detail.

As before, posterior evidence relative to the prior supplies a variational reward. A contrastive model can represent this evidence using logits. But logits are only defined relative to a normalization term. Subtract the log average exponential score over candidate skills to obtain a normalized density ratio for the chosen skill.

This distinction matters when the estimate becomes another learner's reward. A score can grow through arbitrary offsets without representing additional control. The paper discusses practical classifier variants, including a joint classifier in continuous settings. Our derivation uses the ideal conditional form, and the lab uses exact finite distributions so every normalization can be checked directly.""",
 'Scaling §4.1, practical classifier discussion in §4.2, and appendix A.1. Exact finite decoder is a teaching model.'),
 C('A skill value becomes an empowerment estimate','value',[
 ('Average across discounted future times',r'V_z(s_0)=(1-\gamma)\mathbb{E}\sum_{t\geq0}\gamma^t r_z(S_{t+1};s_0)','The normalization matches a geometric future-state distribution.'),
 ('Keep the two approximation gaps',r'\mathbb{E}_z V_z(s_0)\leq I_\pi(Z;S^+\mid s_0)\leq\mathcal{E}_{\mathrm{pot}}(s_0)','Decoder error and incomplete skills are different gaps.'),
 ('Estimate with sampled skills',r'\widehat{\mathcal{E}}(s_0)=\frac{1}{K}\sum_{k=1}^{K}V_{z_k}(s_0)','Finite samples and learned critics add estimation error.')],
 """The future state in the theory is sampled at a geometric time. Equivalently, average the decoder reward along a rollout with discount weights and multiply by one minus gamma. A value function can estimate that normalized discounted return for each skill and starting context.

Now average the skill values. In the ideal population calculation, this quantity lower-bounds the information realized by the current skill family. That realized information, in turn, cannot exceed the best available capacity. The first gap comes from the decoder; the second comes from skills that may not exploit every controllable outcome.

In code, we also approximate the skill average with a finite sample and fit the value function from data. Those approximations are not guaranteed lower bounds on each individual estimate. Increasing the sample count reduces ordinary sampling variance under independence, but cannot fix a biased critic. The lab separates true capacity, realized information, and the estimated score.""",
 'Scaling Eqs. 6–9; finite-sample and critic caveats follow from the distinction between population objectives and fitted estimates.'),
 C('Collect data for both levels','rollout',[
 ('Prepare the starting context',r's_0\sim\mathrm{rollout}(\pi_{\mathrm{pot}})','The outer policy visits candidate empowered states.'),
 ('Branch into a sampled skill',r'z\sim p(z),\qquad\tau\sim\pi_{\mathrm{eff}}(\cdot\mid\cdot,z;s_0)','The skill measures what can be done from that context.'),
 ('Train the coupled system',r'\mathrm{data}\to\text{decoder and values}\to\mathrm{policies}','Data coverage and reward estimation evolve together.')],
 """There is a data-collection problem hidden inside the equations. We cannot first solve every possible skill from every possible state in a large environment. We need a way to sample the contexts that matter while learning the skills that measure those contexts.

SEE collects two-stage rollouts: run the potential policy, then sample a skill and execute it from the reached state. The outer trajectory proposes a promising starting context. The skill continuation probes its available control. Data from these interactions updates the representations, value estimates, and policies, producing a moving feedback loop.

A useful debugging plot would show both phases separately. If preparation reaches the same state every time, ask whether its estimated advantage is real. If skills collapse to identical outcomes, a low empowerment estimate might reflect weak skills rather than a fundamentally powerless state. This is why recording only the outer reward curve can hide which component failed.""",
 'Scaling §4.2 and algorithm appendix: two-stage data collection. Debugging plots and failure interpretation are original implementation guidance.'),
 C('Choose the variables that count as control','bottleneck',[
 ('Specify measured outcomes',r'Y=g(S^+)','The policy may observe more than the empowerment decoder.'),
 ('Define a resolution',r'\widetilde Y=Y+\epsilon,\quad\epsilon\sim\mathcal{N}(0,\sigma^2I)','Measurement noise can prevent microscopic distinctions from dominating.'),
 ('State the inductive bias',r'I(Z;\widetilde Y)\leq I(Z;Y)','Discarding information can favor robust, meaningful differences.')],
 """Suppose an agent can wiggle an irrelevant display with extremely fine precision. A sufficiently expressive decoder might distinguish many skill labels from tiny display changes. That could create a large information score without producing the resource gathering or object manipulation that motivated the experiment.

The paper therefore treats the measurement channel as a design choice. Its practical implementation restricts which state variables enter empowerment estimation and adds a noise-based bottleneck in continuous settings. The policy can still receive the full observation needed for control. What the agent can see and what counts toward the empowerment objective need not be identical.

The data-processing inequality gives a useful intuition: adding independent measurement noise cannot increase true mutual information. It can suppress fragile distinctions below a chosen resolution. That is an inductive bias, not a proof that all remaining behavior is useful. In the lab, compare meaningful outcome noise with a deliberately biased empowerment estimate and observe their different effects.""",
 'Scaling §4.2 and appendix A.1: restricted outcome variables and Gaussian noising. Display example and lab are original.'),
 C('What scaling does—and does not—establish','evaluation',[
 ('Separate the two policies in evaluation',r'\pi_{\mathrm{pot}}\;\mathrm{prepares},\qquad\pi_{\mathrm{eff}}\;\mathrm{acts}','Show contexts reached and skill outcomes from those contexts.'),
 ('Audit the estimator',r'\widehat{\mathcal{E}}\neq\mathcal{E}\quad\text{in general}','An improved neural score is not by itself verified capacity.'),
 ('Measure the downstream claim separately',r'\mathrm{control}\neq\text{universal task success}','Empowerment can support exploration without replacing evaluation.')],
 """The authors report emergent behaviors in their tested environments, including resource gathering and environment modification. These are empirical observations about a particular method, measurement channel, and training setup. They are not evidence that arbitrary agents will discover every useful behavior from an unrestricted information objective.

For your own experiment, evaluate three things independently. First, inspect the states reached by the preparation policy. Second, execute different skills from those states and measure whether their effects remain distinguishable. Third, evaluate any downstream task you actually care about. A score produced by the same learned estimator used for training is not an independent validation.

The central algorithmic idea is reusable: let skills estimate controllable futures, then learn to seek states where that estimate is large. Its reliability depends on representation choices, data coverage, and the quality of the estimator. The next lesson asks what the empowerment objective itself can tell us about which state features a representation should keep.""",
 'Scaling experiments and discussion; audit checklist is original. This October 2026 work is presented as a preprint, not an established universal result.')]),

E('representation',4,'Representations','Learn what matters for control',
 'Mahsa Bastankhah, Sophie Broderick, Benjamin Eysenbach','ICML 2026','#f4cc78',
 'Derive posterior-based representations, distinguish forward from backward information, and keep the invariance assumptions visible.',[
 C('More pixels do not mean more control','features',[
 ('Separate three kinds of state',r'S=(Y,W,E)','Y is controllable; W affects control; E is irrelevant to control.'),
 ('An uncontrollable variable may matter',r'p(Y^+\mid Y,W,A)','Wind can change motion even when the agent cannot change the wind.'),
 ('An irrelevant process evolves separately',r'p(S^+\mid S,A)=p(Y^+\mid Y,W,A)p(W^+\mid W)p(E^+\mid E)','This factorization is an assumption, not a property of every dataset.')],
 """A camera sees a robot, moving shadows, a door, and a changing display. Which features should a control representation retain? Keeping every pixel is expensive. Discarding every uncontrollable variable is also wrong: the robot may not control the wind, but wind can determine which actions move it toward a target.

Use three conceptual components. One changes in response to the agent's actions. A second evolves on its own but influences the first component's dynamics. A third evolves independently and has no effect on control. The displayed factorization makes those distinctions precise. It is a model assumption about dynamics, not a label we can assign from visual appearance alone.

Learning to Perceive the World Through Control studies representations induced by empowerment-based skill learning. Its key question is whether those representations can ignore control-irrelevant variation while retaining the features needed to distinguish what the agent can do. Our wind-and-display example makes the relevant distinction before we examine the mathematical assumptions.""",
 'Representation paper §5.2, Definition 5.3. Robot, wind, and display illustration is original.'),
 C('The decoder is also a representation model','factorization',[
 ('Represent the start and the outcome',r'q(z\mid s_0,s^+)=q(z\mid\phi(s_0),\psi(s^+))','Forward and backward encoders play different roles.'),
 ('Recover the optimal posterior',r'p(z\mid s_0,s^+)=\frac{p(z\mid s_0)d_z(s^+\mid s_0)}{\sum_{z^\prime}p(z^\prime\mid s_0)d_{z^\prime}(s^+\mid s_0)}','Bayes rule links the representation to skill-conditioned occupancy.'),
 ('Ask what changes the posterior',r'\text{same posterior}\Rightarrow\text{same minimal representation}','Minimality rules out retaining irrelevant extra coordinates.')],
 """Start with the skill decoder from earlier lessons, but factor it through two encoders. One represents the initial state and the other represents the future state. Together they retain the information needed to infer which skill produced the outcome. These are called forward and backward representations.

Bayes rule makes their target explicit. Multiply the skill prior by the probability that the skill reaches the observed outcome, then normalize across skills. A feature matters to this posterior only if it changes the relative evidence for skill identities. This creates a representation-learning signal without supplying a downstream task label.

There is a crucial qualification. A sufficiently large network could predict the correct posterior while also storing arbitrary irrelevant details. The theory therefore studies minimal sufficient representations: representations that preserve exactly the distinctions needed by the posterior. Correct prediction alone is not the same as compression, and a practical neural network is not guaranteed to satisfy minimality.""",
 'Representation paper §4 and Definition 4.1: Bayes-optimal decoder, sufficiency, and minimality assumptions.'),
 C('Forward asks: what can happen next?','forward',[
 ('Compare outgoing control possibilities',r'\{p(\cdot\mid s,a):a\in\mathcal{A}(s)\}','The action labels themselves need not have intrinsic meaning.'),
 ('Match actions by their effects',r'p(\cdot\mid s,a)=p(\cdot\mid\hat s,\hat a)','Compare behavior under corresponding controls.'),
 ('Alias under the theorem conditions',r'\phi(s)=\phi(\hat s)','The forward representation can ignore superficial interface changes.')],
 """Think of the forward representation as describing the control possibilities available from a state. Two versions of a machine might use different button names while offering the same effects. If actions can be matched by their transition distributions, the superficial interface labels should not define different underlying capabilities.

In our diagram, one panel maps the upper button to opening a gate, while another swaps the physical labels. The useful comparison pairs actions by their consequences. A controller still needs to issue the correct button in each interface, but a representation of the available control structure can identify the equivalent starting situations.

The paper formalizes such equivalences under its policy and representation assumptions. The point is not that two states with similar pictures must have the same embedding. It is that a specific relation between their available transition distributions can justify aliasing. Changing a real obstacle, an actuator limit, or the effect of an action may break that relation.""",
 'Representation paper Theorem 5.1 under its stated conditions. Gate/button illustration is original and does not claim a universal encoder guarantee.'),
 C('Backward asks: how could I get here?','backward',[
 ('Compare incoming evidence',r'd_z(y\mid s_0)=c(s_0)d_z(\hat y\mid s_0)\quad\forall z','A shared positive proportionality factor cancels in Bayes rule.'),
 ('The skill posterior agrees',r'p(z\mid s_0,y)=p(z\mid s_0,\hat y)','The two outcomes provide the same evidence about the skill.'),
 ('Alias the outcomes, not their futures',r'\psi(y)=\psi(\hat y)\;\not\Rightarrow\;\phi(y)=\phi(\hat y)','Incoming reachability and outgoing controllability differ.')],
 """The backward representation answers a different question: what does observing this outcome tell us about the skill that brought us here? Suppose two outcomes occur in the same proportion under every skill from a given starting state. Their likelihoods differ by a shared factor, so that factor cancels when computing the posterior over skills.

Under the corresponding conditions across starting states, a minimal backward representation can identify these outcomes. Yet their future control possibilities might differ. Arriving at two locations by indistinguishable routes does not imply that the same exits will be available afterward. Incoming evidence and outgoing control are separate structures.

This is why forcing the two encoders to be identical can discard useful distinctions. In the companion, compare small tables of skill-conditioned probabilities and directly compute the posterior for each outcome. You can see when columns carry the same evidence even though we assign the resulting states different future options in the toy model.""",
 'Representation paper Proposition 5.2. Table-based Bayes calculation is an original illustration of backward aliasing.'),
 C('Why independent noise can cancel','invariance',[
 ('Factor a skill-independent nuisance',r'p(x^+,e^+\mid z,s_0)=p(x^+\mid z,s_0)p(e^+\mid s_0)','This simplified teaching factorization makes the cancellation explicit.'),
 ('Cancel it from the posterior',r'p(z\mid x^+,e^+,s_0)=p(z\mid x^+,s_0)','Extra nuisance variation supplies no skill evidence.'),
 ('State the stronger theorem conditions',r'\text{optimal decoder + minimal policies + minimal representations}','Independent dynamics alone do not guarantee every trained network is invariant.')],
 """We can see the core cancellation in a simple probability model. Let the outcome contain a controllable coordinate and an independent nuisance. If the nuisance has the same distribution for every skill, its probability appears in both the numerator and denominator of Bayes rule. It cancels, leaving the same posterior without the nuisance.

That calculation explains why nuisance variation need not help skill classification. It does not prove that any finite-data neural network will ignore it. A network might memorize correlations, a policy might condition unnecessarily on the nuisance, or a restricted skill set might fail to expose important controllable distinctions.

The paper's invariance result adds explicit conditions, including its structured dynamics, optimal-posterior analysis, and minimality assumptions for policies and representations. Those conditions matter. In our lab, independent duplicate observation channels leave information unchanged, while action-dependent changes can alter it. This isolates one algebraic mechanism without presenting the toy calculation as the full theorem.""",
 'Representation paper Theorem 5.6 and associated assumptions. Product-channel cancellation is a simplified original worked example.'),
 C('A useful encoder still needs an audit','representation_audit',[
 ('Check sufficiency',r'q(z\mid\phi(s_0),\psi(s^+))\approx p(z\mid s_0,s^+)','Does the encoding preserve the required skill evidence?'),
 ('Check the intended invariance',r'\phi(x,e)\approx\phi(x,\hat e)','Vary nuisance features while holding the control problem fixed.'),
 ('Check relevant sensitivity',r'\text{changed capabilities}\Rightarrow\text{test for changed encoding}','Invariance is useful only when important distinctions survive.')],
 """A good representation experiment needs both invariance and sensitivity tests. Vary an irrelevant display while holding the control problem fixed: the representation should ideally stay stable. Then change a door's availability or an actuator's effect: the representation should preserve the distinction if it changes the relevant skill posterior.

Also test the policy and decoder together. An encoder that ignores an important variable can still look compact, and a highly accurate classifier can still store irrelevant information. Compression, predictive sufficiency, and downstream control are related but different properties. Treating any one metric as a complete answer hides the assumptions behind the theory.

The lesson is that empowerment-based interaction offers a principled route toward control-centered representations. It does not remove the need to specify what counts as relevant control or to verify the learned model. Next we will change the subject of empowerment: instead of expanding the robot's own choices, we will ask the robot to expand a human's effective control.""",
 'Original evaluation guidance informed by Representation §§5–6. The guarantees remain conditional on the paper assumptions.')]),
E('assistance',5,'Human assistance','Increase the human’s control, without inferring a reward',
 'Vivek Myers, Evan Ellis, Sergey Levine, Benjamin Eysenbach, Anca Dragan','NeurIPS 2024','#86c5ff',
 'Derive effective human empowerment and the contrastive density-ratio reward used by ESR.',[
 C('Whose choices should the robot expand?','human',[
 ('Two agents share a world',r'a^R\sim\pi_R(\cdot\mid s),\qquad a^H\sim\pi_H(\cdot\mid s)','The assistant changes the channel available to the human.'),
 ('Measure the human’s influence',r'I(A^H;S^+\mid s,a^R)','Keep the human action as the information-bearing input.'),
 ('Optimize the assistant',r'\max_{\pi_R}\mathbb{E}\sum_t\gamma^t I(A_t^H;S^+\mid S_t,A_t^R)','The assistant is optimized; the measured subject is the human.')],
 """A robot stands beside a person at a workbench. It could perform the entire task itself, or clear an obstruction so the person can choose what to build. Both might change the environment, but only one necessarily increases the person's control. Before writing an empowerment objective, identify whose action is the input to the channel.

Learning to Assist Humans without Inferring Rewards places the human's current action on that input side. The assistant changes the environment and therefore changes how human actions influence future states. The objective is to learn an assistant that improves this influence over time, rather than explicitly reconstructing a hidden human reward function.

This does not mean the method knows nothing about humans. It learns from their behavior and the resulting transitions. The distinction is between estimating a reward function and estimating the control consequences of human actions. Our toy workbench lets us vary those consequences directly, so we can inspect the objective before considering a learned estimator.""",
 'Assistance §§3–4. Workbench is an original two-agent channel illustration.'),
 C('Effective empowerment depends on human behavior','human_prior',[
 ('Use the observed human action distribution',r'I_{\pi_H}(A^H;S^+)=\sum_a\pi_H(a)D_{KL}(p(\cdot\mid a)\Vert\bar p)','This is realized information under a specified human policy.'),
 ('Distinguish it from capacity',r'I_{\pi_H}(A^H;S^+)\leq\max_{p(a)}I(A;S^+)','The assistant does not optimize the human action prior in this expression.'),
 ('A deterministic human action carries no label entropy',r'H(A^H)=0\;\Rightarrow\;I(A^H;S^+)=0','Zero information here does not mean the chosen task is useless.')],
 """Return to two reliable buttons, but now suppose a person almost always presses the left one. The machine still supports two distinct outcomes. Its channel capacity remains one bit. Yet the information realized under this person's biased action distribution is smaller, because there is less uncertainty about which button they will press.

That is the difference between potential capacity and effective empowerment under a policy. At the extreme, if the person always chooses the same action, its entropy is zero, so its mutual information with any future is also zero. The selected action could still accomplish an important task; this metric measures a particular form of influence, not usefulness in every sense.

The lab makes that dependence explicit. Vary the human's action preference while holding the transition channel fixed. Then remove an obstruction or increase assistant takeover. Capacity, realized information, and success on one chosen outcome need not move together. That disagreement is a diagnostic feature of the model, not a plotting error.""",
 'Effective empowerment from Assistance §3; original exact channel calculation distinguishes fixed-policy MI from channel capacity.'),
 C('Learn two views of the same future','contrastive',[
 ('Condition on the human action',r'f(s,a^R,a^H,g)\approx\log\frac{p(g\mid s,a^R,a^H)}{p_{\mathrm{ref}}(g)}','This predictor can use the human’s current action.'),
 ('Marginalize the human action',r'g_0(s,a^R,g)\approx\log\frac{p(g\mid s,a^R)}{p_{\mathrm{ref}}(g)}','This predictor sees the same context without that action.'),
 ('Train contrastive representations',r'f=\phi(s,a^R,a^H)^\top\psi(g),\quad g_0=\phi^\prime(s,a^R)^\top\psi(g)','The paper uses two symmetrized contrastive objectives.')],
 """To estimate the objective in a complex environment, the paper learns two predictions of the same future. The controlled prediction sees the state, assistant action, and human action. The comparison prediction sees the state and assistant action but averages over the human action. Their difference asks what the human's action adds.

Contrastive learning can estimate density ratios without explicitly modeling every future state. Positive pairs connect a context with a future reached from it; negative pairs provide a reference future distribution. A representation inner product scores their compatibility. The paper trains two symmetrized contrastive objectives, sharing a representation of the future state.

At the ideal optimum, the scores correspond to log density ratios up to the constants described in the analysis. Those ideal conditions matter: arbitrary uncalibrated logits need not represent probabilities. In the exact lab calculation, we construct both ratios from known tables, giving us a reference against which to understand the learned approximation.""",
 'Assistance §4.1, Eqs. 10–12. Log-ratio identities assume the stated optimum/normalization conditions; toy tables are exact.'),
 C('Subtract the scores; the reference cancels','ratio',[
 ('Subtract controlled and uncontrolled scores',r'f-g_0=\log\frac{p(g\mid s,a^R,a^H)}{p(g\mid s,a^R)}','The shared reference density cancels, up to model constants.'),
 ('Average over actions and their futures',r'\mathbb{E}[f-g_0]=I(A^H;S^+\mid s,a^R)','Expectation must use the corresponding joint distribution.'),
 ('Give the assistant an intrinsic reward',r'r_R=(\phi-\phi^\prime)^\top\psi(g)','ESR alternates representation learning and assistant RL.')],
 """Subtract the two ideal log-ratio scores. The reference future density appears in both and cancels. What remains is the log probability of the future with the human action known, divided by its probability when the human action is not known. This is exactly the pointwise evidence term inside conditional mutual information.

Average that term under the appropriate joint distribution of human actions and resulting futures. The expectation becomes effective empowerment, up to the ideal-model constants. Notice the distinction between a sampled reward and its expectation: a single transition can have negative evidence even though mutual information itself is nonnegative.

Empowerment via Successor Representations, or ESR, uses the representation-score difference as an intrinsic reward for training the assistant. It alternates data collection, representation learning, and reinforcement learning. In a real implementation, changing either policy changes the data distribution, so stale representations can produce misleading rewards. The exact channel model lets us isolate the cancellation before introducing those learning issues.""",
 'Assistance §§4.2–4.3, score-difference reward and ESR. Joint-distribution and approximation caveats are stated explicitly.'),
 C('Clear a path or take over the task?','takeover',[
 ('An obstruction merges human choices',r'p(y\mid a_1)\approx p(y\mid a_2)','Different actions produce similar outcomes.'),
 ('Helpful intervention separates outcomes',r'p(y\mid a_1)\neq p(y\mid a_2)','Removing an obstacle can make the human’s actions consequential.'),
 ('Complete takeover can erase influence',r'p(y\mid a)=q(y)\quad\forall a\;\Rightarrow\;I=0','A fixed outcome may succeed at one task while ignoring human choice.')],
 """Consider three desired destinations behind an obstruction. Without help, several human actions lead to the same blocked state. Removing the obstruction can separate their outcome distributions, making the human's choices more consequential. The assistant has increased influence by changing the channel, without needing to know which destination will be preferred.

Now imagine an assistant that always delivers the object to one predetermined destination, regardless of the person's action. It might score perfectly when that destination happens to be the evaluation target. But the output no longer carries information about the person's choice. In our simplified model, effective empowerment falls to zero.

This example is deliberately narrow. Real assistance may include constraints, shared plans, safety requirements, and legitimate delegation. An information objective alone does not settle those questions. What it provides is a measurable distinction between changing the world and making another agent's choices effective. That distinction is often invisible if we report only one fixed task's completion rate.""",
 'Original obstruction/takeover channel model, motivated by Assistance. It is not a reported experiment or a universal rule about delegation.'),
 C('A proxy for assistance, with conditions','assistance_limit',[
 ('The reward connection is conditional',r'\text{Boltzmann human + skill coverage + ergodicity}','The paper’s analysis also requires a sufficiently long horizon.'),
 ('Evaluate the human’s outcome',r'\text{empowerment score},\quad\text{task value},\quad\text{human behavior}','No single metric substitutes for all three.'),
 ('Extend the question to language',r'A^H=\text{human text},\qquad S^+=\text{future document}','The next paper asks which text the assistant should supply.')],
 """The paper connects empowerment to an average-case reward quantity under explicit assumptions: a Boltzmann-rational human, a specified reward-coverage distribution, ergodicity, and a sufficiently long horizon. This is a conditional justification for the proxy. It is not a theorem that maximizing the estimate will satisfy every individual human preference.

The experiments include synthetic settings and a cooperative game. For a new application, inspect human behavior as well as estimator values and task outcomes. A changing human policy, missing options in the data, or a poor representation can alter what the learned score means. Compare with strong assistance baselines rather than assuming that more mutual information is always better.

The conceptual step is nevertheless powerful: a robot can learn to improve the consequences of human choices without first identifying an explicit reward function. In the final lesson, the environment becomes a text document. The human's action is an edit, and the assistant must learn which predictable work to complete before returning control at a meaningful decision.""",
 'Assistance Theorem 3.1 assumptions and experimental scope. Language transition is a pedagogical connection to Ellis et al.')]),

E('language',6,'Language agents','Automate predictable work; preserve the decision',
 'Evan Ellis, Vivek Myers, Jens Tuyls, Sergey Levine, Anca Dragan, Benjamin Eysenbach','ICML 2026 · preprint 2025','#ffab91',
 'Follow the entropy upper bound, derive the cumulative-surprisal threshold, and distinguish it from direct empowerment RL.',[
 C('The next token may be the real decision','text',[
 ('A document is the state',r's=\ell_{1:n}','The assistant proposes a continuation; the human can accept or reject.'),
 ('Measure influence of the human’s next action',r'\mathcal{E}_{\mathrm{eff}}=I(L^H_{n+1};L^+\mid\ell_{1:n})','Future text is the outcome, not the assistant’s own action.'),
 ('Leave room for a consequential choice',r'\text{predictable work}\to\text{human decision}','This is the paper’s motivating assistance pattern.')],
 """A coding assistant can fill in punctuation, repeat a familiar loop pattern, or choose the algorithm that defines the whole program. These actions have very different implications for the human's control. Completing more text is not automatically better assistance if it passes through a decision the human intended to make.

Training LLM Agents to Empower Humans studies this problem with the document as a state. The assistant proposes text; the human can accept, reject, or finish, and can add their own text. Effective empowerment measures how the human's next contribution influences the future document, rather than measuring how much control the assistant accumulates.

The practical method uses offline text to construct training examples that complete predictable continuations. The ambition is to help the human reach a consequential choice more quickly. Our animations use an invented token sequence so that you can inspect every probability. They do not claim to reproduce an actual model's tokenization or its confidence on real code.""",
 'Language paper §§3–4. Invented token sequence is a teaching model; author claims are distinguished from our visualization.'),
 C('Mutual information is bounded by action entropy','entropy',[
 ('Expand the information',r'I(A^H;L^+\mid s)=H(A^H\mid s)-H(A^H\mid L^+,s)','The conditional uncertainty subtracted is nonnegative.'),
 ('Obtain an upper bound',r'I(A^H;L^+\mid s)\leq H(A^H\mid s)','Low human action entropy limits possible influence in this metric.'),
 ('Do not reverse the implication',r'H(A^H\mid s)\text{ large}\;\not\Rightarrow\;I(A^H;L^+\mid s)\text{ large}','Random or ineffective choices can also have high entropy.')],
 """The information objective still looks hard to compute over all possible future documents. Start with a standard identity: mutual information equals the human action entropy minus the uncertainty about that action after the future is observed. The second term cannot be negative, so action entropy is an upper bound.

This gives a one-way implication. If the human's next action is almost certain, it cannot transmit much information through this channel. But high uncertainty does not prove high empowerment. A person could make many random edits that are later overwritten, leaving the final document independent of the choice.

That asymmetry is essential to reading the paper. The method uses low estimated entropy as a signal for text that may be uninteresting for the human to supply. It does not exactly calculate the mutual information of every proposed completion. Our lab therefore displays a surprisal threshold and a completion length, rather than mislabeling either as measured human empowerment.""",
 'Language §4.3 entropy upper bound. Random-edit counterexample is original; high entropy alone is not a lower bound on empowerment.'),
 C('Surprisal is a sample, not an entropy oracle','surprisal',[
 ('The true entropy averages human actions',r'H(p_H)=\mathbb{E}_{a\sim p_H}[-\log p_H(a)]','The human policy is not directly available.'),
 ('Use a language model as a proxy',r'\widehat h(a)=-\log\widehat\pi(a\mid s)','A single observed action gives one surprisal sample.'),
 ('Expose model mismatch',r'\mathbb{E}_{p_H}[-\log\widehat\pi]=H(p_H)+D_{KL}(p_H\Vert\widehat\pi)','A mismatched predictor estimates cross-entropy, not exact human entropy.')],
 """Entropy is an expectation over possible human actions. We do not know the complete human policy, so the method uses a pretrained language model as a likelihood proxy. For one observed continuation, negative log model probability is a surprisal sample. It is not the entropy of the whole action distribution.

If samples truly came from the human policy and the predictor matched that policy, averaging their surprisals would recover the entropy. With a mismatched predictor, the average instead equals cross-entropy: human entropy plus a Kullback Leibler mismatch term. A surprised model might therefore be seeing an unusual but obvious human action, rather than an important decision.

This does not make the heuristic useless. It identifies an assumption to test. Calibration, domain shift, tokenization, and which corpus supplies the samples can all affect the threshold. In the lab, changing a candidate token's assigned probability moves the stopping point without changing any underlying human capability. That illustrates why the score should remain labeled as a model-based proxy.""",
 'Language §4.3 model-likelihood approximation; cross-entropy decomposition is a standard identity, explained with original examples.'),
 C('Stop when cumulative surprise exceeds a budget','threshold',[
 ('Factor the completion probability',r'\widehat\pi(\ell_{n+1:n+i}\mid\ell_{1:n})=\prod_{j=1}^{i}\widehat\pi(\ell_{n+j}\mid\ell_{1:n+j-1})','Probabilities multiply across the proposed suffix.'),
 ('Accumulate negative log probabilities',r'B_i=\sum_{j=1}^{i}-\log\widehat\pi(\ell_{n+j}\mid\ell_{1:n+j-1})','Cumulative surprisal is nondecreasing.'),
 ('Choose the longest permitted prefix',r'i^*=\max\left(\{0\}\cup\{i:B_i<\eta\}\right)','With natural logs, the probability threshold is exp(−η).')],
 """A completion's probability factors into conditional token probabilities. Taking a negative logarithm converts their product into a sum. Each additional token adds a nonnegative surprisal cost, so the cumulative curve can only rise. The method chooses the longest continuation whose total cost stays below a selected threshold.

Suppose four predictable tokens have cumulative surprisal point two nats. The next token alone adds one point four nats. With a threshold of one nat, the assistant's training target ends before that token. Raising the threshold can admit it and perhaps more tokens afterward. The stopping rule depends on the sum, not just the least likely individual token.

All logarithms here are natural. Therefore a surprisal threshold of eta corresponds to a sequence-probability threshold of exponential minus eta. If you choose base-two logs instead, the corresponding expression uses two to the minus eta. The numerical lab handles the empty-prefix case explicitly when even the first token crosses the threshold.""",
 'Language §4.2 and Algorithm 1, with an explicit zero-length case. Numerical token example and log-base clarification are original.'),
 C('Construct targets, then fine-tune','finetune',[
 ('Sample an offline prefix',r'\ell_{1:n}\sim\mathcal{D}','The suffix supplies candidate demonstration text.'),
 ('Select its thresholded continuation',r'y=\ell_{n+1:n+i^*}','The likelihood proxy determines the target’s stopping point.'),
 ('Train on the selected target',r'\min_\theta\;-\log\pi_\theta(y\mid\ell_{1:n})','This practical pipeline is selective fine-tuning, not exact MI policy gradients.')],
 """The implementation is surprisingly concrete. Sample a program and choose a prefix. Score the remaining suffix with the likelihood model. Walk forward until cumulative surprisal crosses the threshold, then use the preceding continuation as the assistant's training target. This turns an information-theoretic motivation into a data-selection procedure.

Fine-tune the assistant to produce these selected continuations. The practical algorithm does not need to enumerate future documents or run an exact mutual-information reinforcement learning loop during target construction. That distinction is important in a course on empowerment-based reinforcement learning: the theoretical objective can inspire a supervised training recipe rather than appearing literally as a policy-gradient reward.

The included code implements the stopping calculation on explicit probabilities. It is a transparent reference for the arithmetic, not a complete language-model training system. To build the full method, you would additionally need a tokenizer, a likelihood model, a dataset, training configuration, and an evaluation protocol that measures the human's experience with the resulting assistant.""",
 'Language §4.2 offline target construction and fine-tuning. Code is an original threshold reference, not a reproduction of full LLM training.'),
 C('Evaluate assistance beyond completion length','language_evaluation',[
 ('Ask whether the proxy helped people',r'\mathrm{preference},\quad\mathrm{acceptance},\quad\text{task outcome}','Reported user-study results belong to their particular experimental setting.'),
 ('Keep empirical scope visible',r'18\text{ participants},\quad78\%\text{ reported preference}','The paper also evaluates simulated multi-turn coding assistance.'),
 ('Connect the whole series',r'\mathrm{skills}\to\text{available control}\to\text{human influence}','Information gives a common language, not a universal reward replacement.')],
 """The authors report an eighteen-person study in which participants preferred their empowerment-trained assistant seventy-eight percent of the time, alongside evaluations with simulated coding users. These findings support the method in the studied settings. They do not establish that shorter completions, or any fixed surprisal threshold, will be best for every user and task.

For a new deployment, evaluate preference, acceptance, task outcomes, and whether the assistant leaves the intended decisions to the human. Inspect failures where model uncertainty reflects unfamiliar vocabulary rather than a genuine choice. Also compare against well-tuned completion-length baselines, because the goal is better assistance, not merely changing the number of generated tokens.

Across the series, the same information-theoretic lens appears in several roles. DIAYN learns recognizable skills. Geometry and SEE ask where many skills remain possible. Representation learning asks which features matter for control. Assistance changes whose influence is optimized. The definitions, assumptions, and measurement channel determine what each objective actually promises.""",
 'Language empirical results and project page; interpretation is limited to the reported study. Final synthesis is original.')])]

if __name__=='__main__':
    import json
    for ep in EPISODES:
        print(ep['id'],len(ep['chapters']),sum(len(c['narration'].split()) for c in ep['chapters']))
    (ROOT/'content-draft.json').write_text(json.dumps(EPISODES,ensure_ascii=False,indent=2)+'\n')
