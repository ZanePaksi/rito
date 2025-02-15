from rito import rito


def test_validator_no_version():
    try:
        rito.Validator()
        assert False
    except TypeError:
        assert True


def test_validator_unsupported_version():
    try:
        rito.Validator('fake-version')
        assert False
    except LookupError:
        assert True


def test_r3_create():
    r3 = rito.Validator('r3')
    r3_cls_method = rito.Validator.r3()
    assert r3.fhir_version == 'r3'
    assert r3_cls_method.fhir_version == 'r3'


def test_r4_create():
    r4 = rito.Validator('r4')
    r4_cls_method = rito.Validator.r4()
    assert r4.fhir_version == 'r4'
    assert r4_cls_method.fhir_version == 'r4'


def test_r4b_create():
    r4 = rito.Validator('r4b')
    r4_cls_method = rito.Validator.r4b()
    assert r4.fhir_version == 'r4b'
    assert r4_cls_method.fhir_version == 'r4b'


def test_r5_create():
    r5 = rito.Validator('r5')
    r5_cls_method = rito.Validator.r5()
    assert r5.fhir_version == 'r5'
    assert r5_cls_method.fhir_version == 'r5'
