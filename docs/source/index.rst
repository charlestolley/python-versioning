Python Component Versioning
===========================
Version numbers are most often used at the package level to communicate the
compatibility of one release of a package with applications that depend on a
previous release of the same package. The purpose of this library is to apply
that same practice *within* a package.

Developers are often taught to program to interfaces, rather than to
implementations. This is excellent advice, but it misses the fact that interface
definitions can change as well. This package gives developers a way to declare,
nearly in-line, the version of the interface that they are programming to. If an
incompatible change is made to the interface, the difference in version number
will trigger an assertion error before the incompatibility has the chance to
cause strange bugs.

Nothing in this package claims to be a silver bullet. It's easy to complain that
this package creates a lot more problems than it solves, by requiring you to
write up detailed interface specifications, and then write tests to validate
them, and then think through the compatibility every time you make a change. The
fact is, to quote Aragorn, that **these problems are upon you, whether you would
use this package or not.** If you change the interfaces in your code without
considering how those interfaces are used, you *will* cause bugs, and the people
who have to debug them are not likely to be the ones responsible for causing
them. To quote Gandalf the Grey, **I AM NOT TRYING TO ROB YOU!!! ... I'm trying
to help you.**

Background
----------
The word "interface" refers to the shared surface(s) of two components in a
system. In a mechanical system, this might be the contact surface of a tire on
the road, or the precise way in which the gears of a clock fit together. In a
software system, an interface might be a function call and it's return type,
or the structure of a network packet and its response. Notice that this
relationship is not symmetrical. One component drives the interaction, and the
other component simply reacts. The proactive component has some understanding
of the reactive component, and the reactive component has an understanding of
how it should react to different types of inputs. This interplay between the two
components enables the system as a whole to work smoothly to serve whatever
purpose it was designed for.

As the designers of software systems, we can capture this mutual understanding
in the form of an "interface specification." This is a document detailing the
precise features of an interface. These features define the attributes, methods,
etc., that one component must provide, as well as the behavior an meaning of
each. They also impose conditions and limitations upon the other component in
its usage of these features. The first component is said to "implement," or
"conform to" the interface, and the other component is said to "use," "invoke,"
or "depend on" the interface. The developers of these components are called
"implementors" and "users," respectively.

The implementor(s) and user(s) of an interface share the responsibility for the
correct operation of the system as a whole. The implementor must ensure that the
component checks every box of each interface specification that it claims to
implement, and the user must ensure that the code that invokes the interface
does not assume anything about the object's behavior other than that which is
explicitly required by the interface specification.

The trouble with interface specifications is that they have to be published in
order to be used, and once a document is published, it really should not be
changed (the term "published" is used somewhat loosely, basically it means that
the specification is made available to multiple people, and understood to be
ready to implement). Instead, from the very start, you should assign a version
number to the publication, so that when you (inevitably) publish an updated
revision, you have a way to tell the two apart. This brings up a new problem:
with multiple revisions of an interface specification, you must consider whether
the components that share this interface are following the same revision, or, if
not, whether the two revisions that they *are* following are *compatible* with
one another.

Compatibility
-------------
Imagine an interface specification, labelled as version "A", and an updated
revision labelled as version "B". Version B is compatible with version A if and
only if an implementation of version A can be replaced by an implementation of
version B without changing the behavior observed by any of its users. A
compatible revision preserves all the features of the previous revision, and
does not impose any additional usage requirements. On the other hand, a revision
that would allow the implementation to violate the requirements of the previous
revision *in any way* is *incompatible* with that revision.

Now, to be clear, there is nothing wrong with incompatible changes *per se*; in
fact, in many cases it is good, and even necessary, to redesign an interface in
this way. The key is that an incompatible interface may as well be a completely
new interface, as far as the user is concerned, and until every bit of code has
been rewritten to use the new interface, the implementor *must* continue to
maintain an implementation of the old one.

Version Numbers
---------------
This package uses a three-part version number to identify each revision of an
interface specification. The version number is a string formatted as "x.y.z",
where x, y, and z are each non-negative integers. These fields are called the
"major," "minor," and "patch" version numbers, respectively, and they each fill
a specific role in expressing the compatiblity of an interface with its previous
revisions.

The first published revision of an interface specification should be called
version "1.0.0". This specification does not have to be complete, or even good,
it simply has to define some set of features for a component to implement, and
make it clear how to use them. Once this baseline has been established, the
developers are free to update the specification in any way they choose, so long
as they follow these rules in selecting the version number for each revision.
If the revision defines an interface that is incompatible with the previous
revision, it must increment its major version number and set the minor and patch
numbers to zero. If the revision defines a compatible interface that requires
new features to be implemented, it should retain the same major version number,
increment the minor version number, and set the patch number to zero. Finally,
if the changes in a revision act only to clarify the previous revision, in a way
that preserves the intended meaning, then the patch number should be incremented
and the major and minor numbers should remain unchanged.

