# Sucream

## > 프로젝트 Front-end/Back-end 소개

- 한정판 거래 플랫폼인 [Kream](https://kream.co.kr/) 클론 프로젝트
- 개발적인 부분에만 집중하기 위해 디자인/기획 부분을 클론했습니다.
- 개발은 초기 세팅부터 전부 직접 구현했으며, 아래 데모 영상에서 보이는 부분은 모두 직접 개발한 백앤드와 연결하여 실제 서비스 수준으로 개발한 것입니다.

### 개발 인원 및 기간

- 개발기간 : 2021/01/10 ~ 2022/01/21
- 개발 인원 : 프론트엔드 3명, 백엔드 2명
- [백엔드 github 링크](https://github.com/wecode-bootcamp-korea/28-2nd-Sucream-backend.git)

### 데모 영상(이미지 클릭)
<br>

[<img width=400px alt="Scuream_스크린샷" src="https://user-images.githubusercontent.com/65281583/150671430-10f1ffe4-7b49-4ba5-aac0-25334f5f6159.png"> <br>
Web Page 데모 영상](https://youtu.be/zBTthX1EFLk)

[<img width=400px alt="Sucream_Server_스크린샷" src=""> <br>
Web Server 응답 영상](https://youtu.be/)

<br>

## 적용 기술 및 구현 기능

### 적용 기술

> - Back-End :
>>  - Python
>>  - Django web framework
>>  - MySQL
>>  - JWT
> - Common :
>>  - RESTful API
>>  - httpie

### 협업 도구

> - github
> - slack 
> - notion
> - trello

#### Database Modeling

- ERD
- <img width="560" alt="TERAROSA_ERD" src="https://user-images.githubusercontent.com/65281583/150671830-d78b931d-6357-4342-bbcf-bbc8e4c21546.png">

### 구현 기능

#### 서비스 접속 유저 관리

1. 카카오 소셜 로그인 API를 사용한 웹 사이트 로그인 API 구현
2. 유저 point 조회 API를 통한 유저의 point정보 navigation bar에 표시

#### 제품 리스트 조회

1. 메인 페이지 랜딩 시, API를 통해 등록된 전체 제품의 정보 호출.<br>
(화면 좌측 필터링 항목 함께 조회)
2. 필터링(브랜드, 사이즈)와 정렬 기준에 따른 페이지 상의 제품 리스트 재 호출
3. 리스트 상의 제품링크를 통한 제품 디테일 페이지 연결,<br>
디테일 페이지에서 상품의 상세 정보 및 거래관련 정보 호출.

#### 제품 입찰 및 판매,구매 (@제품의 디테일 페이지)

1. 제품에 해당하는 사이즈별로 등록된 입찰가격 표현 (판매, 구매 별도)
2. 거래 완료된 이력들에 대해 그래프로 시세 표현
3. 등록된 입찰정보를 통해 제품 거래 시, 선택한 사이즈 정보에 맞게 입찰 정보 매칭
입찰한 유저와 거래에 응한 유저 정보사이에서 포인트 이전 발생.
4. 신규 입찰 등록 시, 제품, 사이즈, 입찰가격에 맞게 신규 입찰 정보 생성

<br>

## Reference

- 이 프로젝트는 [Kream](https://kream.co.kr/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
  (사용 이미지는 대부분 저작권Free를 사용했으나 2차 배포에 대한 사용 권한은 없습니다.)