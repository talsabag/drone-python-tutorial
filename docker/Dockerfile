FROM josebarn/python-2.7-base:latest

WORKDIR /app
COPY . /app
RUN virtualenv /env
RUN /env/bin/pip install -r requirements.txt
RUN /env/bin/pip install --upgrade pip setuptools wheel
RUN /env/bin/pip wheel -r requirements.txt --wheel-dir=wheeldir --find-links=wheeldir
RUN /env/bin/pip wheel -r test-requirements.txt --wheel-dir=wheeldir --find-links=wheeldir
RUN /env/bin/pip install --use-wheel --no-index --find-links=wheeldir -r requirements.txt
RUN /env/bin/pip install --use-wheel --no-index --find-links=wheeldir -r test-requirements.txt
RUN /env/bin/python setup.py sdist bdist
RUN /env/bin/python setup.py install

ENV PATH $PATH:/env/bin/

EXPOSE 5000
CMD simple-service
