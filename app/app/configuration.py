import logging
import os

from flask import url_for, current_app
from kubernetes import config


def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    app = current_app
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


def load_kubernetes_config():
    _flask_env = os.environ.get("FLASK_ENV")
    logging.info(_flask_env)
    if _flask_env == 'development':
        config.load_kube_config()
    else:
        config.load_incluster_config()


def set_logging_level():
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger('deployment').setLevel(logging.INFO)
    logging.getLogger('event').setLevel(logging.INFO)
    logging.getLogger('ingress').setLevel(logging.INFO)
    logging.getLogger('namespace').setLevel(logging.INFO)
    logging.getLogger('pod').setLevel(logging.INFO)
    logging.getLogger('replicaset').setLevel(logging.INFO)
    logging.getLogger('service').setLevel(logging.INFO)
    logging.debug("logging level set")
