# ✅ Décisions Prises et Historique du Projet

> **Dernière mise à jour** : 30 juin 2026  
> **Statut** : Phase d'élaboration (Brainstorming multi-IA en cours)  
> **Repository** : [Sunnynio/Automatisation-Ultime](https://github.com/Sunnynio/Automatisation-Ultime)
> **Objectif** : **Centraliser toutes les décisions validées** pour éviter les redondances et clarifier l’avancement du projet.

---

## 📌 **Comment Utiliser ce Fichier**

1. **Pour les IA (Gemini, Mistral, etc.)** :
   - Consulter ce fichier **avant de proposer une nouvelle idée** pour vérifier si elle a déjà été validée ou rejetée.
   - **Ne pas modifier** ce fichier sans validation de Franck (sauf pour ajouter des décisions prises lors d’une session).

2. **Pour Franck** :
   - **Valider les décisions** en ajoutant un ✅ ou en modifiant le statut.
   - **Archiver les décisions obsolètes** (ex: si une idée est abandonnée).
   - **Mettre à jour** les décisions en fonction des tests et retours.

3. **Format** :
   - **✅ Décision validée** : Décision finale, à implémenter.
   - **❌ Décision rejetée** : Idée abandonnée avec justification.
   - **🔄 En discussion** : Décision non encore validée.
   - **📅 À revalider** : Décision à revoir (ex: après un test).

---

## 🏗️ **Décisions sur l’Architecture Globale**

### **1. Structure du Système**
| Décision | Statut | Date | Responsable | Justification | Lien |
|---------|--------|------|-------------|---------------|------|
| Le système repose sur **3 piliers** : Notion (base de données), Google Calendar (temps), et les IA (Gemini pour l’interface, Mistral pour l’automatisation). | ✅ | 30/06/2026 | Franck + IA | Simplicité et flexibilité. Notion comme cœur central permet une intégration facile avec les IA. | [README](../README.md#-architecture-technique) |
| **Notion** est la **source de vérité** pour les tâches. Google Calendar est utilisé pour le *Time Blocking* et la synchronisation. | ✅ | 30/06/2026 | Franck + IA | Éviter les doublons et centraliser la gestion des tâches. |
| Les **workflows principaux** sont : Filtre contextuel, Routines, Gamification, Automatisation IA. | ✅ | 30/06/2026 | Franck + IA | Couvre tous les cas d’usage identifiés. | [README](../README.md#-workflows-principaux) |

---

### **2. Rôle des IA**
| Décision | Statut | Date | Responsable | Justification | Lien |
|---------|--------|------|-------------|---------------|------|
| **Gemini** est l’**interface principale** pour l’utilisateur (requêtes vocales/écrites, filtrage GPS). | ✅ | 30/06/2026 | Franck + IA | Intégration native avec Google (Calendar, Gmail, Drive). |
| **Mistral** est responsable de **l’automatisation et de l’exécution des tâches** (manipulation Notion, analyse de données, préparation de livrables). | ✅ | 30/06/2026 | Franck + IA | Mistral est plus flexible pour les scripts Python et l’intégration avec Notion. |
| Les IA **ne modifient pas directement** Google Calendar (sauf validation explicite de Franck). | ✅ | 30/06/2026 | Franck | Sécurité : éviter les modifications accidentelles. |

---

## 📊 **Décisions sur la Structure Notion**

### **1. Master Board (Base Principale)**

#### **Propriétés Validées**
| Propriété | Type | Valeurs Possibles | Statut | Date | Justification |
|-----------|------|------------------|--------|------|---------------|
| **Nom** | Titre | Libre | ✅ | 30/06/2026 | Obligatoire pour identifier les tâches. |
| **⏱️ Durée** | Sélection | 10 min, 30 min, 1h, 1h30, 2h, Demi-journée, 1 jour + | ✅ | 30/06/2026 | Permet un filtrage par temps disponible. |
| **💻 Support** | Sélection Multiple | PC Portable, PC Fixe, Téléphone, Tablette, Global | ✅ | 30/06/2026 | Permet de filtrer par appareil disponible. |
| **🌍 Pays/Lieu** | Sélection | Global, Thaïlande, France, Saudi Arabia, Avion, Hôtel, Bureau | ✅ | 30/06/2026 | Permet un filtrage par localisation. |
| **⚙️ Statut** | Statut (Kanban) | Pas commencé, En cours, En pause, À déléguer à l’IA, En attente de validation, Terminé | ✅ | 30/06/2026 | Suivi de l’avancement des tâches. |
| **🎯 Priorité** | Sélection | Urgent, Important, Secondaire, Optionnel, Sans priorité | ✅ | 30/06/2026 | Permet de prioriser les suggestions. |
| **🔄 Récurrence** | Sélection | Unique, Quotidienne, Hebdomadaire, Mensuelle, Trimestrielle, Voyage, Pré-départ, Post-arrivée | ✅ | 30/06/2026 | Gestion des tâches récurrentes. |
| **📌 Contexte** | Texte | Mots-clés (ex: "Admin", "Client X", "Apprentissage Thai") | ✅ | 30/06/2026 | Filtrage contextuel avancé. |
| **🕒 Heure de la journée** | Sélection | Matin, Après-midi, Soir, Nuit, Indifférent | ✅ | 30/06/2026 | Permet de filtrer par moment idéal. |
| **🔗 Dépendances** | Relation | Lien vers d’autres tâches Notion | ✅ | 30/06/2026 | Gestion des tâches bloquantes. |
| **📅 Date Limite** | Date | JJ/MM/AAAA | ✅ | 30/06/2026 | Suivi des échéances. |
| **📅 Date de Début** | Date | JJ/MM/AAAA | ✅ | 30/06/2026 | Planification des tâches. |
| **📝 Notes** | Texte | Libre | ✅ | 30/06/2026 | Détails supplémentaires. |

#### **Propriétés pour l’Automatisation (Mistral)**
| Propriété | Type | Valeurs Possibles | Statut | Date | Justification |
|-----------|------|------------------|--------|------|---------------|
| **🤖 Délégable à l’IA** | Case à cocher | Oui/Non | ✅ | 30/06/2026 | Identifier les tâches que Mistral peut exécuter. |
| **📄 Livrable** | URL | Lien vers le livrable (Google Doc, email, etc.) | ✅ | 30/06/2026 | Stocker le résultat de l’exécution par l’IA. |
| **🔄 Statut IA** | Sélection | Non délégée, En attente, En cours, Terminée, Échec | ✅ | 30/06/2026 | Suivi de l’exécution par l’IA. |
| **📅 Date de Délégation** | Date | JJ/MM/AAAA | ✅ | 30/06/2026 | Historique des délégations. |

#### **Propriétés pour la Gamification**
| Propriété | Type | Valeurs Possibles | Statut | Date | Justification |
|-----------|------|------------------|--------|------|---------------|
| **✅ Date de Complétion** | Date | JJ/MM/AAAA | ✅ | 30/06/2026 | Historique des tâches terminées. |
| **⏱️ Temps Réel** | Nombre | Minutes | ✅ | 30/06/2026 | Temps réel passé sur la tâche (pour stats). |
| **🌟 Points** | Nombre | Entier | ✅ | 30/06/2026 | Système de points pour la gamification. |

---

#### **Propriétés en Discussion**
| Propriété | Type | Valeurs Possibles | Statut | Date | Questions Ouvertes |
|-----------|------|------------------|--------|------|-------------------|
| **🔋 Énergie Requise** | Sélection | Faible, Moyenne, Élevée, Très élevée | 🔄 | 30/06/2026 | Faut-il l’ajouter ? Comment l’utiliser dans le filtrage ? |
| **🎨 Type de Tâche** | Sélection | Administrative, Créative, Technique, Apprentissage, etc. | 🔄 | 30/06/2026 | Utile pour un filtrage par type d’activité ? |
| **🧠 Niveau de Concentration** | Sélection | Profonde, Superficielle | 🔄 | 30/06/2026 | Permet-il d’améliorer les suggestions ? |
| **📊 Complexité** | Nombre | 1-5 | 🔄 | 30/06/2026 | Comment l’utiliser pour prioriser ? |
| **🔄 Tâche Récurrente Automatique** | Case à cocher | Oui/Non | 🔄 | 30/06/2026 | Comment implémenter la recréation automatique ? |
| **🔗 Lien vers Ressources** | URL | Lien vers un document, site web, etc. | 🔄 | 30/06/2026 | Utile pour associer des ressources aux tâches ? |
| **👨‍👩‍👧‍👦 Tâche Parent** | Relation | Lien vers une tâche parent | 🔄 | 30/06/2026 | Permet-il une hiérarchie utile ? |

---

### **2. Base "Routines"**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| Créer une **base dédiée** pour les routines (Matin, Soir, Voyage, etc.). | ✅ | 30/06/2026 | Franck + IA | Permet de réutiliser des checklists et de les afficher via des widgets. |
| Chaque routine contient une **liste de tâches** (relation vers le Master Board). | ✅ | 30/06/2026 | Franck + IA | Évite de dupliquer les tâches. |
| Ajouter une propriété **Complétion** (case à cocher) pour suivre l’avancement. | ✅ | 30/06/2026 | Franck + IA | Permet de générer des stats de complétion. |

---

### **3. Base "Journal de Bord"**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| Créer une **base dédiée** pour archiver les résumés quotidiens. | ✅ | 30/06/2026 | Franck + IA | Centraliser les stats de productivité. |
| Chaque entrée contient : **Date**, **Résumé**, **Tâches Terminées**, **Temps Total**, **Priorités**. | ✅ | 30/06/2026 | Franck + IA | Données nécessaires pour la gamification. |
| Le résumé quotidien est **généré par Mistral** et **stocké dans Notion**. | ✅ | 30/06/2026 | Franck + IA | Automatisation complète. |

---

## 🔄 **Décisions sur la Synchronisation**

### **1. Calendar ↔ Notion**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| Utiliser **Make.com** pour prototyper la synchronisation. | ✅ | 30/06/2026 | Franck | No-code, facile à configurer. |
| **Sens de la synchronisation** : **Calendar → Notion** (pour commencer). | ✅ | 30/06/2026 | Franck + IA | Éviter de surcharger Calendar. |
| Utiliser un **ID unique** (ex: `GCAL_{ID_EVENEMENT}`) dans Notion pour lier les entrées. | ✅ | 30/06/2026 | Franck + IA | Éviter les doublons. |
| **Ne pas synchroniser** les tâches "Terminées" vers Calendar (optionnel). | ✅ | 30/06/2026 | Franck | Éviter de surcharger Calendar. |

---

### **2. Notion ↔ Mistral**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| Mistral **scanne régulièrement** le Master Board pour les tâches avec `Statut = À déléguer à l’IA`. | ✅ | 30/06/2026 | Franck + IA | Automatisation de l’exécution. |
| Après exécution, Mistral **met à jour Notion** : `Statut IA = Terminée` + ajoute un `Livrable` (lien). | ✅ | 30/06/2026 | Franck + IA | Suivi clair de l’exécution. |
| Mistral **notifie l’utilisateur** (email/Slack) quand une tâche est prête pour validation. | ✅ | 30/06/2026 | Franck + IA | Transparence et collaboration. |

---

## 🎯 **Décisions sur les Workflows**

### **1. Filtre Contextuel**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| L’algorithme de priorisation est : **Priorité > Durée > Date Limite**. | ✅ | 30/06/2026 | Franck + IA | Simple et efficace pour commencer. |
| Le filtre retourne **les 3 meilleures tâches** par défaut. | ✅ | 30/06/2026 | Franck + IA | Éviter la surcharge cognitive. |
| Le format de sortie est un **tableau Markdown** (pour les widgets) ou une **liste vocalisée** (via Google TTS). | ✅ | 30/06/2026 | Franck + IA | Adapté à tous les supports. |
| Le filtre **croisera avec Google Calendar** pour éviter les chevauchements. | ✅ | 30/06/2026 | Franck + IA | Optimisation du temps. |

---

### **2. Routines**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| Les routines sont **affichées via des widgets Notion** sur mobile/PC. | ✅ | 30/06/2026 | Franck + IA | Accès rapide et visuel. |
| À la fin de la journée, Mistral **génère un résumé** des routines complétées. | ✅ | 30/06/2026 | Franck + IA | Gamification et motivation. |

---

### **3. Gamification**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| **Système de points** : 10 points par 30 min de tâche terminée (base). | ✅ | 30/06/2026 | Franck + IA | Simple et motivant. |
| **Bonus** : +50% de points pour les tâches **Urgent** ou **Important**. | ✅ | 30/06/2026 | Franck + IA | Encourager la priorisation. |
| Le **résumé quotidien** est envoyé par **email** (via Gmail API). | ✅ | 30/06/2026 | Franck + IA | Notification passive. |
| Le **Journal de Bord** est une **base Notion** avec des stats quotidiennes/mensuelles. | ✅ | 30/06/2026 | Franck + IA | Historique et analyse. |

---

### **4. Automatisation IA**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| Les tâches **"À déléguer à l’IA"** sont exécutées par **Mistral**. | ✅ | 30/06/2026 | Franck + IA | Centralisation de l’automatisation. |
| Mistral **ne modifie pas Google Calendar** (sauf validation explicite). | ✅ | 30/06/2026 | Franck | Sécurité. |
| Les **livrables** (emails, documents) sont stockés dans **Google Drive** ou **Gmail**. | ✅ | 30/06/2026 | Franck + IA | Intégration avec l’écosystème Google. |

---

## 🛠️ **Décisions Techniques**

### **1. Langages et Outils**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| **Python** est le langage principal pour les scripts d’automatisation. | ✅ | 30/06/2026 | Franck + IA | Flexibilité et bibliothèques disponibles (Notion API, Google API). |
| **Bibliothèques Python** : `notion-client`, `google-api-python-client`, `requests`. | ✅ | 30/06/2026 | Franck + IA | Standard pour les API utilisées. |
| **Make.com** est utilisé pour les workflows **no-code** (synchronisation Calendar ↔ Notion). | ✅ | 30/06/2026 | Franck | Rapidité de prototypage. |
| **Google Cloud Functions** est utilisé pour héberger les scripts Python en production. | ✅ | 30/06/2026 | Franck | Scalabilité et coût raisonnable. |

---

### **2. Sécurité**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| Les **tokens API** sont stockés dans `.env` et **jamais commités**. | ✅ | 30/06/2026 | Franck | Sécurité de base. |
| Les **permissions API** sont **minimales** (ex: Notion en lecture/écriture sur une base spécifique). | ✅ | 30/06/2026 | Franck | Principe du moindre privilège. |
| Les **tokens sont rotés** tous les **3-6 mois**. | ✅ | 30/06/2026 | Franck | Bonne pratique de sécurité. |

---

### **3. Hébergement**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| Les scripts sont **testés en local** avant d’être déployés. | ✅ | 30/06/2026 | Franck | Éviter les erreurs en production. |
| En production, les scripts sont **hébergés sur Google Cloud Functions**. | ✅ | 30/06/2026 | Franck | Intégration avec Google, coût raisonnable. |
| **Make.com** est utilisé pour les workflows **no-code** (pas d’hébergement nécessaire). | ✅ | 30/06/2026 | Franck | Simplicité. |

---

## 📅 **Décisions sur le Planning**

### **1. Priorisation des Tâches**
| Décision | Statut | Date | Responsable | Justification |
|---------|--------|------|-------------|---------------|
| **Priorité 1** : Finaliser la structure du Master Board Notion. | ✅ | 30/06/2026 | Franck + IA | Base du système. |
| **Priorité 2** : Prototyper le filtre contextuel (script Python). | ✅ | 30/06/2026 | Franck + IA | Fonctionnalité clé. |
| **Priorité 3** : Configurer Make.com pour Calendar ↔ Notion. | ✅ | 30/06/2026 | Franck | Synchronisation essentielle. |
| **Priorité 4** : Créer un script pour générer le résumé quotidien. | ✅ | 30/06/2026 | Franck + IA | Gamification. |
| **Priorité 5** : Ajouter la propriété "Énergie Requise" et tester le filtrage. | ✅ | 30/06/2026 | Franck + IA | Amélioration du filtrage. |

---

### **2. Échéances**
| Tâche | Échéance | Statut |
|-------|----------|--------|
| Finaliser la structure du Master Board | 02/07/2026 | 📅 À faire |
| Prototyper le filtre contextuel | 03/07/2026 | 📅 À faire |
| Configurer Make.com | 04/07/2026 | 📅 À faire |
| Script de résumé quotidien | 05/07/2026 | 📅 À faire |
| Ajouter "Énergie Requise" | 06/07/2026 | 📅 À faire |

---

## 🔄 **Décisions en Attente de Validation**

### **1. Structure Notion**
| Décision | Statut | Date | Questions Ouvertes |
|---------|--------|------|-------------------|
| Ajouter la propriété **"Énergie Requise"**. | 🔄 | 30/06/2026 | Faut-il l’ajouter ? Comment l’utiliser dans le filtrage ? |
| Ajouter la propriété **"Type de Tâche"**. | 🔄 | 30/06/2026 | Utile pour un filtrage par type d’activité ? |
| Ajouter la propriété **"Niveau de Concentration"**. | 🔄 | 30/06/2026 | Permet-il d’améliorer les suggestions ? |

---

### **2. Synchronisation**
| Décision | Statut | Date | Questions Ouvertes |
|---------|--------|------|-------------------|
| Synchroniser **Notion → Calendar** (en plus de Calendar → Notion). | 🔄 | 30/06/2026 | Utile ou trop complexe ? |
| Utiliser **Zapier** en plus de Make.com. | 🔄 | 30/06/2026 | Nécessaire ou redondant ? |

---

### **3. Automatisation**
| Décision | Statut | Date | Questions Ouvertes |
|---------|--------|------|-------------------|
| Permettre à Mistral de **modifier Google Calendar**. | 🔄 | 30/06/2026 | Risque de sécurité vs gain de fonctionnalité. |
| Ajouter un **système de validation automatique** pour certaines tâches. | 🔄 | 30/06/2026 | Quels critères pour valider automatiquement ? |

---

## 🗑️ **Décisions Rejetées ou Archivées**

### **1. Structure Notion**
| Décision | Statut | Date | Justification |
|---------|--------|------|---------------|
| Utiliser **plusieurs bases Notion** dès le début. | ❌ | 30/06/2026 | Trop complexe pour commencer. On séparera si nécessaire (ex: > 1000 tâches). |
| Ajouter une propriété **"Couleur"** pour les tâches. | ❌ | 30/06/2026 | Redondant avec `Priorité` (qui utilise déjà des couleurs). |

---

### **2. Synchronisation**
| Décision | Statut | Date | Justification |
|---------|--------|------|---------------|
| Synchroniser **toutes les tâches Notion** vers Calendar. | ❌ | 30/06/2026 | Risque de surcharger Calendar et de créer des doublons. |

---

### **3. Workflows**
| Décision | Statut | Date | Justification |
|---------|--------|------|---------------|
| Proposer **toutes les tâches possibles** dans le filtre contextuel. | ❌ | 30/06/2026 | Trop de choix = surcharge cognitive. On limite à 3 suggestions. |

---

## 📝 **Historique des Mises à Jour**

| Date | Auteur | Modifications |
|------|--------|---------------|
| 30/06/2026 | Franck + IA | Création du fichier. Ajout des décisions initiales sur l’architecture, Notion, synchronisation, workflows, et planning. |

---

## 🔗 **Liens Utiles**
- [README du Projet](../README.md) : Vision globale et workflows.
- [Structure Notion](../docs/notion_structure.md) : Détails des bases de données.
- [Guide des API](../docs/api_guide.md) : Comment utiliser les API.
- [Brainstorming en Cours](../brainstorming/idees.md) : Idées et questions ouvertes.

---

> **Comment Contribuer** :
> - **Pour les IA** : Proposer des décisions dans [brainstorming/idees.md](../brainstorming/idees.md) avant de les ajouter ici.
> - **Pour Franck** : Valider les décisions en les marquant ✅ ou en les modifiant.
> - **Pour tous** : Respecter les décisions validées pour éviter les incohérences.