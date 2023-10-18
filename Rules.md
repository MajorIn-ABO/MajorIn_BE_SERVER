### Commit Rule
```
__Type__ __FileName__ : __Description__
```
- Type 리스트
  : 모든 타입의 첫 글자는 대문자로 작성
    - Add : 새로운 파일이나 기능을 추가
    - Update : 기존에 있던 파일을 수정
    - Remove : 특정 파일을 삭제
    - Design : CSS 등 사용자 UI 디자인을 변경
    - Init : 초기 생성
- FileName : 추가,수정,삭제한 파일의 이름을 작성
    - 폴더 이름을 수정하거나 추가한 경우에도 동일하게 폴더 이름을 작성
- Description : 해당 커밋 내용을 간단하게 요약하여 작성


---

### PR Rule
- Issue 작성 시, Assignee은 본인 프로필을 지정. 알맞은 Label을 지정. 
- PR 작성 시, 적절한 Assignee와 Label을 지정.
  
#### Title
```
[TYPE] TITLE
```
- TYPE
    - DEV : 일반적인 개발 사항
    - FIX : 기존 개발에서 버그 내용을 해결하였을 경우
    - REF : 리팩토링
    - DOC : 문서에 관련된 사항
 
- TITLE
  : PR 내용을 간단한 제목으로 표현. 가능하면 issue title과 동일하게 작성

```
[DEV] FE 메인 페이지 UI 구현
```

####  Content
```markdown
## Summary
PR 간단하게 요약하여 작성
ex. 메인 페이지 UI를 구현하였습니다.

```
```
## Description
- PR의 내용을 상세하게 작성
- ui 구현시 스크린샷 첨부, 오류 수정시 파일명과 함께 오류 해결 내용 상세히 작성
```

---

### Branch Rule
```
TYPE/BRANCH_NAME
```
- TYPE
  : Issue의 타입과 동일하게 선택
    - dev : 일반적인 개발 사항
    - fix : 기존 개발에서 버그 내용을 해결하였을 경우
    - ref : 리팩토링
    - doc : 문서에 관련된 사항
- BRANCH_NAME
  : 해당하는 Issue의 Title을 적절히 변형

#### Branch Example
```
dev/main-ui
```
```
docs/login-api
