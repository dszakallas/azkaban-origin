#!/usr/bin/env sh

set -ex

for arg in "$@"; do
    generate-schema-doc --config template_name=md "$arg" $(echo "$arg" | sed -e 's/\.json$/.md/g')
done
