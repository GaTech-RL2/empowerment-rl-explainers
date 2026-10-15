"""Spoken-first revision: two timed utterances per visual beat.

The full mathematical derivations remain in content.py and the companion.
Pipes separate complete utterances, never arbitrary character-length chunks.
Each utterance has an audio-measured cue; the film draws only the current idea.
"""
SCRIPTS = {}

SCRIPTS['diayn'] = [
('Can you tell which button I pressed?', [
"Imagine two buttons and a puck. The blue button sends the puck left; the yellow button sends it right. Watch what happens when I press blue. | Now hide the buttons. Just by looking at the puck, you can tell which one I pressed. My choice has left a readable mark on the world.",
"Let's change one thing. Disconnect both buttons, and let a fan push the puck randomly left or right. There are still two possible outcomes. | But now seeing the puck tells you nothing about my choice. Variety by itself is not control. We need outcomes that depend on the input.",
"Put those experiments side by side. Both produce the same overall spread of puck positions. Only the working buttons let us send a message. | Mutual information measures how much of our choice survives in the outcome. With two equally likely, perfectly readable buttons, that is one bit, or about point six nine nats."
]),
('Turn a button into a skill', [
"A skill is a button that runs a whole behavior. Give the robot a blue label and keep that label fixed while it moves. | Give it yellow, and it can learn a different behavior. The policy sees both its current state and the chosen label at every step.",
"Now collect many runs. Blue leaves a cloud of visited states; yellow leaves another. Forget the individual paths for a moment and look at those clouds. | Where the clouds overlap, the label is hard to guess. As they separate, a state becomes stronger evidence about which skill was running.",
"This is the central idea of DIAYN, pronounced dye in: learn skills whose states make their identities recognizable, before specifying a task reward. | The method also encourages action randomness within each skill. That flexibility is useful, provided the different skills still leave distinguishable patterns of states."
]),
('Build a reward from a guessing game', [
"Suppose we have four skill labels, all equally likely. Before seeing the robot, a guesser assigns each label probability one quarter. This is the prior. | After seeing a state, the guesser updates its probabilities. The probability assigned to the skill that actually ran tells us how much evidence the state provides.",
"Compare the probability after seeing the state with the probability before. Divide the two, then take a logarithm. That gives the intrinsic reward. | Why a ratio? A guess of one quarter was already available without observing anything. We reward the extra evidence created by the robot's behavior.",
"A perfect guesser would recover mutual information when we average this reward. In practice, we train a neural classifier, so its guesses can be wrong. | The resulting average is a lower bound. The missing amount is a nonnegative divergence between the true posterior and our classifier, averaged over states."
]),
('Watch the reward change', [
"Let's put numbers on the picture. The true label is blue. Its prior probability is one quarter, and the classifier now assigns it point eight. | That is three point two times the prior probability. Taking the natural logarithm gives a positive reward of about one point one six nats.",
"Now move the state into the overlap. The classifier returns to one quarter for blue, exactly where it started before seeing the state. | The ratio becomes one, and its logarithm becomes zero. A state that reveals nothing about the label earns no information reward in this example.",
"Finally, imagine a confident mistake. The classifier assigns the true blue label probability point zero five, even though it strongly prefers another label. | Blue's reward is now negative. Confidence alone is not the target; the observation has to provide evidence for the skill that was actually selected."
]),
('Learn the behavior and the guesser', [
"Where do the training labels come from? We chose them ourselves. Sample blue, run the policy, and store the visited states with that blue label. | These labeled examples train the classifier. It learns which regions of the world each skill tends to visit, without receiving a downstream task reward.",
"Then the classifier supplies rewards to the policy. States that make blue easier to recognize become attractive when the robot is running the blue skill. | The policy improves, its state cloud changes, and the classifier learns again. Picture a feedback loop between better experiments and a better reader of their effects.",
"At first the clouds may nearly coincide. Learning can pull them apart, while the action entropy term allows multiple ways of producing each recognizable pattern. | This is an optimization process, not a guarantee. A weak classifier can give poor rewards, and the features it sees determine which differences count."
]),
('A repertoire is a beginning', [
"After training, the labels act like a small menu of behaviors. A later task can try them, select one, or build a longer sequence from several. | But the menu need not contain every useful behavior. Learning distinguishable skills does not prove that the robot can solve an arbitrary future task.",
"Return to our buttons, now placed at a junction. Each button takes the robot down a different one-way passage. The choices are perfectly distinguishable. | Yet after leaving the junction, the robot may have very few choices left. Demonstrating control and preserving future control are different objectives.",
"Keep the picture of the two clouds in mind. DIAYN asks for behaviors whose states reveal which skill produced them. The classifier turns that question into reward. | Next, we will ask where a robot should stand so that many such choices remain available. That takes us from learning skills to the geometry of empowerment."
])]

