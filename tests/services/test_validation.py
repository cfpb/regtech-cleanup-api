from regtech_cleanup_api.services.validation import is_valid_cleanup_lei


def test_is_valid_cleanup_lei():
    invalid_cleanup_lei_1 = "123456NOTTEST7890123"
    invalid_cleanup_lei_2 = "12345E2ETEST78901234"
    valid_cleanup_lei = "123456E2ETEST7890123"

    assert not is_valid_cleanup_lei()
    assert not is_valid_cleanup_lei(invalid_cleanup_lei_1)
    assert not is_valid_cleanup_lei(invalid_cleanup_lei_2)
    assert is_valid_cleanup_lei(valid_cleanup_lei)
