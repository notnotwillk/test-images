# Test images

Sample runner images, each an [mkosi](https://github.com/systemd/mkosi) project built from git by a
control plane's image recipes, plus one Containerfile recipe that builds an
[OSv](https://github.com/cloudius-systems/osv) unikernel with
[capstan](https://github.com/cloudius-systems/capstan).

- `base/` is a bootable Debian 13: its kernel and initramfs, systemd, networkd, resolved and
  cloud-init.
- `registry/` is the base plus an OCI registry on port 5000.
- `nginx/` is the base plus nginx on port 80, serving a static page.
- `toolbox/` is the base plus common command-line and build tools.
- `nfs-server/` is the base plus an NFS server: `/srv/nfs` over NFSv4.1 and 4.2, on TCP port 2049
  only, as the NFSv4 root (clients mount `HOST:/`). A runner on the same adapter mounts it as a
  volume with `--volume nfs://NAME.buzzherd/:/mnt/nfs`; runners on other adapters mount it through
  an exposure of port 2049 (`bh host adapter expose NAME 2049 --as SHARE`), as
  `nfs://SHARE.mesh/`. The image they run needs an NFS client (`nfs-common`). It trusts clients'
  user IDs (`sec=sys`) and lets their root write as root, so keep it to tests and private
  networks.
- `potato/` is the potato server: the base plus nginx on port 80, configured only to serve the
  Potato Operations Center page.
- `micro-potato/` is the potato server as an OSv unikernel (tool `containerfile`): a small C
  server, `potato.c`, serving the same page on port 80. Its `Containerfile` compiles it, composes it
  with capstan v1.0.0 onto OSv v0.57.0's loader (every download checked against a pinned SHA-256),
  and leaves `/osv/disk.qcow2` and `/osv/kernel.elf`, which runners boot under QEMU or Firecracker
  on amd64 adapters. The capstan package itself is `meta/`, so `make` then
  `capstan package compose --pull-missing --fs rofs micro-potato` builds it by hand too.

Each directory is self-contained: the images carry their own copy of the base's settings.

## Using one

Each image's directory has a README with the `bh cp` commands to add it to a control plane, build
it, and run it.

## Adding an image

1. Copy `base/` to `NAME/`, and add packages to `[Content] Packages=` in `NAME/mkosi.conf`. Don't
   change the kernel, init or cloud-init.
2. Put files to copy into the image under `NAME/mkosi.extra/`, and enable services in
   `NAME/mkosi.postinst.chroot`, which runs inside the image after its packages are installed.

A runner image needs systemd as init, cloud-init, and exactly one kernel and initramfs in `/boot`,
which the adapter boots directly. That's why each image sets `Bootable=no` and picks the kernel by
architecture in `mkosi.conf.d/`.
