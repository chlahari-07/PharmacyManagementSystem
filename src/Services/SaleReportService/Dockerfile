FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app
COPY ["src/Common/PharmacyManagement.Common/PharmacyManagement.Common.csproj", "src/Common/PharmacyManagement.Common/"]
COPY ["src/Services/SaleReportService/SaleReportService.csproj", "src/Services/SaleReportService/"]
RUN dotnet restore "src/Services/SaleReportService/SaleReportService.csproj"
COPY . .
WORKDIR "/app/src/Services/SaleReportService"
RUN dotnet build "SaleReportService.csproj" -c Release -o /app/build
RUN dotnet publish "SaleReportService.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:5005
EXPOSE 5005
ENTRYPOINT ["dotnet", "SaleReportService.dll"]
