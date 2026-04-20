from datetime import datetime
from typing import Any, Dict, Optional


def first_value(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", []):
            return value
    return None


def format_time(value: Any) -> str:
    if value in (None, ""):
        return "Unbekannt"

    try:
        ts = int(value)
        if ts > 1000000000000:
            ts = ts / 1000
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(value)


def normalize_user_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    user_info = data.get("userInfo") or {}
    user = user_info.get("user") or {}
    stats = user_info.get("stats") or {}
    stats_v2 = user_info.get("statsV2") or {}
    share_meta = data.get("shareMeta") or {}

    username = user.get("uniqueId")
    nickname = user.get("nickname")
    user_id = user.get("id")
    sec_uid = user.get("secUid")

    follower_count = first_value(
        stats.get("followerCount"),
        stats_v2.get("followerCount"),
        0,
    )

    following_count = first_value(
        stats.get("followingCount"),
        stats_v2.get("followingCount"),
        0,
    )

    likes_count = first_value(
        stats.get("heartCount"),
        stats.get("heart"),
        stats_v2.get("heartCount"),
        stats_v2.get("heart"),
        0,
    )

    video_count = first_value(
        stats.get("videoCount"),
        stats_v2.get("videoCount"),
        0,
    )

    friend_count = first_value(
        stats.get("friendCount"),
        stats_v2.get("friendCount"),
        0,
    )

    private_account = first_value(
        user.get("privateAccount"),
        user.get("secret"),
        False,
    )

    avatar = first_value(
        user.get("avatarLarger"),
        user.get("avatarMedium"),
        user.get("avatarThumb"),
        "Unbekannt",
    )

    bio = user.get("signature")
    if not bio:
        bio = "Keine Bio"

    permalink = f"https://www.tiktok.com/@{sec_uid}" if sec_uid else ""

    # Diese API liefert KEIN echtes Account-Erstellungsdatum.
    # Wir versuchen deshalb nichts zu raten.
    create_time = "Unbekannt"

    return {
        "username": username,
        "nickname": nickname,
        "user_id": user_id,
        "sec_uid": sec_uid,
        "bio": bio,
        "private_account": private_account,
        "avatar": avatar,
        "follower_count": follower_count,
        "following_count": following_count,
        "likes_count": likes_count,
        "video_count": video_count,
        "friend_count": friend_count,
        "create_time": create_time,
        "permalink": permalink,
        "share_title": share_meta.get("title"),
        "share_desc": share_meta.get("desc"),
        "nickname_modify_time": format_time(user.get("nickNameModifyTime")),
    }