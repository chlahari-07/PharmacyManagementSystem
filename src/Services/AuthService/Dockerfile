FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY ["src/Common/PharmacyManagement.Common/PharmacyManagement.Common.csproj", "src/Common/PharmacyManagement.Common/"]
COPY ["src/Services/AuthService/AuthService.csproj", "src/Services/AuthService/"]
RUN dotnet restore "src/Services/AuthService/AuthService.csproj"
COPY . .
WORKDIR "/app/src/Services/AuthService"
RUN dotnet build "AuthService.csproj" -c Release -o /app/build
RUN dotnet publish "AuthService.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:5001
EXPOSE 5001
ENTRYPOINT ["dotnet", "AuthService.dll"]
