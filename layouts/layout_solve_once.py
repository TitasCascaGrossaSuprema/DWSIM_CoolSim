import dash
from dash import dcc, html, Input, Output, State, ctx, dash_table, Patch
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc


def layout_solve_once(M, MWm, Hours):
    layout = html.Div([
        html.Br(),

        html.Div([
            html.Div("Reaction Time (h):",
                     style={'width': '150px', 'textAlign': 'center', 'paddingRight': '10px', 'fontWeight': 'bold'}),
            dcc.Input(
                id="reaction_time_value_2",
                type='number',
                value=Hours,
                disabled=False,
                style={'width': '80px', 'textAlign': 'center', 'fontWeight': 'bold'}
            ),

            html.Div("Styrene Monomer Concentration (mol⋅L−1):",
                     style={'width': '150px', 'textAlign': 'center', 'paddingRight': '10px', 'fontWeight': 'bold'}),
            dcc.Input(
                id="styrene_monomer_value_2",
                type='number',
                value=M,
                disabled=False,
                style={'width': '80px', 'textAlign': 'center', 'fontWeight': 'bold'}
            ),

            html.Div("Monomer Molar Mass (g⋅mol−1):",
                     style={'width': '150px', 'textAlign': 'center', 'paddingRight': '10px', 'fontWeight': 'bold'}),
            dcc.Input(
                id="monomer_molar_mass_value_2",
                type='number',
                value=MWm,
                disabled=False,
                style={'width': '80px', 'textAlign': 'center', 'fontWeight': 'bold'}
            ),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '20px'}),

        html.Br(),

        html.Div([
            html.Div("P0X/C:",
                     style={'width': '150px', 'textAlign': 'center', 'paddingRight': '10px', 'fontWeight': 'bold'}),
            dcc.Input(
                id="POX_C_value",
                type='number',
                value="",
                disabled=False,
                style={'width': '80px', 'textAlign': 'center', 'fontWeight': 'bold'}
            ),

            html.Div("C/A:",
                     style={'width': '150px', 'textAlign': 'center', 'paddingRight': '10px', 'fontWeight': 'bold'}),
            dcc.Input(
                id="C_A_value",
                type='number',
                value="",
                disabled=False,
                style={'width': '80px', 'textAlign': 'center', 'fontWeight': 'bold'}
            ),

            html.Div("POX/M:",
                     style={'width': '150px', 'textAlign': 'center', 'paddingRight': '10px', 'fontWeight': 'bold'}),
            dcc.Input(
                id="POX_M_value",
                type='number',
                value="",
                disabled=False,
                style={'width': '80px', 'textAlign': 'center', 'fontWeight': 'bold'}
            ),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '20px'}),

        html.Div([
            html.Br(),
            html.Button('Run Simulation!', id='simulation-once-btn', n_clicks=0,
                        style={'backgroundColor': 'orange', 'color': 'white', 'fontWeight': 'bold',
                               'fontSize': '20px'}),
        ], style={'textAlign': 'center'}),

        html.Br(),
        dbc.Spinner(html.Div(id="loading-output4"), spinner_style={"marginTop": "40px"}),
        html.Br(),
        html.Br(),
        dcc.Graph(id='graph1', style={'display': 'none'}),
        dcc.Graph(id='graph2', style={'display': 'none'}),
        dcc.Graph(id='graph3', style={'display': 'none'}),
        dcc.Graph(id='graph4', style={'display': 'none'}),

    ], style={'textAlign': 'center'})

    return layout