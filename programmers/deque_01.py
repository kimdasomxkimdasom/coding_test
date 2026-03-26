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
    # 1단계: 각 작업의 소요일수 계산
    days = []
    for p, s in zip(progresses, speeds):
        cnt = 0
        while p < 100:  # p가 100 미만인 동안 계속 더하기
            p += s
            cnt += 1
        days.append(cnt)
    # days 예시: [7, 3, 9] → 첫 번째 7일, 두 번째 3일, 세 번째 9일

    # 2단계: 앞 작업 기준으로 그룹핑
    result = [1]            # 첫 번째 작업은 무조건 새 배포 그룹
    max_day = days[0]       # 현재 배포 그룹의 기준 일수

    for i in range(1, len(days)):
        if days[i] <= max_day:
            # 앞 작업보다 빨리 끝남 → 같이 배포 (현재 그룹에 +1)
            result[-1] += 1
        else:
            # 앞 작업보다 늦게 끝남 → 새 배포 그룹 시작
            max_day = days[i]
            result.append(1)

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
    progresses = deque(progresses)
    speeds = deque(speeds)
    result = []

    while progresses:
        # 1. 매일 모든 작업의 진도를 올림
        for i in range(len(progresses)):
            progresses[i] += speeds[i]

        # 2. 맨 앞 작업이 100% 이상이면 연속으로 꺼냄
        cnt = 0
        while progresses and progresses[0] >= 100:
            progresses.popleft()
            speeds.popleft()
            cnt += 1

        # 3. 이번 날에 배포된 기능이 있으면 기록
        if cnt > 0:
            result.append(cnt)

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
    # 각 작업의 소요일수를 한 줄로 계산
    days = [ceil((100 - p) / s) for p, s in zip(progresses, speeds)]

    result = [1]
    max_day = days[0]

    for i in range(1, len(days)):
        if days[i] <= max_day:
            result[-1] += 1
        else:
            max_day = days[i]
            result.append(1)

    return result


# ============================================================
# 풀이 4: deque + math.ceil (큐 + 수학 조합)
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
    # 남은 일수를 계산해서 deque에 넣기
    days = deque(ceil((100 - p) / s) for p, s in zip(progresses, speeds))

    result = []

    while days:
        # 현재 배포 그룹의 기준 일수 = 큐의 맨 앞 작업
        max_day = days.popleft()
        cnt = 1  # 기준 작업 자체가 1개

        # 다음 작업이 기준 일수 이내에 끝나면 함께 배포
        while days and days[0] <= max_day:
            days.popleft()
            cnt += 1

        result.append(cnt)

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
        all_passed = True
        for progresses, speeds, expected in test_cases:
            result = func(progresses[:], speeds[:])  # 원본 보존을 위해 복사
            status = "PASS" if result == expected else "FAIL"
            if status == "FAIL":
                all_passed = False
                print(f"  {status}: {progresses} → {result} (expected {expected})")
        if all_passed:
            print("  ALL PASSED!")
        print()
