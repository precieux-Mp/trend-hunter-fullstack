# ===== Étape 1 : compilation (build) =====
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# On copie d'abord le pom.xml pour profiter du cache Docker
COPY pom.xml .
COPY .mvn/ .mvn/
COPY mvnw .

# On télécharge les dépendances (mises en cache si le pom ne change pas)
RUN mvn dependency:go-offline -B

# On copie le code source et on compile en .jar (sans lancer les tests)
COPY src/ src/
RUN mvn clean package -DskipTests -B

# ===== Étape 2 : exécution (runtime) =====
FROM eclipse-temurin:17-jre
WORKDIR /app

# On récupère UNIQUEMENT le .jar produit à l'étape 1
COPY --from=build /app/target/*.jar app.jar

# Le backend écoute sur le port 8080
EXPOSE 8080

# Commande lancée au démarrage du conteneur
ENTRYPOINT ["java", "-jar", "app.jar"]
