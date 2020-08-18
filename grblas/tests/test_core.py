import pytest
import grblas


def test_import_special_attrs():
    not_hidden = {x for x in dir(grblas) if not x.startswith("_")}
    # Is everything imported?
    assert len(not_hidden & grblas._SPECIAL_ATTRS) == len(grblas._SPECIAL_ATTRS)
    # Is everything special that needs to be?
    not_special = {x for x in dir(grblas) if not x.startswith("_")} - grblas._SPECIAL_ATTRS
    assert not_special == {"backend", "backends", "init", "mask"}
    # Make sure these "not special" objects don't have objects that look special within them
    for attr in not_special:
        assert not set(dir(getattr(grblas, attr))) & grblas._SPECIAL_ATTRS


def test_bad_init():
    # same params is okay
    params = dict(grblas._init_params)
    del params["automatic"]
    grblas.init(**params)
    # different params is bad
    params["blocking"] = not params["blocking"]
    with pytest.raises(grblas.exceptions.GrblasException, match="different init parameters"):
        grblas.init(**params)


def test_bad_libget():
    with pytest.raises(AttributeError, match="GrB_bad_name"):
        grblas.base.libget("GrB_bad_name")


def test_lib_attrs():
    for attr in dir(grblas.lib):
        getattr(grblas.lib, attr)
