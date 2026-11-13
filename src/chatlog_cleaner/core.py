"""Core functions of chatlog_cleaner."""


def load_chat(path):
    """Read a UTF-8 chat log file and return its lines.

    Args:
        path (str): Path to the chat log file. Must be UTF-8 encoded.

    Returns:
        list[str]: One string per line, without trailing newlines.
        The original file is not modified.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        UnicodeDecodeError: If the file is not valid UTF-8.

    Examples:
        >>> load_chat("examples/chat.txt")[0]
        '[2026-11-09 14:05] 민수: 안녕하세요'
    """
    raise NotImplementedError


def parse_messages(lines):
    """Split each line into time, speaker, and content.

    Args:
        lines (list[str]): Lines in the form ``[time] speaker: content``.

    Returns:
        list[dict]: One dict per message with keys ``time``,
        ``speaker`` and ``text``. Lines that do not match are skipped.

    Examples:
        >>> parse_messages(["[2026-11-09 14:05] 민수: 안녕"])
        [{'time': '2026-11-09 14:05', 'speaker': '민수', 'text': '안녕'}]
    """
    raise NotImplementedError


def normalize_time(raw):
    """Convert a time string into the format ``YYYY-MM-DD HH:MM``.

    Args:
        raw (str): A time such as ``2026.11.9 오후 2:05`` or
            ``11/09/2026 14:05``.

    Returns:
        str: The same moment written as ``YYYY-MM-DD HH:MM``.

    Raises:
        ValueError: If ``raw`` matches none of the supported formats.

    Examples:
        >>> normalize_time("2026.11.9 오후 2:05")
        '2026-11-09 14:05'
    """
    raise NotImplementedError


def sort_messages(messages):
    """Sort messages by time, keeping the original order for equal times.

    Args:
        messages (list[dict]): Messages with a normalized ``time`` key.

    Returns:
        list[dict]: A new sorted list. The input list is not changed.

    Examples:
        >>> msgs = [{'time': '2026-11-09 14:06', 'text': 'b'},
        ...         {'time': '2026-11-09 14:05', 'text': 'a'}]
        >>> [m['text'] for m in sort_messages(msgs)]
        ['a', 'b']
    """
    raise NotImplementedError


def remove_system_messages(messages):
    """Remove system messages such as join and leave notices.

    Args:
        messages (list[dict]): Parsed messages with a ``text`` key.

    Returns:
        list[dict]: The messages whose text does not match a known
        system pattern (for example ``님이 들어왔습니다``).

    Examples:
        >>> msgs = [{'text': '민수님이 들어왔습니다.'}, {'text': 'hi'}]
        >>> remove_system_messages(msgs)
        [{'text': 'hi'}]
    """
    raise NotImplementedError


def mask_pii(text):
    """Mask phone numbers and email addresses in one message.

    Args:
        text (str): Message content. May mix Korean and English.

    Returns:
        str: The text with phone numbers replaced by ``[PHONE]`` and
        emails by ``[EMAIL]``. Everything else is unchanged.

    Examples:
        >>> mask_pii("연락처 010-1234-5678, mail kim@example.com")
        '연락처 [PHONE], mail [EMAIL]'
    """
    raise NotImplementedError