SCRIPTS['geometry'] = [
('A junction and a dead end', [
"Place a robot at a junction with three exits. From here it can deliberately reach the blue room, the yellow room, or the pink room. | Move it into a dead end with a one-way entrance. The robot still exists, but two of those choices have disappeared. Location changes its opportunities.",
"At the junction, selecting a skill sends a readable message into the future. At the dead end, different skill labels may all produce the same result. | The Geometry of Empowerment separates the control a particular skill family achieves from the best control available at the current starting state.",
"There is then a second question: how should the robot move to obtain that opportunity? Returning to a useful junction may matter more than immediately exercising a skill. | We will build the geometry behind this idea using three rooms. This small example illustrates the mathematics; it is not a reconstruction of the paper's experiments."
]),
('A point can represent a distribution', [
"A skill does not always end in one room. Suppose blue reaches its room half the time, yellow's room one quarter, and pink's room one quarter. | Draw those probabilities as three bars. Their heights must add to one. We can represent the same three numbers with a single point inside a triangle.",
"The blue corner means all probability is in blue. Halfway along the blue-yellow edge means half in each, with no probability in pink. | The center means equal probability for all three rooms. Moving a point in this triangle changes a distribution, not the robot's physical position.",
"The paper uses distributions of future states sampled at a discounted random time, rather than just a fixed endpoint. Near-future states receive more weight. | The weights are normalized to sum to one. Once we have a distribution for each skill, the same probability geometry applies to those future-state occupancies."
]),
('Information is separation from the average', [
"Give each skill its own point. If blue, yellow, and pink reliably reach different rooms, their points sit near different corners of our probability triangle. | Now choose a skill at random. The overall outcome distribution is the weighted average of the three points. Equal sampling places that mixture at the center.",
"Compare a skill's outcome distribution with that average. A large difference means observing the outcome provides evidence about which skill was chosen. | The relevant difference is a Kullback Leibler divergence, or KL. Mutual information is the sampling-weighted average of these divergences, not the largest one.",
"Now slide all three skill points toward the center. Their outcomes become harder to distinguish, so the information falls. When they coincide, it is zero. | This explains why three names do not necessarily give three choices. What matters is the difference between the distributions those names can actually produce."
]),
('Count effects, not labels', [
"Add a fourth skill, colored teal, that does exactly what blue does. We have increased the number of labels, but added no new physical effect. | If we optimize how often each label is selected, the channel capacity stays the same. Duplicating a button does not create a new distinguishable outcome.",
"Noise also shrinks control. Consider just blue and yellow, and gradually increase the chance that each button produces the other button's outcome. | At a fifty-fifty outcome for either input, the buttons become indistinguishable. Outcome randomness remains, but information about our choice has vanished.",
"Capacity lets us optimize the input probabilities too. For a fixed finite channel, it equals the smallest possible worst-case KL distance to a reference distribution. | Think of finding the best center for a KL information radius. This is a capacity identity after optimization, not a formula replacing every fixed-prior average."
]),
('Why more options is not every reward', [
"Suppose our three rooms offer very different futures. High empowerment favors keeping those futures distinguishable and available. It does not say which room you personally want. | If your only reward is in blue, an agent must still learn that preference. A wide menu and the right order are different pieces of information.",
"The reachable set matters too. Imagine a fourth room behind a sealed wall. Nothing in the robot's current action repertoire reaches it. | An information objective over existing skills cannot make that missing option appear by definition. Learning new dynamics or new skills is an additional problem.",
"So read the geometry as a description of a particular control channel: its starting state, available behaviors, observations, and horizon all shape the picture. | Changing any of those can change the capacity. This precision keeps the appealing phrase 'many options' connected to something we can actually calculate and test."
]),
('Two jobs for two policies', [
"We can now separate two jobs. Inside a chosen state, skill policies discover different futures. Outside that calculation, a preparation policy moves toward useful starting states. | In our example, the preparation policy returns to the junction. The skill policy then chooses which exit to take. The two policies solve different problems.",
"The preparation policy needs a score for each state: how much control could I exercise from here? Computing that score exactly is usually difficult. | A learned skill family and decoder can estimate part of it. But poor skills may make a promising junction look less useful than it really is.",
"Remember the triangle: skills are distributions, their mixture is an average, and information measures how distinguishable the skill-conditioned outcomes are. Capacity optimizes the available choices. | The next paper turns this two-level picture into a scalable learning system, with approximations for the skill, the decoder, and the value of preparing to act."
])]

