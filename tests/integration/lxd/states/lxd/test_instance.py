# -*- coding: utf-8 -*-
import pytest

IMAGE_ALIAS = "alpine/3.10"


@pytest.mark.asyncio
async def test_present(hub, ctx):
    image = await hub.exec.lxd.images.copy_from(ctx, IMAGE_ALIAS)
    assert IMAGE_ALIAS in image

    ret = await hub.states.lxd.containers.present(
        ctx, name="testingvm", image=IMAGE_ALIAS,
    )
    assert ret["name"] == "testingvm"
    assert ret["result"], ret["comment"]
    assert "created" in ret["comment"]
    assert not ret["changes"].get("old")
    assert ret["changes"]["new"]


@pytest.mark.asyncio
async def test_absent(hub, ctx):
    ret = await hub.states.lxd.containers.absent(ctx, name="testingvm",)
    assert ret["name"] == "testingvm"
    assert ret["result"], ret["comment"]
    assert "Deleting" in ret["comment"]
    assert ret["changes"]["old"]
    image = await hub.exec.lxd.images.delete(ctx, IMAGE_ALIAS, wait=True)
    assert "has been deleted" in image["status"]
