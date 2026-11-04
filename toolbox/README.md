# Toolbox

The base plus common command-line and build tools: `build-essential`, `curl`, `git`, `jq`, `less`,
the OpenSSH client and `vim-tiny`. It builds for amd64 and arm64 adapters.

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
   bh cp recipe set toolbox --tool mkosi \
     --repo https://github.com/notnotwillk/test-images.git --ref main --directory toolbox
   ```

3. Build it on your adapter. This runs in the background and the first build can take many minutes;
   `builds` shows `ready` when it's done:

   ```sh
   bh cp recipe build toolbox --adapter ADAPTER
   bh cp recipe builds
   ```

4. Add a runner profile that boots it:

   ```sh
   bh cp profile set toolbox --image recipe:toolbox
   ```

   Anything left out takes its default: QEMU, 2 CPUs, 512M of memory, a 16G disk and the nat
   network.

5. Create a runner from the profile. This also runs in the background; `list` shows it as running
   once it has started, and `console` shows it booting:

   ```sh
   bh cp runner create toolbox --profile toolbox --adapter ADAPTER
   bh cp runner list
   bh cp runner console toolbox --adapter ADAPTER
   ```

6. It has no service and no SSH server, so give it work as cloud-init user data. To run a script at
   first boot, write it to a file and add `--user-data FILE` to the profile in step 4. Output sent to
   `/dev/console` shows in `console`:

   ```sh
   #!/bin/sh
   git --version > /dev/console 2>&1
   ```

## Remove it

```sh
bh cp runner stop toolbox --adapter ADAPTER
bh cp runner delete toolbox --adapter ADAPTER
bh cp profile delete toolbox
bh cp recipe delete toolbox
```

Deleting the runner also removes its disk. Deleting the recipe keeps the images
already built.
