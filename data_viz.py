from turtle import xcor
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
        super().__init__(parent=None, title=title, size=(900,600))
        self.panel = wx.Panel(self)
        self.data = data
        self.cat_graph_type = 'Bar chart'
        self.num_graph_type = 'Histogram'

        cat_columns =  ['protocol_type', 'service', 'flag', 'label']

        self.num_columns = ["duration","src_bytes","dst_bytes","wrong_fragment","urgent","hot","num_failed_logins","num_compromised","num_root","num_file_creations",
            "num_shells","num_access_files","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
            "srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate"]

        self.bin_columns = ['land', 'logged_in', 'root_shell', 'su_attempted', 'is_host_login', 'is_guest_login']

        # categorical data
        lbl = wx.StaticText(self.panel, -1 , pos=(10, 15), style = wx.ALIGN_CENTER)
        lbl.SetLabel('Visualization of categorical atributes')
        rb_1 = wx.RadioButton(self.panel, label='Bar chart', pos=(180, 40), style=wx.RB_GROUP)
        rb_2 = wx.RadioButton(self.panel, label='Pie chart', pos=(250, 40))
        self.panel.Bind(wx.EVT_RADIOBUTTON, self.onClick)
        self.cb_1 = wx.ComboBox(self.panel, value=cat_columns[0], choices=cat_columns, pos=(10,40), size=(150,45), style=wx.CB_READONLY)
        b_1 = wx.Button(self.panel, label='Show graph', pos=(320, 40))
        b_1.Bind(wx.EVT_BUTTON, self.onSubmit)
        

        # heatmap
        lbl5 = wx.StaticText(self.panel, -1 , pos=(10, 80), style = wx.ALIGN_CENTER)
        lbl5.SetLabel('Heatmap of continuous atributes')
        b_2 = wx.Button(self.panel, label='Show heatmap', pos=(10, 100))
        b_2.Bind(wx.EVT_BUTTON, self.showHeatmap)


        # numerical data (histograms & boxplots)
        lbl5 = wx.StaticText(self.panel, -1 , pos=(10, 140), style = wx.ALIGN_CENTER)
        lbl5.SetLabel('Visualization of continuous atributes')
        self.cb_5 = wx.ComboBox(self.panel, value=self.num_columns[0], choices=self.num_columns, pos=(10,160), size=(180,45), style=wx.CB_READONLY)
        rb_3 = wx.RadioButton(self.panel, label='Histogram', pos=(210, 160), style=wx.RB_GROUP)
        rb_3 = wx.RadioButton(self.panel, label='Boxplot', pos=(300, 160))
        self.panel.Bind(wx.EVT_RADIOBUTTON, self.onClick)
        b_4 = wx.Button(self.panel, label='Show graph', pos=(365, 160))
        b_4.Bind(wx.EVT_BUTTON, self.showNumAtribViz)


        # numerical data (scatterplots)
        lbl1 = wx.StaticText(self.panel, -1 , pos=(10, 200), style = wx.ALIGN_CENTER)
        lbl1.SetLabel('Scatterplots')
        lbl2 = wx.StaticText(self.panel, -1 , pos=(10, 222), style = wx.ALIGN_CENTER)
        lbl2.SetLabel('X:')
        lbl3 = wx.StaticText(self.panel, -1 , pos=(220, 222), style = wx.ALIGN_CENTER)
        lbl3.SetLabel('Y:')
        lbl4 = wx.StaticText(self.panel, -1 , pos=(430, 222), style = wx.ALIGN_CENTER)
        lbl4.SetLabel('Hue:')
        self.cb_2 = wx.ComboBox(self.panel, value=self.num_columns[0], choices=self.num_columns, pos=(30,220), size=(180,45), style=wx.CB_READONLY)
        self.cb_3 = wx.ComboBox(self.panel, value=self.num_columns[0], choices=self.num_columns, pos=(240,220), size=(180,45), style=wx.CB_READONLY)
        self.cb_4 = wx.ComboBox(self.panel, value=self.bin_columns[0], choices=self.bin_columns, pos=(460,220), size=(120,45), style=wx.CB_READONLY)
        b_3 = wx.Button(self.panel, label='Show graph', pos=(600, 220))
        b_3.Bind(wx.EVT_BUTTON, self.showScatterplot)

        self.Show()


    # choose selected visualization type (from radio button)
    def onClick(self, event):
        rb = event.GetEventObject()
        self.cat_graph_type = rb.GetLabel()
        self.num_graph_type = rb.GetLabel()


    # create visualization of categorical atributes
    def onSubmit(self, event):
        selected = self.cb_1.GetStringSelection()
        plt.figure(figsize = (18, 9))
        categories = self.data[selected].value_counts().index
        counts = self.data[selected].value_counts().values
        
        if self.cat_graph_type == 'Bar chart':
            plt.bar(categories, counts, width=0.25)
            plt.xlabel('Categories', fontsize = 16)
            plt.ylabel('Count', fontsize = 16)
        else:
            plt.pie(counts, labels=categories, autopct='%1.1f%%')

        plt.grid(alpha=0.3)
        plt.legend()
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.xticks(rotation=90)
        plt.show()


    # show heatmap of every numerical atributes
    def showHeatmap(self, event):
        #self.figure = Figure(figsize = (40, 35))
        plt.figure(figsize = (40, 35))
        sns.heatmap(self.data[self.num_columns].corr(), fmt = ".2f", annot = True)
        plt.show()


    # show scatterplot of selected atributes (with hue)
    def showScatterplot(self, event):
        x = self.cb_2.GetStringSelection()
        y = self.cb_3.GetStringSelection()
        hue = self.cb_4.GetStringSelection()
        plt.figure(figsize=(15, 10))
        sns.scatterplot(data=self.data, x=x, y=y, hue=hue)
        plt.show()


    # create visualization of numerical atributes
    def showNumAtribViz(self, event):
        x = self.cb_5.GetStringSelection()
        plt.figure(figsize=(15, 10))
        transform_f = lambda x : np.log(x + 1)

        if self.num_graph_type == 'Histogram':
            a = sns.histplot(x=transform_f(self.data[x]), data=self.data)
            a.set_ylabel('count',fontsize=15)
        else:
            a = sns.boxplot(x=transform_f(self.data[x]))
        a.set_xlabel(x,fontsize=15)
        plt.show()


# create window with existing visualization menu
def data_viz(kdd):
    app = wx.App()
    frame = Window('Vizualizácia vstupného datasetu', kdd)
    app.MainLoop()