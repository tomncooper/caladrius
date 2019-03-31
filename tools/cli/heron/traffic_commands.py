""" This module contains commands for querying the Magpie traffic prediction end points
for Apache Heron topologies. """

import logging
import json

from typing import List, Dict, Any, Union

import click
import requests

from humanfriendly.tables import format_smart_table

LOG: logging.Logger = logging.getLogger("Magpie_CLI.heron.traffic")


@click.group(short_help="Heron topology traffic modelling options")
@click.pass_obj
def traffic(magpie):
    """ Provides access to the traffic modelling options for Apache Heron."""
    pass


@traffic.command(short_help="List available traffic models")
@click.pass_obj
def model_info(magpie):
    """ Returns the options available for modelling and predicting traffic into an Apache
    Heron topology."""

    LOG.debug("Requesting traffic model information")

    try:
        response: requests.Response = requests.get(
            magpie.url + "/model/traffic/heron/model_info"
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

        click.echo("\nAvailable Traffic Models for Apache Heron Topologies:\n")
        click.echo(format_smart_table(data, headings))


@traffic.command(short_help="Predict traffic levels into a topology")
@click.option("--topology", "-t", required=True, help="The topology ID string")
@click.option("--cluster", "-c", required=True, help="The cluster name")
@click.option(
    "--environ", "-e", required=True, help="The environment (PROD, DEVEL etc)"
)
@click.option("--model", "-m", required=True, help="The model you wish to run")
@click.option(
    "--source_hours",
    "-sh",
    required=True,
    help="The number of hours of " "source data to use in the prediction",
)
@click.option(
    "--future_mins",
    "-fm",
    required=True,
    help="The number of minutes of future traffic to predict",
)
@click.pass_obj
def prediction(magpie, topology, cluster, environ, model, source_hours, future_mins):
    """ Issues a request to the Magpie traffic prediction end point for Apache Heron
    topologies."""

    LOG.debug(
        f"Predicting Traffic levels over the next {future_mins} minutes for topology: "
        f"{topology}, cluster: {cluster}, environment: {environ} using model: {model} "
        f"based on {source_hours} hours of data"
    )

    response: requests.Response = requests.get(
        magpie.url + "/model/traffic/heron",
        params={
            "topology_id": topology,
            "cluster": cluster,
            "environ": environ,
            "model": model,
            "source_hours": source_hours,
            "future_mins": future_mins,
        },
    )

    results: Dict[str, Union[List[str], Dict[str, Any]]] = response.json()

    if "errors" in results:
        LOG.error("Traffic prediction failed")
        click.echo("The following errors were reported by the Magpie server:")
        for error in results["errors"]:
            if "model" in error:
                click.echo(f"Model: {error['model']}")
            click.echo(f"Error type: {error['type']}")
            click.echo(f"Error message: {error['error']}")

    else:
        for model_name, model_results in results.items():
            click.echo(f"Model: {model_name}")
            for key, value in model_results.items():
                click.echo(key)
                click.echo(json.dumps(value, indent=4))
