# Recipe Transformer

## Installation

This project uses [`pipenv`](https://pipenv.readthedocs.io/en/latest/) to manage dependencies. Make sure you have it installed before working on the project:

```sh
pip install --user pipenv
```

First navigate to the `project2` directory. Then install dependencies:

```sh
pipenv install
```

Now activate the virtual environment:

```sh
pipenv shell
```

Now you should be good to go.

## Using `pipenv`

Adding dependencies:

```sh
pipenv install <package-name>
```

Removing dependencies:

```sh
pipenv uninstall <package-name>
```

Exiting virtual environment:

```sh
exit
```

Lint Python files:

```sh
pipenv run lint
```

## Using the Program

`py/main.py` takes an AllRecipes url from standard input and prints a transformed recipe to standard ouput. Eg:

```sh
python py/main.py < address
```
