def ext_print(msg: str):
    """
    Function that prints a message.
    Makes sure to format the message accordingly and flush it, so it can be taken in by the extension.
    :param msg: Message to be printed.
    :return:
    """
    print('[S] ' + msg, flush=True)
