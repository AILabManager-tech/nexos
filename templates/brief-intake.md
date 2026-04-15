# NEXOS v3.0 — Brief Client

> Ce formulaire recueille TOUTES les informations nécessaires pour générer un site web
> conforme à la Loi 25 du Québec sans recontacter le client.

---

## 1. Informations légales de l'entreprise

- **Dénomination sociale complète** : ___
- **Numéro d'entreprise du Québec (NEQ)** : ___
  (10 chiffres, ex: 1234567890)
- **Adresse du siège** : ___
- **Téléphone principal** : ___
- **Courriel principal** : ___

---

## 2. Projet web

- **Nom du client** : ___
- **Slug (URL-friendly)** : ___
  (ex: plomberie-quebec-plus — lettres minuscules, chiffres, tirets)
- **Secteur d'activité** : ___
- **URL existante** (si migration) : ___
- **Domaine cible** : ___
- **Type** : [ ] Vitrine [ ] E-commerce [ ] Portfolio [ ] Blog [ ] Application
- **Pages souhaitées** : ___
  (ex: accueil, services, à propos, contact, blogue)
- **Langues** : [ ] Français [ ] Anglais [ ] Autres : ___
- **Charte graphique / Logo** : [ ] Fourni [ ] À créer
- **Références visuelles** (URLs de sites que vous aimez) : ___
- **Hébergement** : [ ] Vercel (défaut) [ ] IONOS [ ] Autre : ___
- **Fonctionnalités** :
  [ ] Formulaire de contact
  [ ] Carte Google Maps
  [ ] Chatbot IA
  [ ] Infolettre
  [ ] Portfolio / Galerie
  [ ] Calendrier de réservation
  [ ] E-commerce / Boutique
  [ ] Autre : ___
- **Concurrents à analyser** (3-5 URLs) : ___
- **Mots-clés SEO prioritaires** : ___
- **Contexte libre** : ___

---

## 3. Conformité légale — Loi 25 du Québec

> La Loi 25 (Loi modernisant des dispositions législatives en matière de protection
> des renseignements personnels) est pleinement en vigueur depuis septembre 2024.
> Chaque site web doit s'y conformer.

### 3.1 Responsable de la protection des renseignements personnels (RPP)

- **Nom du RPP désigné** : ___
  (Loi 25, art. 3.1 : Obligation de désigner un RPP. Si non désigné, c'est le dirigeant le plus haut placé.)
- **Courriel du RPP** : ___
- **Titre / Fonction** : ___

### 3.2 Collecte de renseignements personnels

- **Le site collectera-t-il des renseignements personnels ?** [ ] Oui [ ] Non
  (Nom, courriel, téléphone, adresse = renseignements personnels au sens de la loi)
- **Types de données collectées** :
  [ ] Nom / Prénom
  [ ] Courriel
  [ ] Téléphone
  [ ] Adresse postale
  [ ] Données de navigation (cookies, analytics)
  [ ] Données de paiement
  [ ] Données sensibles (santé, opinions, biométrie)
  [ ] Autres : ___

### 3.3 Finalités de la collecte

- **Pourquoi collectez-vous ces données ?** :
  [ ] Formulaire de contact
  [ ] Infolettre / Marketing
  [ ] Traitement de commandes
  [ ] Prise de rendez-vous
  [ ] Analyse de trafic (Google Analytics, etc.)
  [ ] Autre : ___
  (Loi 25, art. 4 : La collecte doit être nécessaire et limitée aux finalités déclarées)

### 3.4 Conservation et transfert

- **Durée de conservation prévue** : ___
  (Loi 25, art. 23 : obligation de détruire les RP lorsque la finalité est atteinte)
- **Les données seront-elles transférées hors Québec ?** [ ] Oui [ ] Non
  (Loi 25, art. 17 : Évaluation des facteurs relatifs à la vie privée obligatoire)
- **Si oui, vers quels pays/services ?** : ___
  (Ex: Vercel = serveurs US, Google Analytics = transfert US, Resend = serveurs US)

### 3.5 Services tiers

- **Quels services tiers le site utilisera-t-il ?**
  [ ] Google Analytics (ou alternative)
  [ ] Google Maps
  [ ] Formulaire Resend / Mailchimp
  [ ] Chat en direct
  [ ] Réseaux sociaux (pixels, embeds)
  [ ] Hébergement Vercel (US)
  [ ] Autre : ___
  (Chaque service tiers qui traite des RP doit être déclaré dans la politique de confidentialité)

### 3.6 Consentement

- **Quel mécanisme de consentement souhaitez-vous ?**
  [ ] Bandeau cookies avec opt-in (Recommandé — conforme Loi 25)
  [ ] Bandeau cookies avec opt-out
  [ ] Page de gestion du consentement complète
  (Loi 25, art. 8.1 : Consentement manifeste, libre et éclairé. Par défaut = le plus haut niveau de confidentialité)

### 3.7 Incident de confidentialité

- **Avez-vous un processus de gestion des incidents ?** [ ] Oui [ ] Non
  (Loi 25, art. 3.5 : Obligation de signaler à la CAI tout incident présentant un risque de préjudice sérieux)
- **Courriel de notification d'incident** : ___

---

## 4. Design & Marque

- **Palette de couleurs** (si existante) : ___
- **Typographies préférées** : ___
- **Style visuel souhaité** : [ ] Minimaliste [ ] Coloré [ ] Corporatif [ ] Créatif [ ] Autre
- **Audience cible** : ___
- **Zone géographique** : [ ] Locale [ ] Québec [ ] Canada [ ] International

---

## 5. Monétisation & Analytics

> Ces informations permettent de configurer automatiquement AdSense, Google Analytics,
> et Google Search Console lors du post-déploiement.

### 5.1 Monétisation publicitaire

- **Souhaitez-vous monétiser le site avec des publicités ?** [ ] Oui [ ] Non
- **Si oui, avez-vous un compte Google AdSense ?** [ ] Oui [ ] Non [ ] À créer
- **Publisher ID AdSense** (si existant) : ___
  (Format: ca-pub-XXXXXXXXXXXXXXXX)
- **Emplacements publicitaires souhaités** :
  [ ] Après le hero (bannière horizontale)
  [ ] Entre les sections
  [ ] Sidebar (si applicable)
  [ ] Annonces automatiques (Google décide)
  [ ] Autre : ___
- **IMPORTANT** : AdSense requiert un domaine de premier niveau (pas de sous-domaine Vercel)

### 5.2 Analytics & Suivi

- **Souhaitez-vous Google Analytics ?** [ ] Oui [ ] Non
- **ID de mesure GA4** (si existant) : ___
  (Format: G-XXXXXXXXXX)
- **Autres outils de suivi** :
  [ ] Google Search Console
  [ ] Facebook Pixel
  [ ] LinkedIn Insight Tag
  [ ] Hotjar / Clarity
  [ ] Autre : ___
- **RAPPEL Loi 25** : Tous les trackers non-essentiels doivent être activés
  APRÈS le consentement explicite de l'utilisateur (via bandeau cookies)

### 5.3 Code de vérification

- **Code Google Search Console** : ___
  (Balise meta, format: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX)
  (Sera ajouté automatiquement dans le `<head>` du site)

---

## 6. Budget & Délai

- **Budget** : ___
- **Délai souhaité** : ___
- **Priorité** : [ ] Qualité [ ] Rapidité [ ] Budget

---

## Notes libres
