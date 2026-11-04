# Volumes

A runner can mount volumes beside its root disk. You give each one in its profile as
`--volume SOURCE:TARGET[:ro]`: what to mount, the absolute path to mount it at, and `:ro` to make it
read-only. The **Volumes** box on the Runner profiles page takes the same text, one per line.

| Kind | Source | What it is | QEMU | Firecracker |
| --- | --- | --- | --- | --- |
| [Shared directory](#shared-directories) | `dir:/PATH` | A directory on the adapter | Shared live | Read-only: a copy made at each start |
| [Disk](#disks) | `disk:NAME` | An ext4 disk the adapter keeps, which outlives its runners | Yes | Yes |
| [NFS](#nfs) | `nfs://HOST[:PORT]/EXPORT` | An NFSv4 export the runner mounts itself | Yes | Yes |

Which to use:

- **To give runners files from the adapter,** use a shared directory.
- **To keep one runner's data after it's deleted,** use a disk.
- **To share files between runners,** or across adapters, use NFS.

## Shared directories

A shared directory is a directory on the adapter that the runner sees. Only directories inside
`/var/lib/bh/shares` can be shared, so a runner never sees the rest of the adapter.

First, put the files on the adapter. Run this on the adapter itself, over SSH:

```sh
sudo mkdir -p /var/lib/bh/shares/site
sudo cp -r ./site/. /var/lib/bh/shares/site/
```

Then mount it in a profile and create the runner. This serves those files from the `nginx` image in
this repository, read-only:

```sh
bh cp profile set site --image recipe:nginx --volume dir:/var/lib/bh/shares/site:/var/www/html:ro
bh cp runner create site --profile site --adapter "$ADAPTER"
```

- **Under QEMU,** the directory is shared live: a change on the adapter shows in the runner at once.
  Leave off `:ro` to let the runner write to it.
- **Under Firecracker,** `:ro` is required, because Firecracker can't share a directory. The runner
  gets a copy made each time it starts, so changes show at its next start. Use a disk or NFS for
  anything a Firecracker runner writes.
- **To share a directory from elsewhere on the adapter,** bind-mount it inside `/var/lib/bh/shares`.

## Disks

A disk is an ext4 file system that the adapter keeps. It outlives the runner, so the next runner
finds what the last one wrote.

Disks live on one adapter, so make them there. Run this on the adapter's host, or use
`sudo bh adapter volume` on the adapter itself:

```sh
bh host adapter volume create data --size 1G
bh host adapter volume list
```

Then mount it in a profile, and create the runner on that same adapter:

```sh
bh cp profile set notes --image recipe:toolbox --volume disk:data:/srv/data
bh cp runner create notes --profile notes --adapter "$ADAPTER"
```

- **Names and sizes:** a disk's name is a lowercase DNS label of up to 12 characters. Its size is 16M
  to 1T. Disks can't be resized or snapshotted yet.
- **One runner at a time:** creating a second runner with a disk that's in use is refused, so a
  profile with a disk can have only one runner at a time.
- **Deleting:** deleting a runner frees its disk and keeps its data. To delete the disk itself, once
  no runner uses it:

```sh
bh host adapter volume delete data
```

## NFS

With NFS, the runner mounts an NFSv4 export over its own network. NFS works under both QEMU and
Firecracker, and can be shared between runners and across adapters.

The runner needs two things:

- **A network:** `--network nat`, which is the profile default.
- **An NFS client in its image:** the `nfs-common` package. Installing it from user data is too late,
  because volumes are mounted before user data runs.

The server can be another runner, on this adapter or another, or anything the runner's network
reaches. It can't be the adapter itself, because runners can't reach their adapter.

### Run a server

The `nfs-server` image in this repository serves `/srv/nfs`. Add its recipe and build it, as its
README says, then run it:

```sh
bh cp profile set nfs-server --image recipe:nfs-server
bh cp runner create nfs-server --profile nfs-server --adapter "$ADAPTER"
```

Its export is its NFSv4 root, so clients mount `/`.

**This server is for tests and private networks.** It trusts the user IDs that clients send
(`sec=sys`) and lets their root user write as root.

### Mount it on the same adapter

A runner reaches others on its adapter as `NAME.buzzherd`. This image has an NFS client, so it can be
the client as well as the server. Start the server before the client:

```sh
bh cp profile set nfs-client --image recipe:nfs-server --volume nfs://nfs-server.buzzherd/:/mnt/nfs
bh cp runner create nfs-client --profile nfs-client --adapter "$ADAPTER"
```

### Mount it from another adapter

Publish the server's port 2049 on the mesh, on its adapter's host, or with **Expose…** on the Runners
page. See [Exposures](exposures.md):

```sh
bh host adapter expose nfs-server 2049 --as nfs-share
```

Within about half a minute, runners on your other adapters can mount it as
`nfs://nfs-share.mesh/`:

```sh
bh cp profile set nfs-remote --image recipe:nfs-server --volume nfs://nfs-share.mesh/:/mnt/nfs
bh cp runner create nfs-remote --profile nfs-remote --adapter OTHER_ADAPTER
```

A server on a port other than 2049 goes in the source, as `nfs://HOST:PORT/EXPORT`.

## Rules for every volume

- **Limits:** a runner can have at most 8 volumes, each at its own absolute path, which can't be `/`.
- **OSv runners take no volumes,** because they have no cloud-init to mount them.
- **The adapter checks when you create the runner:** that the disk exists and is free, that the
  directory is a shared one, and that the VMM can mount it. If not, it refuses.
- **A failed mount doesn't stop the runner.** Every volume is mounted `nofail`, so a runner whose NFS
  server is down still boots, without that volume.

## Check that a volume mounted

The runner has no shell for you to log in to, so ask it from user data. Volumes are mounted before
user data runs, so this script sees them:

```sh
#!/bin/sh
{ mountpoint /mnt/nfs; ls -l /mnt/nfs; } > /dev/console 2>&1
```

Add the file to the profile with `--user-data FILE` before creating the runner, then read the
result:

```sh
bh cp runner console nfs-client --adapter "$ADAPTER" --lines 200
```

If it didn't mount, see [Troubleshooting](troubleshooting.md#a-volume-is-empty-or-missing).

Next: [Exposures](exposures.md).
