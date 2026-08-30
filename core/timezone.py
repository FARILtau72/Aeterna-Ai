"""
AETERNA AI — Timezone & Date Helpers (Asia/Jakarta WIB)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import pandas as pd

JAKARTA_TZ = timezone(timedelta(hours=7))

def get_jakarta_now() -> datetime:
    """Return current timestamp locked to Waktu Indonesia Barat (UTC+7)."""
    return datetime.now(JAKARTA_TZ)

def parse_flexible_date(date_input: Optional[str], default_year: int = 2026) -> Optional[pd.Timestamp]:
    """Parse various date formats into a standard pandas Timestamp."""
    if not date_input:
        return None
    date_input = str(date_input).strip()
    for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m-%d", "%d %B %Y", "%d %b %Y", "%B %d, %Y"]:
        try:
            parsed = datetime.strptime(date_input, fmt)
            if fmt == "%m-%d":
                parsed = parsed.replace(year=default_year)
            return pd.Timestamp(parsed)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: '{date_input}'. Supported format is YYYY-MM-DD.")
