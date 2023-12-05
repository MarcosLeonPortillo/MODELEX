from django import forms


class MaestroDetalleForm(forms.Form):
    marca_modelo = forms.CharField(label='Marca/Modelo',label_suffix=":", required=False)
    libre_alquilada = forms.ChoiceField(label='Estado Moto', choices=[(0,'Cualquiera'),(1,'Libre'),(2,'Alquilada')], initial=0,
                                        widget=forms.RadioSelect)