SCRIPTS['scaling'] = [
('First reach the workshop', [
"Imagine a robot in a narrow corridor, beside a workshop with several tools. In the corridor, its skills mostly move it forward or backward. | Inside the workshop, those skills could produce many more distinct outcomes. Before using a tool, the robot has to reach a place where tools are available.",
"That creates two learning problems. One policy practices distinguishable behaviors from a starting state. Another policy learns to reach promising starting states in the first place. | Scaling Empowered Agents builds around this separation. We will call these the skill policy and the preparation policy, and keep their jobs visually distinct.",
"The skill policy asks what different effects it can produce here. The preparation policy asks where it should go to make those effects possible. | Our workshop is a teaching example. The important feature is the dependency: preparing the world can expand the set of choices an agent will have later."
]),
('Measure a skill through its effect', [
"At the workshop entrance, choose one of four skill labels. Run that skill, then show its future state to a classifier that tries to recover the label. | If the resulting states are distinct, the classifier can identify the skill. Its log probability gain over the prior supplies an intrinsic reward, as in DIAYN.",
"This time, also tell the classifier where the skill started. A future state can have different meanings depending on the starting state that came before it. | For example, ending beside a tool says something different if you began beside it already. Conditioning on the start isolates the information carried by the skill.",
"There are now two reasons for a low score. The skills may produce the same effects, or the classifier may fail to recognize effects that are different. | Keep those failures separate. A low learned information estimate does not, by itself, prove that the starting state has few genuinely achievable options."
]),
('Replace repeated experiments with a value', [
"Testing every skill from every state would be expensive. So learn a value function that predicts the future intrinsic return of the skill policy. | Think of the value as a fast estimate of how readable the skill's future effects will be. It replaces repeated long experiments with a prediction.",
"The paper uses a discounted future-state distribution. Its weights include a factor of one minus gamma, making the entire distribution sum to one. | An ordinary discounted reward sum does not include that normalization. Keep the scale factor when connecting a value estimate to a normalized information quantity.",
"With exact expectations and the appropriate decoder, the population variational objective is a lower bound on information. A fitted neural value is an approximation to that objective. | Its prediction errors can go either way. A high number on a learned critic is therefore not a mathematical certificate of equally high empowerment."
]),
('Prepare, then demonstrate', [
"Now let the preparation policy act. It moves from the corridor toward states where the learned skill value is high. In our example, it enters the workshop. | Only then do we select a skill and demonstrate an effect. The orange preparation path and the colored skill paths belong to different levels of the system.",
"As skills improve, the workshop's estimated usefulness can increase. Better preparation then brings the agent to states that support richer skill practice. | This feedback can help learning, but it can also amplify errors. A bad value estimate may attract the preparation policy to a location that only looks promising.",
"So we should occasionally return to direct evidence. Fix a starting state, sample skills, and inspect the actual resulting distributions rather than only the predicted value. | The key comparison is between opportunities that exist, opportunities the current skills realize, and opportunities the current measurement system manages to recognize."
]),
('Watch the measurement bottleneck', [
"Suppose two tools produce visibly different physical outcomes, but our observation encoder maps both outcomes to exactly the same feature vector. | The classifier cannot distinguish them through that representation. Information about the chosen skill has been lost before the decoder even gets to see the data.",
"Now add a flashing background light that changes independently of the skill. The observation becomes more variable, but the light carries no information about our choice. | In the ideal information calculation, independent nuisance variation cancels. A finite learned system can still waste capacity modeling it, which makes representation design matter.",
"Three bottlenecks now stand between real options and the reported score: the skills themselves, the representation of their outcomes, and the learned decoder or value. | Improving one bottleneck need not fix the others. This is why a larger reported intrinsic return is not enough evidence that an agent became more capable."
]),
('Check what improved', [
"To evaluate the system, hold the starting state fixed and test the skill family. Do different labels reliably produce different outcomes, including on held-out experience? | Then evaluate the preparation policy separately. Does it reach states where those distinctions become easier to achieve, or merely states where the critic is overconfident?",
"The paper develops practical neural approximations to make this learning scalable, including approximations to the relevant classifier structure. Our boxes are the conceptual decomposition. | They are not a complete implementation or a claim that every approximation is exact. The companion gives the equations, source references, and a small inspectable experiment.",
"Keep the workshop picture: first learn what you can do from a place, then learn to reach places where you can do more. | The value function makes that second search practical. Its usefulness depends on how well the skills, observations, and decoder measure the control the world actually permits."
])]

