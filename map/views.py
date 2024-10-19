from django.shortcuts import render
from django.views.generic import TemplateView
import folium
import pandas as pd

class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        figure = folium.Figure()

        # Coordenadas dos municípios
        municipios_coordenadas = {
            'João Pessoa': [-7.11532, -34.861],
            'Mamanguape': [-6.830279074483519, -35.11999458809625],
            'Guarabira':[-6.850598322874815, -35.49112792483982],
            'Pedra Branca': [-7.421690, -38.068900]
        }

        # Carregar os dados do CSV
        data = pd.read_csv('util\locais_de_servicos_do_governo_pb_att.csv')

        # Extrair os municípios únicos
        municipios = data['Municipio'].unique()

        # Filtrar dados com base nos parâmetros da requisição
        city = self.request.GET.get('city', 'todas')
        local_type = self.request.GET.get('local_type', 'todos')

        # Se o município for selecionado, filtra pelos dados correspondentes
        if city != 'todas':
            data = data[data['Municipio'] == city]

        if local_type != 'todos':
            data = data[data['Categoria'] == local_type]

        # Se o município estiver no dicionário, centralizar no local correto
        map_location = municipios_coordenadas.get(city, [-7.11532, -34.861])  # Default: João Pessoa

        # Criar o mapa centralizado na cidade selecionada
        map = folium.Map(
            location=map_location,  
            zoom_start=11,
            tiles='OpenStreetMap'
        )

        # Propriedades dos ícones dos marcadores por categoria
        marker_properties = {
            'Trânsito': {'icon': 'car', 'color': 'blue'},
            'Educação': {'icon': 'graduation-cap', 'color': 'green'},
            'Segurança': {'icon': 'shield', 'color': 'red'},
        }

        # Adicionar os marcadores no mapa
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

        # Adicionar o mapa à figura
        map.add_to(figure)
        figure.render()

        # Passar os municípios e seleção para o contexto
        return {
            "map": figure,
            "municipios": municipios,
            "selected_city": city,
            "selected_category": local_type
        }

