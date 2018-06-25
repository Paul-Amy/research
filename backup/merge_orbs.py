fout = open("hermustest66.50orb.merge","a+")
for line in open("hermustest66.gen.orbit.0.params"):
  fout.write(line)
for num in range(1,49):
  f = open("hermustest66.gen.orbit." + str(num) + ".params")
  f.next()
  for line in f:
    fout.write(line)
  f.close()
fout.close()