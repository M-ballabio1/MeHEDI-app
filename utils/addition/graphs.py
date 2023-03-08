from streamlit_elements import elements, mui
from streamlit_elements import nivo

DATA = [{"taste": "RISULTATI", "Peso Area": 4},
        {"taste": "CONSAPEVOLEZZA E FIDUCIA", "Peso Area": 3},
        {"taste": "COINVOLGIMENTO", "Peso Area": 3.5},
        {"taste": "DISTINTIVITA'", "Peso Area": 4},
        {"taste": "COMPORTAMENTI", "Peso Area": 4.3}]

def graph_pes(DATA):
        with elements("nivo_charts"):        
            with mui.Box(sx={"height": 400}):
                nivo.Radar(
                    data=DATA,
                    keys=["Peso Area"],
                    indexBy="taste",
                    maxValue=5,
                    valueFormat=">-.2f",
                    margin={"top": 80, "right": 50, "bottom": 80, "left": 50},
                    borderColor={"from": "color"},
                    gridLabelOffset=36,
                    dotSize=10,
                    dotColor="#ec8989",
                    dotBorderWidth=2,
                    motionConfig="wobbly",
                    legends=[
                        {
                            "anchor": "top-left",
                            "direction": "column",
                            "translateX": -70,
                            "translateY": -100,
                            "itemWidth": 40,
                            "itemHeight": 20,
                            "itemTextColor": "#999",
                            "symbolSize": 12,
                            "symbolShape": "circle",
                            "effects": [
                                {
                                    "on": "hover",
                                    "style": {
                                        "itemTextColor": "#000"
                                    }
                                }
                            ]
                        }
                    ],
                    theme={
                        "background": "#E4E3E3",
                        "textColor": "#31333F",
                        "tooltip": {
                            "container": {
                                "background": "#E4E3E3",
                                "color": "#31333F",
                            }
                        }
                    }
                )
