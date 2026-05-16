---
name: python-testing
description: Python testing standards, patterns, and best practices
---

## Mandatory Rules

### Pre-Change Gate

All existing tests must pass before any changes are made. If tests are already failing before you touch anything, document this and do not treat subsequent failures as your regressions.

### Coverage Thresholds (branch coverage)

These are **targets**, not hard gates that block all work on a new or under-tested codebase. When starting below these thresholds, note the gap and treat all cleanup/refactor candidates as "needs care" until coverage reaches the minimum.

| Scope          | Minimum Target |
| -------------- | -------------- |
| Business logic | ≥ 95%          |
| APIs           | ≥ 90%          |
| Models         | ≥ 85%          |

### Every Task Requires

- [ ] Static checks pass (lint + types)
- [ ] Positive test case (expected behavior)
- [ ] Negative test case (bad/edge input)
- [ ] Regression tests still pass
- [ ] Rollback procedure validated

### Test Authoring Rules

- Tests are fully **independent** — no shared state between tests.
- Follow **AAA pattern**: Arrange → Act → Assert.
- No test chaining; no flaky tests; minimize mocking.
- **Never delete, weaken, or skip a test to make a diff pass.** Surface the failure instead.

---

## Test Organization

- Place tests in `tests/` directory.
- Mirror source structure: `src/module.py` → `tests/test_module.py`.
- Use descriptive test names: `test_calculate_total_with_discount()`.
- Group related tests in classes: `class TestCalculator:`.

---

## Test Patterns

### Basic Unit Test

```python
def test_addition():
    """Test basic addition."""
    assert Calculator.add(2, 3) == 5
```

### Parametrized Test

```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_addition_parametrized(a, b, expected):
    """Test addition with multiple inputs."""
    assert Calculator.add(a, b) == expected
```

### Property-Based Test

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Test that addition is commutative."""
    assert Calculator.add(a, b) == Calculator.add(b, a)
```

### Test with Fixture

```python
@pytest.fixture
def calculator():
    """Provide a calculator instance."""
    return Calculator()

def test_calculator_initial_state(calculator):
    """Test calculator starts with zero."""
    assert calculator.memory == 0
```

### Mock Test

```python
# Assumes mock_db_connection fixture defined in conftest.py

def test_save_to_database(mock_db_connection):
    """Test saving data to database."""
    service = DataService(db_conn=mock_db_connection)
    result = service.save_data({"id": 1, "name": "Test"})

    mock_db_connection.insert.assert_called_once()
    assert result is True
```

### Class-Based Tests

```python
class TestCalculator:
    def setup_method(self):
        """Setup for each test."""
        self.calc = Calculator()

    def test_add(self):
        """Test addition."""
        result = self.calc.add(2, 3)
        assert result == 5

    def test_multiply(self):
        """Test multiplication."""
        result = self.calc.multiply(3, 4)
        assert result == 12
```

### Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_async_api_call():
    """Test async API call."""
    api_client = ApiClient()
    result = await api_client.fetch_data("endpoint")

    assert isinstance(result, dict)
    assert "data" in result
```

### Error Condition Testing

```python
def test_division_by_zero():
    """Test division by zero raises error."""
    calc = Calculator()

    with pytest.raises(ZeroDivisionError):
        calc.divide(5, 0)
```

---

## Integration Testing

### Database Integration

```python
@pytest.fixture(scope="session")
def db_connection():
    """Create database connection for tests."""
    conn = create_test_database()
    yield conn
    destroy_test_database(conn)

def test_create_user(db_connection):
    """Test creating a user in database."""
    user_service = UserService(db_connection)
    user = user_service.create_user("john@example.com", "John Doe")

    assert user.id is not None
    assert user.email == "john@example.com"
```

### API Integration

```python
@pytest.fixture
def api_client():
    """Create test API client."""
    app = create_app()
    with TestClient(app) as client:
        yield client

def test_get_user_endpoint(api_client):
    """Test GET /users/{id} endpoint."""
    response = api_client.get("/users/1")

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] == 1
```

---

## Security Testing

### Input Validation

```python
def test_sql_injection_prevention():
    """Test that SQL injection attempts are prevented."""
    db_service = DatabaseService()
    malicious_input = "'; DROP TABLE users; --"
    result = db_service.get_user_by_name(malicious_input)

    assert result is None or isinstance(result, list) and len(result) == 0
```

### Authentication

```python
def test_unauthorized_access():
    """Test that unauthorized access is prevented."""
    client = TestClient(create_app())
    response = client.get("/admin/dashboard")

    assert response.status_code == 401
```

---

## Commands

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-branch --cov-fail-under=85

# Run specific test file
uv run pytest tests/test_module.py

# Run specific test function
uv run pytest tests/test_module.py::test_function_name

# Show missing coverage lines
uv run pytest --cov=src --cov-report=term-missing

# Run with verbose output
uv run pytest -v

# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
```

---

## Best Practices

- **Naming**: `test_` prefix, descriptive names, include expected outcome.
- **Structure**: AAA pattern — Arrange, Act, Assert.
- **Isolation**: Each test independent, use fixtures for setup/teardown, no shared mutable state.
- **Documentation**: Docstrings for complex test cases, explain edge case importance.
