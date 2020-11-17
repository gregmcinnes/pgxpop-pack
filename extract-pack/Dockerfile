FROM python:3.8.6

#RUN git clone https://github.com/pbilling/pgxpop-pack.git
RUN mkdir -p /pgxpop-pack/extract-pack
COPY . /pgxpop-pack/extract-pack/

RUN pip install -r /pgxpop-pack/extract-pack/requirements.txt

RUN echo -e '#!/bin/bash\npython3 /pgxpop-pack/extract-pack/main.py' > \
    /usr/bin/pgx-extract && \
    chmod +x /usr/bin/pgx-extract
