import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from io import StringIO

# Original software by P. Chris Pistorius
# This version modified March 26, 2016 by Mauro Elias Ferreira and January 10, 2017 by Chris Pistorius
# Modified August 19, 2014 to include adjustable aspect ratio; input widgets on grid layout
# Modified August 21, 2014 to include option of 50% liquid boundaries (chosen with radio button)
# Modified March 8, 2016 to include the S-Ca-Al 50% liquid line with 5% MgO
#                           include global variables 'maxcount', 'totalcount', 'maxarea' and 'area fraction' to create plot legend
#                           include plot legend
# Modified March 25, 2016 to include number of inclusions, analyzed area, and number density in legend
# Modified July 22, 2016 to include Area Fraction and some minor aesthetics improvements
# Modified January 10, 2017 - position of legends changed
# Minor modification November 11, 2025 - updated to be compatible with Python 3.1x
#
# Set up class for input
class Application(Frame):
    def read_name(self):
        name = self.text_entry.get('1.0','1.end')
        return name

    def read_scanarea(self):
        scanarea = self.text_entry.get('2.0','2.end')
        return scanarea
    
    def read_elements(self):
        elements_string = self.text_entry.get('3.0','3.end')
        return elements_string

    def read_text(self):
        thetext = self.text_entry.get('4.0','end')
        return thetext

    def read_aspect(self):
        aspect_input = self.aspect_read.get()
        return aspect_input

    def read_button(self):
        selected = self.buttonvar.get()
        return selected

    def createWidgets(self):
        self.left_frame = Frame(self,width=300)
        self.right_frame = Frame(self,width=300)
        self.left_frame.grid (column=0,row=0)
        self.right_frame.grid (column=1,row=0)

        # Data entry box
        self.text_entry = Text(self.right_frame,width=60,font='Courier 10')
        self.text_entry.pack(side="top", fill="both", expand=True)

        # Button to exit data entry and plot distributions
        self.QUIT = Button(self.right_frame, text='Plot', command = self.quit, fg='red', font='Helvetica 12')
        self.QUIT.pack(side="top", expand=False)

        self.info_frame = Frame(self.left_frame,width=300)
        self.info_frame.pack(side="top",fill="both", expand=True)
        # Info label
        self.info_label = Message(self.info_frame,text = 'Paste data into box at right. \nPut sample ID in first row, ' 
                        '\nanalyzed area in mm'+chr(178)+' in the second row, '
                        '\nelement symbols in third row, \nand data from fourth row. '
                        '\nThen click the Plot button.'
                        '\n\n(The data should be in four columns separated by spaces or tabs:'
                        '\nThe three element fractions, and inclusion area in '+chr(181)+'m'+chr(178)+')',
                justify = LEFT, font='Helvetica 12', width=500)
        self.info_label.pack(side="top", fill="both", expand=True)

        self.liquid_frame = Frame(self.left_frame,width=300,bd=3,relief='ridge')
        self.liquid_frame.pack(side="top",fill="x", expand=True,pady=30)
        # Selection of 50% liquid border
        self.button_label = Message(self.liquid_frame,text = '50% liquid boundary to be drawn: '
        '\nIf used, compositions must be in mole fractions,'
        'and elements in order Mg-Al-Ca or S-Al-Ca',
        font ='Helvetica 12', justify = LEFT, width=400)
        self.buttonvar = IntVar()
        self.buttonvar.set(1)
        self.radio1 = Radiobutton(self.liquid_frame, text="None", variable=self.buttonvar, value=1, font ='Helvetica 10',relief='ridge', bd=2)
        self.radio2 = Radiobutton(self.liquid_frame, text="Mg-Al-Ca", variable=self.buttonvar, value=2, font ='Helvetica 10',relief='ridge', bd=2)
        self.radio3 = Radiobutton(self.liquid_frame, text="S-Al-Ca", variable=self.buttonvar, value=3, font ='Helvetica 10',relief='ridge', bd=2)
        self.radio4 = Radiobutton(self.liquid_frame, text="S-Al-Ca w/ 5% MgO", variable=self.buttonvar, value=4, font ='Helvetica 10',relief='ridge', bd=2)
        self.button_label.grid(column=0, row=0, rowspan=3,sticky=(W), padx=5)
        self.radio1.grid(column=1,row=0, sticky=(W))
        self.radio2.grid(column=1,row=1, sticky=(W))
        self.radio3.grid(column=1,row=2, sticky=(W))
        self.radio4.grid(column=1,row=3, sticky=(W))
        self.liquid_frame.columnconfigure(0,weight=2)
        self.liquid_frame.columnconfigure(1,weight=1)

        # Aspect ratio adjustment
        self.aspect_frame = Frame(self.left_frame,width=400)
        self.aspect_frame.pack(side="top",fill="x", expand=True)
        self.aspect_entry_label = Label(self.aspect_frame,text = 'Aspect ratio factor (h/w):', font='Helvetica 12')
        self.aspect_read = StringVar()
        self.aspect_read.set("1.00")
        self.aspect_entry = Entry(self.aspect_frame, textvariable = self.aspect_read, font='Courier 12',width=4)
        self.aspect_entry_label.grid(column=0, row=0, padx=5, sticky=E)
        self.aspect_entry.grid(column=1, row=0, sticky=W, padx=5)
        self.aspect_frame.columnconfigure(0,weight=4)
        self.aspect_frame.columnconfigure(1,weight=1)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()


