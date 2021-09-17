---
template: main_with_numbered_headings.html
---
# Coding Style

This page describes the preferred coding style for LEMMA. To quote Linus
Torvalds in the 
[Linux Kernel Documentation](https://www.kernel.org/doc/html/latest/process/coding-style.html):

!!!quote
     Coding style is very personal, and I won't **force** my views on anybody, but
     this is what goes for anything that I have to be able to maintain, and I'd
     prefer it for most other things too. Please at least consider the points
     made here.

To rephrase: We greatly welcome all kinds of contributions to LEMMA and its
various modules, and hereby **encourage** all contributors to employ the coding
style outlined as follows, even if it contradicts your personal style of
programming. That is, because we perceive consistency in source code appearance
crucial to ensure a codebase's readability and comprehensibility. Thank you!

## Scope

This style guide concerns all programming languages used in LEMMA modules
besides

  - Python, for which we adhere to [PEP 8]({{ pep8_url }}); and
  - Bash scripts (at least partially and as described below).

## Indentation

Except for [ATL]({{ atl_url }}) modules (files with the ``.atl`` extension), we
use **spaces instead of tabs** to indent LEMMA's source code. An indentation
level is introduced by **{{ coding_style_tab_size }} spaces**. In ATL modules,
we use tabs (instead of spaces) with column width {{ coding_style_tab_size }}
for indentation, which is mainly due to historical reasons.

Except for package/module definitions and import statements, a line of code
should not exceed **{{ coding_style_column_width }} columns**. Moreover, the
maximum count of indentation levels should be **3**. If you require more
indentation levels, please refactor your code by introducing, e.g., additional
data structures or helper methods. For instance, [Xtend]({{ xtend_url }}) code
like

```lemmaxtend
class Example {
    def myMethod(String param1, int param2) {
        if (param1 == "someString")
            if (param2 > 0) {
                ...
            } else if (param2 == 0) {
                ...
            } else {
                ...
            }
    }
}
```

should be refactored into something like

```lemmaxtend
class Example {
    def myMethod(String param1, int param2) {
        if (param1 == "someString")
            handleSomeString(param2)
    }

    private def handleSomeString(int param) {
        if (param > 0) {
            ...
        } else if (param == 0) {
            ...
        } else {
            ...
        }
    }
}
```

`switch` statements are an exception to the rule of the maximum indentation
level 3. For `switch` statements we accept a maximum indentation level of 4.
Thus, it is perfectly fine to refactor the first Xtend listing above into
something like

```lemmaxtend
class Example {
    def myMethod(String param1, int param2) {
        switch(param1) {
            case "someString":
                handleSomeString(param2)
            case "someOtherString":
                ...
            default:
                ...
        }
    }
}
```

Each line of code should contain **exactly one statement**, e.g.,

```lemmaxtend
class Example {
    def myMethod(String param1, int param2) {
        // Wrong
        myOtherMethod() myOtherOtherMethod()

        // Right
        myOtherMethod()
        myOtherOtherMethod()
    }
}
```

## Braces

As in [K&R style]({{ kr_coding_style_url }}), **opening curly braces should be**
**put last on the same line as the statement** to which they belong. Divide the
statement and the opening curly brace by a **single space**. Conversely,
**closing curly braces should be put on their own line**:

```lemmaxtend
class Example {
    // Wrong
    def myFirstMethod()
    {
        ...
    }

    // Right (curly bracing on class/method level also follows K&R style for
    // statements)
    def myMethod(String param1, int param2) {
        // Wrong
        if (param1)
        {
            doSomething1
            doSomething2
        }

        // Also wrong (no space before opening curly brace)
        if (param1){
            doSomething1
            doSomething2
        }

        // Right
        if (param1) {
            doSomething1
            doSomething2
        }
    }
}
```

## Spaces and Newlines

### Spaces

There should be **one space**

  - after keywords like `if`, `case`, `do`, `for`, and `while`;
  - on each side of binary and ternary operators like `=`, `+`, `-`, `<`, `>`,
    `*`, `/`, `%`, `|`, `&`, `^`, `<=`, `>=`, `==`, `!=`, `?:`;
  - after statements that are followed by a block (cf. the [Braces](#2-braces)
    example listing).

There should be **no space**

  - after keywords like `catch` and `switch`;
  - before parameter lists of methods/functions;
  - after unary operators like `!`;
  - before postfix increment and decrement unary operators, i.e., `++` and `--`;
  - after prefix increment and decrement unary operators, i.e., `++` and `--`;
  - around operators that access members of classes/data structures, e.g., `.`
    or `->`.

**Remove spaces that do not comply with the above rules** whenever possible,
e.g.,

  - in empty lines,
  - at the end of a line,
  - at the end of a file.

We **never require horizontal alignment** as the resulting maintainability
effort does not justify the possible (and usually small) gain in readability:

```lemmaxtend
class Example {
    // Wrong
    static val MY_FIRST_CONSTANT              = 1       // Integer
    static val MY_SECOND_CONSTANT_IS_A_STRING = "foo"   // String, of course

    // Right
    static val MY_FIRST_CONSTANT = 1 // Integer
    static val MY_SECOND_CONSTANT_IS_A_STRING = "foo" // String, of course
}
```

### Newlines

Add **one empty line between the definition of semantically or syntactically**
**coherent code blocks** so that they are recognizable as such. For example,
there should be one empty line between a block of constants and the following
block of attributes in a class (semantic cohesion). Similarly, there should be
one empty line between the end of a method body and the start of the next
method's signature (syntactic cohesion).

We **do not place a newline at the end of a file**.

## Optional Syntax Constructs

**Omit optional constructs as permitted by the respective programming language**
as much as possible to decrease the amount of characters one has to read to
understand your code. For example, leave out round braces for functions in
Xtend's standard library and semicolons when they are not necessary:

```lemmaxtend
def myMethod(String param1, int param2) {
    // Wrong (well-known built-in function, omit round braces)
    val myMap1 = newHashMap()
    // Right
    val myMap2 = newHashMap

    // Wrong (well-known built-in function, omit round braces; also omit
    // optional semicolon)
    val myMap3 = newHashMap();
    // Also wrong (omit optional semicolon)
    val myMap4 = newHashMap;
    // Right
    val myMap5 = newHashMap

    // Wrong
    if (param1 == "someString") {
        // Wrong
        doSomething1
    } else {
        doSomething2()
        andSomethingElse()
    }

    // Right (omit braces for first if-branch)
    if (param1 == "someString")
        // Right (custom method, don't omit braces to make clear that this is
        // a custom method)
        doSomething1()
    else {
        doSomething2()
        andSomethingElse()
    }
}
```

An exception to the rule of omitting unnecessary constructs are code blocks that
are empty by intent, e.g., empty `catch`-blocks or constructor bodies. To
communicate the intent of leaving such blocks empty, you should add (i) an
explicit comment describing why the respective code block is empty
(for `catch`-blocks and non-trivial constructors); or (ii) an explicit "NOOP"
line comment (for trivial constructors):

```lemmaxtend
class Example2 extends Example {
    // Right
    private new() {
        // NOOP
    }

    // Also right
    new(String param) {
        // Empty constructor body because we don't care about "param"
        // whatsoever
    }

    private def myMethod(String s) {
        ...

        try {
            return scanner.nextDouble()
        } catch (InputMismatchException ex) {
            // Wrong: No explanation why this exception is not handled
            // NOOP
        } catch (NoSuchElementException ex) {
            // Right
            // We don't handle this exception due to the following sensible
            // reasoning:
            // ...
        }
    }
}
```

## Breaking Long Lines

### Basic Formatting

Lines **wider than {{ coding_style_column_width }} columns should be broken**
**into sensible chunks**, unless exceeding {{ coding_style_column_width }}
columns significantly increases readability and does not hide information.
Descendants should follow LEMMA's coding style w.r.t.
[indentation](#indentation):

```lemmaxtend
class Example {
    def myMethod(String param1, int param2) {
        // Wrong: No indentation of descendant param2
        val myVariableWithAVeryLongName = myFunctionWithAVeryLongName(param1,
        param2)

        // Wrong: Indentation exceeds {{ coding_style_tab_size }} spaces for descendant param2
        val myVariableWithAVeryLongName = myFunctionWithAVeryLongName(param1,
                param2)

        // Right
        val myVariableWithAVeryLongName = myFunctionWithAVeryLongName(param1,
            param2)
    }
}
```

### Functions With Long Parameter Lists

**Functions/methods, whose parameter lists exceed**
**{{ coding_style_column_width }} columns**, and that

  - have more than two parameters; and
  - breaking parameters into descendant lines result in at least one descendant
    line comprising only one parameter, which is not the last one

should be formatted so that **each parameter definition is in its own line**. In
addition, the closing round brace of the parameter list and the opening curly
brace of the function/method body **should go on their own line on the same**
**indentation level** as the start of the function/method definition:

```lemmaxtend
class Example {
    // Right (single parameter is the last one)
    def myMethod2(String param1, int param2, MyClassWithAVeryLongName param3, 
        MyClassWithAnEvenLongerName param4) {
        ...
    }

    // Wrong (param4 stands on its own line and is not the last parameter)
    def myMethod3(String param1, int param2, MyClassWithAVeryLongName param3, 
        MyClassWithAnEvenLongerNameThatMakesParam4StandAloneInBetween param4,
        int param5, boolean param6) {
        ...
    }

    // Right (all parameters on their own line)
    def myMethod3(
        String param1,
        int param2,
        MyClassWithAVeryLongName param3, 
        MyClassWithAnEvenLongerNameThatMakesParam4StandAloneInBetween param4,
        int param5,
        boolean param6
    ) {
        ...
    }

    // Wrong (there are only two parameters and both would fit on their own
    // line)
    def myMethod4(
        MyClassWithAVeryLongName myParamWithAVeryLongName,
        MyClassWithAnEvenLongerName myParamWithAnEvenLongerName
    ) {
        ...
    }

    // Right
    def myMethod4(MyClassWithAVeryLongName myParamWithAVeryLongName,
        MyClassWithAnEvenLongerName myParamWithAnEvenLongerName) {
        ...
    }
}
```

### Binary Operators

When breaking long statements, **binary operators should remain on the**
**previous line**:

```lemmaxtend
class Example {
    def myMethod(String param1, int param2) {
        // Wrong
        println("This statement will print a very long string that "
            + "exceeds the maximum recommended width of a column")

        // Right
        println("This statement will print a very long string that " +
            "exceeds the maximum recommended width of a column")

        // Wrong
        if (param1 != "strThatUnfortunatelyExceedsTheMaximumColumnWidth"
            && param2 > 0)
            ...

        // Right
        if (param1 != "strThatUnfortunatelyExceedsTheMaximumColumnWidth" &&
            param2 > 0)
            ...
    }
}
```

In case there are more than two binary operators in an expression that exceeds
{{ coding_style_column_width }} columns, **each operand should go in its own**
**line**, possibly followed by the binding operator:

```lemmaxtend
class Example {
    def myMethod4(String param1, int param2, boolean param3) {
        // Wrong
        if (param1 != "strThatUnfortunatelyExceedsTheMaximumColumnWidth"
            && param2 > 0 || !param3)
            ...

        // Right
        if (param1 != "strThatUnfortunatelyExceedsTheMaximumColumnWidth" &&
            param2 > 0 ||
            !param3)
            ...
    }
}
```

### Assignments and Member Accesses

For assignments and members accesses, the respective operators **should go**
**into the same line as the assigned value or the accessed member**,
respectively:

```lemmaxtend
class Example {
    def myMethod4(String param1, int param2, boolean param3) {
        // Wrong
        val myVar =
            "strThatUnfortunatelyExceedsTheMaximumColumnWidth"

        // Right
        val myVar
            = "strThatUnfortunatelyExceedsTheMaximumColumnWidth"

        // Wrong
        myObject.
            longMethodNameThatUnfortunatelyExceedsTheMaximumColumnWidth()
            .doSomeMoreStuff()

        // Right
        myObject
            .longMethodNameThatUnfortunatelyExceedsTheMaximumColumnWidth()
            .doSomeMoreStuff()
    }
}
```

## Naming

Except for Python scripts, where we adhere to the style suggested by
[PEP 8]({{ pep8_url }}), and Bash scripts, where we follow the
[Linux Kernel style of Naming](https://www.kernel.org/doc/html/latest/process/coding-style.html#naming),
the following naming rules shall be applied to all LEMMA module implementations.

### Basic Formatting

Names should be kept readable but also as short as possible. Suppose a method
that allows the concatentation of an arbitrary number of strings into a single
file path string. A proper name for this method would be `joinPathSegments`
rather than `join` (too generic), `jps` (incomprehensible), or
`joinPathSegmentsFromAnArbitraryNumberOfStrings` (too long without a reason,
i.e., the `FromAnArbitraryNumberOfStrings` suffix does not add any significant
information to the `joinPathSegments` name prefix).

### Modules/Packages

Names of modules/packages shall follow the `all_lowercase_with_underscore`
style. For example, a valid package name is
`de.fhdo.lemma.model_processing.code_generation.container_base`, and not
`de.fhdo.lemma.model_processing.code_generation.containerBase` or (even worse)
`de.fhdo.lemma.model_processing.code_generation.ContainerBase`.

### Classes
Names of classes shall follow the `UpperCamelCase` style. For the conversion of
English phrases into upper camel-case, we follow the
[conversion scheme defined in Google's Java Style Guide](https://google.github.io/styleguide/javaguide.html#s5.3-camel-case):

  1. Convert the phrase to plain ASCII and remove any apostrophes. For example,
     "Müller's algorithm" becomes "Muellers algorithm".
  2. Divide this result into words, splitting on spaces and any remaining
     punctuation (typically hyphens). If any word already has a conventional
     camel-case appearance in common usage, split this into its constituent
     parts (e.g., "AdWords" becomes "ad words"). Note that a word such as "iOS"
     is not really in camel-case per se.
  3. Now lowercase everything (including acronyms), then uppercase only the
     first character of each word, to yield `UpperCamelCase`.
  4. Finally, join all the words into a single identifier.

Examples:

|Prose form              | Right               | Wrong               |
| :--------------------- | :------------------ | :------------------ |
|"XML HTTP request"      | `XmlHttpRequest`    | `XMLHTTPRequest`    |
|"YouTube importer"      | `YouTubeImporter`   | `YoutubeImporter`   |

### Variables and Functions/Methods

Names of variables and functions/methods shall follow the `lowerCamelCase`
style. For the conversion of English phrases into lower camel-case, we follow the
[conversion scheme defined in Google's Java Style Guide](https://google.github.io/styleguide/javaguide.html#s5.3-camel-case):

  1. Convert the phrase to plain ASCII and remove any apostrophes. For example,
     "Müller's algorithm" becomes "Muellers algorithm".
  2. Divide this result into words, splitting on spaces and any remaining
     punctuation (typically hyphens). If any word already has a conventional
     camel-case appearance in common usage, split this into its constituent
     parts (e.g., "AdWords" becomes "ad words"). Note that a word such as "iOS"
     is not really in camel-case per se.
  3. Now lowercase everything (including acronyms), then uppercase only the
     first character of each word except the first, to yield `lowerCamelCase`.
  4. Finally, join all the words into a single identifier.

Examples:

|Prose form              | Right               | Wrong               |
| :--------------------- | :------------------ | :------------------ |
|"new customer ID"       | `newCustomerId`     | `newCustomerID`     |
|"inner stopwatch"       | `innerStopwatch`    | `innerStopWatch`    |
|"supports IPv6 on iOS?" | `supportsIpv6OnIos` | `supportsIPv6OnIOS` |

As opposed to hungarian notation, we **do not encode the type of a variable**
**in its name**:

```lemmaxtend
class Example {
    // Wrong
    int nAge

    // Worse
    MySecondExampleClass objSecondExample

    // Evil
    MySecondExampleClass mySecondExampleClassInstance

    // Right
    int age

    // Right
    MySecondExampleClass secondExample
}
```
### Constants

Constants are an exception to the `lowerCamelCase` rule for variables. Their
names shall follow the `ALL_UPPERCASE_WITH_UNDERSCORE` style:

```lemmaxtend
class Example {
    // Wrong
    static val myConstant = "foo"

    // Right
    static val MY_CONSTANT = "foo"
}
```

### Avoidance of Offensive Terms

Avoid introducing the terms `master` and `slave` as well as `blacklist` and
`whitelist`. We consider them offensive. Instead, you can use these
alternatives:

  - for `master`/`slave`:
    - `primary`,`main`/`secondary`,`replica`,`subordinate`
    - `initiator`,`requester`/`target`,`responder`
    - `controller`,`host`/`device`,`worker`,`proxy`
    - `leader`/`follower`
    - `director`/`performer`
  - for `blacklist`/`whitelist`:
    - `denylist`/`allowlist`
    - `blocklist`/`passlist`

## Source File Language, Encoding, and Ordering

### Language

The **language for all source file contents is {{ coding_style_language }}**. An
exception to this rule might be localized status messages or texts in user
dialogs. However, **{{ coding_style_language }} is also the first language to**
**consider** for messages or dialog texts.

### Encoding

Source file encoding is `UTF-8`.

### Ordering

The ordering of source file contents should be logical (and, in particular, not
chronological or based on visibility). For instance, variables should be defined
closely to their first usage and the order of methods should reflect their call
chains. Consider the following example of a badly ordered Xtend class:

```lemmaxtend
class Example {
    def myPublicMethod(String param1, int param2) {
        myPrivateMethod(param1, param2)
    }

    def myOtherPublicMethod(boolean param2) {
        myOtherPrivateMethod()
    }

    private def myPrivateMethod(String param1, int param2) {
        val exactlyOneParamIsEmpty = param1.nullOrEmpty && param2 > 0 ||
            !param1.nullOrEmpty && param2 <= 0
        // Lots of statements before first usage of exactlyOneParamIsEmpty
        ...
        if (exactlyOneParamIsEmpty)
            ...
    }

    private def myOtherPrivateMethod() {
        ...
    }
}
```

The contents of this class should instead be ordered as follows:

```lemmaxtend
class Example {
    def myPublicMethod(String param1, int param2) {
        myPrivateMethod(param1, param2)
    }

    // Method definition now follows immediately after the method that
    // invokes it first
    private def myPrivateMethod(String param1, int param2) {
        // Lots of statements before first usage of exactlyOneParamIsEmpty
        ...

        // exactlyOneParamIsEmpty is now defined immediately before its first
        // usage
        val exactlyOneParamIsEmpty = param1.nullOrEmpty && param2 > 0 ||
            !param1.nullOrEmpty && param2 <= 0
        if (exactlyOneParamIsEmpty)
            ...
    }

    def myOtherPublicMethod(boolean param2) {
        myOtherPrivateMethod()
    }

    // Method definition now follows immediately after the method that
    // invokes it first
    private def myOtherPrivateMethod() {
        ...
    }
}
```

Imports are ordered as follows:

  1. All non-static imports in a single block.
  2. All static imports in a single block.

## Comments

### Basics

Try not to over-comment your code and aim to write your code in a way that it is
understandable without comments. In any case, **do not use comments to explain**
**HOW your code works but WHAT it does**:

```lemmaxtend
class Example {
    def myMethod(String param1, int param2) {
        // Wrong
        // Initialize the max looping index
        val maxIndex = list.size()
        // Loop from zero to max looping index
        for (i : 0 ..< maxIndex) {
            // Do something on the list using index i
            ...
        }

        // Better
        /* Loop over the list to... */
        val maxIndex = list.size()
        for (i : 0 ..< maxIndex) {
            ...
        }

        // Even more better (no comments, because it is obvious what happens
        // to the looped list)
        val maxIndex = list.size()
        for (i : 0 ..< maxIndex) {
            ...
        }
    } 
}
```

Proper names in comments, e.g., "Eclipse", "IFile", "LEMMA", and "Spring Boot",
are **capitalized as intended by the inventors/providers** of the mentioned
frameworks/products/technologies/entities.

In addition, **we never (ever) hyphenate within comments**.

### JVM Specifics

Try also to avoid comments in method or function bodies to the maximum extent
possible. However, we **almost always place comments before the signature of a**
**function/method and its defining class**. Exceptions to this rule are
trivial functions/methods like getters or setters, and trivial classes like
POJOs. For functions/methods and classes in JVM languages use the following
comment style:

```lemmaxtend
/**
 * Class that exemplifies LEMMA's style of source code comments. This
 * sentence of the comment even exceeds the first line of the comment for the
 * sake of illustrating LEMMA's comment style.
 */
class Example {
    /**
     * Public method of the example class. It does some very interesting
     * stuff with its two parameters.
     */
    def myMethod(String param1, int param2) {
        ...
    }

    /**
     * In case the comment consists of only one sentence, you may omit the
     * trailing period
     */
    private def myMethod2(
        String param1,
        int param2,
        MyClassWithAVeryLongName param3, 
        MyClassWithAnEvenLongerName param4
    ) {
        ...
    }

    def getAnAttribute() {
        return anAttribute
    }
}
```

In case you developed a JVM function/method that consists of several logical
steps, whose decomposition into other methods does not make sense, you may use
multi-line comments to separate coherent steps and single-line comments within a
compound of coherent steps. However, this form of commenting (and organizing
functions/methods) should be avoided at all sane costs.

### Python Specifics

For Python scripts, we use the comment style suggested by
[PEP 8]({{ pep8_url }}).

### ATL Specifics

For ATL modules, use `---` to comment global variables, rules, or helpers, and
`--` to comment everything else.

## Programming Practices

### Always Use `@Override`

While languages like Kotlin and Xtend require you to use the `override` keyword
when overriding inherited methods, Java does not enforce the usage of the 
`@Override` annotation. However, you should add `@Override` to Java methods
**whenever they override an inherited method**.

### Access Static Members By Their Defining Classes

When accessing static members in a qualified manner, use the defining class's
name and not an instance of the defining class:

```lemmaxtend
Example example = ...

// Wrong
example.myStaticMethod()

// Also wrong
getExampleInstance().myStaticMethod()

// Right
Example.myStaticMethod()
```

### Do Not Reinvent Utility Functions

LEMMA comes with an extensive set of utility functions, e.g., in the
[`LemmaUtils` class](https://github.com/SeelabFhdo/lemma/blob/{{ lemma_main_branch_name }}/de.fhdo.lemma.utils/src/de/fhdo/lemma/utils/LemmaUtils.xtend)
or [Xcore]({{ xcore_url }}) metamodel specifications. Please use such functions
rather than explicitly coding some variant of them yourself.

### Lowest Applicable Visibility

In languages that support a notion of visibility for module members, we always
employ the lowest level of visibility applicable to a member concerning its
intended usage. For Java, for example, apply visibility in the following order
(i.e., make classes package-private whenever possible and make their members
`private` whenever possible):

  1. `private` (class members only)
  2. no modifier, i.e., package-private visibility
  3. `protected` (class members only)
  4. `public`

## Commits

### Commit Cohesion

Your commits should always reflect coherent changes to LEMMA's codebase. For
example, you should not add two different major functionalities in the same
commit. However, a commit **must always** result in a functioning (compileable
and buildable)
[`{{ lemma_main_branch_name }}`](https://github.com/SeelabFhdo/lemma/tree/{{ lemma_main_branch_name }})
branch and not break any tests. In you own feature branches, your commits might
introduce compile and/or build failures, which is totally fine as long as the
commits are isolated from `{{ lemma_main_branch_name }}`. However, before
you open a pull request for `{{ lemma_main_branch_name }}`, you **must ensure**
that your commits will result in a functioning `{{ lemma_main_branch_name }}`
branch.

Merges of commits into `{{ lemma_main_branch_name }}` are expected to be
fast-forward (in fact, they are done using
[git's `--ff-only` option for the `merge` sub-command](https://git-scm.com/docs/git-merge)).
Consequently, you should
[rebase your feature branch onto `{{ lemma_main_branch_name }}`](https://git-scm.com/docs/git-rebase)
before creating a pull request on GitHub.

In case your commit results in generated code (as is the case, e.g., with
Xtend), **only commit generated code that actually results from the changes**
**within source code files relevant to the commit**. For instance, in case
Eclipse performs a workspace re-build and generates Java code from Xtend files
all over the place, your commit should only comprise those generated Java files
that immediately result from changes to Xtend files in the
[LEMMA module](#lemma-module-names) that is actually affected by your commit.

In addition, a commit should be **revertable without breaking existing code**
whenever possible. Sometimes this approach might, however, not be achievable in
a sane manner. We accept such cases then. Still, you should try to create
revertable commits as much as possible.

### Commit Messages

Commit messages in LEMMA consist of **three parts**:

  1. The **name of the LEMMA module** that is affected by the commit in
     {{ coding_style_language }}.
  2. A **colon** that separates the module name from the commit description.
  3. The **commit description** in {{ coding_style_language }}.

#### LEMMA Module Names

Currently, we do not have a standardized collection of LEMMA module names.
However, you might execute the following Bash command on LEMMA's
`{{ lemma_main_branch_name }}` branch in a cloned copy of LEMMA's repository
to get a glimpse of common module names:

```bash
git log --oneline | cut -d" " -f2- | cut -d: -f1 | sort -u
```

This command will result in a list comprising entries like
```
...
Data DSL
DDD Genlet
Documentation
...
Eclipse UI
Examples
...
Intermediate metamodels
Intermediate Service Model
...
Model Processing Framework
...
OCL plugin
Operation DSL
...
Spring Cloud Genlet
Static Analyzer
Static Analyzer Library
...
```

which are all good candidates for module names. Please capitalize nouns in
module names, e.g., "Intermediate Metamodels" is preferred over
"Intermediate metamodels".

In case your commit concerns **more than one LEMMA module**, you might separate
the module names with commas and an "and", e.g.,

```
...
Service DSL and Technology DSL
Service DSL, Mapping DSL, and Operation DSL
...
```

If your commit **does not concern a LEMMA module or all LEMMA modules**, omit
module names entirely, e.g.,

```
Lift version identifiers to release 0.8.5
...
Update .gitignore
Update license
Update README
...
```

#### Colon Separator

In case your commit affects one or more [LEMMA modules](#lemma-module-names), place a
colon immediately after the module names. A space after the colon shall then
separate the colon from the commit description:

```bash
# Wrong (space after module name)
Xtext Editor Plugin : Set module encoding to UTF-8

# Wrong (missing module name)
Set module encoding to UTF-8

# Wrong (missing space after colon)
Xtext Editor Plugin:Set module encoding to UTF-8

# Wrong (space after module name and missing space after colon)
Xtext Editor Plugin :Set module encoding to UTF-8

# Right
Xtext Editor Plugin: Set module encoding to UTF-8
```

#### Commit Description

Commit descriptions shall start with a verb in active form for the first person
(I/we). Moreover, the description shall consist of at least one sentence in
{{ coding_style_language }}. The verb at the beginning of a commit message
starts with an uppercase letter. All other words of the commit message follow
regular capitalization in {{ coding_style_language }}. In particular,
[proper names are capitalized the same way as within comments](#basics):

```bash
# Wrong (verb at description beginning is not in first person; should be
# "Set" instead of "Sets")
Xtext Editor Plugin: Sets module encoding to UTF-8

# Wrong (verb at description beginning is not capitalized)
Xtext Editor Plugin: set module encoding to UTF-8

# Wrong ("eclipse" and "eclipse equinox" are proper names and should be
# capitalized as "Eclipse" and "Eclipse Equinox")
Update eclipse equinox version to 3.14.100

# Wrong (Java is a proper name)
Java Base Generator: Streamline java-based Genlet implementation

# Wrong (uncommon {{ coding_style_language }}: first word of second sentence is
# not capitalized and sentence does not end with a period)
Some LEMMA Module: Add the foo to the bar. fixes baz due to use of ding

# Right
Xtext Editor Plugin: Set module encoding to UTF-8
Update Eclipse Equinox version to 3.14.100
Java Base Generator: Streamline Java-based Genlet implementation

# Right but not preferred
Some LEMMA Module: Add the foo to the bar. Fixes baz due to use of ding.
```

While the latter message is basically correct, we nowadays **prefer "long git**
**commit messages" for commit descriptions that consist of more than one**
**sentence**. The template for a "long git commit message" is as follows:

```
[LEMMA_MODULE_NAMES]: [COMMIT_SUMMARY_WITHOUT_TRAILING_PERIOD]

[LONG_MESSAGE]
```

The `[LONG_MESSAGE]` template variable is a block of text with a **maximum**
**width of {{ coding_style_column_width }} columns, in which each line is
indented by {{ coding_style_tab_size }} spaces**. Consequently, the latter
example commit message above should be reformatted as follows:

```bash
Some LEMMA Module: Add the foo to the bar

    This fixes baz due to use of ding.
```

A real-world example of a "long git commit message" can be found in LEMMA commit
[9237b941](https://github.com/SeelabFhdo/lemma/commit/9237b941562b6dc0950b1fc2b775c5e96dbbc8c7):

```
Live Validation Framework: Refactor towards loosely coupled Java implementation
    
    We split the current implementation of the Live Validation Framework into the
    following modules:
        - util: Shared utilities.
        - model: Shared classes for Live Validation issue representation.
        - protocol: LSP extensions specific to LEMMA Live Validation.
        - client: Framework components for Live Validation client implementation.
        - server: Standalone executable implementation of Live Validation server.
    
    The refactoring of the framework towards a Java implemention facilitates the
    usage of the Live Validation Framework by both the Eclipse editor plugin
    (Xtend-based) and LEMMA's Model Processing Framework (Kotlin-based). In
    particular, we split the server-related from the client-related parts and do
    no longer require the installation of Kotlin-specific artifacts via a dedicated
    Eclipse updatesite.
```

To gain further insights on *short* LEMMA commit descriptions, you may execute
the following Bash command on LEMMA's `{{ lemma_main_branch_name }}` branch in a
cloned copy of LEMMA's repository:

```bash
git log --oneline | cut -d" " -f2- | cut -d: -f2- | \
    sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | sort -u
```
