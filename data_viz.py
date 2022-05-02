import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import numpy as np
from vpython import *
import wx


class Window(wx.Frame):
    def __init__(self, title, data):
        super().__init__(parent=None, title=title, size=(800,600))
        self.panel = wx.Panel(self)
        self.data = data

        cat_columns =  ['protocol_type', 'service', 'flag', 'label']

        self.num_columns = ["duration","src_bytes","dst_bytes","wrong_fragment","urgent","hot","num_failed_logins","num_compromised","num_root","num_file_creations",
            "num_shells","num_access_files","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
            "srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate"]

        self.bin_columns = ['land', 'logged_in', 'root_shell', 'su_attempted', 'is_host_login', 'is_guest_login']

        # categorical data
        rb_1 = wx.RadioButton(self.panel, label='Bar chart', pos=(180, 20), style=wx.RB_GROUP)
        rb_2 = wx.RadioButton(self.panel, label='Pie chart', pos=(250, 20))
        self.panel.Bind(wx.EVT_RADIOBUTTON, self.onClick)

        self.cb_1 = wx.ComboBox(self.panel, value=cat_columns[0], choices=cat_columns, pos=(10,20), size=(150,45), style=wx.CB_READONLY)
        b_1 = wx.Button(self.panel, label='Show graph', pos=(320, 20))
        b_1.Bind(wx.EVT_BUTTON, self.onSubmit)
        self.graph_type = 'Bar chart'
        
        # heatmap
        b_2 = wx.Button(self.panel, label='Show heatmap', pos=(10, 60))
        b_2.Bind(wx.EVT_BUTTON, self.showHeatmap)

        # numerical data (scatterplots)
        self.cb_2 = wx.ComboBox(self.panel, value=self.num_columns[0], choices=self.num_columns, pos=(10,100), size=(180,45), style=wx.CB_READONLY)
        self.cb_3 = wx.ComboBox(self.panel, value=self.num_columns[0], choices=self.num_columns, pos=(200,100), size=(180,45), style=wx.CB_READONLY)
        self.cb_4 = wx.ComboBox(self.panel, value=self.bin_columns[0], choices=self.bin_columns, pos=(400,100), size=(150,45), style=wx.CB_READONLY)
        
        b_3 = wx.Button(self.panel, label='Show graph', pos=(560, 100))
        b_3.Bind(wx.EVT_BUTTON, self.showScatterplot)

        self.Show()


    def onClick(self, event):
        rb = event.GetEventObject()
        self.graph_type = rb.GetLabel()


    def onSubmit(self, event):
        selected = self.cb_1.GetStringSelection()
        plt.figure(figsize = (18, 9))
        categories = self.data[selected].value_counts().index
        counts = self.data[selected].value_counts().values

        if self.graph_type == 'Bar chart':
            plt.bar(categories, counts, width=0.25)
        else:
            plt.pie(counts, labels=categories, autopct='%1.1f%%')

        plt.xlabel('Categories', fontsize = 16)
        plt.ylabel('Count', fontsize = 16)
        plt.grid(alpha=0.3)
        plt.legend()
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xticks(rotation=90)
        plt.show()


    def showHeatmap(self, event):
        plt.figure(figsize = (40, 35))
        sns.heatmap(self.data[self.num_columns].corr(), fmt = ".2f", annot = True)
        plt.show()


    def showScatterplot(self, event):
        x = self.cb_2.GetStringSelection()
        y = self.cb_3.GetStringSelection()
        hue = self.cb_4.GetStringSelection()
        plt.figure(figsize=(15, 10))
        sns.scatterplot(data=self.data, x=x, y=y, hue=hue)
        plt.show()


def data_viz(kdd):
    app = wx.App()
    frame = Window('Vizualizácia vstupného datasetu', kdd)
    app.MainLoop()