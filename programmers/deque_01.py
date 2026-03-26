"""
문제: 스택/큐 > 기능개발
난이도: LEVEL 2
출처: 프로그래머스

[문제 설명]
프로그래머스 팀에서는 기능 개선 작업을 수행 중입니다.
각 기능은 진도가 100%일 때 서비스에 반영할 수 있습니다.

뒤에 있는 기능이 앞에 있는 기능보다 먼저 개발될 수 있고,
이때 뒤에 있는 기능은 앞에 있는 기능이 배포될 때 함께 배포됩니다.

예시:
    progresses = [93, 30, 55], speeds = [1, 30, 5]
    → 첫 번째: 7일, 두 번째: 3일, 세 번째: 9일
    → 7일째: 1,2번 배포(2번은 3일에 끝났지만 1번 기다림) / 9일째: 3번 배포
    → [2, 1]

[제한사항]
- 작업의 개수(progresses, speeds 배열의 길이)는 100개 이하
- 작업 진도는 100 미만의 자연수
- 작업 속도는 100 이하의 자연수
- 배포는 하루에 한 번만 할 수 있으며, 하루의 끝에 이루어진다고 가정

[핵심 개념]
    각 작업의 "완료까지 남은 일수"를 구하면 문제가 단순해진다.
    남은 일수 = ceil((100 - progress) / speed)
    → 앞 작업의 남은 일수보다 작거나 같으면 함께 배포, 크면 새 배포 그룹 시작.
"""

from collections import deque
from math import ceil


# ============================================================
# 풀이 1: while 루프로 남은 일수 계산 (직접 시뮬레이션)
# ------------------------------------------------------------
# 핵심 아이디어:
#   각 작업마다 progress가 100을 넘을 때까지 speed를 반복해서 더하며
#   며칠 걸리는지 직접 센다. 그 뒤 앞 작업과 비교하여 그룹핑.
#   → math를 쓰지 않고 "직접 세보는" 가장 직관적인 방법.
# 시간복잡도: O(n * d) (d: 최대 소요일수, 최악 100일)
# 공간복잡도: O(n)
# ============================================================
def solution1(progresses, speeds):
    # ── 1단계: 각 작업의 소요일수 계산 ──
    days = []
    # zip(progresses, speeds)로 진도와 속도를 한 쌍씩 꺼냄
    # 예: zip([93,30,55], [1,30,5]) → (93,1), (30,30), (55,5)
    for p, s in zip(progresses, speeds):
        cnt = 0
        while p < 100:  # 진도가 100 미만이면 아직 미완성
            p += s       # 하루에 s만큼 진도 증가
            cnt += 1     # 하루 경과
        days.append(cnt) # 이 작업이 며칠 걸리는지 저장
    # 예: progresses=[93,30,55], speeds=[1,30,5]
    #     → days = [7, 3, 9]

    # ── 2단계: 앞 작업 기준으로 그룹핑 ──
    result = [1]            # 첫 번째 작업은 무조건 새 배포 그룹 (1개)
    max_day = days[0]       # 현재 배포 그룹의 기준 일수 (첫 작업 = 7일)

    for i in range(1, len(days)):  # 두 번째 작업부터 순회
        if days[i] <= max_day:
            # 기준보다 빨리 끝남 → 앞 작업이랑 같이 배포
            # result[-1]은 현재 그룹의 개수, 거기에 +1
            result[-1] += 1
        else:
            # 기준보다 늦게 끝남 → 새 배포 그룹 시작
            max_day = days[i]   # 기준 일수 갱신
            result.append(1)    # 새 그룹 추가 (1개부터 시작)
    # 예: days=[7,3,9]
    #     i=1: days[1]=3 <= 7 → 같이 배포, result=[2]
    #     i=2: days[2]=9 > 7  → 새 그룹,   result=[2, 1]

    return result


# ============================================================
# 풀이 2: deque 시뮬레이션 (매일 진도 증가)
# ------------------------------------------------------------
# 핵심 아이디어:
#   실제로 매일 진도를 1씩 올려보는 시뮬레이션 방식.
#   deque를 사용하면 popleft()가 O(1)이라 앞에서 꺼내기 효율적.
#   (list.pop(0)은 O(n)이라 느림)
#   → "큐에서 앞에서부터 꺼내기" 동작을 그대로 구현한 풀이.
# 시간복잡도: O(d * n) (d: 최대 소요일수)
# 공간복잡도: O(n)
# ============================================================
def solution2(progresses, speeds):
    # 리스트를 deque로 변환 (앞에서 꺼낼 때 popleft()가 O(1)으로 빠름)
    progresses = deque(progresses)  # 예: deque([93, 30, 55])
    speeds = deque(speeds)          # 예: deque([1, 30, 5])
    result = []

    while progresses:  # 모든 작업이 빠질 때까지 반복 (하루씩 시뮬레이션)
        # 1. 하루가 지남 → 모든 작업의 진도를 각각의 속도만큼 올림
        for i in range(len(progresses)):
            progresses[i] += speeds[i]
        # 예: 1일차 → deque([94, 60, 60])
        #     2일차 → deque([95, 90, 65])
        #     ...
        #     7일차 → deque([100, 240, 90])

        # 2. 맨 앞 작업이 100% 이상이면 배포! 연속으로 꺼냄
        cnt = 0
        while progresses and progresses[0] >= 100:
            progresses.popleft()  # 완료된 작업 제거
            speeds.popleft()      # 해당 속도도 같이 제거
            cnt += 1
        # 예: 7일차 → progresses[0]=100 제거, progresses[1]=240 제거
        #     → cnt=2, 남은 deque([90])

        # 3. 이번 날에 배포된 기능이 있으면 기록
        if cnt > 0:
            result.append(cnt)  # 예: result = [2]

    return result


