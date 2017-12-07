FROM sd2e/base:ubuntu16

COPY nciplot-master/ nciplot-master

RUN apt-get update && \
    apt-get install -y gfortran make python3 python3-pip && \
    pip3 install pandas numpy && \
    rm -rf /var/lib/apt/lists/* && \
    cd /nciplot-master/src && \
    make && \
    rm -rf /var/lib/apt/lists/*

COPY nci.py /usr/local/bin
COPY data_prep_nci_integrations.py /usr/local/bin
COPY run-nciplot /usr/local/bin

#RUN cd /usr/local/bin && \
#    chmod a+x run-nciplot data_prep_nci_integrations.py nci.py