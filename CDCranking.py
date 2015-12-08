import numpy as np

def CDCrank(pagefiles,outfile=None,disqual_flags=None,top=20):
    if np.shape(pagefiles)==(): 
        pagefiles=np.loadtxt(pagefiles,dtype='|S8')
    if disqual_flags==None:
        disqual_flags=np.ones((len(pagefiles),20),dtype='bool')
    elif np.shape(pagefiles)==():
        disqual_flags=np.loadtxt(disqual_flags,dtype='bool')
    disqual_flags[0][0]=0
    vote_arr,names_arr,score_arr=np.zeros((len(pagefiles),20),dtype='i8'),np.zeros((len(pagefiles),20),dtype='|S8'),np.zeros((len(pagefiles),20),dtype='f8')
    avgs_arr=np.zeros(len(pagefiles))
    for page in range(0,len(pagefiles)):
        curpage=open(page).read()
        findnames_temp1=curpage.split('">/private-messages/send?recipient=')
        pagelen=len(findnames_temp1)-1
        pagenames=np.zeros(0,dtype='|S8')
        for i in range(0,pagelen):
            temparr=findnames_temp1[i+1].split('</a>')
            pagenames[i]=temparr[0]
        findvotes_temp1=curpage.split('<span class="html-attribute-name">data-rating-sum</span>="<span class="html-attribute-value">')
        pagevotes=np.zeros(0)
        for i in range(0,pagelen):
            temparr=findvotes_temp1[i+1].split('</span>')
            pagevotes[i]=int(temparr[0])-1
        if page==len(pagefiles)-1: disqual_flags[page][pagelen:]=0
        vote_arr[page],names_arr[page]=pagevotes,pagenames
        score_arr[page][disqual_flags[page]]=pagevotes*np.sum(disqual_flags[page])*1./np.sum(pagevotes)
        avgs_arr[page]=np.sum(pagevotes)*1./np.sum(disqual_flags[page])
    sort_inds=np.argsort(-1*score_arr.flatten()[disqual_flags.flatten()])
    tot_entries=np.sum(disqual_flags)
    if outfile != None: 
        FILE=open(outfile,'w')
        FILE.write('# Rank Name                           Page Post Votes Score Vote Avg.\n')
    print 'Rank Name                           Page Post Votes Score Vote Avg.'
    for i in range(0,top):
        print '%4i %30s %4i %4i %7.3 %7.3'%(i,names_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],1+(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20,20%(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]]),votes_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],score_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],avgs_arr[(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20])
        if outfile != None: FILE.write('%4i %30s %4i %4i %7.3 %7.3\n'%(i,names_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],1+(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20,20%(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]]),votes_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],score_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],avgs_arr[(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20]))
    FILE.close()
