import sys
import git
from django.utils import simplejson
from django.conf import settings

from github import *

import time
import os

def get_directory():

	path = settings.REPOSITORY_PATH
	if (path[len(path)-2] != '/'):
		path += '/'

	resp_json = []

	for listed_name in os.listdir(path):
		if os.path.isdir(path+listed_name):
			resp_json+=[listed_name]

	return simplejson.dumps(resp_json)



def get_branches(repository):

        path = settings.REPOSITORY_PATH
        if (path[len(path)-2] != '/'):
                path += '/'

	repo = git.Repo(path+repository)
	resp_json = {"active_branch": repo.active_branch, "branches":len(repo.branches)}

	i = 1
	for b in repo.branches:
		resp_json[str(i)]=b.name
		i+=1

	return simplejson.dumps(resp_json)


def get_commits(repository, branch, page):
        path = settings.REPOSITORY_PATH
        if (path[len(path)-2] != '/'):
                path += '/'

	repo = git.Repo(path+repository)
	commits = repo.commits(branch, max_count=10, skip=int(page)*10)
	n_commits = len(commits)
	resp_json = {"commits": n_commits}
	
	next_page = True
	end_pagination = repo.commits(branch, max_count=10, skip=int(page)*10+10)
	if (end_pagination == []):
		next_page = False
	resp_json["next_page"] = next_page

	i=0
	while i < n_commits:
		resp_json[str(i)]=[commits[i].id,				# id del commit
				   commits[i].tree.id,				# id del arbol asociado al commit
				   commits[i].author.name, 			# nombre del autor del codigo
				   commits[i].author.email, 			# email del autor del codigo
				   time.asctime(commits[i].authored_date), 	# fecha de creacion del codigo
				   commits[i].committer.name, 			# nombre del autor del commit
	  			   commits[i].committer.email, 			# email del autor del commit
				   time.asctime(commits[i].committed_date), 	# fecha del commit
				   commits[i].message] 				# mensaje asociado al commit
		i+=1

	return simplejson.dumps(resp_json)

def get_head(repository, commit):
        path = settings.REPOSITORY_PATH
        if (path[len(path)-2] != '/'):
                path += '/'

	repo = git.Repo(path+repository)
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


def get_tree(repository, tree_id):
        path = settings.REPOSITORY_PATH
        if (path[len(path)-2] != '/'):
                path += '/'

	repo = git.Repo(path+repository)
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


def get_blob(repository, blob_id):
        path = settings.REPOSITORY_PATH
        if (path[len(path)-2] != '/'):
                path += '/'

	repo = git.Repo(path+repository)
	blob = repo.blob(blob_id)

	resp_json = {"mime": blob.mime_type, "data": str(blob.data), "size": blob.size}

	return simplejson.dumps(resp_json)
	

def get_branches_github(user, repository):
	gh = github.GitHub()
	resp_json = {"active_branch": "master"}
	i=0
	for branchname in gh.repos.branches(user, repository):
		i+=1
		resp_json[str(i)]=branchname

	resp_json["branches"]=i
	
        return simplejson.dumps(resp_json)


def get_commits_github(user, repository, branch):
	gh = github.GitHub()

	resp_json={}
	commits = gh.commits.forBranch(user, repository, branch)

	i=0
	for commit in commits:
		i+=1
		resp_json[str(i)]=[commit.id,
				   commit.tree,
				   commit.author.name,
				   commit.author.email,
				   commit.authored_date,
				   commit.committer.name,
				   commit.committer.email,
				   commit.committed_date,
				   commit.message]

	resp_json["commits"] = i

        return simplejson.dumps(resp_json)


def get_tree_github(user, repository, tree_id):
	gh = github.GitHub()
	
	tree = gh.objects.tree(user, repository, tree_id)
        resp_json = {}

	i=0
	for name, item in tree.items():
		i+=1
		dic_item = {}
		dic_item["name"] = name
		dic_item["id"] = item.sha
		dic_item["type"] = item.type
		resp_json["node"+str(i)]=dic_item

        resp_json["length"]=i

        return simplejson.dumps(resp_json)


def get_blob_github(user, repository, blob_id):
	gh = github.GitHub()

	blob = gh.objects.raw_blob(user, repository, blob_id)

        resp_json = {"data": blob}

        return simplejson.dumps(resp_json)



