# Integrating New Modules With LEMMA's Continuous Integration Pipeline

LEMMA provides a sophisticated Continuous Integration (CI) pipeline, whose
configuration is visible from the
[Jenkinsfile in LEMMA's `{{ lemma_main_branch_name }}` branch]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/Jenkinsfile).
This pipeline supports:

  - LEMMA builds under Windows
  - Dockerized LEMMA builds under Linux
  - Deployments of LEMMA artifacts in public Maven repositories (only from
    `{{ lemma_main_branch_name }}` branch)
  - Deployment of LEMMA's Eclipse Updatesite (only from
    `{{ lemma_main_branch_name }}` branch)
  - Deployment of Docker images specific to LEMMA modules (only from
    `{{ lemma_main_branch_name }}` branch)

The various results of successful pipeline executions are obtainable from the
following online resources:

  - LEMMA builds: [{{ lemma_build_job_url }}]({{ lemma_build_job_url }})
  - Deployed artifacts: [{{ lemma_repository_artifacts_url }}]({{ lemma_repository_artifacts_url }})
  - Deployed Eclipse Updatesite: [{{ lemma_updatesite_url }}]({{ lemma_updatesite_url }})
  - Deployed Docker images: [{{ lemma_repository_docker_images_url }}]({{ lemma_repository_docker_images_url }})
  
New modules for the LEMMA ecosystem can participate in the CI pipeline, and thus
provide their own artifacts, Eclipse plugins, and Docker images for publication
via LEMMA's CI pipeline.

This page describes how to teach LEMMA's CI pipeline the consideration of new
modules and their contributions to the ecosystem.

## Module Build

### Relevant Program Versions

LEMMA builds rely on the following versions of programs or have been tested with
them:

  - [Gradle]({{ gradle_url }}): {{ employed_gradle_releases }} (mentioned for
                                completeness as Gradle downloads its required
                                release for a given module when a build is
                                triggered)
  - Eclipse: {{ minimum_eclipse_release }}
  - Java: {{ minimum_java_release }}
  - Linux: {{ minimum_linux_release }}
  - Linux (in dockerized builds): {{ minimum_linux_release_for_docker }}
  - [Maven]({{ maven_url }}): {{ minimum_maven_release }}
  - Windows: {{ minimum_windows_release }}

### Build Scripts

LEMMA's codebase comprises two specialized build scripts for Unix-like operating
systems (including macOS) and Windows. Both scripts are located in the `build`
folder of LEMMA's codebase:

  - [`lemma.sh`]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/build/lemma.sh):
    Build script for Unix-like operating systems.
  - [`lemma.bat`]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/build/lemma.bat):
    Build script for Windows.

These scripts are executed by LEMMA's CI pipeline but it is also possible to
invoke them on local hardware to build and install all necessary LEMMA
dependencies in a local development file system.

By contrast to the `lemma.bat` script, `lemma.sh` runs within a Docker container
during builds with LEMMA's CI pipeline. The corresponding image's Dockerfile and
related files are available from the
[`build/docker` folder in LEMMA's GitHub repository]({{ lemma_github_url }}/tree/{{ lemma_main_branch_name }}/build/docker).

### Integrating New Modules With the Build Scripts

The `lemma.sh` script invokes builds consecutively for the LEMMA modules listed
in the
[`lemma-build-modules.txt` file]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/build/lemma-build-modules.txt)
located in the `build` folder of LEMMA's codebase. Each module name in the file
corresponds to the name of a top-level folder in LEMMA's codebase.

!!! hint
    To participate in LEMMA builds, the folder names of new modules may be added
    to the `lemma-build-modules.txt` file. However, their addition is **only**
    **necessary** if they are not already considered by parent modules. For
    example, the file comprises only the entry
    `de.fhdo.lemma.data.datadsl.parent` for LEMMA's
    [Domain Data Modeling Language](../../user-guide/domain-data-modeling-language/index.md)
    because the
    [`pom.xml` in this folder]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.data.datadsl.parent/pom.xml)
    is the parent Maven [POM]({{ maven_pom_url }}) for all of the language's
    modules. Consequently, a new module for the Domain Data Modeling Language
    does not belong in the `lemma-build-modules.txt` file.

