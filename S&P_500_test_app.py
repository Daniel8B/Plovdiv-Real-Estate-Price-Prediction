{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyM/TNw3jgR2uYwl75ZTJ+/l",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Daniel8B/Plovdiv-Real-Estate-Price-Prediction/blob/main/S%26P_500_test_app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "tp619hUw9OBC"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import base64\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "import numpy as np\n",
        "import yfinance as yf\n",
        "\n",
        "st.title('S&P 500 App')\n",
        "\n",
        "st.markdown(\"\"\"\n",
        "This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!\n",
        "* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn\n",
        "* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).\n",
        "\"\"\")\n",
        "\n",
        "st.sidebar.header('User Input Features')\n",
        "\n",
        "# Web scraping of S&P 500 data\n",
        "#\n",
        "@st.cache\n",
        "def load_data():\n",
        "    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'\n",
        "    html = pd.read_html(url, header = 0)\n",
        "    df = html[0]\n",
        "    return df\n",
        "\n",
        "df = load_data()\n",
        "sector = df.groupby('GICS Sector')\n",
        "\n",
        "# Sidebar - Sector selection\n",
        "sorted_sector_unique = sorted( df['GICS Sector'].unique() )\n",
        "selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)\n",
        "\n",
        "# Filtering data\n",
        "df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]\n",
        "\n",
        "st.header('Display Companies in Selected Sector')\n",
        "st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')\n",
        "st.dataframe(df_selected_sector)\n",
        "\n",
        "# Download S&P500 data\n",
        "# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806\n",
        "def filedownload(df):\n",
        "    csv = df.to_csv(index=False)\n",
        "    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions\n",
        "    href = f'<a href=\"data:file/csv;base64,{b64}\" download=\"SP500.csv\">Download CSV File</a>'\n",
        "    return href\n",
        "\n",
        "st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)\n",
        "\n",
        "# https://pypi.org/project/yfinance/\n",
        "\n",
        "data = yf.download(\n",
        "        tickers = list(df_selected_sector[:10].Symbol),\n",
        "        period = \"ytd\",\n",
        "        interval = \"1d\",\n",
        "        group_by = 'ticker',\n",
        "        auto_adjust = True,\n",
        "        prepost = True,\n",
        "        threads = True,\n",
        "        proxy = None\n",
        "    )\n",
        "\n",
        "# Plot Closing Price of Query Symbol\n",
        "def price_plot(symbol):\n",
        "  df = pd.DataFrame(data[symbol].Close)\n",
        "  df['Date'] = df.index\n",
        "  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)\n",
        "  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)\n",
        "  plt.xticks(rotation=90)\n",
        "  plt.title(symbol, fontweight='bold')\n",
        "  plt.xlabel('Date', fontweight='bold')\n",
        "  plt.ylabel('Closing Price', fontweight='bold')\n",
        "  return st.pyplot()\n",
        "\n",
        "num_company = st.sidebar.slider('Number of Companies', 1, 5)\n",
        "\n",
        "if st.button('Show Plots'):\n",
        "    st.header('Stock Closing Price')\n",
        "    for i in list(df_selected_sector.Symbol)[:num_company]:\n",
        "        price_plot(i)"
      ]
    }
  ]
}