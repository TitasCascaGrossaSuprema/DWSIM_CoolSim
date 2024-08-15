import pandas as pd
import numpy as np
import time

import io
from scipy.integrate import solve_ivp
import plotly.graph_objs as go

from tensorflow.keras.models import load_model
import pickle
from apps.run_DWSIM import *


def Simulate_DWSIM_DOE():
    # Marcar o início
    inicio = time.time()

    df = pd.read_excel('datasets/DOE_LHC.xlsx')
    numberofsimulations = len(df)

    exportdataset = pd.DataFrame(columns=['Evaporator Temperature',
                                          'Condenser Temperature',
                                          'Adiabatic Efficiency',
                                          'Compressor Energy',
                                          'Electric Current',
                                          'Discharge Temperature',
                                          'Refrigerant Mass Flow'])

    for i in range(numberofsimulations):
        inicio_i = time.time()
        evaporator_temperature_value = df.iloc[i]['Evaporator Temperature']
        condenser_temperature_value = df.iloc[i]['Condenser Temperature']
        adiabatic_efficiency_value = df.iloc[i]['Adiabatic Efficiency']

        energy, discharge_temperature, mass_flow = run_DWSIM(evaporator_temperature=evaporator_temperature_value,
                                                             condenser_temperature=condenser_temperature_value,
                                                             adiabatic_efficiency=adiabatic_efficiency_value)

        energy = energy * 1000
        discharge_temperature = discharge_temperature - 273.15
        mass_flow = mass_flow * 60
        electric_current = energy / 220

        print(str(i+1) + ' of ' + str(numberofsimulations))
        # Marcar o fim
        fim = time.time()

        # Calcular e exibir o tempo decorrido
        tempo_i = fim - inicio_i
        print(f"Time spent on the iteration: {tempo_i:.2f} s")

        estimated_time = ((fim - inicio)/(i+1))*(numberofsimulations-(i+1))
        print(f"Estimated time for DOE completion: {estimated_time/60:.1f} min")

        designdata = np.array([evaporator_temperature_value,
                               condenser_temperature_value,
                               adiabatic_efficiency_value,
                               energy,
                               electric_current,
                               discharge_temperature,
                               mass_flow])

        exportdataset.loc[len(exportdataset)] = designdata

        if i % int(numberofsimulations / 10) == 0:
            status = round((i / numberofsimulations) * 100, 0)
            with open('assets/status.txt', 'w') as file:
                file.write(str(status))

    exportfile = 'datasets/ODEs_Dataset.xlsx'
    exportdataset.to_excel(exportfile, index=False)
