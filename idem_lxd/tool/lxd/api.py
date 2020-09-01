# -*- coding: utf-8 -*-
"""
Utilities to interact with the LXD api
"""
import pylxd


async def request(
    hub, ctx, resource: str, resource_func: str, **kwargs,
):
    """
    Make an LXD api request.
    :param resource: The name or type of the resource to fetch (i.e. "containers" or "images"). This will match the pylxd module name
    :param resource_func: The function to call on the resource
    :param kwargs: Other arguments to pass to the resource function
    """
    try:
        mod = getattr(ctx["acct"]["session"], resource)
        return getattr(mod, resource_func)(**kwargs)
    except pylxd.exceptions.LXDAPIException as e:
        if "not authorized" in str(e):
            return {"error": str(e)}
        elif "not found" in str(e):
            return {"error": '{}: Does not exist. "{}"'.format(resource, str(e))}
        else:
            raise
