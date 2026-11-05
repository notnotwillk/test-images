# Hermes with OpenRouter

The base plus [Hermes Agent](https://github.com/NousResearch/hermes-agent) and its web dashboard, behind nginx on
port 80. It builds for amd64 and arm64 adapters, and Hermes's own dependencies come from its installer when the
image is built.

Until the runner is granted the `openrouter-api-key` secret, every page is the instructions for getting one. Hermes
starts within about 10 seconds of the grant, and stops again if the grant goes away.

**There's no login.** Anything on the mesh that can open this exposure can use the agent, which can run commands in
this runner, spend your OpenRouter credit and read the key. Use a key with a low credit limit.

## Add this image

The [`hermes-openrouter` bundle](../bundles/README.md) does it all, and `bootstrap` includes it. Once it's installed,
open `http://hermes/` from the Buzz Herd app's Applications tab, and follow the page.

## What's in it

- **`mkosi.prepare.chroot`** installs Hermes with its published installer, pinned to one release.
- **`hermes-gate`** reads the secret and switches nginx between the setup page and Hermes. The key is only ever in
  memory, in `/run/hermes/env`.
- **`mkosi.extra/usr/share/hermes-image/skills/`** holds the skills the image starts with. Add a directory there for
  another. The only one so far is `prove-it`: ask Hermes to prove it works.

Chats and anything else Hermes saves are on the runner's disk, so they're gone when the runner is replaced.
