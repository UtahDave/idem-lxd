# -*- coding: utf-8 -*-
"""
Manage LXD containers
"""
import pylxd
from typing import List


__func_alias__ = {"list_": "list"}


async def list_(
    hub, ctx,
):
    """
    List all running containers

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.list
    """
    ret = []
    try:
        containers = ctx["acct"]["session"].containers.all()
    except pylxd.exceptions.LXDAPIException as e:
        if "not authorized" in str(e):
            return {"error": str(e)}
    for container in containers:
        item = await _get_container_info(container)
        ret.append(item)
    return {"instances": ret}


async def get(hub, ctx, name: str):
    """
    Get a container's information.

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.get container01
    """
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    return {name: container.expanded_config}


async def start(hub, ctx, name: str, wait=False):
    """
    Start a container

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.start container01
    """
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    container.start(wait=wait)
    if wait:
        return {"status": container.status}
    else:
        return {"status": "Starting"}


async def stop(hub, ctx, name: str, wait=False):
    """
    Stop a container

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.stop container01
    """
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    container.stop(wait=wait)
    if wait:
        return {"status": container.status}
    else:
        return {"status": "Stopping"}


async def status(hub, ctx, name: str):
    """
    Get a container's status

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.status container01
    """
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    return {"status": container.status}


async def create(hub, ctx, name: str, image: str, wait=False):
    """
    Create a new container.

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.create container01 centos7
        idem exec lxd.containers.create container01 centos7 wait=True
    """
    if ctx["acct"]["session"].containers.exists(name):
        return {"status": 'Instance: "{}" already exists'.format(name)}
    config = {}
    config["name"] = name
    config["source"] = {}
    config["source"]["type"] = "image"
    config["source"]["alias"] = image

    container = ctx["acct"]["session"].containers.create(config, wait=wait)
    if wait:
        return {"status": container.status}
    else:
        return {"status": "Creating image: {}".format(name)}


async def delete(hub, ctx, name: str, wait=False):
    """
    Delete container.

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.delete container01
        idem exec lxd.containers.delete container01 wait=True
    """
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    container.delete(wait=wait)
    if wait:
        return {"status": container.status}
    else:
        return {"status": "Deleting container: {}".format(name)}


async def _get_container_info(container):
    """
    Collect and format container info
    """
    item = {}
    item[container.name] = {}
    item[container.name]["name"] = container.name
    item[container.name]["architecture"] = container.architecture
    item[container.name]["created_at"] = container.created_at
    item[container.name]["description"] = container.description
    item[container.name]["status"] = container.status
    return item
