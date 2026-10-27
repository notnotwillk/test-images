# Test images

Sample runner images, each an [mkosi](https://github.com/systemd/mkosi) project built from git by a
control plane's image recipes.

- `base/` is a bootable Debian 13: its kernel and initramfs, systemd, networkd, resolved and
  cloud-init. The others include it.
- `registry/` is the base plus an OCI registry on port 5000.
- `nginx/` is the base plus nginx on port 80, serving a static page.
- `toolbox/` is the base plus common command-line and build tools.

## Using one

Add an image recipe (tool `mkosi`) with two git files, both from
`https://github.com/notnotwillk/test-images.git` at ref `main`:

| Path in the project | Path in the repository |
| ------------------- | ---------------------- |
| (empty)             | the image, such as `registry` |
| `base`              | `base`                 |

The image's `mkosi.conf` includes `base`, so both end up in the image. `base` alone is a recipe
too, with one git file: path empty, path in the repository `base`.

## Adding an image

1. Make `NAME/mkosi.conf` with `[Config] Include=base`, and add packages under `[Content]
   Packages=`. Don't change the kernel, init or cloud-init.
2. Put files to copy into the image under `NAME/mkosi.extra/`, and enable services in an executable
   `NAME/mkosi.postinst.chroot`, which runs inside the image after its packages are installed.

A runner image needs systemd as init, cloud-init, and exactly one kernel and initramfs in `/boot`,
which the adapter boots directly. That's why `base` sets `Bootable=no` and picks the kernel by
architecture in `base/mkosi.conf.d/`.
