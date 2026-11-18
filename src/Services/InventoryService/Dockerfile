FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY ["src/Common/PharmacyManagement.Common/PharmacyManagement.Common.csproj", "src/Common/PharmacyManagement.Common/"]
COPY ["src/Services/InventoryService/InventoryService.csproj", "src/Services/InventoryService/"]
RUN dotnet restore "src/Services/InventoryService/InventoryService.csproj"
COPY . .
WORKDIR "/app/src/Services/InventoryService"
RUN dotnet build "InventoryService.csproj" -c Release -o /app/build
RUN dotnet publish "InventoryService.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:5002
EXPOSE 5002
ENTRYPOINT ["dotnet", "InventoryService.dll"]
