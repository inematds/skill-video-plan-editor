# video_plan_editor/detect.py
from __future__ import annotations

import re
from urllib.parse import urlparse

from .models import SourceKind

VIDEO_EXTENSIONS = (".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v")
VIDEO_DOMAINS = ("youtube.com", "youtu.be", "vimeo.com", "tiktok.com", "instagram.com")

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def classify_input(text: str) -> SourceKind:
    s = text.strip()
    if not _URL_RE.match(s):
        return SourceKind.topic
    parsed = urlparse(s)
    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").lower()
    if path.endswith(VIDEO_EXTENSIONS):
        return SourceKind.video
    if any(host == d or host.endswith("." + d) for d in VIDEO_DOMAINS):
        return SourceKind.video
    return SourceKind.page
