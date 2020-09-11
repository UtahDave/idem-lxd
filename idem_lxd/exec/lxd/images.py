# -*- coding: utf-8 -*-
"""
Manage LXD images
"""
import pylxd
from typing import List

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """
    List all images

    CLI Example:

    .. code-block:: bash

        idem exec lxd.images.list
    """
    images = await hub.tool.lxd.api.request(ctx, "images", "all")
    if "error" in images:
        return images
    ret = []
    for image in images:
        item = await _get_image_info(image)
        ret.append(item)
    return ret


async def get_by_alias(hub, ctx, name: str):
    """
    Get an image's info by using an alias

    CLI Example:

    .. code-block:: bash

        idem exec lxd.images.get_by_alias centos7
    """
    image = await hub.tool.lxd.api.request(ctx, "images", "get_by_alias", alias=name)
    if "error" in image:
        return image
    return await _get_image_info(image)


async def get(hub, ctx, name):
    """
    Get an image's info by using a fingerprint

    CLI Example:

    .. code-block:: bash

        idem exec lxd.images.get f603184f60a0f9cfe6641b33596edcb27e7852e6795cbd3cc06cfc3fdd647512
    """
    image = await hub.tool.lxd.api.request(ctx, "images", "get", fingerprint=name)
    if "error" in image:
        return image
    return await _get_image_info(image)


async def _get_image_info(image):
    """
    Return image info
    """
    item = {}
    names = []
    # print(dir(image))
    # return True
    for alias in image.aliases:
        names.append(alias["name"])
    name = image.fingerprint
    if len(names) > 0:
        name = names[0]
    item[name] = {}
    item[name]["fingerprint"] = image.fingerprint
    item[name]["public"] = image.public
    item[name]["auto_update"] = image.auto_update
    item[name]["properties"] = image.properties
    item[name]["size"] = image.size
    item[name]["upload_date"] = image.uploaded_at
    item[name]["aliases"] = names
    return item


async def copy_from(hub, ctx, alias, server=None, public=False, auto_update=False):
    """
    Copy an image from a remote simplestream server

    CLI Example:

    .. code-block:: bash

        idem exec lxd.images.copy_from 'alpine/3.11'
        idem exec lxd.images.copy_from 'alpine/3.11' public=True auto_update=True
    """
    if not server:
        server = "https://images.linuxcontainers.org"
    if await hub.tool.lxd.api.request(
        ctx, "images", "exists", fingerprint=alias, alias=True
    ):
        return {"status": 'Image: "{}" already exists'.format(alias)}
    image = await hub.tool.lxd.api.request(
        ctx,
        "images",
        "create_from_simplestreams",
        server=server,
        alias=alias,
        public=public,
        auto_update=auto_update,
    )
    if "error" in image:
        return image
    for item in image.aliases:
        if alias == item["name"]:
            return await _get_image_info(image)
    image.add_alias(alias, alias)
    return await _get_image_info(image)


async def delete(hub, ctx, alias, wait=False):
    """
    Delete an image using an Alias

    CLI Example:

    .. code-block:: bash

        idem exec lxd.images.delete 'debian/11'
    """
    image = await hub.tool.lxd.api.request(ctx, "images", "get_by_alias", alias=alias)
    if "error" in image:
        return image
    image.delete(wait=wait)
    if wait:
        if not await hub.tool.lxd.api.request(
            ctx, "images", "exists", fingerprint=alias, alias=True
        ):
            return {"status": 'Image: "{}" has been deleted.'.format(alias)}
    return {"status": "Deleting image: {}".format(alias)}
