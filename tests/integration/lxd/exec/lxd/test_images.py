import pytest


@pytest.mark.asyncio
async def test_copy_from(hub, ctx):
    # currently this is hard coded to use the "alpine/3.11" image
    image = await hub.exec.lxd.images.copy_from(ctx, "alpine/3.11")
    assert "alpine/3.11" in image


@pytest.mark.asyncio
async def test_get_by_alias(hub, ctx):
    image = await hub.exec.lxd.images.get_by_alias(ctx, "alpine/3.11")
    assert "alpine/3.11" in image
    # assert image["alpine/3.11"]["public"] is True
    # assert image["alpine/3.11"]["auto_update"] is True


@pytest.mark.asyncio
async def test_delete(hub, ctx):
    image = await hub.exec.lxd.images.delete(ctx, "alpine/3.11")
    assert "Deleting image: alpine/3.11" in image["status"]


@pytest.mark.asyncio
async def test_copy_from_w_args(hub, ctx):
    # currently this is hard coded to use the "alpine/3.11" image
    image = await hub.exec.lxd.images.copy_from(
        ctx, "alpine/3.11", public=True, auto_update=True
    )
    assert "alpine/3.11" in image
    assert image["alpine/3.11"]["public"] is True
    assert image["alpine/3.11"]["auto_update"] is True


@pytest.mark.asyncio
async def test_delete_wait(hub, ctx):
    image = await hub.exec.lxd.images.delete(ctx, "alpine/3.11", wait=True)
    assert "has been deleted" in image["status"]
