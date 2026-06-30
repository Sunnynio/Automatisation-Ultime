# Package Utils pour les Scripts Python

> **Fichier** : `scripts/utils/__init__.py`  
> **Rôle** : Rendre le dossier `utils` importable comme un package Python.  
> **Contenu** : Importation des modules utilitaires pour une utilisation simplifiée.

---

## 📌 **Contenu**

Ce fichier permet d'importer directement les modules du dossier `utils` :

```python
from utils import config, helpers, logger
```

---

## 🔧 **Code**

```python
# Importer les modules utilitaires pour les rendre accessibles via `from utils import ...`
from .config import (
    get_notion_client,
    get_google_calendar_service,
    get_gmail_service,
    get_mistral_headers,
    check_config,
    NOTION_TOKEN,
    NOTION_DATABASE_ID,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REFRESH_TOKEN,
    GMAIL_SENDER_EMAIL,
    MISTRAL_API_KEY,
    DATA_DIR,
    TIMEZONE
)

from .helpers import (
    get_current_time,
    get_today_date_str,
    get_time_in_timezone,
    duration_to_minutes,
    minutes_to_duration,
    filter_tasks_by_context,
    sort_tasks_by_priority_and_duration,
    sort_tasks_by_deadline,
    calculate_points_for_task,
    calculate_daily_stats,
    format_task_for_display,
    format_tasks_as_markdown_table,
    format_daily_summary,
    get_time_until_deadline,
    is_task_overdue
)

from .logger import (
    setup_logger,
    logger,
    log_info,
    log_warning,
    log_error,
    log_debug,
    log_exception,
    log_function_call,
    log_execution_time
)

# Définir ce qui est exporté par défaut avec `from utils import *`
__all__ = [
    # Config
    "get_notion_client",
    "get_google_calendar_service",
    "get_gmail_service",
    "get_mistral_headers",
    "check_config",
    "NOTION_TOKEN",
    "NOTION_DATABASE_ID",
    "GOOGLE_CLIENT_ID",
    "GOOGLE_CLIENT_SECRET",
    "GOOGLE_REFRESH_TOKEN",
    "GMAIL_SENDER_EMAIL",
    "MISTRAL_API_KEY",
    "DATA_DIR",
    "TIMEZONE",
    # Helpers
    "get_current_time",
    "get_today_date_str",
    "get_time_in_timezone",
    "duration_to_minutes",
    "minutes_to_duration",
    "filter_tasks_by_context",
    "sort_tasks_by_priority_and_duration",
    "sort_tasks_by_deadline",
    "calculate_points_for_task",
    "calculate_daily_stats",
    "format_task_for_display",
    "format_tasks_as_markdown_table",
    "format_daily_summary",
    "get_time_until_deadline",
    "is_task_overdue",
    # Logger
    "setup_logger",
    "logger",
    "log_info",
    "log_warning",
    "log_error",
    "log_debug",
    "log_exception",
    "log_function_call",
    "log_execution_time"
]
```

---

## 📝 **Explications**

### **1. Importation Simplifiée**
- Ce fichier permet d'importer **tous les modules utilitaires** en une seule ligne :
  ```python
  from utils import config, helpers, logger
  ```
  ou
  ```python
  from utils import *  # Importe tout ce qui est dans __all__
  ```

---

### **2. `__all__`**
- La liste `__all__` définit quels **noms sont exportés** lorsque `from utils import *` est utilisé.
- Cela évite de polluer l'espace de noms avec des variables internes.

---

## 🚀 **Utilisation**

### **1. Importer un Module Spécifique**
```python
from utils import config

notion = config.get_notion_client()
```

### **2. Importer Plusieurs Fonctions**
```python
from utils import get_notion_client, get_current_time, logger

notion = get_notion_client()
now = get_current_time()
logger.info(f"Client Notion initialisé à {now}")
```

### **3. Importer Tout**
```python
from utils import *

# Toutes les fonctions et variables de __all__ sont disponibles
notion = get_notion_client()
tasks = fetch_tasks_by_context({"pays": "Thaïlande"})
```

---

## ✅ **Bonnes Pratiques**
- **Évitez `from utils import *`** dans les grands projets pour éviter les conflits de noms.
- **Préférez les imports explicites** : `from utils import get_notion_client, logger`.
- **Utilisez des alias si nécessaire** : `from utils import logger as log`.