SCRIPTS['representation'] = [
('What should the robot remember?', [
"A robot pushes a puck across a table. Its camera also sees a patterned wall, and a fan blows across the surface. Which details should its representation keep? | The puck position matters because the robot can change it. The wind matters because it changes what a push will do. The wallpaper might not matter at all.",
"Now animate the wallpaper independently. Millions of pixels change, although nothing about the robot's useful choices has changed. A pixel reconstruction objective still has to explain that motion. | An objective based on control asks a different question: which differences help predict the effects of what the agent can choose to do?",
"Learning to Perceive the World Through Control studies how empowerment objectives shape representations. The target is not simply every moving object, or everything outside the robot. | The puck, wind, and wallpaper separate controllable state, relevant context, and irrelevant nuisance."
]),
('Separate the cause from the context', [
"First, freeze the wind. Choose a leftward or rightward push and watch the puck respond. The chosen action leaves a recognizable effect in the puck position. | A useful representation should preserve that distinction. If both outcomes are encoded identically, the representation erases control that the robot actually had.",
"Next, keep the same push but reverse the wind. The future puck position changes. The robot did not choose the wind, yet needs it to predict the outcome. | This is the crucial middle category. Uncontrollable does not mean irrelevant. Removing the wind would make the same encoded state and action produce confusing predictions.",
"Finally, change only the wallpaper. Keep the puck, wind, and chosen push fixed. The physically relevant transition stays the same despite a very different image. | The paper's representation framework separates relevant control structure from exogenous structure. Our three-layer picture illustrates why a representation must retain context while ignoring independent visual clutter."
]),
('Look forward: what can happen next?', [
"Imagine two observations with different wallpaper but identical puck position and wind. From either observation, the same action produces the same distribution over relevant futures. | For predicting those futures, the observations can share a representation. This is the forward-looking idea: compare what can happen next under each available choice.",
"Now compare observations with opposite wind. Apply the same rightward push in both. Their future-state distributions differ, even though the initial puck positions match. | Merging these observations would hide a distinction needed for control. The representation must retain enough context to separate those different consequences of the same action.",
"Notice that we compare distributions, not just one sampled outcome. Two noisy transitions can land in the same place once while still following different underlying dynamics. | A forward equivalence is about matching the appropriate future behavior across actions. A few visually similar examples are not sufficient evidence for that equivalence."
]),
('Look backward: what could have caused it?', [
"There is also a backward-looking question. Given an observed outcome, what does it tell us about the earlier state and the action or skill that produced it? | This is the decoding direction we saw in DIAYN. The final puck position can be evidence about a preceding push, even before we name a downstream task.",
"Two outcomes are equivalent in this direction when they carry the same relevant predecessor evidence. Changing independent wallpaper should not suddenly identify a different preceding skill. | But moving the puck may change that evidence. The forward and backward views preserve different aspects of the same relationship between choices and their consequences.",
"The paper combines information objectives with minimality conditions to characterize which distinctions a representation retains. Minimality prevents it from simply keeping every irrelevant detail too. | These are results under specified assumptions and optimality conditions. They do not say that an arbitrary neural encoder automatically discovers the desired factors during training."
]),
('Why independent clutter cancels', [
"Let a blue skill move the puck left and a yellow skill move it right. Add a background light that independently flashes on or off. | Each skill now has twice as many visible outcomes. Yet after seeing the puck, the light gives no additional evidence about which skill was chosen.",
"Write the information as a log ratio: the outcome probability under a skill, divided by its probability before knowing the skill. The independent light contributes the same factor to both. | Those factors cancel. So the exact mutual information is unchanged, even though the full observation has more entropy and contains more varying pixels.",
"Now connect the light to the wind, or let it reveal the selected skill. The independence assumption breaks, and that cancellation may no longer apply. | Test the assumption: does this feature change dynamics, or reveal the selected skill?"
]),
('Test invariance without losing dynamics', [
"A useful audit changes one part of the scene at a time. Change wallpaper only: the control representation should remain stable when that variation is genuinely irrelevant. | Change wind instead: predictions should adjust because the dynamics changed. Good invariance preserves the distinctions needed for action while removing the ones that do not help.",
"Then test actual behavior. Can a policy using the representation still select different puck outcomes? Does it adapt correctly when the wind changes? | Test control and prediction directly; a tidy embedding alone does not establish either capability.",
"Return to the three layers. Puck position records a controllable effect. Wind supplies necessary context. Independent wallpaper contributes detail without changing the control problem. | The assumptions support the theory; interventions let us investigate these distinctions experimentally."
])]

