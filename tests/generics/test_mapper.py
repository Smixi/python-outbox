from python_outbox.generic.mapper import IdentityMapper


def test_identity_mapper():
    mapper = IdentityMapper()
    assert mapper.convert("test") == "test"
    assert mapper.convert({"test"}) == {"test"}
