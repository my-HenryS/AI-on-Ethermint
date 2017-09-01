FROM adrianbrink/ethermint

RUN  mkdir -p /temp/setup/keystore
COPY ./genesis.json /temp/setup
COPY ./keystore /temp/setup/keystore
RUN ethermint --datadir /ethermint init /temp/setup/genesis.json && cp -r /temp/setup/keystore /ethermint