SCRIPTS['assistance'] = [
('Help someone keep their choices', [
"Imagine a person choosing among three destinations. A box blocks one route. A helper robot can move the box, or simply carry the person to a destination itself. | Both actions change the world. Only one clearly expands what the person can choose. That difference is the starting point for empowerment-based assistance.",
"Move the box aside. Now the person's left, middle, and right choices lead to three distinct outcomes. Their action has more influence over what happens next. | Carry them to the middle regardless of their choice, and that influence disappears. Even a neat-looking outcome can leave the human with less control.",
"Learning to Assist Humans without Inferring Rewards explores assistance through human influence over future states. The assistant learns from interaction instead of first reconstructing an explicit human reward function. | We will use the three routes to understand the objective, then examine how two learned predictors can estimate it, and where the interpretation needs care."
]),
('Whose choices are being measured?', [
"Put the human's action at the input of our channel, and the future state at the output. The assistant changes the environment connecting those two. | If knowing the human's action helps predict the outcome, there is mutual information. Clearing a route can increase that dependence by making another choice effective.",
"But we do not generally choose how often the human presses each button. Their behavior supplies an action distribution, including habits and preferences. | This matters mathematically. Information under an observed human policy differs from the maximum channel capacity obtained by optimizing an arbitrary distribution over human actions.",
"For example, if the human always chooses left, observed action variation is absent. A perfectly usable middle route will not automatically reveal itself in those observations. | The score depends on both the physical possibilities and the human behavior used to probe them. Keep that distinction when interpreting claims about increasing human empowerment."
]),
('Learn two predictions', [
"Suppose we could predict future outcomes twice. The first predictor knows the current context and the human's action; the second knows the context but not that action. | If the action matters, the first predictor gains a real advantage. For a chosen left turn, its prediction concentrates on the left destination.",
"The second predictor averages over the human's possible actions. Its prediction is broader because it has to account for left, middle, and right choices together. | Compare the probability of the actual future under these two predictions. Their log ratio measures the extra information supplied by knowing the human's action.",
"The paper learns the needed quantities using contrastive comparisons between observed futures and reference samples. The predictors distinguish compatible pairs from mismatched ones. | We show probability bars to make the target understandable. The trained contrastive scores approximate density ratios rather than requiring an explicit table of every future state."
]),
('Subtract the shared reference', [
"A contrastive score contains more than the future probability we want. It compares that probability to a reference distribution used to draw contrasting examples. | Picture the same gray reference term underneath both predictors. It is a shared measuring stick, rather than an extra source of human control.",
"Subtract the action-blind score from the action-aware score. When their reference terms match, those terms cancel, leaving the log ratio between the two future predictions. | Averaging the appropriate ratio over interactions gives the mutual-information target. Learning a good estimate still depends on data, model fit, and the assumptions of the estimator.",
"This gives the assistant an intrinsic signal without explicitly identifying a human reward function first. It can favor changes that make the human's choices more consequential. | Return to the box: removing it separates the futures associated with different human actions. That separation is what the learning signal is trying to detect."
]),
('Helpful motion versus taking over', [
"Compare three worlds. With the box in place, two choices collapse onto the same accessible route. The human has fewer distinguishable effects. | With the box removed, all three choices can lead to their intended destinations. In this toy example, the human's influence over the future increases.",
"Now let the robot take over completely. It sends the human to the middle destination whether they choose left, middle, or right. | The outcome may be consistent, but all three arrows merge. The human's action conveys no information about the destination, so this channel has zero mutual information.",
"The picture illustrates why an assistant can be powerful while the person it assists is not. We must specify whose action supplies the channel input. | It also explains why task completion alone can miss a loss of agency. But preserving choice still does not tell us every preference the person has."] ),
('What the objective does and does not establish', [
"A person might dislike all three destinations. Giving them more ways to choose among those destinations does not automatically make the available options desirable. | Empowerment describes influence under a particular model of the interaction. Human benefit can depend on preferences, context, and outcomes that this measurement does not capture.",
"The paper relates its objective to reward under additional assumptions, including a model of human action choice and conditions on tasks and dynamics. | Those assumptions carry real weight. The connection is not a universal proof that maximizing measured influence always improves every person's reward in every environment.",
"Keep the image of clearing the blocked route. The assistant changes what is possible, while the human's choice still determines which future happens. | That is the intuition. The two predictors provide a way to learn a signal for it, and the assumptions tell us how far that signal's interpretation can go."
])]

