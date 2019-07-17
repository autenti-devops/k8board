from datetime import datetime

from flask import Blueprint, render_template, Response, request, redirect, url_for

from .deployment.service import get_my_deployments, get_my_deployment
from .event.service import get_my_events
from .ingress.service import get_my_ingresses, get_my_ingress
from .namespace.service import get_namespaces_names
from .pod.service import get_my_pod, get_pod_logs, delete_namespace_pod
from .service.service import get_my_services, get_my_service

bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    _namespaces = get_namespaces_names()
    return render_template('index.html', namespaces=_namespaces)


@bp.route('/namespace/<namespace_name>')
def namespace(namespace_name):
    return render_template('namespace.html',
                           deployments=get_my_deployments(namespace_name),
                           services=get_my_services(namespace_name),
                           ingresses=get_my_ingresses(namespace_name),
                           namespace_name=namespace_name,
                           events=get_my_events(namespace_name))


@bp.route('/namespace/<namespace_name>/deployment/<deployment_name>')
def deployment(namespace_name, deployment_name):
    return render_template('deployment.html',
                           namespace_name=namespace_name,
                           deployment=get_my_deployment(namespace_name, deployment_name))


@bp.route('/namespace/<namespace_name>/pod/<pod_name>', methods=['GET', 'POST'])
def pod(namespace_name, pod_name):
    if request.method == 'GET':
        return render_template('pod.html',
                               namespace_name=namespace_name,
                               pod=get_my_pod(namespace_name, pod_name))
    else:
        delete_namespace_pod(namespace_name, pod_name)
        return redirect(url_for('home.namespace',
                                namespace_name=namespace_name))


@bp.route('/namespace/<namespace_name>/service/<service_name>')
def service(namespace_name, service_name):
    return render_template('service.html',
                           namespace_name=namespace_name,
                           service=get_my_service(namespace_name, service_name))


@bp.route('/namespace/<namespace_name>/ingress/<ingress_name>')
def ingress(namespace_name, ingress_name):
    return render_template('ingress.html',
                           namespace_name=namespace_name,
                           ingress=get_my_ingress(namespace_name, ingress_name))


@bp.route('/namespace/<namespace_name>/pod/<pod_name>/container/<container_name>')
def logs(namespace_name, pod_name, container_name):
    _log = get_pod_logs(namespace_name, pod_name, container_name)
    filename = str(
        "%s-%s-%s-%s.log" % (datetime.now().strftime('%Y%m%d%H%M%S'), namespace_name, pod_name, container_name))
    return Response(_log,
                    mimetype='text/plain',
                    headers={"Content-disposition": "attachment; filename=%s" % filename})
