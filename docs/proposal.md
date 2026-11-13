# 프로젝트 제안서(Project proposal): "다국어 채팅 기록 전처리기(Multilingual Chat Log Preprocessor)"

## 1. 프로젝트 주제(Project topic)

### 만들고 싶은 프로그램(What we want to build)

여러 언어가 섞인 채팅 기록을 불러와 정제하고, 전화번호와 이메일 같은 개인정보를 마스킹하는 전처리 Python 패키지를 개발한다.
(We will build a Python package that loads multilingual chat logs, cleans them, and masks personal information such as phone numbers and email addresses.)

### 사용자 정의 및 해결할 문제(Users and problem)

채팅 기록을 분석하거나 데이터셋으로 공유하려는 사용자는 시간 형식이 제각각이고, 시스템 메시지가 섞여 있으며, 전화번호와 이메일이 그대로 노출된 기록을 직접 하나씩 정리하고 가려야 한다. 이 프로그램은 파싱, 시간 형식 통일, 정렬, 시스템 메시지 제거, 개인정보 마스킹을 한 번에 처리해 이 반복 작업을 줄여 준다.
(Users who want to analyze chat logs or share them as a dataset must manually clean logs with inconsistent time formats and mixed-in system messages, and hide exposed phone numbers and emails one by one. This program parses, normalizes time formats, sorts, removes system messages, and masks personal information in one pass, reducing this repetitive work.)

## 2. 개발할 기능(Planned features)

### 입력(Input)

사용자가 컴퓨터에 저장한 UTF-8 인코딩의 채팅 기록 파일. 한국어, 영어 등 여러 언어가 섞여 있으며, 각 메시지에는 시간, 발언자, 발언 내용이 포함된다.
(A UTF-8 encoded chat log file stored on the user's computer. It mixes multiple languages such as Korean and English, and each message contains a time, a speaker, and the message content.)

### 처리(Processing)

1. UTF-8 인코딩으로 여러 언어가 섞인 채팅 기록 파일을 불러온다(Load the multilingual chat log file with UTF-8 encoding).
2. 메시지별로 시간, 발언자, 발언 내용을 파싱한다(Parse the time, speaker, and content of each message).
3. 시간 형식을 하나로 통일한다(Normalize all times into a single format).
4. 발언 시간 순서대로 정렬하고, 시간이 같으면 원본 순서를 유지한다(Sort messages by time; messages with the same time keep their original order).
5. 고정된 패턴의 시스템 메시지를 식별해 제거한다(Identify and remove system messages that follow fixed patterns).
6. 정규표현식으로 전화번호와 이메일을 찾아 대체 문자열로 마스킹한다(Find phone numbers and email addresses with regular expressions and replace them with mask strings).

### 결과(Output)

정제된 채팅 기록을 입력 파일과 같은 형식의 UTF-8 파일로 새로 저장한다. 각 메시지는 통일된 시간 형식, 발언자, 발언 내용으로 구성되고 시간 순서대로 정렬된다. 시스템 메시지는 제거되며, 발언 내용은 전화번호와 이메일이 마스킹된 부분 외에는 원문과 동일하게 보존한다. 원본 파일은 수정하지 않는다.
(The program saves the cleaned chat log as a new UTF-8 file in the same format as the input file. Each message consists of a normalized time, the speaker, and the content, sorted by time. System messages are removed, and message content stays identical to the original except for the masked phone numbers and emails. The original file is not modified.)

### 개발 범위(Scope)

- 포함할 기능(In scope): UTF-8 다국어 채팅 기록 불러오기, 메시지 파싱, 시간 형식 통일 및 정렬, 고정 패턴 시스템 메시지 제거, 전화번호·이메일 마스킹(Loading UTF-8 multilingual chat logs, parsing messages, normalizing and sorting times, removing fixed-pattern system messages, and masking phone numbers and emails).
- 제외할 기능(Out of scope): 이름·주소 등 전화번호와 이메일 외 개인정보 마스킹, 번역, 이미지·파일 첨부 처리(Masking personal information other than phone numbers and emails such as names or addresses, translation, and handling attached images or files).
- 한계(Limitation): 정규표현식에 맞지 않는 비표준 형식의 전화번호나 이메일, 정의되지 않은 패턴의 시스템 메시지는 처리되지 않을 수 있으므로 결과를 직접 확인해야 한다(Phone numbers or emails in non-standard formats and system messages with undefined patterns may not be handled, so the output must be checked manually).

### 사용 예시(Usage example)

사용자가 한국어와 영어가 섞인 채팅 기록 `chat.txt`를 입력한다. 프로그램은 메시지를 파싱해 시간 형식을 통일하고 시간 순서대로 정렬한 뒤, 입장·퇴장 같은 시스템 메시지를 제거하고 전화번호와 이메일을 마스킹해 `chat_clean.txt`를 새로 저장한다. 사용자는 테스트 샘플의 출력 결과가 기대 결과와 일치하는지, 마스킹된 부분 외의 발언 내용이 원문과 같은지 확인한다.
(The user provides `chat.txt`, a chat log mixing Korean and English. The program parses the messages, normalizes time formats, sorts them by time, removes system messages such as join and leave notices, masks phone numbers and emails, and saves a new file, `chat_clean.txt`. The user checks that the output for the test sample matches the expected result and that message content is identical to the original except for the masked parts.)
