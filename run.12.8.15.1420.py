execfile('/home/rumbaugh/git/CDCranking/CDCranking.py')

filebase='/home/rumbaugh/Downloads/WUCDC/12-8-15-1200/view-source_www.hearthpwn.com_forums_hearthstone-general_fan-creations_86577-the-winter-unveiling-a-card-design-competition'

filearr=np.zeros(30,dtype='|S200')
filearr[0]='%s.html'%filebase
for i in range(1,30): filearr[i]='%s_page=%i.html'%(filebase,i+1)

dcr=np.loadtxt('/home/rumbaugh/git/CDCranking/disqual_list_WUCDC.dat',dtype='i8')
#dcr[dcr>548]-=1
dqa=np.ones((30,20),dtype='bool')
dqf=dqa.flatten()
dqf[dcr-1]=0
dqa2=dqf.reshape((30,20))

CDCrank(filearr,disqual_flags=dqa2,top=30)
