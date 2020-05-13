FROM python:3.7

COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY ssh-tunnel-operator.py tunnel-deployment.yaml /src/
CMD kopf run /src/ssh-tunnel-operator.py