Conversely to `lemma.sh`, the `lemma.bat` script requires direct modification
for new LEMMA modules that are not covered by parent modules. More specifically,
the name of a new module's top-level folder in LEMMA's codebase must be added to
the `modules` array:

```bat
...
REM Analyzer
set modules=%modules%;de.fhdo.lemma.analyzer.lib
set modules=%modules%;de.fhdo.lemma.analyzer

REM New (Group of) Module(s)
set modules=%modules%;{NEW_MODULE_PATH}
...
```

!!! tip
    If you want do debug local LEMMA builds on a selected set of modules, you
    may temporarily adapt the `lemma-build-modules.txt` file (for `lemma.sh`)
    and/or the `modules` array (in `lemma.bat`), and remove modules from the
    local build process you do not care about. However, be aware that module
    removals in should not be become part of 
    [pull requests](../coding-style/index.md#commits) when their only purpose is
    build debugging.

### Customizing Module Builds

Maven is LEMMA's default build system and both [build scripts](#build-scripts)
by default invoke the `mvn clean install` command to perform module builds (and
installations to the local file system). However, this behavior is adaptable by
putting a `build.sh` and/or `build.bat` script into the folder of a module. In
case a `build.sh` file is present, the `lemma.sh` script will invoke it instead
of `mvn clean install` for the module's builds on Unix-like operating systems.
A `build.bat` script will then be employed for Windows builds of the respective
module.

We use this mechanism of build customization, for instance, to perform builds
with other build systems than Maven, e.g., Gradle. The `lemma.sh` and
`lemma.bat` scripts do not pass any information from the build process to
`build.sh` or `build.bat` scripts. However, they check the return codes of
custom builds and immediately abort the build process if a custom build script
finishes with a return code greater `0`.

You can find many examples of customized builds in LEMMA's codebase. Good
(and generic) starters are the custom build scripts of LEMMA's
[static analysis library](../static-analysis-library/index.md), whose code you
can find under the following links and that trigger the Gradle build of the
static analysis library:

  - [`de.fhdo.lemma.analyzer.lib/build.sh`]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.analyzer.lib/build.sh)
  - [`de.fhdo.lemma.analyzer.lib/build.bat`]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.analyzer.lib/build.bat)

## Eclipse Updatesite Build

LEMMA's CI pipeline performs an extra build for LEMMA's Eclipse Updatesite in
case **all** [module builds](#module-build) ran successfully.

### Updatesite Build Script

By contrast to the scripts that control LEMMA module builds, there exists only
one script that is responsible for build artifact deployment, i.e.,
[`lemma-updatesite.sh` in the `build/updatesite` folder of LEMMA's codebase]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/build/updatesite/lemma-updatesite.sh).

Similarly to the `lemma.sh` build script, the execution of `lemma-updatesite.sh`
during CI pipeline runs happens from a Docker container, whose Dockerfile and
related files are available from the
[`build/updatesite/docker` folder in LEMMA's GitHub repository]({{ lemma_github_url }}/tree/{{ lemma_main_branch_name }}/build/updatesite/docker).

### Integrating New Modules With the Updatesite Build Script

The `lemma-updatesite.sh` script invokes builds consecutively for the LEMMA
modules listed in the
[`lemma-build-updatesite-modules.txt` file]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/build/updatesite/lemma-build-updatesite-modules.txt)
located in the `build/updatesite` folder of LEMMA's codebase. Each module name
in the file corresponds to the name of a top-level folder in LEMMA's codebase.

!!! hint
    To participate in Eclipse Updatesite builds, the folder names of new modules
    may be added to the `lemma-build-updatesite-modules.txt` file. However,
    their addition is **only necessary** if they are not already considered by
    parent modules. For example, the file comprises only the entry
    `de.fhdo.lemma.data.datadsl.parent` for LEMMA's
    [Domain Data Modeling Language](../../user-guide/domain-data-modeling-language/index.md)
    because the
    [`pom.xml` in this folder]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.data.datadsl.parent/pom.xml)
    is the parent Maven POM for all of the language's modules. Consequently, a
    new module for the Domain Data Modeling Language does not belong in the
    `lemma-build-updatesite-modules.txt` file.

In addition, it is necessary to add new LEMMA modules to the
[`feature.xml` file]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.eclipse.updatesite.feature/feature.xml)
in LEMMA's `de.fhdo.lemma.eclipse.updatesite.feature` module. Otherwise, the
built Updatesite will not comprise them.

