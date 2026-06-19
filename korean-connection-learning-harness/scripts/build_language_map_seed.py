#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "domain" / "02_language_map"
SITUATIONS = ROOT / "domain" / "03_situations"
PROFILES = ROOT / "domain" / "04_profiles"

SOURCE_BY_BAND = {
    "A0": [
        "international_standard_curriculum_report",
        "nuri_sejong_korean_intro",
        "nuri_sejong_korean_1a",
    ],
    "A1": [
        "international_standard_curriculum_report",
        "nuri_sejong_korean_1a",
        "nuri_sejong_korean_1b",
    ],
    "A2": [
        "international_standard_curriculum_report",
        "nuri_sejong_korean_2a",
        "nuri_sejong_korean_2b",
    ],
}
PRIMARY_SEQUENCE_SOURCE_BY_BAND = {
    "A0": ("nuri_sejong_korean_intro", "official_content_scope"),
    "A1": ("nuri_sejong_korean_1a", "official_table_of_contents"),
    "A2": ("nuri_sejong_korean_2a", "official_table_of_contents"),
}


def dump(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def examples(form: str, function: str) -> dict:
    return {
        "basic": [
            f"{form}을 사용해 {function}을 수행한다.",
            f"짧은 문장에서 {form}을 알아듣는다.",
            f"질문에 {form}을 사용해 답한다.",
            f"새 상황에서 {form}을 스스로 말한다.",
        ],
        "situation_variants": [
            f"서비스 상황: {form}",
            f"일상 대화: {form}",
            f"역할극 전이: {form}",
        ],
        "contrasts": [
            f"{form} 사용 / 형태를 생략한 표현",
            f"{form} 사용 / 다른 기능의 유사 표현",
        ],
        "error_examples": [
            f"오류: {form}의 결합 위치를 바꿈",
            f"오류: {form}을 관계와 상황에 맞지 않게 사용함",
        ],
    }


def target(
    target_id: str,
    target_type: str,
    form: str,
    band: str,
    function: str,
    *,
    situations: list[str] | None = None,
    hard: list[str] | None = None,
    soft: list[str] | None = None,
    varieties: list[str] | None = None,
    status: str = "active",
    source_refs: list[str] | None = None,
    extra: dict | None = None,
) -> dict:
    sources = SOURCE_BY_BAND[band] if source_refs is None else source_refs
    sequence_source, sequence_locator = PRIMARY_SEQUENCE_SOURCE_BY_BAND[band]
    record = {
        "target_id": target_id,
        "target_type": target_type,
        "canonical_form": form,
        "level": {
            "primary_band": band,
            "confidence": "medium" if sources else "low",
            "source_refs": sources,
        },
        "functions": [function],
        "situation_refs": situations or [],
        "prerequisites": {"hard": hard or [], "soft": soft or []},
        "complexity": {
            "prerequisite_depth": len(hard or []),
            "morphology_load": "medium",
            "semantic_load": "medium",
            "processing_load": "medium",
            "register_load": "medium",
            "discourse_load": "medium",
        },
        "skill_mastery": {
            "listening": [f"{form}의 {function} 기능을 알아듣는다"],
            "speaking": [f"{form}을 사용해 {function}을 수행한다"],
            "reading": [f"문장에서 {form}을 식별한다"],
            "writing": [f"짧은 문장에 {form}을 적용한다"],
            "pronunciation": [],
            "interaction": [f"상황에 맞게 {function}을 수행한다"],
        },
        "language_varieties": varieties or ["standard"],
        "explanations": {
            "ko": f"`{form}`은/는 초급 학습자가 {function}을 수행할 때 사용하는 항목이다.",
            "en": f"`{form}` helps a beginner perform the function: {function}.",
        },
        "english_speaker_notes": {
            "literal_translation_risk": "Do not map the Korean form one-to-one onto a single English word.",
            "common_transfer_error": "English word order or directness may produce an unnatural Korean choice.",
        },
        "common_errors": [
            f"{form}의 형태 결합을 잘못함",
            f"{form}을 기능이나 상황에 맞지 않게 사용함",
        ],
        "examples": examples(form, function),
        "example_refs": [],
        "source_refs": sources,
        "source_evidence": [
            {
                "source_ref": "international_standard_curriculum_report",
                "locator_ref": "curriculum_content",
                "claim_scope": "교육 내용 범주와 초급 지도 구성의 공식 기준. 개별 A0/A1/A2 등치는 내부 추천 metadata이다.",
            },
            {
                "source_ref": sequence_source,
                "locator_ref": sequence_locator,
                "claim_scope": "공식 입문·초급 과정 배열과의 교차 확인. 자체 생성 설명과 예문을 복사 근거로 사용하지 않는다.",
            },
        ] if sources else [],
        "status": status,
    }
    if extra:
        record.update(extra)
    return record


GRAMMAR = [
    ("grammar_copula_ieyo_yeyo", "N이에요/예요", "A0", "identify_or_describe"),
    ("grammar_copula_anieyo", "N이/가 아니에요", "A0", "negate_identity"),
    ("grammar_present_haeyo", "V/A-아/어요", "A0", "state_present_action_or_quality"),
    ("grammar_question_haeyo", "V/A-아/어요?", "A0", "ask_basic_question"),
    ("grammar_exist_isseoyo", "N이/가 있어요", "A0", "state_existence"),
    ("grammar_exist_eopseoyo", "N이/가 없어요", "A0", "state_nonexistence"),
    ("grammar_negative_an", "안 V/A", "A1", "negate_action_or_quality"),
    ("grammar_negative_ji_anhayo", "V/A-지 않아요", "A1", "formal_negative"),
    ("grammar_inability_mot", "못 V", "A1", "state_inability"),
    ("grammar_past_eosseoyo", "V/A-았/었어요", "A1", "state_past_event"),
    ("grammar_future_eul_geoyeyo", "V-(으)ㄹ 거예요", "A1", "state_future_plan"),
    ("grammar_request_verb_eo_juseyo", "V-아/어 주세요", "A1", "request_action"),
    ("grammar_imperative_seyo", "V-(으)세요", "A1", "give_polite_instruction"),
    ("grammar_prohibition_ji_maseyo", "V-지 마세요", "A1", "prohibit_action"),
    ("grammar_suggestion_eulkkayo", "V-(으)ㄹ까요?", "A1", "make_suggestion"),
    ("grammar_suggestion_gachi", "같이 V-아/어요", "A1", "suggest_joint_action"),
    ("grammar_want_go_sipeoyo", "V-고 싶어요", "A1", "express_desire"),
    ("grammar_intention_euryeogo_haeyo", "V-(으)려고 해요", "A1", "express_intention"),
    ("grammar_ability_eul_su_isseoyo", "V-(으)ㄹ 수 있어요", "A1", "express_ability"),
    ("grammar_inability_eul_su_eopseoyo", "V-(으)ㄹ 수 없어요", "A1", "express_inability"),
    ("grammar_permission_eodo_dwaeyo", "V-아/어도 돼요?", "A1", "ask_permission"),
    ("grammar_prohibition_eumyeon_an_dwaeyo", "V-(으)면 안 돼요", "A1", "state_prohibition"),
    ("grammar_obligation_eoya_dwaeyo", "V-아/어야 돼요", "A1", "state_obligation"),
    ("grammar_try_eoboseyo", "V-아/어 보세요", "A1", "suggest_trying"),
    ("grammar_experience_eobon_jeok", "V-아/어 본 적이 있어요", "A2", "state_experience"),
    ("grammar_before_gi_jeone", "V-기 전에", "A1", "sequence_before"),
    ("grammar_after_eun_hue", "V-(으)ㄴ 후에", "A2", "sequence_after"),
    ("grammar_when_eul_ttae", "V/A-(으)ㄹ 때", "A1", "locate_event_in_time"),
    ("grammar_during_neun_jung", "V-는 중이에요", "A2", "state_ongoing_action"),
    ("grammar_simultaneous_eumyeonseo", "V-(으)면서", "A2", "express_simultaneous_actions"),
    ("grammar_reason_eoseo", "V/A-아/어서", "A1", "give_reason"),
    ("grammar_reason_eunikka", "V/A-(으)니까", "A2", "give_reason_or_basis"),
    ("grammar_reason_gi_ttaemune", "V/A-기 때문에", "A2", "give_explicit_reason"),
    ("grammar_condition_eumyeon", "V/A-(으)면", "A1", "state_condition"),
    ("grammar_concession_eodo", "V/A-아/어도", "A2", "state_concession"),
    ("grammar_sequence_go", "V/A-고", "A1", "connect_actions_or_qualities"),
    ("grammar_sequence_eoseo", "V-아/어서", "A1", "connect_sequential_actions"),
    ("grammar_contrast_jiman", "V/A-지만", "A1", "contrast_clauses"),
    ("grammar_background_neundeyo", "V/A-는데요", "A2", "provide_background"),
    ("grammar_alternative_geona", "V-거나", "A2", "offer_action_alternatives"),
    ("grammar_noun_alternative_na", "N(이)나", "A1", "offer_noun_alternative"),
    ("grammar_comparison_boda", "N보다", "A1", "compare_entities"),
    ("grammar_similarity_cheoreom", "N처럼", "A2", "express_similarity"),
    ("grammar_degree_deo", "더", "A1", "increase_degree"),
    ("grammar_superlative_gajang", "가장", "A1", "express_superlative"),
    ("grammar_conjecture_geot_gatayo", "V/A-(으)ㄴ/는 것 같아요", "A2", "express_conjecture"),
    ("grammar_uncertainty_euljido_mollayo", "V/A-(으)ㄹ지도 몰라요", "A2", "express_uncertainty"),
    ("grammar_commitment_eulgeyo", "V-(으)ㄹ게요", "A2", "make_commitment"),
    ("grammar_change_ge_dwaeyo", "V-게 돼요", "A2", "describe_change"),
    ("grammar_decision_giro_haeyo", "V-기로 해요", "A2", "state_decision"),
    ("grammar_wish_eumyeon_jokesseoyo", "V/A-(으)면 좋겠어요", "A2", "express_wish"),
    ("grammar_purpose_eureo_gayo", "V-(으)러 가요", "A1", "state_movement_purpose"),
    ("grammar_purpose_euryeogo", "V-(으)려고", "A2", "state_purpose"),
    ("grammar_purpose_gi_wihae", "V-기 위해(서)", "A2", "state_formal_purpose"),
    ("grammar_relative_present_neun_n", "V-는 N", "A2", "modify_noun_present"),
    ("grammar_relative_past_eun_n", "V-(으)ㄴ N", "A2", "modify_noun_past"),
    ("grammar_relative_future_eul_n", "V-(으)ㄹ N", "A2", "modify_noun_future"),
    ("grammar_adjective_relative_eun_n", "A-(으)ㄴ N", "A1", "modify_noun_with_quality"),
    ("grammar_nominalization_gi", "V-기", "A2", "nominalize_action"),
    ("grammar_nominalization_neun_geot", "V-는 것", "A2", "nominalize_event"),
    ("grammar_indirect_statement_dago", "V/A-다고 해요", "A2", "report_statement"),
    ("grammar_indirect_noun_irago", "N(이)라고 해요", "A2", "report_noun_statement"),
    ("grammar_indirect_question_nyago", "V/A-(으)냐고 해요", "A2", "report_question"),
    ("grammar_indirect_command_rago", "V-(으)라고 해요", "A2", "report_command"),
    ("grammar_indirect_suggestion_jago", "V-자고 해요", "A2", "report_suggestion"),
    ("grammar_honorific_si", "V/A-(으)시-", "A2", "honor_subject"),
    ("grammar_honorific_kke", "N께", "A2", "mark_honored_recipient"),
    ("grammar_honorific_deurida", "드리다", "A2", "use_humble_giving"),
    ("grammar_from_eseobuteo", "N에서부터", "A2", "mark_starting_point"),
    ("grammar_until_kkaji", "N까지", "A1", "mark_end_point"),
    ("grammar_approximate_jjeum", "N쯤", "A2", "express_approximation"),
    ("grammar_addition_edaga", "N에다가", "A2", "add_or_layer_information"),
    ("grammar_while_daga", "V-다가", "A2", "interrupt_or_change_action"),
    ("grammar_repeated_mada", "N마다", "A2", "express_each_or_every"),
    ("grammar_only_man", "N만", "A1", "express_only"),
    ("grammar_also_do", "N도", "A0", "express_addition"),
    ("grammar_together_rang", "N(이)랑", "A1", "connect_companions"),
    ("grammar_and_hago", "N하고", "A0", "connect_nouns"),
    ("grammar_range_buteo_kkaji", "N부터 N까지", "A1", "express_range"),
    ("grammar_before_e", "N 전에", "A1", "state_time_before"),
    ("grammar_after_daeume", "V-(으)ㄴ 다음에", "A2", "state_next_sequence"),
    ("grammar_suggestion_neun_ge_eottaeyo", "V-는 게 어때요?", "A2", "make_soft_suggestion"),
    ("grammar_preference_neun_pyeonieyo", "V/A-(으)ㄴ/는 편이에요", "A2", "describe_general_tendency"),
    ("grammar_desire_go_sipeunde", "V-고 싶은데요", "A2", "soften_desire_or_request"),
    ("grammar_try_eobwasseoyo", "V-아/어 봤어요", "A2", "state_attempted_experience"),
    ("grammar_permission_eodo_dwaeyo_statement", "V-아/어도 돼요", "A2", "grant_permission"),
    ("grammar_prohibition_ji_mara", "V-지 말다", "A2", "express_prohibition_base"),
    ("grammar_reason_eoseo_result", "V/A-아/어서 결과", "A1", "connect_cause_and_result"),
    ("grammar_descriptive_ge", "A-게", "A2", "form_adverb"),
    ("grammar_easy_gi_joayo", "V-기가 좋아요", "A2", "evaluate_action"),
    ("grammar_from_hanteseo", "N한테서", "A2", "mark_informal_source"),
    ("grammar_topic_neunyo", "N은/는요?", "A1", "return_or_shift_topic"),
    ("grammar_quote_irago", "N(이)라고", "A2", "quote_or_name"),
]

PARTICLES = [
    ("particle_topic_eunneun", "은/는", "A0", "mark_topic"),
    ("particle_contrast_eunneun", "은/는", "A1", "mark_contrast"),
    ("particle_subject_iga", "이/가", "A0", "mark_subject"),
    ("particle_subject_focus_iga", "이/가", "A1", "focus_new_subject"),
    ("particle_object_eulreul", "을/를", "A0", "mark_object"),
    ("particle_time_e", "에", "A0", "mark_time"),
    ("particle_destination_e", "에", "A0", "mark_destination"),
    ("particle_location_e", "에", "A0", "mark_existence_location"),
    ("particle_action_location_eseo", "에서", "A0", "mark_action_location"),
    ("particle_origin_eseo", "에서", "A1", "mark_origin"),
    ("particle_direction_euro", "(으)로", "A1", "mark_direction"),
    ("particle_means_euro", "(으)로", "A1", "mark_means"),
    ("particle_recipient_hante", "한테", "A1", "mark_informal_recipient"),
    ("particle_recipient_ege", "에게", "A1", "mark_recipient"),
    ("particle_honorific_recipient_kke", "께", "A2", "mark_honored_recipient"),
    ("particle_companion_hago", "하고", "A0", "mark_companion"),
    ("particle_companion_rang", "(이)랑", "A1", "mark_colloquial_companion"),
    ("particle_with_wa_gwa", "와/과", "A1", "connect_nouns_formally"),
    ("particle_also_do", "도", "A0", "mark_addition"),
    ("particle_only_man", "만", "A1", "mark_exclusion"),
    ("particle_from_buteo", "부터", "A1", "mark_start"),
    ("particle_until_kkaji", "까지", "A1", "mark_end"),
    ("particle_comparison_boda", "보다", "A1", "mark_comparison_standard"),
    ("particle_approximation_jjeum", "쯤", "A2", "mark_approximation"),
    ("particle_every_mada", "마다", "A2", "mark_each"),
    ("particle_choice_na", "(이)나", "A2", "mark_choice_or_approximation"),
]

REGISTERS = [
    ("register_haeyo_polite", "해요체", "A1", "safe_politeness"),
    ("register_hamnida_formal", "합니다체", "A2", "formal_politeness"),
    ("register_hae_casual", "해체", "A2", "casual_peer_speech"),
    ("register_honorific_si", "높임 선어말 -(으)시-", "A2", "honor_subject"),
    ("register_service_brief_polite", "서비스 상황의 짧은 존댓말", "A1", "brief_service_politeness"),
    ("register_address_role_title", "역할·직함 호칭", "A2", "select_address_term"),
    ("register_omit_second_person", "2인칭 대명사 생략", "A2", "avoid_direct_second_person"),
    ("register_softener_jom", "좀", "A1", "soften_request"),
    ("register_indirect_refusal", "완곡한 거절", "A2", "soften_refusal"),
    ("register_sentence_ending_choice", "문장 종결 선택", "A2", "manage_relationship_distance"),
    ("register_colloquial_contraction", "구어 축약", "A2", "recognize_colloquial_form"),
    ("register_online_neologism_boundary", "온라인 신조어 선택 경계", "A2", "avoid_unapproved_neologism"),
    ("register_slang_peer_boundary", "친밀한 또래 속어 선택 경계", "A2", "avoid_unapproved_slang"),
]

DISCOURSE = [
    ("discourse_short_noun_iyo", "N-(이)요", "A1", "short_noun_answer"),
    ("discourse_topic_eunneunyo", "은/는요?", "A1", "return_question"),
    ("discourse_geureondeyo", "그런데요", "A2", "signal_background_or_issue"),
    ("discourse_geureomyeon", "그러면", "A1", "continue_from_condition"),
    ("discourse_geuraeseo", "그래서", "A1", "connect_result"),
    ("discourse_a_geuraeyo", "아, 그래요?", "A1", "react_to_information"),
    ("discourse_majayo", "맞아요", "A0", "confirm_shared_information"),
    ("discourse_aniyo_geuge_anira", "아니요, 그게 아니라요", "A2", "repair_misunderstanding"),
    ("discourse_topic_shift", "화제 전환", "A2", "shift_topic"),
    ("discourse_clarifying_question", "되묻기", "A1", "ask_for_clarification"),
    ("discourse_confirmation_check", "확인하기", "A1", "confirm_understanding"),
    ("discourse_self_correction", "자기 수정", "A1", "repair_own_speech"),
    ("discourse_hold_turn", "말을 이어가기", "A2", "hold_turn"),
    ("discourse_answer_react_ask", "답하기→반응→되묻기", "A1", "sustain_conversation"),
    ("discourse_open_greeting", "인사로 열기", "A0", "open_exchange"),
    ("discourse_close_thanks", "감사로 닫기", "A0", "close_exchange"),
    ("discourse_sequence_first_next", "먼저/그다음", "A1", "sequence_information"),
    ("discourse_example_deureoseo", "예를 들어", "A2", "introduce_example"),
    ("discourse_reason_geon", "왜냐하면", "A2", "introduce_reason"),
    ("discourse_summary_geureonikka", "그러니까", "A2", "summarize_or_infer"),
    ("discourse_hesitation_eo", "어…", "A1", "buy_time"),
    ("discourse_one_moment", "잠시만요", "A0", "pause_interaction"),
    ("discourse_acknowledge_ne", "네", "A0", "acknowledge_turn"),
    ("discourse_reject_aniyo", "아니요", "A0", "reject_or_negate"),
    ("discourse_partial_agreement", "그렇긴 한데요", "A2", "partially_agree"),
    ("discourse_opinion_marker", "제 생각에는", "A2", "frame_opinion"),
    ("discourse_experience_frame", "제 경우에는", "A2", "frame_personal_experience"),
    ("discourse_check_next_step", "그다음은요?", "A1", "check_next_step"),
    ("discourse_repeat_key_item", "핵심어 반복", "A1", "confirm_key_item"),
    ("discourse_public_boundary_close", "공개 발화 경계 닫기", "A2", "close_public_interaction"),
]

INTERACTIONS = [
    ("interaction_greet", "인사하기", "A0", "greet"),
    ("interaction_self_introduce", "자기소개하기", "A0", "self_introduce"),
    ("interaction_request_item", "물건 요청하기", "A1", "request_item"),
    ("interaction_request_action", "행동 요청하기", "A1", "request_action"),
    ("interaction_ask_permission", "허락 구하기", "A1", "ask_permission"),
    ("interaction_refuse_softly", "부드럽게 거절하기", "A1", "refuse_softly"),
    ("interaction_apologize", "사과하기", "A0", "apologize"),
    ("interaction_thank", "감사하기", "A0", "thank"),
    ("interaction_confirm_and_answer", "확인하고 답하기", "A1", "confirm_and_answer"),
    ("interaction_ask_back", "되묻기", "A1", "ask_back"),
    ("interaction_request_correction", "수정 요청하기", "A1", "request_correction"),
    ("interaction_buy_time", "시간 벌기", "A1", "buy_time"),
    ("interaction_signal_nonunderstanding", "이해 실패 표시하기", "A0", "signal_nonunderstanding"),
    ("interaction_explain_problem", "문제 설명하기", "A1", "explain_problem"),
    ("interaction_ask_help", "도움 요청하기", "A0", "ask_help"),
    ("interaction_adjust_appointment", "약속 조정하기", "A2", "adjust_appointment"),
    ("interaction_state_opinion", "의견 말하기", "A2", "state_opinion"),
    ("interaction_agree", "동의하기", "A1", "agree"),
    ("interaction_disagree", "비동의하기", "A2", "disagree"),
    ("interaction_react_and_ask", "반응 후 되묻기", "A1", "react_and_ask"),
    ("interaction_close_conversation", "대화 종료하기", "A1", "close_conversation"),
    ("interaction_answer_question", "질문에 답하기", "A0", "answer_question"),
    ("interaction_ask_question", "질문하기", "A0", "ask_question"),
    ("interaction_select_option", "선택하기", "A0", "select_option"),
    ("interaction_report_emergency", "긴급 문제 보고하기", "A1", "report_emergency"),
    ("interaction_follow_instruction", "지시 확인하고 따르기", "A1", "follow_instruction"),
    ("interaction_repair_misheard_item", "잘못 들은 항목 고치기", "A1", "repair_misheard_item"),
    ("interaction_manage_public_boundary", "공개 상호작용 경계 관리하기", "A2", "manage_public_boundary"),
    ("interaction_coordinate_work", "업무 조정하기", "A2", "coordinate_work"),
    ("interaction_give_feedback", "피드백 말하기", "A2", "give_feedback"),
]

CHUNKS = [
    ("chunk_request_noun_juseyo", "N 주세요", "A1", "request_item"),
    ("chunk_repeat_dasi_malsseumhae_juseyo", "다시 말씀해 주세요", "A1", "request_repeat"),
    ("chunk_slowly_cheoncheonhi", "천천히 말씀해 주세요", "A1", "request_slow_speech"),
    ("chunk_dont_know_jal_moreugesseoyo", "잘 모르겠어요", "A0", "signal_nonunderstanding"),
    ("chunk_one_moment_jamsimanyo", "잠시만요", "A0", "buy_time"),
    ("chunk_gwaenchanayo", "괜찮아요", "A0", "accept_or_decline"),
    ("chunk_check_majayo", "맞아요?", "A1", "check_correctness"),
    ("chunk_what_is_this", "이게 뭐예요?", "A0", "ask_item_identity"),
    ("chunk_how_say", "어떻게 말해요?", "A1", "ask_expression"),
    ("chunk_self_repair", "제가 잘못 말했어요", "A1", "repair_own_speech"),
    ("chunk_not_that", "그게 아니라요", "A1", "correct_misunderstanding"),
    ("chunk_hello_annyeonghaseyo", "안녕하세요", "A0", "greet"),
    ("chunk_thanks_gamsahamnida", "감사합니다", "A0", "thank"),
    ("chunk_sorry_joesonghamnida", "죄송합니다", "A0", "apologize"),
    ("chunk_yes_ne", "네", "A0", "confirm"),
    ("chunk_no_aniyo", "아니요", "A0", "negate"),
    ("chunk_here_isseoyo", "여기 있어요", "A0", "indicate_location"),
    ("chunk_none_eopseoyo", "없어요", "A0", "state_absence"),
    ("chunk_where_eodiyeyo", "어디예요?", "A0", "ask_location"),
    ("chunk_how_much_eolmayeyo", "얼마예요?", "A0", "ask_price"),
    ("chunk_takeout_pojangieyo", "포장이에요", "A1", "state_takeout"),
    ("chunk_dine_in_meokgo_gayo", "먹고 갈게요", "A1", "state_dine_in"),
    ("chunk_card_payment", "카드로 할게요", "A1", "select_payment"),
    ("chunk_help_dowajuseyo", "도와주세요", "A0", "ask_help"),
    ("chunk_hurts_apayo", "아파요", "A0", "state_pain"),
    ("chunk_since_eojebuteoyo", "어제부터요", "A1", "state_duration_start"),
    ("chunk_can_i_eodo_dwaeyo", "이거 해도 돼요?", "A1", "ask_permission"),
    ("chunk_no_problem_munje_eopseoyo", "문제없어요", "A1", "confirm_no_problem"),
    ("chunk_wait_gidaryeo_juseyo", "기다려 주세요", "A1", "request_wait"),
    ("chunk_stop_meomchwo_juseyo", "멈춰 주세요", "A1", "request_stop"),
    ("chunk_little_more_jom_deo", "조금 더요", "A1", "request_more"),
    ("chunk_little_less_jom_deol", "조금 덜요", "A1", "request_less"),
    ("chunk_when_eonjeyeyo", "언제예요?", "A0", "ask_time"),
    ("chunk_available_ganeunghaeyo", "가능해요?", "A1", "ask_availability"),
    ("chunk_goodbye_annyeonghi", "안녕히 가세요", "A0", "close_exchange"),
]

PHONOLOGY = [
    ("phonology_hangul_vowel_values", "한글 모음 음가", "A0", "perceive_vowels"),
    ("phonology_hangul_consonant_values", "한글 자음 음가", "A0", "perceive_consonants"),
    ("phonology_plain_aspirated_tense", "평음·격음·경음", "A0", "distinguish_laryngeal_series"),
    ("phonology_batchim_representative", "받침 대표음", "A0", "produce_final_consonants"),
    ("phonology_liaison", "연음", "A1", "recognize_liaison"),
    ("phonology_nasalization", "비음화", "A1", "recognize_nasalization"),
    ("phonology_liquidization", "유음화", "A2", "recognize_liquidization"),
    ("phonology_tensification", "된소리되기", "A1", "recognize_tensification"),
    ("phonology_palatalization", "구개음화", "A2", "recognize_palatalization"),
    ("phonology_h_changes", "ㅎ 관련 음운 변화", "A2", "recognize_h_changes"),
    ("phonology_contraction", "축약", "A1", "recognize_contraction"),
    ("phonology_deletion", "음운 탈락", "A2", "recognize_deletion"),
    ("phonology_particle_attachment", "조사 결합 발음", "A1", "produce_particle_attachment"),
    ("phonology_ending_attachment", "어미 결합 발음", "A1", "produce_ending_attachment"),
    ("phonology_colloquial_reduction", "구어 속도 축약", "A2", "recognize_fast_speech"),
    ("phonology_statement_intonation", "평서문 억양", "A0", "produce_statement_intonation"),
    ("phonology_question_intonation", "의문문 억양", "A0", "produce_question_intonation"),
    ("phonology_confirmation_intonation", "확인 질문 억양", "A1", "produce_confirmation_intonation"),
    ("phonology_native_numbers", "고유어 수 발음", "A1", "produce_native_numbers"),
    ("phonology_sino_numbers", "한자어 수 발음", "A1", "produce_sino_numbers"),
    ("phonology_units_counters", "숫자·단위 결합 발음", "A1", "produce_number_unit_sequences"),
    ("phonology_loanword_adaptation", "외래어 발음 적응", "A2", "recognize_loanword_adaptation"),
]

ORTHOGRAPHY = [
    ("orthography_jamo_combination", "자모 조합", "A0", "combine_jamo"),
    ("orthography_syllable_block", "음절 블록", "A0", "build_syllable_block"),
    ("orthography_basic_batchim", "받침 표기", "A0", "write_batchim"),
    ("orthography_double_batchim_awareness", "겹받침 인식", "A2", "recognize_complex_batchim"),
    ("orthography_basic_spacing", "기초 띄어쓰기", "A1", "space_basic_units"),
    ("orthography_particle_attachment", "조사 붙여쓰기", "A1", "attach_particles"),
    ("orthography_ending_attachment", "어미 붙여쓰기", "A1", "attach_endings"),
    ("orthography_dependent_noun_spacing", "의존 명사 띄어쓰기", "A2", "space_dependent_nouns"),
    ("orthography_number_unit", "숫자와 단위 표기", "A1", "write_numbers_and_units"),
    ("orthography_sentence_punctuation", "문장부호", "A1", "use_punctuation"),
    ("orthography_question_mark", "물음표", "A0", "mark_question"),
    ("orthography_contraction_original", "축약형과 원형", "A2", "connect_contraction_and_base"),
    ("orthography_spoken_standard", "구어형과 표준 표기", "A2", "distinguish_spoken_and_standard"),
    ("orthography_loanword_spacing", "외래어 표기와 띄어쓰기", "A2", "write_common_loanwords"),
    ("orthography_chat_line_break", "메시지 줄바꿈", "A2", "format_short_messages"),
    ("orthography_form_fields", "양식의 이름·날짜·번호 표기", "A1", "complete_basic_form"),
]


def make_records(items: list[tuple[str, str, str, str]], target_type: str) -> list[dict]:
    return [
        target(item_id, target_type, form, band, function)
        for item_id, form, band, function in items
    ]


def build_registries() -> None:
    registries = {
        "grammar_constructions.json": ("grammar_construction", GRAMMAR),
        "particle_functions.json": ("particle_function", PARTICLES),
        "register_features.json": ("register_feature", REGISTERS),
        "discourse_patterns.json": ("discourse_pattern", DISCOURSE),
        "interactional_functions.json": ("interactional_function", INTERACTIONS),
        "core_interaction_chunks.json": ("core_interaction_chunk", CHUNKS),
        "phonology_features.json": ("phonology_feature", PHONOLOGY),
        "orthography_features.json": ("orthography_feature", ORTHOGRAPHY),
    }
    for filename, (target_type, items) in registries.items():
        records = make_records(items, target_type)
        if target_type == "phonology_feature":
            for record in records:
                record.update(
                    {
                        "perception_goals": [f"{record['canonical_form']}을 구별한다"],
                        "production_goals": [f"{record['canonical_form']}을 산출한다"],
                        "common_confusions": ["철자와 실제 발음을 동일하게 처리함", "인접 음운 환경을 무시함"],
                        "orthography_links": [],
                    }
                )
                record["examples"] = {
                    "representative": [
                        record["canonical_form"],
                        f"{record['canonical_form']} 대표 예시 1",
                        f"{record['canonical_form']} 대표 예시 2",
                        f"{record['canonical_form']} 대표 예시 3",
                    ],
                    "confusions": [
                        f"{record['canonical_form']} 관련 흔한 혼동 1",
                        f"{record['canonical_form']} 관련 흔한 혼동 2",
                    ],
                }
        if target_type == "orthography_feature":
            for record in records:
                record["examples"]["representative"] = [
                    record["canonical_form"],
                    f"{record['canonical_form']} 적용 예시 1",
                    f"{record['canonical_form']} 적용 예시 2",
                    f"{record['canonical_form']} 적용 예시 3",
                ]
                record["examples"]["confusions"] = [
                    f"{record['canonical_form']} 관련 흔한 혼동 1",
                    f"{record['canonical_form']} 관련 흔한 혼동 2",
                ]
        if target_type in {"discourse_pattern", "interactional_function", "core_interaction_chunk"}:
            for record in records:
                record["examples"] = {
                    "situation_examples": [
                        f"생활 상황에서 {record['canonical_form']}",
                        f"서비스 상황에서 {record['canonical_form']}",
                        f"관계 상황에서 {record['canonical_form']}",
                    ],
                    "register_variants": [
                        f"해요체: {record['canonical_form']}",
                        f"관계 거리를 확인한 변형: {record['canonical_form']}",
                    ],
                }
        for record in records:
            if record["target_id"] == "register_online_neologism_boundary":
                record["language_varieties"] = ["neologism"]
                record.update(
                    {
                        "usage_status": "active",
                        "volatility": "high",
                        "last_reviewed_at": "2026-06-19",
                        "age_group_affinity": [],
                        "platform_affinity": [],
                        "default_selection_allowed": False,
                    }
                )
            if record["target_id"] == "register_slang_peer_boundary":
                record["language_varieties"] = ["slang"]
                record.update(
                    {
                        "usage_status": "active",
                        "volatility": "high",
                        "last_reviewed_at": "2026-06-19",
                        "age_group_affinity": [],
                        "platform_affinity": [],
                        "default_selection_allowed": False,
                    }
                )
        dump(MAP / filename, {"registry_type": target_type, "records": records})


ACTIVE_PACK_IDS = [
    "survival_basics", "self_introduction", "daily_routine", "shopping_checkout",
    "cafe_ordering", "restaurant_ordering", "transport_navigation", "directions_location",
    "housing_home", "clinic_pharmacy", "appointments_scheduling",
    "emergency_problem_reporting", "making_friends", "small_talk",
    "preferences_opinions", "invitations_plans", "family_relationships",
    "messaging_calls", "conflict_repair", "delivery_pickup", "banking_payment",
    "public_services", "mobile_internet", "neighborhood_life", "workplace_core",
    "office_work",
]
RESERVED_PACK_IDS = [
    "service_work", "food_service_work", "logistics_work",
    "medical_work", "education_work", "field_work",
]

PACK_SUBS = {
    "survival_basics": ["ask_help", "signal_nonunderstanding", "request_repeat", "close_safely"],
    "self_introduction": ["greet", "say_name", "say_role", "ask_back"],
    "daily_routine": ["morning", "work_or_study", "meal", "evening"],
    "shopping_checkout": ["find_item", "ask_price", "select_quantity", "pay_or_decline"],
    "cafe_ordering": ["order_item", "answer_staff_question", "request_takeout", "correct_order"],
    "restaurant_ordering": ["get_seated", "ask_menu", "order", "request_extra", "pay"],
    "transport_navigation": ["select_route", "buy_or_pay", "board", "transfer", "exit"],
    "directions_location": ["approach", "ask_location", "follow_steps", "confirm_landmark"],
    "housing_home": ["describe_home", "ask_location", "report_issue", "request_service"],
    "clinic_pharmacy": ["state_symptom", "state_duration", "confirm_instruction", "ask_next_step"],
    "appointments_scheduling": ["request_slot", "confirm_time", "reschedule", "cancel"],
    "emergency_problem_reporting": ["get_attention", "state_problem", "state_location", "follow_instruction"],
    "making_friends": ["answer", "react", "ask_back", "find_shared_interest"],
    "small_talk": ["open_topic", "react", "follow_up", "close_topic"],
    "preferences_opinions": ["state_preference", "ask_opinion", "give_reason", "talk_about_hobbies"],
    "invitations_plans": ["invite", "check_availability", "accept_or_decline", "confirm_plan"],
    "family_relationships": ["identify_relation", "describe_person", "state_contact", "manage_privacy"],
    "messaging_calls": ["open", "identify", "request", "repair_delay", "close"],
    "conflict_repair": ["signal_problem", "clarify_intent", "apologize", "agree_next_step"],
    "delivery_pickup": ["identify_order", "check_status", "receive_item", "report_missing_item"],
    "banking_payment": ["state_purpose", "choose_method", "confirm_amount", "report_problem"],
    "public_services": ["identify_service", "ask_process", "complete_form", "confirm_next_step"],
    "mobile_internet": ["choose_plan", "report_issue", "follow_setup", "confirm_service"],
    "neighborhood_life": ["greet_neighbor", "ask_local_info", "manage_noise", "request_help"],
    "workplace_core": ["greet_colleague", "receive_task", "ask_clarification", "report_status"],
    "office_work": ["join_meeting", "coordinate_task", "send_message", "receive_feedback"],
}


def pack(pack_id: str, *, reserved: bool = False) -> dict:
    targets = {
        "cafe_ordering": [
            "chunk_request_noun_juseyo",
            "discourse_short_noun_iyo",
            "interaction_confirm_and_answer",
            "grammar_request_verb_eo_juseyo",
        ],
        "preferences_opinions": [
            "grammar_want_go_sipeoyo",
            "interaction_state_opinion",
            "interaction_ask_back",
        ],
        "survival_basics": [
            "chunk_dont_know_jal_moreugesseoyo",
            "chunk_repeat_dasi_malsseumhae_juseyo",
            "interaction_ask_help",
        ],
    }.get(pack_id, ["register_haeyo_polite", "interaction_confirm_and_answer"])
    return {
        "pack_id": pack_id,
        "status": "reserved" if reserved else "active",
        "runtime_selectable": not reserved,
        "title_ko": pack_id.replace("_", " "),
        "title_en": pack_id.replace("_", " ").title(),
        "level_range": {"min": "A0", "max": "A2"},
        "profile_affinities": ["general_adult_conversation"],
        "sub_situations": PACK_SUBS.get(
            pack_id,
            ["open_interaction", "perform_core_task", "repair_problem", "close_interaction"],
        ),
        "interactional_function_refs": [
            ref for ref in targets if ref.startswith("interaction_")
        ],
        "recommended_language_target_refs": targets[:3],
        "optional_language_target_refs": targets[3:],
        "phonology_focus_refs": ["phonology_question_intonation"],
        "orthography_focus_refs": ["orthography_basic_spacing"],
        "vocabulary_retrieval": {
            "search_intents": [f"{pack_id} communicative vocabulary"],
            "required_semantic_groups": ["people or roles", "actions", "objects or places"],
            "productive_selection_hints": ["mission-critical high-frequency items"],
            "receptive_selection_hints": ["likely counterpart questions and responses"],
            "excluded_default_varieties": ["slang", "neologism", "dialect", "historical", "specialized"],
        },
        "transfer_pack_refs": [],
        "source_refs": [],
    }


def build_packs() -> None:
    dump(SITUATIONS / "active_packs.json", {"packs": [pack(pack_id) for pack_id in ACTIVE_PACK_IDS]})
    dump(
        SITUATIONS / "reserved_packs.json",
        {"packs": [pack(pack_id, reserved=True) for pack_id in RESERVED_PACK_IDS]},
    )


def build_profiles() -> None:
    base = load_json(PROFILES / "general_adult_conversation.json")
    base["priority_situation_refs"] = ACTIVE_PACK_IDS
    dump(PROFILES / "general_adult_conversation.json", base)
    overlays = [
        ("korea_resident_worker", "active", True, ["workplace_core", "office_work", "public_services"]),
        ("heritage_oral", "active", True, ["family_relationships", "making_friends", "daily_routine"]),
        ("heritage_reconnection", "active", True, ["family_relationships", "neighborhood_life", "self_introduction"]),
        ("topik_exam", "reserved", False, []),
    ]
    for profile_id, status, selectable, priorities in overlays:
        dump(
            PROFILES / "overlays" / (
                f"{profile_id}.reserved.json" if status == "reserved" else f"{profile_id}.json"
            ),
            {
                "profile_id": profile_id,
                "profile_type": "overlay",
                "status": status,
                "runtime_selectable": selectable,
                "priority_situation_refs": priorities,
                "skill_imbalance_hints": [],
                "explanation_preferences": ["preserve learner-safe and identity-safe framing"],
                "pronunciation_reading_support": ["adjust only from evidence"],
                "goal_adjustments": ["reprioritize situations without duplicating curriculum"],
                "default_exclusions": ["private identity assumptions", "automatic level gating"],
            },
        )
    dump(
        PROFILES / "profile_manifest.json",
        {
            "schema_version": 1,
            "base_profile_ref": "general_adult_conversation",
            "active_overlay_refs": [
                "korea_resident_worker",
                "heritage_oral",
                "heritage_reconnection",
            ],
            "reserved_overlay_refs": ["topik_exam"],
        },
    )


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    gate = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_language_map.py"),
            "--schema-migration-gate",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if gate.returncode != 0:
        print(gate.stdout.strip())
        raise SystemExit("BLOCKED: population requires the schema and migration gate")
    print(gate.stdout.strip())
    build_registries()
    build_packs()
    build_profiles()
    print("WROTE: A0-A2 language map seed registries, profiles, and situation packs")


if __name__ == "__main__":
    main()
