import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# function converts txt file to csv file (longer porecessing time)
def txt_to_csv(txt_name):
	with open(txt_name +'.txt') as f:
		lines = f.readlines()

	output = pd.DataFrame()
	for riadok in lines[20:]:
		hodnota = riadok.split('\t')
		row_dict = {
			'time': float(hodnota[0]),
			'Fx': float(hodnota[1]),
			'Fy': float(hodnota[2]),
			'Fz': float(hodnota[3]),
			'Mx': float(hodnota[4]),
			'My': float(hodnota[5]),
			'Mz': float(hodnota[6]),
		}
		df_dictionary = pd.DataFrame([row_dict])
		output = pd.concat([output, df_dictionary], ignore_index=True)

	output.to_csv(txt_name +'.csv')
	print(output.head())


def plot_graph(dataset, ax_x, ax_y):
	plt.style.use('_mpl-gallery')
	dataset.plot(x=ax_x,y=ax_y)
	plt.show()	

#txt_to_csv('rn45_t3')

hodnoty = pd.read_csv('rn15_t1.csv')
plot_graph(dataset=hodnoty.iloc[1:], ax_x='time', ax_y=['Fx','Fy','Fz'])


