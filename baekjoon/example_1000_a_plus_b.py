"""
문제: A+B
출처: 백준 1000번 https://www.acmicpc.net/problem/1000
난이도: 브론즈 5
"""
import sys
input = sys.stdin.readline


def solve():
    a, b = map(int, input().split())
    print(a + b)


if __name__ == "__main__":
    solve()
