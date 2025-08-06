# SSD 프로젝트 by Team AllClear
### 참고사항
- tdd채점 시 ssd_controller의 commit은 feature/controller_read, feature/controller_write을 참고 부탁드립니다.
```
main으로 rebase하는 rule을 사용했는데 그 과정에서 conflict resolve가 불가능한 상태로 꼬여, feature/controller_read2, feature/controller_write2 브랜치를 새로 만들어 작업을 이어갔습니다.
```
### 개요
```
SSD 제품을 테스트 할수있는Test Shell 을 제작
- 실제HW가아닌, SW로가상으로구현한다.
- Test Shell 프로그램을 제작하여 SSD 동작을 테스트 할 수 있다.
- 다양한Test Script를 제작한다.
```
### 구성
```
1. SSD
 - HW 대신, Software로 구현한다.
2. Test Shell
 - SSD를 테스트하는프로그램
3. Test Script
 - Test Shell 안에서 구현되는 SSD 테스트 코드
```
### 설계
<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/7bac7b22-56cd-402e-a3f5-5ef6d7325e10" />

### 역할 분담
- 팀장: 장진섭</br>
- 팀원: 이규홍, 임소현, 최준식, 이휘은, 박성일

### [백로그 문서](backlog.md)
