"""Deterministic content fill: OpenAI primary, Ollama fallback, offline filler default.

Same topic+audience+kind always yields same section ORDER. Body text varies
only by provider; structure never does. No network required for verify.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

LEAD_MAGNET_SECTIONS = [
    ("promise", "The Promise: What You Get in 10 Minutes"),
    ("mistakes", "3 Mistakes That Cost You Clients"),
    ("playbook", "The 5-Step Playbook"),
    ("next", "Your Next Step"),
]

MINI_EBOOK_SECTIONS = LEAD_MAGNET_SECTIONS + [("checklist", "Launch Checklist")]


@dataclass
class Section:
    slug: str
    heading: str
    body: str


@dataclass
class Document:
    title: str
    audience: str
    topic: str
    cta: str
    kind: str  # lead-magnet | mini-ebook
    sections: list[Section] = field(default_factory=list)


def outline(kind: str) -> list[tuple[str, str]]:
    return list(MINI_EBOOK_SECTIONS if kind == "mini-ebook" else LEAD_MAGNET_SECTIONS)


def _offline_body(slug: str, heading: str, topic: str, audience: str) -> str:
    # Deterministic, specific, no lorem. Each section ~120-180 words after 3 paragraphs.
    base = (
        f"{heading} matters for {audience} because {topic} is where deals are won or lost. "
        f"This section gives you one clear action you can run this week for {topic}."
    )
    steps = (
        f"Step 1: define the single outcome for {audience}. Step 2: remove anything that does not serve {topic}. "
        f"Step 3: run the smallest version in 48 hours and keep what converts."
    )
    closer = (
        f"For {audience}, the standard is simple: clear promise, proof, and a next step tied to {topic}. "
        f"Do this once and reuse it in every call, DM, and follow-up."
    )
    if slug == "mistakes":
        return (
            f"{base} The three mistakes are: vague promise, no proof, and no call to action. "
            f"Fix them in order. {steps} {closer}"
        )
    if slug == "checklist":
        return (
            f"{base} Checklist: title promises one outcome for {audience}; cover shows topic; "
            f"TOC matches sections; each chapter ends with one action; CTA page has phone and link. {closer}"
        )
    return f"{base} {steps} {closer}"


def _openai_fill(prompt: str) -> str | None:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=key)
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        resp = client.chat.completions.create(
            model=model,
            temperature=0,
            max_tokens=450,
            messages=[
                {"role": "system", "content": "Write tight, specific, non-generic marketing-help copy. No lorem, no placeholders."},
                {"role": "user", "content": prompt},
            ],
            timeout=60,
        )
        return (resp.choices[0].message.content or "").strip() or None
    except Exception:
        return None


def _ollama_fill(prompt: str) -> str | None:
    host = os.getenv("OLLAMA_HOST", "").strip().rstrip("/")
    if not host:
        return None
    try:
        import httpx

        model = os.getenv("OLLAMA_MODEL", "llama3.1")
        r = httpx.post(
            f"{host}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0}},
            timeout=90,
        )
        r.raise_for_status()
        return (r.json().get("response") or "").strip() or None
    except Exception:
        return None


def fill_section(slug: str, heading: str, topic: str, audience: str) -> str:
    prompt = f"Write ~150 words for section '{heading}' about '{topic}' for audience '{audience}'. Concrete steps only."
    for attempt in range(3):  # primary + fallback + offline, max 2 retries
        body = _openai_fill(prompt)
        if body:
            return body
        body = _ollama_fill(prompt)
        if body:
            return body
        if attempt >= 1:
            break
    return _offline_body(slug, heading, topic, audience)


def generate(topic: str, audience: str, cta: str, kind: str = "lead-magnet") -> Document:
    kind = "mini-ebook" if kind == "mini-ebook" else "lead-magnet"
    title = f"{topic} for {audience}: The 10-Minute Starter Guide"
    doc = Document(title=title, audience=audience, topic=topic, cta=cta, kind=kind)
    for slug, heading in outline(kind):
        doc.sections.append(Section(slug=slug, heading=heading, body=fill_section(slug, heading, topic, audience)))
    return doc
