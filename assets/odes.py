import pandas as pd
import numpy as np
import io
from scipy.integrate import solve_ivp

from assets.ReactionConstants import *


def ARGET_ODES(t, y):
    #Momentos de ordem zero para as cadeias:
    R0 = y[0] # Vivas
    Q0 = y[1] # Dormentes
    D0 = y[2] # Mortas

    #Momentos de ordem um para as cadeias:
    R1 = y[3] # Vivas
    Q1 = y[4] # Dormentes
    D1 = y[5] # Mortas

    #Momentos de ordem dois para as cadeias:
    R2 = y[6] # Vivas
    Q2 = y[7] # Dormentes
    D2 = y[8] # Mortas

    #Monomero
    M = y[9]

    #Iniciador
    P0X = y[10]

    #Radicais de iniciação
    P0 = y[11]

    #Espécie ativadora
    C = y[12]

    #Espécie desativadora
    CX = y[13]

    #Agente redutor
    A = y[14]

    #Agente redutor na forma oxidada
    AX = y[15]


    #Momentos de ordem zero para as cadeias:
    dR0dt = kp*M*P0 +kact*C*Q0 -kdact*CX*R0 -kt*(P0 + R0)*R0 -ktr*R0
    dQ0dt = -kact*C*Q0 +kdact*CX*R0
    dD0dt = (ktc/2)*R0*R0 +ktd*R0*R0 +kt*P0*R0 +ktr*R0

    dR1dt = kp*M*(P0 + R0) +kact*C*Q1 -kdact*CX*R1 -kt*(P0 + R0)*R1 -ktr*R1
    dQ1dt = -kact*C*Q1 +kdact*CX*R1
    dD1dt = kt*(P0 + R0)*R1 +ktr*R1

    dR2dt = kp*M*(P0 + R0 +2*R1) +kact*C*Q2 -kdact*CX*R2 -kt*(P0 + R0)*R2 -ktr*R2
    dQ2dt = -kact*C*Q2 +kdact*CX*R2
    dD2dt =kt*(P0 + R0)*R2 +ktc*R1*R1 +ktr*R2

    #Monômero
    dMdt = -kp*M*(R0 + P0)

    #Iniciador
    dP0Xdt = -kact0*P0X*C +kdact0*P0*CX

    #Radicais de iniciação
    dP0dt = -kp*M*P0 +kact0*P0X*C -kdact0*P0*CX -kt*(R0 + P0)*P0 -ktr*P0

    #Espécie ativadora
    dCdt = -kact0*P0X*C +kdact0*P0*CX -kact*C*Q0 +kdact*CX*R0 +kr*A*CX

    #Espécie desativadora
    dCXdt = -dCdt

    #Agente redutor
    dAdt = -kr*A*CX

    #Agente redutor na forma oxidada
    dAXdt = -dAdt

    return [dR0dt, dQ0dt, dD0dt,
            dR1dt, dQ1dt, dD1dt,
            dR2dt, dQ2dt, dD2dt,
            dMdt,
            dP0Xdt, dP0dt,
            dCdt, dCXdt,
            dAdt, dAXdt]


def SolveODEs(initial_conditions):
    global t, y
    total_time = 40*3600
    t_eval = np.linspace(0, total_time, num=int(total_time*10), endpoint=True)

    sol = solve_ivp(ARGET_ODES,
                [0, total_time],
                initial_conditions,
                method='LSODA', #Radau / LSODA
                t_eval=t_eval)
    t = np.transpose(sol.t)
    y = np.transpose(sol.y)



def MoreUsableDataset():
    global t, y

    df_time = pd.DataFrame({'Time':t})

    temp_variable_names = ['R0', 'Q0', 'D0',
                           'R1', 'Q1', 'D1',
                           'R2', 'Q2', 'D2',
                           'M',
                           'P0X', 'P0',
                           'C', 'CX',
                           'A', 'AX']

    df_num_sol = pd.DataFrame(y, columns=temp_variable_names)
    results = pd.concat([df_time,df_num_sol], axis=1)

    results['X'] = (results['M'].iloc[0]-results['M'])/results['M'].iloc[0]
    results['DPn'] = (results['R1']+results['Q1']+results['D1'])/(results['R0']+results['Q0']+results['D0'])
    results['DPw'] = (results['R2']+results['Q2']+results['D2'])/(results['R1']+results['Q1']+results['D1'])

    results['Mn'] = MWm * results['DPn']
    results['PDI'] = results['DPw']/results['DPn']
    results['Time'] = results['Time']/3600

    return results


def SimulateODEs():
    df = pd.read_excel('datasets/DOE_LHC.xlsx')
    numberofsimulations = len(df)

    exportdataset = pd.DataFrame(columns=['POX/C',
                                          'C/A',
                                          'POX/M',
                                          'X',
                                          'PDI',
                                          'Mn'])

    for i in range(numberofsimulations):
        Temp_P0XC = df.iloc[i]['POX/C']
        Temp_CA = df.iloc[i]['C/A']
        Temp_POXM = df.iloc[i]['POX/M']

        POX = Temp_POXM * M
        C = POX / Temp_P0XC
        A = C / Temp_CA

        Initial_Conditions = [0, 0, 0,
                              0, 0, 0,
                              0, 0, 0,
                              M,
                              POX, 0,
                              C, 0,
                              A, 0]

        SolveODEs(Initial_Conditions)
        results = MoreUsableDataset()

        designdata = np.array([POX / C, C / A, POX / M,
                               results['X'].iloc[-1],
                               results['PDI'].iloc[-1],
                               results['Mn'].iloc[-1]])

        exportdataset.loc[len(exportdataset)] = designdata

        if i % int(numberofsimulations / 20) == 0:
            status = round((i / numberofsimulations) * 100, 0)
            with open('assets/status.txt', 'w') as file:
                file.write(str(status))

    exportfile = 'datasets/ARGET_ATRP_ODEs_Dataset.xlsx'
    exportdataset.to_excel(exportfile, index=False)


    
    