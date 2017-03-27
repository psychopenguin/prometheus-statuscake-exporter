FROM python:3-onbuild
ENTRYPOINT ["python", "exporter.py"]
EXPOSE 9213
LABEL container.name=psychopenguin/prometheus-statuscake-exporter
