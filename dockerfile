FROM python:3.8
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y git cmake wget nano

RUN git config --global --add safe.directory '*'

RUN wget https://github.com/libgit2/libgit2/releases/download/v1.1.0/libgit2-1.1.0.tar.gz &&\
  tar xzf libgit2-1.1.0.tar.gz && \
  cd libgit2-1.1.0/ && \
  cmake . && \
  make && \
  make install

RUN pip install --upgrade pip

RUN pip --no-cache-dir install --upgrade \
    pip \
    docopt \
    pandas \
    requests \
    pygit2 \
    tqdm \
    p_tqdm \
    fasttext \
    transformers \
    matplotlib \
    flair \
    segtok

# COPY src/docs/THIRD_PARTY_NOTICE.md .

WORKDIR "/home/dev"

CMD ["bash"]
