import pylxd
from typing import List


__func_alias__ = {"list_": "list"}


async def list_(
    hub, ctx,
):
    """
    List all running containers

    status = all will return all containers regardless of running status
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
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    return {name: container.expanded_config}


async def start(hub, ctx, name: str, wait=False):
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    container.start(wait=wait)
    if wait:
        return {"status": container.status}
    else:
        return {"status": "Starting"}


async def stop(hub, ctx, name: str, wait=False):
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    container.stop(wait=wait)
    if wait:
        return {"status": container.status}
    else:
        return {"status": "Stopping"}


async def status(hub, ctx, name: str):
    if not ctx["acct"]["session"].containers.exists(name):
        return {"error": 'Instance: "{}" does not exist'.format(name)}
    container = ctx["acct"]["session"].containers.get(name)
    return {"status": container.status}


async def create(hub, ctx, name: str, image: str, wait=False):
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
    Collect container info
    """
    item = {}
    item[container.name] = {}
    item[container.name]["name"] = container.name
    item[container.name]["architecture"] = container.architecture
    item[container.name]["created_at"] = container.created_at
    item[container.name]["description"] = container.description
    item[container.name]["status"] = container.status
    return item
