import dict_tools
import pop.hub
import mock
import pytest
import random
import string
from typing import Any, Dict, List


@pytest.fixture(scope="session", autouse=True)
def acct_subs() -> List[str]:
    return ["lxd"]


@pytest.fixture(scope="session", autouse=True)
def acct_profile() -> str:
    return "test_development_idem_lxd"


@pytest.fixture(scope="session")
def hub(hub):
    hub.pop.sub.add("idem.idem")
    with mock.patch("sys.argv", ["idem", "state"]):
        hub.pop.config.load(["idem", "acct"], "idem", parse_cli=True)
    yield hub


@pytest.mark.asyncio
@pytest.fixture(scope="module")
async def ctx(hub, acct_subs: List[str], acct_profile: str) -> Dict[str, Any]:
    ctx = dict_tools.data.NamespaceDict(run_name="test", test=False)
    # Add the profile to the account
    hub.acct.init.unlock(hub.OPT.acct.acct_file, hub.OPT.acct.acct_key)
    ctx.acct = await hub.acct.init.gather(acct_subs, acct_profile)
    yield ctx


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    hub = pop.hub.Hub()
    hub.pop.loop.create()
    yield hub.pop.Loop
    hub.pop.Loop.close()
