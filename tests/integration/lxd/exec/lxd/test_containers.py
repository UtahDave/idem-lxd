import pytest

IMAGE_ALIAS = "alpine/3.10"


@pytest.mark.asyncio
async def test_create(hub, ctx):
    # currently this is hard coded to download and use the "alpine/3.11" image.
    # TODO: create a fixture to make sure the correct image exists
    image = await hub.exec.lxd.images.copy_from(ctx, IMAGE_ALIAS)
    assert IMAGE_ALIAS in image

    container = await hub.exec.lxd.containers.create(ctx, "testlxdcreate", IMAGE_ALIAS)
    assert "Creating container: testlxdcreate" in container["status"]


@pytest.mark.asyncio
async def test_get(hub, ctx):
    container = await hub.exec.lxd.containers.get(ctx, "testlxdcreate")
    assert "amd64" in container["testlxdcreate"]["image.architecture"]
    assert "Alpine" in container["testlxdcreate"]["image.os"]


@pytest.mark.asyncio
async def test_start(hub, ctx):
    container = await hub.exec.lxd.containers.start(ctx, "testlxdcreate", wait=True)
    status = await hub.exec.lxd.containers.status(ctx, "testlxdcreate")
    assert "Running" in status["status"]


@pytest.mark.asyncio
async def test_stop(hub, ctx):
    container = await hub.exec.lxd.containers.stop(ctx, "testlxdcreate", wait=True)
    status = await hub.exec.lxd.containers.status(ctx, "testlxdcreate")
    assert "Stopped" in status["status"]


@pytest.mark.asyncio
async def test_delete(hub, ctx):
    container = await hub.exec.lxd.containers.delete(ctx, "testlxdcreate")
    assert "Deleting container: testlxdcreate" in container["status"]
    image = await hub.exec.lxd.images.delete(ctx, IMAGE_ALIAS, wait=True)
    assert "has been deleted" in image["status"]
