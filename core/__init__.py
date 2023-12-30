from .allinone.views import app as allinone_view
from .app import application

application.register_blueprint(allinone_view, url_prefix="/")
