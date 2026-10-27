# Test images

Image recipes for [Buzz Herd](https://github.com/notwillk/boxlab) runners, as git-backed recipe
files. Each directory is an mkosi project; on a control plane's **Runner images** page, add a recipe
with one git file: URL `https://github.com/notnotwillk/test-images.git`, ref `main`, and the
directory as its path in the repository.

- `registry/`: Debian 13 with an OCI registry (`docker-registry`) on port 5000.
