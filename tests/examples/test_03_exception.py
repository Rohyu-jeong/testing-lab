"""
pytest 기초 - 예외 테스트
========================
학습 목표: pytest.raises를 사용하여 예외 발생을 검증하는 방법

사용 상황:
- 잘못된 입력에 대해 적절한 예외가 발생하는지 확인할 때
- 예외 메시지가 올바른지 검증할 때
- 에러 처리 로직이 제대로 동작하는지 테스트할 때
"""

import pytest


class TestBasicUsage:
    """기본 사용법 - pytest.raises로 예외 잡기"""

    def test_raises_basic(self):
        """with문으로 예외가 발생하는지 확인"""
        # pytest.raises는 context manager로 사용
        # with 블록 안에서 지정한 예외가 발생하면 테스트 통과
        # 예외가 발생하지 않거나 다른 예외가 발생하면 테스트 실패
        with pytest.raises(ZeroDivisionError):
            1 / 0

    def test_raises_common_exceptions(self):
        """자주 사용하는 예외 타입들"""
        # ValueError: 값이 잘못됐을 때
        with pytest.raises(ValueError):
            int("hello")

        # KeyError: 딕셔너리에 없는 키 접근
        with pytest.raises(KeyError):
            {"a": 1}["b"]

        # TypeError: 타입이 맞지 않을 때
        with pytest.raises(TypeError):
            "hello" + 123

        # IndexError: 리스트 범위 초과
        with pytest.raises(IndexError):
            [1, 2, 3][10]

    def test_exception_info(self):
        """as 절로 예외 정보 가져오기"""
        # as exc_info로 예외 정보를 담은 객체를 받을 수 있음
        with pytest.raises(ValueError) as exc_info:
            int("hello")

        # exc_info.type: 발생한 예외의 클래스
        assert exc_info.type is ValueError

        # exc_info.value: 실제 예외 객체 (메시지 포함)
        # str()로 변환하면 예외 메시지를 얻을 수 있음
        assert "invalid literal" in str(exc_info.value)

    def test_match_parameter(self):
        """match로 예외 메시지 패턴 확인"""
        # 같은 예외 타입이라도 발생 원인이 다를 수 있음
        # match로 메시지를 확인해서 의도한 곳에서 발생했는지 구분
        with pytest.raises(ValueError, match="invalid"):
            int("hello")