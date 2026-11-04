# Registry

The base plus an OCI registry on port 5000, storing images on the runner's disk. It builds for amd64
and arm64 adapters. It's plain HTTP with no sign-in, and allows deleting images, so anyone who can
reach it can change what it holds. Keep it to tests and private networks.

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
   bh cp recipe set registry --tool mkosi \
     --repo https://github.com/notnotwillk/test-images.git --ref main --directory registry
   ```

3. Build it on your adapter. This runs in the background and the first build can take many minutes;
   `builds` shows `ready` when it's done:

   ```sh
   bh cp recipe build registry --adapter "$ADAPTER"
   bh cp recipe builds
   ```

4. Add a runner profile that boots it:

   ```sh
   bh cp profile set registry --image recipe:registry
   ```

   Anything left out takes its default: QEMU, 2 CPUs, 512M of memory, a 16G disk and the nat
   network.

5. Create a runner from the profile. This also runs in the background; `list` shows it as running
   once it has started, and `console` shows it booting:

   ```sh
   bh cp runner create registry --profile registry --adapter "$ADAPTER"
   bh cp runner list
   bh cp runner console registry --adapter "$ADAPTER"
   ```

6. Publish its port 5000 on the mesh. Run this on the adapter's host, or use **Expose…** on the
   Runners page:

   ```sh
   bh host adapter expose registry 5000 --as registry
   ```

   Within about half a minute, runners on any of your adapters can reach
   `http://registry.mesh:5000/v2/`. The adapter and its other nat runners can already reach
   `registry.buzzherd:5000`.

7. On the adapter's host, copy an image into it, then boot a runner from the copy:

   ```sh
   bh host adapter image push recipe:registry registry.buzzherd:5000/test/registry:1
   bh host adapter runner create r2 --image registry.buzzherd:5000/test/registry:1 --network nat --start
   ```

## Remove it

```sh
bh cp runner stop r2 --adapter "$ADAPTER"
bh cp runner delete r2 --adapter "$ADAPTER"
bh cp runner stop registry --adapter "$ADAPTER"
bh cp runner delete registry --adapter "$ADAPTER"
bh cp profile delete registry
bh cp recipe delete registry
```

Deleting the runner also removes its disk and exposure. Deleting the recipe keeps the images
already built.
