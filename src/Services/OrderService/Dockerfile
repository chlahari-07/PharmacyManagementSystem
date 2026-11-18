FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY ["src/Common/PharmacyManagement.Common/PharmacyManagement.Common.csproj", "src/Common/PharmacyManagement.Common/"]
COPY ["src/Services/OrderService/OrderService.csproj", "src/Services/OrderService/"]
RUN dotnet restore "src/Services/OrderService/OrderService.csproj"
COPY . .
WORKDIR "/app/src/Services/OrderService"
RUN dotnet build "OrderService.csproj" -c Release -o /app/build
RUN dotnet publish "OrderService.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:5003
EXPOSE 5003
ENTRYPOINT ["dotnet", "OrderService.dll"]
