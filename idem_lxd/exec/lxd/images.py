# -*- coding: utf-8 -*-
"""
Manage LXD images
"""
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
