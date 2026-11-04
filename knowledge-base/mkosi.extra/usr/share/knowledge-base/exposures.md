# Exposures

## On the same adapter

A runner on the `nat` network reaches the other runners on its adapter by name, on every port, with
nothing to set up:

```text
http://potato.buzzherd/
```

The adapter reaches them the same way. A runner can't reach its adapter itself.

## From anywhere on the mesh

An exposure publishes one TCP port of a runner on the mesh, under a name of its own. **Expose…** on
the Runners page makes one, as does this command, which runs on the adapter's host:

```sh
bh host adapter expose potato 80 --as potato
bh host adapter exposures
```

Within about half a minute, others can reach it:

| From | Address |
| --- | --- |
| A runner on any of your adapters | `http://potato.mesh/`, or `potato.mesh:PORT` for other ports |
| An adapter | `potato.mesh:PORT` |
| The Buzz Herd app | `potato.mesh:80`, or `http://potato:80/` |

- **The name** is a lowercase DNS label, unique on the mesh.
- **The port** must be one the exposure publishes: other ports are refused.
- **The runner** must be on the `nat` network, and needs nothing installed.
- **Everyone on the mesh can reach it.** Access can't be narrowed per exposure yet, so use a service's
  own sign-in if it needs one.

A browser on your own computer isn't on the mesh, so it can't open these addresses. Use the Buzz Herd
app, which reaches the mesh from inside the app.

## Remove an exposure

```sh
bh host adapter unexpose potato
```

Deleting the runner also removes its exposures.

Next: [Troubleshooting](troubleshooting.md).
