# Test images

Sample runner images, each an [mkosi](https://github.com/systemd/mkosi) project built from git by a
control plane's image recipes.

- `base/` is a bootable Debian 13: its kernel and initramfs, systemd, networkd, resolved and
  cloud-init.
- `registry/` is the base plus an OCI registry on port 5000.
- `nginx/` is the base plus nginx on port 80, serving a static page.
- `toolbox/` is the base plus common command-line and build tools.
- `potato/` is the potato server: the base plus nginx on port 80, configured only to serve the
  Potato Operations Center page.

Each directory is self-contained: the images carry their own copy of the base's settings.

## Using one

Add an image recipe (tool `mkosi`) with repository `https://github.com/notnotwillk/test-images.git`,
ref `main`, and the image's directory, such as `registry`.

## Adding an image

1. Copy `base/` to `NAME/`, and add packages to `[Content] Packages=` in `NAME/mkosi.conf`. Don't
   change the kernel, init or cloud-init.
2. Put files to copy into the image under `NAME/mkosi.extra/`, and enable services in
   `NAME/mkosi.postinst.chroot`, which runs inside the image after its packages are installed.

A runner image needs systemd as init, cloud-init, and exactly one kernel and initramfs in `/boot`,
which the adapter boots directly. That's why each image sets `Bootable=no` and picks the kernel by
architecture in `mkosi.conf.d/`.
