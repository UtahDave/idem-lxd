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
    images = ctx["acct"]["session"].images.all()
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

    try:
        image = ctx["acct"]["session"].images.get_by_alias(name)
    except pylxd.exceptions.NotFound:
        return "Image not found"
    return await _get_image_info(image)


async def get(hub, ctx, name):
    """
    Get an image's info by using a fingerprint

    CLI Example:

    .. code-block:: bash

        idem exec lxd.images.get f603184f60a0f9cfe6641b33596edcb27e7852e6795cbd3cc06cfc3fdd647512
    """
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
