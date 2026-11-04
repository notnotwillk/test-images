# nginx

The base plus nginx on port 80, serving a static page. It builds for amd64 and arm64 adapters.

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
   bh cp recipe set nginx --tool mkosi \
     --repo https://github.com/notnotwillk/test-images.git --ref main --directory nginx
   ```

3. Build it on your adapter. This runs in the background and the first build can take many minutes;
   `builds` shows `ready` when it's done:

   ```sh
   bh cp recipe build nginx --adapter ADAPTER
   bh cp recipe builds
   ```

4. Add a runner profile that boots it:

   ```sh
   bh cp profile set nginx --image recipe:nginx
   ```

   Anything left out takes its default: QEMU, 2 CPUs, 512M of memory, a 16G disk and the nat
   network.

5. Create a runner from the profile. This also runs in the background; `list` shows it as running
   once it has started, and `console` shows it booting:

   ```sh
   bh cp runner create nginx --profile nginx --adapter ADAPTER
   bh cp runner list
   bh cp runner console nginx --adapter ADAPTER
   ```

6. Publish its port 80 on the mesh. Run this on the adapter's host, or use **Expose…** on the
   Runners page:

   ```sh
   bh host adapter expose nginx 80 --as nginx
   ```

   Within about half a minute, runners on any of your adapters can open `http://nginx.mesh/`, and
   the Buzz Herd app can open `nginx.mesh:80`. Runners on the same adapter can already open
   `http://nginx.buzzherd/`.

## Remove it

```sh
bh cp runner stop nginx --adapter ADAPTER
bh cp runner delete nginx --adapter ADAPTER
bh cp profile delete nginx
bh cp recipe delete nginx
```

Deleting the runner also removes its disk and exposure. Deleting the recipe keeps the images
already built.
