import os
import click
from app.app import setup_app
from aiohttp.web import run_app


@click.command()
@click.option('--service', default='api', help='Choose service to run')
def main(service: str) -> None:
    cfg_path = os.path.join(os.path.dirname(__file__), 'config.yml')

    choose = {
        'api': lambda: run_app(setup_app(cfg_path)),
    }

    try:
        func = choose[service]
    except KeyError:
        print(f'Bad service was received: {service}')
    else:
        print('Service is okay!')
        func()


if __name__ == "__main__":
    main()
