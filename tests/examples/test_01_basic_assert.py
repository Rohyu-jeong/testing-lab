"""
pytest 기초 - 기본 Assertion
============================
학습 목표: assert 문으로 값을 검증하는 방법 익히기

사용 상황:
- 함수의 반환값이 예상과 같은지 확인할 때
- 두 값이 같거나 다른지 비교할 때
- 컬렉션(리스트, 딕셔너리)에 특정 값이 있는지 확인할 때
- None이나 True/False인지 확인할 때
"""

import pytest


class TestBasicUsage:

    def test_equal(self):
        """두 값이 같은지 확인 (==)"""
        result = 1 + 1
        assert result == 2

    def test_not_equal(self):
        """두 값이 다른지 확인 (!=)"""
        result = 1 + 1
        assert result != 3

    def test_contains(self):
        """포함 여부 확인 (in)"""
        fruits = ["apple", "banana", "cherry"]
        assert "apple" in fruits
        assert "grape" not in fruits

    def test_is_none(self):
        """None인지 확인 (is None)"""
        result = None
        assert result is None

    def test_is_not_none(self):
        """None이 아닌지 확인 (is not None)"""
        result = "something"
        assert result is not None

    def test_is_true_false(self):
        """True/False인지 확인 (is True, is False)"""
        success = True
        failed = False
        assert success is True
        assert failed is False


class TestVariousPatterns:
    """다양한 패턴 - 상황별 사용법"""

    # --- 숫자 비교 ---

    def test_number_comparison(self):
        """숫자 크기 비교: <, >, <=, >="""
        value = 10
        assert value > 5    # 크다
        assert value < 20   # 작다
        assert value >= 10  # 크거나 같다
        assert value <= 10  # 작거나 같다

    def test_number_range(self):
        """숫자가 범위 안에 있는지 확인"""
        score = 85
        # Python은 연쇄 비교가 가능하다
        assert 0 <= score <= 100

    # --- 문자열 비교 ---

    def test_string_contains(self):
        """문자열에 특정 문자가 포함되어 있는지"""
        message = "hello world"
        assert "world" in message
        assert "python" not in message

    def test_string_startswith_endswith(self):
        """문자열의 시작과 끝 확인"""
        filename = "report_2024.pdf"
        assert filename.startswith("report")
        assert filename.endswith(".pdf")

    # --- 리스트 비교 ---

    def test_list_equal(self):
        """리스트가 같은지 확인 (순서 포함)"""
        result = [1, 2, 3]
        # 리스트 비교는 순서까지 같아야 한다
        assert result == [1, 2, 3]
        assert result != [3, 2, 1]

    def test_list_length(self):
        """리스트 길이 확인"""
        items = [1, 2, 3, 4, 5]
        assert len(items) == 5

    # --- 딕셔너리 비교 ---

    def test_dict_equal(self):
        """딕셔너리가 같은지 확인"""
        user = {"name": "Alice", "age": 30}
        assert user == {"name": "Alice", "age": 30}

    def test_dict_key_exists(self):
        """딕셔너리에 특정 키가 있는지"""
        config = {"host": "localhost", "port": 8080}
        # in은 딕셔너리의 키를 확인한다
        assert "host" in config
        assert "password" not in config

    def test_dict_value_check(self):
        """딕셔너리의 특정 키 값 확인"""
        user = {"name": "Alice", "age": 30}
        assert user["name"] == "Alice"
        assert user["age"] == 30

    # --- Truthy / Falsy ---

    def test_truthy_falsy(self):
        """Truthy/Falsy - 빈 값 체크에 유용

        Falsy: False, None, 0, "", [], {}
        Truthy: 그 외 모든 값
        """
        # 빈 값들은 falsy
        assert not ""
        assert not []
        assert not {}
        assert not 0

        # 내용이 있는 값들은 truthy
        assert "hello"
        assert [1, 2, 3]
        assert {"a": 1}
        assert 42


class TestCommonMistakes:
    """흔한 실수 - 이렇게 하면 안 된다"""

    def test_is_vs_equal(self):
        """[실수] 값 비교에 is를 사용하면 안 된다

        is: 같은 객체인가? (동일성)
        ==: 값이 같은가? (동등성)
        """
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]

        # 잘못된 방법: 값 비교에 is 사용
        # assert list1 is list2  # 실패! 다른 객체이므로

        # 올바른 방법: 값 비교에 == 사용
        assert list1 == list2

    def test_none_with_is(self):
        """[실수] None 비교에 ==를 사용하면 안 된다"""
        value = None

        # 잘못된 방법
        # assert value == None  # 동작은 하지만 PEP 8 위반

        # 올바른 방법: None은 싱글톤이므로 is 사용
        assert value is None

    def test_float_with_approx(self):
        """[실수] 부동소수점을 ==로 직접 비교하면 안 된다"""
        result = 0.1 + 0.2

        # 잘못된 방법
        # assert result == 0.3  # 실패! 0.30000000000000004

        # 올바른 방법: pytest.approx() 사용
        assert result == pytest.approx(0.3)


class TestTips:
    """꿀팁 - 알아두면 유용한 것들"""

    def test_assert_message(self):
        """실패 시 원인 파악을 위한 메시지 추가"""
        value = 42
        # 쉼표 뒤에 메시지를 추가하면 실패 시 출력된다
        assert value > 0, f"값이 양수여야 합니다. 현재 값: {value}"

    def test_approx_tolerance(self):
        """pytest.approx()에 허용 오차 지정하기"""
        # rel: 상대 오차 (비율)
        assert 99.5 == pytest.approx(100, rel=0.01)  # 1% 오차 허용

        # abs: 절대 오차 (고정값)
        assert 99.5 == pytest.approx(100, abs=0.5)  # 0.5 차이 허용

    def test_approx_collection(self):
        """리스트/딕셔너리의 부동소수점도 approx로 비교"""
        result_list = [0.1 + 0.1, 0.1 + 0.2]
        assert result_list == pytest.approx([0.2, 0.3])

        result_dict = {"x": 0.1 + 0.2}
        assert result_dict == pytest.approx({"x": 0.3})
        