import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


def get_contributor_maintainers(path : str) :
    with open(path, 'r', encoding='utf8') as f :
        data = json.load(f)
    
    contributors_list = []
    maintainers_list = []
    for entry in range(len(data)) :
        pr = data[entry]
        contributor = pr['Meta']['PR_author']
        if contributor not in contributors_list :
            contributors_list.append(contributor) 
        
        comments = pr['original_comments']
        for i in range(len(comments)) :
            com_dict = comments[i]
            com_author = com_dict['comment_author']
            if com_author not in maintainers_list :
               maintainers_list.append(com_author) 
               
               
    return contributors_list, maintainers_list, data

def message_valence_per_contributor(table_dict, data) :
    for entry in range(len(data)) :
        pr = data[entry]
        contributor = pr['Meta']['PR_author']
        comments = pr['original_comments']
        for i in range(len(comments)) :
            com_dict = comments[i]
            com_author = com_dict['comment_author']
            sentiment = pr['valences'][i]['Sentiment']
            
            table_dict[contributor][com_author][sentiment] += 1
    
    return table_dict
        
if __name__ == "__main__" :
    table_dict = {}
    contributors_list, maintainers_list, data = get_contributor_maintainers("PR_Metrics/Spring-secu-with-authors.json")
     
  
    for contributor in contributors_list :
        table_dict[contributor] = {}
        for maintainer in maintainers_list :
            table_dict[contributor][maintainer] = {}
            table_dict[contributor][maintainer]['Positive'] = 0
            table_dict[contributor][maintainer]['Negative'] = 0
            table_dict[contributor][maintainer]['Neutral'] = 0
            
    table_dict = message_valence_per_contributor(table_dict=table_dict, data=data)
      
    matrix = []
    for i in (contributors_list) :
        row = []
        for j in (maintainers_list) :
            pos = table_dict[i][j]['Positive']
            neg = table_dict[i][j]['Negative']
            neu = table_dict[i][j]['Neutral']
            cell_value = (pos,neg,neu)
            
            row.append(cell_value)
        
        matrix.append(row)
    
    
    
    #pprint(matrix)
    i = 0
    total_interactions = []
    maintainer_interactions = []
    for row in range(len(matrix)) :
         
        pos_counter = 0
        neg_counter = 0
        neu_counter = 0
        
        
        
        for el in matrix[row] :
            #if el != (0,0,0) :
             #   i+=1
            pos_counter += el[0]
            neg_counter += el[1]
            neu_counter += el[2]
        row_interactions = (pos_counter, neg_counter, neu_counter)
        total_interactions.append(row_interactions)
                
    print(f'number of total interaction : {i}\n')
    #print(f'number of total pos : {pos_counter} | neg : {neg_counter} | neu : {neu_counter}\n')
    print(f'contrib : {len(contributors_list)} || maintain : {len(maintainers_list)}')
    
    

    
    pos_list, neg_list, neu_list = [], [], [] 
    pos_maint_list, neg_maint_list, neu_maint_list = [], [], []
    
    n = 0
    for contrib in range(len(contributors_list)) :
        
        pos_list.append(total_interactions[contrib][0])
        neg_list.append(total_interactions[contrib][1])
        neu_list.append(total_interactions[contrib][2])
        #print(f' {n} : interactions for contributors {contributors_list[contrib]} : {total_interactions[contrib]}\n')
        n +=1
        
    n = 0
    for maint in range(len(maintainers_list)) :
        #print(f' {n} : amount of messages sent by {maintainers_list[maint]} : {maintainer_interactions[maint]}\n')
        n+=1
    #plt.imshow(matrix, interpolation='none')
    #ax.set_xlim(0, len(maintainers_list))
    #ax.set_ylim(0, len(contributors_list))
    #ax.set_xticks(np.arange(len(maintainers_list)))
    #ax.set_yticks(np.arange(len(contributors_list)))
    #ax.grid()
    #plt.show()
    
    
    #x = np.arange(len(contributors_list))
#
    #plt.figure(figsize=(12, max(6, len(contributors_list)*0.4)))
#
    #plt.barh(x, pos_list, label='Positifs')
    #plt.barh(x, neg_list, left=pos_list, label='Négatifs')
    #plt.barh(x, neu_list, left=np.array(pos_list)+np.array(neg_list), label='Neutres')
