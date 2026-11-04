# Buzz Herd knowledge base

How to use a Buzz Herd control plane: what it does, and how to build images, run runners on your
adapters, mount volumes in them, and reach what they serve.

These pages are fixed into this image when it's built, so they describe `bh` as of that build. For
the current options, run `bh cp --help`.

## How it fits together

The **control plane** keeps what you've defined and tells your **adapters** what to do. An adapter
is the Debian machine that runs your **runners**, which are small virtual machines.

From nothing to a running service, you go through these steps:

1. An **image recipe** says where an image's files are, in a public git repository.
2. A **build** on an adapter makes the image from the recipe.
3. A **runner profile** says which image to boot, how big to make the runner, and what to mount.
4. A **runner** is created from the profile on an adapter.
5. An **exposure** publishes one of the runner's ports on the mesh, so other machines can reach it.

## Where to do what

Each page of the control plane's website has matching commands, which you can run from any machine.

| Web page | Commands | What it's for |
| --- | --- | --- |
| Adapters | `bh cp adapter`, `bh cp host` | Add, adopt and remove adapters and their hosts |
| Image recipes | `bh cp recipe` | Define image recipes, and build them |
| Runner profiles | `bh cp profile` | Define what runners are created from |
| Runners | `bh cp runner` | Create, start, stop and delete runners, and read their consoles |
| Secrets | `bh cp secret` | Give runners secrets, and check that adapters hold them |
| Settings | `bh cp registry` | Choose the image registry that builds are pushed to |

Two things aren't under `bh cp`:

- **Exposures:** use **Expose…** on the Runners page, or `bh host adapter expose` on the adapter's
  host.
- **Disks and shared directories:** these live on an adapter, so you make them with
  `bh host adapter volume` or on the adapter itself. See [Volumes](volumes.md).

## Pages

- [Getting started](getting-started.md): sign in, and find your adapter.
- [Image recipes](image-recipes.md): define and build images.
- [Runners](runners.md): profiles, and creating and controlling runners.
- [Volumes](volumes.md): shared directories, disks and NFS.
- [Exposures](exposures.md): reach what a runner serves.
- [Troubleshooting](troubleshooting.md): when something doesn't work.
