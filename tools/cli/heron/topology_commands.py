""" This module contains the topology performance modelling commands for Apache Heron """
import logging

from typing import List, Dict

import click
import requests

from humanfriendly.tables import format_smart_table

LOG: logging.Logger = logging.getLogger("Magpie_CLI.heron.topology")


@click.group(short_help="Heron topology performance modelling options")
@click.pass_obj
def topology(magpie):
    """ Provides access to the topology performance modelling options for Apache Heron."""
    pass


@topology.command(short_help="List available topology performance models")
@click.pass_obj
def model_info(magpie):
    """ Returns the options available for modelling and predicting the performance of an
    Apache Heron topology."""

    LOG.debug("Requesting topology performance model information")

    try:
        response: requests.Response = requests.get(
            magpie.url + "/model/topology/heron/model_info"
        )
    except requests.exceptions.ConnectionError:
        LOG.error(
            "Unable to connect to Magpie server at: %s, is the server active?",
            magpie.url,
        )

    else:
        models: List[Dict[str, str]] = response.json()

        data: List[List[str]] = []

        headings = ["Name", "Description"]

        for model in models:
            data.append([model["name"], model["description"]])

        click.echo("\nAvailable performance models for Apache Heron topologies:\n")
        click.echo(format_smart_table(data, headings))
