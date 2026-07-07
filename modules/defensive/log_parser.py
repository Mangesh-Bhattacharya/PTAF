"""SIEM-agnostic log parsing utilities for PTAF's defensive module.

Goal: turn heterogeneous log lines (Windows Event Log exports, Sysmon,
Suricata eve.json, Zeek TSV, plain syslog) into one normalized record
shape that the rest of PTAF (detection validation, AI analysis, reporting)
can consume without caring where the log came from.

This is intentionally dependency-light scaffolding. Real SIEM integrations
(Splunk HEC, Elastic ingest, Sentinel Data Collector API, etc.) should be
added as separate, optional adapters that produce the same NormalizedEvent
shape -- see modules/defensive/README.md.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, Iterator


@dataclass
class NormalizedEvent:
    """A single log event in PTAF's common shape."""

    source: str  # e.g. "sysmon", "suricata", "zeek", "syslog"
    event_type: str  # e.g. "process_creation", "network_connection"
    timestamp: str | None
    host: str | None
    raw: dict[str, Any] = field(default_factory=dict)

    def get(self, field_name: str, default: Any = None) -> Any:
        return self.raw.get(field_name, default)


def parse_json_lines(lines: Iterable[str], source: str) -> Iterator[NormalizedEvent]:
    """Parse newline-delimited JSON logs (e.g. Suricata eve.json).

    Unparseable lines are skipped rather than raising, since real log
    files commonly contain the occasional truncated/corrupt line.
    """
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        yield NormalizedEvent(
            source=source,
            event_type=str(record.get("event_type", "unknown")),
            timestamp=record.get("timestamp"),
            host=record.get("host") or record.get("src_ip"),
            raw=record,
        )


def parse_sysmon_xml_event(event: dict[str, Any]) -> NormalizedEvent:
    """Normalize a single, already-parsed Sysmon event dict.

    Expects the caller to have parsed the underlying EVTX/XML (e.g. via
    python-evtx) into a plain dict -- this function only does the shape
    normalization, to keep this module free of a hard XML-parsing
    dependency.
    """
    event_id = event.get("EventID")
    type_map = {
        1: "process_creation",
        3: "network_connection",
        11: "file_create",
        22: "dns_query",
    }
    return NormalizedEvent(
        source="sysmon",
        event_type=type_map.get(int(event_id), f"sysmon_event_{event_id}")
        if event_id is not None
        else "unknown",
        timestamp=event.get("UtcTime"),
        host=event.get("Computer"),
        raw=event,
    )


def correlate_by_host(events: Iterable[NormalizedEvent]) -> dict[str, list[NormalizedEvent]]:
    """Group normalized events by host -- a minimal building block for
    log correlation. Real correlation logic (time windows, process trees,
    identity linking) should build on top of this, not replace it.
    """
    grouped: dict[str, list[NormalizedEvent]] = {}
    for event in events:
        key = event.host or "unknown-host"
        grouped.setdefault(key, []).append(event)
    return grouped


def to_epoch_seconds(timestamp: str | None) -> float | None:
    """Best-effort ISO-8601 timestamp -> epoch seconds, for time-window
    correlation. Returns None if the timestamp can't be parsed.
    """
    if not timestamp:
        return None
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None
