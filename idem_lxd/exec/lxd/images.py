from typing import List
import pylxd

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    List all images

    status = all will return all containers regardless of running status
    """
    images = ctx["acct"]["session"].images.all()
    ret = []
    for image in images:
        item = await _get_image_info(image)
        ret.append(item)
    return ret


async def get_by_alias(hub, ctx, name: str):
    try:
        image = ctx["acct"]["session"].images.get_by_alias(name)
    except pylxd.exceptions.NotFound:
        return "Image not found"
    return await _get_image_info(image)


async def get(hub, ctx, name):
    try:
        image = ctx["acct"]["session"].images.get(name)
    except pylxd.exceptions.NotFound:
        return "Image not found"
    return await _get_image_info(image)


async def _get_image_info(image):
    """
    Return image info
    """
    item = {}
    item[image.fingerprint] = {}
    item[image.fingerprint]["fingerprint"] = image.fingerprint
    item[image.fingerprint]["public"] = image.public
    item[image.fingerprint]["arch"] = image.architecture
    item[image.fingerprint]["size"] = image.size
    item[image.fingerprint]["upload_date"] = image.uploaded_at
    names = []
    for alias in image.aliases:
        names.append(alias["name"])
    item[image.fingerprint]["aliases"] = names
    return item


async def start(hub, ctx, name: str, wait=False):
    container = ctx["acct"]["session"].containers.get(name)
    container.start(wait=wait)
    if wait:
        return container.status
    else:
        return "Starting"


async def stop(hub, ctx, name: str, wait=False):
    container = ctx["acct"]["session"].containers.get(name)
    container.stop(wait=wait)
    if wait:
        return container.status
    else:
        return "Stopping"


async def status(hub, ctx, name: str):
    container = ctx["acct"]["session"].containers.get(name)
    # print(help(container.start))
    return container.status
