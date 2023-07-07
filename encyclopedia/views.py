from django.shortcuts import render
import markdown

from . import util

def conver_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    html_content = conver_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist" #to display with the variable message in the error html
            }) #show error page
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
            }) #show entry page
        
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q'] 
        html_content = conver_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "content": html_content
            }) #show entry page
        else:
            allEntries = util.list_entries() #aqui ponemos todas las entradas
            recommendation = [] #variable para poner la lista de las entradas sugeridas
            for entry in allEntries: 
                if entry_search.lower() in entry.lower(): #esto compara si lo que buscamos esta dentro de lo que tenemos en el listado de entradas
                    recommendation.append(entry) #agregar al listado todo lo que encontramos
            return render(request, "encyclopedia/search.html", {
                "recommendation" : recommendation
            }) 
            
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message":"Entry already exist!"
            })
        else:
            util.save_entry(title, content)
            html_content = conver_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title":title,
                "content":html_content
            })

