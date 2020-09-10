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
    containers = await hub.tool.lxd.api.request(ctx, "containers", "all")
    if "error" in containers:
        return containers
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
    container = await hub.tool.lxd.api.request(ctx, "containers", "get", name=name)
    if "error" in container:
        return container
    return {name: container.expanded_config}


async def start(hub, ctx, name: str, wait=False):
    """
    Start a container

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.start container01
    """
    container = await hub.tool.lxd.api.request(ctx, "containers", "get", name=name)
    if "error" in container:
        return container

    if "Running" in container.status:
        return {"status": container.status}

    container.start(wait=wait)
    if wait:
        return {"status": container.status}
    return {"status": "Starting"}


async def stop(hub, ctx, name: str, wait=False):
    """
    Stop a container

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.stop container01
    """
    container = await hub.tool.lxd.api.request(ctx, "containers", "get", name=name)
    if "error" in container:
        return container

    if "Stopped" in container.status:
        return {"status": container.status}

    container.stop(wait=wait)
    if wait:
        return {"status": container.status}
    return {"status": "Stopping"}


async def status(hub, ctx, name: str):
    """
    Get a container's status

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.status container01
    """
    container = await hub.tool.lxd.api.request(ctx, "containers", "get", name=name)
    if "error" in container:
        return container
    return {"status": container.status}


async def create(hub, ctx, name: str, image: str, wait=False):
    """
    Create a new container.

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.create container01 centos7
        idem exec lxd.containers.create container01 centos7 wait=True
    """
    if await hub.tool.lxd.api.request(ctx, "containers", "exists", name=name):
        return {"status": 'Instance: "{}" already exists'.format(name)}
    config = {}
    config["name"] = name
    config["source"] = {}
    config["source"]["type"] = "image"
    config["source"]["alias"] = image

    container = await hub.tool.lxd.api.request(
        ctx, "containers", "create", config=config
    )
    if "error" in container:
        return container
    return {"status": "Creating container: {}".format(name)}


async def delete(hub, ctx, name: str, wait=False, force=False):
    """
    Delete container.

    CLI Example:

    .. code-block:: bash

        idem exec lxd.containers.delete container01
        idem exec lxd.containers.delete container01 wait=True
    """
    container = await hub.tool.lxd.api.request(ctx, "containers", "get", name=name)
    if "error" in container:
        return container
    if force and ("Running" in container.status):
        await stop(hub, ctx, name, wait=True)
    try:
        container.delete(wait=wait)
    except pylxd.exceptions.LXDAPIException as e:
        if "is running" in str(e):
            return {
                "error": "{} is running. Use 'force=True' to force deletion.".format(
                    name
                )
            }
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
