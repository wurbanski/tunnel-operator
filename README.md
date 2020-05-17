# tunnel-operator

Simple kubernetes operator creating SSH tunnels for services

## Why

Because sometimes you need a quick-and-a-little-dirty way to expose your services.

## How it works

For every service that exists and contains an annotation `tunnel-operator.wurbanski.me/open-tunnel: yes`, tunnel-operator will create a ssh tunnel from your service, first specified port to your remote host, same port number.
The tunnel is then created as a scale-1 deployment in `tunnel` namespace.

## How to use it

0. Setup SSH server and user on remote host
1. Apply manifests from `manifests/` directory of the repo (`namespace.yaml`, `serviceaccount.yaml`, `rbac.yaml`, `deployment.yaml`)
2. Create configuration (configmap and secret), based on `example-config` directory and apply it.
3. Add `tunnel-operator.wurbanski.me/open-tunnel: yes` annotation to your service that you want to forward.

Further tuning through annotations:

* `tunnel-operator.wurbanski.me/forward-port: "<number>"` - use specified port to forward from service. The same port will be chosen on the remote, unless overriden as below.
* `tunnel-operator.wurbanski.me/remote-port: "<number>` - use specified remote port (still prefixed with 127.0.0.1 on remote host)

## Is it safe?

It depends on configuration of your SSH server mostly. I take no responsibilities for any damage that using this operator might cause. Sorry!

Some good resources with configuration guidelines include:

* [secure secure shell](https://stribika.github.io/2015/01/04/secure-secure-shell.html)
* [mozilla infosec for openssh](https://infosec.mozilla.org/guidelines/openssh)
* [ssh-audit](https://github.com/arthepsy/ssh-audit)

## Future:

[ ] jsonnet files for manifests
[ ] automation of registering endpoints on the server
[ ] tests?

