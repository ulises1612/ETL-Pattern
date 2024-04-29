##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: application.py
# Capitulo: Flujo de Datos
# Autor(es): Perla Velasco & Yonathan Mtz. & Jorge Solís
# Version: 1.0.0 Noviembre 2022
# Descripción:
#
#   Este archivo define la aplicación que sirve la UI y la lógica 
#   del componente
#
#-------------------------------------------------------------------------
from src.controller.dashboard_controller import DashboardController
from src.view.dashboard import Dashboard
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Output, Input
import plotly.express as px

app = dash.Dash(
    external_stylesheets=[dbc.themes.LUX],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

@app.callback(
    Output('orders-value', 'children'),
    Input('start-date', 'start_date'),
    Input('start-date', 'end_date')
)
def update_orders_from_date_range(start_date, end_date):
    if start_date is None or end_date is None:
        return 'No data'
    orders = DashboardController.load_orders_by_period(start_date, end_date)
    return orders['orders']

@app.callback(
    Output('products-value', 'children'),
    Input('start-date', 'start_date'),
    Input('start-date', 'end_date')
)
def update_products_from_date_range(start_date, end_date):
    if start_date is None or end_date is None:
        return 'No data'
    products = DashboardController.load_products_by_period(start_date, end_date)
    return products['products']

@app.callback(
    Output('providers-value', 'children'),
    Input('start-date', 'start_date'),
    Input('start-date', 'end_date')
)
def update_providers_from_date_range(start_date, end_date):
    if start_date is None or end_date is None:
        return 'No data'
    providers = DashboardController.load_providers_by_period(start_date, end_date)
    return providers['providers']

@app.callback(
    Output('sales-value', 'children'),
    Input('start-date', 'start_date'),
    Input('start-date', 'end_date')
)
def update_sales_from_date_range(start_date, end_date):
    if start_date is None or end_date is None:
        return 'No data'
    sales = DashboardController.load_sales_by_period(start_date, end_date)
    return f'$ {sales["sales"]:.2f}'

@app.callback(
    Output('sales-per-location-value', 'figure'),
    Input('start-date-2', 'start_date'),
    Input('start-date-2', 'end_date')
)
def update_sales_per_location_from_date_range(start_date, end_date):
    if start_date is None or end_date is None:
        return 'No data'
    sales = DashboardController.load_sales_per_location_by_period(start_date, end_date)
    bar_char_fig = px.bar(sales, x="location", y="sales")
    return bar_char_fig

app.title = "ETL"

dashboard = Dashboard()

app.layout = dashboard.document()