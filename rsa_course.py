import streamlit as st

def main():
    st.title("Algorithme de chiffrement RSA")
    
    st.header("1) Chiffrement symétrique et asymétrique")
    st.subheader("a) Chiffrement symétrique")
    st.write("Une seule clé est utilisée à la fois pour chiffrer et déchiffrer les messages.")
    
    st.subheader("b) Chiffrement asymétrique")
    st.write("Deux clés distinctes sont utilisées :")
    st.write("- Une **clé publique** permettant de **chiffrer** un message.")
    st.write("- Une **clé privée** permettant de **déchiffrer** ce message.")
    st.write("RSA est un algorithme de chiffrement asymétrique.")
    
    st.header("2) Principe du RSA")
    st.write("L'algorithme RSA s'appuie sur des propriétés mathématiques d'arithmétique modulaire pour assurer le chiffrement et le déchiffrement des messages.")
    st.write("Sa sécurité repose sur la difficulté de factoriser un grand nombre entier qui est le produit de deux nombres premiers distincts.")
    st.write("L'algorithme comporte trois étapes :")
    st.markdown("""
    - **Génération des clés** (publique et privée).
    - **Chiffrement** du message avec la clé publique.
    - **Déchiffrement** du message avec la clé privée.
    """)
    
    st.header("3) Génération des clés")
    st.markdown("""
    1. Choisir deux grands nombres premiers distincts $p$ et $q$.
    2. Calculer leur produit :
    """)
    st.latex(r"n = p 	imes q")
    st.markdown("""
    3. Calculer l'indicatrice d'Euler de $n$ :
    """)
    st.latex(r"\varphi(n) = (p - 1)(q - 1)")
    st.markdown("""
    4. Choisir un entier appelé **exposant de chiffrement** $e$ tel que :
    """)
    st.latex(r"1 < e < \varphi(n) \quad 	ext{et} \quad \gcd(e, \varphi(n)) = 1")
    st.markdown("""
    Fréquemment, on choisit $e = 65537$.
    5. Déterminer l'**exposant de déchiffrement** $d$, tel que :
    """)
    st.latex(r"e \times d \equiv 1 \mod \varphi(n)")
    
    st.header("4) Chiffrement et déchiffrement")
    st.write("Le chiffrement et le déchiffrement suivent ces formules :")
    st.latex(r"C \equiv M^e \mod n")
    st.latex(r"M \equiv C^d \mod n")
    
    st.header("5) Justification mathématique")
    st.write("L'entier $e$ étant premier avec $\varphi(n)$, l'identité de Bézout garantit l'existence de deux entiers $d$ et $k$ tels que :")
    st.latex(r"e \times d + \varphi(n) 	imes k = 1")
    
    st.header("6) Exemple de génération de clés, chiffrement et déchiffrement")
    st.write("Nous allons illustrer le fonctionnement de RSA avec des petits nombres pour simplifier les calculs.")
    
    st.subheader("6.1 Génération des clés")
    st.latex(r"p = 3, \quad q = 11")
    st.latex(r"n = p 	imes q = 3 	imes 11 = 33")
    st.latex(r"\varphi(n) = (3 - 1) 	imes (11 - 1) = 2 	imes 10 = 20")
    st.latex(r"e = 3")
    st.latex(r"d = 7")
    
    st.subheader("6.2 Chiffrement")
    st.write("Bob veut envoyer le message $M = 4$ à Alice. Il chiffre le message avec la clé publique :")
    st.latex(r"C = M^e \mod n")
    st.latex(r"C = 4^3 \mod 33 = 31")
    
    st.subheader("6.3 Déchiffrement")
    st.write("Alice reçoit $C = 31$ et le déchiffre avec sa clé privée :")
    st.latex(r"M' = C^d \mod n")
    st.latex(r"M' = 31^7 \mod 33 = 4")
    
    st.subheader("6.4 Conclusion")
    st.write("Cet exemple illustre bien le fonctionnement de RSA, même si en pratique on utilise des nombres bien plus grands pour garantir la sécurité.")
    
if __name__ == "__main__":
    main()
