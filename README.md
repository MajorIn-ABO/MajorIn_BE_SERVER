# MajorIn_BE_SERVER

## Backend 아키텍쳐

<img width="408" alt="backend-아키텍쳐" src="https://github.com/user-attachments/assets/0f809fa1-9331-45ed-bf9d-97a0bfc99b5a">

## 시작 가이드
```
cd Desktop

chmod 400 ./[key-name].pem

ssh -i [key-name].pem ubuntu@[ip]

source majorin/bin/activate

cd MajorIn_BE/

gunicorn --bind 0.0.0.0:8000 majorinBE.wsgi:application

http://[ip]:80/

```

## gunicorn 관련
```
재시작
> sudo systemctl restart gunicorn

상태 확인
> systemctl status gunicorn

서비스 중지
> sudo systemctl stop gunicorn.service

pid 확인
> ps ax|grep gunicorn

종료
> kill -9 <pid>

```

## NGINX 관련
```
재시작
> sudo systemctl restart nginx

상태 확인
> systemctl status nginx.service

종료
> sudo systemctl stop nginx

로그 확인
> sudo vi /var/log/nginx/error.log

```

## DB 접속
```
mysql -u root -p 

USE majorin
```

## majorin 링크

[majorin site url](http://majorin.s3-website-ap-southeast-2.amazonaws.com/)
