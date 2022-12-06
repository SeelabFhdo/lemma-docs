# Installation

The implementation of LEMMA's modeling languages is based on
[Eclipse](https://www.eclipse.org) and the majority of LEMMA's components comes
as a set of plugins for the [Eclipse IDE](https://www.eclipse.org/ide). To
facilitate the installation of these plugins, we provide an Eclipse Updatesite
for LEMMA that you can install as described below.

## 1. Ensure a Suitable Package of the Eclipse IDE
LEMMA works with all [Eclipse packages](https://www.eclipse.org/downloads/packages)
greater or equal version **{{ minimum_eclipse_release }}** that provide built-in
Java support.

In case you don't have a suitable Eclipse installation at hand or want to try
LEMMA with a fresh installation, hit the following button to download the
Eclipse IDE for Java Developers:

<div markdown="1" align="center">
[Download the Eclipse IDE for Java Developers](https://www.eclipse.org/downloads/packages/release/{{ current_eclipse_release }}/r/eclipse-ide-java-developers){ .md-button }
</div>

!!! info "Minimum Eclipse Release"
    The above download link for the Eclipse package points to Eclipse release
    **{{ current_eclipse_release }}** which, at the time of writing, is the
    latest release of Eclipse. As already mentioned above, however, you may use
    LEMMA with any Eclipse release greater or equal
    **{{ minimum_eclipse_release }}**.

## 2. Install LEMMA from its Eclipse Updatesite
You can install LEMMA in an existing or fresh Eclipse installation by means of
Eclipse's [Updatesite mechanism](https://help.eclipse.org/{{ current_eclipse_release }}/index.jsp?topic=/org.eclipse.platform.doc.user/tasks/tasks-127.htm). The required link to LEMMA's
Updatesite is as follows:

<div align="center">
<pre id="__code_0"><button class="md-clipboard md-icon" title="Copy to clipboard" data-clipboard-target="#__code_0 > code"></button><code><a href="{{ lemma_updatesite_url }}">{{ lemma_updatesite_url }}</a></code></pre>
</div>

Restart your Eclipse IDE after the installation of LEMMA from this Updatesite.

## 3. Verify Installation
A first indicator for the successful installation of LEMMA is provided by the
new entry "LEMMA" in Eclipse's main menu. Click on the menu entry and select the
sub-menu entry "About LEMMA". The following window should appear to inform about
the currently installed version of LEMMA.

<figure>
  <img src="figures/about.png" loading="lazy"/>
  <figcaption>LEMMA's About dialog.</figcaption>
</figure>

To verify the successful installation of LEMMA even further, you can create a
model in one of [LEMMA's modeling languages](../user-guide/index.md) and check
whether the Eclipse IDE recognizes it correctly:

1. Create a new Java project in Eclipse.
2. Within the project, create a new file called `test.data`. Note that it is
    mandatory to use the extension `.data` as otherwise Eclipse will not be able to
    associate the file with
    [LEMMA's Domain Data Modeling Language](../user-guide/domain-data-modeling-language/index.md).
    In case the "Configure Xtext" dialog appears, just hit "Yes":
    <figure>
        <img src="figures/configure_xtext.png" loading="lazy"/>
        <figcaption>Configure Xtext dialog.</figcaption>
    </figure>
3. Add the following domain model code to the `test.data` file:
```lemmadomaindata
context HelloWorldCtx {
  structure HelloWorldStruct<valueObject> {
        immutable string string_field1,
        immutable string string_field2 = "constant",
        immutable double double_field
    }
}
```

Eclipse should highlight the model code as follows:
<figure>
  <img src="figures/example_model_code.png" loading="lazy"/>
  <figcaption>Example model code highlighted in Eclipse.</figcaption>
</figure>

Congratulations, you have successfully installed LEMMA. Now, you may want to
take the [Tour](tour/index.md) and explore some of LEMMA's core features.

## Troubleshooting
Having trouble with the installation of LEMMA? Please do not hesitate to contact
us via [e-mail](mailto:{{ info_email }}) or
[open issue at LEMMA's GitHub page]({{ lemma_github_url }}/issues).
