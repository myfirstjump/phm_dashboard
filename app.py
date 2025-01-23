import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

# 產生假資料
x_data = np.arange(1, 16)
y_data = np.array([0.05, 0.08, 0.06, 0.10, 0.32, 0.30, 0.07, 0.12, 0.05, 0.02, 0.09, 0.03, 0.01, 0.05, 0.06])

# 建立主圖表（含綠色取樣範圍）
main_fig = go.Figure(
    data=[go.Scatter(x=x_data, y=y_data, mode='lines+markers', name='測試數據')]
)
main_fig.update_layout(
    title='圖表標題',
    shapes=[
        dict(
            type='rect',
            xref='x',
            yref='paper',
            x0=3,
            x1=6,
            y0=0,
            y1=1,
            fillcolor='green',
            opacity=0.2,
            line_width=0
        )
    ],
    margin=dict(l=50, r=50, t=50, b=50),
    plot_bgcolor='rgba(240,240,240,1)'  # 淺色背景讓綠色區塊比較明顯
)

# 建立4個小圖表（油門、缸壓、溫度、震動）
titles = ['油門', '缸壓', '溫度', '震動']
small_figs = []
for t in titles:
    fig = go.Figure(
        data=[go.Scatter(x=x_data, y=y_data, mode='lines+markers', name=t)]
    )
    fig.update_layout(
        title=t,
        margin=dict(l=40, r=40, t=40, b=40),
        height=200,
        plot_bgcolor='rgba(240,240,240,1)'
    )
    small_figs.append(fig)

# -----------------------------------------------------------------------------
# Dash Layout
# -----------------------------------------------------------------------------
app.layout = html.Div(
    style={
        'backgroundColor': '#333333',
        'color': 'white',
        'fontFamily': 'Arial, sans-serif',
        'height': '100vh',       # 讓視窗滿高(可依需要調整/移除)
        'margin': '0',
        'padding': '10px'
    },
    children=[
        # 系統標題
        html.H2('PHM預診系統', style={'margin': '10px 0'}),
        
        # 「外框」：整個畫面分左右兩欄 (使用 Flex)
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'row',
                'height': '85%',     # 讓左右欄共用大約 85% 的高度
            },
            children=[
                # 左側容器
                html.Div(
                    style={
                        'flex': '0 0 65%',   # 左側佔 65% 寬度
                        'backgroundColor': '#444444',
                        'marginRight': '10px',
                        'display': 'flex',
                        'flexDirection': 'column',  # 上下排
                        'justifyContent': 'space-between',
                        'border': '2px solid #555', # 示意外框
                        'padding': '10px'
                    },
                    children=[
                        # 上方：資料路徑、預診結果(並排)
                        html.Div(
                            style={
                                'display': 'flex',
                                'flexDirection': 'row',
                                'justifyContent': 'space-between',
                                'marginBottom': '10px'
                            },
                            children=[
                                # 資料路徑
                                html.Div(
                                    style={
                                        'flex': '0 0 48%', 
                                        'border': '1px solid #666',  # 示意邊框
                                        'padding': '10px'
                                    },
                                    children=[
                                        html.Label('資料路徑：',
                                                   style={'marginRight': '10px'}),
                                        dcc.Dropdown(
                                            id='data-path-dropdown',
                                            options=[
                                                {'label': 'C:\\Users\\project\\data1.csv', 'value': 'data1.csv'},
                                                {'label': 'C:\\Users\\project\\data2.csv', 'value': 'data2.csv'},
                                            ],
                                            value='data1.csv',
                                            style={'width': '100%', 'color': '#000000'}
                                        )
                                    ]
                                ),
                                # 預診結果
                                html.Div(
                                    style={
                                        'flex': '0 0 48%',
                                        'border': '1px solid #666',  # 示意邊框
                                        'padding': '10px'
                                    },
                                    children=[
                                        html.Label('預診結果：',
                                                   style={'marginRight': '10px'}),
                                        dcc.Input(
                                            id='diagnosis-result',
                                            type='text',
                                            placeholder='請輸入預診結果',
                                            style={'width': '100%', 'color': '#000000'}
                                        )
                                    ]
                                )
                            ]
                        ),

                        # 中間：主圖表
                        html.Div(
                            style={
                                'borderTop': '2px solid #555',
                                'borderBottom': '2px solid #555',
                                'flex': '1',
                                'marginBottom': '10px',
                                'padding': '10px'
                            },
                            children=[
                                dcc.Graph(
                                    id='main-chart',
                                    figure=main_fig,
                                    style={'height': '100%'}
                                )
                            ]
                        ),

                        # 下方：取樣範圍 + 說明
                        html.Div(
                            style={
                                'border': '1px solid #666',
                                'padding': '10px',
                                'marginBottom': '10px'
                            },
                            children=[
                                html.Span("取樣範圍: 3 ~ 6 (可自訂)"),
                            ]
                        )
                    ]
                ),

                # 右側容器（資料預覽）
                html.Div(
                    style={
                        'flex': '0 0 35%',
                        'backgroundColor': '#444444',
                        'border': '2px solid #555', # 示意外框
                        'display': 'flex',
                        'flexDirection': 'column',
                        'justifyContent': 'space-around',
                        'padding': '10px'
                    },
                    children=[
                        # 小圖1
                        html.Div(
                            dcc.Graph(figure=small_figs[0]),
                            style={'marginBottom': '10px'}
                        ),
                        # 小圖2
                        html.Div(
                            dcc.Graph(figure=small_figs[1]),
                            style={'marginBottom': '10px'}
                        ),
                        # 小圖3
                        html.Div(
                            dcc.Graph(figure=small_figs[2]),
                            style={'marginBottom': '10px'}
                        ),
                        # 小圖4
                        html.Div(
                            dcc.Graph(figure=small_figs[3]),
                            style={'marginBottom': '10px'}
                        ),
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
