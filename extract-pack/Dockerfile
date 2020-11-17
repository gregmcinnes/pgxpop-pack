FROM python:3.8.6

RUN git clone https://github.com/pbilling/pgxpop-pack.git

RUN pip install -r pgxpop-pack/extract-pack/requirements.txt

RUN echo -e 'python3 /pgxpop-pack/extract-pack/main.py' > \
    /usr/bin/pgx-extract && \
    chmod +x /usr/bin/pgx-extract