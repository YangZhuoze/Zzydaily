import sae
sae.add_vendor_dir('vendor')

from sae.ext.shell import ShellMiddleware
from app import create_app

app = create_app('production')

application = sae.create_wsgi_app(ShellMiddleware(app))