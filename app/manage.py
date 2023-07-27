#!/usr/bin/env python
import click
import uvicorn
from settings import config


@click.group()
def main_group():
    pass


@click.group("site")
def site_group():
    """Work with server"""


@site_group.command()
@click.option(
    "-h",
    "--host",
    default=config.HOST,
    help="IP address or local domain name to run server on",
)
@click.option("-p", "--port", default=config.PORT, help="Server port")
@click.option(
    "-l",
    "--log-level",
    default=config.DEBUG,
    help="Logging level. One of: [critical|error|warning|info|debug|trace]",
)
def run(
    host: str = "0.0.0.0",
    port: int = 8000,
    log_level: str = "info",
):
    """Run server"""

    app_name = "server:app"

    uvicorn.run(
        app_name, host=host, port=port, log_level=log_level, reload=True
    )


main_group.add_command(site_group)


if __name__ == "__main__":
    main_group()
