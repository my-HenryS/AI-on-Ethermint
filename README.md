## **AI on Blockchain**

### Overview

The project provides a distributed hand writing recognition serivce running on Ethermint.

With the client node processes user's image with the first few layers of CNN, the service node then continue analyzes the processed data with the rest layers (full connnected layers).

![demo_result](https://github.com/my-HenryS/AI-on-Ethermint/blob/master/bean-hwr/static/images/Model_Illustration.png)

It aims at protecting data privacy since service node cannot get access to the original data while the customer cannot obtain the whole analyze model.

The result looks like this. You can trace the service process on the console of right side and receive the result.

![demo_result](https://github.com/my-HenryS/AI-on-Ethermint/blob/master/bean-hwr/static/images/demo_result.png)



### Deployment

1. Environment

   OS: **Linux / Mac OS / Windows** (under experiment)

   Docker: The entire project is wrapped in **Docker** containers.

2. Deploy

   - Build Docker Images

     In directory named "AI on Ethermint"

     ```shell
     cd ethermint    #create ethermint image
     docker build -f Dockerfile -t bianjie_ethermint ./

     cd ../bean-hwr-server #create server image
     docker build -f docker/Dockerfile -t bean-hwr-server ./

     cd ../bean-hwr #create client image
     docker build -f docker/Dockerfile -t bean-hwr ./

     ```

   - Run the project!

     ```shell
     cd ..
     bash run.sh
     ```

     Then you will see echo message

     ```
     service running on http://localhost:8080
     ```

     And the service is successfully running on http://localhsot:8080

     You can type ***"docker ps"*** and then you shall see five containers:

     ```shell
     AI on Ethermint Anonymous$ docker ps
     CONTAINER ID        IMAGE                    COMMAND                  CREATED             STATUS              PORTS                                            NAMES
     95d5667032d3        bean-hwr                 "bash -c 'python i..."   About an hour ago   Up 2 seconds        0.0.0.0:5001->5001/tcp, 0.0.0.0:8080->8080/tcp   bean-hwr
     77f8103b2acb        postgres:9.6.2           "docker-entrypoint..."   About an hour ago   Up 2 seconds        0.0.0.0:5437->5432/tcp                           docker_beanhwr-postgresql_1
     6344c61d70bd        bean-hwr-server          "bash -c 'python e..."   About an hour ago   Up 4 seconds                                                         bean-hwr-server
     c348371c568b        bianjie_ethermint        "bash -c 'ethermin..."   About an hour ago   Up 4 seconds        0.0.0.0:8545->8545/tcp, 46658/tcp                ethermint-service
     0419998ff14c        adrianbrink/tendermint   "bash -c 'tendermi..."   About an hour ago   Up 5 seconds        46656-46657/tcp                                  tendermint-service
     ```

   - Terminate the service

     ```bash
     bash terminate.sh
     ```

   - Enjoy!