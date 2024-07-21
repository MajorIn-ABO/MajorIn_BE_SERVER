# Major:IN >> BE_SERVER
### 사회적 교류 지원을 위한 멘토링 제공 학과 중심 커뮤니티 플랫폼
대학교 중심이 아닌 학과 중심의 정보 공유 및 네트워킹 창구를 만들어 유사 학과 전공생들 간의 교류를 활성화하는 웹서비스입니다.

### 👾기능소개👾
1. OCR 기반 자체 개발 학생증 인식 모델 활용
2. 학과 중심의 커뮤니티 게시판, 스터디 게시판
3. 학과간 중고거래 활성화
4. 취업 정보 공유
5. '챗봇' 기반 심리 상담 후, 맞춤형 멘토링 추천
   
<br>

## Backend 아키텍쳐

<img width="816" alt="BACKEND-architecture" src="https://github.com/user-attachments/assets/ccb94fc4-5f64-4422-ab38-acc594060fb4">

## ERD 설계

![ERD](https://github.com/user-attachments/assets/fed349dd-2530-4c4d-8d61-d3ba94020695)

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
