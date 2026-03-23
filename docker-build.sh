#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: ./docker-build.sh <image:tag>" >&2
  echo "Example: ./docker-build.sh us-docker.pkg.dev/rational-aria-186218/lambdaplex-public/plex-hbot:0.2.0" >&2
  exit 2
fi

IMAGE_TAG="$1"

branch=""
commit=""
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  branch="$(git rev-parse --abbrev-ref HEAD)"
  commit="$(git rev-parse HEAD)"
fi

build_date="$(date -u +%FT%TZ)"

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t "$IMAGE_TAG" \
  --build-arg "BRANCH=${branch}" \
  --build-arg "COMMIT=${commit}" \
  --build-arg "BUILD_DATE=${build_date}" \
  --push \
  .
