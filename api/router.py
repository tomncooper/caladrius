# Copyright 2018 Twitter, Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

""" This module contains the methods to load the configured model and client
classes and create routing logic for the magpie API. """

import logging

from typing import List, Dict, Any, Type

from flask import Flask
from flask_restful import Api

from magpie import loader
from magpie.config.keys import ConfKeys
from magpie.graph.gremlin.client import GremlinClient
from magpie.metrics.heron.client import HeronMetricsClient
from magpie.api.model.topology.heron import (
    HeronTopologyModels,
    HeronCurrent,
    HeronProposed,
)
from magpie.api.model.traffic.heron import HeronTraffic, HeronTrafficModels

LOG: logging.Logger = logging.getLogger(__name__)


def create_router(config: Dict[str, Any]) -> Flask:
    """ Creates the Flask router object by first creating all the client and
    model classes defined in the supplied configuration dictionary.

    Arguments:
        config (dict):  The configuration dictionary containing client and
                        model class paths and their associated configurations

    Returns:
        A Flask instance containing the routing logic for the API.
    """

    LOG.info("Creating REST API routing object")

    router: Flask = Flask("magpie")
    api: Api = Api(router)

    # ### GRAPH CLIENT ###

    # TODO: Consider making a copy of this for each model/resource to prevent
    # locking issue if we go multi-threaded
    graph_client: GremlinClient = loader.get_class(config["graph.client"])(
        config["graph.client.config"]
    )

    # ### HERON METRICS CLIENT ###

    # TODO: Consider making a copy of this for each heron model to prevent
    # locking issues if we go multi-threaded
    heron_metrics_client: HeronMetricsClient = loader.get_class(
        config["heron.metrics.client"]
    )(config["heron.metrics.client.config"])

    # ### TRAFFIC MODEL ENDPOINTS ###

    heron_traffic_model_classes: List[Type] = loader.get_model_classes(
        config, "heron", "traffic"
    )

    api.add_resource(
        HeronTrafficModels,
        "/model/traffic/heron/model_info",
        resource_class_kwargs={"model_classes": heron_traffic_model_classes},
    )

    api.add_resource(
        HeronTraffic,
        "/model/traffic/heron",
        resource_class_kwargs={
            "model_classes": heron_traffic_model_classes,
            "model_config": config["heron.traffic.models.config"],
            "metrics_client": heron_metrics_client,
            "graph_client": graph_client,
            "tracker_url": config[ConfKeys.HERON_TRACKER_URL.value],
        },
    )

    # ### TOPOLOGY MODEL ENDPOINTS ###

    heron_topology_model_classes: List[Type] = loader.get_model_classes(
        config, "heron", "topology"
    )

    # ### MODEL INFORMATION ENDPOINT ###

    api.add_resource(
        HeronTopologyModels,
        "/model/topology/heron/model_info",
        resource_class_kwargs={"model_classes": heron_topology_model_classes},
    )

    # ### CURRENT TOPOLOGY MODELS ###

    api.add_resource(
        HeronCurrent,
        "/model/topology/heron/current",
        resource_class_kwargs={
            "model_classes": heron_topology_model_classes,
            "model_config": config["heron.topology.models.config"],
            "metrics_client": heron_metrics_client,
            "graph_client": graph_client,
            "tracker_url": config[ConfKeys.HERON_TRACKER_URL.value],
        },
    )

    # ### PROPOSED TOPOLOGY MODELS ###

    api.add_resource(
        HeronProposed, "/model/topology/heron/proposed/<string:topology_id>"
    )

    LOG.info("REST API router created")

    return router
