import matplotlib.pyplot as plt
import pylab as py
import files as fi

data=fi.read_file("50_orbits_vary_data.csv", ",")
data1=fi.read_file("hermustest64.forward.100M.csv.params", ",")
data2=fi.read_file("hermustest64.back.100M.csv.params", ",")
x = data[:,0]
y = data[:,1]
z = data[:,2]
r = data[:,8]
vgsr = data[:,9]
l = data[:,10]
i = 0
for i in range(len(l)):
  if l[i] > 180:
    l[i] = l[i] - 360.0
b = data[:,11]

xorbfor = data1[:,0]
yorbfor = data1[:,1]
zorbfor = data1[:,2]
rorbfor = data1[:,8]
vgsrorbfor = data1[:,9]
lorbfor = data1[:,10]
j = 0 
for j in range(len(lorbfor)):
  if lorbfor[j] > 180:
    lorbfor[j] = lorbfor[j] - 360.0
borbfor = data1[:,11]

xorbback = data2[:,0]
yorbback = data2[:,1]
zorbback = data2[:,2]
rorbback = data2[:,8]
vgsrorbback = data2[:,9]
lorbback = data2[:,10]
k = 0 
for k in range(len(lorbback)):
  if lorbback[k] > 180:
    lorbback[k] = lorbback[k] - 360.0
borbback = data2[:,11]


#plt.scatter(l,b,s=0.1,color='black',marker='.',alpha=0.007)
#plt.axis([100,-50,-90,90])
#plt.xlabel('$l$')
#plt.ylabel('$b$')
#plt.savefig('l-b_plot_02272017.pdf', dpi=600)
#plt.savefig('l-b_plot_02272017.png',dpi=600)
#plt.scatter(lorbfor,borbfor,s=0.1,color='black',marker='.')
#plt.savefig('l-b_plot_02272017.pdf', dpi=600)
#plt.savefig('l-b_plot_02272017.png',dpi=600)
#plt.scatter(lorbback,borbback,s=0.1,color='black',marker='.')
#plt.savefig('l-b_plot_02272017.png',dpi=600)
#plt.savefig('l-b_plot_02272017.pdf', dpi=600)
#plt.clf()

#plt.scatter(l,vgsr,s=0.1,color='black',marker='.',alpha=0.007)
#plt.axis([100,-50,-100,100])
#plt.xlabel('$l$')
#plt.ylabel('$V_{gsr}$')
#plt.savefig('l-vgsr_plot_02272017.png', dpi=600)
#plt.scatter(lorbfor,vgsrorbfor,s=0.1,color='black',marker='.')
#plt.savefig('l-vgsr_plot_02272017.png', dpi=600)
#plt.scatter(lorbback,vgsrorbback,s=0.1,color='black',marker='.')
#plt.savefig('l-vgsr_plot_02272017.png', dpi=600)
#plt.clf()

#plt.scatter(l,r,s=0.1,c='r',marker='.',alpha=0.007)
#plt.axis([100,-50,4,24])
#plt.xlabel('$l$')
#plt.ylabel('$r$ (kpc)')
#plt.savefig('l-r_plot_02272017.pdf', dpi=600)
#plt.scatter(lorbfor,rorbfor,s=0.1,c='r',marker='.')
#plt.savefig('l-r_plot_02272017.pdf', dpi=600)
#plt.scatter(lorbback,rorbback,s=0.1,c='r',marker='.')
#plt.savefig('l-r_plot_02272017.pdf', dpi=600)
#plt.clf()

#plt.scatter(x,y,s=0.1,color='black',marker='.',alpha=0.0055)
#plt.axis([-16,16,-16,16])
#plt.xlabel('$x$')
#plt.ylabel('$y$')
#plt.savefig('x-y_plot_02272017.png', dpi=600)
#plt.scatter(xorbfor,yorbfor,s=0.1,color='black',marker='.')
#plt.savefig('x-y_plot_02272017.png', dpi=600)
#plt.scatter(xorbback,yorbback,s=0.1,color='black',marker='.')
#plt.savefig('x-y_plot_02272017.png', dpi=600)
#plt.clf()

#plt.scatter(x,z,s=0.1,color='black',marker='.',alpha=0.007)
#plt.axis([-16,16,-16,16])
#plt.xlabel('$x$')
#plt.ylabel('$z$')
#plt.savefig('x-z_plot_02272017.png', dpi=600)
#plt.scatter(xorbfor,zorbfor,s=0.1,color='black',marker='.')
#plt.savefig('x-z_plot_02272017.png', dpi=600)
#plt.scatter(xorbback,zorbback,s=0.1,color='black',marker='.')
#plt.savefig('x-z_plot_02272017.png', dpi=600)
#plt.clf()

#plt.scatter(y,z,s=0.1,color='black',marker='.',alpha=0.007)
#plt.axis([-16,16,-16,16])
#plt.xlabel('$y$')
#plt.ylabel('$z$')
#plt.savefig('y-z_plot_02272017.png', dpi=600)
#plt.scatter(yorbfor,zorbfor,s=0.1,color='black',marker='.')
#plt.savefig('y-z_plot_02272017.png', dpi=600)
#plt.scatter(yorbback,zorbback,s=0.1,color='black',marker='.')
#plt.savefig('y-z_plot_02272017.png', dpi=600)
#plt.clf()

plt.subplots_adjust(wspace=0.3, hspace=0.3)	
ax1=py.subplot(221)
ax2=py.subplot(222)
ax3=py.subplot(223)
ax1.scatter(x,z,s=0.1,color='black',marker='.',alpha=0.0055)
ax2.scatter(y,z,s=0.1,color='black',marker='.',alpha=0.005)
ax3.scatter(x,y,s=0.1,color='black',marker='.',alpha=0.005)
ax1.scatter(xorbfor,zorbfor,s=0.1,color='black',marker='.')
ax1.scatter(xorbback,zorbback,s=0.1,color='black',marker='.')
ax2.scatter(yorbfor,zorbfor,s=0.1,color='black',marker='.')
ax2.scatter(yorbback,zorbback,s=0.1,color='black',marker='.')
ax3.scatter(xorbfor,yorbfor,s=0.1,color='black',marker='.')
ax3.scatter(xorbback,yorbback,s=0.1,color='black',marker='.')
ax1.axis([-16,16,-16,16])
ax2.axis([-16,16,-16,16])
ax3.axis([-16,16,-16,16])
ax1.set_ylabel('Z (kpc)', fontsize=16)
ax2.set_ylabel('Z (kpc)', fontsize=16)
ax3.set_ylabel('Y (kpc)', fontsize=16)
ax1.set_xlabel('X (kpc)', fontsize=16)
ax2.set_xlabel('Y (kpc)', fontsize=16)
ax3.set_xlabel('X (kpc)', fontsize=16)

plt.savefig('xyz_trip_plot.png',dpi=600)