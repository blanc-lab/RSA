import streamlit as st
import random

# Titre et introduction
st.title("Cryptographie : cours sur l'Algorithme RSA")
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
1. Choisir deux grands nombres premiers distincts p et q.
2. Calculer leur produit n = p × q.
3. Calculer la fonction d'Euler : φ(n) = (p - 1)(q - 1).
4. Choisir un exposant de chiffrement e, tel que :
   - 1 < e < φ(n) et pgcd(e, φ(n)) = 1.
   - Un choix fréquent est e = 65537, car il optimise les calculs tout en étant sécurisé.
5. Calculer l'exposant de déchiffrement d, tel que : e × d ≡ 1 mod φ(n).

Clés générées :
- **Clé publique** : (n, e) → utilisée pour chiffrer.
- **Clé privée** : (n, d) → utilisée pour déchiffrer.
""")

# Section 6: Algorithme d'Euclide Étendu et Inverse Modulaire
st.header("6. Algorithme d'Euclide Étendu et Inverse Modulaire")

st.write("""
L'algorithme d'Euclide étendu permet de calculer le **plus grand commun diviseur** (pgcd) de deux entiers, tout en trouvant des coefficients entiers \( x \) et \( y \) tels que :

$$
\text{pgcd}(a, b) = ax + by
$$

Cette relation est connue sous le nom **d'identité de Bézout**, et les entiers \( x \) et \( y \) sont appelés **coefficients de Bézout**.

---
### a) Théorème de Bézout :
Soient \( a \) et \( b \) deux entiers relatifs non nuls. Il existe toujours deux entiers \( x \) et \( y \) vérifiant l'équation :

$$
\text{pgcd}(a,b) = ax + by
$$

---
### b) Propriété clé de l'algorithme d'Euclide :
L'algorithme d'Euclide repose sur la propriété suivante :

$$
\text{pgcd}(a,b) = \text{pgcd}(b, a \mod b)
$$

Ce qui signifie que le pgcd de deux nombres ne change pas si l'on remplace \( a \) par son reste dans la division euclidienne de \( a \) par \( b \). Cette propriété permet une **réduction rapide** de la taille des nombres à chaque itération.

---
### c) Code de l'algorithme d'Euclide étendu :
Le code suivant implémente l'algorithme d'Euclide étendu en Python :
""")

st.code("""
def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = euclide_etendu(b, a % b)
        return g, y, x - (a // b) * y
""")

st.write("""
---
### d) Lien entre pgcd et inverse modulaire :
L'inverse modulaire de \( a \) modulo \( m \) est un entier \( x \) tel que :

$$
a 	imes x \equiv 1 \mod m
$$

L'algorithme d'Euclide étendu permet de trouver cet inverse si \( 	ext{pgcd}(a, m) = 1 \). En effet, d'après le théorème de Bézout, si \( 	ext{pgcd}(a, m) = 1 \), alors il existe \( x \) et \( y \) tels que :

$$
a 	imes x + m 	imes y = 1
$$

En prenant cette équation **modulo \( m \)**, le terme \( m 	imes y \) disparaît, ce qui donne :

$$
a 	imes x \equiv 1 \mod m
$$

Ainsi, \( x \) est l'inverse modulaire de \( a \) modulo \( m \).

---
### e) Exemple avec trace pour \( a = 13 \), \( b = 7 \) :

Voici la trace des appels récursifs de l'algorithme d'Euclide étendu :

| Étape | \( a \) | \( b \) | \( a \mod b \) | \( x \) | \( y \) |
|-------|----|----|---------|----|----|
| 1 | 13 | 7 | 6 | 1 | 0 |
| 2 | 7 | 6 | 1 | 0 | 1 |
| 3 | 6 | 1 | 0 | 1 | -1 |
| 4 | 1 | 0 | - | -1 | 2 |

Finalement, nous obtenons :

$$
\text{pgcd}(13,7) = 1, \quad x = -3, \quad y = 2
$$

Ce qui signifie que :

$$
13 \times (-3) + 7 \times 2 = 1
$$

Donc, l'inverse modulaire de 13 modulo 7 est **4** (car \( -3 \equiv 4 \mod 7 \)).

Cette méthode est essentielle en cryptographie, notamment pour RSA.
""")
