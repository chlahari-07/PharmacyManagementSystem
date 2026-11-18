FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY ["src/Common/PharmacyManagement.Common/PharmacyManagement.Common.csproj", "src/Common/PharmacyManagement.Common/"]
COPY ["src/Services/PaymentService/PaymentService.csproj", "src/Services/PaymentService/"]
RUN dotnet restore "src/Services/PaymentService/PaymentService.csproj"
COPY . .
WORKDIR "/app/src/Services/PaymentService"
RUN dotnet build "PaymentService.csproj" -c Release -o /app/build
RUN dotnet publish "PaymentService.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:5004
EXPOSE 5004
ENTRYPOINT ["dotnet", "PaymentService.dll"]
