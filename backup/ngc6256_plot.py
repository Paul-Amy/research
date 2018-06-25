import matplotlib.pyplot as plt
import pylab as py
import files as fi

ngc_forward = fi.read_file("ngc6256.forward.250M.csv.params", ",")
ngc_back = fi.read_file("ngc6256.back.250M.csv.params", ",")
herm_forward = fi.read_file("hermustest64.forward.250M.csv.params",",")
herm_back = fi.read_file("hermustest64.back.250M.csv.params",",")

ngc_for_l = ngc_forward[:,10]
ngc_back_l = ngc_back[:,10]
herm_for_l = herm_forward[:,10]
herm_back_l = herm_back[:,10]

ngc_for_rgal = ngc_forward[:,6]
ngc_back_rgal = ngc_back[:,6]
herm_for_rgal = herm_forward[:,6]
herm_back_rgal = herm_back[:,6]

i=0
j=0
k=0
l=0

for i in range(len(ngc_for_l)):
  if ngc_for_l[i] > 180:
    ngc_for_l[i] = ngc_for_l[i] - 360.0

for j in range(len(ngc_back_l)):
  if ngc_back_l[j] > 180:
    ngc_back_l[j] = ngc_back_l[j] - 360.0
    
for k in range(len(herm_back_l)):
  if herm_back_l[k] > 180:
    herm_back_l[k] = herm_back_l[k] - 360.0

for l in range(len(herm_for_l)):
  if herm_for_l[l] > 180:
    herm_for_l[l] = herm_for_l[l] - 360.0

plt.plot(ngc_for_l,ngc_for_rgal,color='blue',linewidth=1.0)
plt.plot(herm_for_l,herm_for_rgal,color='black',linewidth=3.0)
plt.plot(herm_back_l,herm_back_rgal,color='black',linestyle='--',linewidth=3.0)
plt.plot(ngc_back_l,ngc_back_rgal,color='blue',linestyle='--',linewidth=1.0)
plt.axis([-50,100,0,18])
plt.xlabel('$l$')
plt.ylabel('$r_{gal}$ (kpc)')
plt.savefig('l-rgal_plot_02242017.pdf', format='pdf', dpi=600)
plt.savefig('l-rgal_plot_02242017.eps', format='eps')
plt.show()