# Function definitions
def fifty_border(border_id):
    if border_id==1: #No border
        border=np.array([[None,None]])
    else:
        if border_id==2:    #Mg-Al-Ca
            border=np.array([[0.365032404,0.000677813],[0.35563025,0.00808425],[0.347267506,0.013063513],
            [0.34134393, 0.015498229],[0.333019505,0.017095228],[0.328084781,0.016872357],
            [0.322164202,0.015266216],[0.255497535,0.015266216],[0.253065314,0.019813228],
            [0.252456616,0.020940935],[0.249759712,0.025845845],[0.232702212,0.191730845],
            [0.238152986,0.19452243], [0.248515347,0.200822099],[0.25746506,0.208121414],
            [0.268907602,0.222475978],[0.27232843, 0.229035318],[0.27547624,0.237240398],
            [0.278143498,0.248161274],[0.444802793,0.580420139],[0.45359720,0.574607743],
            [0.462724434,0.56892917], [0.4753947,  0.56140431], [0.489318785,0.553277609],
            [0.498001526,0.548148194],[0.511992018,0.53963882], [0.74948106,0.058342621],
            [0.753643575,0.046977885],[0.758559568,0.033484911],[0.762792159,0.02180387],
            [0.766884035,0.010403411],[0.769960001,0.001772978]])
            border[:,0]=1.0-border[:,0] #reverse, because coordinates given above are for Mg-Ca-Al, not Mg-Al-Ca

        else:
                    if border_id==3:    #Ca-Al-S
                            border=np.array([[0.2285248,0.001213213],[0.226548781,0.004535424],[0.223273286,0.011189832],
                            [0.221426973,0.015367361],[0.219320712,0.020405509],[0.215903388,0.029075314],
                            [0.213958022,0.034243121],[0.211595805,0.040721085],[0.302825602,0.351680634],
                            [0.304920635,0.350844053],[0.310331779,0.348979614],[0.317080755,0.347129888],
                            [0.326813852,0.345108199],[0.340377852,0.343110784],[0.350771607,0.342017799],
                            [0.360413547,0.341260778],[0.366314889,0.340903448],[0.368094261,0.340810739],
                            [0.631001359,0.016730337],[0.631200659,0.015771308],[0.631668719,0.013666008],
                            [0.632173773,0.011487258],[0.63302285,0.007865833], [0.63417212,0.00208874],
                            [0.634263352,0.000467697]])

                    else:   #Ca-Al-S w/ 5%MgO
                            border=np.array([[0.233713485,0],[0.224403093,0.018399968],[0.220820137,0.027442363],
                            [0.217440358,0.036378768],[0.227124827,0.086481716],[0.248012014,0.159271635],
                            [0.265793104,0.221388114],[0.281286131,0.274994219],[0.288312902,0.299129784],
                            [0.294890391,0.321718794],[0.302064568,0.342702564],[0.301396173,0.343798013],
                            [0.304486221,0.350340043],[0.312390686,0.358497184],[0.322781529,0.35720758],
                            [0.342769667,0.353279007],[0.362653133,0.351255223],[0.381415509,0.34633915],
                            [0.399040939,0.336554739],[0.442184014,0.306208165],[0.444742374,0.303817769],
                            [0.451939801,0.29208683],[0.51000036,0.238399942],[0.572466654,0.1822383],
                            [0.63524313,0.124068806],[0.666280382,0.094144914],[0.68638496,0.075785483],
                            [0.711699038,0.05102182],[0.739405007,0.025726428],[0.750527145,0.012947905],[0.758453234,0]])

    return (border)



