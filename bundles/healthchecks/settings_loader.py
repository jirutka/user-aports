import os
import sys
from importlib import util as importutil

HC_SETTINGS = os.environ.get('HC_SETTINGS', '/etc/healthchecks/settings.py')


def load_python_source(path, module_name):
    spec = importutil.spec_from_file_location(module_name, path)
    mod = importutil.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if os.path.exists(HC_SETTINGS):
    local_settings = load_python_source(HC_SETTINGS, 'local_settings')

    # Emulate "from local_settings import *".
    globals().update({ k: v
                       for (k, v) in local_settings.__dict__.items()
                       if not k.startswith('_') })
else:
    warnings.warn("%s not found, using defaults" % HC_SETTINGS)
    from hc.settings import *
