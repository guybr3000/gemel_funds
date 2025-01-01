import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

data = pd.read_csv('data.csv')
df = pd.DataFrame(data)

rating_colors = {
    "A": "green",
    "Ba": "lightgreen",
    "Bb": "Wheat",
    "Bc": "darkorange",
    "C": "red"
}

fig = go.Figure()

for grp in df["grp"].unique():
    filtered_df = df[df["grp"] == grp]
    for rating in filtered_df["Rating"].unique():
        rating_df = filtered_df[filtered_df["Rating"] == rating]

       
        hover_text = [
            f"קופה: {row['ID']}<br>ציון קודם: {row['Prev']}<br>ציון נוכחי: {row['Current']}<br>קבוצה: {row['grp']}<br>דירוג: {row['Rating']}"
            for _, row in rating_df.iterrows()
        ]

        fig.add_trace(
            go.Scatter(
                x=rating_df["Current"],
                y=rating_df["Prev"],
                mode="markers",
                name=f"{grp} - {rating}",
                visible=(grp == df["grp"].unique()[0]),  
                marker=dict(size=10, color=rating_colors.get(rating, "gray")),  
                hoverinfo="text",
                text=hover_text,  
            )
        )



fig.add_trace(
    go.Scatter(
        x=[0, 1],  
        y=[0, 1], 
        mode="lines",
        name="45° Line",
        line=dict(color="black", dash="dash", width=1, backoff=0.5),  
        showlegend=True,
    )
)

dropdown_buttons = [
    {
        "label": "הכל",
        "method": "update",
        "args": [
            {"visible": [True] * len(fig.data)}, 
            {"title": "כל הקבוצות"},
        ],
    }
]

for grp in df["grp"].unique():
    visible_list = [False] * (len(fig.data) - 1) + [True]  
    for i, trace in enumerate(fig.data[:-1]):
        if grp in trace.name:
            visible_list[i] = True  
    dropdown_buttons.append(
        {
            "label": grp,
            "method": "update",
            "args": [
                {"visible": visible_list},  
                {"title": f"שם קבוצה: {grp}"},  
            ],
        }
    )


fig.update_layout(
    updatemenus=[
        {
            "buttons": dropdown_buttons,
            "direction": "down",
            "showactive": True,
            "x": 0.1,
            "y": 1.15,
        }
    ],

    title_x=0.5,  
    xaxis_title="ציון נוכחי",
    yaxis_title="ציון קודם",
    width=1000,
    height=600,
)

st.title("קופות גמל - ניתוח קלאסטרים")



st.plotly_chart(fig, use_container_width=True)

