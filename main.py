from collections import deque
# regaeghe
graph = {}
graph['Me'] = ['Alica','Piter', 'Alex']
graph['Alica'] = ['Sam', 'Katy', 'Poly']
graph['Piter'] = ['Alexander','Irina','Bob']
graph['Alex'] = ['Gorge', 'Mary', 'Caty']

def person_is_seller(name):
    if len(name) < 4:
        return True
    return False

def search_name(name):
    search_queue = deque()
    search_queue += graph[name]
    searched = []
    while search_queue:
        person = search_queue.popleft()
        if not person in searched:
            if person_is_seller(person):
                print (person + " is seller !");
                return True
            else:
                search_queue += graph[person]
                searched.append(person)
    print ("Not found seller mango!")
    return False

search_name('Me')
