# define the liboqs tag to be used
ARG LIBOQS_TAG=0.10.0

# define the liboqs-python tag to be used
ARG LIBOQS_PYTHON_TAG=0.10.0

FROM python:bookworm

# Install dependencies
RUN apt-get -y update && \
    apt-get install -y build-essential git cmake libssl-dev wget unzip python3 python3-venv pip


# Enable a normal user
RUN useradd -m -c "Open Quantum Safe" oqs
# USER oqs
WORKDIR /home/oqs

# Get liboqs current version
RUN git clone --depth 1 --branch ${LIBOQS_TAG} https://github.com/open-quantum-safe/liboqs

# Install liboqs
RUN cmake -S liboqs -B liboqs/build -DBUILD_SHARED_LIBS=ON
RUN cmake --build liboqs/build --parallel 4
RUN cmake --build liboqs/build --target install

# Get liboqs-python
RUN git clone --depth 1 --branch ${LIBOQS_PYTHON_TAG} https://github.com/open-quantum-safe/liboqs-python.git

COPY ./json-server-httpd-reverse-proxy-curl/json-server/db.json .
COPY ./jwt-post-quantum ./jwtpostquantum
COPY ./json-server-httpd-reverse-proxy-curl/json-server/server.py .
COPY ./json-server-httpd-reverse-proxy-curl/json-server/requirements.txt .

# Install liboqs-python
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
ENV PYTHONPATH=$PYTHONPATH:/home/oqs/liboqs-python

# Create a Python 3 virtual environment
RUN python3 -m venv ./venv
RUN . ./venv/bin/activate
RUN pip install -r requirements.txt 

# Install liboqs-python
RUN pip install ./liboqs-python 

CMD ["python", "server.py"]