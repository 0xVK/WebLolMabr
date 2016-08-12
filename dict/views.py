from django.shortcuts import render, redirect
from dict.models import Text, Solution
from .diff_match_patch import diff_match_patch as dmp
from django.http import HttpResponse


def show_texts(request):

    texts = Text.objects.all()
    return render(request, 'texts.html', {'texts': texts})


def write_text(request, text_id):

    text = Text.objects.get(id=text_id)

    if not request.method == 'POST':

        return render(request, template_name='write.html')

    else:

        user_text = request.POST.get('text')
        author = request.user

        s = Solution.objects.create(text=text, author=author, user_text=user_text)
        s.save()

        return redirect('/solution/{}'.format(s.id))


def solution(request, id):

    sol = Solution.objects.get(id=id)

    Dmp = dmp()
    d = Dmp.diff_main(text2=sol.text.text, text1=sol.user_text)
    Dmp.diff_cleanupSemantic(d)
    r = Dmp.diff_prettyHtml(d)
    return render(request, template_name='solution.html', context={'rez': r})


def solutions(request):

    user = request.user
    sols = Solution.objects.filter(author=user)

    return render(request, template_name='solutions.html', context={'sols': sols})





