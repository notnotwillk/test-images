# Image recipes

An image recipe says how to make a runner's image: a build tool, and a directory of a public git
repository. Adapters do the building. The **Image recipes** page does everything here too.

## Add a recipe

```sh
bh cp recipe set potato --tool mkosi \
  --repo https://github.com/notnotwillk/test-images.git --ref main --directory potato
```

- **`--tool`:** `mkosi` for an mkosi project, or `containerfile` for a directory with a
  `Containerfile`. `capstan` recipes can be kept, but aren't built.
- **`--repo`:** a public repository's HTTPS URL.
- **`--ref`:** a branch, tag or commit. It's `main` if you leave it out.
- **`--directory`:** the directory to use. It's the whole repository if you leave it out.

The control plane fetches the directory when you save, and refuses a recipe it can't fetch. Running
`set` again replaces the recipe.

To see what you have, and to read a file as it was last fetched:

```sh
bh cp recipe list
bh cp recipe show potato
bh cp recipe file potato mkosi.conf
```

## Build it

```sh
bh cp recipe build potato --adapter "$ADAPTER"
bh cp recipe builds
```

The build runs in the background, and the first one can take many minutes. The recipe is fetched
again first, so a new commit on `--ref` is picked up. `builds` shows each build's state:

| State | Meaning |
| --- | --- |
| `building` | It's still going |
| `ready` | It's done, and runners on that adapter can boot it at once |
| `failed` | It stopped. See [Troubleshooting](troubleshooting.md#a-build-failed) |

## Use it

A runner boots a recipe's image when its profile says `--image recipe:NAME`:

```sh
bh cp profile set potato --image recipe:potato
```

The runner uses the recipe's current version: that adapter's build of it, or a pull from the image
registry if the registry has it. If neither has it, the adapter builds it there and then, so
creating the runner takes as long as the build. See [Runners](runners.md).

## Share builds through a registry

So that adapters don't each have to build an image, one adapter can push its build to an image
registry for the others to pull.

The registry is a mesh address: a mesh name, a port and an optional path. The name has no dots, so
it's usually an [exposure](exposures.md), not a public host. The `registry` image in this repository
can be that registry, once its port 5000 is exposed as `registry`:

```sh
bh cp registry set registry:5000/bh
bh cp recipe build potato --adapter "$ADAPTER" --push
bh cp registry images
```

**Settings** on the website sets the same thing. `bh cp registry show` prints the address, and
`bh cp registry clear` removes it.

## Remove a recipe

```sh
bh cp recipe delete potato
```

Images already built are kept.

Next: [Runners](runners.md).
