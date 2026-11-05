# Bundles

A bundle is a file that says what to set up on an adapter: which image recipes, runner profiles, runners,
exposures and applications to make, and which other bundles it needs. These build on the images in this repository.

| Bundle | What it sets up |
| --- | --- |
| [`bootstrap`](bootstrap/bundle.yaml) | All of the others. It has no entities of its own |
| [`knowledge-base`](knowledge-base/bundle.yaml) | The [knowledge base](../knowledge-base/README.md), exposed as `knowledge-base`, and an application to open it |
| [`potato`](potato/bundle.yaml) | The [potato server](../potato/README.md), exposed as `potato`, and an application to open it |
| [`hermes-openrouter`](hermes-openrouter/bundle.yaml) | [Hermes with OpenRouter](../hermes-openrouter/README.md), exposed as `hermes`, and an application to open it. It needs an OpenRouter key, and a slow first build. It runs under Firecracker, which needs KVM: without it, set `vmm=qemu` |

Their recipes use this repository at the bundle's own commit, so one commit pins everything. They're kept
here rather than in each image's directory, because a file in that directory would become part of the
recipe and change its version.

## Using one

You need an adapter and `bh cp`. Sign in, and find your adapter's name:

```sh
bh auth login
bh cp adapter list
export ADAPTER=NAME
```

Save the bundle, along with everything it depends on, and see what installing it would do:

```sh
bh cp bundle add --repo https://github.com/notnotwillk/test-images.git --path bundles/bootstrap/bundle.yaml
bh cp bundle install bootstrap --adapter "$ADAPTER" --dry-run
```

Install it, and watch how far it has got. The first install builds each image, which can take many minutes:

```sh
bh cp bundle install bootstrap --adapter "$ADAPTER"
bh cp bundle installed
```

To change a param, set it. A dependency's param takes the dependency's name first:

```sh
bh cp bundle update bootstrap --adapter "$ADAPTER" --set potato.memory=1G
```

The Buzz Herd app lists the applications on its Applications tab, and opens one in its Mesh tab. Each
application takes its name from its exposure.

An exposure's name is unique across the mesh, so a second adapter needs its own:

```sh
bh cp bundle install bootstrap --adapter "$OTHER_ADAPTER" --set potato.exposure=potato-2 --set knowledge-base.exposure=knowledge-base-2 --set hermes-openrouter.exposure=hermes-2
```

Uninstalling removes what it made, and the dependencies nothing else needs:

```sh
bh cp bundle uninstall bootstrap --adapter "$ADAPTER"
```
