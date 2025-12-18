# =========================
# Étape 1 : Build
# =========================
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src

# Copier uniquement le fichier csproj pour profiter du cache
COPY Worker.csproj ./

# Restaurer les dépendances
RUN dotnet restore

# Copier le reste du code
COPY . .

# Publier l'exécutable (production)
RUN dotnet publish -c Release --self-contained false --no-restore -o /app/publish

# =========================
# Étape 2 : Runtime
# =========================
FROM mcr.microsoft.com/dotnet/runtime:7.0
WORKDIR /app

# Copier le résultat publié
COPY --from=build /app/publish .

# Point d'entrée
ENTRYPOINT ["dotnet", "Worker.dll"]
