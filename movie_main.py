import tkinter as tk
import tmdbsimple as tmdb
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def sentiment(text):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer=SentimentIntensityAnalyzer()
    score=analyzer.polarity_scores(text)
    return score

r = tk.Tk()
r.configure(bg="misty rose")
r.title("Movie analysis")
r.geometry('720x650')

def keyword(key):
    k=key.get()
    search = tmdb.Search()
    search.movie(query=k)
    mv=[]
    for s in search.results:
        mv.append(s['title']+'  '+str(s['id']))
    #------------------------------------------
    m_id=tk.StringVar()
    l1= tk.Label(r, text="Enter Movie ID: ",width=30,height = 2,bg = "lavender",font = ("Candara",15))
    l1.grid(row=1,column=1)
    e1 = tk.Entry(r,width=27,bd=5,textvariable=m_id)
    e1.grid(row=2, column=1,pady=10)
    a=tk.Button(r,text='Get Reviews',font=("Arial Bold", 12),activebackground='salmon',bg='lemon chiffon',height=2,width=20,command=lambda: get_review(m_id))
    a.grid(row=3,column=1,pady=10)
    #----------------------------------------------
    
    text = tk.Label(r, text="LIST OF MOVIES",bg = "#1A5276" ,fg = "WHITE",font = ("Arial Bold", 18))
    text.grid(column=0, row=4,pady=10)
    t = tk.Text(r,width=36,height=15,pady=10,bg = "azure",font = ("Candara",13))
    for x in mv:
        t.insert(tk.END,'*' + x + '\n')
    t.grid(row=5,column=0)
        
def get_review(m_id):
    id=m_id.get()
    import requests
    data=requests.get("https://api.themoviedb.org/3/movie/"+id+"/reviews?api_key=4d9c9de3bdf0d3b6837c49c086e3b190").json()
    l=[]
    for i in data['results']:
        l.append(i['content'])
    
    if l==[]:
        t = tk.Text(r,width=30,height=4,bg = "tomato",font = ("Candara",13,'bold'))
        t.insert(tk.END,'\n          NO REVIEWS AVAILABLE\n  SELECT ANY OTHER MOVIE')
        t.grid(row=5,column=1)
    else:
        rev=[]
        for i in range(len(l)):
            char_list = [l[i][j] for j in range(len(l[i])) if ord(l[i][j]) in range(65536)]
            view=''
            for j in char_list:
                view=view+j
            rev.append(view)
            
    #----------------------------------------------------------------------
    a=tk.Button(r,text='Analyze',font=("Arial Bold", 12),activebackground='salmon',bg='lemon chiffon',height=2,width=20,command=lambda: get_visual(l))
    a.grid(row=6,column=1,pady=10)
    #------------------------------------------------------------------------
    text = tk.Label(r, text="REVIEWS"+' '+'[Total='+str(len(l))+']',bg = "#1A5276" ,fg = "WHITE",font = ("Arial Bold", 18))
    text.grid(column=1, row=4,pady=10)
    t = tk.Text(r,width=80,height=15,pady=10,bg = "lavender",font = ("Candara",13))
    for i in rev:
        t.insert(tk.END,'*' + i + '\n\n')
    t.grid(row=5,column=1)
    
def get_visual(x):
    l=[]
    for i in x:
        l.append(sentiment(i))
        
    k=[]
    for i in l:
        k.append(i['compound'])
        
    p=n=nl=0
    for i in k:
        if i>=0.5:
            p+=1
        elif i>-0.5 and i<0.5:
            nl+=1
        else:
            n+=1
        
    neg=n/len(l)
    neu=nl/len(l)
    pos=p/len(l)
    
    labels=['Positive','Negative','Neutral']
    fig = matplotlib.figure.Figure(figsize=(5,5))
    a = fig.add_subplot(111)
    a.pie([pos,neg,neu],colors=['limegreen','dodgerblue','orange'],startangle=90,autopct='%1.1f%%')
    a.legend(labels,bbox_to_anchor=(1,1.1), loc="upper right")
    
    canvas = FigureCanvasTkAgg(fig, master=r)
    canvas.get_tk_widget().grid(row=5,column=2)
    canvas.draw()   

key=tk.StringVar()
text = tk.Label(r, text="ANALYSIS OF MOVIES",bg = "#1A5276" ,fg = "WHITE",font = ("Arial Bold", 22))
text.grid(column=0, row=0,pady=10)
l1= tk.Label(r, text="Enter Keyword: ",width=22,height = 2,font = ("Candara",15))
l1.grid(row=1)   
e1 = tk.Entry(r,width=27,bd=5,textvariable=key)
e1.grid(row=2, column=0,pady=10)
a=tk.Button(r,text='Get List of Movies',font=("Arial Bold", 12),activebackground='salmon',bg='lemon chiffon',height=2,width=20,command=lambda: keyword(key))
a.grid(row=3,column=0,pady=10)  

r.mainloop()