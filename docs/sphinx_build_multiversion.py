"""Script to loop over a number of git branches/tags, check them out and build the
the sphinx docs.
The branches/tags for which the docs are generated are defined in the file
"docs/source/_static/switcher.json" (note that the docs do not use the local version
by default, but instead the version from the latest commit on GH-Pages. This is due to
the fact that this button prefers urls instead of local filenames).

This script has to be executed in the root of the repository!
"""

import json
import os
from shutil import copy
from subprocess import run
import subprocess


def build_docs_version(version):
    """Builds the docs for a specific version. The latest conf.py is used no matter
    if it differs from the version from back then.

    Parameters
    ----------
    version : str
        Branch or tag name for which the docs are built
    """
    # checkout the version/tag and obtain latest conf.py
    run(f"git checkout {version}", shell=True, check=True)
    if os.path.isfile("docs/source/conf.py"):
        # removing the old conf.py file to make room for the latest one
        os.remove("docs/source/conf.py")
    copy("conf_latest.py", "docs/source/conf.py")

    # run librep on markdown files (render placeholders with sytax §§§filename§§§)
    run(
        "librep --ref_dir $PWD --input 'docs/**/*.md' --no_backup",
        shell=True,
        check=True,
    )

    # build the docs for this version
    run(
        f"sphinx-build -b html docs/source docs/_build/html/{version}",
        shell=True,
        check=True,
    )
    run("git stash", shell=True, check=True)


def main():
    """main function that is executed when the script is called."""
    with open("docs/source/_static/switcher.json", "r") as f:  # pylint: disable=W1514
        version_switcher = json.load(f)

    # get currently active branch
    # command = "git rev-parse --abbrev-ref HEAD".split()
    # try:
    #     initial_branch = (
    #         run(command, capture_output=False, check=True, stderr=subprocess.STDOUT)
    #         .stdout.strip()
    #         .decode("utf-8")
    #     )
    # except subprocess.CalledProcessError as e:
    #     print("Exception on process, rc=", e.returncode, "output=", e.output)
    initial_branch = "master"

    # copy("docs/source/conf.py", "./conf_latest.py")

    # build docs for main branch no matter what versions are present in the switcher
    build_docs_version("master")

    # build docs for the version that are listed in the version switcher
    # for entry in version_switcher:
    #     if entry["version"] == "master":
    #         continue
    #     build_docs_version(entry["version"])

    # # checkout initial branch for following steps
    # run(f"git checkout {initial_branch}", shell=True, check=True)
    # os.remove("./conf_latest.py")


if __name__ == "__main__":
    main()