def draw_frame(width, resolution, line_width, labelA, labelB, labelC, ID, aspect_ratio): # width in inches, resolution in dpi, line_width in pixels
    "Procedure that draws frame for ternary diagram"
    global fig, axes, axes2
    frame=np.array([[0,0],[1,0],[0.5,1],[0,0]], dtype = float)  # coordinates of ternary frame
    grid_coord=np.array([[0.25,0],[0.125,0.25],[0.875,0.25],[0.75,0],[0.375,0.75],[0.625,0.75],
            [0.25,0],[0.5,0],[0.25,0.5],[0.75,0.5],[0.5,0]])
    width=width*1.1/0.8
    height=width*(3.0**0.5)/4*aspect_ratio # height is 0.866 times width, for equilateral triangle
    fig = plt.figure(figsize=(width,height), dpi=resolution, facecolor='white') #set image area to achieve correct aspect ratio
    
    # set up axes for left hand plot
    axes = fig.add_axes([0.05, 0.05, 0.4, 0.8]) # left, bottom, width, height (range 0 to 1)
    axes.set_ylim([-0.05,1.05])
    axes.set_xlim([-0.05,1.05])
    axes.axis('off')
    axes.plot(frame[:,0],frame[:,1],color='black', linewidth=line_width) # draw frame of ternary plot
    axes.plot(grid_coord[:,0],grid_coord[:,1],color='black', linewidth=line_width*0.75, linestyle=':') # draw grid of ternary plot
    axes.text(0.5,1.02,labelA,ha='center',va='bottom') # Label the corners
    axes.text(1.01,-0.02,labelB,ha='center',va='top')
    axes.text(-0.01,-0.02,labelC,ha='center',va='top')
    ID_label = ID+'\nNumber-based distribution'
    axes.text(-0.05,0.92,ID_label,ha='left',va='bottom',fontsize=8) # Label plot with sample ID
    
    # set up axes for right hand plot
    axes2 = fig.add_axes([0.48, 0.05, 0.4, 0.8]) # left, bottom, width, height (range 0 to 1)
    axes2.set_ylim([-0.05,1.05])
    axes2.set_xlim([-0.05,1.05])
    axes2.axis('off')
    axes2.plot(frame[:,0],frame[:,1],color='black', linewidth=line_width) # draw frame of ternary plot
    axes2.plot(grid_coord[:,0],grid_coord[:,1],color='black', linewidth=line_width*0.75, linestyle=':') # draw grid of ternary plot
    axes2.text(0.5,1.02,labelA,ha='center',va='bottom') # Label the corners
    axes2.text(1.01,-0.02,labelB,ha='center',va='top')
    axes2.text(-0.01,-0.02,labelC,ha='center',va='top')
    ID_label = ID+'\nArea-based distribution'
    axes2.text(-0.05,0.92,ID_label,ha='left',va='bottom',fontsize=8) # Label plot with sample ID
    return
#
def find_indices(divisions,x,y):
    "Procedure to locate composition point in composition triangle"
    x_size=1.0/divisions
    y_size=1.0/divisions
    if abs(1-y)<y_size:
        tri_x=0
        tri_y=(2*divisions-2)
    else:   
        offset=-1 if (1.0*int((x-y/2.0)/x_size)==((x-y/2.0)/x_size)) and ((x-y/2.0)/x_size > 0) else 0
        tri_x = int((x-y/2.0)/x_size) + offset  # calculate x index of composition triangle
        x_edge = x_size*(1.0+tri_x+0.5*int(y/y_size))
        tri_y = 2*int(y/y_size) + \
            (x > (x_edge - 0.5*(y-y_size*( int(y/y_size) ) ) ) ) # y index of triangle
    return [tri_x,tri_y]
#
def count_inclusions(divisions,x,y,areas):
    "Procedure that counts inclusions and returns array of counts"
    global maxcount, percentage, totalcount, maxarea, area_fraction, total_af
    counted = np.zeros(shape=(2*divisions-1,divisions),dtype=float) # set initial counts to zero
    areacounted = np.zeros(shape=(2*divisions-1,divisions),dtype=float) # set initial area counts to zero
    for i in range(len(x)):    # Iterate over the total set of inclusion compositons
        if x[i] != None:    # ...except invalid compositions, as flagged when these were read
            tri_xy = find_indices(divisions,x[i],y[i])
            counted[tri_xy[1],tri_xy[0]] += 1
            areacounted[tri_xy[1],tri_xy[0]] += areas[i]
    maxcount=np.max(counted)
    percentage = maxcount/np.sum(counted)*100
    totalcount=np.sum(counted)
    maxarea=np.max(areacounted)
    area_fraction=maxarea/np.sum(areacounted)*100
    total_af=np.sum(areacounted)/float(scanned_area)
    counted=((counted/maxcount)**0.57) * 1.0/divisions  # note exponent 0.57 rather than 0.5
    areacounted=((areacounted/maxarea)**0.57) * 1.0/divisions  # note exponent 0.57 rather than 0.5
    return ([counted,areacounted])

