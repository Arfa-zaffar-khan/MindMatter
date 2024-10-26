from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

blogs = {
    1: {
        "id": 1,
        "title": "python",
        "description": "python is high level programming language which is use for genral purpous",
    },
    2: {
        "id": 2,
        "title": "java",
        "description": "java is based on oops and it is high level programming language ",
    },
}


@csrf_exempt
@api_view(["GET", "POST"])
def createAndGetAllBlogs(request):
    if request.method == "GET":
        return JsonResponse({"blogs": list(blogs.values())}, safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        new_id = max(blogs.keys()) + 1
        new_blog = {
            "id": new_id,
            "title": data.get("title"),
            "description": data.get("description"),
        }
        blogs[new_id] = new_blog
        return JsonResponse(
            {"message": "Blog Created Successfully", "blog": new_blog}, status=201
        )


@api_view(["GET", "PUT", "DELETE"])
def getUpdateDeleteBlog(request, id):
    blog = blogs.get(id)
    if request.method == "GET":
        return JsonResponse({"blog": blog})

    elif request.method == "PUT":
        data = json.loads(request.body)
        blog.update(
            {"title": data.get("title"), "description": data.get("description")}
        )
        return JsonResponse({"message": "Blog updated successfully", "blog": blog})

    elif request.method == "DELETE":
        del blogs[id]
        return JsonResponse({"message": "Blog deleted successfully"}, status=204)
