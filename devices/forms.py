from django import forms
from .models import Device
from .models import SolarPlant


class DeviceForm(forms.ModelForm):

    class Meta:
        model = Device

        fields = [
            "plant",
            "device_name",
            "serial_number",
            "manufacturer",
            "model",
            "device_type",
            "status",
            "installed_on",
        ]

        widgets = {
            "plant": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "device_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter device name"
                }
            ),

            "serial_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter serial number"
                }
            ),

            "manufacturer": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter manufacturer"
                }
            ),

            "model": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter model"
                }
            ),

            "device_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "installed_on": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }



class SolarPlantForm(forms.ModelForm):

    class Meta:
        model = SolarPlant

        fields = [
            "plant_name",
            "location",
            "capacity_kw",
            "status",
        ]

        widgets = {
            "plant_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter solar plant name",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter plant location",
                }
            ),

            "capacity_kw": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Capacity in kW",
                    "step": "0.01",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }