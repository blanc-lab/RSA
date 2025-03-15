import streamlit as st
import random

# Titre et introduction
st.title("Cryptographie ;Cours sur l'Algorithme RSA ")
st.write("""
L'algorithme RSA est l'un des systèmes de chiffrement asymétrique les plus utilisés en cryptographie. 
Il repose sur la difficulté de factoriser de grands nombres et assure la confidentialité et l'authentification des communications.
""")

# Section 1: Introduction à la cryptographie asymétrique
st.header("1. Introduction à la cryptographie asymétrique")
st.write("""
En cryptographie, il existe deux types de chiffrement :
- **Chiffrement symétrique** : Une seule clé est utilisée pour chiffrer et déchiffrer.
- **Chiffrement asymétrique** : Utilise une clé publique pour chiffrer et une clé privée pour déchiffrer.

L’algorithme RSA appartient à la cryptographie asymétrique, ce qui permet :
- La **confidentialité** : Seul le détenteur de la clé privée peut lire le message.
- L’**authentification** : RSA est utilisé dans les signatures numériques pour garantir l’identité du signataire.
""")

# Section 2: Principe de fonctionnement de RSA
st.header("2. Principe de fonctionnement de RSA")
st.write("""
L'algorithme RSA repose sur trois étapes :
- **Génération des clés** (publique et privée).
- **Chiffrement du message** avec la clé publique.
- **Déchiffrement du message** avec la clé privée.

Sa sécurité repose sur la difficulté de factoriser un grand nombre composé de deux nombres premiers.
""")

# Section 3: Génération des clés RSA
st.header("3. Génération des clés RSA")
st.write("""
Étapes :
1. Choisir deux grands nombres premiers distincts \( p \) et \( q \).
2. Calculer leur produit \( n = p \times q \) (modulus).
3. Calculer la fonction d'Euler : \( \phi(n) = (p-1)(q-1) \).
4. Choisir un exposant de chiffrement \( e \), tel que :
   - \( 1 < e < \phi(n) \) et \( \text{PGCD}(e, \phi(n)) = 1 \).
   - Un choix fréquent est \( e = 65537 \), car il optimise les calculs tout en étant sécurisé.
5. Calculer l'exposant de déchiffrement \( d \), tel que : \( e \times d \equiv 1 \mod \phi(n) \).
   
Clés générées :
- **Clé publique** : \( (n, e) \) → utilisée pour chiffrer.
- **Clé privée** : \( (n, d) \) → utilisée pour déchiffrer.
""")

# Section 4: Chiffrement et Déchiffrement RSA
st.header("4. Chiffrement et Déchiffrement RSA")
st.write("""
Chiffrement :
- Pour un message \( m \), l’expéditeur utilise la clé publique \( (n, e) \) :
  \[ c = m^e \mod n \]
  où \( c \) est le message chiffré.

Déchiffrement :
- Le destinataire utilise la clé privée \( (n, d) \) pour retrouver \( m \) :
  \[ m = c^d \mod n \]
  
D'après le **théorème d'Euler**, on a :
\[
m^{ed} \equiv m \mod n
\]
Ce qui garantit la récupération correcte du message initial.
""")

# Section 5: Sécurité et résistance aux attaques
st.header("5. Sécurité et résistance aux attaques")
st.write("""
Pourquoi RSA est sécurisé ?
- **Difficulté de la factorisation** : Retrouver \( p \) et \( q \) à partir de \( n \) est très difficile.
- **Temps de calcul** : Aucune méthode efficace connue ne permet de factoriser \( n \) en un temps raisonnable pour des clés de 2048 bits ou plus.

Risques et vulnérabilités :
- **Mauvais choix de nombres premiers** : Si \( p \) ou \( q \) est composé, la clé est faible.
- **Attaques possibles** :
  - **Attaque par factorisation** : Si \( n \) est trop petit, il peut être factorisé avec des algorithmes modernes.
  - **Attaque quantique** : L’algorithme de Shor pourrait casser RSA avec un ordinateur quantique suffisamment puissant.
""")

# Section 6: Algorithme d'Euclide Étendu
st.header("6. Algorithme d'Euclide Étendu")
st.write("""
L'algorithme d’Euclide étendu est utilisé pour trouver l'inverse modulaire \( d \).

Il permet de résoudre \( ax + by = \text{PGCD}(a, b) \).

Si \( a \) et \( b \) sont premiers entre eux, alors \( x \) est l'inverse modulaire de \( a \) modulo \( b \).
""")

st.subheader("Implémentation de l'algorithme d'Euclide Étendu en Python")
st.code("""
def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = euclide_etendu(b, a % b)
        return g, y, x - (a // b) * y
""")

# Section 7: Test de primalité de Miller-Rabin
st.header("7. Test de primalité de Miller-Rabin")
st.write("""
Le test de Miller-Rabin est un algorithme probabiliste utilisé pour tester si un nombre est premier.

Principe :
1. Écrire \( n - 1 = 2^s \times d \).
2. Tester des bases aléatoires \( a \) :
   - \( x = a^d \mod n \).
3. Si aucun des tests ne réussit, alors \( n \) est composé.
""")

st.subheader("Implémentation du test de Miller-Rabin en Python")
st.code("""
import random

def est_probablement_premier(n, k=10):
    if n < 2 or n % 2 == 0:
        return False
    s, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
""")

# Section 8: Exponentiation Modulaire Rapide
st.header("8. Exponentiation Modulaire Rapide")
st.write("""
RSA implique des puissances très grandes, nécessitant une méthode efficace pour \( m^e \mod n \).

L'algorithme de **Square and Multiply** optimise l'exponentiation modulaire.
""")

st.subheader("Implémentation de l'exponentiation modulaire rapide en Python")
st.code("""
def exp_mod(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result
""")

# Section 9: Conclusion
st.header("9. Conclusion")
st.write("""
- **RSA** repose sur la difficulté de factoriser de grands nombres.
- La **génération de clés** nécessite des tests de primalité robustes.
- L’**exponentiation modulaire rapide** optimise les calculs.
- **RSA est sécurisé** contre les attaques classiques, mais vulnérable aux attaques quantiques.

### Perspectives :
Des alternatives comme les **courbes elliptiques** et la **cryptographie post-quantique** sont en développement.
""")
