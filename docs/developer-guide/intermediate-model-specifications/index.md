# Intermediate Model Specifications

LEMMA defines *intermediate specifications* for
[domain models](../../user-guide/domain-data-modeling-language/index.md),
[service models](../../user-guide/service-modeling-language/index.md), and
[operation models](../../user-guide/operation-modeling-language/index.md) in
order to facilitate [model processing](../model-processing-framework/index.md).
However, there exist no intermediate specifications for
[technology models](../../user-guide/technology-modeling-language/index.md) and
[mapping models](../../user-guide/service-technology-mapping-modeling-language/index.md).
First, technology information is a crucial concern in model processing.
Therefore, LEMMA will directly incorporate possible technology information
assigned to the elements of domain, service, and operation models into the
corresponding *intermediate models* during the
[process of intermediate model derivation](obtaining-intermediate-models/index.md).
Hence, model processors have immediate access to all technology information.
Second, since mapping models import service models for their technology-specific
refinement, the transformation of a mapping model into an intermediate
representation boils down to the iterative derivation of the intermediate
representations of all imported service models.

## Benefits of Intermediate Models

While it would also be possible to leverage
[Xtext's standalone mechanism]({{ xtext_standalone_url }}) to parse LEMMA models
and then iterate the resulting object graph for model processing purposes,
the usage of intermediate models based on well-defined intermediate
specifications is beneficial in model processing for several reasons:

- Intermediate representations of modeling language concepts can constitute a
  well-defined API for model processors.
- Intermediate specifications decouple modeling languages from model processors.
  As a result, modeling languages may evolve independently from model processors
  as long as the corresponding intermediate representations remain stable.
- Intermediate specifications decrease the semantic gap between modeling
  languages and certain kinds of model processing. That is, because they allow
  implicit incorporation of language-specific characteristics into intermediate
  models. Such characteristics may comprise, e.g., resolved inheritance
  hierarchies or reified default values. Consequently, technology-specific model
  processors like code generators can directly use these information. First,
  this form of preprocessing relieves model processors from acquiring
  language-specific information. Second, it fosters consistent behavior of model
  processors by centralizing the responsibility for the provisioning of
  language-specific information.
- In the context of LEMMA, intermediate models make model processing independent
  of a certain modeling technology. That is, because LEMMA serializes
  intermediate models in the vendor-independent
  [XML Metadata Interchange (XMI) format]({{ xmi_url }}).

## What's Next?

In the following, we describe how to obtain the intermediate representation of a
LEMMA model as an XMI file and provide the intermediate specifications for
[domain models](../../user-guide/domain-data-modeling-language/index.md),
[service models](../../user-guide/service-modeling-language/index.md), and
[operation models](../../user-guide/operation-modeling-language/index.md). More
precisely, these specifications constitute dedicated *intermediate metamodels*
that govern the intermediate representations of LEMMA models both physically
(i.e., within XMI files) and in-memory (i.e., as object graphs that originated
from XMI parsing).
