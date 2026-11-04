# NFS server

The base plus an NFS server: `/srv/nfs` over NFSv4.1 and 4.2, on TCP port 2049 only, as the NFSv4
root, so clients mount `HOST:/`. It builds for amd64 and arm64 adapters. It trusts clients' user IDs
(`sec=sys`) and lets their root write as root, so keep it to tests and private networks.

## Add this image

This assumes a working adapter, and that `bh config get default-control-plane` prints your control
plane.

1. Sign this CLI in, find your adapter's name, and put it in `ADAPTER` for the commands below:

   ```sh
   bh auth login
   bh cp adapter list
   export ADAPTER=NAME
   ```

2. Add the image recipe:

   ```sh
   bh cp recipe set nfs-server --tool mkosi \
     --repo https://github.com/notnotwillk/test-images.git --ref main --directory nfs-server
   ```

3. Build it on your adapter. This runs in the background and the first build can take many minutes;
   `builds` shows `ready` when it's done:

   ```sh
   bh cp recipe build nfs-server --adapter "$ADAPTER"
   bh cp recipe builds
   ```

4. Add a runner profile that boots it:

   ```sh
   bh cp profile set nfs-server --image recipe:nfs-server
   ```

   Anything left out takes its default: QEMU, 2 CPUs, 512M of memory, a 16G disk and the nat
   network.

5. Create a runner from the profile. This also runs in the background; `list` shows it as running
   once it has started, and `console` shows it booting:

   ```sh
   bh cp runner create nfs-server --profile nfs-server --adapter "$ADAPTER"
   bh cp runner list
   bh cp runner console nfs-server --adapter "$ADAPTER"
   ```

6. Mount it from a runner on the same adapter. The image that runner boots needs an NFS client
   (`nfs-common`). This image has one, so it can be the client too; add `nfs-common` to any other
   image's packages:

   ```sh
   bh cp profile set nfs-client --image recipe:nfs-server --volume nfs://nfs-server.buzzherd/:/mnt/nfs
   bh cp runner create nfs-client --profile nfs-client --adapter "$ADAPTER"
   ```

7. To mount it from other adapters, publish port 2049 on the mesh. Run this on the adapter's host,
   or use **Expose…** on the Runners page:

   ```sh
   bh host adapter expose nfs-server 2049 --as nfs-share
   ```

   Within about half a minute, profiles on any of your adapters can use
   `--volume nfs://nfs-share.mesh/:/mnt/nfs`.

## Remove it

```sh
bh cp runner stop nfs-client --adapter "$ADAPTER"
bh cp runner delete nfs-client --adapter "$ADAPTER"
bh cp profile delete nfs-client
bh cp runner stop nfs-server --adapter "$ADAPTER"
bh cp runner delete nfs-server --adapter "$ADAPTER"
bh cp profile delete nfs-server
bh cp recipe delete nfs-server
```

Deleting the runner also removes its disk and exposure. Deleting the recipe keeps the images
already built.
