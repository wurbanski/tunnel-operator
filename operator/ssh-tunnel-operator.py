import os
import kopf
import kubernetes
import yaml

ann_ns = 'tunnel-operator.wurbanski.me'
ann_filter={f'{ann_ns}/open-tunnel': 'yes'}

@kopf.on.create('', 'v1', 'services', annotations=ann_filter)
def create_tunnel(meta, spec, namespace, logger, **kwargs):

    name = meta['name']
    namespace = meta['namespace']

    default_port = spec['ports'][0]['port']
    forward_port = meta['annotations'].get(f'{ann_ns}/forward-port', default_port)
    remote_port = meta['annotations'].get(f'{ann_ns}/remote-port', default_port)

    path = os.path.join(os.path.dirname(__file__), 'tunnel-deployment.yaml')
    with open(path, 'rt') as tmpl_file:
        tmpl = tmpl_file.read()

    text = tmpl.format(
        name=name,
        namespace=namespace,
        forward_port=forward_port,
        remote_port=remote_port
    )
    data = yaml.safe_load(text)

    kopf.adopt(data)

    api = kubernetes.client.AppsV1Api()
    api.create_namespaced_deployment(
        namespace="tunnel",
        body=data
    )


@kopf.on.update('', 'v1', 'services', annotations=ann_filter)
def update_tunnel(meta, spec, namespace, logger, **kwargs):

    name = meta['name']

    default_port = spec['ports'][0]['port']
    forward_port = meta['annotations'].get(f'{ann_ns}/forward-port', default_port)
    remote_port = meta['annotations'].get(f'{ann_ns}/remote-port', default_port)
    
    deployment_patch = {
        'spec': {
            'template': {
                'spec': {
                    'containers': [
                        {'name': 'tunnel', 
                         'env': [
                             {'name': 'svc', 'value': f'{name}.{namespace}'},
                             {'name': 'remote_port', 'value': str(remote_port) },
                             {'name': 'forward_port', 'value': str(forward_port) }
                         ]
                        }
                    ]
                }
            }
        }
    }

    api = kubernetes.client.AppsV1Api()
    obj = api.patch_namespaced_deployment(f"tunnel-{name}-{namespace}", "tunnel", deployment_patch)