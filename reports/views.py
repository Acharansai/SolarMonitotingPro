from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
)

from devices.models import Device, SolarPlant
from monitoring.models import SensorData


@login_required
def reports(request):

    # Get filters
    start = request.GET.get("start_date", "").strip()
    end = request.GET.get("end_date", "").strip()

    plant_id = request.GET.get("plant", "").strip()
    device_id = request.GET.get("device", "").strip()

    # Base queryset
    reports = (
        SensorData.objects
        .select_related("device", "device__plant")
        .order_by("-timestamp")
    )

    # Date filter
    if start and end:

        reports = reports.filter(
            timestamp__date__range=[start, end]
        )

    elif start:

        reports = reports.filter(
            timestamp__date__gte=start
        )

    elif end:

        reports = reports.filter(
            timestamp__date__lte=end
        )

    # Solar Plant filter
    if plant_id:

        reports = reports.filter(
            device__plant_id=plant_id
        )

    # Device filter
    if device_id:

        reports = reports.filter(
            device_id=device_id
        )

    # Pagination
    paginator = Paginator(
        reports,
        20
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    # Solar Plants
    plants = (
        SolarPlant.objects
        .all()
        .order_by("plant_name")
    )

    # Devices
    if plant_id:

        devices = (
            Device.objects
            .filter(plant_id=plant_id)
            .select_related("plant")
            .order_by("device_name")
        )

    else:

        devices = (
            Device.objects
            .select_related("plant")
            .all()
            .order_by("device_name")
        )

    # Context
    context = {
        "page_obj": page_obj,

        "plants": plants,

        "devices": devices,

        "start": start,

        "end": end,

        "selected_plant": plant_id,

        "selected_device": device_id,
    }

    return render(
        request,
        "reports/reports.html",
        context
    )

@login_required
def export_excel(request):

    start = request.GET.get("start_date", "").strip()
    end = request.GET.get("end_date", "").strip()

    plant_id = request.GET.get("plant", "").strip()
    device_id = request.GET.get("device", "").strip()


    reports = (
        SensorData.objects
        .select_related("device", "device__plant")
        .order_by("-timestamp")
    )


    # Date filters

    if start and end:

        reports = reports.filter(
            timestamp__date__range=[start, end]
        )

    elif start:

        reports = reports.filter(
            timestamp__date__gte=start
        )

    elif end:

        reports = reports.filter(
            timestamp__date__lte=end
        )


    # Plant filter

    if plant_id:

        reports = reports.filter(
            device__plant_id=plant_id
        )


    # Device filter

    if device_id:

        reports = reports.filter(
            device_id=device_id
        )


    # Create workbook

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Solar Report"


    # Headers

    headers = [
        "#",
        "Date & Time",
        "Solar Plant",
        "Device",
        "Voltage (V)",
        "Current (A)",
        "Power (W)",
        "Energy (kWh)",
        "Temperature (°C)",
        "Frequency (Hz)",
        "Power Factor",
    ]


    worksheet.append(headers)


    # Data

    for index, data in enumerate(
        reports,
        start=1
    ):

        worksheet.append([

            index,

            data.timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            data.device.plant.plant_name,

            data.device.device_name,

            float(data.voltage),

            float(data.current),

            float(data.power),

            float(data.energy),

            float(data.temperature),

            float(data.frequency),

            float(data.power_factor),

        ])


    # Column widths

    widths = [
        8,
        22,
        25,
        20,
        15,
        15,
        15,
        15,
        18,
        18,
        18,
    ]


    for column, width in enumerate(
        widths,
        start=1
    ):

        worksheet.column_dimensions[
            chr(64 + column)
        ].width = width


    # Response

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        )
    )


    response[
        "Content-Disposition"
    ] = (
        'attachment; filename="solar_report.xlsx"'
    )


    workbook.save(response)


    return response

@login_required
def export_pdf(request):

    start = request.GET.get("start_date", "").strip()
    end = request.GET.get("end_date", "").strip()

    plant_id = request.GET.get("plant", "").strip()
    device_id = request.GET.get("device", "").strip()


    reports = (
        SensorData.objects
        .select_related("device", "device__plant")
        .order_by("-timestamp")
    )


    # Date filters

    if start and end:

        reports = reports.filter(
            timestamp__date__range=[start, end]
        )

    elif start:

        reports = reports.filter(
            timestamp__date__gte=start
        )

    elif end:

        reports = reports.filter(
            timestamp__date__lte=end
        )


    # Plant filter

    if plant_id:

        reports = reports.filter(
            device__plant_id=plant_id
        )


    # Device filter

    if device_id:

        reports = reports.filter(
            device_id=device_id
        )


    response = HttpResponse(
        content_type="application/pdf"
    )


    response[
        "Content-Disposition"
    ] = (
        'attachment; filename="solar_report.pdf"'
    )


    document = SimpleDocTemplate(

        response,

        pagesize=landscape(A4),

        rightMargin=8 * mm,

        leftMargin=8 * mm,

        topMargin=8 * mm,

        bottomMargin=8 * mm,
    )


    table_data = [

        [
            "#",
            "Date & Time",
            "Plant",
            "Device",
            "Voltage",
            "Current",
            "Power",
            "Energy",
            "Temp",
            "Freq",
            "PF",
        ]

    ]


    for index, data in enumerate(
        reports,
        start=1
    ):

        table_data.append([

            index,

            data.timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            data.device.plant.plant_name,

            data.device.device_name,

            str(data.voltage),

            str(data.current),

            str(data.power),

            str(data.energy),

            str(data.temperature),

            str(data.frequency),

            str(data.power_factor),

        ])


    table = Table(
        table_data,
        repeatRows=1
    )


    table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.black
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

        ])

    )


    document.build([table])


    return response