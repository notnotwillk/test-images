# Getting started

## Sign in

Tell `bh` which control plane you use, then sign in. Replace the address with your control plane's:

```sh
bh config set default-control-plane https://CONTROL_PLANE
bh auth login
```

`bh auth login` prints a code and a link. Approve the code in a browser where you're signed in to
the control plane. `bh auth status` shows whether you're signed in.

## Find your adapter

Most commands need to know which adapter to act on. List them, and put your adapter's name in
`ADAPTER`, which these pages use:

```sh
bh cp adapter list
export ADAPTER=NAME
bh cp adapter status "$ADAPTER"
```

An adapter can be given by its name or its ID. A name that more than one adapter has is refused.

## Add an adapter

If you don't have an adapter yet, make a one-time token, which also prints the command to run on the
machine that will host it. **Add adapter** on the Adapters page does the same:

```sh
bh cp adapter token create
```

That command looks like this:

```sh
bh host adapter add --delete-policy retain --control-plane-url https://CONTROL_PLANE --token TOKEN
```

An adapter registered without a token waits for you to adopt it. **Adopt** on the Adapters page
does that, as does this command:

```sh
bh cp adapter adopt "$ADAPTER"
```

## Which command acts on what

| Command | Run it | It acts on |
| --- | --- | --- |
| `bh cp ...` | Anywhere, signed in with `bh auth login` | The control plane, and any adapter through it |
| `bh host ...` | On the machine that hosts the adapter | That machine, and its one adapter |
| `bh adapter ...` | On the adapter itself, with `sudo` | That adapter |

`bh host adapter runner`, `image` and `volume` run the matching `bh adapter` command in the adapter
for you, so you don't need SSH. Use `bh adapter` over SSH, or on an adapter with no host.

Next: [Image recipes](image-recipes.md).
