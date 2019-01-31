# Magpie

Performance modelling for Distributed Stream Processing Systems (DSPS)
such as [Apache Heron](https://apache.github.io/incubator-heron/) and [Apache
Storm](http://storm.apache.org/).

**NOTE**: Magpie is a prototype project, which is based on Caladrius, itself a 
prototype project that was the result of a 3 month internship with Twitter's 
Real Time Compute Team. It should be considered alpha level software. All 
contributions are welcome, please see the contributing page on the documentation 
website for more details.

## Setup

### Python

Magpie requires Python 3.6, additional Python dependencies are listed in
the Pipfile. Dependencies can be installed using
[pipenv](https://docs.pipenv.org/) by running the following command in the
caladrius root directory:

    $ pipenv install 

Add the `--dev` flag to the above command to install development dependencies.

Magpie should also be added to your `PYTHONPATH`. The best way to do this is
by adding the folder above the Caladrius repo to the `PYTHONPATH` environment
variable using a command like the one below:

    $ export PYTHONPATH=$PYTHONPATH:<path/to/folder/above/magpie>

This line should be added to your `.profile` (or similar) start up script to
preserve this across reboots.

### Graph Database

Magpie requires a [Gremlin
Server](http://tinkerpop.apache.org/docs/current/reference/#gremlin-server)
instance running [TinkerPop](http://tinkerpop.apache.org/) 3.3.2 or higher. 

The reference gremlin sever can be downloaded from 
[here](https://www.apache.org/dyn/closer.lua/tinkerpop/3.3.3/apache-tinkerpop-gremlin-server-3.3.3-bin.zip).

The Gremlin server should have the [Gremlin
Python](http://tinkerpop.apache.org/docs/current/reference/#gremlin-python)
plugin installed:

    $ gremlin-server.sh install org.apache.tinkerpop gremlin-python 3.3.3

Start the server with the gremlin python config (included in the standard
server distribution):

    $ gremlin-server.sh start conf/gremlin-server-modern-py.yaml

*Please note:* The default settings for the Gremlin Server result in an
in-memory TinkerPop Server instance. If graphs need to be persisted to disk
then these settings can be altered in the appropriate configuration file in the
`conf` directory of the Gremlin Server distribution.
    
## Running Magpie

### Configuration

All configuration is done via the `yaml` file provided to the `app.py` script
(see section below). This file defines the models run by the various API
endpoints and any connection details, modelling variables or other
configurations they may require.

An example configuration file with sensible defaults is provided in
`config/main.yaml.example`. You should copy this and edit it with your specific
configurations.

### Starting the API Server

The Magpie API server can be started by running the `server.py` script in the
root directory. This can be run in the appropriate virtual environment using
pipenv (make sure your `python` command points to Python 3):

    $ pipenv run python server.py --config /path/to/config/file

Additional command line arguments are available via:

    $ pipenv run python server.py --help

## Documentation

Documentation for stable releases is hosted on
[ReadTheDocs](http://magpie.readthedocs.io/).

If you want to build the latest documentation then this can be done using
[Sphinx](http://www.sphinx-doc.org/en/master/index.html). Assuming you have
installed the development dependencies above, the docs can be built using the
following commands in the repository root:

    $ pipenv run sphinx-apidoc -f -o docs/source . tests/*
    $ cd docs
    $ pipenv run make html

This will place the constructed html documentation in the `docs/build`
directory.
