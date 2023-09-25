# copyright: 2023 ACSONE SA/NV (https://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import hashlib

ORJSON = False
try:
    import orjson as json

    ORJSON = True
except ImportError:
    import json


def compare_json(a: dict, b: dict) -> bool:
    """Compare 2 dictionaries and return False if they are different."""
    if ORJSON:
        a_bytes = json.dumps(a, option=json.OPT_SORT_KEYS)
        b_bytes = json.dumps(b, option=json.OPT_SORT_KEYS)
    else:
        a_bytes = json.dumps(a, sort_keys=True).encode()
        b_bytes = json.dumps(b, sort_keys=True).encode()
    return hashlib.sha256(a_bytes).hexdigest() == hashlib.sha256(b_bytes).hexdigest()
