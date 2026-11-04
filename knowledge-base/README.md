# Knowledge base

The base plus nginx on port 80, serving a knowledge base about using a Buzz Herd control plane: how
to build images, run runners, mount volumes and reach what they serve. It builds for amd64 and arm64
adapters.

The pages are Markdown in `mkosi.extra/usr/share/knowledge-base/`, which you can also read on GitHub.
`render.py`, beside them, turns them into HTML when the image is built, and fails the build on a dead
link. To add a page, add its file and an entry in `PAGES` in `render.py`.

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
   bh cp recipe set knowledge-base --tool mkosi \
     --repo https://github.com/notnotwillk/test-images.git --ref main --directory knowledge-base
   ```

3. Build it on your adapter. This runs in the background and the first build can take many minutes;
   `builds` shows `ready` when it's done:

   ```sh
   bh cp recipe build knowledge-base --adapter "$ADAPTER"
   bh cp recipe builds
   ```

4. Add a runner profile that boots it:

   ```sh
   bh cp profile set knowledge-base --image recipe:knowledge-base
   ```

   Anything left out takes its default: QEMU, 2 CPUs, 512M of memory, a 16G disk and the nat
   network.

5. Create a runner from the profile. This also runs in the background; `list` shows it as running
   once it has started, and `console` shows it booting:

   ```sh
   bh cp runner create knowledge-base --profile knowledge-base --adapter "$ADAPTER"
   bh cp runner list
   bh cp runner console knowledge-base --adapter "$ADAPTER"
   ```

6. Publish its port 80 on the mesh. Run this on the adapter's host, or use **Expose…** on the
   Runners page:

   ```sh
   bh host adapter expose knowledge-base 80 --as knowledge-base
   ```

   Within about half a minute, runners on any of your adapters can open
   `http://knowledge-base.mesh/`, and the Buzz Herd app can open `knowledge-base.mesh:80`. Runners on
   the same adapter can already open `http://knowledge-base.buzzherd/`. Each page is also there as
   Markdown, such as `http://knowledge-base.mesh/volumes.md`, which is easier to read from a runner.

## Remove it

```sh
bh cp runner stop knowledge-base --adapter "$ADAPTER"
bh cp runner delete knowledge-base --adapter "$ADAPTER"
bh cp profile delete knowledge-base
bh cp recipe delete knowledge-base
```

Deleting the runner also removes its disk and exposure. Deleting the recipe keeps the images
already built.
