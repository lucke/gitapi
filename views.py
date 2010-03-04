# Create your views here.

from django.http import HttpResponse

import gitapi


def index(request):
	""" En la pagina de indice, devolvemos una descripcion del funcionamiento de la API REST """
	resp_text = "Git // Mercurial API REST</br>"
	resp_text += "<hr></br>"
	resp_text += "This API recieves 2 arguments for all its operations:</br>"
	resp_text += "<ul><li>Path: Path to repository in local drive without quotes. Example: /usr/local/repository.</li><li>Op: Operation to perform. Depending on the operation chosen, more arguments may follow, as seen bellow.</li>"
	resp_text += "<ul><li>1: Get Repository Branches.</li>"
	resp_text += "<li>2: Get Repository Commits. (anyadir la paginacion)</li>"
	resp_text += "<li>3: Get Commit. Needs param \"commit\"=commit_id</li>"
	resp_text += "<li>4: Get Tree. Needs param \"tree\"=tree_id</li>"
	resp_text += "<li>5: Get Blob. Needs param \"blob\"=blob_id</li></ul>"

	return HttpResponse(resp_text)

def api(request):
	""" Por ahora vamos implementar los metodos de lectura de la API, devolvemos una respuesta JSON. Tomamos como argumento el PATH a un repositorio GIT, y que queremos leer:
        Podemos leer:
                - Branches (active branch, branches)
                - Commits  (Todos los commits, por cada commit sus atributos)
                - Tree  (arbol de "blobs" asociados a un commit)
                - Blobs (Ficheros)
                - Diff? """

	if request.method == 'GET':
		apiquery = request.GET
		operation = apiquery.__getitem__("op")
		github = apiquery.__getitem__("github")
		operation = int(operation)
		github = int(github)
		if (operation == -1):
			return HttpResponse("OK");
		if (operation == 0 and github == 0):
			return HttpResponse(gitapi.get_directory())
		elif (operation == 1 and github == 0):
	                repository = apiquery.__getitem__("repository")
			return HttpResponse(gitapi.get_branches(repository))
		elif (operation == 2 and github == 0):
	                repository = apiquery.__getitem__("repository")
			branch = apiquery.__getitem__("branch")
			page = apiquery.__getitem__("page")
			return HttpResponse(gitapi.get_commits(repository, branch, page))
		elif (operation == 3 and github == 0):
	                repository = apiquery.__getitem__("repository")
			commit = apiquery.__getitem__("commit")
			return HttpResponse(gitapi.get_head(repository,commit))
		elif (operation == 4 and github == 0):
	                repository = apiquery.__getitem__("repository")
			tree = apiquery.__getitem__("tree")
			return HttpResponse(gitapi.get_tree(repository,tree))
		elif (operation == 5 and github == 0):
	                repository = apiquery.__getitem__("repository")
			blob = apiquery.__getitem__("blob")
			return HttpResponse(gitapi.get_blob(repository,blob))
		elif (operation == 1 and github == 1):
			user = apiquery.__getitem__("user")
			repository = apiquery.__getitem__("repository")
			return HttpResponse(gitapi.get_branches_github(user, repository))
		elif (operation == 2 and github == 1):
			user = apiquery.__getitem__("user")
			repository = apiquery.__getitem__("repository")
			branch = apiquery.__getitem__("branch")
			return HttpResponse(gitapi.get_commits_github(user, repository, branch))
		elif (operation == 4 and github == 1):
			user = apiquery.__getitem__("user")
			repository = apiquery.__getitem__("repository")
			tree = apiquery.__getitem__("tree")
			return HttpResponse(gitapi.get_tree_github(user, repository, tree))
		elif (operation == 5 and github == 1):
			user = apiquery.__getitem__("user")
			repository = apiquery.__getitem__("repository")
			blob = apiquery.__getitem__("blob")
			return HttpResponse(gitapi.get_blob_github(user, repository, blob))
		else:
			return HttpResponse("Invalid arguments for the API")		


