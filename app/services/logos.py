# app/services/logos.py
_LOGO_CACHE: dict[str, str] = {}

def club_logo(team: str) -> str:
    """
    Very-lightweight logo resolver.
    • First checks the in-memory cache
    • Falls back to a generic placeholder if we can’t map the team
    """
    if team in _LOGO_CACHE:
        return _LOGO_CACHE[team]

    # naive mapping – extend / replace with your own lookup
    slug = (
        team.lower()
            .replace(" fc", "")
            .replace(" ", "-")
            .replace(".", "")
    )
    url = f"https://raw.githubusercontent.com/willcaul/club-crest-icons/main/128/{slug}.png"

    # keep a fallback in case the URL 404s
    if slug in {"chelsea", "arsenal", "barcelona", "bayern-munich"}:
        _LOGO_CACHE[team] = url
    else:                                # fallback: grey shield
        _LOGO_CACHE[team] = "https://placehold.co/32x32?text=⚽︎"

    return _LOGO_CACHE[team]
