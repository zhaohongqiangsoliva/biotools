<h3 align="center">SubmitMQ</h3>

<div align="center">


[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-RabbitMQ](https://img.shields.io/badge/Made%20with-RabbitMQ-blue)](https://www.rabbitmq.com/)
<br>



</div>

------------------------------------------

> Leverages the distributed nature of RabbitMQ to allow users to submit their code to a master that distributes work to workers. It offloads the responsibility of fault tolerance, distribution and scalabililty to RabbitMQ.

------------------------------------------

<br>

<div align="center">
    <h3>Architecture/Event flow<h3>
</div>

![](./assets/architecture.png)


The project uses the RabbitMQ broker as a messaging queue to store the task generated by the clients, which is shared among wokers.

The clients send the job they want to submit to an exchange, which sends it to an appropriate queue based on the binding key.

<div align="center">
    <h3>Client<h3>
</div>

The client can submit new tasks or view tasks previously submitted. Screenshots:

![](./assets/dashboard.png)

<div align="center"><h5> Dashhboard </h5></div>


![](./assets/history.png)

<div align="center"><h5> View submitted tasks </h5></div>

![](./assets/new_task.png)

<div align="center"><h5> Create new task </h5></div>

![](./assets/task_info.png)

<div align="center"><h5> View details of task</h5></div>

#### Using API endpoints

```
POST /upload/<page_num>: Get details for the submitted tasks

POST /jobs/<job_id>: Get info about a specific task
```

<div align="center">
    <h3>Future work<h3>
</div>

- [ ] Add charts on dashboard
- [ ] Add pagination in frontend
- [ ] Add support for more languages
- [ ] Safe execution of code
- [ ] Add option for batch file upload
- [ ] Notify users when task is completed
- [ ] Multiple views for different users
- [ ] Add logging


<div align="center">
    <h3>Running the project locally<h3>
</div>

Setup the RabbitMQ server:
#### Using docker

```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.8
```

Run the flask server for the client using 
```
python3 client/app.py
```

Running the worker nodes:

```
$ cd workers/

$ docker-compose up --scale python=2 --scale cpp=3
```

![](./assets/start.png)

<div align="center"><h5> Scaling the services using docker-compose</h5></div>



Since the project only supports pymongo and uses mongo atlas to store data, you need to define an .env file (in the folders client/, workers/python/ and workers/cpp/) with the following two parameters:

```
RABBITMQ_SERVER: host running the rabbitMQ broker

MONGO_URL: Where the data is to be stored.
```



#### ...but why would I use this?

This isn't a completed project. It's far from done. But the possibilities in which this project could progress are endless - this just serves as a base to build upon a specific application.

The two options that I had in mind while building the project were:

- Use it as a submission system for programming contests (something like codechef has). You can collect details as required by the application and use those to create charts to display on the dashboard. (Just make sure to ensure only executing safe code).

- Training ml/dl models with different hyperparameters in parallel across various devices if you have access to multiple idle machines (like access to a computer lab). It would make it convenient and fast. Further features that could be added in this include notifications when a task is done, comparision among the various results etc..