# -*- coding: utf-8 -*-
"""
Manage LXD container snapshots
"""
__func_alias__ = {"list_": "list"}


async def list_(hub, ctx, name: str):
    """
    List all snapshots for a container

    CLI Example:

    .. code-block:: bash

        idem exec lxd.snapshots.list container01
    """
    ret = []
    container = ctx["acct"]["session"].containers.get(name)
    snapshots = container.snapshots.all()
    for snap in snapshots:
        item = await _get_snapshot_info(snap)
        ret.append(item)
    return {"snapshots": ret}


async def _get_snapshot_info(snap):
    """
    Collect snapshot info
    """
    item = {}
    item[snap.name] = {}
    item[snap.name]["name"] = snap.name
    item[snap.name]["created_at"] = snap.created_at
    item[snap.name]["stateful"] = snap.stateful
    return item
