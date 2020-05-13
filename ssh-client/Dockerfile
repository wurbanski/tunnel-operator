FROM alpine:3.11.6

RUN apk update && apk add --no-cache openssh-client gettext

COPY entrypoint.sh ssh_config.tmpl /etc/ssh/

ENTRYPOINT [ "/etc/ssh/entrypoint.sh" ]