SCRIPTS['language'] = [
('Where should the assistant stop?', [
"Imagine an assistant drafting a message with you. It begins: 'I recommend we...' The next word might be 'approve' or 'reject.' That is a meaningful choice. | The assistant can finish the sentence on its own, or pause and leave that decision to you. Fluent continuation and preserving your influence are different objectives.",
"Training LLM Agents to Empower Humans studies how to automate predictable portions of an interaction while handing consequential choices back to a person. | The paper uses a practical information-based proxy. To understand it, we need to separate three quantities that are easy to blur together: entropy, surprisal, and empowerment.",
"Keep our unfinished sentence on screen. Common introductory words offer little branching; 'approve' and 'reject' can lead to very different outcomes. | This is an illustrative example, not a quotation of a paper experiment. It will let us compute the stopping rule token by token and inspect its limitations."
]),
('Uncertainty is not automatically influence', [
"Entropy measures uncertainty across possible choices. If a human's decision is completely fixed, there is no variation in that decision to transmit through the interaction. | That gives an upper bound: information between the human's choice and the eventual outcome cannot exceed the entropy of the choice itself.",
"But an upper bound does not work in reverse. High choice entropy does not guarantee that those choices have any effect on what the assistant does. | Imagine a random decision followed by an assistant that always sends the same message. The decision is unpredictable, yet its influence on the output is zero.",
"This matters because a likelihood-based language-model score is easier to compute than full human-to-outcome mutual information. It can supply a useful approximation for deciding when to pause. | We should still call it a proxy. Surprising text might reflect a meaningful human choice, an unfamiliar phrase, or simply a poor predictive model."
]),
('A token spends a surprise budget', [
"Now look at a single predicted token. If the model assigns it probability point nine, its surprisal is the negative logarithm of point nine: a small amount. | If the probability is point one, the surprisal is much larger. A token that the model expected less spends more of our surprise budget.",
"Surprisal belongs to a particular observed token. Entropy is the average surprisal under the distribution itself. One surprising token is not a complete entropy estimate. | And when our model's probabilities differ from the real distribution, average model surprisal includes an extra mismatch term, the KL divergence between those distributions.",
"That mismatch is why a rare name might trigger a pause even when no important decision is being made. The model can be surprised for the wrong reason. | Conversely, a familiar but consequential decision may be easy to predict. A practical stopping policy must be evaluated on interactions, not justified by the proxy's name alone."
]),
('Walk through the stopping rule', [
"Give the assistant a cumulative budget of one nat. Add the negative log probability of each generated token to a running total, starting from zero. | The words 'I recommend we' are all highly probable in this toy model. Their combined surprise stays low, so the assistant can continue through that predictable prefix.",
"Now consider 'approve,' assigned probability point one five. That word alone costs about one point nine nats, pushing the total beyond our one-nat budget. | The accepted prefix stops before that token. It ends at 'I recommend we,' leaving the branch between approval and rejection for the human to decide.",
"The rule uses a strict threshold: the accepted cumulative surprise must stay below the budget. Equivalently, the prefix probability must stay above the exponential of minus that budget. | These are two views of the same arithmetic. They do not guarantee that every threshold crossing identifies a meaningful human decision in a real conversation."
]),
('Learn from the accepted prefix', [
"The budget now determines which parts of a demonstration become training targets. Predictable prefixes are kept; the continuation beyond the selected stopping point is excluded from those targets. | The model is then fine-tuned on the selected material. This is a concrete way for the stopping criterion to shape what the assistant learns to automate.",
"Move the budget slider downward and the accepted prefix gets shorter. Move it upward and the model can continue farther before yielding control. | This creates a tradeoff between doing useful routine work and leaving choices available. The best setting depends on the interaction and the quality of the likelihood model.",
"The paper's practical training procedure uses target selection and supervised fine-tuning. It does not directly optimize an exact human empowerment quantity through a standard policy-gradient estimator. | That distinction is useful when reproducing the method: first understand the scoring, prefix selection, and training targets, then evaluate the resulting interaction behavior."
]),
('Evaluate the handoff', [
"To test the method, watch what happens at the handoff. Does the assistant complete the predictable work? Does it pause before committing the user to a consequential branch? | Also check unnecessary interruptions. A system that asks about every token preserves very little convenience, even if it leaves every microscopic choice to the human.",
"The paper reports human preference evidence in a particular study, alongside its other evaluations. Such results support claims about that setting, not every possible user or task. | For a new deployment, measure both task outcomes and retained human influence. The two can move differently, and a language-model likelihood score cannot replace either measurement.",
"Return to our sentence. A helpful assistant writes the predictable setup, then leaves 'approve' or 'reject' open when that is the decision the person should make. | The recurring question is whose choices remain distinguishable in the future. Here, useful progress should keep the human in that loop."
])]

def validate():
    for key, chapters in SCRIPTS.items():
        assert len(chapters)==6,key
        for title,beats in chapters:
            assert len(beats)==3,title
            assert all(len(b.split('|'))==2 for b in beats),title
        words=sum(len(b.replace('|','').split()) for _,beats in chapters for b in beats)
        print(key,words,'words')

if __name__=='__main__':validate()