#
    #plt.yticks(x, contributors_list)
    #plt.xlabel('Nombre de messages')
    #plt.title('Distribution des messages')
    #plt.legend()
    #plt.show()
    
    
    #--------------------------------------------------------------------------------------
    
    
    bleu   = "#5f6fe0"
    rouge  = "#e77657"
    vert   = "#1abc9c"

    
    
    maintainers_tuple_list = list(zip(*matrix))
    
    
    # Mainteneurs
    grouped = list(zip(*matrix))
    result = [tuple(map(sum, zip(*group))) for group in grouped]
    print(len(result))
    total = [sum(t) for t in result]
    indices = np.argsort(total)[-20:]  # Top 20
    names_top = [maintainers_list[i] for i in indices]
    result_top = [result[i] for i in indices]


    
    #contributeurs
    row_grouped = list(zip(matrix))

    
    # somme des interactions par contributeur
    result_contrib = [
        tuple(map(sum, zip(*row)))
        for row in matrix
    ]

    # total global par contributeur
    contrib_total = [sum(t) for t in result_contrib]

    # indices top 20
    contrib_indices = np.argsort(contrib_total)[-20:]

    # sélection des contributeurs
    contrib_top = [contributors_list[i] for i in contrib_indices]

    # extraire pos / neg / neu
    pos_top = [result_contrib[i][0] for i in contrib_indices]
    neg_top = [result_contrib[i][1] for i in contrib_indices]
    neu_top = [result_contrib[i][2] for i in contrib_indices]

    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=contributors_list,
        x=pos_list,
        name='Positifs',
        orientation='h',
        marker=dict(color=vert)
    ))

    fig.add_trace(go.Bar(
        y=contributors_list,
        x=neg_list,
        name='Négatifs',
        orientation='h',
        marker=dict(color=rouge)
    ))

    fig.add_trace(go.Bar(
        y=contributors_list,
        x=neu_list,
        name='Neutres',
        orientation='h',
        marker=dict(color=bleu)
    ))

    fig.update_layout(
        barmode='stack',
        height=80 * len(contrib_top),
        width = 1200,
        title="Distribution des messages reçus par les contributeurs",
        
        xaxis_title="Nombre de messages reçus",
        yaxis_title="Contributeurs",
 
        yaxis=dict(
            tickmode='linear'  
        )
    )

    fig.show()
    
    vals1 = [t[0] for t in result]
    vals2 = [t[1] for t in result]
    vals3 = [t[2] for t in result]
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=maintainers_list,
        x=vals1,
        name='Positifs',
        orientation='h',
        marker=dict(color=vert)
    ))

    fig.add_trace(go.Bar(
        y=maintainers_list,
        x=vals2,
        name='Négatifs',
        orientation='h',
        marker=dict(color=rouge)
    ))

    fig.add_trace(go.Bar(
        y=maintainers_list,
        x=vals3,
        name='Neutres',
        orientation='h',
        marker=dict(color=bleu)
    ))

    fig.update_layout(
        barmode='stack',
        height=90 * len(contrib_top),
        width = 1200,
        title="Distribution des messages envoyés par les mainteneurs",
        
        xaxis_title="Nombre de messages envoyés",
        yaxis_title="Mainteneurs",
 
        yaxis=dict(
            tickmode='linear'  
        )
    )

    fig.show()
    
    
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=contrib_top,
        x=pos_top,
        name='Positifs',
        orientation='h',
        marker=dict(color=vert)
    ))

    fig.add_trace(go.Bar(
        y=contrib_top,
        x=neg_top,
        name='Négatifs',
        orientation='h',
        marker=dict(color=rouge)
    ))

    fig.add_trace(go.Bar(
        y=contrib_top,
        x=neu_top,
        name='Neutres',
        orientation='h',
        marker=dict(color=bleu)
    ))

    fig.update_layout(
        barmode='stack',
        height=30 * len(contrib_top),
        width = 1200,
        title="Distribution des messages reçus par les contributeurs (Top 20)",
        
        xaxis_title="Nombre de messages reçus",
        yaxis_title="Contributeurs",
 
        yaxis=dict(
            tickmode='linear'  
        )
    )

    fig.show()
    
    
    vals1 = [t[0] for t in result_top]
    vals2 = [t[1] for t in result_top]
    vals3 = [t[2] for t in result_top]



    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=names_top,
        x=vals1,
        name='Positifs',
        orientation='h',
        marker=dict(color = vert)
    ))

    fig.add_trace(go.Bar(
        y=names_top,
        x=vals2,
        name='Négatifs',
        orientation='h',
        marker=dict(color=rouge)
    ))

    fig.add_trace(go.Bar(
        y=names_top,
        x=vals3,
        name='Neutres',
        orientation='h',
        marker=dict(color=bleu)
    ))

    fig.update_layout(
        barmode='stack',
        height=30 * len(names_top),
        width = 1200,  
        title="Distribution des messages envoyés par les mainteneurs (Top 20)",
        
        xaxis_title="Nombre de messages envoyés",
        yaxis_title="Mainteneurs",

        yaxis=dict(
            tickmode='linear'  
        )
    )

    fig.show()

    