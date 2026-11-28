from chatlog_cleaner import mask_pii, sort_messages


# ---------- mask_pii ----------

# normal: the example from the docstring
def test_mask_pii_docstring_example():
    text = "연락처 010-1234-5678, mail kim@example.com"
    assert mask_pii(text) == "연락처 [PHONE], mail [EMAIL]"


# normal: phone number formats people actually type
def test_mask_pii_phone_formats():
    for phone in ["01012345678", "010.1234.5678", "02-123-4567",
                  "031-123-4567", "+82 10 1234 5678", "+82 010-1234-5678"]:
        assert mask_pii(phone) == "[PHONE]"


# normal: digits inside an email must not become [PHONE]
def test_mask_pii_email_with_digits():
    assert mask_pii("user01012345678@gmail.com") == "[EMAIL]"


# boundary: empty string stays empty
def test_mask_pii_empty_string():
    assert mask_pii("") == ""


# boundary: dates, prices, long numbers are not phone numbers
def test_mask_pii_leaves_other_numbers():
    for text in ["2026-11-09 14:05", "12000원", "20261109123456", "0123456789"]:
        assert mask_pii(text) == text


# ---------- sort_messages ----------

# normal: the example from the docstring
def test_sort_messages_docstring_example():
    msgs = [{"time": "2026-11-09 14:06", "text": "b"},
            {"time": "2026-11-09 14:05", "text": "a"}]
    assert [m["text"] for m in sort_messages(msgs)] == ["a", "b"]


# normal: equal times keep their original order
def test_sort_messages_keeps_order_for_equal_times():
    msgs = [{"time": "2026-11-09 14:05", "text": "first"},
            {"time": "2026-11-09 14:04", "text": "earlier"},
            {"time": "2026-11-09 14:05", "text": "second"}]
    assert [m["text"] for m in sort_messages(msgs)] == ["earlier", "first", "second"]


# normal: the input list is not changed
def test_sort_messages_does_not_change_input():
    msgs = [{"time": "2026-11-09 14:06", "text": "b"},
            {"time": "2026-11-09 14:05", "text": "a"}]
    sort_messages(msgs)
    assert [m["text"] for m in msgs] == ["b", "a"]


# boundary: an empty list
def test_sort_messages_empty_list():
    assert sort_messages([]) == []