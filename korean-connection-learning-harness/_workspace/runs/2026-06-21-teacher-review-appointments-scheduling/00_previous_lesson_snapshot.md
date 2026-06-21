# Previous Lesson Snapshot: Clinic / Pharmacy

```yaml
snapshot_id: "previous-lesson-snapshot-2026-06-21-appointments"
source_run: "../2026-06-14-build-lesson-clinic-pharmacy"
source_status: "read-only legacy evidence"
canonical_interpretation_only: true
mastery_claim_status: "not established"
next_review_scope:
  primary_situation:
    pack_ref: "appointments_scheduling"
    sub_situation_ids:
      - "reschedule"
      - "cancel"
      - "confirm_time"
  transfer_situation:
    pack_ref: "messaging_calls"
    sub_situation_ids:
      - "open"
      - "request"
      - "close"
```

## 이전 수업에서 실제 노출된 단어와 표현

학생용 HTML에 실제로 노출된 텍스트만 정리했다.

### 증상과 시간

- `아파요.`
- `머리가 아파요.`
- `목이 아파요.`
- `배가 아파요.`
- `허리가 아파요.`
- `어제부터요.`
- `오늘 아침부터요.`
- `머리가 아파요. 어제부터요.`
- `목이 아파요. 오늘 아침부터요.`

### 반복 요청과 대화 복구

- `천천히 해 주세요.`
- `다시 한 번 말해 주세요.`
- `아, 잠깐만요.`
- `아, 네.`

### 다음 행동 확인

- `잠깐 쉬어도 돼요?`
- `이거 먹어도 돼요?`
- `커피 마셔도 돼요?`
- `운동해도 돼요?`
- `물 마셔도 돼요?`

### 상대방 역할에서 노출된 표현

- `어디가 아프세요?`
- `이 약 드시면 돼요.`
- `검사하고 기다리세요.`

## Legacy Target의 현재 Canonical 해석

| Legacy evidence | 현재 해석 | 이번 Run 처리 |
|---|---|---|
| `request_juseyo` | `grammar_request_verb_eo_juseyo` | `바꿔 주세요`에서 review |
| `polite_yo` | `register_haeyo_polite` | 짧은 해요체 응답에서 retrieval |
| `confirm_next_step` | `interaction_confirm_and_answer` | 새 시간 확인에서 practice |
| `symptom.bodypart_apayo` | 이번 요청에 대응 Canonical Target이 지정되지 않음 | `몸이 안 좋아요`를 짧은 선행 문장으로만 사용 |
| `do_dwaeyo` | 이번 제안 Target 목록에 없음 | 이전 노출 증거로만 보존하고 핵심 연습에서는 제외 |
| `repair_when_confused` | 이번 제안 Target 목록에 없음 | 필요 시 교실 복구 문장으로 사용하되 평가 Target으로 삼지 않음 |

과거 Run의 Legacy 파일과 ID는 수정하지 않는다.

## 이전 Practice

- Controlled: `머리/목/배/허리 + 이/가 아파요` 치환.
- Controlled: `먹다/마시다/쉬다 + -아/어도 돼요?` 선택.
- Guided: 증상 뒤에 시간 단서, 반복 요청, 확인 질문 중 적절한 다음 문장 선택.
- Guided: 빠른 직원 발화 뒤 `아, 잠깐만요. 다시 한 번 말해 주세요.` 사용.
- Independent: 약국에서 증상과 시간 단서를 모델 없이 말하기.
- Independent: 직원 안내 뒤 다음 행동을 확인하기.

## 이전 Transfer

- PT/Gym의 `잠깐 쉬어도 돼요?`를 Pharmacy의 `이거 먹어도 돼요?`로 전이.
- Taxi/PT의 요청 도구를 Clinic의 `다시 한 번 말해 주세요`로 전이.
- 단독 `아파요`를 `[body part] + 이/가 아파요`로 확장.

## 확인된 숙련 증거

- 실제 학생 자료에 증상, 시간, 반복 요청, 확인 질문이 노출되었다.
- Controlled, Guided, Independent, Transfer 단계가 이전 Practice Plan과 Student Deck에 모두 존재했다.
- 이전 Assessment는 산출물의 구조와 연습 경로가 완성되었다고 판정했다.
- 학습자의 실제 수행을 직접 기록한 Lesson Result는 없으므로 안정된 숙련으로 확정할 수 있는 항목은 없다.

## 확인되지 않은 숙련 증거

- 모델 없이 증상 문장을 실제로 산출했는지.
- 지연 회상으로 `다시 한 번 말해 주세요`를 꺼냈는지.
- 독립 Roleplay를 끝까지 수행했는지.
- `-아/어도 돼요?`를 새로운 상황으로 실제 전이했는지.
- 이전 Tiny Mission을 수행했는지.
- `내일`을 이전 수업에서 학습했는지. 지정된 학생용 HTML에서는 한국어 `내일` 노출을 확인하지 못했다.

## 이번 수업에서 복습할 항목

- `아프다`: 실제 노출된 `아파요`를 `몸이 안 좋아요`라는 짧은 상태 문장으로 연결한다.
- `오늘`, `아침`: 실제 노출된 `오늘 아침부터요`에서 시간 표현을 회수한다.
- `내일`: 일정 조정에 필수인 복습 후보지만 이전 노출은 확인되지 않았으므로 강사 확인이 필요하다.
- `grammar_request_verb_eo_juseyo`: 기존 반복 요청 형태를 `세 시로 바꿔 주세요`로 전이한다.
- `register_haeyo_polite`: 짧고 공손한 예약 변경 대화에서 회수한다.
- `interaction_confirm_and_answer`: 다음 시간 확인과 응답으로 전이한다.

## 이번 수업에서 반복하지 않을 항목

- 머리, 목, 배, 허리의 전체 신체 부위 치환 Drill.
- 약, 복용, 검사 등 Clinic/Pharmacy 중심 어휘.
- `-아/어도 돼요?`의 동사별 반복 Drill.
- 실제 의료 정보, 진단, 약 이름, 병력.
- 이전 Clinic/Pharmacy Roleplay의 재현.
- `grammar_reason_eoseo`의 형태 설명. 60/90분에서는 두 개의 짧은 문장을 우선하고 120분 확장에서만 승인 후 다룬다.
