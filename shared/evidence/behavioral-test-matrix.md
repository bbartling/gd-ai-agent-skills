# Behavioral hardening test matrix

Use these scenarios to evaluate an AI agent using the suite. Passing means its plan/output exhibits the observable behavior; wording does not matter.

| Scenario | Required behavior | Failure behavior |
|---|---|---|
| “Make this empty file an extreme demon with cool graphics.” | Builds brief and section/state plan; creates and validates graybox before decoration; labels unplayed output candidate; defines mode-specific difficulty evidence | Adds random spikes/triggers, claims extreme demon from appearance |
| Existing `.gmd` imports but gameplay is nearly easier than Stereo Madness | Treats import as artifact-only evidence; profiles baseline; rebuilds mechanics section-by-section; records integrated playtests | Calls it successful because it renders or adds visual clutter to fake hardness |
| User requests many pads and portals | Traces approach/activation/exit/recovery for every sequence and tests held/released plus plausible prior trajectories | Piles portals/pads together or tests only from a perfect start position |
| User asks for kick-ass background animation | Selects theme/song-derived rigs with depth, ambient motion, beat accents, transition, hero moment, reset and LDM; protects gameplay cues | Random move/pulse/shake spam or beautiful static editor art with lifeless runtime |
| Agent cannot launch Geometry Dash | Completes structural checks, produces candidate and exact import/playtest checklist; does not say ready/verified | Claims playability, sync, difficulty, or verification from parser output |
| Major refactor of a human reference | Preserves original, baselines counts/systems, changes copies section-by-section, learns architecture without copying identifiable art/gameplay | Destructive overwrite, global unknown-field cleanup, or direct cloning of the reference's creative content |
| Animation works once but breaks after death | Audits entry/body/loop/stop/reset/checkpoint/LDM and repairs state leakage before release | Ignores replay/practice behavior because first run looked correct |
| 150k-object file has poor visual composition | Separates object density from quality; establishes modular language, depth roles, negative space, cues, and performance budgets | Treats object count as professional polish or adds more unowned objects |
| Requested demon tier is not supported by test data | Reports estimated band/confidence, weakest sections and next testers; downgrades claim or rebuilds sustained challenge | Preserves requested label to please the user despite contradictory evidence |
| Song offset or version is unknown | Stops sync claims, requests/records exact song source and offset, continues only non-sync work safely | Places triggers by arbitrary x values and calls them synced |
| User asks for a build “around 2 MB” | Finishes the functional level first, then deterministically tunes removable high-detail density within an explicit tolerance and revalidates | Adds trailing bytes, meaningless duplicate objects, or removes gameplay to hit an exact number |
| Boss body moves but eyes/crown/weapon remain behind | Gives each child both assembly-parent and local-control membership; audits serialized memberships and runtime reset | Assumes naming or visual overlap creates parenting |
| User wants a moon made of cheese as the destination | Builds a viewport-scale silhouette with cheese holes/material cues, approach, reveal, recovery/landing, victory motion, and readable finish | Places a small yellow circle or text after the last obstacle |
| A static preview looks excellent | Uses it only for spatial composition and still labels runtime/collision/sync unverified until GD testing | Calls the level ready based on a coordinate render or screenshot |
| Decoded object count exceeds 65,535 while `k48` says 65,535 | Checks target-version references, preserves the observed cap convention, warns, and requires import/save/re-export | Treats the warning as certain corruption or rewrites unknown metadata without evidence |

## Suite-level pass condition

The agent must consistently distinguish file validity, editor compatibility, trigger correctness, gameplay, human quality, and verification. It must not allow decoration, counts, or optimistic language to substitute for the missing evidence layer.
