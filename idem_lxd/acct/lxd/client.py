from typing import Any, Dict
import pylxd

from requests.packages.urllib3 import disable_warnings

disable_warnings()


async def gather(hub) -> Dict[str, Any]:
    """
    Get profile names from encrypted AWS credential files

    Example:
    .. code-block:: yaml
        lxd.client:
          profile_name:
            endpoint: https://example.com:8443
            password: XXXXXXXX
            crt: /path/to/cert
            key: /path/to/cert
            verify: False
    """
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get("lxd.client", {}).items():
        # TODO if client isn't trusted, reauth
        sub_profiles[profile] = {
            "password": ctx["password"],
            "session": pylxd.Client(
                endpoint=ctx["endpoint"],
                cert=(ctx["cert"], ctx["key"]),
                verify=ctx["verify"],
            ),
        }

        # If client isn't trusted, try to authenticate.
        if not sub_profiles[profile]["session"].trusted:
            sub_profiles[profile]["session"].authenticate(ctx["password"])

    return sub_profiles
