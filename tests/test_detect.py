from __future__ import annotations

import pytest

from video_plan_editor.detect import classify_input
from video_plan_editor.models import SourceKind


@pytest.mark.parametrize("text,expected", [
    ("como fazer pão caseiro", SourceKind.topic),
    ("Os 5 erros mais comuns em vendas", SourceKind.topic),
    ("https://youtube.com/watch?v=abc123", SourceKind.video),
    ("https://youtu.be/abc123", SourceKind.video),
    ("https://www.tiktok.com/@x/video/123", SourceKind.video),
    ("https://cdn.exemplo.com/clipe.mp4", SourceKind.video),
    ("https://exemplo.com/post/artigo-sobre-vendas", SourceKind.page),
    ("https://blog.exemplo.com/", SourceKind.page),
])
def test_classify_input(text, expected):
    assert classify_input(text) == expected


def test_whitespace_is_stripped():
    assert classify_input("   https://youtu.be/abc   ") == SourceKind.video
