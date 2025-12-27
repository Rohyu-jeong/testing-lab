"""
pytest 기초 - 파라미터화 테스트
==============================
학습 목표: 하나의 테스트 함수로 여러 입력값을 검증하는 방법

사용 상황:
- 같은 로직을 다양한 입력값으로 테스트하고 싶을 때
- 테스트 코드 중복을 줄이고 싶을 때
- 어떤 입력에서 실패했는지 명확하게 알고 싶을 때
"""

import pytest


# 테스트 대상 함수들
# 실제 프로젝트에서는 from my_module import add 처럼 가져온다
# 여기서는 학습을 위해 같은 파일에 작성


def add(a, b):
    """두 수를 더한다"""
    return a + b


class TestBasicUsage:
    """기본 사용법 - 이것만 알면 시작할 수 있다"""

    @pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
    def test_single_param(self, number):
        """단일 파라미터 - 가장 기본적인 형태"""
        # 이 테스트는 5번 실행된다:
        #   test_single_param[1] → number=1
        #   test_single_param[2] → number=2
        #   ...
        #
        # 장점:
        #   - 각 값이 독립적인 테스트로 실행됨
        #   - 하나가 실패해도 나머지는 계속 실행됨
        #   - 어떤 값에서 실패했는지 즉시 알 수 있음
        assert number > 0

    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ])
    def test_multiple_params(self, a, b, expected):
        """다중 파라미터 - 입력값과 기대값을 함께 전달"""
        # 가장 흔한 패턴: (입력1, 입력2, 기대값)
        # 튜플의 요소 개수 = 변수 개수 (반드시 일치해야 함)
        assert add(a, b) == expected