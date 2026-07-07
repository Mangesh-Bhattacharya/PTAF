"""Threat-pattern clustering for PTAF's AI-analysis module.

Groups NormalizedEvent-shaped records (see modules/defensive/log_parser.py)
into clusters so a human analyst can review "one representative per
pattern" instead of every individual event. This is intentionally a thin,
explainable wrapper around scikit-learn -- see config.yaml for tunables.

This module does not make blocking/allow decisions on its own. It surfaces
groupings and, per config.yaml's explainability settings, which features
drove each grouping -- final judgment stays with the analyst.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence


@dataclass
class ClusterResult:
    cluster_id: int
    member_indices: list[int]
    size: int
    representative_index: int
    top_features: dict[str, Any] = field(default_factory=dict)


def _hash_feature(value: Any, buckets: int = 256) -> int:
    """Deterministic, dependency-free feature hashing for categorical
    values (event_type, host, etc.) so this module works even without
    scikit-learn installed, for environments that only want the
    structure without the ML dependency.
    """
    return hash(str(value)) % buckets


def featurize(
    records: Sequence[dict[str, Any]], feature_names: Sequence[str]
) -> list[list[float]]:
    """Turn a list of flat dict records into numeric feature vectors."""
    vectors: list[list[float]] = []
    for record in records:
        vectors.append(
            [float(_hash_feature(record.get(name))) for name in feature_names]
        )
    return vectors


def cluster_events(
    records: Sequence[dict[str, Any]],
    feature_names: Sequence[str],
    n_clusters: int = 8,
    random_state: int = 42,
) -> list[ClusterResult]:
    """Cluster records with scikit-learn KMeans if available.

    Raises ImportError with a clear message if scikit-learn isn't
    installed -- callers can catch this and fall back to
    cluster_events_naive() below.
    """
    try:
        from sklearn.cluster import KMeans
    except ImportError as exc:  # pragma: no cover - exercised in envs without sklearn
        raise ImportError(
            "scikit-learn is required for cluster_events(); install it or "
            "use cluster_events_naive() instead."
        ) from exc

    if not records:
        return []

    vectors = featurize(records, feature_names)
    n_clusters = max(1, min(n_clusters, len(records)))
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    labels = model.fit_predict(vectors)

    return _summarize_clusters(records, feature_names, labels)


def cluster_events_naive(
    records: Sequence[dict[str, Any]],
    feature_names: Sequence[str],
) -> list[ClusterResult]:
    """Dependency-free fallback: group records that share identical
    values across all feature_names. Cruder than KMeans, but requires
    no ML libraries and is fully deterministic/explainable.
    """
    groups: dict[tuple, list[int]] = {}
    for index, record in enumerate(records):
        key = tuple(record.get(name) for name in feature_names)
        groups.setdefault(key, []).append(index)

    results = []
    for cluster_id, (key, indices) in enumerate(groups.items()):
        results.append(
            ClusterResult(
                cluster_id=cluster_id,
                member_indices=indices,
                size=len(indices),
                representative_index=indices[0],
                top_features=dict(zip(feature_names, key)),
            )
        )
    return sorted(results, key=lambda r: r.size, reverse=True)


def _summarize_clusters(
    records: Sequence[dict[str, Any]],
    feature_names: Sequence[str],
    labels: Sequence[int],
) -> list[ClusterResult]:
    by_label: dict[int, list[int]] = {}
    for index, label in enumerate(labels):
        by_label.setdefault(int(label), []).append(index)

    results = []
    for cluster_id, indices in by_label.items():
        representative = indices[0]
        top_features = {
            name: records[representative].get(name) for name in feature_names
        }
        results.append(
            ClusterResult(
                cluster_id=cluster_id,
                member_indices=indices,
                size=len(indices),
                representative_index=representative,
                top_features=top_features,
            )
        )
    return sorted(results, key=lambda r: r.size, reverse=True)
