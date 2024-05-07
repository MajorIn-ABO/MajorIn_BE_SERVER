# MajorIn_BE_SERVER

## 시작 가이드
```
cd Desktop

chmod 400 ./[key-name].pem

ssh -i [key-name].pem ubuntu@[ip]

source majorin/bin/activate

cd MajorIn_BE/

gunicorn --bind 0.0.0.0:8000 majorinBE.wsgi:application

http://[ip]:8000/

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