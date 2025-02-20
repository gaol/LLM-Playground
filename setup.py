import os
from typing import List

from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)


def get_path(*filepath) -> str:
    return os.path.join(ROOT_DIR, *filepath)

def read_readme() -> str:
    """Read the README file if present."""
    p = get_path("README.md")
    if os.path.isfile(p):
        with open(get_path("README.md"), encoding="utf-8") as f:
            return f.read()
    else:
        return ""


def read_requirements(filename: str) -> List[str]:
    with open(get_path(filename)) as f:
        return f.read().strip().split("\n")

requirements = read_requirements(get_path("requirements.txt"))

setup(
    name="llms_playground",
    version="0.0.1",
    author="Lin Gao",
    license="Apache 2.0",
    description=("A playground to infer with remote LLM Providers"),
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/gaol/llms_playground",
    project_urls={
        "Homepage": "https://github.com/gaol/llms_playground"
    },
    packages=["llms_playground"],
    install_requires=requirements,
)
