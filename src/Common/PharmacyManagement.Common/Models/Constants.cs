namespace PharmacyManagement.Common.Models;

public static class UserRoles
{
    public const string Admin = "Admin";
    public const string Doctor = "Doctor";
}

public static class OrderStatuses
{
    public const string Cart = "Cart";
    public const string Pending = "Pending";
    public const string Verified = "Verified";
    public const string PickedUp = "PickedUp";
    public const string Cancelled = "Cancelled";

    public static readonly HashSet<string> ValidStatuses = new(StringComparer.OrdinalIgnoreCase)
    {
        Cart,
        Pending,
        Verified,
        PickedUp,
        Cancelled
    };
}

public static class PaymentStatuses
{
    public const string Pending = "Pending";
    public const string Completed = "Completed";
    public const string Failed = "Failed";
}

public static class ReportTypes
{
    public const string Daily = "Daily";
    public const string Weekly = "Weekly";
    public const string Monthly = "Monthly";
    public const string Yearly = "Yearly";

    public static readonly HashSet<string> ValidReportTypes = new(StringComparer.OrdinalIgnoreCase)
    {
        Daily,
        Weekly,
        Monthly,
        Yearly
    };
}