If you are familiar with Semantic Versioning, these rules should sound very
famililar. However, the key distinction between this system and SemVer is that
the latter applies this type of version number to the software release, whereas
this system applies the version number to the interface specification itself.
Notice that this package is released under a four-part version number. The first
three numbers tell you which version of the ``versioning`` interface the package
implements, and the fourth number tells you nothing, but allows the developer(s)
to refactor, fix typos in comments, or make any other change, so long as it does
not affect compatibility.

``versioning`` API version 1.0.0
--------------------------------
A module implementing this interface contains the following components:

.. function:: register(obj: Any, interface: str, version: str) 

    This function registers an interface name and version to the given object,
    indicating that the object implements that version of the interface. The
    name itself has no meaning to this function. The developer(s) should
    document the interface definition separately, and follow the conventions
    described above to determine the appropriate version number each time the
    interface definition changes. It is also the developer's responsibility to
    ensure that the object correctly implements any interface registered to it.

    The version argument is a string, formatted as ``"major.minor.patch"``,
    where each of the three fields is a non-negative integer.

    There is no limit to the number of interfaces that may be registered to a
    single object. It is also legal to register multiple versions of the same
    interface, with different major version numbers, to a single object.

    This function sets and modifies the ``__interfaces__`` attribute of the
    given object. The data type and structure of this attribute are
    implementation-specific.

    This function is not required to have any effect when optimization is
    enabled (i.e. the builtin constant ``__debug__`` is ``False``).

.. function:: require(obj: Any, interface: str, version: str)

    Assert that the given object implements a compatible version of the required
    interface. Unlike :func:`register`, the accepted format for the version
    argument is ``"major.minor"``. If an interface of the same name has been
    registered to the object, with an equal major version number, and an equal
    or greater minor version number, then the function will do nothing. If the
    interface name has not been registered to the object, or it has, but not
    with a compatible version, the function raises a :class:`FailedRequirement`
    exception.

    This function is not required to have any effect when optimization is
    enabled (i.e. the builtin constant ``__debug__`` is ``False``).

.. exception:: FailedRequirement(AssertionError)

Example
-------
This example shows how to properly use the :func:`register` and :func:`require`
functions to verify an object's compliance with the expected interface. Note
that the ``OldFoo`` and ``NewFoo`` classes do not actually implement the ``Foo``
interface, but rather the *instances* of these classes.  On the other hand,
since Python classes are callable, we can treat the classes themselves as
factory methods.

This code references the following interfaces:

``Foo`` API version 1.0.0
^^^^^^^^^^^^^^^^^^^^^^^^^
An object implementing this interface defines the following method:

.. method:: bar()
    :noindex:

    Print the string ``"bar"``.

``Foo`` API version 1.1.0
^^^^^^^^^^^^^^^^^^^^^^^^^
An object implementing this interface defines the following methods:

.. method:: bar()
    :noindex:

    Print the string ``"bar"``.

.. method:: baz()
    :noindex:

    Print the string ``"baz"``.

``FooFactory`` API version 1.0.0
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
An object implementing this interface is callable, with no arguments, and, when
called, returns an implementation of the ``Foo`` interface. The version of
``Foo`` that the object implements is implementation-dependent.

Example Code
^^^^^^^^^^^^

.. code-block:: python

    import versioning

    class OldFoo:
        def __init__(self):
            versioning.register(self, "Foo", "1.0.0")

        def bar(self):
            print("bar")

    class NewFoo:
        def __init__(self):
            versioning.register(self, "Foo", "1.1.0")

        def bar(self):
            print("bar")

        def baz(self):
            print("baz")

    versioning.register(OldFoo, "FooFactory", "1.0.0")
    versioning.register(NewFoo, "FooFactory", "1.0.0")

    def call_functions(factory):
        versioning.require(factory, "FooFactory", "1.0.0")
        foo = factory()
        call_bar(foo)
        call_baz(foo)

    def call_bar(foo):
        versioning.require(foo, "Foo", "1.0")
        foo.bar()

    def call_baz(foo):
        versioning.require(foo, "Foo", "1.1")
        foo.baz()

    if __name__ == "__main__":
        for factory in (NewFoo, OldFoo):
            call_functions(factory)

Output
^^^^^^
If you run this code (without optimizations), you should see the output of the
first three method calls, and then a :class:`FailedRequirement` exception when
``call_functions()`` calls ``call_baz()`` with an ``OldFoo`` argument:

.. code-block:: console

    bar
    baz
    bar
    ...
    versioning.requirements.FailedRequirement: (<__main__.OldFoo object at 0x7f03b67a1668>, 'Foo', '1.1')

If you run the same code with optimizations enabled (one way to do this is with
``python -O``, you can see that the :class:`FailedRequirement` exception
prevented a bug. In this case, the bug simply causes an ``AttributeError``, but
in a larger project, the cause of the bug is not guaranteed to be quite so
obvious.

.. code-block:: console

    bar
    baz
    bar
    ...
    AttributeError: 'OldFoo' object has no attribute 'baz'
