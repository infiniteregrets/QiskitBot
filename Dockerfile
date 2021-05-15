# FROM ubuntu:20.04 AS BASE 
# RUN apt-get update -y \
#     && apt-get install -y --no-install-recommends \
#         autoconf \
#         bison \
#         ca-certificates \
#         flex \
#         g++ \
#         gcc \
#         git \
#         libprotobuf-dev \
#         libnl-route-3-dev \
#         libtool \
#         make \
#         pkg-config \
#         protobuf-compiler       
        
# RUN git clone --recursive https://github.com/google/nsjail.git /nsjail \    
#     && cd /nsjail \
#     && git checkout a9790e14bf88e3fa7c1a543ca5a07f5d8e8c7a5c \
#     && make 

FROM ubuntu:20.10 AS ROOT
#COPY --from=BASE /nsjail/nsjail /usr/bin
RUN apt-get update -y \
    && apt-get install -y\
    libprotobuf-dev \
    libnl-route-3-dev \
    chromium-driver \
    ca-certificates \
    python3.9\
    python3-pip \
    podman \
    runc \ 
    criu 

ARG DEBIAN_FRONTEND='noninteractive'
RUN apt-get install -y iptables-persistent       
      
WORKDIR /qiskitbot
COPY ./ ./ 
RUN pip3 install pipenv 
RUN pipenv install \
    discord \
    beautifulsoup4 \
    requests-html \ 
    arsenic 
CMD ["pipenv", "run", "python3", "."]    