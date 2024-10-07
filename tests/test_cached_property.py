from operator import not_
from types import ModuleType

import pytest


def test_cached_property(propcache_module: ModuleType) -> None:
    class A:
        def __init__(self):
            self._cache = {}

        @propcache_module.cached_property
        def prop(self):
            return 1

    a = A()
    assert a.prop == 1


def test_cached_property_class(propcache_module: ModuleType) -> None:
    class A:
        def __init__(self):
            """Init."""
            # self._cache not set because its never accessed in this test

        @propcache_module.cached_property
        def prop(self):
            """Docstring."""

    assert isinstance(A.prop, propcache_module.cached_property)
    assert A.prop.__doc__ == "Docstring."


def test_cached_property_without_cache(propcache_module: ModuleType) -> None:
    class A:

        __slots__ = ()

        def __init__(self):
            pass

        @propcache_module.cached_property
        def prop(self):
            """Mock property."""

    a = A()

    with pytest.raises(AttributeError):
        a.prop = 123


def test_cached_property_check_without_cache(propcache_module: ModuleType) -> None:
    class A:

        __slots__ = ()

        def __init__(self):
            pass

        @propcache_module.cached_property
        def prop(self):
            """Mock property."""

    a = A()
    with pytest.raises((TypeError, AttributeError)):
        assert a.prop == 1


def test_cached_property_caching(propcache_module: ModuleType) -> None:

    class A:
        def __init__(self):
            self._cache = {}

        @propcache_module.cached_property
        def prop(self):
            """Docstring."""
            return 1

    a = A()
    assert 1 == a.prop


def test_cached_property_class_docstring(propcache_module: ModuleType) -> None:

    class A:
        def __init__(self):
            """Init."""

        @propcache_module.cached_property
        def prop(self):
            """Docstring."""

    assert isinstance(A.prop, propcache_module.cached_property)
    assert "Docstring." == A.prop.__doc__


def test_set_name(propcache_module: ModuleType) -> None:
    """Test that the __set_name__ method is called and checked."""

    class A:

        @propcache_module.cached_property
        def prop(self):
            """Docstring."""

    A.prop.__set_name__(A, "prop")

    match = r"Cannot assign the same cached_property to two "
    with pytest.raises(TypeError, match=match):
        A.prop.__set_name__(A, "something_else")


def test_get_without_set_name(propcache_module: ModuleType) -> None:
    """Test that get without __set_name__ fails."""
    cp = propcache_module.cached_property(not_)

    class A:
        """A class."""

    A.cp = cp  # type: ignore[attr-defined]
    match = r"Cannot use cached_property instance "
    with pytest.raises(TypeError, match=match):
        _ = A().cp  # type: ignore[attr-defined]


def test_class_getitem(propcache_module: ModuleType) -> None:
    """Test __class_getitem__ is implemented."""
    cached_property = propcache_module.cached_property
    assert str(cached_property[int]).endswith("cached_property[int]")
