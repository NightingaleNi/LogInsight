def test_guess_level():
    from loginsight.parse import guess_level

    assert guess_level("ERROR boom") == "error"
    assert guess_level("WARN something") == "warn"
    assert guess_level("INFO ok") == "info"
    assert guess_level("misc") == "other"

