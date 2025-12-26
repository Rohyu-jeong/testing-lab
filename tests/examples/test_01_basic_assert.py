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
    """기본 사용법 - 이것만 알면 시작할 수 있다

    assert 문의 핵심:
    - assert 뒤에 True가 되는 조건을 쓴다
    - 조건이 False면 테스트가 실패한다
    """

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