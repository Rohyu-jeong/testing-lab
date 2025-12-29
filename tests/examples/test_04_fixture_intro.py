"""
pytest 기초 - Fixture 맛보기
===========================
학습 목표: fixture로 테스트 데이터를 준비하고 정리하는 방법

사용 상황:
- 여러 테스트에서 같은 데이터를 사용할 때
- 테스트 전에 준비 작업이 필요할 때
- 테스트 후에 정리 작업이 필요할 때
- 복잡한 객체를 미리 만들어두고 싶을 때
"""

import pytest


# Fixture 정의 - 테스트에서 사용할 데이터를 미리 준비
# 이 파일 안에서만 쓰는 fixture는 여기에 정의
# 여러 파일에서 공유하려면 conftest.py에 정의 (import 없이 자동 인식)

@pytest.fixture
def sample_list():
    """단순한 리스트를 제공하는 fixture"""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def sample_dict():
    """단순한 딕셔너리를 제공하는 fixture"""
    return {"name": "python", "version": 3}


@pytest.fixture
def empty_list():
    """빈 리스트를 제공하는 fixture"""
    return []


class TestBasicUsage:
    """기본 사용법 - 이것만 알면 시작할 수 있다"""

    def test_fixture_injection(self, sample_list):
        """fixture는 함수 파라미터로 받아서 사용한다"""
        # sample_list fixture가 자동으로 주입됨
        # 테스트 함수 파라미터 이름 = fixture 함수 이름
        assert sample_list == [1, 2, 3, 4, 5]
        assert len(sample_list) == 5

    def test_fixture_provides_fresh_data(self, sample_list):
        """각 테스트는 새로운 fixture 데이터를 받는다"""
        # 이전 테스트에서 sample_list를 수정해도
        # 이 테스트는 새로운 [1, 2, 3, 4, 5]를 받음
        sample_list.append(6)
        assert len(sample_list) == 6

    def test_fixture_still_fresh(self, sample_list):
        """위에서 append(6)을 했지만 여기는 영향 없음"""
        # fixture는 매번 새로 실행됨
        assert sample_list == [1, 2, 3, 4, 5]
        assert 6 not in sample_list

    def test_multiple_fixtures(self, sample_list, sample_dict):
        """여러 fixture를 동시에 사용할 수 있다"""
        # 필요한 만큼 파라미터로 받으면 됨
        assert len(sample_list) == 5
        assert sample_dict["name"] == "python"


class TestFixtureDependency:
    """Fixture 간 의존성 - fixture가 다른 fixture를 사용"""

    # fixture가 다른 fixture를 파라미터로 받을 수 있음

    @pytest.fixture
    def doubled_list(self, sample_list):
        """sample_list의 각 원소를 2배로 만든 리스트"""
        return [x * 2 for x in sample_list]

    @pytest.fixture
    def list_with_sum(self, sample_list):
        """리스트와 합계를 함께 제공"""
        return {
            "items": sample_list,
            "total": sum(sample_list)
        }

    def test_dependent_fixture(self, doubled_list):
        """다른 fixture에 의존하는 fixture 사용"""
        # doubled_list는 내부적으로 sample_list를 사용
        assert doubled_list == [2, 4, 6, 8, 10]

    def test_fixture_with_computed_value(self, list_with_sum):
        """계산된 값을 포함하는 fixture"""
        assert list_with_sum["items"] == [1, 2, 3, 4, 5]
        assert list_with_sum["total"] == 15


class TestFixtureWithYield:
    """Setup과 Teardown - yield로 정리 작업하기"""

    @pytest.fixture
    def resource_with_cleanup(self):
        """
        yield 전: setup (준비)
        yield 값: 테스트에서 사용할 데이터
        yield 후: teardown (정리)
        """
        # Setup: 테스트 전에 실행
        data = {"status": "created", "items": []}
        print("\n[Setup] 리소스 생성됨")

        yield data  # 이 값이 테스트에 전달됨

        # Teardown: 테스트 후에 실행 (성공/실패 상관없이)
        data.clear()
        print("[Teardown] 리소스 정리됨")

    @pytest.fixture
    def temp_file_simulation(self):
        """파일 생성/삭제를 시뮬레이션하는 fixture"""
        # 실제로는 파일을 만들지 않고 시뮬레이션
        file_info = {"name": "test.txt", "exists": True}
        print(f"\n[Setup] 파일 생성: {file_info['name']}")

        yield file_info

        file_info["exists"] = False
        print(f"[Teardown] 파일 삭제: {file_info['name']}")

    def test_resource_is_ready(self, resource_with_cleanup):
        """yield 이전 코드가 실행된 후 테스트 시작"""
        assert resource_with_cleanup["status"] == "created"
        resource_with_cleanup["items"].append("test_item")

    def test_cleanup_runs_after(self, resource_with_cleanup):
        """각 테스트 후 정리 코드가 실행됨"""
        # 이전 테스트에서 추가한 item이 없음
        # (새로운 fixture 인스턴스이므로)
        assert resource_with_cleanup["items"] == []

    def test_temp_file_available(self, temp_file_simulation):
        """임시 파일이 테스트 중에는 존재"""
        assert temp_file_simulation["exists"] is True
        assert temp_file_simulation["name"] == "test.txt"


class TestPracticalExamples:
    """실용적인 예제 - 이런 상황에서 fixture를 쓴다"""

    @pytest.fixture
    def user_data(self):
        """사용자 데이터 fixture"""
        return {
            "id": 1,
            "name": "홍길동",
            "email": "hong@example.com",
            "active": True
        }

    @pytest.fixture
    def shopping_cart(self):
        """장바구니 fixture"""
        return {
            "items": [],
            "total": 0
        }

    @pytest.fixture
    def cart_with_items(self, shopping_cart):
        """상품이 담긴 장바구니"""
        shopping_cart["items"] = [
            {"name": "사과", "price": 1000, "qty": 3},
            {"name": "바나나", "price": 500, "qty": 5}
        ]
        shopping_cart["total"] = 1000 * 3 + 500 * 5
        return shopping_cart

    def test_user_is_active(self, user_data):
        """사용자 활성 상태 확인"""
        assert user_data["active"] is True
        assert "@" in user_data["email"]

    def test_empty_cart(self, shopping_cart):
        """빈 장바구니 테스트"""
        assert shopping_cart["items"] == []
        assert shopping_cart["total"] == 0

    def test_cart_total(self, cart_with_items):
        """장바구니 합계 테스트"""
        assert len(cart_with_items["items"]) == 2
        assert cart_with_items["total"] == 5500  # 3000 + 2500

