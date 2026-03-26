"""
문제: 해시 > 베스트앨범
난이도: LEVEL 3
출처: 프로그래머스

[문제 설명]
스트리밍 사이트에서 장르 별로 가장 많이 재생된 노래를 두 개씩 모아 베스트 앨범을 출시하려 합니다.

수록 기준:
    1. 속한 노래가 많이 재생된 장르를 먼저 수록
    2. 장르 내에서 많이 재생된 노래를 먼저 수록
    3. 장르 내에서 재생 횟수가 같으면 고유 번호가 낮은 노래를 먼저 수록

[제한사항]
- genres[i]는 고유번호가 i인 노래의 장르
- plays[i]는 고유번호가 i인 노래의 재생 횟수
- genres와 plays의 길이는 같으며, 1 이상 10,000 이하
- 장르 종류는 100개 미만
- 장르에 속한 곡이 하나라면, 하나의 곡만 선택
- 모든 장르는 재생된 횟수가 다름
"""

from collections import defaultdict


# ============================================================
# 풀이 1: 딕셔너리 하나로 처리
# ------------------------------------------------------------
# 핵심 아이디어:
#   genre_songs 딕셔너리에 장르별 노래 목록을 저장하고,
#   장르 정렬 시 sum()으로 총 재생횟수를 계산한다.
#   구현이 직관적이지만, 정렬할 때마다 sum을 반복 계산하는 비효율이 있다.
# 시간복잡도: O(n log n) / 공간복잡도: O(n)
# ============================================================
def solution1(genres, plays):
    result = []
    genre_songs = {}  # {장르: [(재생횟수, 고유번호), ...]}

    for i in range(len(genres)):
        genre = genres[i]
        play = plays[i]

        if genre not in genre_songs:
            genre_songs[genre] = []
        genre_songs[genre].append((play, i))

    # 장르별 총 재생횟수 기준 내림차순 정렬
    sorted_genres = sorted(
        genre_songs.keys(),
        key=lambda g: sum(play for play, _ in genre_songs[g]),
        reverse=True,
    )

    for genre in sorted_genres:
        songs = genre_songs[genre]
        # 재생횟수 내림차순 → 같으면 고유번호 오름차순
        songs.sort(key=lambda x: (-x[0], x[1]))
        # 최대 2곡만 수록
        result.extend([idx for _, idx in songs[:2]])

    return result


# ============================================================
# 풀이 2: 총 재생횟수를 미리 계산 (개선된 버전) ⭐ 출제 의도에 가장 부합
# ------------------------------------------------------------
# 핵심 아이디어:
#   genre_total 딕셔너리에 장르별 총 재생횟수를 미리 누적해두어,
#   정렬 시 sum()을 반복 호출하지 않도록 개선.
#   → 데이터가 클 때 풀이 1보다 효율적.
# 시간복잡도: O(n log n) / 공간복잡도: O(n)
# ============================================================
def solution2(genres, plays):
    result = []
    genre_songs = {}   # 장르별 노래 목록
    genre_total = {}   # 장르별 총 재생횟수

    for i in range(len(genres)):
        genre = genres[i]
        play = plays[i]

        # 장르별 노래 목록 업데이트
        if genre not in genre_songs:
            genre_songs[genre] = []
        genre_songs[genre].append((play, i))
        genre_total[genre] = genre_total.get(genre, 0) + play

    # 미리 계산된 총 재생횟수로 정렬 (sum 반복 호출 제거)
    sorted_genres = sorted(genre_total, key=genre_total.get, reverse=True)

    for genre in sorted_genres:
        songs = genre_songs[genre]
        # 재생횟수 내림차순 → 같으면 고유번호 오름차순
        # x[0]은 재생횟수, x[1]은 고유번호
        # -x[0]으로 내림차순, x[1]으로 오름차순 정렬
        songs.sort(key=lambda x: (-x[0], x[1]))

        # 최대 2곡만 수록
        result.extend([idx for _, idx in songs[:2]])

    return result


# ============================================================
# 풀이 3: defaultdict + enumerate 활용 (간결한 버전)
# ------------------------------------------------------------
# 핵심 아이디어:
#   defaultdict로 초기화 코드를 줄이고,
#   enumerate + zip으로 인덱스를 더 파이썬답게 처리.
# 시간복잡도: O(n log n) / 공간복잡도: O(n)
# ============================================================
def solution3(genres, plays):
    genre_songs = defaultdict(list)   # 장르별 노래 목록
    genre_total = defaultdict(int)    # 장르별 총 재생횟수

    for i, (genre, play) in enumerate(zip(genres, plays)):
        genre_songs[genre].append((play, i))
        genre_total[genre] += play

    result = []
    for genre in sorted(genre_total, key=genre_total.get, reverse=True):
        # 재생횟수 내림차순, 고유번호 오름차순으로 정렬 후 최대 2곡 수록
        top2 = sorted(genre_songs[genre], key=lambda x: (-x[0], x[1]))[:2]
        result.extend([idx for _, idx in top2])

    return result


# ============================================================
# 테스트
# ============================================================
if __name__ == "__main__":
    test_cases = [
        # 기본 케이스
        (
            ["classic", "pop", "classic", "classic", "pop"],
            [500, 600, 150, 800, 2500],
            [4, 1, 3, 0],  # pop(3100) → 4,1 / classic(1450) → 3,0
        ),
        # 장르가 1개뿐일 때
        (
            ["rock", "rock", "rock"],
            [100, 300, 200],
            [1, 2],  # 300(idx1), 200(idx2)
        ),
        # 장르에 곡이 1개뿐일 때 → 1곡만 수록
        (
            ["pop", "jazz"],
            [1000, 500],
            [0, 1],  # pop → 0 / jazz → 1
        ),
        # 같은 장르 내 재생횟수가 동일할 때 → 고유번호가 낮은 것 우선
        (
            ["dance", "dance", "dance"],
            [100, 100, 100],
            [0, 1],  # 재생횟수 동일 → 고유번호 0, 1 선택
        ),
        # 장르가 3개 이상일 때
        (
            ["pop", "rock", "jazz", "pop", "rock", "jazz"],
            [500, 200, 100, 600, 300, 50],
            [3, 0, 4, 1, 2, 5],  # pop(1100)→3,0 / rock(500)→4,1 / jazz(150)→2,5
        ),
    ]

    solutions = [
        ("풀이 1 (기본 dict)",         solution1),
        ("풀이 2 (total 미리 계산)",   solution2),
        ("풀이 3 (defaultdict+zip)",   solution3),
    ]

    for name, func in solutions:
        print(f"--- {name} ---")
        for genres, plays, expected in test_cases:
            result = func(genres, plays)
            status = "PASS" if result == expected else "FAIL"
            print(f"  {status}: result={result}, expected={expected}")
        print()
