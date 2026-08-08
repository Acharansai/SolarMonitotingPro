from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render


from .models import Device, SolarPlant
from .forms import DeviceForm, SolarPlantForm


@login_required
def device_list(request):

    devices = Device.objects.select_related("plant").all()

    search = request.GET.get("search", "").strip()

    if search:
        devices = devices.filter(
            device_name__icontains=search
        ) | devices.filter(
            serial_number__icontains=search
        ) | devices.filter(
            manufacturer__icontains=search
        )

    devices = devices.order_by("device_name")

    paginator = Paginator(devices, 20)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "devices/device_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        },
    )


@login_required
def device_create(request):

    if request.method == "POST":

        form = DeviceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("devices:device_list")

    else:
        form = DeviceForm()

    return render(
        request,
        "devices/device_form.html",
        {
            "form": form,
            "title": "Add Device",
        },
    )


@login_required
def device_detail(request, pk):

    device = get_object_or_404(
        Device.objects.select_related("plant"),
        pk=pk,
    )

    return render(
        request,
        "devices/device_detail.html",
        {
            "device": device,
        },
    )


@login_required
def device_update(request, pk):

    device = get_object_or_404(Device, pk=pk)

    if request.method == "POST":

        form = DeviceForm(
            request.POST,
            instance=device
        )

        if form.is_valid():
            form.save()
            return redirect(
                "devices:device_detail",
                pk=device.pk
            )

    else:
        form = DeviceForm(instance=device)

    return render(
        request,
        "devices/device_form.html",
        {
            "form": form,
            "title": "Edit Device",
            "device": device,
        },
    )


@login_required
def device_delete(request, pk):

    device = get_object_or_404(Device, pk=pk)

    if request.method == "POST":
        device.delete()
        return redirect("devices:device_list")

    return render(
        request,
        "devices/device_confirm_delete.html",
        {
            "device": device,
        },
    )

@login_required
def plant_list(request):

    plants = SolarPlant.objects.all().order_by("plant_name")

    search = request.GET.get("search", "").strip()

    if search:
        plants = plants.filter(
            plant_name__icontains=search
        ) | plants.filter(
            location__icontains=search
        )

    paginator = Paginator(plants, 20)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "devices/plant_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        },
    )


@login_required
def plant_create(request):

    if request.method == "POST":

        form = SolarPlantForm(request.POST)

        if form.is_valid():
            plant = form.save()

            return redirect(
                "devices:plant_detail",
                pk=plant.pk
            )

    else:
        form = SolarPlantForm()

    return render(
        request,
        "devices/plant_form.html",
        {
            "form": form,
            "title": "Add Solar Plant",
        },
    )


@login_required
def plant_detail(request, pk):

    plant = get_object_or_404(
        SolarPlant,
        pk=pk
    )

    devices = plant.devices.all()

    return render(
        request,
        "devices/plant_detail.html",
        {
            "plant": plant,
            "devices": devices,
        },
    )


@login_required
def plant_update(request, pk):

    plant = get_object_or_404(
        SolarPlant,
        pk=pk
    )

    if request.method == "POST":

        form = SolarPlantForm(
            request.POST,
            instance=plant
        )

        if form.is_valid():

            form.save()

            return redirect(
                "devices:plant_detail",
                pk=plant.pk
            )

    else:

        form = SolarPlantForm(
            instance=plant
        )

    return render(
        request,
        "devices/plant_form.html",
        {
            "form": form,
            "title": "Edit Solar Plant",
            "plant": plant,
        },
    )


@login_required
def plant_delete(request, pk):

    plant = get_object_or_404(
        SolarPlant,
        pk=pk
    )

    if request.method == "POST":

        plant.delete()

        return redirect(
            "devices:plant_list"
        )

    return render(
        request,
        "devices/plant_confirm_delete.html",
        {
            "plant": plant,
        },
    )