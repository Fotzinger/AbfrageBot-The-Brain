from typing import Any, Dict, List


def yes_no(value: Any) -> str:
    if value is True:
        return "Ja✅"
    if value is False:
        return "Nein❌"
    return "Unbekannt"


def safe(value: Any, fallback: str = "Unbekannt") -> str:
    if value is None or value == "":
        return fallback
    return str(value)


def latest_change_time(profile: Dict[str, Any]) -> str:
    username_changes = profile.get("username_changes", [])
    nickname_changes = profile.get("nickname_changes", [])

    all_times = []
    for item in username_changes:
        if item.get("changed_at"):
            all_times.append(item.get("changed_at"))
    for item in nickname_changes:
        if item.get("changed_at"):
            all_times.append(item.get("changed_at"))

    if not all_times:
        return "Keine gespeichert"

    return sorted(all_times)[-1]


def format_seen(profile: Dict[str, Any]) -> str:
    if not profile:
        return "Nein, dieses Profil kenne ich noch nicht."

    notes = profile.get("notes", [])
    snapshots = profile.get("snapshots", [])
    return (
        "Ja, dieses Profil kenne ich schon.\n\n"
        f"Erstmalig gesehen: {safe(profile.get('first_seen_at'))}\n"
        f"Zuletzt gesehen: {safe(profile.get('last_seen_at'))}\n"
        f"Anzahl gespeicherter Checks: {len(snapshots)}\n"
        f"Anzahl Notizen: {len(notes)}"
    )


def format_full_report(profile: Dict[str, Any]) -> str:
    if not profile:
        return "Kein gespeichertes Profil gefunden."

    normalized = profile.get("last_normalized", {})
    username_changes: List[Dict[str, Any]] = profile.get("username_changes", [])
    nickname_changes: List[Dict[str, Any]] = profile.get("nickname_changes", [])
    notes: List[Dict[str, Any]] = profile.get("notes", [])

    lines = []
    lines.append(f"👤 Name: {safe(normalized.get('nickname'))}")
    lines.append(f"🔖 Username: @{safe(normalized.get('username'), 'unbekannt')}")
    lines.append(f"🆔 User ID: {safe(normalized.get('user_id'))}")
    lines.append(f"🔐 Sec UID: {safe(normalized.get('sec_uid'))}")
    lines.append("")
    lines.append("📊 Statistiken:")
    lines.append(f"└ Follower: {safe(normalized.get('follower_count'))}")
    lines.append(f"└ Folgt: {safe(normalized.get('following_count'))}")
    lines.append(f"└ Likes: {safe(normalized.get('likes_count'))}")
    lines.append(f"└ Videos: {safe(normalized.get('video_count'))}")
    lines.append("")
    lines.append(f"👥 Freunde: {safe(normalized.get('friend_count'))}")
    lines.append(f"📅 Account erstellt: {safe(normalized.get('create_time'))}")
    lines.append(f"🖊️ Letzte Namensänderung: {latest_change_time(profile)}")
    lines.append("")
    lines.append(f"🔒 Privater Account: {yes_no(normalized.get('private_account'))}")
    lines.append("")
    lines.append(f"🖼️ Profilbild: {safe(normalized.get('avatar'))}")
    lines.append("")
    lines.append("────────────────────────────────")
    lines.append(f"🌐 Permalink: {safe(normalized.get('permalink'))}")
    lines.append("────────────────────────────────")
    lines.append("")
    lines.append(f"📝 Bio: {safe(normalized.get('bio'))}")
    lines.append("")
    lines.append("────────────────────────────────")
    lines.append(f"👀 Erstmalig gesehen: {safe(profile.get('first_seen_at'))}")
    lines.append(f"🕒 Zuletzt gesehen: {safe(profile.get('last_seen_at'))}")
    lines.append(f"📦 Gespeicherte Checks: {len(profile.get('snapshots', []))}")
    lines.append("────────────────────────────────")
    lines.append("")
    lines.append("📝 Username Änderungen:")
    if username_changes:
        for item in username_changes[-10:]:
            lines.append(
                f"└ {safe(item.get('changed_at'))}: {safe(item.get('from'))} → {safe(item.get('to'))}"
            )
    else:
        lines.append("└ Keine gespeichert")
    lines.append("────────────────────────────────")
    lines.append("")
    lines.append("👤 Nickname Änderungen:")
    if nickname_changes:
        for item in nickname_changes[-10:]:
            lines.append(
                f"└ {safe(item.get('changed_at'))}: {safe(item.get('from'))} → {safe(item.get('to'))}"
            )
    else:
        lines.append("└ Keine gespeichert")
    lines.append("────────────────────────────────")
    lines.append("")
    lines.append("🗒️ Notizen:")
    if notes:
        for item in notes[-10:]:
            lines.append(f"└ {safe(item.get('created_at'))}: {safe(item.get('text'))}")
    else:
        lines.append("└ Keine gespeichert")

    return "\n".join(lines)