#
def make_triangles(divisions,scale):
    "Function that creates polygons to plot proportional symbols"
    y_divisions=2*divisions-1
    el_width=1.0/divisions
    polytri = np.empty(shape=(0, 2),dtype=float)  # initialize array of polygon coordinates
    for j in range(y_divisions): # iterate over y dimension (rows)
        imax = divisions - j//2 - j%2 # maximum x index for this y row
        x_start = ((j+1)//2 + 1) * el_width/2  # center of first triangle in x direction
        y = (3*(j//2) + 1 + j%2) * el_width/3   # center of triangles in y direction
        y_sign = 1.0*((j%2)*2-1) # controls whether triangle points up or down
        for i in range(imax):
            x=x_start + el_width*i
            polytri=np.append(polytri,[[x-scale[j,i]/2,y+y_sign*scale[j,i]/3],
                    [x+scale[j,i]/2,y+y_sign*scale[j,i]/3], 
                    [x,y-y_sign*scale[j,i]*2/3],
                    [None, None]],axis=0)
    # Add triangle for legend, centered on x=-0.02; y=0.78
    polytri=np.append(polytri,[[-0.02-0.5*el_width,0.78-el_width/3],
            [-0.02+0.5*el_width,0.78-el_width/3], 
            [-0.02,0.78+el_width*2/3],
            [None, None]],axis=0)
    return (polytri)

#Main program
divisions=20  # number of divisions along each of the composition axes
# Set up data input window
root = Tk() 
root.title('Data input')
app = Application(master=root) # Open data entry window
app.mainloop() # Wait for data entry
sample_id = app.read_name() # Read sample ID from first line
scanned_area = float(app.read_scanarea())# Read scanned area from second line
elements = StringIO(app.read_elements()) # Read column headers from third line
A,B,C = np.genfromtxt(elements, usecols=(0, 1, 2), dtype = str, unpack=True) # Read element labels
text_in = StringIO(app.read_text())  # Read entered text containing values to be plotted, from fourth line
a_data,b_data,c_data,area_data = np.genfromtxt(text_in, usecols=(0, 1, 2, 3), unpack=True) #...and convert to arrays
# Test that all compositions are non-negative and convert to x-y coordinates
x_data=[(b_data[i]+a_data[i]/2.0) if ((a_data[i]>=0) and (b_data[i]>=0) and (c_data[i]>=0)) else None for i in range(len(a_data))]
y_data=[a_data[i] if ((a_data[i]>=0) and (b_data[i]>=0) and (c_data[i]>=0)) else None for i in range(len(a_data))]
asp_ratio = float(app.read_aspect())
boundary = app.read_button()   # read in which 50% liquid boundary to draw
get_border=fifty_border(boundary)  # ...and retrieve the coordinates of the appropriate boundary

# Close data entry window
root.destroy() 

# now count the inclusions and calculate linear dimensions of the symbols
counts=count_inclusions(divisions,x_data,y_data,area_data)  # item 0 in counts is number distribution, item 1 area distribution
count_triangles=make_triangles(divisions,counts[0]) # convert symbol sizes to polygons: number count
area_triangles=make_triangles(divisions,counts[1]) # convert symbol sizes to polygons: areas
draw_frame(6.0,200,0.5, A, B, C, sample_id,asp_ratio) # set up figure and axes
axes.fill(count_triangles[:,0],count_triangles[:,1],facecolor='k',edgecolor='none') #draw polygons of proportional symbols - number count
axes2.fill(area_triangles[:,0],area_triangles[:,1],facecolor='k',edgecolor='none') #draw polygons of proportional symbols - area count
axes.plot(get_border[:,0],get_border[:,1],color='grey', linewidth=0.5) # draw 50% liquid boundary
axes2.plot(get_border[:,0],get_border[:,1],color='grey', linewidth=0.5) # draw 50% liquid boundary

axes.text(-0.05,0.915,str(round(totalcount/scanned_area,1))+' inclusions/mm'+chr(178)+'\n'+str(int(totalcount))+' inclusions',
          ha='left',va='top',fontsize=8) # Show inclusion number density (i.e. inclusions/scanned area) and total number of inclusions
axes2.text(-0.05,0.915,str(int(total_af))+' ppm area fraction'+'\n'+str(int(totalcount))+' inclusions',
           ha='left',va='top',fontsize=8) # Show inclusion area fraction and total number of inclusions

axes.text(-0.04+1.0/divisions,0.78,str(int(percentage))+'%',ha='left',va='center',fontsize=8) # Number percentage of largest triangle
axes2.text(-0.04+1.0/divisions,0.78, str(int(area_fraction))+'%',ha='left',va='center',fontsize=8) # Area percentage of largest triangle

plt.show()     # Show plot
