from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Post, Comment


def post_list(request):
    post_list = Post.objects.all()
    
    #pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page number is out of the page then show last page 
        posts = paginator.page(paginator.num_pages)
        
    
    return render(
        request,
        '../templates/list.html',
        {'posts':posts}
    )
    

# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(
#         Post,
#         status = Post.Status.PUBLISHED,
#         slug = post,
#         publish__year = year,
#         publish__month = month,
#         publish__day = day
#     )
    
#     comments = post.comments.filter(active=True)
#     form = CommentForm()
    
#     return render(
#         request,
#         '../templates/detail.html',
#         {
#             'post':post,
#             'comments':comments,
#             'form':form
#         },
        
        
#     )
    
# @require_POST
# def post_comment(request, post_id):
#     post = get_object_or_404(
#         Post,
#         id=post_id,
#         status = Post.Status.PUBLISHED
#     )
#     comment = None
#     form = CommentForm(date=request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.save()
    
#     return render(
#         request,
#         "../templates/comment.html",
#         {
#             'post': post,
#             'form': form,
#             'comment':comment
#         }
#     )



def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(request.path_info)  # prevent form resubmission on reload
    else:
        form = CommentForm()

    return render(
        request,
        "../templates/detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": form,
            "new_comment": new_comment
        }
    )
