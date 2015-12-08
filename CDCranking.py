import numpy as np

def CDCrank(pagefiles,outfile=None,disqual_flags=None,top=20):
    if np.shape(pagefiles)==(): 
        pagefiles=np.loadtxt(pagefiles,dtype='|S200')
    if disqual_flags==None:
        disqual_flags=np.ones((len(pagefiles),20),dtype='bool')
    elif np.shape(pagefiles)==():
        disqual_flags=np.loadtxt(disqual_flags,dtype='bool')
    disqual_flags[0][0]=0
    vote_arr,names_arr,score_arr=np.zeros((len(pagefiles),20),dtype='i8'),np.zeros((len(pagefiles),20),dtype='|S100'),np.zeros((len(pagefiles),20),dtype='f8')
    avgs_arr=np.zeros(len(pagefiles))
    for page in range(0,len(pagefiles)):
        curpage=open(pagefiles[page]).read()
        finddecks_temp1=curpage.split('<span class="html-attribute-name">data-rating-form-type</span>="<span class="html-attribute-value">up-down')
        delinds=np.zeros(0)
        if len(finddecks_temp1)>1:
            findvotes_temp0=curpage.split('data-rating-form-type')
            for i in range(1,len(finddecks_temp1)):
                temparr=findvotes_temp0[i+1].split('<span class="html-attribute-name">data-rating-form-type</span>="<span class="html-attribute-value">up-down')
                if len(temparr)>1: delinds=np.append(delinds,i)
        findnames_temp1=curpage.split('">/private-messages/send?recipient=')
        if len(delinds)>0:findnames_temp1=np.delete(findnames_temp1,delinds)
        pagelen=len(findnames_temp1)-1
        pagenames=np.zeros(0,dtype='|S100')
        for i in range(0,pagelen):
            temparr=findnames_temp1[i+1].split('</a>')
            pagenames=np.append(pagenames,temparr[0])
        findvotes_temp1=curpage.split('<span class="html-attribute-name">data-rating-sum</span>="<span class="html-attribute-value">')
        if len(delinds)>0:findvotes_temp1=np.delete(findvotes_temp1,delinds)
        pagevotes=np.zeros(0)
        for i in range(0,pagelen):
            temparr=findvotes_temp1[i+1].split('</span>')
            pagevotes=np.append(pagevotes,int(temparr[0])-1)
        vote_arr[page][:pagelen],names_arr[page][:pagelen]=pagevotes,pagenames
        if page==len(pagefiles)-1: 
            disqual_flags[page][pagelen-1:]=0
            pagevotes=np.append(pagevotes,np.zeros(20-pagelen))
        #print page,disqual_flags[page],pagevotes
        score_arr[page][disqual_flags[page]]=pagevotes[disqual_flags[page]]*np.sum(disqual_flags[page])*1./np.sum(pagevotes[disqual_flags[page]])
        avgs_arr[page]=np.sum(pagevotes[disqual_flags[page]])*1./np.sum(disqual_flags[page])
    sort_inds=np.argsort(-1*score_arr.flatten()[disqual_flags.flatten()])
    tot_entries=np.sum(disqual_flags)
    if outfile != None: 
        FILE=open(outfile,'w')
        FILE.write('# Rank           Name                 Page Post Votes Score Vote Avg.\n')
    print 'Rank           Name                 Page Post Votes Score Vote Avg.'
    for i in range(0,top):
        print '%4i %30s %4i %4i %4i %7.3f %7.3f'%(i+1,names_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],1+(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20,(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])%20,vote_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],score_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],avgs_arr[(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20])
        if outfile != None: FILE.write('%4i %30s %4i %4i $4i %7.3 %7.3\n'%(i+1,names_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],1+(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20,(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])%20,vote_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],score_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],avgs_arr[(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20]))
    if outfile != None:FILE.close()
