# Troubleshooting

## A recipe won't save

The control plane fetches the directory when you save, and says why it couldn't:

| Error | What to check |
| --- | --- |
| `git_unreachable` | The URL is right, and the repository is public and on HTTPS |
| `git_ref_not_found` | The branch, tag or commit exists |
| `git_path_not_found` | The directory exists at that ref |
| `git_too_large` | The directory isn't too big: it can have at most 200 files |
| `git_unsupported_entry` | The directory has no symlinks or submodules |

## A build failed

`bh cp recipe builds` shows the state, and the reason is in its JSON. When mkosi or buildah failed,
that includes the end of its output, which the Image recipes page shows under **Output**:

```sh
bh cp recipe builds --json
```

## A runner failed to create

`bh cp runner list` shows it as `failed`, and its JSON says why. A runner whose create failed can
only be deleted, so fix the cause, delete it and create it again:

```sh
bh cp runner list --json
bh cp runner delete potato --adapter "$ADAPTER"
```

Creating a runner is refused at once when its volumes can't work:

| Refusal is about | What to do |
| --- | --- |
| A disk | Make it on that adapter, or free it from the runner using it |
| A directory | Move it inside `/var/lib/bh/shares` |
| A directory on Firecracker | Add `:ro`, or use a disk or NFS |
| An OSv image | Remove the volumes: OSv runners take none |

## A runner won't boot

Read its console. A runner that crashed shows as `failed`, and its console prints why:

```sh
bh cp runner console potato --adapter "$ADAPTER" --lines 200
```

`running` means only that the virtual machine is up. If `booted` stays false in
`bh cp runner list --json`, the console shows how far it got.

## A volume is empty or missing

Volumes are mounted `nofail`, so a runner boots without one that couldn't be mounted. To see whether
it mounted, [ask from user data](volumes.md#check-that-a-volume-mounted).

- **NFS:**
    - The runner's image must have `nfs-common`. Installing it from user data is too late.
    - The server must be up when the runner boots. If it wasn't, restart the runner.
    - The profile needs `--network nat`.
    - From another adapter, use the exposure's name, `NAME.mesh`, rather than `NAME.buzzherd`.
- **A shared directory:** under Firecracker, changes on the adapter show only at the next start.
- **A disk:** a new runner sees what's on the disk, so it can look empty if the last runner wrote
  somewhere else.

## An exposure doesn't answer

- Give it about half a minute after you make it.
- Run `bh host adapter exposures` to check its name and port.
- Check that the runner is on the `nat` network and is running.
- Check that the service inside is listening on that port, from another runner on the adapter:
  `NAME.buzzherd:PORT`.

## An adapter didn't answer

`bh cp runner list` names any adapter that didn't answer. Ask it directly, and on its host, check
that it's running:

```sh
bh cp adapter status "$ADAPTER"
bh host adapter status
bh host adapter start
```

## A command is refused

- **You're not signed in:** run `bh auth login`.
- **"no control plane":** run `bh config set default-control-plane https://CONTROL_PLANE`.
- **"this host has no adapter":** `bh host` acts on the machine you're on, so run it on the adapter's
  host. For another machine's adapter, use `bh cp`.
