# Тестирование с использованием mock и patch

В этом проекте демонстрируются различные способы использования `unittest.mock` для тестирования.

## Основные концепции:

### 1. `Mock` - создание мок-объектов
```python
from unittest.mock import Mock

# Создание мок-объекта
mock_obj = Mock()

# Настройка возвращаемых значений
mock_obj.method.return_value = "result"

# Настройка атрибутов
mock_obj.attribute = "value"