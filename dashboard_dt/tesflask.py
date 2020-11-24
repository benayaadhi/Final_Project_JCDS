# Flask : library utama untuk membuat API
# render_template : agar dapat memberikan respon file html
# request : untuk membaca data yang diterima saat request datang
from flask import Flask, render_template, request
# plotly dan plotly.graph_objs : membuat plot
import plotly
import plotly.graph_objs as go
# pandas : untuk membaca csv dan men-generate dataframe
import pandas as pd
import json
from sqlalchemy import create_engine

## Joblib untuk Load Model
import joblib
model = joblib.load('ModelRF')
app = Flask(__name__)

# category plot function
def category_plot(
    cat_plot = 'histplot',
    cat_x = 'Item_Type_New', cat_y = 'Item_Outlet_Sales',
    estimator = 'count', hue = 'Item_Fat_Content'):

    # generate dataframe tips.csv
    tips = pd.read_csv('./static/bigmartclean.csv')



    # jika menu yang dipilih adalah histogram
    if cat_plot == 'histplot':
        # siapkan list kosong untuk menampung konfigurasi hist
        data = []
        # generate config histogram dengan mengatur sumbu x dan sumbu y
        for val in tips[hue].unique():
            hist = go.Histogram(
                x=tips[tips[hue]==val][cat_x],
                y=tips[tips[hue]==val][cat_y],
                histfunc=estimator,
                name=val
            )
            #masukkan ke dalam array
            data.append(hist)
        #tentukan title dari plot yang akan ditampilkan
        title='Histogram'
    elif cat_plot == 'boxplot':
        data = []

        for val in tips[hue].unique():
            box = go.Box(
                x=tips[tips[hue] == val][cat_x], #series
                y=tips[tips[hue] == val][cat_y],
                name = val
            )
            data.append(box)
        title='Box'
    # menyiapkan config layout tempat plot akan ditampilkan
    # menentukan nama sumbu x dan sumbu y
    if cat_plot == 'histplot':
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=estimator),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    else:
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    #simpan config plot dan layout pada dictionary
    result = {'data': data, 'layout': layout}

    #json.dumps akan mengenerate plot dan menyimpan hasilnya pada graphjson
    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# akses halaman menuju route '/' untuk men-test
# apakah API sudah running atau belum
@app.route('/')
def index():

    plot = category_plot()
    # dropdown menu
    # kita lihat pada halaman dashboard terdapat menu dropdown
    # terdapat lima menu dropdown, sehingga kita mengirimkan kelima variable di bawah ini
    # kita mengirimnya dalam bentuk list agar mudah mengolahnya di halaman html menggunakan looping
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('Item_Type_New', 'Item Type'), ('Item_Fat_Content', 'Item Fat Content'), ('Outlet_Type', 'Tipe Outlet'), ('Outlet_Identifier', 'Jenis Outlet')]
    list_y = [('Item_Outlet_Sales', 'Sales'), ('Item_MRP', 'MaxRetailPrice')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('Outlet_Size', 'Size'), ('Item_Fat_Content', 'Fat Content'), ('Outlet_Location_Type', 'Location Type'), ('Outlet_Type', 'Outlet Tipe')]

    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot='histplot',
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x='Item_Type_New',

        # untuk sumbu Y tidak ada, nantinya menu dropdown Y akan di disable
        # karena pada histogram, sumbu Y akan menunjukkan kuantitas data

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator='count',
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue='Item_Fat_Content',
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_est,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue)
@app.route('/cat_fn/<nav>')
def cat_fn(nav):

    # saat klik menu navigasi
    if nav == 'True':
        cat_plot = 'histplot'
        cat_x = 'Item_Type_New'
        cat_y = 'Item_Outlet_Sales'
        estimator = 'count'
        hue = 'Outlet_Size'
    
    # saat memilih value dari form
    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')
        cat_y = request.args.get('cat_y')
        estimator = request.args.get('estimator')
        hue = request.args.get('hue')

    # Dari boxplot ke histogram akan None
    if estimator == None:
        estimator = 'count'
    
    # Saat estimator == 'count', dropdown menu sumbu Y menjadi disabled dan memberikan nilai None
    if cat_y == None:
        cat_y = 'Item_Outlet_Sales'

    # Dropdown menu
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('Item_Type_New', 'Item Type'), ('Item_Fat_Content', 'Item Fat Content'), ('Outlet_Type', 'Tipe Outlet'), ('Outlet_Identifier', 'Jenis Outlet')]
    list_y = [('Item_Outlet_Sales', 'Sales'), ('Item_MRP', 'MaxRetailPrice')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('Outlet_Size', 'Size'), ('Item_Fat_Content', 'Fat Content'), ('Outlet_Location_Type', 'Location Type'), ('Outlet_Type', 'Outlet Tipe')]


    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot=cat_plot,
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x=cat_x,
        focus_y=cat_y,

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator=estimator,
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue=hue,
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_est,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue
    )

