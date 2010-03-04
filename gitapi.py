import sys
import git
from django.utils import simplejson

import time


def branches(path):
	repo = git.Repo(path)
	resp_json = {"active_branch": repo.active_branch, "branches":len(repo.branches)}

	i = 1
	for b in repo.branches:
		resp_json[str(i)]=b.name
		i+=1

	return simplejson.dumps(resp_json)


#def commits(path):
#	repo = git.Repo(path)
#	commits = repo.commits()
#	n_commits = len(repo.commits())
#	resp_json = {"commits": n_commits}
#	i=0
#	while i < n_commits:
#		resp_json[str(i)]=repo.commits()[i].id
#		i+=1
#
#	return simplejson.dumps(resp_json)


def ordenar(posibles):
	no_ordenada = []
	ordenada = []
	no_ordenada = posibles
	if (len(posibles)>0):
		reciente = no_ordenada[0]
	while (len(no_ordenada)>0):
		for i in no_ordenada:
			if reciente.authored_date < i.authored_date:
				reciente = i
		no_ordenada.remove(reciente)
		ordenada += [reciente]
		if (len(no_ordenada)>0):
			reciente = no_ordenada[0]
	return ordenada


def esta(commit, posibles):
	found = False
	i=0
	while (not found and i<(len(posibles))):
		if (posibles[i].id == commit.id):
			found = True
		else:
			i+=1
	return found

# commits devuelve los 10 ultimos commits ordenados por fecha (de mas reciente a mas antiguo)
# para ello necesita guardar una lista de "posibles commits" para ver cual es mas reciente (posibles)
# el algoritmo es "anyadir" los padres del actual a posibles, calcular el mas reciente, anyadirlo a la lista, anyadir sus padres a posibles...
def commits(path):
	repo = git.Repo(path)
	head = repo.commits()[0]
	i=0
	resp_json = {"commits": 10}
	resp_json[str(i)] = head.id
	i+=1
	posibles = []
	posibles += head.parents
	while i<10:
		posibles = ordenar(posibles)
		print posibles
		if (len(posibles)>0):
			head = posibles[0]
			posibles.remove(head)
			resp_json[str(i)] = head.id
			for j in head.parents:
				if (not esta(j, posibles)):
					posibles += [j]
		i+=1
	return simplejson.dumps(resp_json)

def head(path, commit):
	repo = git.Repo(path)
	head = repo.commits(commit)[0]
	n_parents = len(head.parents)
	resp_json = {"id": head.id, "parents": n_parents}

	i=0
	while i < n_parents:
		resp_json[str(i)]=head.parents[i].id
		i+=1

	resp_json["tree"] = head.tree.id
	resp_json["author_name"] = head.author.name
	resp_json["author_email"] = head.author.email
	resp_json["fecha_creacion"] = time.asctime(head.authored_date)
	resp_json["committer_name"] = head.committer.name
	resp_json["committer_email"] = head.committer.email
	resp_json["fecha_commit"] = time.asctime(head.committed_date)
	resp_json["message"] = head.message

	return simplejson.dumps(resp_json)


def tree(path, tree_id):
	repo = git.Repo(path)
	tree = repo.tree(tree_id)

	resp_json = {}

	i=1
	for item in tree.items():
		dic_item = {}
		dic_item["name"] = item[0]
		dic_item["id"] = item[1].id
		if item[1].__class__ == tree.__class__:
			dic_item["type"]= "tree"
		else:
			dic_item["type"]= "blob"
		resp_json["node"+str(i)]=dic_item
		i+=1

	resp_json["length"]=i-1

	return simplejson.dumps(resp_json)


def blobs(path, blob_id):
	repo = git.Repo(path)
	blob = repo.blob(blob_id)

	resp_json = {"mime": blob.mime_type, "data": str(blob.data), "size": blob.size}

	return simplejson.dumps(resp_json)
	


	



