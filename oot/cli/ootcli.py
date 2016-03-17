__author__ = 'tardis'
import click
import sys
from dalek import config
from oot import DEFAULT_CONFIG
import jsonpickle

sys.path.append("/home/xiaoxubeii/Workspace/PycharmProjects/oot")
from oot.resource.server import Server
from oot.resource.cluster import Cluster


@click.group()
def cli():
    pass


@cli.command('server-list')
def list_server():
    s = Server()
    click.echo(jsonpickle.encode(s.list()))


@cli.command('server-get')
@click.argument('id')
def get_server(id):
    s = Server()
    click.echo(jsonpickle.encode(s.get(id)))


@cli.command('server-delete')
@click.argument('id')
def get_server(id):
    s = Server()
    click.echo(jsonpickle.encode(s.delete(id)))


@cli.command('server-register')
@click.argument('server')
def register_server(server):
    server = jsonpickle.decode(server)
    s = Server()
    s.register(server)


@cli.command('server-update')
@click.argument('server')
def register_server(server):
    server = jsonpickle.decode(server)
    s = Server()
    s.update(server)


@cli.command('cluster-get')
@click.argument('id')
def get_cluster(id):
    c = Cluster()
    click.echo(jsonpickle.encode(c.get(id)))


@cli.command('cluster-create')
@click.argument('cluster')
def create_cluster(cluster):
    cluster = jsonpickle.decode(cluster)
    c = Cluster()
    c.create(cluster)


@cli.command('cluster-list')
def list_cluster():
    c = Cluster()
    click.echo(jsonpickle.encode(c.list()))


@cli.command('cluster-delete')
@click.argument('id')
def delete_cluster(id):
    c = Cluster()
    c.delete(id)


@cli.command('cluster-update')
@click.argument('cluster')
def update_cluster(cluster):
    c = Cluster()
    c.update(jsonpickle.decode(cluster))


if __name__ == '__main__':
    config.parse_args([], default_config_files=[DEFAULT_CONFIG])
    cli()
