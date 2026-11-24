
# chatlog-cleaner

다국어 채팅 기록을 불러와 정제하고, 전화번호와 이메일 같은 개인정보를 마스킹하는 Python 패키지입니다.

## 1. What it does

`chatlog-cleaner`는 여러 언어가 섞인 채팅 기록을 전처리하는 Python 패키지입니다.

채팅 기록을 분석하거나 데이터셋으로 공유하려는 사용자가 시간 형식이 다른 메시지, 시스템 메시지, 노출된 개인정보를 직접 정리해야 하는 반복 작업을 줄여 줍니다.

주요 기능은 다음과 같습니다.

- UTF-8 인코딩의 다국어 채팅 기록 불러오기
- 메시지별 시간, 발언자, 발언 내용 파싱
- 시간 형식 통일
- 메시지를 시간순으로 정렬하고, 시간이 같으면 원본 순서 유지
- 미리 정의된 패턴의 시스템 메시지 제거
- 정규표현식을 이용한 전화번호와 이메일 마스킹

정제된 채팅 기록은 입력 파일과 같은 형식의 새로운 UTF-8 파일로 저장합니다. 원본 파일은 수정하지 않으며, 전화번호와 이메일이 마스킹된 부분을 제외한 발언 내용은 원문 그대로 보존합니다.

이름과 주소 등 전화번호·이메일 이외의 개인정보 마스킹, 번역, 이미지 및 파일 첨부 처리는 지원 범위에 포함되지 않습니다. 비표준 형식의 개인정보나 정의되지 않은 시스템 메시지는 처리되지 않을 수 있으므로 결과를 직접 확인해야 합니다.

## 2. Installation

TestPyPI에서 `chatlog-cleaner` 0.1.0을 설치합니다.

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ chatlog-cleaner==0.1.0
```

## 3. Quick start

채팅 기록 파일을 불러와 전처리한 뒤 새로운 파일로 저장하는 것을 목표로 합니다.

예시 입력 파일:

```text
chat.txt
```

예시 출력 파일:

```text
chat_clean.txt
```

전처리 과정은 다음과 같습니다.

1. 채팅 기록 파일 불러오기
2. 메시지 파싱
3. 시간 형식 통일 및 정렬
4. 시스템 메시지 제거
5. 전화번호와 이메일 마스킹
6. 정제된 결과를 새 파일로 저장

다음 실제 Python 사용 예시는 전화번호와 이메일이 포함된 문자열에서 개인정보를 마스킹하는 방법입니다.
from chatlog_cleaner import mask_pii

message = "연락처 010-1234-5678, 이메일 kim@example.com"
cleaned_message = mask_pii(message)

print(cleaned_message)

실행 결과:
연락처 [PHONE], 이메일 [EMAIL]

## 4. Dependencies

현재 `pyproject.toml`의 프로젝트 의존성은 없습니다.

- Python: 3.10 이상
- Runtime dependencies: 없음
- Build backend: Hatchling

## 5. Tests

TODO: 테스트 샘플 및 테스트 실행 방법을 추가합니다.

## 6. Documentation

- [Project proposal](docs/proposal.md): 프로젝트 목적, 사용자 및 개발 범위
- [API reference](docs/api.md): 공개 함수 및 docstring 기반 API 문서
- [Team rules](docs/team-rules.md): 브랜치, PR, 리뷰 및 머지 규칙
- [Documentation 
site](https://oss26-team-07.github.io/chatlog-cleaner/)

## 7. Release

TODO: 정식 PyPI 배포 후 릴리스 버전 및 설치 방법을 추가합니다.

## 8. Team

| Name | Contribution |
|---|---|
| 서울아논 | 패키지 설정, 빌드 및 TestPyPI 업로드 |
| 심예린 | TestPyPI 설치 확인 |
| 강선아 | README 작성 및 `normalize_time` 구현 |
| 목행창 | README 리뷰 |
| 최은서 | README 리뷰 |

팀 작업 규칙은 [team-rules.md](docs/team-rules.md)를 참고합니다.

## 9. License

MIT License. 자세한 내용은 [LICENSE](LICENSE)를 참고하세요.
