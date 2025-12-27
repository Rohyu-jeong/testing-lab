# Testing Lab

> pytest 기초, 이것만 알면 Python 학습 테스트를 시작할 수 있다

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![pytest Version](https://img.shields.io/badge/pytest-8.0-green.svg)](https://docs.pytest.org/)

## 📌 소개

이 저장소는 **pytest의 핵심 기능 4가지**만 빠르게 익히는 것을 목표로 합니다.

testing-lab을 학습할 때 필요한 **최소한의 테스트 지식**만 담았습니다.

```
"테스트 도구를 배우느라 정작 Python 공부를 못하면 안 되니까"
```

## 🎯 학습 목표

- pytest **설치부터 실행**까지 완료
- 기본 **assertion**으로 코드 동작 검증
- **parametrize**로 여러 케이스 한 번에 테스트
- **fixture**로 테스트 데이터 재사용

## 🛠 기술 스택

| 구분 | 기술           |
|------|--------------|
| Language | Python 3.10+ |
| Test Framework | pytest 9.0   |

## 📁 프로젝트 구조

```
testing-lab/
├── README.md
├── pyproject.toml
├── requirements.txt
│
└── tests/
    ├── __init__.py
    └── examples/
        ├── __init__.py
        ├── test_01_basic_assert.py      # 기본 assert
        ├── test_02_parametrize.py       # 여러 케이스 한번에
        ├── test_03_exception.py         # 예외 테스트
        └── test_04_fixture_intro.py     # fixture 맛보기
```

## 📚 학습 내용

<details>
<summary><b>01. Basic Assert</b> - 기본 검증 </summary>

| 내용 | 설명 |
|------|------|
| 숫자 비교 | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| 문자열 비교 | `==`, `in`, `startswith` |
| 컬렉션 비교 | `==`, `in`, `len()` |
| 불리언/None | `is True`, `is False`, `is None` |
| 동일성 vs 동등성 | `==` vs `is` |
| 부동소수점 | `pytest.approx()` |

**핵심 포인트**
- pytest는 그냥 `assert`만 쓰면 된다
- 실패하면 pytest가 알아서 상세한 diff를 보여준다
- 특별한 assertion 라이브러리 없이도 충분하다

```python
def test_simple():
    assert 1 + 1 == 2
    assert "hello" in "hello world"
    assert [1, 2, 3] == [1, 2, 3]
```

</details>

<details>
<summary><b>02. Parametrize</b> - 여러 케이스 테스트 </summary>

| 내용 | 설명 |
|------|------|
| 기본 사용법 | `@pytest.mark.parametrize` |
| 단일 파라미터 | 여러 입력값 테스트 |
| 다중 파라미터 | 입력 + 기대값 조합 |
| 케이스 이름 | `pytest.param(id="...")` |

**핵심 포인트**
- 같은 로직을 여러 값으로 테스트할 때 사용
- 테스트 함수 하나로 여러 케이스를 커버
- 경계값 테스트에 특히 유용

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

</details>

<details>
<summary><b>03. Exception</b> - 예외 테스트 </summary>

| 내용 | 설명 |
|------|------|
| 기본 사용법 | `pytest.raises()` |
| 예외 타입 검증 | `pytest.raises(ValueError)` |
| 메시지 검증 | `exc_info.value` |
| 정규식 매칭 | `match="pattern"` |

**핵심 포인트**
- "이 코드는 에러가 나야 정상"인 경우 테스트
- 예외 타입과 메시지 모두 검증 가능

```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

</details>

<details>
<summary><b>04. Fixture Intro</b> - 테스트 데이터 준비 </summary>

| 내용 | 설명 |
|------|------|
| 기본 사용법 | `@pytest.fixture` |
| 데이터 주입 | 테스트 함수 파라미터로 받기 |
| fixture 조합 | fixture가 다른 fixture 사용 |
| setup/teardown | `yield` 활용 |

**핵심 포인트**
- 여러 테스트에서 같은 데이터를 쓸 때 유용
- 테스트 함수 파라미터에 fixture 이름 쓰면 자동 주입

```python
@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_length(sample_list):
    assert len(sample_list) == 3
```

</details>

## 🚀 빠른 시작

### 1. 설치

```bash
pip install pytest
```

### 2. 첫 테스트 작성

```python
# test_hello.py
def test_hello():
    assert "hello" == "hello"
```

### 3. 실행

```bash
pytest
```

끝! 이게 전부입니다.

## 📝 자주 쓰는 명령어

```bash
# 기본 실행
pytest                    # 전체 테스트
pytest test_01.py         # 특정 파일
pytest -v                 # 상세 출력

# 필터링
pytest -k "list"          # 이름에 'list' 포함된 것만

# 디버깅
pytest -x                 # 첫 실패에서 중단
pytest -s                 # print 출력 보기
pytest --tb=short         # 에러 메시지 짧게
```

## ✅ 체크리스트

이 4가지만 할 줄 알면 testing-lab을 시작할 수 있습니다:

- [ ] `assert`로 값 비교하기
- [ ] `@pytest.mark.parametrize`로 여러 케이스 테스트
- [ ] `pytest.raises`로 예외 테스트
- [ ] `@pytest.fixture`로 테스트 데이터 준비

## 💡 이것만 기억하세요

| 상황 | 사용할 것 |
|------|----------|
| 값이 맞는지 확인 | `assert a == b` |
| 여러 값으로 같은 테스트 | `@pytest.mark.parametrize` |
| 에러가 나야 정상 | `pytest.raises(ErrorType)` |
| 테스트마다 같은 데이터 | `@pytest.fixture` |

## ❓ FAQ

### Q: AssertJ 같은 라이브러리 안 써도 되나요?
pytest의 `assert`만으로 충분합니다. 실패 시 자동으로 상세한 diff를 보여줍니다.

### Q: conftest.py는 뭔가요?
여러 파일에서 공유하는 fixture를 모아두는 파일입니다. 지금은 몰라도 됩니다.

### Q: fixture scope는요?
심화 내용입니다. 기본(function)만 알면 됩니다.

### Q: mock은요?
외부 의존성이 있을 때 씁니다. python-basic-lab에서는 필요 없습니다.

## 📖 더 배우고 싶다면

- [pytest 공식 문서](https://docs.pytest.org/)
- [Real Python - pytest](https://realpython.com/pytest-python-testing/)

## 🔗 관련 저장소

| 저장소 | 설명 | 순서 |
|--------|------|------|
| **testing-lab** | pytest 기초 (현재) | 1️⃣ 먼저 |
| python-basic-lab | Python 문법 입문 | 2️⃣ 다음 |
| python-core-lab | Python 내부 구현 | 3️⃣ 나중에 |

---

<div align="center">

**"Test first, understand later"**

*테스트 먼저, 이해는 그 다음*

</div>