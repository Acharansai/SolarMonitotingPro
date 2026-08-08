from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from .models import Alert


@login_required
def alert_list(request):

    alerts = Alert.objects.all().order_by("-created_at")

    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    severity = request.GET.get("severity")

    if start and end:
        alerts = alerts.filter(created_at__date__range=[start, end])

    if severity:
        alerts = alerts.filter(severity=severity)

    critical_count = Alert.objects.filter(severity="CRITICAL").count()
    warning_count = Alert.objects.filter(severity="WARNING").count()
    info_count = Alert.objects.filter(severity="INFO").count()
    open_count = Alert.objects.count()

    paginator = Paginator(alerts, 20)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "alerts/alerts.html",
        {
            "page_obj": page_obj,
            "critical_count": critical_count,
            "warning_count": warning_count,
            "info_count": info_count,
            "open_count": open_count,
            "start": start,
            "end": end,
            "severity": severity,
        },
    )



@login_required
def export_alerts_excel(request):

    alerts = Alert.objects.all().order_by("-created_at")

    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    severity = request.GET.get("severity")

    if start and end:
        alerts = alerts.filter(created_at__date__range=[start, end])

    if severity:
        alerts = alerts.filter(severity=severity)

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Alerts"

    sheet.append([
        "Date & Time",
        "Device",
        "Title",
        "Message",
        "Severity"
    ])

    for alert in alerts:

        sheet.append([
            alert.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            alert.device.device_name,
            alert.title,
            alert.message,
            alert.severity,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="alerts.xlsx"'
    )

    workbook.save(response)

    return response


@login_required
def export_alerts_pdf(request):

    alerts = Alert.objects.all().order_by("-created_at")

    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    severity = request.GET.get("severity")

    if start and end:
        alerts = alerts.filter(created_at__date__range=[start, end])

    if severity:
        alerts = alerts.filter(severity=severity)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="alerts.pdf"'

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph("<b>SolarMonitorPro - Alerts Report</b>", styles["Title"])

    elements.append(title)

    table_data = [[
        "Date",
        "Device",
        "Title",
        "Severity"
    ]]

    for alert in alerts:

        table_data.append([
            alert.created_at.strftime("%Y-%m-%d %H:%M"),
            alert.device.device_name,
            alert.title,
            alert.severity,
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("BOTTOMPADDING", (0,0), (-1,0), 10),

    ]))

    elements.append(table)

    doc.build(elements)

    return response