import pytest


@pytest.mark.asyncio
async def test_create(hub, ctx):
    # currently this is hard coded to use an image named 'centos7'
    # You must have a local image with an alias of 'centos7' for this test to pass
    # TODO: create a fixture to make sure the correct image exists
    container = await hub.exec.lxd.containers.create(ctx, "testlxdcreate", "centos7")
    assert "Creating container: testlxdcreate" in container["status"]


@pytest.mark.asyncio
async def test_delete(hub, ctx):
    container = await hub.exec.lxd.containers.delete(ctx, "testlxdcreate")
    assert "Deleting container: testlxdcreate" in container["status"]
