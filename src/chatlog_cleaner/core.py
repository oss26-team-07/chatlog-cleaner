"""Core functions of chatlog_cleaner.

Input format:
    One message per line, written as ``[time] speaker: content``,
    for example ``[2026-11-09 14:05] 민수: 안녕``. This is the format
    of this project. The export formats of KakaoTalk are not supported
    yet: the PC version writes ``[민수] [오후 2:05] 안녕`` and the mobile
    version writes ``2026년 11월 9일 오후 2:05, 민수 : 안녕``.

Processing order:
    1. ``load_chat``: read the file into lines.
    2. ``parse_messages``: turn the lines into message dicts.
    3. ``normalize_time``: rewrite the ``time`` of every message.
    4. ``sort_messages``: sort by time. This step needs step 3 first,
       because times are compared as strings.
    5. ``remove_system_messages``: drop join and leave notices.
    6. ``mask_pii``: mask the ``text`` of every message.

Not provided yet:
    ``clean_chat(src, dst)``: runs steps 1 to 6 and writes the result
    to a new UTF-8 file in the input format, without changing the
    original file. ``normalize_time`` only raises ``ValueError`` and
    never skips anything itself. Skipping is the job of
    ``clean_chat``: when ``normalize_time`` raises ``ValueError`` for
    one message, ``clean_chat`` skips only that message and shows a
    warning, so that one bad line does not stop the whole file.

Out of scope:
    Masking names, addresses, and other personal data besides phone
    numbers and emails; translation; images and file attachments.
"""

import re

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(
    r"(?<!\d)(?:\+82[-.\s]?0?|0)(?:1[016789]|2|[3-6][1-5]|70)"
    r"[-.\s]?\d{3,4}[-.\s]?\d{4}(?!\d)"
)


def load_chat(path):
    """Read a chat log file and return its lines.

    The file is read as UTF-8 first. A byte order mark (BOM) at the
    start is removed. If the file is not valid UTF-8, it is read again
    as CP949.

    Args:
        path (str): Path to the chat log file. Encoded in UTF-8
            (with or without BOM) or CP949.

    Returns:
        list[str]: One string per line, without trailing newlines.
        Both ``\\n`` and ``\\r\\n`` line endings are handled. An empty
        file gives an empty list. The original file is not modified.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        UnicodeDecodeError: If the file is neither UTF-8 nor CP949.

    Note:
        The example below reads ``examples/chat.txt``. This file must be
        added to the repository together with the implementation, and
        its first line must be ``[2026-11-09 14:05] 민수: 안녕하세요``.

    Examples:
        >>> load_chat("examples/chat.txt")[0]
        '[2026-11-09 14:05] 민수: 안녕하세요'
    """
    raise NotImplementedError


def parse_messages(lines):
    """Split each line into time, speaker, and content.

    Each line is handled by the first rule that matches:

    1. Empty lines and date lines such as ``2026년 11월 9일 일요일`` or
       ``--------------- 2026년 11월 9일 일요일 ---------------`` are
       skipped. The date in a date line is not used. An empty line
       inside a message with several lines is also skipped.
    2. ``[time] speaker: content`` starts a new message. The line is
       split at the first ``": "`` after ``]``, so the content may
       contain ``": "`` but the speaker name may not.
    3. ``[time] content`` with no ``"speaker: "`` is a system message,
       such as ``[2026-11-09 14:06] 지은님이 들어왔습니다.``. It starts a
       new message whose ``speaker`` is ``''``. It must not be joined
       to the previous message, or ``remove_system_messages`` cannot
       remove it.
    4. Any other line is the next line of a message with several
       lines. It is added to the ``text`` of the previous message.
       Such a line before the first message is skipped.

    ``[time]`` means any text in square brackets at the start of the
    line. The text inside is not checked here. So a line of a message
    with several lines that starts with ``[``, such as ``[참고] 내일``,
    is read as a new message by rule 2 or 3.

    The ``time`` is kept as written. ``normalize_time`` converts it.
    Spaces at the start and end of ``speaker`` and ``text`` are removed.

    Args:
        lines (list[str]): Lines from ``load_chat``.

    Returns:
        list[dict]: One dict per message with keys ``time``,
        ``speaker`` and ``text``, in the order of the input. Lines of
        one message are joined with ``\\n``.

    Examples:
        >>> parse_messages(["[2026-11-09 14:05] 민수: 안녕"])
        [{'time': '2026-11-09 14:05', 'speaker': '민수', 'text': '안녕'}]
        >>> parse_messages(["[2026-11-09 14:05] 민수: 안녕", "반가워"])
        [{'time': '2026-11-09 14:05', 'speaker': '민수', 'text': '안녕\\n반가워'}]
        >>> parse_messages(["[2026-11-09 14:06] 지은님이 들어왔습니다."])
        [{'time': '2026-11-09 14:06', 'speaker': '', 'text': '지은님이 들어왔습니다.'}]
    """
    raise NotImplementedError


