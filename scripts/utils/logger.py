# Module de Journalisation pour les Scripts Python

> **Fichier** : `scripts/utils/logger.py`  
> **Rôle** : Configurer un logger centralisé pour le projet, avec support pour la console et les fichiers.  
> **Dépendances** : `logging`, `os`

---

## 📌 **Fonctionnalités**
- Configuration d’un **logger centralisé** pour tous les scripts.
- **Niveaux de log** : DEBUG, INFO, WARNING, ERROR, CRITICAL.
- **Sorties** : Console + fichier (si le dossier `DATA_DIR` existe).
- **Format personnalisé** : Inclut le timestamp, le nom du logger, le niveau, et le message.
- **Gestion des erreurs** : Capture et journalise les exceptions.

---

## 🔧 **Code**

```python
import logging
import os
from typing import Optional
from datetime import datetime

# ======================
# Configuration par Défaut
# ======================
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FILE = "automatisation_ultime.log"
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ======================
# Fonction de Configuration du Logger
# ======================

def setup_logger(
    name: str = "automatisation_ultime",
    log_level: int = DEFAULT_LOG_LEVEL,
    log_file: Optional[str] = None,
    log_dir: Optional[str] = None
) -> logging.Logger:
    """
    Configure et retourne un logger pour le projet.
    
    Args:
        name: Nom du logger (par défaut : "automatisation_ultime").
        log_level: Niveau de log (ex: logging.INFO, logging.DEBUG).
        log_file: Nom du fichier de log (par défaut : DEFAULT_LOG_FILE).
        log_dir: Dossier pour le fichier de log (par défaut : DATA_DIR depuis .env).
    
    Returns:
        logging.Logger: Logger configuré.
    """
    # Créer le logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Éviter les doublons de handlers
    if logger.handlers:
        return logger
    
    # Formatter
    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
    
    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)
    
    # Handler pour le fichier (si log_dir est spécifié et existe)
    if log_dir and os.path.exists(log_dir):
        file_path = os.path.join(log_dir, log_file or DEFAULT_LOG_FILE)
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
        logger.info(f"Journalisation activée dans {file_path}")
    else:
        logger.warning(f"Dossier de log non trouvé: {log_dir}. Les logs ne seront pas enregistrés dans un fichier.")
    
    return logger


# ======================
# Logger Global
# ======================
# Initialiser le logger global avec les paramètres par défaut
logger = setup_logger(
    name="automatisation_ultime",
    log_dir=os.getenv("DATA_DIR", "./data")
)


# ======================
# Fonctions de Journalisation Spécifiques
# ======================

def log_info(message: str, logger_instance: Optional[logging.Logger] = None) -> None:
    """
    Journalise un message au niveau INFO.
    
    Args:
        message: Message à journaliser.
        logger_instance: Logger à utiliser (par défaut : logger global).
    """
    (logger_instance or logger).info(message)


def log_warning(message: str, logger_instance: Optional[logging.Logger] = None) -> None:
    """
    Journalise un message au niveau WARNING.
    
    Args:
        message: Message à journaliser.
        logger_instance: Logger à utiliser (par défaut : logger global).
    """
    (logger_instance or logger).warning(message)


def log_error(message: str, logger_instance: Optional[logging.Logger] = None) -> None:
    """
    Journalise un message au niveau ERROR.
    
    Args:
        message: Message à journaliser.
        logger_instance: Logger à utiliser (par défaut : logger global).
    """
    (logger_instance or logger).error(message)


def log_debug(message: str, logger_instance: Optional[logging.Logger] = None) -> None:
    """
    Journalise un message au niveau DEBUG.
    
    Args:
        message: Message à journaliser.
        logger_instance: Logger à utiliser (par défaut : logger global).
    """
    (logger_instance or logger).debug(message)


def log_exception(
    exception: Exception,
    message: str = "Une erreur est survenue",
    logger_instance: Optional[logging.Logger] = None
) -> None:
    """
    Journalise une exception avec son traceback.
    
    Args:
        exception: Exception à journaliser.
        message: Message supplémentaire (par défaut : "Une erreur est survenue").
        logger_instance: Logger à utiliser (par défaut : logger global).
    """
    (logger_instance or logger).exception(f"{message}: {exception}")


# ======================
# Décorateurs pour la Journalisation
# ======================

def log_function_call(func):
    """
    Décorateur pour journaliser les appels de fonction (niveau DEBUG).
    
    Args:
        func: Fonction à décorer.
    
    Returns:
        Fonction décorée.
    """
    def wrapper(*args, **kwargs):
        logger.debug(f"Appel de {func.__name__} avec args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} a retourné: {result}")
            return result
        except Exception as e:
            log_exception(e, f"Erreur dans {func.__name__}")
            raise
    return wrapper


def log_execution_time(func):
    """
    Décorateur pour journaliser le temps d'exécution d'une fonction.
    
    Args:
        func: Fonction à décorer.
    
    Returns:
        Fonction décorée.
    """
    import time
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"Début de {func.__name__}")
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.debug(f"{func.__name__} a pris {execution_time:.2f} secondes")
            return result
        except Exception as e:
            log_exception(e, f"Erreur dans {func.__name__}")
            raise
    return wrapper


# ======================
# Exemple d'Utilisation
# ======================

if __name__ == "__main__":
    # Exemple 1: Utilisation basique
    logger.info("Ceci est un message INFO")
    logger.warning("Ceci est un message WARNING")
    logger.error("Ceci est un message ERROR")
    
    # Exemple 2: Journalisation d'une exception
    try:
        1 / 0
    except ZeroDivisionError as e:
        log_exception(e, "Division par zéro")
    
    # Exemple 3: Utilisation des fonctions spécifiques
    log_info("Test de log_info")
    log_warning("Test de log_warning")
    log_error("Test de log_error")
    
    # Exemple 4: Décorateurs
    @log_function_call
    def exemple_function(a: int, b: int) -> int:
        return a + b
    
    exemple_function(2, 3)
    
    @log_execution_time
    def long_running_function():
        import time
        time.sleep(1)
        return "Terminé"
    
    long_running_function()
```

