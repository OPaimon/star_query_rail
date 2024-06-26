# star_query_rail

<div align="center">

[![Build status](https://github.com/OPaimon/star_query_rail/workflows/build/badge.svg?branch=main&event=push)](https://github.com/OPaimon/star_query_rail/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/star_query_rail.svg)](https://pypi.org/project/star_query_rail/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/OPaimon/star_query_rail/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/OPaimon/star_query_rail/blob/main/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/OPaimon/star_query_rail/releases)
[![License](https://img.shields.io/github/license/OPaimon/star_query_rail)](https://github.com/OPaimon/star_query_rail/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)

A tool for query some infomation about a game

</div>

## Quick start

We use rye to manager the Project
For Linux User

```bash
curl -sSf https://rye.astral.sh/get | bash
```

Sync the project
```bash
rye sync
```

Then you can run the server using the following command:

```bash
rye run uvicorn star_query_rail.main:app
```


### Makefile usage

[`Makefile`](https://github.com/OPaimon/star_query_rail/blob/main/Makefile) contains a lot of functions for faster development.


<details>
<summary>Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>Codestyle and type checks</summary>
<p>

Automatic formatting uses `ruff`.

```bash
make polish-codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `ruff` and `darglint` library

</p>
</details>

<details>
<summary>Code security</summary>
<p>

> If this command is not selected during installation, it cannnot be used.

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

<details>
<summary>Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>All linters</summary>
<p>

Of course there is a command to run all linters in one:

```bash
make lint
```

the same as:

```bash
make check-codestyle && make test && make check-safety
```

</p>
</details>


<details>
<summary>Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 🛡 License

[![License](https://img.shields.io/github/license/OPaimon/star_query_rail)](https://github.com/OPaimon/star_query_rail/blob/main/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/OPaimon/star_query_rail/blob/main/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{star_query_rail,
  author = {star_query_rail},
  title = {A tool for query some infomation about a game},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/OPaimon/star_query_rail}}
}
```

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/P3G-%F0%9F%9A%80-brightgreen)](https://github.com/Undertone0809/python-package-template)

This project was generated with [P3G](https://github.com/Undertone0809/P3G)
