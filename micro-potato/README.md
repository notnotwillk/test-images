# Micro potato

The potato server as an [OSv](https://github.com/cloudius-systems/osv) unikernel: a small C server
serving the same page on port 80. It builds and boots on amd64 adapters only.

## Add this image

This assumes a working adapter, and that `bh config get default-control-plane` prints your control
plane.

1. Sign this CLI in, and find your adapter's name, which replaces `ADAPTER` below:

   ```sh
   bh auth login
   bh cp adapter list
   ```

2. Add the image recipe:

   ```sh
   bh cp recipe set micro-potato --tool containerfile \
     --repo https://github.com/notnotwillk/test-images.git --ref main --directory micro-potato
   ```

3. Build it on your adapter. This runs in the background and the first build can take many minutes;
   `builds` shows `ready` when it's done:

   ```sh
   bh cp recipe build micro-potato --adapter ADAPTER
   bh cp recipe builds
   ```

4. Add a runner profile that boots it:

   ```sh
   bh cp profile set micro-potato --image recipe:micro-potato
   ```

   Anything left out takes its default: QEMU, 2 CPUs, 512M of memory, a 16G disk and the nat
   network.

   Add `--vmm firecracker` to boot it under Firecracker, which needs KVM. OSv has no cloud-init, so
   this image takes no user data, and adapters refuse volumes on it.

5. Create a runner from the profile. This also runs in the background; `list` shows it as running
   once it has started, and `console` shows it booting:

   ```sh
   bh cp runner create micro-potato --profile micro-potato --adapter ADAPTER
   bh cp runner list
   bh cp runner console micro-potato --adapter ADAPTER
   ```

6. Publish its port 80 on the mesh. Run this on the adapter's host, or use **Expose…** on the
   Runners page:

   ```sh
   bh host adapter expose micro-potato 80 --as micro-potato
   ```

   Within about half a minute, runners on any of your adapters can open
   `http://micro-potato.mesh/`, and the Buzz Herd app can open `micro-potato.mesh:80`. Runners on
   the same adapter can already open `http://micro-potato.buzzherd/`.

## Remove it

```sh
bh cp runner stop micro-potato --adapter ADAPTER
bh cp runner delete micro-potato --adapter ADAPTER
bh cp profile delete micro-potato
bh cp recipe delete micro-potato
```

Deleting the runner also removes its disk and exposure. Deleting the recipe keeps the images
already built.
