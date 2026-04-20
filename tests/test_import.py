def test_import_alphalens_plus():
    import alphalens_plus as ap
    assert hasattr(ap, '__version__')
    assert hasattr(ap, 'get_clean_factor_and_forward_returns')
    assert hasattr(ap, 'create_full_tear_sheet')
