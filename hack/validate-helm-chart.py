#!/usr/bin/env python

import sys
import pathlib as p
import subprocess

kubeconform_config = ["-strict", "-ignore-missing-schemas", "-schema-location", "default", "-verbose"]

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
    eprint("INFO - Validating Helm charts")
    roots = {root for arg in sys.argv[1:] for root in find_chart_root(p.Path(arg))}

    errors = 0
    for root in roots:
        eprint(f"INFO - Validating Helm chart {root}")
        rendered = subprocess.run(["helm", "--debug", "template", str(root)], capture_output=True)
        if rendered.returncode:
            eprint(f"ERROR - Helm chart {root} could not be rendered")
            eprint(rendered.stderr.decode('utf-8'))
            errors = errors + 1
            break
        conforms = subprocess.Popen(['kubeconform', *kubeconform_config], stdin=subprocess.PIPE)
        conforms.stdin.write(rendered.stdout)
        conforms.stdin.close()
        conforms.wait()
        if conforms.returncode:
            eprint(f"ERROR - Helm chart {root} is invalid")
            errors = errors + 1
            break

    eprint(f"INFO - {errors} errors found")
    if errors:
        sys.exit(1)
