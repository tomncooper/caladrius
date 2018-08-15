import logging

from sys import stdout

import click

from heron.commands import heron

LOG: logging.Logger = logging.getLogger("Caladrius_CLI")

class Caladrius(object):
    """ This is a helper context class for all the Caladrius DSPS sub-commands """

    def __init__(self, url: str, debug: bool) -> None:
        self.url: str = url
        self.debug: bool = debug

@click.argument('url', required=True, envvar="CALADRIUS")
@click.option('--debug/--no-debug', required=False, default=False,
              help="Indicates if debug level information should be output.")
@click.group()
@click.pass_context
def cli(ctx, url, debug):
    """ Command line interface for the Caladrius DSPS modelling server. This program
    allows the server to be queried from the command line and is intended for development
    and testing.

    The URL argument can be supplied as the first argument (before the DSPS subcommands)
    or read from the CALADRIUS environment variable.
    """

    # Setup the logger for the CLI
    if debug:
        LOG.setLevel(logging.DEBUG)
        formatter = logging.Formatter(("{levelname} | {name} | function: {funcName} "
                                       "| line: {lineno} | {message}"),
                                      style='{')
    else:
        LOG.setLevel(logging.INFO)
        formatter = logging.Formatter(("{levelname} | {message}"), style='{')

    console_handler: logging.StreamHandler = logging.StreamHandler(stdout)
    console_handler.setFormatter(formatter)
    LOG.addHandler(console_handler)

    if "http://" not in url:
        LOG.debug("Warning: http:// was not included in the supplied URL. This will be "
                  "added for all calls to the server")
        url = "http://" + url

    ctx.obj = Caladrius(url, debug)

    LOG.debug(f"Connecting to Caladrius server at: {url}")

# Add each of the DSPS subcommands
cli.add_command(heron)

if __name__ == "__main__":

    cli()
