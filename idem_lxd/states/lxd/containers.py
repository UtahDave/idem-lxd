# -*- coding: utf-8 -*-
"""
Idem state to manage LXD containers
"""
import pylxd
from typing import List


async def present(hub, ctx, name: str, image: str, **kwargs):
    """
    Ensure a container is present

    .. code-block:: yaml

        new container:
          lxd.containers.present:
            - name: webserver01
            - image: ubuntu1804
    """
    ret = {
        "result": False,
        "name": name,
        "comment": "",
        "changes": {},
    }
    container = await hub.exec.lxd.containers.get(ctx, name)
    if name in container:
        ret["result"] = True
        ret["comment"] = 'Container "{}" already exists'.format(name)
        return ret
    if ctx["test"]:
        ret["result"] = None
        ret["comment"] = 'Container "{}" does not exist and will be created'.format(
            name
        )
        return ret
    changes = await hub.exec.lxd.containers.create(ctx, name, image, wait=True)
    container = await hub.exec.lxd.containers.get(ctx, name)
    ret["result"] = True
    ret["comment"] = 'Container "{}" was created'.format(name)
    ret["changes"] = {"new": changes["status"]}
    return ret


async def absent(hub, ctx, name: str, **kwargs):
    """
    Ensure a container is absent

    .. code-block:: yaml

        my_container:
          lxd.containers.absent:
            - name: dave
    """
    ret = {
        "result": False,
        "name": name,
        "comment": "",
        "changes": {},
    }
    container = await hub.exec.lxd.containers.get(ctx, name)
    if "error" in container:
        if "Does not exist" in container["error"]:
            ret["result"] = True
            ret["comment"] = 'Container "{}" does not exist'.format(name)
            return ret
    if ctx["test"]:
        ret["result"] = None
        ret["comment"] = 'Container "{}" exists and will be deleted'.format(name)
        return ret
    result = await hub.exec.lxd.containers.delete(ctx, name)
    ret["result"] = True
    ret["comment"] = result["status"]
    ret["changes"] = {"old": result["status"]}
    return ret
