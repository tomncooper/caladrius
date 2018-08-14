import logging
import json

from typing import List, Dict, Any

import click
import requests

from humanfriendly.tables import format_smart_table

LOG: logging.Logger = logging.getLogger("Caladrius_CLI.heron")


@click.group(short_help="Apache Heron modelling options")
@click.pass_obj
def heron(caladrius):
    """ Provides access to the Heron modelling options within Caladrius"""
    pass


@heron.group(short_help="Heron topology traffic modelling options")
@click.pass_obj
def traffic(caladrius):
    pass


@traffic.command()
@click.pass_obj
def model_info(caladrius):
    LOG.debug("Requesting traffic model information")

    response: requests.Response = requests.get(
        caladrius.url + "/model/traffic/heron/model_info"
    )

    models: List[Dict[str, str]] = response.json()

    data: List[List[str]] = []

    headings = ["Name", "Description"]

    for model in models:
        data.append([model["name"], model["description"]])

    click.echo("\nAvailable Traffic Models for Apache Heron Topologies:\n")
    click.echo(format_smart_table(data, headings))


@traffic.command()
@click.option("--topology", "-t", required=True, help="The topology ID string")
@click.option("--cluster", "-c", required=True, help="The cluster name")
@click.option(
    "--environ", "-e", required=True, help="The environment (PROD, DEVEL etc)"
)
@click.option("--model", "-m", help="The model you wish to run")
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
def prediction(caladrius, topology, cluster, environ, model, source_hours, future_mins):
    LOG.debug(
        f"Predicting Traffic levels over the next {future_mins} minutes for topology: "
        f"{topology}, cluster: {cluster}, environment: {environ} using model: {model} "
        f"based on {source_hours} hours of data"
    )

    response: requests.Response = requests.get(
        caladrius.url + "/model/traffic/heron",
        params={
            "topology_id": topology,
            "cluster": cluster,
            "environ": environ,
            "model": model,
            "source_hours": source_hours,
            "future_mins" : future_mins
        },
    )

    results: Dict[str, Dict[str, Any]] = response.json()

    for model_name, model_results in results.items():
        click.echo(f"Model: {model_name}")
        for key, value in model_results.items():
            click.echo(key)
            click.echo(json.dumps(value, indent=4))