def normalize_time(raw):
    """Convert a time string into the format ``YYYY-MM-DD HH:MM``.

    Supported formats:

    - ``2026-11-09 14:05``
    - ``2026.11.9 14:05``
    - ``2026.11.9 오후 2:05`` or ``2026.11.9 PM 2:05``
    - ``2026년 11월 9일 오후 2:05`` or ``2026년 11월 9일 14:05``
    - ``11/09/2026 14:05`` (month/day/year)

    ``오전``/``오후`` and ``AM``/``PM`` can be used in every format.
    ``오전``/``오후`` comes before the time. ``AM``/``PM`` may come before
    or after it, as in ``11/09/2026 2:05 PM``. With one of these, the
    hour must be 1 to 12, so ``오후 14:05`` is an error.
    ``오전 12:30`` is ``00:30`` and ``오후 12:30`` is ``12:30``.
    Month, day, and hour may have one or two digits. Minutes must have
    two digits, so ``2:5`` is an error. Spaces at the
    start and end are ignored. Seconds are not supported.

    A time in no supported format is not guessed, because a wrong
    guess gives a wrong order without any warning. A date that does
    not exist, such as ``2026.13.40``, is also an error.

    Args:
        raw (str): A time in one of the supported formats.

    Returns:
        str: The same moment written as ``YYYY-MM-DD HH:MM``.

    Raises:
        ValueError: If ``raw`` matches none of the supported formats,
            or the date or time does not exist.

    Examples:
        >>> normalize_time("2026.11.9 오후 2:05")
        '2026-11-09 14:05'
        >>> normalize_time("2026년 11월 9일 오전 9:30")
        '2026-11-09 09:30'
    """
    raise NotImplementedError


def sort_messages(messages):
    """Sort messages by time, keeping the original order for equal times.

    Args:
        messages (list[dict]): Messages with a ``time`` key. Every
            ``time`` must already be converted by ``normalize_time``.
            Times are compared as strings, so a time in another format
            is put in a wrong place without any error.

    Returns:
        list[dict]: A new sorted list. The input list is not changed.
        The dicts are not copied: the new list holds the same dicts.

    Examples:
        >>> msgs = [{'time': '2026-11-09 14:06', 'text': 'b'},
        ...         {'time': '2026-11-09 14:05', 'text': 'a'}]
        >>> [m['text'] for m in sort_messages(msgs)]
        ['a', 'b']
    """
    return sorted(messages, key=lambda message: message["time"])


def remove_system_messages(messages):
    """Remove system messages such as join and leave notices.

    A message is removed only when both are true:

    - Its ``speaker`` is ``''`` or it has no ``speaker`` key.
      ``parse_messages`` gives ``''`` to lines with no speaker.
    - Its ``text`` contains one of the known system patterns:
      ``님이 들어왔습니다``, ``님이 나갔습니다``, ``님을 초대했습니다``,
      ``님을 내보냈습니다``.

    Because of the first rule, a person who writes one of these
    patterns in a normal message is not removed. A system message with
    a pattern that is not in the list is kept, so users must check the
    result.

    Args:
        messages (list[dict]): Parsed messages with a ``text`` key.

    Returns:
        list[dict]: A new list without the system messages, in the same
        order. The input list is not changed.

    Examples:
        >>> msgs = [{'text': '민수님이 들어왔습니다.'}, {'text': 'hi'}]
        >>> remove_system_messages(msgs)
        [{'text': 'hi'}]
    """
    raise NotImplementedError


def mask_pii(text):
    """Mask phone numbers and email addresses in one message.

    Masked:

    - Emails such as ``kim@example.com``.
    - Korean mobile numbers (010, 011, 016 to 019), Seoul numbers (02),
      area numbers (031 to 035, 041 to 045, 051 to 055, 061 to 065),
      and internet phone numbers (070).
      The parts may be joined by ``-``, ``.``, a space, or nothing,
      as in ``010-1234-5678`` or ``01012345678``. A ``+82`` prefix
      with or without the first ``0`` also works, as in
      ``+82 10-1234-5678``.

    Not masked:

    - Numbers such as ``1588-1234``, foreign numbers such as
      ``+1 212-555-1234``, and resident registration numbers such as
      ``901010-1234567``.
    - Names, addresses, and any other personal data.

    Emails are masked before phone numbers. If phone numbers were
    masked first, an email such as ``01012345678@naver.com`` would
    become ``[PHONE]@naver.com``. Digits that are part of a longer
    number, such as an order number, are not masked.

    Args:
        text (str): Message content. May mix Korean and English.

    Returns:
        str: The text with phone numbers replaced by ``[PHONE]`` and
        emails by ``[EMAIL]``. Everything else is unchanged.

    Examples:
        >>> mask_pii("연락처 010-1234-5678, mail kim@example.com")
        '연락처 [PHONE], mail [EMAIL]'
    """
    text = _EMAIL_RE.sub("[EMAIL]", text)
    text = _PHONE_RE.sub("[PHONE]", text)
    return text
