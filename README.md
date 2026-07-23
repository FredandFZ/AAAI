# UHD: An E-Recruitment Recommendation Dataset for Impression-Aware Recommendation

UHD (**Upwork Hiring Dataset**) is a large-scale e-recruitment recommendation dataset collected from the Upwork platform. It is designed to support research on **impression-aware recommendation**, **sequential recommendation**, **multi-behavior recommendation**, **item-level fairness**, and **conversion-rate prediction** in online hiring.

Unlike conventional recommendation datasets that record only user–item interactions, UHD also records the freelancer profiles that were actually shown to each employer, the true on-screen order in which they appeared, and the behaviors that followed the exposure. This makes it possible to distinguish:

- an item that was **exposed but ignored**, and
- an item that was **never exposed**.

This distinction is important because treating every unobserved interaction as negative feedback can introduce exposure bias, selection bias, and popularity bias.

> **Recommendation direction:** UHD models employers as users and freelancers as items. The primary task is to recommend suitable freelancer candidates to employers.

---

## Table of Contents

- [Why Impression Data Matter](#why-impression-data-matter)
- [Key Features](#key-features)
- [Dataset Statistics](#dataset-statistics)
- [Data Construction](#data-construction)
- [Repository and Data Files](#repository-and-data-files)
- [Data Schema](#data-schema)
- [Impression Encoding](#impression-encoding)
- [Loading the Data](#loading-the-data)
- [Supported Research Tasks](#supported-research-tasks)
- [Benchmark Models and Evaluation](#benchmark-models-and-evaluation)
- [Main Findings](#main-findings)
- [Data Quality, Privacy, and Ethics](#data-quality-privacy-and-ethics)
- [Scope and Limitations](#scope-and-limitations)
- [Citation](#citation)

---

## Why Impression Data Matter

Most recommender systems learn user preferences from historical interactions such as clicks, messages, purchases, or hires. However, interaction-only logs do not reveal whether an uninteracted item was actually shown to the user.

For example:

- A freelancer profile was shown to an employer, but the employer did not click it.
- Another freelancer profile was never shown to the employer.

These two cases should not be treated as equivalent negative feedback. The first case contains evidence of exposure without interaction, while the second contains no direct preference signal.

UHD addresses this problem by linking each interaction to its exact exposure context.

![How Impressions Influence User Interactions?](figures/toy.png)

In UHD, an impression represents a single search session in which an employer is shown an ordered list of freelancer profiles. Each record preserves the true display order and indicates whether the employer clicked, invited, messaged, or hired any exposed freelancer.

---

## Key Features

- **Real-world e-recruitment data** collected from the Upwork platform.
- **Employer-to-freelancer recommendation**, rather than the more common job-to-job-seeker direction.
- **Rank-aware impressions** that preserve the true on-screen order of exposed freelancer profiles.
- **Session-level exposure context**, independently logged for each employer and search session.
- **Four interaction types:** click, invite, message, and hire.
- **Interaction–impression linkage** through `impression_id`.
- **Anonymized freelancer profiles** with job titles, descriptions, skills, and availability information.
- **Multiple dataset scales:** UHD-full, UHD-50K, and UHD-5K.
- Support for studying **recommendation accuracy, long-tail fairness, exposure bias, and delayed conversion feedback**.

---

## Dataset Statistics

| Statistic | UHD-full | UHD-50K | UHD-5K |
|---|---:|---:|---:|
| Users / employers | 228,595 | 50,000 | 5,000 |
| Items / freelancers | 178,407 | 156,241 | 57,015 |
| Interactions | 7,730,713 | 1,697,797 | 209,622 |
| Impressions | 6,024,820 | 1,326,560 | 137,944 |
| Average impression length | 5.33 | 5.32 | 5.22 |
| Clicks | 4,506,944 | 989,624 | 118,138 |
| Invites | 1,460,965 | 318,681 | 50,251 |
| Messages | 1,520,621 | 336,343 | 35,565 |
| Hires | 242,183 | 53,149 | 5,668 |

### Time Coverage

- **Impression logs:** January 8, 2024 to June 1, 2024
- **Interaction logs:** January 8, 2024 to approximately mid-June 2024

The interaction period extends beyond the impression period to capture delayed behaviors, especially messages and hires that may occur several days after the initial exposure.

---

## Data Construction

![UHD Construction Pipeline and Quality Controls](figures/uhd.png)

The UHD construction pipeline contains three main stages.

### 1. Period Determination

A relatively stable platform period is selected to reduce the influence of major recommendation-policy or business-strategy changes.

### 2. Data Cleansing

The cleaning process includes:

- removing records that violate business logic;
- filtering inactive employers and freelancers;
- detecting duplicated, corrupted, or incomplete records;
- removing implausibly long impression sessions;
- checking consistency between impression and interaction logs;
- validating temporal order between exposure and subsequent interaction.

The filtering process is designed conservatively to preserve the original data distribution while reducing logging artifacts.

### 3. Identifier Anonymization

All employer, freelancer, and impression identifiers are anonymized. Free-text profile fields are processed to reduce re-identification risk while preserving useful semantic information.

Examples of privacy processing include:

- generalizing precise locations to the country level;
- removing contact information;
- replacing specific school names with coarse descriptions;
- replacing specific employer names with coarse categories;
- retaining non-sensitive text when no identifying information is detected.

---

## Repository and Data Files

```text
UHD-demo/
├── behaviors.tsv
├── impressions.tsv
├── freelancer_meta.jsonl
├── sample.py
├── figures/
│   ├── toy.png
│   └── uhd.png
└── README.md
```

| File | Description |
|---|---|
| `behaviors.tsv` | Timestamped employer–freelancer interaction logs. |
| `impressions.tsv` | Ordered freelancer exposure lists for individual search sessions. |
| `freelancer_meta.jsonl` | Anonymized and cleaned freelancer profile metadata. |
| `sample.py` | Utility for constructing demo, UHD-5K, or UHD-50K subsets from UHD-full. |

> Due to GitHub file-size limits, large data files are distributed through the repository's **Release Assets** rather than committed directly to the Git repository.

---

## Data Schema

### Interaction Data

File: `behaviors.tsv`

| Field | Type | Description |
|---|---|---|
| `user_id` | string / integer | Anonymized employer identifier. |
| `item_id` | string / integer | Anonymized freelancer identifier. |
| `behavior_ts` | timestamp | Time at which the interaction occurred. |
| `behavior_type` | integer | Interaction type: `1` click, `2` invite, `3` message, `4` hire. |
| `impression_id` | string / integer | Identifier of the impression session that exposed the freelancer. |

### Interaction Type Mapping

| Value | Behavior |
|---:|---|
| `1` | Click |
| `2` | Invite |
| `3` | Message |
| `4` | Hire |

The `impression_id` field makes it possible to trace an interaction back to the exact recommendation list and display position that preceded it.

---

### Impression Data

File: `impressions.tsv`

| Field | Type | Description |
|---|---|---|
| `impression_id` | string / integer | Unique anonymized identifier for the impression session. |
| `user_id` | string / integer | Anonymized employer who received the impression. |
| `impression_ts` | timestamp | Time at which the recommendation list was shown. |
| `impressions` | string / list | Ordered list of exposed freelancers and their session behaviors. |

Each row corresponds to one search or recommendation session. Items in `impressions` are ordered according to their true on-screen display positions.

---

### Freelancer Metadata

File: `freelancer_meta.jsonl`

| Field | Type | Description |
|---|---|---|
| `item_id` | string / integer | Anonymized freelancer identifier. |
| `registration_date` | date / timestamp | Date on which the freelancer profile was registered. |
| `job_title` | string | Professional title shown on the freelancer profile. |
| `overview` | string | Anonymized self-introduction or profile overview. |
| `skill_tags` | list / string | Skills associated with the freelancer profile. |
| `open_to_hire` | boolean / integer | Whether the freelancer is open to new hiring opportunities. |
| `available_hours` | numeric | Profile availability duration, measured in hours. |

---

## Impression Encoding

The `impressions` field uses the following format:

```text
item_id:behavior,item_id:behavior,item_id:behavior,...
```

The list order is the real display order.

For each exposed freelancer:

- `0` means that the freelancer was shown but received no recorded interaction in that session.
- One or more interaction IDs indicate the observed behaviors.
- Multiple behaviors are separated by `/`.

### Example

```text
V120288:0,V12057:1/3,V73451:0
```

This example means:

1. `V120288` was displayed first and received no interaction.
2. `V12057` was displayed second and received both a click (`1`) and a message (`3`).
3. `V73451` was displayed third and received no interaction.

A possible parser is shown below:

```python
def parse_impression_list(value: str) -> list[dict]:
    """Parse an ordered UHD impression string."""
    parsed = []

    for position, entry in enumerate(value.split(","), start=1):
        item_id, behavior_text = entry.split(":", maxsplit=1)

        if behavior_text == "0":
            behaviors = []
        else:
            behaviors = [int(x) for x in behavior_text.split("/")]

        parsed.append(
            {
                "position": position,
                "item_id": item_id,
                "behaviors": behaviors,
            }
        )

    return parsed
```

---

## Loading the Data

The following example loads the three TSV files with `pandas`.

```python
from pathlib import Path

import pandas as pd

data_dir = Path("path/to/UHD")

behaviors = pd.read_csv(data_dir / "behaviors.tsv", sep="\t")
impressions = pd.read_csv(data_dir / "impressions.tsv", sep="\t")
freelancers = pd.read_csv(data_dir / "freelancer_meta.tsv", sep="\t")

print("Interactions:", len(behaviors))
print("Impression sessions:", len(impressions))
print("Freelancer profiles:", len(freelancers))
```

### Join Interactions with Exposure Context

```python
interaction_context = behaviors.merge(
    impressions[
        ["impression_id", "user_id", "impression_ts", "impressions"]
    ],
    on=["impression_id", "user_id"],
    how="left",
    validate="many_to_one",
)

print(interaction_context.head())
```

This join connects each observed click, invite, message, or hire to the recommendation list that exposed the corresponding freelancer.

### Basic Integrity Checks

```python
assert behaviors["user_id"].notna().all()
assert behaviors["item_id"].notna().all()
assert behaviors["behavior_type"].isin([1, 2, 3, 4]).all()
assert impressions["impression_id"].is_unique

linked_ratio = behaviors["impression_id"].isin(
    impressions["impression_id"]
).mean()

print(f"Interactions linked to an impression: {linked_ratio:.2%}")
```

---

## Supported Research Tasks

UHD can support several recommendation and e-recruitment research directions.

### 1. Sequential Recommendation

Predict the next freelancer with whom an employer will interact from the employer's chronological behavior history.

Possible targets include:

- next click;
- next invitation;
- next message;
- next hire.

### 2. Impression-Aware Recommendation

Use historical exposure lists to distinguish exposed-but-uninteracted freelancers from freelancers that were never shown.

This enables more faithful negative sampling and preference estimation.

### 3. Multi-Behavior Recommendation

Model the progression among different employer behaviors:

```text
impression → click → invite/message → hire
```

The four behavior types can be treated as different levels of engagement or conversion.

### 4. Candidate Ranking

Rank freelancer candidates for an employer while accounting for:

- historical interactions;
- historical impressions;
- display position;
- freelancer profile content;
- freelancer availability.

### 5. Exposure and Popularity Bias

Study how platform exposure affects observed interactions and how impression-aware models can reduce the over-recommendation of popular freelancers.

### 6. Long-Tail Fairness

Evaluate whether recommendation models provide sufficient visibility to freelancers with relatively low historical exposure and interaction frequency.

### 7. Conversion-Rate Prediction

Predict conversion processes such as:

- impression → click;
- impression → invite;
- impression → message;
- impression → hire.

### 8. Delayed Feedback Modeling

Model interactions that occur after a delay, especially hires that may happen several days after the original profile exposure.

### 9. Content-Based Recommendation

Use `job_title`, `overview`, `skill_tags`, and availability features to recommend freelancers when interaction histories are sparse.

### 10. Generative Recommendation

Use freelancer identifiers or profile representations as targets in generative sequential recommendation models.

---

## Benchmark Models and Evaluation

The accompanying paper evaluates seven representative recommenders from three model families.

### Sequential Models

- Attention
- SASRec
- GRU4Rec

### Graph-Based Models

- LightGCN
- MBHT

### Generative Models

- CVAE
- DiffuRec

### Evaluation Protocol

The paper uses a chronological leave-one-out protocol for sequential recommendation:

- the latest interaction is used as the test target;
- the second-latest interaction is used for validation;
- earlier interactions are used for training.

Full-sort evaluation is used, meaning that the model ranks the complete candidate set rather than a small set of sampled negatives.

### Ranking Metrics

- `HR@5`
- `HR@10`
- `NDCG@5`
- `NDCG@10`

`HR@K` measures whether the ground-truth freelancer appears in the top-K list. `NDCG@K` additionally rewards models that place the relevant freelancer closer to the top.

### Conversion Metrics

For conversion-rate prediction, metrics such as AUC, log loss, and accuracy can be used.

### Fairness Analysis

Items can be divided into `HEAD`, `MID`, and `TAIL` groups according to their exposure and interaction frequencies. The proportion of each group in the top-K recommendation list can then be used to study item-level exposure fairness.

---

## Main Findings

Experiments reported in the paper show that impression information provides useful signals beyond interaction-only histories.

### Recommendation Accuracy

Adding impression information improves ranking performance across all evaluated model families.

Representative results include:

- LightGCN obtains approximately 26% improvement in `HR@10`.
- SASRec obtains a 21.19% improvement in `HR@5` on UHD-50K.
- DiffuRec obtains a 24.76% improvement in `NDCG@5` on UHD-50K.

The improvements suggest that historical exposure contains preference information that cannot be recovered from interaction logs alone.

### Long-Tail Fairness

For the Attention recommender's Top-10 results:

| Item group | Interaction only | Interaction + impression |
|---|---:|---:|
| HEAD | 86.3% | 55.3% |
| MID | 11.3% | 32.5% |
| TAIL | 2.4% | 12.2% |

The results show that impression-aware learning can substantially increase the representation of medium-popularity and long-tail freelancers.

### Conversion Prediction

Impression information also improves conversion prediction:

| Conversion task | Interaction only | With impression |
|---|---:|---:|
| Impression → Click AUC | 0.76 | 0.81 |
| Impression → Hire AUC | 0.60 | 0.65 |

The gain on impression-to-hire prediction is particularly relevant because hiring decisions often involve longer feedback delays than clicks.

---

## Data Quality, Privacy, and Ethics

UHD is constructed from anonymized platform logs in accordance with Upwork's privacy and user-consent policies.

The dataset construction process includes:

- identifier anonymization;
- personally identifiable information removal;
- coarse generalization of schools, employers, and locations;
- manual inspection of sampled records;
- temporal consistency checks;
- distribution and stability checks;
- semantic validation between employer needs and interacted freelancer profiles.

Users of UHD should:

- use the data only for legitimate research purposes;
- avoid attempts to re-identify employers or freelancers;
- follow the repository's license and data-use terms;
- report aggregate results rather than exposing individual records;
- consider fairness implications when developing hiring recommendation systems.

---

## Scope and Limitations

UHD is primarily a benchmark for recommendation and exposure modeling. It does not by itself provide a complete evaluation environment for an end-to-end hiring agent.

For example, the released data do not directly evaluate whether an agent can:

- conduct a multi-turn requirements clarification dialogue;
- decide when to search, inspect profiles, or ask follow-up questions;
- reason about all client constraints;
- negotiate with freelancers;
- verify final work quality after hiring.

UHD can nevertheless serve as a strong component for candidate retrieval, ranking, readiness modeling, and hiring-conversion prediction in a broader agent benchmark.

The impression logs are observational platform data. Researchers should therefore remain cautious about causal conclusions, since exposure is influenced by the production recommendation system and platform policies.

---

## Citation

Citation information will be updated after publication.

```bibtex
@inproceedings{uhd2026,
  title     = {UHD: An E-Recruitment Recommendation Dataset for Impression-Aware Recommendation},
  author    = {Anonymous},
  booktitle = {To appear},
  year      = {2026}
}
```

---


