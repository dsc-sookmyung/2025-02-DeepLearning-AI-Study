# 📘 2025-Q1 AI/DL Study Repository

[25-26 GDG on Campus Sookmyung 6기] 1분기 스터디 (AI/DL – CV & NLP) 저장소

## 📌 TL;DR

> 1. 개인 브랜치 생성 → `이름_트랙`
> 2. 주차별 폴더(`WEEK01/`) 추가 → `summary.md` & `practice/` 제출
> 3. 개인 브랜치 → main으로 PR → 팀 멤버 리뷰 & 머지
> 4. PR과 commit 규칙 지켜주세요! ☺️

---

## 💁🏻‍♀️ 스터디원

- Team member: 김혜나, 최서영, 최윤서
- Member: 곽해림, 김찬란, 오현서, 이은재

---

## 📚 과제 규칙

- **마감 기한**: 매주 **화요일 23:59**
- **제출 내용**:
  - 강의 요약 (노션 정리 후, 깃허브에는 핵심 요약 및 노션 링크만 삽입)
  - 실습 코드 및 리소스 (practice/)

---

## 📚 커리큘럼 & 참고 자료

스터디 세부 커리큘럼과 진행 방식은 아래 링크에서 확인하실 수 있습니다 👇

- [AI/DL 스터디 커리큘럼 (Notion)](https://www.notion.so/1-AI-DL-27133fc61813811c85a7dccdb3c6e3e9?source=copy_link)
- [GDG Sookmyung 티스토리 블로그](https://dsc-sookmyung.tistory.com) → 격주 업로드

(순서: 서영님 → 혜나님 → 현서님 → 은재님 → 윤서님 → 찬란님 → 해림님)

---

## 🛠 브랜치 & 디렉토리 규칙

### 1) 브랜치

- **개인별 브랜치 1개 생성** (main에서 분기)
- 이름 규칙: `이름_트랙`
  - ex. `Hannah_NLP` / `Hannah_CV`
  - 둘 다 참여하는 경우 → 두 개 브랜치 생성

---

### 2) 디렉토리 구조

- 개인 브랜치 안에서 주차별 폴더를 늘려가며 관리

```bash
 ├── Hannah_NLP/                  # ← 본인 이름_트랙
 │    ├── WEEK01/
 │    │    ├── summary.md         # 강의 요약 (샘플 참고)
 │    │    └── practice/          # 실습 코드 & 리소스
 │    └── WEEK02/
 │         ├── summary.md
 │         └── practice/
 └── Hannah_CV/
      └── WEEK01/ ...
```

👉 summary.md에는 핵심 요약 + 노션 링크 기록

👉 개인 폴더 안에 README.md 작성 여부는 자유 (추천: 개인 학습 기록용)

---

### 3) 강의 요약 템플릿 (summary.md)

- 아래 템플릿 예시를 그대로 복사해 사용하세요 👇

```Markdown
# WEEK01 Summary - 분야 (이름)

### 📖 강의 핵심
- Word Embedding 기본 개념 (one-hot → dense vector)
- Distributional Hypothesis: "You shall know a word by the company it keeps"
- Assignment: word2vec 구현 실습

### 📌 상세 정리
👉 [노션 링크](https://notion.so/your-link)

### 💻 코드
- practice/word2vec.py
```

---

## 🔄 PR 규칙

- PR 제목 규칙: `[Merge] 개인 브랜치 이름 → main (WEEK주차)`

  예) `[Merge] Hannah_NLP → main (WEEK01)`

- base/compare 규칙: `base: main ← compare: 개인브랜치`
- PR 리뷰 & 머지: Team Member가 리뷰 후 승인/머지

---

## ✏️ Commit 규칙

- 일관된 메시지 사용합니다!

```bash
feat : WEEK01 강의 요약 및 코드 추가
fix : WEEK01 코드 버그 수정
chore : 디렉토리 구조 정리
```

---

## 🚨 주의사항

- main에는 직접 푸시 금지
- 브랜치 및 폴더 네이밍 규칙 반드시 준수
- 파일명은 영어 + snake_case 권장 (예: week01_summary.md)
- PR은 반드시 주차 단위로 제출
- 팀 멤버가 아닌 경우 main으로 직접 PR 금지 (개인 브랜치만 사용)
