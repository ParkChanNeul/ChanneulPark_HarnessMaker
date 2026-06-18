# Teacher Decision Card

## 한 줄 진단

학생은 주문 표현을 알고 있지만 직원의 후속 질문에 즉시 반응하는 연습이 필요하다.

```yaml
decision_card_id: cafe-card-001
teacher_facts: [A1, 50분, 카페 상황]
agent_interpretations: [후속 질문 반응이 핵심 부담일 수 있음]
options:
  - option_id: A
    mode: advance
    benefits: [새 표현 확장]
    risks: [반응 연습 부족]
  - option_id: B
    mode: mixed
    vocabulary_scope: {new_item_count: 10, productive_core_count: 6, receptive_support_count: 4, homework_expansion_count: 2}
    benefits: [주문과 후속 질문을 함께 연습]
    risks: [시간 관리 필요]
recommendation: {option_id: B, rationale: 후속 질문 대응을 포함할 수 있음, limitations: 실제 수업 관찰 전 추정}
scope_status: ready_to_lock
```
