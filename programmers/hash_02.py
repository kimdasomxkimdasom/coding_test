"""
문제: 해시 > 의상
난이도: LEVEL 2
출처: 프로그래머스

[문제 설명]
코니는 매일 다른 옷을 조합하여 입는 것을 좋아합니다.

예시:
    종류    이름
    얼굴    동그란 안경, 검정 선글라스
    상의    파란색 티셔츠
    하의    청바지
    겉옷    긴 코트

코니가 가진 의상들이 담긴 2차원 배열 clothes가 주어질 때,
서로 다른 옷의 조합의 수를 return.

[핵심 수학 원리]
    각 종류별로 "안 입는 경우"를 포함하면 (개수 + 1)가지 선택지가 있다.
    모든 종류의 선택지를 곱한 뒤, 아무것도 안 입는 경우 1가지를 빼면 된다.
    예: 얼굴(2+1) × 상의(1+1) × 하의(1+1) × 겉옷(1+1) - 1 = 3×2×2×2 - 1 = 23

[제한사항]
- clothes의 각 행은 [의상의 이름, 의상의 종류]
- 코니가 가진 의상의 수는 1개 이상 30개 이하
- 같은 이름을 가진 의상은 존재하지 않음
- 모든 문자열의 길이는 1 이상 20 이하, 알파벳 소문자 또는 '_'로만 구성
"""

from collections import Counter, defaultdict
from math import prod


# ============================================================
# 풀이 1: Counter 사용
# ------------------------------------------------------------
# 핵심 아이디어:
#   Counter로 종류별 의상 개수를 세고,
#   각 종류마다 (개수 + 1)을 곱한 뒤 1을 뺀다.
# 시간복잡도: O(n) / 공간복잡도: O(n)
# ============================================================
def solution1(clothes):
    # 종류(type)별 개수 세기
    counts = Counter([cloth_type for _, cloth_type in clothes])

    result = 1
    for count in counts.values():
        result *= (count + 1)  # 각 종류별 "안 입는 경우" 포함

    return result - 1  # 아무것도 안 입는 경우 제외


# ============================================================
# 풀이 2: math.prod 사용 (한 줄로 처리)
# ------------------------------------------------------------
# 핵심 아이디어:
#   풀이 1과 동일한 로직을 prod()로 간결하게 표현.
#   prod()는 iterable의 모든 원소를 곱해주는 함수. (Python 3.8+)
# 시간복잡도: O(n) / 공간복잡도: O(n)
# ============================================================
def solution2(clothes):
    counts = Counter([cloth_type for _, cloth_type in clothes])
    return prod(count + 1 for count in counts.values()) - 1


# ============================================================
# 풀이 3: defaultdict 사용
# ------------------------------------------------------------
# 핵심 아이디어:
#   Counter 대신 defaultdict(int)로 직접 카운팅.
#   defaultdict는 없는 키에 접근하면 자동으로 기본값(여기선 0)을 생성.
# 시간복잡도: O(n) / 공간복잡도: O(n)
# ============================================================
def solution3(clothes):
    counts = defaultdict(int)

    for _, cloth_type in clothes:
        counts[cloth_type] += 1

    result = 1
    for count in counts.values():
        result *= (count + 1)
    return result - 1


# ============================================================
# 풀이 4: 순수 딕셔너리만 사용 (import 없이)
# ------------------------------------------------------------
# 핵심 아이디어:
#   dict.get(key, default)을 활용하여 Counter/defaultdict 없이 카운팅.
#   외부 라이브러리 없이 풀어야 할 때 유용.
# 시간복잡도: O(n) / 공간복잡도: O(n)
# ============================================================
def solution4(clothes):
    counts = {}
    for _, cloth_type in clothes:
        counts[cloth_type] = counts.get(cloth_type, 0) + 1

    result = 1
    for count in counts.values():
        result *= (count + 1)
    return result - 1


# ============================================================
# 테스트
# ============================================================
if __name__ == "__main__":
    test_cases = [
        # 기본 케이스: 여러 종류에 여러 의상
        ([["yellow_hat", "headgear"], ["blue_sunglasses", "eyewear"], ["green_turban", "headgear"]],
         5),
        # 한 종류에만 여러 의상
        ([["crow_mask", "face"], ["blue_sunglasses", "face"], ["smoky_makeup", "face"]],
         3),
        # 의상이 1개뿐일 때 → 조합은 1가지
        ([["red_hat", "headgear"]],
         1),
        # 종류가 모두 다를 때 (각 종류에 1개씩)
        ([["a", "top"], ["b", "bottom"], ["c", "shoes"]],
         7),  # (1+1)*(1+1)*(1+1) - 1 = 7
        # 한 종류에 많은 의상
        ([["a", "hat"], ["b", "hat"], ["c", "hat"], ["d", "hat"], ["e", "shoes"]],
         9),  # (4+1)*(1+1) - 1 = 9
    ]

    solutions = [
        ("풀이 1 (Counter)",      solution1),
        ("풀이 2 (prod)",         solution2),
        ("풀이 3 (defaultdict)",  solution3),
        ("풀이 4 (순수 dict)",    solution4),
    ]

    for name, func in solutions:
        print(f"--- {name} ---")
        all_passed = True
        for clothes, expected in test_cases:
            result = func(clothes)
            status = "PASS" if result == expected else "FAIL"
            if status == "FAIL":
                all_passed = False
                print(f"  {status}: {clothes} → {result} (expected {expected})")
        if all_passed:
            print("  ALL PASSED!")
        print()
