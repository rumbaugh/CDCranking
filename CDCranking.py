import numpy as np

def CDCrank(pagefiles,outfile=None,disqual_flags=None,top=20,printavgs=False):
    compdelnums=np.zeros(0,dtype='int8')
    if np.shape(pagefiles)==(): 
        pagefiles=np.loadtxt(pagefiles,dtype='|S200')
    if disqual_flags==None:
        disqual_flags=np.ones((len(pagefiles),20),dtype='bool')
    elif np.shape(pagefiles)==():
        disqual_flags=np.loadtxt(disqual_flags,dtype='bool')
    disqual_flags[0][0]=0
    vote_arr,names_arr,score_arr=np.zeros((len(pagefiles),20),dtype='i8'),np.zeros((len(pagefiles),20),dtype='|S100'),np.zeros((len(pagefiles),20),dtype='f8')
    avgs_arr=np.zeros(len(pagefiles))
    #vote_arr,names_arr=vote_arr.flatten(),names_arr.flatten()
    addnumstmp,lastvote=np.zeros(0,dtype='i8'),np.zeros(0,dtype='i8')
    lastname=np.zeros(0,dtype='|S256')
    if printavgs: print 'Average votes per page:'
    for page in range(0,len(pagefiles)):
        curpage=open(pagefiles[page]).read()

        finddecks_temp1=curpage.split('<span class="html-attribute-name">data-rating-form-type</span>="<span class="html-attribute-value">up-down')
        delinds=np.zeros(0)
        if len(finddecks_temp1)>1:
            
            #print 'Found deck on page %i'%(page+1)
            findvotes_temp0=curpage.split('data-rating-form-type')
            for i in range(0,len(findvotes_temp0)-1):
                temparr=findvotes_temp0[i+1].split('<span class="html-attribute-value">up-down')
                if len(temparr)>1: 
                    delinds=np.append(delinds,i)
                    #print "Found it at %i"%i
        findnames_temp1=curpage.split('">/private-messages/send?recipient=')
        pagelen=len(findnames_temp1)-1
        pagenames=np.zeros(0,dtype='|S100')

        for i in range(0,pagelen):
            temparr=findnames_temp1[i+1].split('</a>')
            pagenames=np.append(pagenames,temparr[0])
        pagenames=np.append(lastname,pagenames)
        if page==29:
            pagenames=np.append(lastname,pagenames)
            lastname=pagenames[-1]
        findvotes_temp1=curpage.split('<span class="html-attribute-name">data-rating-sum</span>="<span class="html-attribute-value">')
        if len(delinds)>0:findvotes_temp1=np.delete(findvotes_temp1,delinds+1)
        pagevotes=np.zeros(0)
        for i in range(0,pagelen):
            temparr=findvotes_temp1[i+1].split('</span>')
            pagevotes=np.append(pagevotes,int(temparr[0])-1)
        pagevotes=np.append(lastvote,pagevotes)
        vote_arr[page][:pagelen],names_arr[page][:pagelen]=pagevotes[:pagelen],pagenames[:pagelen]
        if page==len(pagefiles)-1: 
            disqual_flags[page][pagelen-1:]=0
            pagevotes=np.append(pagevotes,np.zeros(20-pagelen))
        #print page,disqual_flags[page],pagevotes


        findnumstmp1=curpage.split('data-index</span>="<span class="html-attribute-value">')
        numtmp=np.zeros(0,dtype='i8')
        numdels=0
        for i in range(0,len(findnumstmp1)-1):
            findnumstmp2=findnumstmp1[i+1].split('</sp')
            numtmp=np.append(numtmp,int(findnumstmp2[0]))
        numtmp=np.append(addnumstmp,numtmp)
        num=np.arange(20*page,20*page+len(numtmp))+1
        difftmp=numtmp[:len(numtmp)]-num
        delnums=np.zeros(0,dtype='i8')
        for i in range(0,len(difftmp)):
            if difftmp[i]!=0:
                for k in range(0,difftmp[i]):
                    delnums=np.append(delnums,numtmp[i]-difftmp[i]+k)
                    compdelnums=np.append(compdelnums,numtmp[i]-difftmp[i]+k)
                numdels+=difftmp[i]
                difftmp-=difftmp[i]
        if numdels>0:
            for i in range(0,numdels):
                pagenames=np.insert(pagenames,delnums[i]-20*page-1,'DELETED')
                pagevotes=np.insert(pagevotes,delnums[i]-20*page-1,0)
                numtmp=np.insert(numtmp,delnums[i]-20*page-1,delnums[i])
        if len(pagenames)>20:
            lastname=pagenames[20:]
            lastvote=pagevotes[20:]
            addnumstmp=numtmp[20:]
        disqual_flags[page][delnums-20*page-1]=0
        score_arr[page][disqual_flags[page]]=pagevotes[disqual_flags[page]]*np.sum(disqual_flags[page])*1./np.sum(pagevotes[disqual_flags[page]])
        avgs_arr[page]=np.sum(pagevotes[disqual_flags[page]])*1./np.sum(disqual_flags[page])
        if printavgs: print '%2i - %6.2f'%(page+1,avgs_arr[page])
    if printavgs: print ' '
    print compdelnums
    sort_inds=np.argsort(-1*score_arr.flatten()[disqual_flags.flatten()])
    tot_entries=np.sum(disqual_flags)
    if outfile != None: 
        FILE=open(outfile,'w')
        FILE.write('# Rank           Name                 Page Post Votes Score Vote Avg.\n')
    print 'Rank           Name                 Page Post Votes Score Vote Avg.'
    for i in range(0,top):
        print '%4i %30s %4i %4i %4i %7.3f %7.3f'%(i+1,names_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],1+(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20,(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])%20,vote_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],score_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],avgs_arr[(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20])
        if outfile != None: FILE.write('%4i %30s %4i %4i %4i %7.3f %7.3f\n'%(i+1,names_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],1+(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20,(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])%20,vote_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],score_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],avgs_arr[(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20]))
    if outfile != None:
        for i in range(top,np.sum(disqual_flags)):
            FILE.write('%4i %30s %4i %4i %4i %7.3f %7.3f\n'%(i+1,names_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],1+(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20,(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])%20,vote_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],score_arr.flatten()[disqual_flags.flatten()][sort_inds[i]],avgs_arr[(1+np.arange(20*len(pagefiles))[disqual_flags.flatten()][sort_inds[i]])/20]))
    if outfile != None:FILE.close()
