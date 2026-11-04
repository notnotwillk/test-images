# Potato server

The base plus nginx on port 80, configured only to serve the Potato Operations Center page. It
builds for amd64 and arm64 adapters.

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
   bh cp recipe set potato --tool mkosi \
     --repo https://github.com/notnotwillk/test-images.git --ref main --directory potato
   ```

3. Build it on your adapter. This runs in the background and the first build can take many minutes;
   `builds` shows `ready` when it's done:

   ```sh
   bh cp recipe build potato --adapter "$ADAPTER"
   bh cp recipe builds
   ```

4. Add a runner profile that boots it:

   ```sh
   bh cp profile set potato --image recipe:potato
   ```

   Anything left out takes its default: QEMU, 2 CPUs, 512M of memory, a 16G disk and the nat
   network.

5. Create a runner from the profile. This also runs in the background; `list` shows it as running
   once it has started, and `console` shows it booting:

   ```sh
   bh cp runner create potato --profile potato --adapter "$ADAPTER"
   bh cp runner list
   bh cp runner console potato --adapter "$ADAPTER"
   ```

6. Publish its port 80 on the mesh. Run this on the adapter's host, or use **Expose…** on the
   Runners page:

   ```sh
   bh host adapter expose potato 80 --as potato
   ```

   Within about half a minute, runners on any of your adapters can open `http://potato.mesh/`, and
   the Buzz Herd app can open `potato.mesh:80`. Runners on the same adapter can already open
   `http://potato.buzzherd/`.

## Remove it

```sh
bh cp runner stop potato --adapter "$ADAPTER"
bh cp runner delete potato --adapter "$ADAPTER"
bh cp profile delete potato
bh cp recipe delete potato
```

Deleting the runner also removes its disk and exposure. Deleting the recipe keeps the images
already built.
