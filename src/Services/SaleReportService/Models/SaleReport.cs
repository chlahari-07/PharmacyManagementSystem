using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace SaleReportService.Models;

[Table("SaleReports")]
public class SaleReport
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int SaleReportId { get; set; }

    [Required]
    [MaxLength(20)]
    public string ReportType { get; set; } = "Daily"; // Daily, Weekly, Monthly, Yearly

    [Required]
    public DateTime FromDate { get; set; }

    [Required]
    public DateTime ToDate { get; set; }

    [Required]
    public int TotalOrders { get; set; }

    [Required]
    [Column(TypeName = "decimal(18,2)")]
    public decimal TotalRevenue { get; set; }

    public DateTime GeneratedDate { get; set; } = DateTime.UtcNow;

    [Required]
    [Column(TypeName = "decimal(18,2)")]
    public decimal Profit { get; set; }
}