---

## 📝 **Explications**

### **1. Configuration du Logger**
- **`setup_logger()`** : Fonction principale pour configurer un logger.
  - **Paramètres** :
    - `name` : Nom du logger (ex: `__name__` pour utiliser le nom du module).
    - `log_level` : Niveau de log (ex: `logging.INFO`, `logging.DEBUG`).
    - `log_file` : Nom du fichier de log (par défaut : `automatisation_ultime.log`).
    - `log_dir` : Dossier pour le fichier de log (par défaut : `DATA_DIR` depuis `.env`).
  - **Retourne** : Un `logging.Logger` configuré.

---

### **2. Logger Global**
- Un logger global (`logger`) est initialisé automatiquement avec les paramètres par défaut.
- **Utilisation** : Importez simplement `logger` depuis ce module.

---

### **3. Fonctions de Journalisation Spécifiques**
- **`log_info()`**, **`log_warning()`**, **`log_error()`**, **`log_debug()`** : Fonctions pour journaliser à différents niveaux.
- **`log_exception()`** : Journalise une exception avec son traceback complet.

---

### **4. Décorateurs**
- **`@log_function_call`** : Journalise les appels de fonction et leurs arguments/retours (niveau DEBUG).
- **`@log_execution_time`** : Journalise le temps d’exécution d’une fonction (niveau DEBUG).

---

## 🚀 **Utilisation**

### **1. Dans un Script**
Importez le logger global ou configurez un logger personnalisé :

#### **Option 1 : Utiliser le Logger Global**
```python
from utils.logger import logger, log_info, log_error, log_exception

# Journaliser un message
logger.info("Début du script")
log_info("Tâche en cours...")

# Journaliser une erreur
try:
    1 / 0
except ZeroDivisionError as e:
    log_exception(e, "Erreur de division")
```

#### **Option 2 : Configurer un Logger Personnalisé**
```python
from utils.logger import setup_logger

# Créer un logger pour un module spécifique
module_logger = setup_logger(name=__name__, log_level=logging.DEBUG)
module_logger.info("Logger personnalisé pour ce module")
```

#### **Option 3 : Utiliser les Décorateurs**
```python
from utils.logger import log_function_call, log_execution_time

@log_function_call
def ma_fonction(a: int, b: int) -> int:
    return a * b

@log_execution_time
def long_process():
    # Code long...
    return "Résultat"
```

---

### **2. Niveaux de Log Recommandés**
| Niveau      | Utilisation                                                                 | Exemple                                  |
|------------|-----------------------------------------------------------------------------|------------------------------------------|
| **DEBUG**  | Détails pour le débogage (développement uniquement).                     | "Appel de fetch_tasks avec filtres: {...}" |
| **INFO**   | Informations sur le déroulement normal du script.                         | "5 tâches récupérées depuis Notion"      |
| **WARNING**| Avertissements pour des situations inattendues mais gérables.               | "Aucune tâche ne correspond au filtre"   |
| **ERROR**  | Erreurs qui empêchent une partie du script de fonctionner.                | "Échec de la connexion à Notion API"       |
| **CRITICAL**| Erreurs critiques qui empêchent le script de continuer.                   | "Token Notion manquant"                    |

---

### **3. Bonnes Pratiques**
1. **Utilisez des messages clairs et descriptifs** :
   - ❌ `logger.info("Erreur")`
   - ✅ `logger.error("Échec de la récupération des tâches Notion: timeout API")`

2. **Journalisez les exceptions avec leur contexte** :
   - ❌ `logger.error(e)`
   - ✅ `log_exception(e, "Erreur lors du filtrage des tâches")`

3. **Évitez de journaliser des données sensibles** :
   - ❌ `logger.info(f"Token: {NOTION_TOKEN}")`
   - ✅ `logger.info("Token Notion chargé depuis .env")`

4. **Utilisez les décorateurs pour les fonctions critiques** :
   - `@log_function_call` pour les fonctions complexes.
   - `@log_execution_time` pour les fonctions longues.

---

## 🔒 **Sécurité et Performance**
- **Ne jamais journaliser de tokens ou données sensibles** : Utilisez des placeholders (ex: `[REDACTED]`).
- **Limiter le niveau de log en production** : Utilisez `logging.INFO` ou `logging.WARNING` pour éviter de surcharger les logs.
- **Rotater les fichiers de log** : Pour les longs scripts, utilisez `RotatingFileHandler` pour éviter des fichiers trop gros.

---

## 📚 **Ressources**
- [Python `logging` Documentation](https://docs.python.org/3/library/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Best Practices for Logging](https://realpython.com/python-logging/)