# ============================================================
# 풀이 3: math.ceil로 남은 일수 계산
# ------------------------------------------------------------
# 핵심 아이디어:
#   남은 일수 = ceil((100 - progress) / speed)
#   → while 루프 없이 수학 한 줄로 소요일수를 구할 수 있다.
#   그 뒤 그룹핑 로직은 풀이 1과 동일.
#
#   ceil을 쓰는 이유:
#     (100 - 93) / 1 = 7.0  → 딱 떨어짐, 7일
#     (100 - 30) / 30 = 2.33 → 올림해서 3일 (2일엔 아직 90%)
# 시간복잡도: O(n) / 공간복잡도: O(n)
# ============================================================
def solution3(progresses, speeds):
    # ceil((100 - 진도) / 속도)로 소요일수를 바로 계산 (while 루프 필요 없음)
    # 예: ceil((100-93)/1)=7, ceil((100-30)/30)=ceil(2.33)=3, ceil((100-55)/5)=9
    days = [ceil((100 - p) / s) for p, s in zip(progresses, speeds)]
    # 예: days = [7, 3, 9]

    # 그룹핑 로직은 풀이 1과 동일
    result = [1]            # 첫 작업은 새 배포 그룹
    max_day = days[0]       # 기준 일수 = 첫 작업의 소요일수

    for i in range(1, len(days)):  # 두 번째 작업부터 순회
        if days[i] <= max_day:
            result[-1] += 1  # 기준보다 빨리 끝남 → 같이 배포
        else:
            max_day = days[i]   # 기준 갱신
            result.append(1)    # 새 배포 그룹

    return result


# ============================================================
# 풀이 4: deque + math.ceil (큐 + 수학 조합) ⭐ 출제 의도에 가장 부합
# ------------------------------------------------------------
# 핵심 아이디어:
#   math.ceil로 남은 일수를 먼저 계산한 뒤 deque에 넣고,
#   앞에서부터 popleft()로 꺼내며 그룹핑한다.
#   → deque의 "앞에서 꺼내기" + math의 "즉시 계산"을 조합한 풀이.
#
#   deque를 쓰는 이점:
#     - popleft()로 "처리 완료된 작업을 큐에서 제거"하는 동작이 직관적
#     - 큐의 맨 앞(first)이 항상 "다음에 배포할 기준 작업"
# 시간복잡도: O(n) / 공간복잡도: O(n)
# ============================================================
def solution4(progresses, speeds):
    # ceil로 소요일수 계산 → deque에 넣기
    days = deque(ceil((100 - p) / s) for p, s in zip(progresses, speeds))
    # 예: deque([7, 3, 9])

    result = []

    while days:  # deque가 빌 때까지 반복
        # 맨 앞 작업을 꺼내서 이번 배포 그룹의 기준으로 삼음
        max_day = days.popleft()  # 예: 7 꺼냄, days = deque([3, 9])
        cnt = 1                   # 기준 작업 자체가 1개

        # 다음 작업의 소요일이 기준 이하면 → 같이 배포
        while days and days[0] <= max_day:
            days.popleft()  # 예: 3 <= 7이니까 꺼냄, days = deque([9])
            cnt += 1        # 같이 배포할 개수 증가
        # 예: 9 > 7이니까 멈춤, cnt = 2

        result.append(cnt)  # 예: result = [2]
    # 다음 루프: max_day=9, deque 비었으니 cnt=1, result = [2, 1]

    return result


# ============================================================
# 테스트
# ============================================================
if __name__ == "__main__":
    test_cases = [
        # 기본 케이스
        ([93, 30, 55], [1, 30, 5], [2, 1]),
        # 프로그래머스 예제 2
        ([95, 90, 99, 99, 80, 99], [1, 1, 1, 1, 1, 1], [1, 3, 2]),
        # 모든 작업이 같은 날에 끝남
        ([50, 50, 50], [50, 50, 50], [3]),
        # 모든 작업이 다른 날에 끝남 (뒤로 갈수록 느림)
        ([99, 98, 97], [1, 1, 1], [1, 1, 1]),
        # 첫 작업이 가장 오래 걸려서 전부 한꺼번에 배포
        ([10, 90, 90, 90], [1, 1, 1, 1], [4]),
    ]

    solutions = [
        ("풀이 1 (while 직접 계산)",   solution1),
        ("풀이 2 (deque 시뮬레이션)",  solution2),
        ("풀이 3 (math.ceil)",         solution3),
        ("풀이 4 (deque + math.ceil)", solution4),
    ]

    for name, func in solutions:
        print(f"--- {name} ---")
        for progresses, speeds, expected in test_cases:
            result = func(progresses[:], speeds[:])  # 원본 보존을 위해 복사
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}: result={result}, expected={expected}")
        print()
