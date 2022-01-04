from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

topic_id = 4
topics = [
    {'id': 1, 'title': 'routing', 'body':'Routing is ..'},
    {'id': 2, 'title': 'view', 'body':'View is ..'},
    {'id': 3, 'title': 'model', 'body':'Model is ..'}
]

def HTMLTemplat(articleTag, id=None):
    global topics
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value = "delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        
        '''
    ol = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/"> Django </a></h1>
        <ol>
            {ol}
        <ol>
        {articleTag}
        <ul>
            <li><a href="/create/">create</a></li>
            {contextUI}
        </ul>
    </body>
    </html>
    '''

# Create your views here.
def index(request):
    article = '''
        <h2>Welcome</h2>
        Hello, Django
        '''
    return HttpResponse(HTMLTemplat(article))

def read(request, id):
    global topics
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplat(article, id))

@csrf_exempt
def create(request):
    global topic_id
    if request.method == 'GET':
        article = '''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplat(article))
    elif request.method == "POST":
        title = request.POST['title']
        body = request.POST['body']
        new_topic = {"id":topic_id, "title":title,"body":body}
        topics.append(new_topic)
        url = "/read/" + str(topic_id)
        topic_id = topic_id + 1
        return redirect(url)

@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title":topic['title'],
                    "body":topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplat(article, id))

    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic in topics:
                if topic['id'] == int(id):
                    topic['title'] = title
                    topic['body'] = body
        return redirect(f'/read/{id}')


@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        new_topic = []
        for topic in topics:
            if topic['id'] != int(id):
                new_topic.append(topic)
        topics = new_topic
        return redirect('/')