##################
## SCATTER PLOT ##
##################

# scatter plot function
def scatter_plot(cat_x, cat_y, hue):


    data = []

    for val in tips[hue].unique():
        scatt = go.Scatter(
            x = tips[tips[hue] == val][cat_x],
            y = tips[tips[hue] == val][cat_y],
            mode = 'markers',
            name = val
        )
        data.append(scatt)

    layout = go.Layout(
        title= 'Scatter',
        title_x= 0.5,
        xaxis=dict(title=cat_x),
        yaxis=dict(title=cat_y)
    )

    result = {"data": data, "layout": layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/scatt_fn')
def scatt_fn():
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    hue = request.args.get('hue')

    # WAJIB! default value ketika scatter pertama kali dipanggil
    if cat_x == None and cat_y == None and hue == None:
        cat_x = 'Total_Item_Sales'
        cat_y = 'Item_Fat_Content'
        hue = 'Item_Type_New'

    # Dropdown menu
    list_x = [('Total_Item_Sales', 'Sales'), ('Item_Fat_Content', 'Fat Content'), ('Outlet_Size', 'Size')]
    list_y = [('Total_Item_Sales', 'Sales'), ('Item_Fat_Content', 'Fat Content'), ('Outlet_Size', 'Size')]
    list_hue = [('Item_Type_New', 'Type'), ('Outlet_Location_Type', 'Location Type'),('Outlet_Size','Size'),('Outlet_Identifier','Jenis Outletx')]

    plot = scatter_plot(cat_x, cat_y, hue)

    return render_template(
        'scatter.html',
        plot=plot,
        focus_x=cat_x,
        focus_y=cat_y,
        focus_hue=hue,
        drop_x= list_x,
        drop_y= list_y,
        drop_hue= list_hue
    )

##############
## PIE PLOT ##
##############

def pie_plot(hue = 'sex'):
    


    vcounts = tips[hue].value_counts()

    labels = []
    values = []

    for item in vcounts.iteritems():
        labels.append(item[0])
        values.append(item[1])
    
    data = [
        go.Pie(
            labels=labels,
            values=values
        )
    ]

    layout = go.Layout(title='Pie', title_x= 0.48)

    result = {'data': data, 'layout': layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/pie_fn')
def pie_fn():
    hue = request.args.get('hue')

    if hue == None:
        hue = 'sex'

    list_hue = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]

    plot = pie_plot(hue)
    return render_template('pie.html', plot=plot, focus_hue=hue, drop_hue= list_hue)

###############
## UPDATE DB ##
###############
### Menampilkan data dari SQL
@app.route('/db_fn')
def db_fn():
    ml=pd.read_csv('bigmartclean.csv')
    tab=ml.head(1000)
    return render_template('predict.html', data=tab.values)


# @app.route('/update_fn', methods=['POST', 'GET'])
# def update_fn():

#     if request.method == 'POST':
#         input = request.form
        
#         sex = ''
#         if input['sex'] == 'male':
#             sex = 'Male'
#         else:
#             sex = 'Female'

#         smoker = ''
#         if input['smoker'] == 'smoker_yes':
#             smoker = 'Yes'
#         else:
#             smoker = 'No'

#         day = ''
#         if input['day'] == 'thur':
#             day = 'Thur'
#         elif input['day'] == 'fri':
#             day = 'Fri'
#         elif input['day'] == 'sat':
#             day = 'Sat'
#         else:
#             day = 'Sun'

#         time = ''
#         if input['time'] == 'lunch':
#             time = 'Lunch'
#         else:
#             time = 'Dinner'
        # ## Memasukkan data ke Tabel SQL
        # new_df = pd.DataFrame({
        #     'total_bill' : [float(input['bill'])],
        #     'tip' : [float(input['tip'])],
        #     'sex' : [sex],
        #     'smoker' : [smoker],
        #     'day' : [day],
        #     'time' : [time],
        #     'size' : [int(input['size'])]
        # })
        # new_df.to_sql('tips', con=dbConnection, if_exists='append', index=False)
        # return render_template('success.html',
        #     total_bill=float(input['bill']),
        #     tip=float(input['tip']),
        #     sex=sex,
        #     smoker=smoker,
        #     day=day,
        #     time=time,
        #     size=int(input['size'])
        #     )


@app.route('/pred_lr')
## Menampilkan Dataset
def pred_lr():
    ml=pd.read_csv('bigmartclean.csv')
    tab=ml.head(1000)
    return render_template('predict.html', data=data.tab.values)

@app.route('/pred_result', methods=['POST', 'GET'])
def pred_result():

    if request.method == 'POST':
    ## Untuk Predict
        input = request.form
        Item_Weight=float(input['Item_Weight'])
        Item_Visibility=float(input['Item_Visibility'])
        Item_MRP=float(input['Item_MRP'])
        Outlet_Establishment_Year = ''
        if input['year'] == '1985':
            Outlet_Establishment_Year = 1985
        elif input['year']=='1987':
            Outlet_Establishment_Year = 1987
        elif input['year']=='1997':
            Outlet_Establishment_Year = 1997
        elif input['year']=='1998':
            Outlet_Establishment_Year = 1998
        elif input['year']=='1999':
            Outlet_Establishment_Year = 1999
        elif input['year']=='2002':
            Outlet_Establishment_Year = 2002
        elif input['year']=='2004':
            Outlet_Establishment_Year = 2004
        elif input['year']=='2007':
            Outlet_Establishment_Year = 2007
        else :
            Outlet_Establishment_Year = 2008

        Item_Fat_Content_0 = ''
        if input['fat'] == 'Low Fat':
            Item_Fat_Content_0 = 1
        else:
            Item_Fat_Content_0 = 0
        Item_Fat_Content_1 =''
        if input['fat']== 'Non-Edible':
            Item_Fat_Content_1 = 1
        else : 
            Item_Fat_Content_1 = 0
        Item_Fat_Content_2 =''
        if input['fat']=='Regular':
            Item_Fat_Content_2 = 1
        else :
            Item_Fat_Content_2 = 0
        

        Outlet_0 = ''
        if input['outlet'] == 'OUT010':
            Outlet_0 = 1
        else :
            Outlet_0 = 0
        Outlet_1 = ''
        if input['outlet'] == 'OUT013':
            Outlet_1 = 1
        else : 
            Outlet_1 = 0
        Outlet_2 = ''
        if input['outlet'] == 'OUT017':
            Outlet_2 = 1
        else : 
            Outlet_2 = 0
        Outlet_3 =''
        if input['outlet'] == 'OUT018':
            Outlet_3 = 1
        else : 
            Outlet_3 = 0
        Outlet_4 =''
        if input['outlet'] == 'OUT019':
            Outlet_4 = 1
        else : 
            Outlet_4 = 0
        Outlet_5 = ''
        if input['outlet'] == 'OUT027':
            Outlet_5 = 1
        else :
            Outlet_5 = 0
        Outlet_6 = ''
        if input['outlet'] == 'OUT035':
            Outlet_6 = 1
        else : 
            Outlet_6 = 0
        Outlet_7 =''
        if input['outlet'] == 'OUT045':
            Outlet_7 = 1
        else :
            Outlet_7 = 0
        Outlet_8 =''
        if input['outlet'] == 'OUT046':
            Outlet_8 = 1
        else : 
            Outlet_8 = 0
        Outlet_9 = ''
        if input['outlet'] =='OUT049':
            Outlet_9 = 1
        else : 
            Outlet_9 = 0

        Outlet_Size_0 = ''
        if input['size'] == 'High':
            Outlet_Size_0 = 1
        else : 
            Outlet_Size_0 = 0
        Outlet_Size_1 =''
        if input['size'] == 'Medium':
            Outlet_Size_1 = 1
        else :
            Outlet_Size_1 = 0
        Outlet_Size_2 = ''
        if input['size'] =='Small':
            Outlet_Size_2 = 1
        else :
            Outlet_Size_2 = 0

        Outlet_Location_Type_0 = ''
        if input['oltype'] == 'Tier 1':
            Outlet_Location_Type_0 = 1
        else : 
            Outlet_Location_Type_0 = 0
        Outlet_Location_Type_1 = ''
        if input['oltype'] == 'Tier 2':
            Outlet_Location_Type_1 = 1
        else : 
            Outlet_Location_Type_1 = 0
        Outlet_Location_Type_2 = ''
        if input['oltype']=='Tier 3':
            Outlet_Location_Type_2 = 1
        else :
            Outlet_Location_Type_2 = 0

        Outlet_Type_0 = ''
        if input['otype'] == 'Grocery Store':
            Outlet_Type_0 = 1
        else : 
            Outlet_Type_0 = 0
        Outlet_Type_1 = ''
        if input['otype'] == 'Supermarket Type1':
            Outlet_Type_1 = 1
        else : 
            Outlet_Type_1 = 0
        Outlet_Type_2 = ''
        if input['otype'] == 'Supermarket Type2':
            Outlet_Type_2 = 1
        else :
            Outlet_Type_2 = 0
        Outlet_Type_3 = ''
        if input['otype'] =='Supermarket Type3':
            Outlet_Type_3 = 1
        else:
            Outlet_Type_3 = 0
        Item_Type_New_0 = ''
        if input['it'] =='non':
            Item_Type_New_0 = 1
        else:
            Item_Type_New_0 = 0
        Item_Type_New_1 = ''
        if input['it'] =='Others':
            Item_Type_New_1 = 1
        else:
            Item_Type_New_1 = 0
        Item_Type_New_2 = ''
        if input['it'] =='perishable':
            Item_Type_New_2 = 1
        else:
            Item_Type_New_2 = 0



        pred = model.predict([[Item_Weight,Item_Visibility, Item_MRP, Outlet_Establishment_Year,Item_Fat_Content_0,Item_Fat_Content_1,Item_Fat_Content_2,Outlet_0,Outlet_1,Outlet_2,Outlet_3,Outlet_4,Outlet_5,Outlet_6,Outlet_7,Outlet_8,Outlet_9,
     Outlet_Size_0,Outlet_Size_1,Outlet_Size_2, Outlet_Location_Type_0,Outlet_Location_Type_1,Outlet_Location_Type_2,Outlet_Type_0,Outlet_Type_1,Outlet_Type_2,Outlet_Type_3,
    Item_Type_New_0, Item_Type_New_1,Item_Type_New_2]])[0].round(2)

        ## Untuk Isi Data
        year_dt = ''
        if input['year'] == '1985':
            year_dt = 1985
        elif input['year']=='1987':
            year_dt = 1987
        elif input['year']=='1997':
            year_dt = 1997
        elif input['year']=='1998':
            year_dt = 1998
        elif input['year']=='1999':
            year_dt = 1999
        elif input['year']=='2002':
            year_dt = 2002
        elif input['year']=='2004':
            year_dt = 2004
        elif input['year']=='2007':
            year_dt = 2007
        else :
            year_dt = 2008

        fat_dt = ''
        if input['fat'] == 'Low Fat':
            fat_dt ='Low Fat'
        elif input['fat']=='Non-Edible':
            fat_dt ='Non-Edible'
        else :
            fat_dt ='Regular'


        outlet_dt = ''
        if input['outlet'] == 'OUT010':
            outlet_dt = 'OUT010'
        if input['outlet'] == 'OUT013':
            outlet_dt = 'OUT013'
        if input['outlet'] == 'OUT017':
            outlet_dt = 'OUT017'
        if input['outlet'] == 'OUT018':
            outlet_dt = 'OUT018'
        if input['outlet'] == 'OUT019':
            outlet_dt ='OUT019'
        if input['outlet'] == 'OUT027':
            outlet_dt ='OUT027'
        if input['outlet'] == 'OUT035':
            outlet_dt ='OUT035'
        if input['outlet'] == 'OUT045':
            outlet_dt ='OUT045'
        if input['outlet'] == 'OUT046':
            outlet_dt ='OUT046'
        else:
            outlet_dt ='OUT049'
        
        outlet_size_dt = ''
        if input['size'] == 'High':
            outlet_size_dt = 'High'
        elif input['size'] == 'Medium':
            outlet_size_dt = 'Medium'
        else :
            outlet_size_dt ='Small'
    
        outlet_loc_dt = ''
        if input['oltype'] == 'Tier 1':
            outlet_loc_dt = 'Tier 1'
        elif input['oltype'] == 'Tier 2':
            outlet_loc_dt = 'Tier 2'
        else : 
            outlet_loc_dt = 'Tier 3'

        outlet_type_dt =''
        if input['otype'] == 'Grocery Store':
            outlet_type_dt ='Grocery Store'
        elif input['otype'] == 'Supermarket Type1':
            outlet_type_dt = 'Supermarket Type1'
        elif input['otype'] == 'Supermarket Type2':
            outlet_type_dt = 'Supermarket Type2'
        else : 
            outlet_type_dt = 'Supermarket Type3'

        item_type_dt = ''
        if input['it'] =='non':
            item_type_dt = 'non'
        elif input['it'] =='Others':
            item_type_dt = 'Others'
        else : 
            item_type_dt = 'perishable'



        return render_template('result.html',
            Item_Weight=float(input['Item_Weight']),
            Item_Visibility=float(input['Item_Visibility']),
            Item_MRP=float(input['Item_MRP']),
            year = year_dt,
            fat=fat_dt,
            outlet=outlet_dt,
            size=outlet_size_dt,
            oltype=outlet_loc_dt,
            otype=outlet_type_dt,
            it = item_type_dt,
            BigMart_pred = pred
            )

if __name__ == '__main__':
    ## Me-Load data dari Database
    # sqlengine = create_engine('mysql+pymysql://kal:s3cret123@127.0.0.1/flaskapp', pool_recycle=3605)
    # dbConnection = sqlengine.connect()
    # engine = sqlengine.raw_connection()
    # cursor = engine.cursor()
    # tips = pd.read_sql("select * from tips", dbConnection)
    ## Load Model

    app.run(debug=True)
# ada dua kondisi di mana kita akan melakukan request terhadap route ini
# pertama saat klik menu tab (Histogram & Box)
# kedua saat mengirim form (saat merubah salah satu dropdown) 
# @app.route('/heart')
# def heart():
#     return render_template('heart.html')

# @app.route('/hasil',methods=['POST'])
# def hasil():
#     if request.method == 'POST':
#         input = request.form
#         sl = (input['sl'])
#         sw = (input['Kelamin'])
#         pl = (input['CP'])
#         pw = (input['pw'])
#         ch = (input['chol'])
#         fbs = input(['fbs'])
#         rest = input['rest']

#         pred = model.predict([[sl,sw,pl,pw,ch,fbs,rest]])[0]
        
#     return render_template('hasil.html',data = input,prediksi = pred)



# if __name__ =='__main__':
#     model = joblib.load("modelLinReg")
#     app.run(debug=True)