# Step 1: Build
FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src

# Copy only the csproj file to leverage Docker cache
COPY Worker.csproj ./

# Restore dependencies
RUN dotnet restore

# Copy the rest of the source code
COPY . .

# Publish the executable (production)
RUN dotnet publish -c Release --self-contained false --no-restore -o /app/publish

# Step 2: Runtime
FROM mcr.microsoft.com/dotnet/runtime:7.0
WORKDIR /app

# Copy the published output knowing from the build stage
COPY --from=build /app/publish .

# Entry point
ENTRYPOINT ["dotnet", "Worker.dll"]
