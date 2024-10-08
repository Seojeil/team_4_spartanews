# SpartaNews
 - GeekNews와 유사한 페이지를 만드는 실습을 통한 협엽 연습
 - 기능개발 자체보다 협업과 회의에 집중을 했음
## ERD/WireFrame
 - ![와이어프레임](wiredrame.JPG)
 - ![ERD](ERD.JPG)

## API specification
### api/accounts/
 - POST: 회원가입을 할 수 있습니다. (윤찬민)
 - DELETE: 해당 유저의 비활성화를 진행 합니다. (김경민)

### api/accounts/verifyemail/
- POST: Signup을 시도하는 유저의 이메일과 인증 코드를 입력 확인 후 사용자를 활성화 시킬수 있습니다. (김경민)

### api/accounts/`<int:account_id>`/
 - GET: 유저의 프로필 페이지의 정보를 조회 할 수 있습니다. (김경민)
 - POST: 로그인한 사용자는 다른 사용자를 팔로우할 수 있습니다. (서재일)
 - PUT: 유저의 프로필을 수정합니다. (김경민)

### api/accounts/password/
- PUT: 유저 본인의 비밀번호를 수정할 수 있습니다. (김경민) 

### api/accounts/login/
 - POST: 사용자의 유저 인증을 하여 로그인을 진행합니다. (김경민)

### api/accounts/logout/
 - POST: 유저 인증된 사용자를 로그아웃합니다. (윤찬민)

### api/articles/
 - GET: 기사 전체를 조회할 수 있습니다. (윤찬민, 서재일, 김경민)
 - POST: 로그인한 사용자는 기사를 작성할 수 있습니다. (서재일, 윤찬민)

### api/articles/`<int:article_pk>`/
 - GET: 특정 기사를 조회할 수 있습니다. (서재일)
 - POST: 로그인한 사용자는 기사를 추천/비추천 할 수 있습니다. (서재일)
 - PUT: 기사의 작성자는 기사를 수정할 수 있습니다. (서재일)
 - DELETE: 기사의 작성자는 기사를 삭제할 수 있습니다. (서재일)

### api/articles/`<int:article_pk>`/comments/
 - POST: 특정 기사의 댓글을 작성할 수 있습니다. (김경민)

### api/articles/comments/`<int:comment_pk>`/
 - POST: 로그인한 유저는 특정 댓글을 추천 또는 비추천 할 수 있습니다. (김경민)
 - PUT: 본인이 올린 댓글을 수정할 수 있습니다. (김경민)
 - DELETE: 본인이 올린 댓글을 삭제할 수 있습니다. (김경민)

## Troubleshooting
 - 장고패키지가 제대로 로드가 안되는것을 확인
    - git clone 및 기본 세팅을 진행한 후 파이썬 코드를 확인하던중 장고 패키지가 제대로 import되지 않는것을 인지
    - 원인 파악을 위해서 git clone 및 기본 세팅을 재반복함
    - 문제가 해결이 되지않아 디렉토리를 확인
    - settings.py에 Django Secret_key가 다른 config.py에서 import된 것을 확인
    - config.py를 새로 생성해주고 새로운 시크릿 키를 생성하여 settings.py에 전달 후 해결 

## Version
annotated-types==0.7.0  
anyio==4.4.0  
asgiref==3.8.1  
async-timeout==4.0.3  
attrs==24.2.0  
autopep8==2.3.1  
certifi==2024.7.4  
charset-normalizer==3.3.2  
colorama==0.4.6  
distro==1.9.0  
Django==4.2  
django-extensions==3.2.3  
django-redis==5.4.0  
django-seed==0.3.1  
django-silk==5.2.0  
djangorestframework==3.15.2  
djangorestframework-simplejwt==5.3.1  
drf-spectacular==0.27.2  
exceptiongroup==1.2.2  
Faker==28.0.0  
gprof2dot==2024.6.6  
h11==0.14.0  
httpcore==1.0.5  
httpx==0.27.2  
idna==3.8  
inflection==0.5.1  
jiter==0.5.0  
jsonschema==4.23.0  
jsonschema-specifications==2023.12.1  
openai==1.43.0  
pillow==10.4.0  
psycopg2==2.9.9  
pycodestyle==2.12.1  
pydantic==2.8.2  
pydantic_core==2.20.1  
PyJWT==2.9.0  
python-dateutil==2.9.0.post0  
PyYAML==6.0.2  
redis==5.0.8  
referencing==0.35.1  
requests==2.32.3  
rpds-py==0.20.0  
six==1.16.0  
sniffio==1.3.1  
sqlparse==0.5.1  
tomli==2.0.1  
toposort==1.10  
tqdm==4.66.5  
typing_extensions==4.12.2  
tzdata==2024.1  
uritemplate==4.1.1  
urllib3==2.2.2  