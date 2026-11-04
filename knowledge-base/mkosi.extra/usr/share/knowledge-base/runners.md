# Runners

A runner is a small virtual machine on an adapter. On the control plane you create one from a
**runner profile**, which says what it boots and how big it is. The **Runner profiles** and
**Runners** pages do everything here too.

## Make a profile

```sh
bh cp profile set potato --image recipe:potato --memory 1G
bh cp profile list
bh cp profile show potato
```

`set` creates the profile, or replaces all of it: anything you leave out returns to its default.

| Option | What it sets | Default |
| --- | --- | --- |
| `--vmm qemu` or `firecracker` | What runs the runner | `qemu` |
| `--image SOURCE` | What it boots: `recipe:NAME`, or an OCI image such as `HOST/REPOSITORY:TAG` | Debian's cloud image |
| `--cpus N` | Virtual CPUs | 2 |
| `--memory SIZE` | Memory, at least 256M | 512M |
| `--disk SIZE` | Root disk, at least 1G | 16G |
| `--network none` or `nat` | Whether it has a network | `nat` |
| `--user-data FILE` | Cloud-init user data | None |
| `--volume SOURCE:TARGET[:ro]` | A volume to mount; repeat it for more. See [Volumes](volumes.md) | None |

A profile's name is a lowercase DNS label of up to 24 characters.

## Create a runner

```sh
bh cp runner create potato --profile potato --adapter "$ADAPTER"
bh cp runner list
bh cp runner console potato --adapter "$ADAPTER"
```

The runner is created and started in the background. `list` shows every adapter's runners, with each
one's state, adapter and address, and says which adapters didn't answer. `console` shows its serial
console, which is where to watch it boot. Add `--lines N` for more of it.

A runner keeps what its profile said when it was created. Editing or deleting a profile changes no
runner, so to change a runner's settings, delete it and create it again.

A runner's name is a lowercase DNS label of up to 32 characters, unique on its adapter.

## Control a runner

```sh
bh cp runner stop potato --adapter "$ADAPTER"
bh cp runner start potato --adapter "$ADAPTER"
bh cp runner delete potato --adapter "$ADAPTER"
```

Start and stop return before the runner has finished, so check `list` to see when it has. What you
can do depends on its state:

| State | What it means | What you can do |
| --- | --- | --- |
| `creating` | It's being created, which can include building its image | Nothing yet |
| `starting`, `running` | It's starting or up | Stop |
| `stopping` | It's shutting down | Nothing yet |
| `stopped` | It's off | Start, delete |
| `failed` | It crashed, or couldn't be created | Delete; start too, unless creating it failed |

Deleting a runner removes its root disk and exposures. It keeps its [disks](volumes.md#disks).

`running` means the virtual machine is up. To see whether it finished booting, look for `booted` in
`bh cp runner list --json`.

## Give a runner work

Runners have no SSH server unless their image adds one. To run something in one, give its profile
cloud-init user data of up to 32 KiB, either `#cloud-config` or a `#!` script:

```sh
bh cp profile set toolbox --image recipe:toolbox --user-data job.sh
```

A script runs once, at the runner's first boot. To see its output, send it to the console:

```sh
#!/bin/sh
git --version > /dev/console 2>&1
```

## QEMU or Firecracker

Both boot the same images. QEMU is the default and works anywhere. Firecracker has more
requirements:

- The adapter needs `/dev/kvm`.
- It boots OCI images only, so its profile must give `--image`.
- [Shared directories](volumes.md#shared-directories) must be read-only, and are copied at each
  start.

The first Firecracker runner on an adapter downloads Firecracker from GitHub.

## Without a profile

On an adapter's host, you can create a runner directly:

```sh
bh host adapter runner create r1 --image recipe:potato --network nat --start
```

The defaults differ here: 1 CPU, a 4G disk and **no network** unless you pass `--network nat`.

Next: [Volumes](volumes.md).
