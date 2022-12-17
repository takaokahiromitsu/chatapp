
from django.contrib import auth  # 追加
from django.shortcuts import redirect, render  # redirect を追加

from django.contrib.auth import views as auth_views  # 追加

from django.contrib.auth.decorators import login_required

from .models import User


# import の数が多くなったので、() で箇条書きにしましょう。
from .forms import (
    SignUpForm,
    LoginForm,
    # TalkForm,
    UsernameChangeForm,
    EmailChangeForm, 
)


from django.urls import reverse_lazy 


def index(request):
    return render(request, "main/index.html")



# もとの signup 関数を、以下で置き換える
def signup(request):
    if request.method == "GET":
        form = SignUpForm()
        print(form)
    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            # モデルフォームは form の値を models にそのまま格納できる
            # save() メソッドがあるので便利
            form.save()

            print(form.cleaned_data)

            # フォームから username と password を読み取る
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            # 認証情報のセットを検証するには authenticate() を利用します。
            # このメソッドは認証情報をキーワード引数として受け取ります。
            user = auth.authenticate(username=username, password=password)

            # 検証する対象はデフォルトでは username と password であり、
            # その組み合わせを個々の認証バックエンドに対して問い合わせ、
            # 認証バックエンドで認証情報が有効とされれば User オブジェクトを返します。
            # もしいずれの認証バックエンドでも認証情報が有効と判定されなければ
            # PermissionDenied エラーが送出され、None が返されます。
            # つまり、autenticate メソッドは"username"と"password"を受け取り、
            # その組み合わせが存在すればその User を返し、不正であれば None を返します。
            if user:
                # あるユーザーをログインさせる場合は、login() を利用します。
                # この関数は HttpRequest オブジェクトと User オブジェクトを受け取ります。
                # ここでの User は認証バックエンド属性を持ってる必要があり、
                # authenticate() が返す User は user.backend（認証バックエンド属性）を持つので連携可能。
                auth.login(request, user)

            return redirect("index")

    context = {"form": form}
    return render(request, "main/signup.html", context)





def login(request):
    return render(request, "main/login.html")
# Create your views here.

# クラスで書かれている
class LoginView(auth_views.LoginView):
    authentication_form = LoginForm  # ログイン用のフォームを指定
    template_name = "main/login.html"  # テンプレートを指定

@login_required
def friends(request):
    friends = User.objects.all()
    context = {
        "friends": friends
    }
    return render(request,"main/friends.html",context)

def talk_room(request, user_id):
    return render(request, "main/talk_room.html")


@login_required
def settings(request):
    return render(request, "main/settings.html")


@login_required
def username_change(request):
    if request.method == "GET":
        # instance を指定することで、指定したインスタンスのデータにアクセスできます
        form = UsernameChangeForm(instance=request.user)
    elif request.method == "POST":
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # 保存後、完了ページに遷移します
            return redirect("username_change_done")

    context = {"form": form}
    return render(request, "main/username_change.html", context)


@login_required
def username_change_done(request):
    return render(request, "main/username_change_done.html")

@login_required
def email_change(request):
    if request.method == "GET":
        form = EmailChangeForm(instance=request.user)
    elif request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("email_change_done")

    context = {"form": form}
    return render(request, "main/email_change.html", context)


@login_required
def email_change_done(request):
    return render(request, "main/email_change_done.html")

class PasswordChangeView(auth_views.PasswordChangeView):
    """Django 組み込みパスワード変更ビュー

    template_name : 表示するテンプレート
    success_url : 処理が成功した時のリダイレクト先
    """

    template_name = "main/password_change.html"
    success_url = reverse_lazy("password_change_done")


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    """Django 標準パスワード変更ビュー"""

    template_name = "main/password_change_done.html"

class LogoutView(auth_views.LogoutView):
    pass