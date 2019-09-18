
# Importing the matplotlb.pyplot 
import matplotlib.pyplot as plt 
  
# Declaring a figure "gnt" 
fig, gnt = plt.subplots(1,1) 
  
# Setting Y-axis limits 
gnt.set_ylim(0, 50) 
  
# Setting X-axis limits 
gnt.set_xlim(0, 160) 
  
# Setting labels for x-axis and y-axis 
gnt.set_xlabel('seconds since start') 
gnt.set_ylabel('Processor') 
  
# Setting ticks on y-axis 
gnt.set_yticks(range(0, 55, 5)) 
# Labelling tickes of y-axis 
#gnt.set_yticklabels(['1', '2', '3']) 
  
# Setting graph attribute 
gnt.grid(True) 
  
# Declaring a bar in schedule
#gnt.broken_barh([(start_time, duration)],
#                 (lower_yaxis, hieght),
#                 facecolors=('tab:colours'))
gnt.broken_barh([(40, 50)], (21.5, 2), facecolors =('tab:orange')) 
  
# Declaring multiple bars in at same level and same width 
gnt.broken_barh([(110, 10), (150, 10)], (6.5, 2), 
                         facecolors ='tab:blue') 
  
gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (11.5, 2), 
                                  facecolors =('tab:red')) 
  
#plt.savefig("gantt1.png") 
plt.show()

