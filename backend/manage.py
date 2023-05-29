import click

from settings import config


@click.group()
def main_group():
    pass


@click.group("site")
def site_group():
    """Work with server"""


@site_group.command()
@click.option(
    '-h', '--host',
    default=config.HOST,
    help="IP address or local domain name to run server on")
@click.option(
    '-p', '--port',
    default=config.PORT,
    help="Server port")
@click.option(
    '-l', '--log-level',
    default=config.DEBUG,
    help="Logging level. One of: [critical|error|warning|info|debug|trace]")
def run(host: str = None, port: int = None, log_level: str = None):
    """Run server"""

    import uvicorn

    app_name = 'server:app'

    uvicorn.run(
        app_name,
        host=host,
        port=port,
        log_level=log_level,
        reload=True
    )


main_group.add_command(site_group)


if __name__ == "__main__":
    main_group()
