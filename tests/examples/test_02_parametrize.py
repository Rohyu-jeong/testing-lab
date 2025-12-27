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


def get_grade(score):
    """점수에 따른 등급을 반환한다"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


def is_valid_username(username):
    """사용자명이 유효한지 검사한다 (3~10자, 영문숫자만)"""
    if not username:
        return False
    if not 3 <= len(username) <= 10:
        return False
    return username.isalnum()


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


class TestVariousPatterns:
    """다양한 패턴 - 상황별 사용법"""

    @pytest.mark.parametrize("score, expected", [
        (100, "A"),  # 최대값
        (90, "A"),   # A 최소 경계
        (89, "B"),   # A 바로 아래 → B
        (80, "B"),   # B 최소 경계
        (79, "C"),   # B 바로 아래 → C
        (70, "C"),   # C 최소 경계
        (69, "D"),   # C 바로 아래 → D
        (60, "D"),   # D 최소 경계
        (59, "F"),   # D 바로 아래 → F
        (0, "F"),    # 최소값
    ])
    def test_boundary_values(self, score, expected):
        """경계값 테스트 - 버그가 가장 많이 발생하는 지점"""
        # 왜 경계값인가?
        #   - if score >= 90 에서 89와 90의 차이가 중요
        #   - off-by-one 에러가 가장 많이 발생하는 지점
        assert get_grade(score) == expected

    @pytest.mark.parametrize("username, expected", [
        pytest.param("abc", True, id="최소길이_3자"),
        pytest.param("user123", True, id="영문숫자_혼합"),
        pytest.param("abcdefghij", True, id="최대길이_10자"),
        pytest.param("", False, id="빈문자열"),
        pytest.param("ab", False, id="너무짧음_2자"),
        pytest.param("abcdefghijk", False, id="너무김_11자"),
        pytest.param("user@name", False, id="특수문자_포함"),
    ])
    def test_with_descriptive_ids(self, username, expected):
        """pytest.param으로 의미있는 테스트 이름 부여"""
        # 실행 결과:
        #   test_with_descriptive_ids[최소길이_3자] PASSED
        #   test_with_descriptive_ids[빈문자열] PASSED
        #
        # id를 사용하면:
        #   - 실패 시 어떤 케이스인지 바로 파악 가능
        #   - 테스트 리포트가 읽기 쉬워짐
        assert is_valid_username(username) == expected

    @pytest.mark.parametrize("a", [1, 2])
    @pytest.mark.parametrize("b", [10, 20])
    def test_combinations(self, a, b):
        """여러 @parametrize 조합 - 모든 경우의 수 테스트"""
        # 2 x 2 = 4개 조합이 자동 생성됨:
        #   (a=1, b=10), (a=1, b=20), (a=2, b=10), (a=2, b=20)
        #
        # 언제 유용한가?
        #   - 여러 독립 변수의 조합을 테스트할 때
        #   - 예: 브라우저 x 화면크기, 언어 x 지역
        assert add(a, b) == a + b


class TestCommonMistakes:
    """흔한 실수 - 이렇게 하면 안 된다"""

    # 잘못된 예 - 실행하면 에러 발생
    # @pytest.mark.parametrize("a, b", [(1, 2, 3)])  # 변수 2개, 값 3개

    @pytest.mark.parametrize("a, b, c", [
        (1, 2, 3),
        (4, 5, 9),
    ])
    def test_param_count_must_match(self, a, b, c):
        """파라미터 개수 = 튜플 요소 개수"""
        # 규칙: "a, b, c" → 3개 변수 → 튜플도 3개 요소
        assert a + b == c

    # 잘못된 예 - 실행하면 TypeError
    # @pytest.mark.parametrize("value", 1)

    @pytest.mark.parametrize("value", [1])
    def test_value_must_be_in_list(self, value):
        """단일 값도 반드시 리스트로 감싸야 한다"""
        assert value == 1

    # 주의: 문자열은 iterable이므로 각 문자가 분리됨!
    # @pytest.mark.parametrize("char", "abc")
    # → 'a', 'b', 'c' 3개의 테스트가 생성됨

    @pytest.mark.parametrize("text", ["abc"])
    def test_string_must_be_wrapped(self, text):
        """문자열 하나를 전달하려면 리스트로 감싸야 한다"""
        # ["abc"] → 1개 테스트, text="abc"
        # "abc"   → 3개 테스트, text='a', 'b', 'c'
        assert text == "abc"

    # 나쁜 패턴
    # def test_without_parametrize(self):
    #     assert add(1, 2) == 3
    #     assert add(0, 0) == 0  # 위에서 실패하면 여기는 실행 안 됨
    #     assert add(-1, 1) == 0

    @pytest.mark.parametrize("a, b, expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ])
    def test_each_case_runs_independently(self, a, b, expected):
        """parametrize 사용 - 모든 값이 독립적으로 실행됨"""
        # 장점:
        #   - 하나가 실패해도 나머지는 계속 실행
        #   - 어떤 값에서 실패했는지 명확히 알 수 있음
        assert add(a, b) == expected

