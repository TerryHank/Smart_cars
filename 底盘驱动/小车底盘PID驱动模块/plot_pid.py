import matplotlib.pyplot as plt

class sub_plot_c:
    	
	def __init__(self):
		self.x = 0
		self.x_list = []
		self.y_list = []

		fig = plt.figure(figsize=(12, 12))
		ax = fig.add_subplot()
		plt.ion()

	def update(self, y):
		self.x += 1
		self.x_list.append(self.x)
		self.y_list.append(y)

	def draw_img(self):
		plt.clf()       
		plt.plot(self.x_list, self.y_list, label = "motor_spd")  

		plt.title("motor_spd") 
		plt.xlabel("x axis Time") 
		plt.ylabel("y axis  spd") 

		plt.grid(linestyle='--', c="gray")
		plt.legend(["motor_spd"])

		plt.pause(0.1)        
		plt.ioff()             # 关闭画图的窗口

	def release():
    		plt.show()


    			
    	



