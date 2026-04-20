import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

from app.config import DATA_DIR

DB_PATH = os.path.join(DATA_DIR, 'profiles.json')


def ensure_storage() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)


def load_db() -> Dict[str, Any]:
    ensure_storage()
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_db(db: Dict[str, Any]) -> None:
    ensure_storage()
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def now_iso() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_profile_key(value: str) -> str:
    return str(value).lower().replace('@', '').strip()


def build_stable_key(normalized: Dict[str, Any], fallback_username: str) -> str:
    sec_uid = normalized.get('sec_uid')
    user_id = normalized.get('user_id')

    if sec_uid:
        return f"secuid:{get_profile_key(sec_uid)}"
    if user_id:
        return f"userid:{get_profile_key(user_id)}"
    return f"username:{get_profile_key(fallback_username)}"


def extract_possible_keys(profile: Dict[str, Any]) -> list[str]:
    keys = []

    last = profile.get('last_normalized', {}) or {}

    possible_values = [
        profile.get('username'),
        last.get('username'),
        last.get('sec_uid'),
        last.get('user_id'),
    ]

    for value in possible_values:
        if value:
            cleaned = get_profile_key(value)
            keys.append(cleaned)
            keys.append(f"username:{cleaned}")
            keys.append(f"secuid:{cleaned}")
            keys.append(f"userid:{cleaned}")

    return list(dict.fromkeys(keys))


def find_existing_profile(db: Dict[str, Any], username: str, normalized: Optional[Dict[str, Any]] = None):
    search_keys = set()

    cleaned_username = get_profile_key(username)
    search_keys.add(cleaned_username)
    search_keys.add(f"username:{cleaned_username}")

    if normalized:
        sec_uid = normalized.get('sec_uid')
        user_id = normalized.get('user_id')
        new_username = normalized.get('username')

        if sec_uid:
            search_keys.add(get_profile_key(sec_uid))
            search_keys.add(f"secuid:{get_profile_key(sec_uid)}")

        if user_id:
            search_keys.add(get_profile_key(user_id))
            search_keys.add(f"userid:{get_profile_key(user_id)}")

        if new_username:
            cleaned_new_username = get_profile_key(new_username)
            search_keys.add(cleaned_new_username)
            search_keys.add(f"username:{cleaned_new_username}")

    for db_key, profile in db.items():
        possible = set(extract_possible_keys(profile))
        possible.add(db_key)
        if search_keys & possible:
            return db_key, profile

    return None, None


def get_profile(username: str) -> Dict[str, Any]:
    db = load_db()
    found_key, profile = find_existing_profile(db, username)
    return profile or {}


def upsert_profile(username: str, payload: Dict[str, Any], normalized: Dict[str, Any]) -> Dict[str, Any]:
    db = load_db()
    found_key, existing = find_existing_profile(db, username, normalized)
    timestamp = now_iso()

    stable_key = build_stable_key(normalized, username)

    if not existing:
        existing = {
            'first_seen_at': timestamp,
            'last_seen_at': timestamp,
            'username': normalized.get('username') or get_profile_key(username),
            'notes': [],
            'snapshots': [],
            'username_changes': [],
            'nickname_changes': [],
            'last_payload': {},
            'last_normalized': {},
        }
    else:
        existing['last_seen_at'] = timestamp

    old_username = (existing.get('last_normalized') or {}).get('username')
    new_username = normalized.get('username')
    if old_username and new_username and old_username != new_username:
        existing['username_changes'].append({
            'changed_at': timestamp,
            'from': old_username,
            'to': new_username,
        })

    old_nickname = (existing.get('last_normalized') or {}).get('nickname')
    new_nickname = normalized.get('nickname')
    if old_nickname and new_nickname and old_nickname != new_nickname:
        existing['nickname_changes'].append({
            'changed_at': timestamp,
            'from': old_nickname,
            'to': new_nickname,
        })

    existing['username'] = new_username or existing.get('username') or get_profile_key(username)
    existing['last_payload'] = payload
    existing['last_normalized'] = normalized
    existing['snapshots'].append({
        'seen_at': timestamp,
        'normalized': normalized,
    })

    if found_key and found_key in db and found_key != stable_key:
        del db[found_key]

    db[stable_key] = existing
    save_db(db)
    return existing


def add_note(username: str, note: str) -> Dict[str, Any]:
    db = load_db()
    found_key, profile = find_existing_profile(db, username)
    timestamp = now_iso()

    if not profile:
        key = f"username:{get_profile_key(username)}"
        profile = {
            'first_seen_at': timestamp,
            'last_seen_at': timestamp,
            'username': get_profile_key(username),
            'notes': [],
            'snapshots': [],
            'username_changes': [],
            'nickname_changes': [],
            'last_payload': {},
            'last_normalized': {},
        }
    else:
        key = found_key or f"username:{get_profile_key(username)}"

    profile['notes'].append({
        'created_at': timestamp,
        'text': note,
    })

    db[key] = profile
    save_db(db)
    return profile