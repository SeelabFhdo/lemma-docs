# Quick Tour

In the following, we will demonstrate some of the basic features of LEMMA
regarding the construction of models for microservice architectures and their
processing. To reproduce the presented modeling and processing steps, you may
first want to [install LEMMA](..) on your computer.

## The Park and Charge Platform Example
For the quick tour of LEMMA, we refer to a single microservice from an
MSA[^1]-based application that allows the management of parking spaces with
capabilities for electric vehicle charging. More specifically, we will call this
application the Park and Charge Platform, or short PACP.

The PACP consists of several microservices, e.g., for user management, parking
space configuration and provisioning, and parking space searching. For the quick
tour of LEMMA, we are going to model the domain data, API, and deployment of the
latter microservice, i.e., the `SearchForFreeSpace` microservice. This
microservice shall provide its clients with means to search for spare parking
spaces with electric vehicle charging capabilities in a given location.

## What you will Learn During the Tour
In the following you will learn how to construct the following types of LEMMA
models for the `SearchForFreeSpace` microservice:

- Domain model: Defines the domain information of the microservice.
- Service model: Defines the API of the microservice.
- Operation model: Defines the deployment of the microservice.

In addition, you will receive an impression on how model processing works with
LEMMA. More specifically, you will learn how to derive executable Java code from
the constructed models.

The next sections will teach you how to construct the aforementioned LEMMA
models for the `SearchForFreeSpace` microservice by means of a
[LEMMA-enabled Eclipse installation](..). If you do not want to construct the
models on your own, you can also
[download a ZIP archive](example_model_code/{{ lemma_tour_models_project_name }}.zip),
which includes all three models.

## Step 1: Creating an Eclipse Project
In the [LEMMA-enabled Eclipse installation](..), create a new Java project
called `{{ lemma_tour_models_project_name }}`. We will use this project to
gather all models for the `SearchForFreeSpace` microservice. In addition, create
a folder called `models` within the project.

The Project Explorer of your Eclipse workspace should now look similar to this:
<figure>
  <img src="../figures/tour-step1-project.png" loading="lazy"/>
</figure>

## Step 2: Create a Domain Model
LEMMA provides several modeling languages to express different viewpoints on a
microservice architecture. A crucial viewpoint in almost every software project
including microservice architecture is the *domain viewpoint*, for which LEMMA
comprises the
[Domain Data Modeling Language](../../user-guide/domain-data-modeling-language)
that enables domain experts and microservice developers to collaboratively
construct *domain models*.

LEMMA recognizes domain models in the Eclipse IDE by means of the file extension
`data`. For the `SearchForFreeSpace` microservice, we cluster related domain
data in a file called `domain.data` within the `models` folder of the previously
created `{{ lemma_tour_models_project_name }}` Eclipse project. Create this file
leveraging the Eclipse IDE. In case a dialog pops up, asking you to convert the
`{{ lemma_tour_models_project_name }}` project to an Xtext project, just confirm
it with `Yes`.

The Project Explorer of your Eclipse workspace should now look similar to this:
<figure>
  <img src="../figures/tour-step2-domain-model.png" loading="lazy"/>
</figure>

As you can see, Eclipse displays an error marker for the model. That is, because
LEMMA's
[Domain Data Modeling Language](../../user-guide/domain-data-modeling-language)
does not allow empty domain models. To fix this issue, add the following model
code to the `domain.data` file by double-clicking the file in Eclipse's Project
Explorer and entering the code in the text editor that just opened:

```lemmadomaindata
--8<-- "getting-started/example_model_code/models/domain.data"
```

