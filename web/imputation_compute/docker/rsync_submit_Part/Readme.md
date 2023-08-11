# docker FILE build

```shell
docker build -t solivehong/imputation_server_web --network host .

```


## docker running 
### 设置挂载目录

1. upload 目录 
2. imputation wdl 目录
3. config setting
4. 设置免密登录
5. 
```shell
   ssh-keygen -t rsa
   ssh-copy-id -i /path/to/your_public_key.pub user@server_ip
   ssh -i /path/to/your_private_key user@server_ip
   
```

```shell
docker run -it --rm --network=host -v /home/shupeng/imputation/uploadfiles:/home/shupeng/imputation/uploadfiles -v /disk/project/imputation/warp19/:/disk/project/imputation/warp19/ solivehong/imputation_server_web /bin/bash



```