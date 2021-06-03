from DXYdata.models import ProvinceData, CityData, DataAfterPca
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pandas as pd
import pyecharts
from pyecharts.charts import Geo, Map, Timeline, Line, Page, Grid
from pyecharts import options as opts
from pyecharts.globals import GeoType
from pyecharts.components import Table
from sklearn.model_selection import train_test_split
from sklearn import tree
import numpy as np
from sklearn import neighbors, datasets
import pandas as pd
from sklearn.datasets.samples_generator import make_classification
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def homePage(request):
	return render(request, "homePage.html")

def dxyNumAna(request):
	provinceList = ProvinceData.objects.all()
	cityList = CityData.objects.all()
	index = request.GET.get('index')
	if not index:
		index = '1'
	df = pd.DataFrame(list(provinceList.values()))
	df2 = pd.DataFrame(list(cityList.values()))
	if index == '1':
		label = 'province_confirmedCount'
		label2 = 'city_confirmedCount'
	elif index == '2':
		label = 'province_increasedConfirmedCount'
		label2 = 'city_increasedConfirmedCount'
	else :
		label = 'province_currentCount'
		label2 = 'city_currentCount'

	x = df['updateTime'].unique()
	x2 = df2['updateTime'].unique()
	y = df[label]
	y21 = df2[df2['cityName']=='佛山'][label2] #佛山
	y22 = df2[df2['cityName']=='东莞'][label2] #东莞
	y23 = df2[df2['cityName']=='深圳'][label2]  #深圳
	y24 = df2[df2['cityName']=='广州'][label2]  #广州
	line = (
		Line(init_opts=opts.InitOpts(width="50%"))
			.set_global_opts(
			tooltip_opts=opts.TooltipOpts(is_show=False),
			xaxis_opts=opts.AxisOpts(type_="category"),
			yaxis_opts=opts.AxisOpts(
				type_="value",
				axistick_opts=opts.AxisTickOpts(is_show=True),
				splitline_opts=opts.SplitLineOpts(is_show=True),
			),
		)
			.add_xaxis(xaxis_data=x)
			.add_yaxis(
			series_name= "广东省",
			y_axis=y,
			symbol="emptyCircle",
			is_symbol_show=True,
			label_opts=opts.LabelOpts(is_show=False),
		)
	)
	line2 = (
		Line(init_opts=opts.InitOpts(width="50%"))
			.set_global_opts(
			tooltip_opts=opts.TooltipOpts(is_show=False),
			xaxis_opts=opts.AxisOpts(type_="category"),
			yaxis_opts=opts.AxisOpts(
				type_="value",
				axistick_opts=opts.AxisTickOpts(is_show=True),
				splitline_opts=opts.SplitLineOpts(is_show=True),
			),
		)
			.add_xaxis(xaxis_data=x2)
			.add_yaxis(
			series_name="佛山",
			y_axis=y21,
			symbol="emptyCircle",
			is_symbol_show=True,
			label_opts=opts.LabelOpts(is_show=False),
		)
			.add_yaxis(
			series_name="东莞",
			y_axis=y22,
			symbol="emptyCircle",
			is_symbol_show=True,
			label_opts=opts.LabelOpts(is_show=False),
		)
			.add_yaxis(
			series_name="深圳",
			y_axis=y23,
			symbol="emptyCircle",
			is_symbol_show=True,
			label_opts=opts.LabelOpts(is_show=False),
		)
			.add_yaxis(
			series_name="广州",
			y_axis=y24,
			symbol="emptyCircle",
			is_symbol_show=True,
			label_opts=opts.LabelOpts(is_show=False),
		)

	)
	page = Page(layout=Page.SimplePageLayout)
	# 需要自行调整每个 chart 的 height/width，显示效果在不同的显示器上可能不同
	page.add(line,line2)
	return render(request, "dxyNumAna.html", {
		'pic':page.render_embed(),
		'selectIndex':str(index)
	})

