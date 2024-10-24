from django.shortcuts import render
from django.views.generic import TemplateView
import folium
import pandas as pd

class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        figure = folium.Figure()


        municipios_coordenadas = {
            'João Pessoa': [-7.11532, -34.861],
            'Mamanguape': [-6.830279074483519, -35.11999458809625],
            'Guarabira':[-6.850598322874815, -35.49112792483982],
            'Pedra Branca': [-7.421690, -38.068900]
        }

        data = pd.read_csv('util/locais_de_servicos_do_governo_pb_att.csv')

        municipios = data['Municipio'].unique() if not data.empty else []

        
        city = self.request.GET.get('city', 'todas')
        local_type = self.request.GET.get('local_type', 'todos')


        if city != 'todas' and not data.empty:
            data = data[data['Municipio'] == city]

        if local_type != 'todos' and not data.empty:
            data = data[data['Categoria'] == local_type]

        
        map_location = municipios_coordenadas.get(city, [-7.11532, -34.861])  # Default: João Pessoa

        
        map = folium.Map(
            location=map_location,  
            zoom_start=11,
            tiles='OpenStreetMap'
        )

        
        marker_properties = {
            'Trânsito': {'icon': 'car', 'color': 'blue'},
            'Educação': {'icon': 'graduation-cap', 'color': 'green'},
            'Segurança': {'icon': 'shield', 'color': 'red'},
        }

        
        if not data.empty:
            for index, row in data.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=f"{row['Categoria'].capitalize()}: {row['Nome']} - {row['Endereco']}",
                    tooltip=row['Nome'],  # Mostra o nome ao passar o mouse
                    icon=folium.Icon(
                        icon=marker_properties.get(row['Categoria'], {'icon': 'info', 'color': 'gray'})['icon'],
                        color=marker_properties.get(row['Categoria'], {'icon': 'info', 'color': 'gray'})['color'],
                        prefix='fa'
                    )
                ).add_to(map)

        
        map.add_to(figure)
        figure.render()

        context = {
            "map": figure,
            "municipios": municipios,
            "selected_city": city,
            "selected_category": local_type,
            "locais": data.to_dict(orient='records') if not data.empty else []
        }

        return context
