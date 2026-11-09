# 팀 규칙(Team rules): "다국어 채팅 기록 전처리기(Multilingual Chat Log Preprocessor)"

## PR 크기(Pull request size)

- PR 하나에는 기능 하나 또는 수정 하나만 포함하며, 변경 줄 수는 약 100줄 이내로 한다(One pull request contains one function or one fix, about 100 changed lines).
- 파싱, 시간 정렬, 시스템 메시지 제거, 마스킹은 각각 별도의 PR로 올린다(Parsing, time sorting, system message removal, and masking are submitted as separate pull requests).

## 리뷰 규칙(Review)

- 모든 PR은 작성자를 제외한 팀원 2명 이상이 리뷰한다(Every pull request is reviewed by at least two members other than the author).
- 리뷰는 PR이 올라온 뒤 48시간 이내에 완료한다(Reviews are completed within 48 hours of the pull request being opened).
- `blocking:` 코멘트가 하나라도 해결되지 않았으면 머지하지 않는다(A pull request is not merged while any `blocking:` comment is unresolved).
- 리뷰어는 연결된 이슈와 일치하는지, 테스트 샘플의 출력이 기대 결과와 같은지, 마스킹된 부분 외의 발언 내용이 원문과 같은지 확인한다(Reviewers check that the change matches the linked issue, that the test sample output matches the expected result, and that message content is identical to the original except for the masked parts).

## 머지 규칙(Merge)

- 마지막으로 승인한 리뷰어가 머지 버튼을 누른다(The last approving reviewer presses the merge button).
- 머지 옵션은 "Create a merge commit"을 사용한다(Use "Create a merge commit").
- 머지 후 브랜치를 삭제한다(Delete the branch after merging).
- main 브랜치에 직접 push하지 않는다(No one pushes directly to main).

## 브랜치 이름(Branch names)

- 새 기능(New feature): `feat/<name>`
- 버그 수정(Bug fix): `fix/<name>`
- 문서(Documentation): `docs/<name>`
- 설정 및 기타(Configuration and others): `chore/<name>`

## 커밋 메시지(Commit messages)

- `영역: 한 문장 설명` 형식으로 쓴다(Use the format `area: one-sentence description`).

## 소통 채널(Communication)

- 팀 논의는 카카오톡 단톡방에서 하고, 결정 사항은 GitHub 이슈에 기록한다(Team discussion happens in the KakaoTalk group chat, and decisions are recorded in GitHub issues).

## AI 사용 공개(AI use)

- 모든 PR의 `## AI use` 섹션에 사용한 도구, 적용한 파일·함수, 사용 방식(생성, 완성, 리팩터링, 설명, 리뷰), 직접 수정하거나 확인한 내용을 적는다(Every pull request states in its `## AI use` section the tool, the files or functions, how it was used (generated, completed, refactored, explained, or reviewed), and what the author changed or verified by hand).
- AI를 사용하지 않았으면 `none`이라고 적는다. 비워 두거나 "used ChatGPT"처럼만 쓰면 인정되지 않는다(If no AI was used, write `none`. Leaving it blank or writing only "used ChatGPT" is not accepted).
- 작성자는 AI가 생성한 코드를 포함해 PR의 모든 줄을 설명할 수 있어야 한다(The author must be able to explain every line of the pull request, including AI-generated code).
