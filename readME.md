# Docker

## 도커를 배워야 하는 이유?

과거에는 애플리케이션 개발은 프로그래밍과 테스트 스킬을 가진 애플리케이션 엔진니어가
환경구축은 네트워크나 하드웨어를 잘아는 인프라 엔진니어가 담당했습니다.

그런데 데이터센터나 서버실을 두고 하는 온프레미스 방식에서 가상의 서버를 여러 대 띄우는 클라우드 방식으로 변화되었습니다.

이런 분산환경에서는 인프라 엔지니어가 수동으로 관리하는 대신 자동화된 툴을 사용해 오케스트레이션 합니다.
따라서 인프라 엔지니어도 자동화를 위해 코드를 작성하는 능력이 필요하게되었습니다.

#### IT Infrastructure?
`IT 인프라`란 애플리케이션을 가동시키기 위한 필요한 하드웨어, OS , 미들웨어, 네트워크 등 시스템의 기반을 말합니다.

## STEP 2. Docker

서비스 운영 환경을 묶어서 손쉽게 배포하고 실행하는 경량 컨테이너 기술로 인프라 구축을 손쉽게 할 수 있는 도구입니다.

### 도커설치

```
# 도커 설치
$ curl -fsSL https://get.docker.com/ | sudo sh

# 도커 설치 확인
$ sudo docker version

# 도커 방화벽(ufw) 설정
$ sudo ufw allow 4243/tcp
```

### 권한 설정

```
# 도커라는 이름의 그룹 설정
$ sudo groupadd docker

# 도커그룹에 유저 등록 
$ sudo gpasswd -a ubuntu docker

#cf) gpasswd -a 는 그룹에 해당 멤버를 추가하는 명령어입니다.

# 재시작
$ sudo service docker restart
```

### 도커 이미지 (Image) 이해하기
`이미지`는 서비스 운영에 필요한 서버 프로그램, 소스 코드, 컴파일된 실행 파일을 묶은 형태

`컨테이너`는 이미지를 실행한 상태

이미지 = 실행파일 /  컨테이너 = 프로세스

=> apt-get install 라이브러리와 같이 해당 내용을 docker pull 라이브러리를 통해 받아올 수 있습니다.

```
# 다운 받았던 이미지 목록 확인
$ docker images

# 해당 이미지[] 다운로드
$ docker pull [ubuntu]
```

### docker 기초 실습!
```
# 도커로 이미지 쉘 접근
$ docker run -i -t ubuntu /bin/bash

# 도커로 접근한 쉘 나가기
$ exit 

# 컨테이너 목록 확인하기
$ docker ps -a

# 컨테이너[] 재시작 하기
$ docker restart [e2af61348652]

# 재시작한 컨테이너[] 접근하기
$ docker attach [e2af61348652]

# git download
$ apt-get update
$ apt-get install -y git
$ git --version

# 컨테이너[] 변경사항 확인하기
$ docker diff [e2af61348652]

# 해당 작업 컨테이너 이미지 저장
$ docker commit [eb0b81046522] ubuntu:git

# 저장된 이미지 확인
sudo docker images | grep git

# 저장된 이미지로 컨테이너 시작
$ docker run -i -t ubuntu:git /bin/bash

# 컨테이너[] 삭제
$ docker rm [e2af61348652]

cf) 컨테이너 모두삭제
$ docker rm `docker ps -a -q`

# 이미지[] 삭제
$ docker rmi [ubuntu:git]

# 이미지 모두 삭제
$ docker rmi `docker images -a -q`
```

### docker-compose

[참고 url](https://soyoung-new-challenge.tistory.com/73)

```
# 도커 컴포즈 버전 설치
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 도커 컴포즈에 권한 설정
$ sudo chmod +x /usr/local/bin/docker-compose

# 심볼릭 링크 설정 -> path오류 방지 
$ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 설치 확인 (버전확인)
$ docker-compose -version 

```