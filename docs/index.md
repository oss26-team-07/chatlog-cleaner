# chatlog_cleaner

## 프로젝트 설명(Project description)

여러 언어가 섞인 채팅 기록을 불러와 정제하고 개인정보를 마스킹하는 전처리 기능을 개발합니다.
(We build a preprocessing package that loads multilingual chat logs, cleans them, and masks personal information.)

## 주요 기능(Main features)

- UTF-8 인코딩으로 여러 언어가 섞인 채팅 기록 불러오기(Load multilingual chat logs encoded in UTF-8)
- 메시지별로 시간, 발언자, 발언 내용을 파싱(Parse the time, speaker, and content of each message)
- 시간 형식을 통일하고 발언 순서대로 정렬 (시간이 같으면 원본 순서 유지)(Normalize time formats and sort by time; equal times keep the original order)
- 고정된 패턴의 시스템 메시지를 식별해 제거(Identify and remove system messages with fixed patterns)
- 정규표현식으로 전화번호와 이메일을 찾아 대체 문자열로 마스킹(Find phone numbers and emails with regular expressions and mask them)

## 목표(Goals)

- 위의 주요 기능을 모두 구현합니다(Implement all of the main features above).
- 테스트 샘플의 출력 결과가 기대 결과와 일치해야 합니다(The output for the test sample must match the expected result).
- 발언 내용은 전화번호와 이메일이 마스킹된 부분 외에는 원문과 동일해야 합니다(Message content must stay identical to the original except for the masked phone numbers and emails).

## 문서(Documents)

- [Proposal](proposal.md): 무엇을, 누구를 위해 만드는지(what we are building and for whom)
- [API](api.md): 모든 공개 함수, docstring에서 자동 생성(every public function, generated from the docstrings)
- [Team rules](team-rules.md): 팀 작업 규칙(how we work)
