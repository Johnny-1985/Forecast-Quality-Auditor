# Forecast Quality Auditor — SPEC.md (v1.0)

## 1. 목적
포트폴리오 서브 프로젝트. 메인 프로젝트(S&OP Reconciliation Simulator)와 달리 **범용 도구**로 설계 — 특정 업계에 종속되지 않고, 사용자가 자신의 forecast vs actual 엑셀을 업로드하면 바로 진단 가능해야 한다.

## 2. 핵심 원칙
통계 계산(MAPE/WMAPE/Bias/Outlier)은 **결정론적 알고리즘**으로 처리한다 — LLM이 숫자를 "판단"하게 하지 않는다. AI는 오직 **이미 계산된 숫자를 해석하는 내러티브**를 생성할 때만, 그것도 사용자가 명시적으로 요청했을 때만 호출된다. 이게 메인 프로젝트(Agent 논쟁)와 이 프로젝트(통계 감사)의 근본적 차이다.

## 3. Phase 1 범위
- **입력:** 사용자 업로드 .xlsx/.xls/.csv (컬럼 구조 무관 — 업로드 후 사용자가 Period/Forecast/Actual 컬럼을 직접 매핑)
- **지표 3종:**
  - **WMAPE** = Σ|Actual-Forecast| / Σ|Actual| × 100 (0으로 나누기 문제에 강건해 주 지표로 사용)
  - **MAPE** = mean(|Actual-Forecast|/|Actual|) × 100 (참고 지표, Actual=0 구간 제외)
  - **Bias (MPE)** = mean((Forecast-Actual)/Actual) × 100 — 부호로 과대/과소 예측 방향성 표시
  - **Outlier 탐지** — 오차율(%) 기준 IQR 방식(Q1-1.5×IQR ~ Q3+1.5×IQR 벗어나면 이상치)
- **품질 점수 (0~100):** 아래 가중 공식으로 산출, 산식을 사용자에게 그대로 노출(설명 가능성 원칙 유지)
  - WMAPE 구간 (60점 만점): `max(0, 60 - (WMAPE/30)*60)` — 0%면 60점, 30% 이상이면 0점
  - |Bias| 구간 (25점 만점): `max(0, 25 - (|Bias|/15)*25)` — 0%면 25점, 15% 이상이면 0점
  - Outlier 비율 구간 (15점 만점): `max(0, 15 - (outlier_ratio/0.2)*15)` — 이상치 0%면 15점, 20% 이상이면 0점
  - 최종 점수 = 세 구간 합, 0~100 클리핑
- **등급 배너:** 85+ Excellent / 70-84 Good / 50-69 Fair / <50 Needs Attention
- **출력:** 점수 + 지표별 요약 카드 + 이상치 하이라이트된 기간별 테이블 (기본 노출)
- **AI 내러티브 (온디맨드):** "Explain with AI" 버튼 클릭 시에만 Claude API 호출 — 계산된 숫자를 근거로 자연어 해설 생성. 자동 호출 금지 (불필요한 API 비용/지연 방지).

## 4. Phase 1 제외 (다음 단계)
- Missing Data, Seasonality, Trend, Intermittent Demand 지표
- 다중 시트/다중 제품 배치 처리
- 결과 히스토리 저장

## 5. 기술 스택
- 단일 HTML 파일, SheetJS(xlsx.js, cdnjs)로 엑셀/CSV 파싱 — 브라우저에서 전부 처리(서버 불필요)
- 통계 계산은 순수 JS
- AI 내러티브만 Anthropic API 직접 호출 (claude-sonnet-4-6), 온디맨드

## 6. 포트폴리오 서사
"AI를 계산기로 쓰지 않는다"는 원칙을 정확히 보여주는 프로젝트 — 숫자는 알고리즘이, 해석은 AI가, 그리고 그 경계를 사용자가 직접 통제(버튼 클릭)한다는 설계 자체가 실무 감각을 보여준다.