### Bounded Contexts
The
[Domain Data Modeling Language](../../user-guide/domain-data-modeling-language)
enables to organize the concepts of a microservice's domain excerpt within
contexts. You can introduce a context with the keyword `context` followed by the
name of the context and a pair of curly brackets. With this approach, the
example domain model for the `SearchForFreeSpace` microservice defines a context
called `ParkingSpace`. LEMMA's notion of context as a cluster for domain
concepts is inspired by the [Bounded Context pattern]({{ bounded_context_url }})
from [Domain-driven Design (DDD)]({{ ddd_def_url }}) and its importance for the
[tailoring of microservices' domain responsibility]( {{ msa_bc_url }} ).

A context clusters one or more domain concepts between a pair of curly brackets.
LEMMA supports several kinds of domain concepts and the above example
illustrates the definition of structured and list concepts.

### Structured Domain Concepts and Domain-Driven Design
A structured concept (or *data structure*) is introduced by the keyword
`structure`, followed by the name of the structure and an arbitrary number of
*features*. In LEMMA domain models, a feature assigns additional semantics like
patterns from [tactical DDD]({{ ddd_tactical_patterns_url }}) to a domain
concept. Furthermore, a data structure consists of an arbitrary number of typed
and named *data fields* clustered in curly brackets. Consider the `Location`
structure from the example domain model above. It receives the *valueObject*
feature to identify it as a [DDD Value Object]({{ ddd_value_object_def_url }}).
Moreover, the structure consists of six data fields, which all exhibit the
`immutable` identifier. That is, the values of the fields remain stable after
their initialization. LEMMA supports all primitive types of Java and also treats
`String` as a primitive type that can store a sequence of characters of
arbitrary length. Take for example the fields `latitude` and `street` of the
`Location` structure, which have the types `double` and `string`, respectively.

The `ParkingSpace` concept is another example of a domain-specific data
structure. It receives the features `aggregate` and `entity`, and is thus a
[DDD Aggregate]({{ ddd_aggregate_def_url }}) and
[DDD Entity]({{ ddd_entity_def_url }}). In DDD terms, based on this combination
of patterns, the structure of the `ParkingSpace` concept also specifies the
structure of the aggregate's *root entity* to be stored, e.g., in a database.
Like the `Location` concept, the `ParkingSpace` concept consists of six data
fields of the `id` field is the `identifier` of the root entity, and the
`capacities` and `location` fields are *parts* of the root entity, whose
structures are to be embedded into the root entity structure upon storage. In
addition, both fields show LEMMA's support for complex typing of data fields.
That is, next to primitive types like `double` and `string`, you can also use
domain concepts such as `VehicleCounts` (see below) and `Location` to type data
fields.

The example domain model contains a third data structure, i.e., `VehicleCount`,
which is a value object and consists of three primitively typed data fields. By
contrast to the fields of the `Location` structure, the `VehicleCount` fields
are mutable due to the lack of the modifier `immutable`.

### List Type Domain Concepts
Next to data structures, the example domain model defines two *list types* using
the `list` keyword. In LEMMA, a list type specifies a sequence of one or more
data fields that can have a primitive or complex type. Both list types in the
example domain model, i.e., `ParkingSpaces` and `VehicleCounts`, have one field
(`parkingSpace` and `vehicleCount`, respectively) of a structured type
(`ParkingSpace` and `VehicleCount`, respectively).

## Step 3: Create a Service Model
In this step, we use LEMMA's
[Service Modeling Language](../../user-guide/service-modeling-language) to
construct a *service model* for the `SearchForFreeSpace` microservice. The
modeling language covers the concerns of microservice developers, thereby
providing a means to express the *service viewpoint* on a microservice
architecture.

In the `models` folder of the `search-for-free-space` Eclipse project, create a
file called `micro.services` so that the Project Explorer of your Eclipse
workspace looks similar to this:
<figure>
  <img src="../figures/tour-step3-service-model.png" loading="lazy"/>
</figure>

As for the initial domain model constructed in Step 2, LEMMA does not allow
empty service models and thus displays an error marker for the `micro.services`
file. To fix this issue, add the following service model code to the file:

```lemmaservices
--8<-- "getting-started/example_model_code/doc-models/technology-agnostic-micro.services"
```

### Domain Concept Imports
LEMMA's modeling languages support an `import` statement that enables to
integrate models for different viewpoints on a microservice architecture. These
statements always have the following syntactic form:
!!! example ""
    `import [ELEMENT_TYPE] from "[MODEL_PATH]" as [ALIAS]`
In the example service model, the imported `[ELEMENT_TYPE]` is `datatypes`,
which accounts for the import of domain concepts to be used as data types for
service operation parameters (see below). The example `[MODEL_PATH]` is
`domain.data`, i.e., it points to the domain model that we constructed above.
All domain concepts from the model are imported under the `[ALIAS]` `domain`.
The alias of a LEMMA import provides a shortcut to access the elements of an
imported model.

### Microservice Definition
A microservice definition is introduced by an optional *visibility modifier*,
followed by a mandatory *service type identifier*, the keyword `microservice`,
and the fully-qualified name of the microservice.

In the example service model, the visibility modifier of the
`SearchForFreeSpace` microservice is `public`, which expresses the intent to
make the microservice available to consumers that are not part of the same
microservice architecture. Microservices without an explicit visibility modifier
receive have `architecture` visibility, i.e., they are visible only to
microservices that belong to the same architecture and are not to be exposed to
external consumers.

The service type identifier is `functional`, which marks the microservice to
fulfill a functional, usually business-oriented capability within the considered
microservice architecture. Other available type identifiers are `infrastructure`
(the microservice provides an infrastructure capability, e.g., monitoring) and
`utility` (the microservice provides a reusable utility capability that is not
motivated by only a single business case, e.g., currency conversion).

The `microservice` keyword determines the name of the microservice, which must
have at least one qualifying level to configure the microservice's *namespace*. 
Qualifying levels are separated by dots (`.`) and, except for the last
qualifying level, determine the microservice's namespace. This mechanism in fact
follows the rules for package declaration in Java. Consequently, the
fully-qualified name of the `SearchForFreeSpace` microservice is 
`com.example.pacp.SearchForFreeSpace`. It consists of the namespace
`com.example.pacp` and the microservice's simple name `SearchForFreeSpace`.

### Interface Definition
In LEMMA, the definition of a microservice must cluster at least one interface
in curly brackets. The modeled interfaces of a microservice specifies one of the
service's APIs as a collection of one or more service operations (see below).

LEMMA provides the `interface` keyword to introduce an interface definition and
expects the interface's simple name after the keyword. That is, the example
service model defines an interface called `SearchSpace` for the
`SearchForFreeSpace` microservice.

Similar to microservices, interfaces can receive visibility modifiers and by
default "inherit" the visibility of their microservices. As a result, the
visibility of the `SearchSpace` is `public` as is the visibility of the 
`SearchForFreeSpace` microservice.

### Operation Definition
In LEMMA, a microservice interface must cluster at least one service operation
between curly brackets. An operation definition does not require a special
keyword. Instead, you state the name of the operation, followed by a pair of
round brackets for possible parameters and a semicolon to end the operation
definition. Thus, in the example service model the `SearchSpace` interface
consists of a single operation, `searchFreeSpace`, which has five parameters
(see below).

In addition, the
[Service Modeling Language](../../user-guide/service-modeling-language)
integrates a special syntax for *API operation comments* that allows the
immediate documentation of an operation's purpose and can later be translated,
e.g., into [OpenAPI specifications](https://www.openapis.org). An API operation
comment has to occur prior to an operation definition within a pair of three
consecutive dashes (`---`). Hence, the example `searchFreeSpace` receives the
API operation comment `Search for a free parking space.` to communicate its
intent.

Furthermore, parameters may also receive documentation as part of API operation
comments. For this purpose, LEMMA provides the *built-in annotations* `@param`
and `@required` to communicate the "importance" of a parameter for a service
operation. While `@param` documents parameter that may be empty upon operation
invocation, `@required` signal callers that a parameter must receive a value for
a service operation to sensibly execute. After the annotation, the name of the
parameter and its comment follow. In the example service model, we document the
purposes of both required, incoming parameters (see below) `inLocation` and
`distance`.

### Parameter Definition
A modeled service operation may receive and return an arbitrary number of
parameters. A parameter definition starts with a keyword that identifies the
parameter's *communication type*. The `sync` keyword introduces parameters,
which an operation expects to receive or promises to return in a synchronous
manner. The `async` keyword, on the other hand, defines parameters, which an
operation expects to receive or promises to return in an asynchronous manner.

Next to a communication type, a parameter definition in LEMMA can explicitly 
state the *direction* of a parameter, which can be incoming (`in` modifier),
outgoing (`out` modifier), or bidirectional (`inout` modifier).

A parameter definition is concluded by the parameter's name and its type,
separated by a colon. The type of a parameter may either be primitive type or a
domain concept imported from a domain model (see above). To reference an
imported domain concept for typing purposes, you first have to state the alias
of the import, followed by two colons (`::`) and the fully-qualified name of the
type within the imported domain model. The fully-qualified name of a domain
concept consists, e.g., of the concept's context and simple name, whereby the
different qualifying levels are separated by a dot.

The following table identifies the communication type, direction, and type of
each parameter of the `searchFreeSpace` operation from the example service model
above.

Parameter     | Communication Type   | Direction        | Type |
| :---------- | :------------------: | :--------------: | :---------------- |
`inLocation`  | synchronous (`sync`) | incoming (`in`)  | `Location` domain concept (from context `ParkingSpace` of imported model with alias `domain`) |
`distance`    | synchronous (`sync`) | incoming (`in`)  | primitive type `float` |
`freeSpaces`  | synchronous (`sync`) | outgoing (`out`) | `ParkingSpace` domain concept (from context `ParkingSpace` of imported model with alias `domain`) |
`allocations` | synchronous (`sync`) | outgoing (`out`) | `VehicleCounts` domain concept (from context `ParkingSpace` of imported model with alias `domain`) |
`foundNone`   | synchronous (`sync`) | outgoing (`out`) | primitive type `boolean` |

In addition, the `foundNone` parameter constitutes a `fault` parameter, i.e.,
the `searchFreeSpace` operation will use the parameter as a flag to communicate
potential errors to callers.

From the definitions of the parameters, we can phrase the purpose of the
`searchFreeSpace` operation in natural language as follows:

!!! abstract "Purpose of the `searchFreeSpace` operation in natural language"
    Take a location and a distance, and return all free parking spaces and their
    allocations by vehicles. In case no parking spaces could be found, return an
    error flag.

## Step 4: Enrich the Service Model with Technology Information
So far, we have used LEMMA's
[Domain Data Modeling Language](../../user-guide/domain-data-modeling-language)
and
[Service Modeling Language](../../user-guide/service-modeling-language) to
construct the domain and service model of the `SearchForFreeSpace` microservice.
Recall that LEMMA organizes its modeling languages into different architecture
viewpoints on microservice architectures. That is, the example domain model
reifies the concepts of the domain view on the `SearchForFreeSpace` microservice
and the example service model represents the service view on the microservice.

Next to domain and service characteristics, another crucial aspect of MSA is
technology or, more precisely, the possibility to employ an arbitrary number of
heterogeneous technologies in microservice development. In fact,
[*technology heterogeneity*]({{ msa_tech_heterogeneity_url }}) may be considered
one of the benefits introduced by MSA as it enables to employ the most
sufficient technologies to implement a microservice. On the other hand, it can
make microservices prone to technical debt and increase the learning curve for
new team members.

LEMMA treats technology heterogeneity as a dedicated concern in microservice
development and thus provides the
[Technology Modeling Language](../../user-guide/technology-modeling-language) to
cluster technology information in *technology models* that are flexibly
applicable to modeled microservices.

In the following, we enrich the technology-agnostic example service model from 
above with technology information for Java and the
[Spring framework]({{ spring_url }}). While this binds the `SearchForFreeSpace`
microservice to a certain technology stack, it makes it also possible to later
generate executable microservice code from the model.

To extend the model of the `SearchForFreeSpace` microservice with technology
information, we first require applicable technology models. To this end, create
the files `Java.technology` and `Spring.technology` in the `models` folder of
the `search-for-free-space` Eclipse project so that the Project Explorer of your
Eclipse workspace looks similar to this:
<figure>
  <img src="../figures/tour-step4-technology-models.png" loading="lazy"/>
</figure>

Next, copy the contents of the following two listings to the corresponding
technology model file.

!!! note
    Here, we will not go into further details concerning the construction of
    technology models. Please refer to the user guide of the 
    [Technology Modeling Language](../../user-guide/technology-modeling-language)
    to learn about technology model construction.

=== "Java.technology"

    ```lemmatechnology
    --8<-- "getting-started/example_model_code/models/Java.technology"
    ```

=== "Spring.technology"

    ```lemmatechnology
    --8<-- "getting-started/example_model_code/models/Spring.technology"
    ```

With the technology models at hand, you can now extend the example service model
and its elements with the technology information identified by the
`// EXTENSION` comments:

```lemmaservices
--8<-- "getting-started/example_model_code/doc-models/technology-extensions-micro.services"
```

### Technology Model Imports and Applications
The example service model extensions with the numbers **(1)** and **(2)** import
the constructed technology models into the example service model. The syntax for
importing technology models into service models is almost equal to that for
importing domain models into service models (see above). Specifically, it only
differs for the element type, which is `technology` instead of `datatypes`.

Extensions **(3)** and **(4)** apply the imported technology models to the
`SearchForFreeSpace` microservice using the built-in annotation `@technology`
followed by the import aliases of the models in round brackets. The application
of technology models to microservices by means of the annotation is mandatory to
indicate that a microservice depends on a certain technology and also makes

### Technology Aspects
Extensions **(5)** to **(8)** of the example service model apply *technology*
*aspects* from the imported `Spring` technology model to the
`SearchForFreeSpace` microservice's `searchFreeSpace` operation and some of its
parameters.

In LEMMA, a technology aspect is similar to an annotation in Java or an
attribute in C# in that it enables to attach metadata to modeled elements. The
syntax for aspect application follows this pattern:

!!! example ""
    `[IMPORTED_TECHNOLOGY_MODEL_ALIAS]::_aspects.[ASPECT_NAME]`

That is, the example service model applies two technology aspects from the
`Spring` technology model. More precisely, it applies the `Get` aspect to the
`searchFreeSpace` operation and the `ResponseStatus` aspect to the operation's
`freeSpaces`, `allocations`, and `foundNone` parameters. The `Spring` technology
model defines these aspects to make the semantics of the Java annotations 
[`GetMapping`]({{ spring_get_mapping_annotation_url }}) and
[`ResponseStatus`]({{ spring_response_status_annotation_url }}) available to
LEMMA modelers. As a result, the `searchFreeSpace` operation will be invokable
by consumers using an HTTP `GET` request, whose outcome will be the HTTP status
`OK` (or `200`) when the parameters `freeSpaces` and `allocations` are returned,
and `404` (or `NOT FOUND`) when the `foundNone` error flag (see above) is
returned.

In fact, the technology aspect mechanism is not constrained to technology alone.
Instead, the
[Technology Modeling Language](../../user-guide/technology-modeling-language)
does not constrain the semantic scope of metadata, thereby making technology
aspects a powerful feature that allows semantic enrichment of LEMMA models as
required by a microservice team and its members. For instance, next to
technology-related configuration metadata, technology aspects are used to
integrate patterns such as [CQRS]({{ cqrs_pattern_def_url}}) and
[Saga]({{ saga_pattern_def_url }}) with LEMMA.

[^1]: MSA: The **M**icro**s**ervice **A**rchitecture style.
