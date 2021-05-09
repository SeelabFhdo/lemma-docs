# Context and Motivation

## Context

LEMMA is rooted in the domain of [Microservice Architecture]({{ msa_def_url }})
(MSA), which is an architectural style targeting distributed, *service-oriented
software systems*.

MSA promotes to decompose a software system into *microservices*, which are
components that

- provide a **single, distinct functional or infrastructure capability** to other
architecture components by means of well-defined interfaces,
- are **as independent as possible** from other components w.r.t.
implementation, data management, testing, deployment, and operation,
- are **fully accountable** for all aspects related to their interaction with
other components,
- are **owned by exactly one team**, which takes full responsibility for design,
implementation, and operation issues related to their microservices.

Given the above characteristics of a microservice, MSA aims to particularly
increase the scalability and maintainability of software systems.

## Motivation

While the adoption of MSA is expected to yield several benefits, it also comes
with an *increased degree of complexity* compared to
[monolithic applications]({{ monolith_def_url }}) and their usual
[multitier architecture]({{ ntier_def_url }}):

- **Design Complexity:** Typical challenges in MSA design comprise the
*identification of microservices*, the *determination of their granularity*, and
the *design of their APIs*.
- **Implementation Complexity:** The increased independence of microservices enables
teams to employ the most suitable technologies to realize their services. These
technologies may concern, e.g., programming languages, database systems,
communication protocols, and data formats. However, the resulting
[technology heterogeneity]({{ tech_hetero_def_url }}) bears a greater risk for
technical debt, additional maintainability costs, and steeper learning curves.
Consequently, it calls for dedicated management activities.
- **Operation Complexity:** MSA emphasizes loose coupling of architecture
components, which increases scalability but also requires dedicated components
that provide microservices with capabilities such as service discovery, API
provisioning, load balancing, and monitoring. These components require regular
maintenance and management, which may be aggravated again by an increased
technology heterogeneity.
- **Organizational Complexity:** MSA is most effective when the structure of the
organization is also aligned towards the architectural style. That is, the
organization or parts thereof are also decomposed along the communication
structures of the eventual software architecture. In particular, MSA fosters
DevOps practices so that teams should be composed of members with heterogeneous
professional backgrounds. However, the introduction of a DevOps culture also
requires the *automation of manual tasks* and *sharing of knowledge across team
boundaries*[^1].

With LEMMA, we [study](../research/index.md) the support of
[Model-driven Engineering]({{ mde_def_url }}), and especially the abstraction
power of models and modeling languages, to mitigate the impact of the
aforementioned degrees of MSA complexity.

[^1]: [{{ devops_culture_url }}]({{ devops_culture_url }})
