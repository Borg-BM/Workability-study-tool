def summarize_diff(previous: dict | None, current: dict) -> str:
    """One-line human summary of what changed vs. the previous version, for the version tray
    label in StudyBuilder.tsx (e.g. "v3  Slewing 90 → 270").

    Deliberately only checks a curated subset of fields (`checks` below), not every key in
    the params dict -- most fields (position, spreading, wave_dir_step_deg, ...) are either
    rarely touched between re-runs or too noisy to be a useful one-line summary. Add a path
    here if a field turns out to matter enough to call out; this is meant to stay short and
    skimmable, not exhaustive (see the "(+N more)" truncation at the bottom).
    """
    if previous is None:
        return "Initial run"

    checks = [
        ("machine.machine_type", "System"),
        ("machine.luffing_angle_deg", "Luffing"),
        ("machine.slewing_angle_deg", "Slewing"),
        ("machine.orientation_deg", "Orientation"),
        ("machine.lifting_radius_m", "Lifting radius"),
        ("environment.tp_min_s", "Tp min"),
        ("environment.tp_max_s", "Tp max"),
        ("environment.standard_deviations", "n-sigma"),
        ("environment.scatter_source", "Scatter source"),
        ("environment.location_id", "Location"),
    ]

    def _get(d: dict, path: str):
        """Reads a dotted path like "machine.machine_type" out of a nested dict, or None
        if any part of the path is missing (covers an older version's params dict from
        before a field existed)."""
        cur = d
        for part in path.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return None
            cur = cur[part]
        return cur

    changes = []
    for path, label in checks:
        old_val = _get(previous, path)
        new_val = _get(current, path)
        # Skip the (None, None) case explicitly -- otherwise two absent-in-both-versions
        # fields would compare equal anyway (None == None), but this reads clearer as an
        # explicit "nothing to compare" skip.
        if old_val != new_val and (old_val is not None or new_val is not None):
            changes.append(f"{label} {old_val} → {new_val}")

    if not changes:
        return "Re-run (no parameter changes)"
    # Show only the first changed field plus a count -- multiple simultaneous changes are
    # common (e.g. switching scatter_source also changes location_id) and listing every one
    # would overflow the version tray's pill-shaped label.
    return changes[0] if len(changes) == 1 else f"{changes[0]} (+{len(changes) - 1} more)"