def getLevel(df):
	lastIncreaseDate = {'东莞':-14,'深圳':-14,'佛山':-14,'广州':-14} #上次有新确诊的日期
	maxLastIncreaseCount = {'东莞':0,'深圳':0,'佛山':0,'广州':0} #14天内最大日增长数
	i = 0
	df['level'] = 1
	for date in df['updateTime'].unique():
		for city in ['东莞','深圳','佛山','广州']:
			index = df.loc[(df.cityName == city) & (df.updateTime == date)].index.to_list()[0]
			tempRow = df.loc[index]
			if tempRow['city_increasedConfirmedCount'] > 0: #有新确诊 更新上次增长日期和最近最大日增长数
				if i - lastIncreaseDate[city] >=14:  #除今天外，14天内无新增长，直接更新最近最大日增长数
					maxLastIncreaseCount[city] = tempRow['city_increasedConfirmedCount']
				lastIncreaseDate[city] = i
				if tempRow['city_increasedConfirmedCount'] > maxLastIncreaseCount[city]:
					maxLastIncreaseCount[city] = tempRow['city_increasedConfirmedCount']
			if tempRow['city_currentCount'] > 50 and (i - lastIncreaseDate[city] < 14 ) and maxLastIncreaseCount[city]>10:
				df['level'][index] = 3;
			elif tempRow['city_currentCount'] > 50 or (i - lastIncreaseDate[city] < 14 ):
				df['level'][index] = 2;
		i +=1
	return df

def dxyDyMap(request):
	tl = Timeline()
	cityList = CityData.objects.all()
	df = pd.DataFrame(list(cityList.values()))
	df = getLevel(df)
	headers = ['等级','东莞', '深圳', '佛山', '广州']
	rows = [
		["1",0,0,0,0],
		["2",0,0,0,0],
		["3",0,0,0,0]
	]
	table = Table()
	dic = {'东莞':1,'深圳':2,'佛山':3,'广州':4}
	for city in ['东莞', '深圳', '佛山', '广州']:
		count = (df.loc[df.cityName==city]['level'].value_counts())
		try:
			rows[0][dic[city]] = count[1]
		except:
			rows[0][dic[city]] = 0
		try:
			rows[1][dic[city]] = count[2]
		except:
			rows[1][dic[city]] = 0
		try:
			rows[2][dic[city]] = count[3]
		except:
			rows[2][dic[city]] = 0

	table.add(headers, rows)
	df.replace({'东莞': '东莞市', '深圳': '深圳市','佛山':'佛山市','广州':'广州市'}, inplace=True)
	for i in df['updateTime'].unique():
		Date1 = df[df['updateTime'] == (i)]
		province = list(Date1['cityName'])
		num = list(Date1['level'])
		c = (
			Map()
				.add("疫情地图", maptype="广东", data_pair=[list(z) for z in zip(province, num)], is_map_symbol_show=False)
				.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
				.set_global_opts(
				visualmap_opts=opts.VisualMapOpts(max_=3, min_=1),
				title_opts=opts.TitleOpts(title="疫情地图"),
			)
		)
		tl.add(c, (i))

	return render(request, "dxyDyMap.html", {
		'dyMap':tl.render_embed(),
		'table' :table.render_embed()
	})

def classification(request):
    cityList = CityData.objects.all()
    df = pd.DataFrame(list(cityList.values()))
    df = getLevel(df)
    # data_after_pca = DataAfterPca.objects.all()
    # data_after_pca = data_after_pca.values()
    # print("**************************************************")
    # print(data_after_pca)
    row_data=df.copy()
    row_data.drop(['updateTime', 'cityName'], axis=1, inplace=True)

    pca = PCA(n_components=2)
    data_after_pca = pd.DataFrame(pca.fit_transform(row_data))
    data_after_pca.columns = ['pca_1', 'pca_2']
    # print("**************************************************")
    # print(data_after_pca)
    # 留出法划分训练测试集
    labels = df['level']
    X_train, X_test, y_train, y_test = train_test_split(data_after_pca, labels, test_size=0.25, random_state=0,stratify=labels)

    # 决策树
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    predict = clf.predict(X_test)


    color1=ListedColormap(['#FFFF99', '#FFCCCC', '#66CCCC'])
    color2=ListedColormap(['#BFEFFF', '#DDA0DD', '#C1FFC1'])

    plt.figure(figsize=(4,4))
    # plt.axis([-500, 900, -50, 450])
    plt.title('DXYData', fontsize=14)
    plt.scatter(X_test["pca_1"],X_test["pca_2"],c=y_test,cmap=color1)


    buffer = BytesIO()
    plt.savefig(buffer)
    plt.close()
    plot_data = buffer.getvalue()
    imb1 = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims1 = imb1.decode()
    imd1 = "data:image/png;base64," + ims1

    plt.figure(figsize=(4, 4))

    plt.title('classification', fontsize=14)
    plt.scatter(X_test["pca_1"], X_test["pca_2"], c=predict, cmap=color2)

    buffer = BytesIO()
    plt.savefig(buffer)
    plt.close()
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    context = {
        'img': imd1,
        'img1': imd,
    }

    return render(request, 'classification.html', context)



