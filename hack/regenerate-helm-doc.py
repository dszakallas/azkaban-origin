#!/usr/bin/env python

import sys
import pathlib as p
import subprocess

cwd = p.Path.cwd()

def find_chart_root(path: p.Path):
    parents = path.parents
    while parents and (directory := parents[0].resolve()).is_relative_to(cwd):
        manifest = directory / 'Chart.yaml'
        if manifest.exists() and manifest.is_file():
            return [directory]
        _, *parents = parents
    return []


def eprint(*args, **kwargs):
  print(*args, **kwargs, file=sys.stderr)


if __name__ == "__main__":

    eprint("INFO - Regenerating Helm documentation for charts")
    roots = {root for arg in sys.argv[1:] for root in find_chart_root(p.Path(arg))}

    for root in roots:
        eprint(f"INFO - Regenerating Helm documentation for chart {root}")
        subprocess.run([
          "helm-docs",
          f"--chart-search-root={str(root)}",
          # A base filename makes it relative to each chart directory found
          *(["--template-files=_extra.gotmpl"] if (root / "_extra.gotmpl").exists() else []),
          f"--template-files={cwd}/hack/README.md.gotmpl"
        ])
