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


class TestVariousPatterns:
    """다양한 패턴 - assert와 parametrize 응용"""

    def test_assert_exception_message(self):
        """assert로 예외 메시지 검증"""
        def divide(a, b):
            if b == 0:
                raise ValueError("0으로 나눌 수 없습니다")
            return a / b

        with pytest.raises(ValueError) as exc_info:
            divide(10, 0)

        # exc_info.value를 문자열로 변환해서 메시지 추출
        message = str(exc_info.value)

        # 1번에서 배운 assert로 메시지 검증
        # 정확히 일치하는지 확인
        assert message == "0으로 나눌 수 없습니다"

        # 특정 문자열이 포함되어 있는지 확인
        assert "0" in message

    @pytest.mark.parametrize("invalid_value", [
        "hello",
        "abc",
        "!@#",
    ])
    def test_parametrize_single_exception(self, invalid_value):
        """parametrize로 여러 잘못된 입력 테스트"""
        # 2번에서 배운 parametrize로 여러 케이스를 한번에 테스트
        # 모든 invalid_value에 대해 ValueError가 발생해야 함
        with pytest.raises(ValueError):
            int(invalid_value)

    @pytest.mark.parametrize("value,expected_exception", [
        ("hello", ValueError),   # 문자열 -> ValueError
        (None, TypeError),       # None -> TypeError
    ])
    def test_parametrize_different_exceptions(self, value, expected_exception):
        """parametrize로 입력별 다른 예외 테스트"""
        def to_int(x):
            if x is None:
                raise TypeError("None은 변환 불가")
            return int(x)

        # 입력값에 따라 다른 예외가 발생하는 것을 테스트
        # expected_exception에 예외 클래스를 넣어서 동적으로 검증
        with pytest.raises(expected_exception):
            to_int(value)

    @pytest.mark.parametrize("value,error_message", [
        pytest.param(-1, "음수", id="negative"),
        pytest.param(101, "100 초과", id="over_100"),
    ])
    def test_parametrize_with_message_check(self, value, error_message):
        """parametrize + match 조합"""
        def validate_score(score):
            if score < 0:
                raise ValueError("음수는 안 됨")
            if score > 100:
                raise ValueError("100 초과는 안 됨")
            return score

        # parametrize로 여러 케이스 + match로 메시지 검증
        # pytest.param의 id는 테스트 실행 시 어떤 케이스인지 보여줌
        with pytest.raises(ValueError, match=error_message):
            validate_score(value)

    def test_multiple_exception_types(self):
        """여러 예외 타입 중 하나 기대"""
        def process(value):
            if value is None:
                raise TypeError("None 안 됨")
            if value < 0:
                raise ValueError("음수 안 됨")
            return value

        # 튜플로 여러 예외 타입 지정 가능
        # 둘 중 하나가 발생하면 테스트 통과
        # 어떤 예외가 발생할지 정확히 모를 때 유용
        with pytest.raises((TypeError, ValueError)):
            process(None)

        with pytest.raises((TypeError, ValueError)):
            process(-1)

    def test_multiple_asserts_after_catch(self):
        """예외 잡은 후 여러 검증 수행"""
        def parse(text):
            if not text:
                raise ValueError("빈 문자열 불가")
            return int(text)

        with pytest.raises(ValueError) as exc_info:
            parse("")

        # with 블록이 끝난 후에 exc_info를 사용해서
        # 여러 가지 검증을 자유롭게 수행할 수 있음
        assert exc_info.type is ValueError
        assert "빈 문자열" in str(exc_info.value)
        assert str(exc_info.value) == "빈 문자열 불가"


class TestCommonMistakes:
    """흔한 실수 - 이렇게 하면 안 된다"""

    def test_wrong_exception_type(self):
        """잘못된 예외 타입을 기대하면 테스트 실패"""
        # int("hello")는 ValueError를 발생시킴
        # 만약 TypeError를 기대하면 테스트가 실패함
        #
        # 잘못된 예:
        # with pytest.raises(TypeError):  # 실패!
        #     int("hello")

        # 올바른 예: 실제 발생하는 예외 타입을 지정
        with pytest.raises(ValueError):
            int("hello")

    def test_no_exception_means_failure(self):
        """예외가 발생하지 않으면 테스트 실패"""
        # pytest.raises는 예외가 반드시 발생해야 통과
        # 정상 동작하는 코드를 넣으면 테스트 실패
        #
        # 잘못된 예:
        # with pytest.raises(ValueError):
        #     int("123")  # 정상 동작 -> 예외 없음 -> 테스트 실패

        # 예외가 없어야 하는 경우는 pytest.raises 없이 그냥 실행
        result = int("123")
        assert result == 123

    def test_exception_outside_block(self):
        """예외는 with 블록 안에서 발생해야 함"""
        # pytest.raises는 with 블록 안의 예외만 잡음
        # 블록 밖에서 예외가 발생하면 테스트 자체가 실패
        #
        # 잘못된 예:
        # x = int("hello")  # 여기서 예외 발생 -> 테스트 실패!
        # with pytest.raises(ValueError):
        #     pass

        # 올바른 예: 예외 발생 코드를 with 블록 안에 넣기
        with pytest.raises(ValueError):
            int("hello")

    def test_avoid_broad_exception(self):
        """Exception은 너무 광범위"""
        # Exception은 모든 예외의 부모 클래스
        # 이걸로 잡으면 어떤 예외든 통과해버림

        # 광범위한 예 (권장하지 않음):
        with pytest.raises(Exception):
            int("hello")

        # 구체적인 예 (권장):
        # 실제로 발생하는 예외 타입을 명시하면
        # 의도하지 않은 예외를 잡는 실수를 방지할 수 있음
        with pytest.raises(ValueError):
            int("hello")