### Customizing Eclipse Updatesite Builds

Internally, the `lemma-updatesite.sh` script invokes the
[`lemma.sh` script for module builds](#build-scripts) on the
`lemma-build-updatesite-modules.txt` file. Consequently, the same
[customization options](#customizing-module-builds) apply to Eclipse Updatesite
builds.

In addition, the `lemma-updatesite.sh` script exports the
`LEMMA_UPDATESITE_BUILD` environment variable with the value `"true"` to make
Eclipse Updatesite builds distinguishable from previous module builds. Using the
variable, Maven POM files may, for instance, behave differently by applying
specialized
[Maven build profiles]({{ maven_build_profiles_url }}), during Eclipse
Updatesite builds. See for example the
[`pom.xml` file of the parent project of LEMMA's Domain Data Modeling Language]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.data.datadsl.parent/pom.xml). It skips tests in its `eclipse-updatesite` profile, which gets
activated when the `LEMMA_UPDATESITE_BUILD` environment variable has the value
`"true"`, to shorten the build time by omitting redundant tests that already
ran during previous module builds.

## Artifact and Eclipse Updatesite Deployment

LEMMA's CI pipeline performs the deployment of build artifacts in case **all**
[module builds](#module-build) and
[Eclipse Updatesite builds](#eclipse-updatesite-build) ran successfully.

!!! hint
    The CI pipeline performs the deployment only for changes in LEMMA's
    `{{ lemma_main_branch_name }}` branch. Concerning the deployment of the
    Eclipse Updatesite to its [server]({{ lemma_updatesite_url }}), it is also
    necessary that the commit, which triggered a CI pipeline run, has a release
    tag of the form `v$MAJOR.$MINOR(.$PATCH)?` with `$MAJOR`, `$MINOR`, and
    `$PATCH` being numerical[^1]. For example, `v0.8` and `v0.8.5` are valid
    release tags.

### Deployment Script

By contrast to the scripts that control LEMMA module builds, there exists only
one script that is responsible for build artifact deployment, i.e.,
[`lemma-deploy.sh` in the `build/deploy` folder of LEMMA's codebase]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/build/deploy/lemma-deploy.sh).
The script is meant to be executed by LEMMA's CI pipeline only. Specifically,
its intended use does not involve deployments from local hardware.

Similarly to the `lemma.sh` build script, the execution of `lemma-deploy.sh`
during CI pipeline runs happens from a Docker container, whose Dockerfile and
related files are available from the
[`build/deploy/docker` folder in LEMMA's GitHub repository]({{ lemma_github_url }}/tree/{{ lemma_main_branch_name }}/build/deploy/docker).

### Integrating New Modules With the Deployment Script

The `lemma-deploy.sh` script invokes builds consecutively for the LEMMA modules
listed in the
[`lemma-deployment-modules.txt` file]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/build/deploy/lemma-deployment-modules.txt)
located in the `build/deploy` folder of LEMMA's codebase. Each module name in
the file corresponds to the name of a top-level folder in LEMMA's codebase.

!!! hint
    To deploy the artifacts of new modules after their successful build from
    LEMMA's CI pipeline, the modules' folder names may be added to the
    `lemma-deployment-modules.txt` file. However, their addition is **only**
    **necessary** if they are not already considered by parent modules. For
    example, the file comprises only the entry
    `de.fhdo.lemma.data.datadsl.parent` for LEMMA's
    [Domain Data Modeling Language](../../user-guide/domain-data-modeling-language/index.md)
    because the
    [`pom.xml` in this folder]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.data.datadsl.parent/pom.xml)
    is the parent Maven POM for all of the language's modules. Consequently, a
    new module for the Domain Data Modeling Language does not belong in the
    `lemma-deployment-modules.txt` file.

### Customizing Module Deployments

As with [module builds](#customizing-module-builds), LEMMA by default relies on
Maven for module deployments. More specifically, the default command invoked by
`lemma-deploy.sh` for this purpose is `mvn deploy`. Again, this behavior is
however customizable, i.e., modules may provide a script called `deploy.sh` in
their top-level folders. The `lemma-deploy.sh` script will then delegate all
deployment steps for the module to the custom `deploy.sh` script.

We use this mechanism of artifact deployment customization, for instance, to
deploy artifacts that were built with other systems than Maven, e.g., Gradle.
The `lemma-deploy.sh` script provides four environment variables that are
accessible by custom deployment scripts:

  - `DEPLOY_MAVEN_USER`: The user to access the
                         [remote artifact repository]({{ lemma_repository_artifacts_url }})
                         for storage of build artifacts.
  - `DEPLOY_MAVEN_PASSWORD`: The password to access the remote artifact
                             repository in combination with the user.
  - `DEPLOY_MAVEN_URL_SNAPSHOTS`: The URL of the remote artifact repository for
                                  snapshot artifacts that are, e.g., not ready
                                  for production.
  - `DEPLOY_MAVEN_URL_RELEASES`: The URL of the remote artifact repository for
                                 release artifacts.

The `lemma-deploy.sh` script checks the return codes of custom deployments and
immediately abort the deployment process (and thus the current CI pipeline run)
if a custom deployment script finishes with a return code greater `0`.

You can find many examples of customized deployments in LEMMA's codebase. A good
starter is the custom deployment script of LEMMA's
[static analysis library](../static-analysis-library/index.md), whose code you
can find under the
[`de.fhdo.lemma.analyzer.lib/deploy.sh` file in LEMMA's codebase]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.analyzer.lib/deploy.sh). The
script uses Gradle to deploy LEMMA's static analysis library as per the
configuration in the [`de.fhdo.lemma.analyzer.lib/deploy.gradle.kts` file]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.analyzer.lib/deploy.gradle.kts).

Furthermore, the `lemma-deploy.sh` scripts exports the environment variable
`LEMMA_DEPLOYMENT` with the value `"true"`. As for
[Eclipse Updatesite builds](#customizing-eclipse-updatesite-builds), the
variable allows an additional means to recognize module deployments. We use this
variable, e.g., to skips tests from previous module builds. See for example the
[`pom.xml` file of the parent project of LEMMA's Domain Data Modeling Language]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.data.datadsl.parent/pom.xml), which activates its `deployment` [build profile]({{ maven_build_profiles_url }})
for this purpose based on the value of the `LEMMA_DEPLOYMENT` environment
variable.

## Build and Deployment of Module-Specific Docker Images

LEMMA's CI pipeline integrates a step to deploy module-specific Docker images,
which may enable to, e.g., provide
[model processors](../model-processing-framework/index.md) as standalone
applications including the required runtime environment.

!!! hint
    The CI pipeline performs the deployment only for changes in LEMMA's
    `{{ lemma_main_branch_name }}` branch.

### Deployment Script

The build and deployment of module-specific Docker images is controlled by the
[`docker-images-push.sh` script in the `build/docker-images-push` folder of LEMMA's codebase]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/build/docker-images-push/docker-images-push.sh). The script is meant to be executed by LEMMA's CI
pipeline only. Specifically, its intended use does not involve deployments from
local hardware.

### Integrating New Modules With the Deployment Script

The `docker-images-push.sh` script operates on the same file of module entries
as the `lemma.sh` script, i.e.,
[`lemma-build-modules.txt`](#integrating-new-modules-with-the-build-scripts). In
case the script encounters a file called `build.sh` in the `docker` folder of a
LEMMA module, it will delegate the build of a Docker image to this script.

The `build.sh` script receives as its first (and only) argument the version of
its module, e.g., `"0.8.5-SNAPSHOT"`, from the `docker-images-push.sh` script.
The version string corresponds to the version configured with the module's build
system. For example, Maven usually determines versions by the `<version>` tag in
a `pom.xml` file, whereas Gradle assigns the version string to the `version`
variable in a `gradle.properties` file.

The `build.sh` script must export an environment variable called
`LEMMA_DOCKER_IMAGE_TAG` with the name of the Docker image that it builds, e.g.,
`"lemma/static_analyzer:latest"`. The content of this variable will then be used
by the `docker-images-push.sh` script to deploy the image, if its build
succeeded, i.e., the `build.sh` script exited with a return code of `0`.

You can find many examples for the provisioning of module-specific Docker images
in LEMMA's codebase. A good starter is the `build.sh` script for the image of
LEMMA's
[static analyzer](../../user-guide/model-processing/static-analysis/index.md),
whose code you
can find under the
[`de.fhdo.lemma.analyzer/docker/build.sh` file in LEMMA's codebase]({{ lemma_github_url }}/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.analyzer/docker/build.sh).

## Checklist

The following checklist provides a quick overview for developers to integrate
their new modules with LEMMA's CI pipeline. It only applies to modules that are
**standalone**, e.g., Maven `parent` projects or executable model processors,
which are not sub-projects of other model processors:

  1. *Optional*: In case the module **uses another build system than Maven**:
    - Customize module build for chosen build system via `build.sh` and
      `build.bat` scripts ([details](#customizing-module-builds)). Depending on
      the operating system, LEMMA's CI pipeline will delegate the module's build
      to these scripts.
    - Customize module deployment for chosen build system via `deploy.sh` script
      ([details](#customizing-module-deployments)). LEMMA's CI pipeline will
      delegate the module's deployment to this script.

  2. Add module folder to `lemma-build-modules.txt` file and the `modules` array
     in the `lemma.bat` script
     ([details](#integrating-new-modules-with-the-build-scripts)). LEMMA's CI
     pipeline will consider the module during the build stage.

  3. Add module folder to the `lemma-deployment-modules.txt` file
     ([details](#integrating-new-modules-with-the-deployment-script)). LEMMA's
     CI pipeline will consider the module during the deployment stage.

  4. *Optional*: In case the module **is an Eclipse plugin**:
    - Add module folder to `lemma-build-updatesite-modules.txt` file as well as
      the `feature.xml` file in LEMMA's
      `de.fhdo.lemma.eclipse.updatesite.feature` module
      ([details](#integrating-new-modules-with-the-updatesite-build-script)).
      LEMMA's CI pipeline will consider the module during the build **and**
      deployment of the Eclipse Updatesite.

  5. *Optional*: Module shall **provide its own Docker image**:
    - Add a `build.sh` script to a folder called `docker` in the module's root
      folder ([details](#integrating-new-modules-with-the-deployment-script_1)).
      LEMMA's CI pipeline will consider the module during the build **and**
      deployment of module-specific Docker images.

[^1]:
    Technically speaking, the Bash-specific regular expression for release tags
    is `^v[0-9]+\.[0-9]+(\.[0-9]+)?`.
