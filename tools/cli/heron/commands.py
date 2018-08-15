import logging
import json

from typing import List, Dict, Any

import click
import requests

from humanfriendly.tables import format_smart_table

from .traffic_commands import traffic
from .topology_commands import topology

LOG: logging.Logger = logging.getLogger("Caladrius_CLI.heron")


@click.group(short_help="Apache Heron modelling options")
@click.pass_obj
def heron(caladrius):
    """ Provides access to the Apache Heron modelling options within Caladrius."""
    pass

heron.add_command(traffic)
heron.add_command(topology)
