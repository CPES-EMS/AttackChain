import networkx as nx
import time

class AttackChain:
    def __init__(self, rawData) -> None:
        self.rawData = rawData

    def checkChainTime(self, current_pos, total_pos, last_time, datadict, appendlist1, position, last_position):
        flag=0
        if current_pos >=total_pos:
            return appendlist1
        elif last_position < len(datadict[current_pos]) and current_pos >=0:
            for i in range(last_position,len(datadict[current_pos])):
                time_test = time.mktime(time.strptime(datadict[current_pos][i],"%Y-%m-%d %H:%M:%S"))
                if time_test < last_time :
                    continue
                elif (time_test-last_time) >=7200:
                    flag=1
                    break
                else:
                    appendlist1.append(i)
                    return self.checkChainTime(current_pos+1,total_pos,time_test,datadict,appendlist1,i,0)
            if flag == 1:
                return self.checkChainTime(current_pos-1,total_pos,last_time,datadict,appendlist1,i,position+1)


    def getAttackChain(self):
        num=1
        datadict = {}
        edgenumber_list=[]
        data_search=[]
        for alert in self.rawData:
            merge = alert[:2]
            if merge not in datadict:
                datadict[merge] = {'number' :1 , 'repetition' :[alert[2]] ,'category':[alert[5]]}
            else:
                datadict[merge]['number'] +=1
                datadict[merge]['repetition'].append(alert[2])
                datadict[merge]['category'].append(alert[5])

            data_search=[]
            for merge, value in datadict.items():
                data_search.append(merge)

        ## 计算最短路径
        digraph=nx.DiGraph()
        for edge in data_search:
            if(edge[0]!= None)  and (edge[1]!=None) :
                digraph.add_edge(edge[0],edge[1])
                edgeTuple=(edge[0],edge[1])
                edgenumber_list.append(edgeTuple)
        shortest_path = nx.algorithms.shortest_paths.generic.shortest_path(digraph)


        ## 为每条边赋予一个边ID
        edgeid_dic={}
        for i in range(len(edgenumber_list)):
            edgeid_dic[edgenumber_list[i]]=i+1


        ##确保告警链的长度大于等于4
        attackchain=[]
        attack_chain_edge=[]
        for key ,value in shortest_path.items():
            for k, y in value.items():
                if len(y)>=4:
                    attackchain.append(y)
                    chain=[]
                    for i in range(len(y)-1):
                        edge_id=edgeid_dic[(y[i],y[i+1])]
                        chain.append(edge_id)
                    attack_chain_edge.append(chain)


        ##将对应ip之间的告警时间和告警类型按照时间顺序对应排序
        for path in attack_chain_edge:
            for edge in path:
                time_category = zip(datadict[data_search[edge-1]]['repetition'],datadict[data_search[edge-1]]['category'])
                sorted_time_category = sorted(time_category,key = lambda x:x[0])
                time_category_split = zip(*sorted_time_category)
                sorted_time,sorted_category =[list(x) for x in time_category_split]
                datadict[data_search[edge-1]]['repetition'] = sorted_time
                datadict[data_search[edge-1]]['category'] = sorted_category


        ##确保告警链先后两跳之间的时间间隔不会超过两小时
        attack_chain_filter=[]
        answerlist=[]
        for path in attack_chain_edge:
            len_route = len(path)
            time_list = []
            category_list = []
            time_path = [[] for i in range(len_route)]
            category_path = [[] for i in range(len_route)]
            pathTime=[]
            pathCategory=[]
            alert = datadict[data_search[path[0]-1]]['repetition']
            category = datadict[data_search[path[0]-1]]['category']
            for i in range(len(alert)):
                time1 = time.mktime(time.strptime(alert[i],"%Y-%m-%d %H:%M:%S"))
                alert1 = datadict[data_search[path[1]-1]]['repetition']
                category1 = datadict[data_search[path[1]-1]]['category']
                for j in range(len(alert1)):
                    time2 = time.mktime(time.strptime(alert1[j],"%Y-%m-%d %H:%M:%S"))
                    if time2 < time1:
                        continue
                    elif (time2-time1) >=7200 :
                        break
                    else:
                        alert2 = datadict[data_search[path[2]-1]]['repetition']
                        category2 = datadict[data_search[path[2]-1]]['category']
                        for k in range(len(alert2)):
                            time3 = time.mktime(time.strptime(alert2[k],"%Y-%m-%d %H:%M:%S"))
                            if time3 < time2:
                                continue
                            elif (time3- time2) >=7200:
                                break
                            elif len_route >=4:
                                appendlist=[]
                                timelist = []
                                current_route=3
                                pos = 0
                                last_pos=0
                                for m in range(3,len_route):
                                    alert_time = datadict[data_search[path[m]-1]]['repetition']
                                    timelist.append(alert_time)
                                appendlist2=self.checkChainTime(0,len_route-current_route,time3,timelist,appendlist,pos,last_pos)
                                timelist2=[]
                                categorylist2=[]
                                if appendlist2:
                                    for m in range(3,len_route):
                                        time_a = datadict[data_search[path[m]-1]]['repetition'][appendlist2[m-3]]
                                        category_a = datadict[data_search[path[m]-1]]['category'][appendlist2[m-3]]
                                        timelist2.append(time_a)
                                        categorylist2.append(category_a)
                                    timelist2=[alert[i],alert1[j],alert2[k]] + timelist2
                                    categorylist2=[category[i],category1[j],category2[k]] + categorylist2
                                    time_list.append(timelist2)
                                    category_list.append(categorylist2)
                            else:
                                time_list.append([alert[i],alert1[j],alert2[k]])
                                category_list.append([category[i],category1[j],category2[k]])
            for i in range(len(time_list)):
                for j in range(len_route):
                    time_path[j].append(time_list[i][j])
                    category_path[j].append(category_list[i][j])
            if time_list:
                for k in range(len_route):
                    timePath = [ i for i in datadict[data_search[path[k]-1]]['repetition'] if i in time_path[k]]
                    categoryPath = [i for i in datadict[data_search[path[k]-1]]['category'] if i in category_path[k]]
                    pathTime.append(timePath)
                    pathCategory.append(categoryPath)
                path.append(pathTime)
                path.append(pathCategory)
                attack_chain_filter.append(path)
        
        attack_chain_delete=[]
        #s删除告警链中的子链部分
        for route in attack_chain_filter:
            for judge in attack_chain_filter:
                if set(route[:-2]) < set(judge[:-2]):
                    attack_chain_delete.append(route)
                    break
        attack_chain_filter1=attack_chain_filter[:]
        for route in attack_chain_filter:
            if route in attack_chain_delete:
                attack_chain_filter1.remove(route)

        for path in attack_chain_filter1:
            time_list=path[-2]
            category_list=path[-1]
            path.remove(time_list)
            path.remove(category_list)
            chainlist=[]
            for i in range(len(path)):
                Chain={
                    'time':time_list[i],
                    'source_ip':data_search[path[i]-1][0],
                    'target_ip':data_search[path[i]-1][1],
                    'attribute':list(set(category_list[i])),
                }
                chainlist.append(Chain)
            answerlist_dic={
                'number':num,
                'spanNumber':len(path),
                'first_chain':chainlist[0],
                'second_chain':chainlist[1],
                'third_chain':chainlist[2],
                'others':chainlist[3:]
            }
            answerlist.append(answerlist_dic)
            num += 1
        result={
            'attackChain' :answerlist
        }
        return result