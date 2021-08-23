FROM ghcr.io/pmem/pmemkv:ubuntu-20.10-latest

USER root

RUN apt update && \
	DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
	libhwloc-dev \
	libgflags-dev \
	cmake-curses-gui \
	ccache \
 && rm -rf /var/lib/apt/lists/*

