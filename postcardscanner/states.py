class PostcardScannerState(object):
    """
    This class simply defines constants used to represent the states of the
    PostcardScanner. Effectively it is a namespace for an enum.
    .. attribute:: disabled
        The scanner is disabled and will not react to inserted cards.
    .. attribute:: enabled
        The scanner is enabled and starts a scan process after detecting a
        postcard.
    .. attribute:: scanning
        The scanner is currently scanning a postcard.
    .. attribute:: error
        The scanner is in an error state which needs to be resolved manually
        by physical interaction. The sensors report invalid values which can
        be caused by a stuck card or an electrical failure.
    """
    disabled = 'disabled'
    enabled = 'enabled'
    scanning = 'scanning'
    error = 'error'
