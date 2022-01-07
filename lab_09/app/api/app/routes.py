from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.app import Application


def setup_routes(app: 'Application'):
    from app.api.stats.routes import setup_routes as queries_setup_routes
    from app.api.workflow.routes import setup_routes as workflow_setup_routes

    queries_setup_routes(app)
    workflow_setup_routes(app)
