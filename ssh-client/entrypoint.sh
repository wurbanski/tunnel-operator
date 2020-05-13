#!/bin/sh

export TUNNEL_HOST=${TUNNEL_HOST:-$(cat /config/tunnel_host)}
export TUNNEL_PORT=${TUNNEL_PORT:-$(cat /config/tunnel_port)}
export TUNNEL_USER=${TUNNEL_USER:-$(cat /config/tunnel_user)}

envsubst < /etc/ssh/ssh_config.tmpl > /etc/ssh/ssh_config

exec ssh -N tunnel "$@"