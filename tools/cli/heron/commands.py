import logging
import json

from typing import List, Dict, Any

import click
import requests

from humanfriendly.tables import format_smart_table

from .traffic_commands import traffic
from .topology_commands import topology

LOG: logging.Logger = logging.getLogger("Magpie_CLI.heron")


@click.group(short_help="Apache Heron modelling options")
@click.pass_obj
def heron(magpie):
    """ Provides access to the Apache Heron modelling options within Magpie."""
    pass


heron.add_command(traffic)
heron.add_command(topology)
