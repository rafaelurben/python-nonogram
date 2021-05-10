"Nonogram CLI"

import click

from rich.table import Table
from rich.rule import Rule

from nonogram.utils import log, setting
from nonogram.game import NonogramGame
from nonogram.examples import all_examples


@click.group()
@click.version_option(message="python-nonogram by rafaelurben, version %(version)s")
def main():
    "The main command"

# Commands


@click.command()
@click.argument('name')
@click.option('--verbose', '-v', default=False, help='Activate verbose output', is_flag=True)
def run_test(name, verbose=False):
    "Test the solver for one example"

    setting('debug', verbose)

    if not name in all_examples:
        log(f"Example {name} not found!")
        return

    log(Rule(f"Running test ({name})"))

    example = all_examples[name][2]
    game = NonogramGame(**example)
    result = game.solve()

    if result:
        log(Rule("Test succeeded"))
    else:
        log(Rule("Test failed"))


@click.command()
def run_tests():
    "Test the solver module for all examples"

    log(Rule(f"Running tests ({len(all_examples)})"))

    tab = Table("Category", "Nr.", "Status", title="Test results")

    for category, num, data in all_examples.values():
        game = NonogramGame(**data)
        result = game.solve()
        tab.add_row(category, str(num), "✅" if result else "❌")

    log(tab, Rule("Tests ended"))

# Add to group


main.add_command(run_test)
main.add_command(run_tests)
